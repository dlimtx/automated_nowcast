import datetime as dt


def get_time():
    time_now = dt.datetime.now()
    year_now = str(time_now.year)
    month_now = time_now.month
    if month_now < 10:
        month_now = f"0{month_now}"
    else:
        month_now = str(month_now)
    day_now = time_now.day
    if day_now < 10:
        day_now = f"0{day_now}"
    else:
        day_now = str(day_now)
    hour_now = time_now.hour
    if hour_now < 10:
        hour_now = f"0{hour_now}"
    else:
        hour_now = str(hour_now)
    minute_now = time_now.minute
    if minute_now == 0:
        minute_now = 1
    minute_split = []
    while minute_now > 0:
        minute_now, rmd = divmod(minute_now, 10)
        minute_split.append(rmd)
        if time_now.minute < 10:
            minute_split.append(0)
    if minute_split[0] > 6:
        minute_split[0] = 5
    elif 2 <= minute_split[0] <= 6:
        minute_split[0] = 0
    else:
        minute_split[0] = 5
        if minute_split[1] == 0:
            minute_split[1] = 5
            if int(hour_now) == 0:
                hour_now = '23'
                if int(day_now) == 1:
                    time_ytd = dt.date.today() - dt.timedelta(1)
                    day_now = str(time_ytd.day)
                    month_now = str(time_ytd.month)
                    if int(month_now) == "12":
                        year_now = str(int(year_now) - 1)
                else:
                    day_now = str(int(day_now) - 1)
            else:
                hour_now = str(int(hour_now) - 1)
        else:
            minute_split[1] -= 1

    time_list = [year_now, month_now, day_now, hour_now, minute_split]
    return time_list


# def get_previous_time():
#     time_previous = dt.datetime.now() - dt.timedelta(minutes=5)
#     year_previous = str(time_previous.year)
#     month_previous = time_previous.month
#     if month_previous < 10:
#         month_previous = f"0{month_previous}"
#     else:
#         month_previous = str(month_previous)
#     day_previous= time_previous.day
#     if day_previous < 10:
#         day_previous = f"0{day_previous}"
#     else:
#         day_previous = str(day_previous)
#     hour_previous = time_previous.hour
#     if hour_previous < 10:
#         hour_previous = f"0{hour_previous}"
#     else:
#         hour_previous = str(hour_previous)
#     minute_previous = time_previous.minute
#     minute_previous_split = []
#     while minute_previous > 0:
#         minute_previous, rmd = divmod(minute_previous, 10)
#         minute_previous_split.append(rmd)
#         if time_previous.minute < 10:
#             minute_previous_split.append(0)
#     if minute_previous_split[0] > 6:
#         minute_previous_split[0] = 5
#     else:
#         minute_previous_split[0] = 0
#
#     time_previous_list = [year_previous, month_previous, day_previous, hour_previous, minute_previous_split]
#     return time_previous_list
