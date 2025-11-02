# app.py
import io
from typing import Dict, List, Tuple
import requests
import cv2
from PIL import Image, ImageFile, UnidentifiedImageError
import streamlit as st
import streamlit.components.v1 as components
import base64
from datetime import datetime, timedelta, timezone

# ==== your modules (kept as-is) ====
from weather_colour_check import colour_dict               # expects: dict[str, tuple[int,int,int]]
from location_grid import location_grids                   # expects: fn(Image) -> dict[str, list[(r,g,b)]]
from nowcast_weather import nowcast_weather                # expects: fn(dict[str,str], image_time:str) -> Optional[path or None]
# from alarm_ui import Alarm_UI                            # replaced by Streamlit alarm panel
import get_time                                            # expects: fn() -> (YYYY, MM, DD, HH, [min_tens, min_ones])

st.set_page_config(page_title="SG Rain Nowcast", page_icon="🌧️", layout="wide")


# ========================
# Helpers from your script
# ========================
def is_rain_detected(nowcast: dict[str, str]) -> bool:
    # any region with Showers / Thundery Showers
    return any(c in ("Showers", "Thundery Showers") for c in nowcast.values())


def render_alarm_audio(src: str):
    # Looping audio element; JS ensures immediate play on re-runs.
    components.html(
        f"""
        <audio id='alarm' autoplay loop>
          <source src='{src}'>
        </audio>
        <script>
          const a = document.getElementById('alarm');
          if (a) {{
            const tryPlay = () => a.play().catch(() => setTimeout(tryPlay, 400));
            tryPlay();
          }}
        </script>
        """,
        height=0,
    )


