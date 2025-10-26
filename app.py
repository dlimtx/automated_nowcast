# app.py
import io
from typing import Dict, List, Tuple
import requests
import cv2
from PIL import Image, UnidentifiedImageError
import streamlit as st

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

from datetime import datetime, timedelta, timezone
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True  # tolerate partial images from the wire

def build_radar_url_and_time(ts: datetime) -> Tuple[str, str]:
    """
    Build the weather.gov.sg 70km dBR radar URL for a given UTC+8 timestamp.
    The filename uses yyyyMMddHHmm0000 (with mm as minute, zero-padded).
    """
    # Make sure we work in local SG time (UTC+8)
    sg = timezone(timedelta(hours=8))
    ts = ts.astimezone(sg)

    year_now  = ts.strftime("%Y")
    month_now = ts.strftime("%m")
    day_now   = ts.strftime("%d")
    hour_now  = ts.strftime("%H")
    minute    = ts.strftime("%M")           # e.g. "07", "12", etc.

    # The site hosts PNGs under HTTPS and v2 path
    # Example: https://www.weather.gov.sg/files/rainarea/50km/v2/dpsri_70km_2025102613070000dBR.dpsri.png
    url = (
        "https://www.weather.gov.sg/files/rainarea/50km/v2/"
        f"dpsri_70km_{year_now}{month_now}{day_now}{hour_now}{minute}0000dBR.dpsri.png"
    )
    image_time = f"{year_now}-{month_now}-{day_now} {hour_now}:{minute}"
    return url, image_time

@st.cache_data(ttl=300, show_spinner=False)
def _download_image_bytes(url: str) -> bytes:
    headers = {
        # Some CDNs block default python UA; a browsery UA avoids 403/5xx HTML pages
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                      "(KHTML, like Gecko) Chrome/120.0 Safari/537.36",
        # weather.gov.sg sometimes expects a same-site referer
        "Referer": "https://www.weather.gov.sg/",
        "Accept": "image/*,*/*;q=0.8",
    }
    r = requests.get(url, headers=headers, timeout=15, allow_redirects=True)
    r.raise_for_status()

    ct = (r.headers.get("Content-Type") or "").lower()
    if "image" not in ct:
        # The “image” is likely HTML text (403/redirect/login). Bubble up a helpful error.
        snippet = r.content[:200].decode("utf-8", errors="ignore")
        raise ValueError(f"Non-image response ({ct}). First bytes: {snippet!r}")

    if not r.content:
        raise ValueError("Downloaded 0 bytes.")

    return r.content

def fetch_radar_image() -> Tuple[Image.Image, str]:
    """
    Try the current timestamp, then walk back in 5-minute steps (up to 4 tries)
    to survive minor publication delays. Cache last-good frame in session.
    """
    # Start from 'now' in SG time; radar is typically 5-minute cadence
    sg_now = datetime.now(timezone(timedelta(hours=8)))
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

    # Fallback to cached frame if available
    if "previous_frame" in st.session_state and st.session_state["previous_frame"]:
        img = Image.open(io.BytesIO(st.session_state["previous_frame"])).convert("RGBA")
        return img, st.session_state.get("previous_time", "Unknown time (cached)")

    raise RuntimeError(f"No radar frame available (tried {attempts} steps). Last error: {last_error}")


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
        refresh_secs = st.slider("Auto-refresh (seconds)", min_value=0, max_value=600, value=300,
                                 help="0 disables auto-refresh. Typical radar cadence is ~5–10 minutes.")
        manual = st.button("Fetch now")
        st.divider()
        st.subheader("About")
        st.markdown(
            "- Uses **weather.gov.sg** radar imagery\n"
            "- Classifies grid colours via your `colour_dict`\n"
            "- Replaces `Alarm_UI` with a Streamlit alarm panel"
        )

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





