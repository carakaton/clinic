from datetime import datetime, timedelta


def get_14_days():
    now = datetime.now()
    d = datetime(year=now.year, month=now.month, day=now.day)
    days = [d]
    for _ in range(17):
        d += timedelta(days=1)
        days.append(d)
    days = [day for day in days if day.weekday() not in {5, 6}]
    return days[:14]


def get_8to20_times(dt: datetime):
    dt += timedelta(hours=8, minutes=0)
    times = [dt]
    for _ in range(47):
        dt += timedelta(minutes=15)
        times.append(dt)
    return times
