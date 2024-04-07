from datetime import datetime, timedelta


def get_14_days():
    now = datetime.now()
    d = datetime(year=now.year, month=now.month, day=now.day)
    week = [d]
    for _ in range(17):
        d += timedelta(days=1)
        week.append(d)
    week = [day for day in week if day.weekday() not in {5, 6}]
    return week[:14]


def get_8to20_times(dt: datetime):
    dt += timedelta(hours=8, minutes=0)
    times = [dt]
    for _ in range(47):
        dt += timedelta(minutes=15)
        times.append(dt)
    return times
