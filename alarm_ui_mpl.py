# alarm_ui_mpl.py (fixed)
import os
import sys
import winsound
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.widgets import Button

FONT = {"fontsize": 12, "fontstyle": "italic"}
THEME_COLOR = "#375362"

def continue_clicked(_event=None):
    winsound.PlaySound(None, winsound.SND_PURGE)

class Alarm_UI_MPL:
    def __init__(self, weather_nowcast_dict):
        self.alarm_on = None
        self.weather_nowcast_dict = weather_nowcast_dict
        self.close_timer = None
        self.stopped = False

        self.fig = plt.figure(figsize=(9, 6))
        try:
            self.fig.canvas.manager.set_window_title("Weather Alarm")
        except Exception:
            pass  # some backends don't support set_window_title

        self.ax_img = self.fig.add_axes([0.05, 0.25, 0.90, 0.70])
        self.ax_img.set_xticks([]); self.ax_img.set_yticks([])
        self.ax_img.set_facecolor(THEME_COLOR)

        self.weather_text_artist = self.ax_img.text(
            0.5, 1.02, "No significant weather",
            ha="center", va="bottom", color="white", transform=self.ax_img.transAxes, **FONT
        )

        # Buttons
        self.ax_alarm   = self.fig.add_axes([0.05, 0.12, 0.20, 0.08])
        self.ax_snooze  = self.fig.add_axes([0.27, 0.12, 0.20, 0.08])
        self.ax_refresh = self.fig.add_axes([0.49, 0.12, 0.20, 0.08])
        self.ax_stop    = self.fig.add_axes([0.71, 0.12, 0.20, 0.08])
        for a in (self.ax_alarm, self.ax_snooze, self.ax_refresh, self.ax_stop):
            a.set_facecolor("#dfe6e9")

        # Alarm status file
        try:
            with open("alarm_status.txt") as f:
                raw = f.read().strip()
        except FileNotFoundError:
            raw = "No"
        self.alarm_on = (raw == "Yes")

        self.btn_alarm = Button(self.ax_alarm, "Alarm: On" if self.alarm_on else "Alarm: Off")
        self.btn_alarm.on_clicked(self.change_alarm_status)

        self.btn_snooze = Button(self.ax_snooze, "Snooze Alarm")
        self.btn_snooze.on_clicked(continue_clicked)

        self.btn_refresh = Button(self.ax_refresh, "Refresh Page")
        self.btn_refresh.on_clicked(self.refresh_nowcast)

        self.btn_stop = Button(self.ax_stop, "Stop Monitoring")
        self.btn_stop.on_clicked(lambda event: self._exit_app())

        self._draw_nowcast_image()
        self._evaluate_nowcast_and_notify()

        # Auto-close after 5 minutes
        self.close_timer = self.fig.canvas.new_timer(interval=300_000)
        self.close_timer.add_callback(self._on_auto_close)
        self.close_timer.start()

        # Ensure sound stops if window is closed by user
        self.fig.canvas.mpl_connect("close_event", self._on_close)

        plt.show()

    # ---- helpers

    def _on_auto_close(self):
        # Only act if the figure still exists
        if self.stopped or not plt.fignum_exists(self.fig.number):
            return
        self._exit_app()

    def _draw_nowcast_image(self):
        if not plt.fignum_exists(self.fig.number):  # guard against late callbacks
            return
        self.ax_img.clear()
        self.ax_img.set_xticks([]); self.ax_img.set_yticks([])
        self.ax_img.set_facecolor(THEME_COLOR)
        try:
            img = mpimg.imread("nowcast_image.png")
            self.ax_img.imshow(img)
        except FileNotFoundError:
            self.ax_img.text(
                0.5, 0.5, "nowcast_image.png not found",
                ha="center", va="center", color="white", transform=self.ax_img.transAxes, **FONT
            )
        self.weather_text_artist = self.ax_img.text(
            0.5, 1.02, self.weather_text_artist.get_text(),
            ha="center", va="bottom", color="white", transform=self.ax_img.transAxes, **FONT
        )
        self.fig.canvas.draw_idle()

    def _evaluate_nowcast_and_notify(self):
        tsra_alert = False
        showers_alert = False
        weather_area = []

        for key, value in self.weather_nowcast_dict.items():
            if value == "Thundery Showers":
                tsra_alert = True
                weather_area.append(key)
            elif value == "Showers":
                showers_alert = True
                weather_area.append(key)

        if tsra_alert:
            area = "many townships" if len(weather_area) > 6 else ", ".join(weather_area)
            self.weather_present("Thundery showers", area)
        elif showers_alert:
            area = "many townships" if len(weather_area) > 6 else ", ".join(weather_area)
            self.weather_present("Showers", area)
        else:
            continue_clicked()
            self._set_weather_text("No significant weather")

    def _set_weather_text(self, text):
        if not plt.fignum_exists(self.fig.number):
            return
        self.weather_text_artist.set_text(text)
        self.fig.canvas.draw_idle()

    def weather_present(self, weather_type, location):
        self._set_weather_text(f"{weather_type} observed at {location}")
        if self.alarm_on and not self.stopped:
            winsound.PlaySound("RingIn.wav", winsound.SND_LOOP | winsound.SND_ASYNC)

    def change_alarm_status(self, _event=None):
        if self.stopped:
            return
        if self.alarm_on:
            self.alarm_on = False
            self.btn_alarm.label.set_text("Alarm: Off")
            with open("alarm_status.txt", "w") as f:
                f.write("No")
            winsound.PlaySound(None, winsound.SND_PURGE)
        else:
            self.alarm_on = True
            self.btn_alarm.label.set_text("Alarm: On")
            with open("alarm_status.txt", "w") as f:
                f.write("Yes")
        self.fig.canvas.draw_idle()

    def refresh_nowcast(self, _event=None):
        if self.stopped:
            return
        # close current UI and relaunch your main script
        self._cleanup_only()
        try:
            os.startfile("main.py")  # Windows
        except AttributeError:
            os.system("python main.py")

    def _on_close(self, _event=None):
        # If user clicks the window 'X'
        self._cleanup_only()

    # --- shutdown helpers
    def _cleanup_only(self):
        if self.stopped:
            return
        self.stopped = True
        try:
            winsound.PlaySound(None, winsound.SND_PURGE)
        except Exception:
            pass
        if self.close_timer is not None:
            try:
                self.close_timer.stop()
            except Exception:
                pass
        try:
            plt.close(self.fig)
        except Exception:
            pass

    def _exit_app(self):
        # Full stop: cleanup, close all figures, then exit process so nothing can recreate the window
        self._cleanup_only()
        try:
            plt.close('all')
        finally:
            # If you're running this inside a notebook or an IDE that shouldn't exit,
            # you can comment out the next two lines. For a standalone script, it's best to exit.
            sys.exit(0)