def file_to_data_url(path: str) -> str:
    # turn a small wav/mp3 in your repo into a data: URL so it works on cloud
    mime = "audio/wav" if path.lower().endswith(".wav") else "audio/mpeg"
    with open(path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode("ascii")
    return f"data:{mime};base64,{b64}"


def color_difference(color1, color2) -> int:
    """Calculate difference as sum of per-channel absolute differences."""
    return sum(abs(a - b) for a, b in zip(color1, color2))


def get_color_name(color) -> str:
    """Guess name using the closest match from colour_dict."""
    diffs = [[color_difference(color, known_color), known_name]
             for known_name, known_color in colour_dict.items()]
    diffs.sort()
    return diffs[0][1]


# --- replace these two functions in app.py ---
ImageFile.LOAD_TRUNCATED_IMAGES = True  # tolerate partial images

def round_down_to_5min(dt: datetime) -> datetime:
    """Return dt rounded down to the nearest 5-minute mark."""
    minute = (dt.minute // 5) * 5
    return dt.replace(minute=minute, second=0, microsecond=0)

def build_radar_url_and_time(ts: datetime) -> tuple[str, str]:
    """Construct the radar PNG URL for a given UTC+8 timestamp."""
    sg = timezone(timedelta(hours=8))
    ts = ts.astimezone(sg)
    ts = round_down_to_5min(ts)  # <-- round down to nearest 5 min

    year  = ts.strftime("%Y")
    month = ts.strftime("%m")
    day   = ts.strftime("%d")
    hour  = ts.strftime("%H")
    minute= ts.strftime("%M")

    url = (
        "https://www.weather.gov.sg/files/rainarea/50km/v2/"
        f"dpsri_70km_{year}{month}{day}{hour}{minute}0000dBR.dpsri.png"
    )
    image_time = ts.strftime("%Y-%m-%d %H:%M")
    return url, image_time

@st.cache_data(ttl=300, show_spinner=False)
def _download_image_bytes(url: str) -> bytes:
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Referer": "https://www.weather.gov.sg/",
        "Accept": "image/*,*/*;q=0.8",
    }
    r = requests.get(url, headers=headers, timeout=15, allow_redirects=True)
    r.raise_for_status()
    if "image" not in (r.headers.get("Content-Type") or "").lower():
        raise ValueError("Non-image response.")
    return r.content

def fetch_radar_image() -> tuple[Image.Image, str]:
    """Try the rounded-down time first, then walk back 5 min steps if needed."""
    sg_now = round_down_to_5min(datetime.now(timezone(timedelta(hours=8))))
    attempts = 4  # now, -5m, -10m, -15m

    last_error = None
    for i in range(attempts):
        ts = sg_now - timedelta(minutes=5 * i)
        url, image_time = build_radar_url_and_time(ts)
        try:
            data = _download_image_bytes(url)
            img = Image.open(io.BytesIO(data)).convert("RGBA")
            st.session_state["previous_frame"] = data
            st.session_state["previous_time"] = image_time
            return img, image_time
        except Exception as e:
            last_error = e
            continue

    # fallback
    if st.session_state.get("previous_frame"):
        img = Image.open(io.BytesIO(st.session_state["previous_frame"])).convert("RGBA")
        return img, st.session_state.get("previous_time", "Unknown (cached)")

    raise RuntimeError(f"No radar frame found (last error: {last_error})")


def classify_nowcast_by_grid(weather_image: Image.Image) -> Dict[str, str]:
    """
    1) Split image into your location grids (provided by your module).
    2) Convert RGB medians to your named color classes.
    3) Map those classes to human-friendly nowcast strings.
    """
    grids: Dict[str, List[Tuple[int, int, int]]] = location_grids(weather_image)

    for key, values in grids.items():
        for i in range(len(values)):
            values[i] = get_color_name(values[i])

    weather_nowcast: Dict[str, str] = {}
    for key, values in grids.items():
        # Preserve your original priority logic
        if 'heavy_tsra_colour' in values:
            weather_nowcast[key] = 'Thundery Showers'
        elif 'tsra_colour' in values:
            weather_nowcast[key] = 'Thundery Showers'
        elif 'light_tsra_colour' in values:
            weather_nowcast[key] = 'Thundery Showers'
        elif 'showers_colour' in values:
            weather_nowcast[key] = 'Showers'
        elif 'light_showers_colour' in values:
            weather_nowcast[key] = 'Showers'
        elif 'partly_cloudy' in values:
            weather_nowcast[key] = 'Partly Cloudy'

    return weather_nowcast


def render_alarm_panel(nowcast: Dict[str, str]) -> None:
    """
    Light-weight replacement for Alarm_UI:
    - Shows a summary banner if any region has rain/TS.
    - Lists regions grouped by condition.
    """
    if not nowcast:
        st.info("No significant weather detected in the monitored grids.")
        return

    groups: Dict[str, List[str]] = {}
    for loc, cond in nowcast.items():
        groups.setdefault(cond, []).append(loc)

    if any(cond in ("Thundery Showers", "Showers") for cond in groups):
        st.warning("Rain detected in one or more regions. See details below.")

    for cond, locs in groups.items():
        with st.expander(f"{cond} — {len(locs)} area(s)", expanded=(cond != "Partly Cloudy")):
            st.write(", ".join(sorted(locs)))


# ================
# Streamlit UI
# ================
def main():
    st.title("Singapore Rain Nowcast (Radar-based) 🌧️")
    st.caption("Wrap of automated nowcast for Streamlit with auto-refresh, caching, and UI alarms.")

    # Sidebar controls
    with st.sidebar:
        st.header("Controls")
        refresh_secs = st.slider("Auto-refresh (seconds)", 0, 600, 300)
        manual = st.button("Fetch now")
    
        st.divider()
        # 👇 User gesture so browsers allow audio autoplay
        st.checkbox("Enable alarm sound", key="alarm_enabled",
                    help="Required by browsers to allow autoplay with audio.")
    
        # Stop button to silence ongoing alarm
        if st.button("Stop alarm"):
            st.session_state["not_stopped"] = False
            st.toast("🔕 Alarm stopped (will stay silent until after the next refresh)")
    
        # Auto refresh (if enabled)
        if refresh_secs > 0:
            try:
                from streamlit_autorefresh import st_autorefresh
                st_autorefresh(interval=refresh_secs * 1000, key="auto-refresh")
            except ImportError:
                st.info(
                    "Auto-refresh requires the package 'streamlit-autorefresh'. Run `pip install streamlit-autorefresh`.")
    
    # Columns for layout
    col1, col2 = st.columns([1.2, 1])

    # Prepare base image
    base_img = Image.open("base-sg.png").convert("RGBA")

    # Fetch & render radar
    with col1:
        st.subheader("Latest Radar Frame")
        try:
            if manual or refresh_secs > 0 or "previous_frame" not in st.session_state:
                image, image_time = fetch_radar_image()
                img_for_overlay = image.resize(base_img.size, Image.BILINEAR)
                overlay = base_img.copy()
                overlay.alpha_composite(img_for_overlay)
            else:
                # Use cached previous frame to avoid repeated network on first paint
                image = Image.open(io.BytesIO(st.session_state["previous_frame"])).convert("RGBA")
                img_for_overlay = image.resize(base_img.size, Image.BILINEAR)
                overlay = base_img.copy()
                overlay.alpha_composite(img_for_overlay)
                image_time = st.session_state.get("previous_time", "Unknown")
            st.image(overlay, caption=f"Radar time: {image_time}", use_container_width=True)
        except Exception as e:
            st.error(f"Could not load radar image. {e}")
            return

    # Classify & show nowcast
    with col2:
        st.subheader("Nowcast (by grid)")
        nowcast = classify_nowcast_by_grid(image)

                # Init session flags once
        st.session_state.setdefault("alarm_active", False)
        st.session_state.setdefault("was_raining", False)
        st.session_state.setdefault("not_stopped", True)
        
        # Detect rain this run
        raining_now = any(c in ("Showers", "Thundery Showers") for c in nowcast.values())
        was_raining = st.session_state["was_raining"]
  
        # Decide when to arm the alarm:
        # - Arm on transition dry→rain (recommended), OR use `if raining_now:` to arm any time it’s raining.
        if raining_now and st.session_state.get("alarm_enabled"):
            st.session_state["alarm_active"] = True
            st.toast("🔊 Rain detected — alarm armed", icon="🌧️")
        
        # If alarm is active, render looping audio every rerun until stopped
        if st.session_state["alarm_active"] and st.session_state.get("alarm_enabled") and st.session_state.get("not_stopped"):
            try:
                src = file_to_data_url("RingIn.wav")  # or use a hosted URL
                render_alarm_audio(src)
                st.caption("Alarm is **ringing** (looping) — press **Stop alarm** in the sidebar to silence.")
            except Exception as e:
                st.error(f"Alarm sound error: {e}")
        
        # Update for next run
        st.session_state["was_raining"] = raining_now
        st.session_state["alarm_active"] = False
        st.session_state["not_stopped"] = True
        
        #         # ===== Alarm logic =====
        # raining_now = is_rain_detected(nowcast)
        # was_raining = st.session_state.get("was_raining", False)
        
        # # Decide when to ring:
        # # - ring on transition (no rain -> rain), OR
        # # - ring every refresh while raining if you prefer (toggle the condition below)
        # # should_ring = (not was_raining and raining_now)  # transition-only
        # should_ring = raining_now  # <-- uncomment to ring every refresh while raining
        
        # if raining_now:
        #     st.warning("Rain detected in one or more regions.")
        # else:
        #     st.info("No rain detected in monitored grids.")
        
        # # Play sound if allowed by user + we should ring
        # if st.session_state.get("alarm_enabled") and should_ring:
        #     try:
        #         # Prefer an embedded data: URL so it works on Streamlit Cloud
        #         src = file_to_data_url("RingIn.wav")  # or host at /alarm.wav and use plain "alarm.wav"
        #         play_alarm(src)
        #         st.toast("🔊 Alarm rang (rain detected).")
        #     except Exception as e:
        #         st.error(f"Alarm sound error: {e}")
        
        # # remember state for next refresh
        # st.session_state["was_raining"] = raining_now
        
        # Optional: write out nowcast overlay/asset using your function
        try:
            _out = nowcast_weather(nowcast, image_time)  # if it saves an image, great
        except Exception:
            # non-fatal: your function might save to disk; ignore if unavailable in cloud
            _out = None

        if _out:
            try:
                if isinstance(_out, str):
                    st.image(_out, caption="Generated Nowcast Overlay", use_container_width=True)
                elif isinstance(_out, Image.Image):
                    st.image(_out, caption="Generated Nowcast Overlay", use_container_width=True)
            except Exception:
                pass

        # Alarm panel (replacement for Alarm_UI)
        render_alarm_panel(nowcast)

        # Download nowcast as CSV
        if nowcast:
            import pandas as pd
            df = pd.DataFrame(
                [{"Location": loc, "Condition": cond} for loc, cond in sorted(nowcast.items())]
            )
            st.dataframe(df, use_container_width=True, hide_index=True)
            st.download_button(
                "Download nowcast CSV",
                df.to_csv(index=False).encode(),
                file_name=f"nowcast_{image_time.replace(':','')}.csv",
                mime="text/csv"
            )
        else:
            st.info("No locations flagged.")


if __name__ == "__main__":
    # Initialize session fallbacks for the very first run
    st.session_state.setdefault("previous_frame", None)
    st.session_state.setdefault("previous_time", None)
    main()




















