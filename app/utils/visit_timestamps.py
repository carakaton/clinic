from datetime import datetime, timedelta


def get_next_14_work_days_timestamps():
    now = datetime.now()
    d = datetime(year=now.year, month=now.month, day=now.day)
    days = [d]
    for _ in range(17):
        d += timedelta(days=1)
        days.append(d)
    days = [day for day in days if day.weekday() not in {5, 6}]
    return days[:14]


def get_visit_timestamps_for_full_work_day(dt: datetime):
    dt += timedelta(hours=8, minutes=0)
    times = [dt]
    for _ in range(47):
        dt += timedelta(minutes=15)
        times.append(dt)

    now = datetime.now() + timedelta(minutes=5)
    times = [t for t in times if t > now]
    return times
