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


def build_radar_url_and_time() -> Tuple[str, str]:
    """
    Recreate your filename pattern from weather.gov.sg based on get_time.get_time().
    """
    year_now, month_now, day_now, hour_now, minute_split = get_time.get_time()
    url = (
        "http://www.weather.gov.sg/files/rainarea/50km/v2/"
        f"dpsri_70km_{year_now}{month_now}{day_now}{hour_now}{minute_split[1]}{minute_split[0]}0000dBR.dpsri.png"
    )
    image_time = f"{year_now}-{month_now}-{day_now} {hour_now}:{minute_split[1]}{minute_split[0]}"
    return url, image_time

def fetch_radar_image() -> Tuple[Image.Image, str]:
    """
    Fetch radar image. If the latest frame fails to open, fall back to the previous
    successful image kept in session state.
    """
    url, image_time = build_radar_url_and_time()
    try:
        resp = requests.get(url, timeout=12)
        resp.raise_for_status()
        img = Image.open(io.BytesIO(resp.content)).convert("RGBA")
        # Keep last successful frame in session (acts like your previous_radar_image.png)
        st.session_state["previous_frame"] = resp.content
        st.session_state["previous_time"] = image_time
        return img, image_time
    except (requests.RequestException, UnidentifiedImageError, OSError):
        # Fallback to last good frame
        if "previous_frame" in st.session_state:
            img = Image.open(io.BytesIO(st.session_state["previous_frame"])).convert("RGBA")
            return img, st.session_state.get("previous_time", "Unknown time (cached)")
        else:
            # As a last resort, raise a clean error for the UI
            raise RuntimeError("No radar frame available yet (network/cache empty).")


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
            st.error(f"Could not load radar image. {e} {image_time}")
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



