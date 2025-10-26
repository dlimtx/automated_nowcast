from tkinter import *
import winsound
import os

FONT = ("Arial", 12, "italic")
THEME_COLOR = "#375362"


def continue_clicked():
    winsound.PlaySound(None, winsound.SND_PURGE)


class Alarm_UI:

    def __init__(self, weather_nowcast_dict):
        self.alarm_on = None
        self.continue_button = None
        self.window = Tk()
        self.window.title("Weather Alarm")
        self.window.config(padx=20, pady=20, bg=THEME_COLOR)

        self.weather_text = Label(text="No significant weather", fg="white", bg=THEME_COLOR, font=FONT)
        self.weather_text.grid(row=1, column=0, columnspan=5)

        self.stop_button = Button(text="Stop Monitoring", command=exit)
        self.stop_button.grid(row=0, column=4)
        with open("alarm_status.txt") as file:
            if file.read() == "Yes":
                self.alarm_on = True
                alarm_button_text = "Alarm: On"
            else:
                self.alarm_on = False
                alarm_button_text = "Alarm: Off"

        self.alarm_button = Button(text=alarm_button_text, command=self.change_alarm_status)
        self.alarm_button.grid(row=0, column=0)

        self.refresh_button = Button(text="Refresh Page", command=self.refresh_nowcast)
        self.refresh_button.grid(row=0, column=2)

        nowcast_image = PhotoImage(file="nowcast_image.png")
        self.image_label = Label(image=nowcast_image)
        self.image_label.grid(row=2, column=0, columnspan=5)

        tsra_alert = False
        showers_alert = False
        weather_area = []

        for key, value in weather_nowcast_dict.items():
            if value == "Thundery Showers":
                tsra_alert = True
                weather_area.append(key)
            elif value == "Showers":
                showers_alert = True
                weather_area.append(key)

        if tsra_alert:
            if len(weather_area) > 6:
                weather_area = "many townships"
            else:
                weather_area = ', '.join(weather_area)
            self.weather_present("Thundery showers", weather_area)
        elif showers_alert:
            if len(weather_area) > 6:
                weather_area = "many townships"
            else:
                weather_area = ', '.join(weather_area)
            self.weather_present("Showers", weather_area)

        self.window.after(300000, lambda: self.window.destroy())

        self.window.mainloop()

    def weather_present(self, weather_type, location):
        self.continue_button = Button(text="Snooze Alarm", command=continue_clicked)
        self.continue_button.grid(row=0, column=1)
        self.weather_text.config(text=f"{weather_type} observed at {location}",
                                 fg="white", bg=THEME_COLOR, font=FONT
                                 )
        if self.alarm_on:
            winsound.PlaySound("RingIn.wav", winsound.SND_LOOP + winsound.SND_ASYNC)

    def change_alarm_status(self):
        if self.alarm_on:
            self.alarm_button.config(text="Alarm: Off")
            self.alarm_on = False
            with open("alarm_status.txt", mode="w") as file:
                file.write("No")
            winsound.PlaySound(None, winsound.SND_PURGE)
        else:
            self.alarm_button.config(text="Alarm: On")
            self.alarm_on = True
            with open("alarm_status.txt", mode="w") as file:
                file.write("Yes")

    def refresh_nowcast(self):
        self.window.destroy()
        os.startfile("main.py")

# class Alarm_UI:
#
#     def __init__(self, weather_nowcast_dict):
#         self.alarm_on = None
#         self.continue_button = None
#         self.window = Tk()
#         self.window.title("Weather Alarm")
#         self.window.config(padx=20, pady=20, bg=THEME_COLOR)
#
#         self.weather_text = Label(text="No significant weather :)", fg="white", bg=THEME_COLOR, font=FONT)
#         self.weather_text.grid(row=0, column=0, columnspan=3)
#         self.stop_button = Button(text="Stop Monitoring", command=exit)
#         self.stop_button.grid(row=1, column=2)
#         with open("alarm_status.txt") as file:
#             if file.read() == "Yes":
#                 self.alarm_on = True
#                 alarm_button_text = "Alarm On"
#             else:
#                 self.alarm_on = False
#                 alarm_button_text = "Alarm Off"
#
#         self.alarm_button = Button(text=alarm_button_text, command=self.change_alarm_status)
#         self.alarm_button.grid(row=1, column=0)
#
#         tsra_alert = False
#         showers_alert = False
#         weather_area = []
#
#         for key, value in weather_nowcast_dict.items():
#             if value == "Thundery Showers":
#                 tsra_alert = True
#                 weather_area.append(key)
#             elif value == "Showers":
#                 showers_alert = True
#                 weather_area.append(key)
#
#         if tsra_alert:
#             if len(weather_area) > 6:
#                 weather_area = "many townships"
#             else:
#                 weather_area = ', '.join(weather_area)
#             self.weather_present("Thundery showers", weather_area)
#         elif showers_alert:
#             if len(weather_area) > 6:
#                 weather_area = "many townships"
#             else:
#                 weather_area = ', '.join(weather_area)
#             self.weather_present("Showers", weather_area)
#
#         self.window.after(300000, lambda: self.window.destroy())
#
#         self.window.mainloop()
#
#     def weather_present(self, weather_type, location):
#         self.continue_button = Button(text="Snooze Alarm", command=continue_clicked)
#         self.continue_button.grid(row=1, column=1)
#         self.weather_text.config(text=f"{weather_type} observed at {location}",
#                                  fg="white", bg=THEME_COLOR, font=FONT
#                                  )
#         if self.alarm_on:
#             winsound.PlaySound("RingIn.wav", winsound.SND_LOOP + winsound.SND_ASYNC)
#
#     def change_alarm_status(self):
#         if self.alarm_on:
#             self.alarm_button.config(text="Alarm Off")
#             self.alarm_on = False
#             with open("alarm_status.txt", mode="w") as file:
#                 file.write("No")
#             winsound.PlaySound(None, winsound.SND_PURGE)
#         else:
#             self.alarm_button.config(text="Alarm On")
#             self.alarm_on = True
#             with open("alarm_status.txt", mode="w") as file:
#                 file.write("Yes")
