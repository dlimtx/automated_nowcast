import datetime as dt


def get_time():
    time_now = dt.datetime.now(dt.timezone(dt.timedelta(hours=8)))
    print(time_now)
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



