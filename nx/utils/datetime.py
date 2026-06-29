from datetime import datetime, time, timedelta
from dataclasses import dataclass
from django.utils import timezone
from django.conf import settings

DatetimeRange = tuple[datetime, datetime]


@dataclass
class StatDatetimeRange:
    today: DatetimeRange
    week: DatetimeRange
    month: DatetimeRange
    year: DatetimeRange


def get_stat_datetime_range() -> StatDatetimeRange:
    if settings.USE_TZ:
        now = timezone.localtime(timezone.now())  # aware
        tzinfo = now.tzinfo
        mk = lambda dt: dt.replace(tzinfo=tzinfo)  # noqa
    else:
        now = timezone.now()  # naive
        mk = lambda dt: dt  # noqa

    one_day = timedelta(days=1)
    one_week = timedelta(days=7)

    # today
    today_start = mk(datetime.combine(now.date(), time.min))  # 00:00:00.000000
    today_next = today_start + one_day
    today_end = today_next - timedelta(microseconds=1)  # 23:59:59.999999

    # week (Mon-Sun)
    monday_date = now.date() - timedelta(days=now.weekday())
    week_start = mk(datetime.combine(monday_date, time.min))  # Mon 00:00:00
    week_next = week_start + one_week  # next Mon 00:00:00
    week_end = week_next - timedelta(microseconds=1)  # Sun 23:59:59.999999

    # month
    month_start = mk(datetime(now.year, now.month, 1, 0, 0, 0))
    if now.month == 12:
        month_next = mk(datetime(now.year + 1, 1, 1, 0, 0, 0))
    else:
        month_next = mk(datetime(now.year, now.month + 1, 1, 0, 0, 0))
    month_end = month_next - timedelta(microseconds=1)

    # year
    year_start = mk(datetime(now.year, 1, 1, 0, 0, 0))
    year_next = mk(datetime(now.year + 1, 1, 1, 0, 0, 0))
    year_end = year_next - timedelta(microseconds=1)

    return StatDatetimeRange(
        today=(today_start, today_end),
        week=(week_start, week_end),
        month=(month_start, month_end),
        year=(year_start, year_end),
    )
