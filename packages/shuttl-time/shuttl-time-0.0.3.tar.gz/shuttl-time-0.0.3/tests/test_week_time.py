from datetime import datetime, timedelta
from itertools import islice

import pytest
from pytz import utc

from shuttl_time import WeekTime
from shuttl_time.weekday import WeekDay
from tests.factories import (
    week_time_dm,
    mt_in_time_zone,
    time_zone_string,
    time_zone,
    mt_in_utc,
)


def test_from_dict_to_week_time():
    week_time_dict = {
        "day_of_week": "MONDAY",
        "start_time": {"time": 1002, "timezone": time_zone_string},
    }
    week_time = week_time_dm(start_time=mt_in_time_zone(time=1002))
    assert week_time == WeekTime.from_dict(week_time_dict)


def test_week_time_creation_from_datetime():
    dt = time_zone.localize(datetime.fromisoformat("2019-01-07T07:18:00"))
    assert WeekTime.from_dt(dt) == week_time_dm(start_time=mt_in_time_zone(time=718))


def test_week_time_ordering():
    week_time_1 = week_time_dm(start_time=mt_in_time_zone(723))
    week_time_2 = week_time_dm(start_time=mt_in_time_zone(724))
    assert week_time_1 < week_time_2


@pytest.mark.parametrize(
    "week_time,start_date,first",
    [
        (
            WeekTime(day_of_week=WeekDay.MONDAY, start_time=mt_in_time_zone(900)),
            time_zone.localize(datetime(year=2019, month=1, day=7, hour=8)),
            time_zone.localize(datetime(year=2019, month=1, day=7, hour=9)),
        ),
        (
            WeekTime(day_of_week=WeekDay.MONDAY, start_time=mt_in_time_zone(930)),
            time_zone.localize(datetime(year=2019, month=1, day=7, hour=8)),
            time_zone.localize(datetime(year=2019, month=1, day=7, hour=9, minute=30)),
        ),
        (
            WeekTime(day_of_week=WeekDay.MONDAY, start_time=mt_in_time_zone(800)),
            time_zone.localize(datetime(year=2019, month=1, day=7, hour=8)),
            time_zone.localize(datetime(year=2019, month=1, day=7, hour=8)),
        ),
        (
            WeekTime(day_of_week=WeekDay.MONDAY, start_time=mt_in_time_zone(800)),
            time_zone.localize(datetime(year=2019, month=1, day=7, hour=9)),
            time_zone.localize(datetime(year=2019, month=1, day=14, hour=8)),
        ),
        (
            WeekTime(day_of_week=WeekDay.TUESDAY, start_time=mt_in_time_zone(800)),
            time_zone.localize(datetime(year=2019, month=1, day=7, hour=9)),
            time_zone.localize(datetime(year=2019, month=1, day=8, hour=8)),
        ),
        (
            WeekTime(day_of_week=WeekDay.TUESDAY, start_time=mt_in_time_zone(800)),
            time_zone.localize(datetime(year=2019, month=1, day=9, hour=9)),
            time_zone.localize(datetime(year=2019, month=1, day=15, hour=8)),
        ),
        (
            WeekTime(day_of_week=WeekDay.TUESDAY, start_time=mt_in_utc(800)),
            time_zone.localize(datetime(year=2019, month=1, day=8, hour=9)),
            utc.localize(datetime(year=2019, month=1, day=8, hour=8)),
        ),
    ],
)
def test_week_time_occurrences(
    week_time: WeekTime, start_date: datetime, first: datetime
):
    occurrences = [first, first + timedelta(days=7), first + timedelta(days=14)]
    assert occurrences == list(islice(week_time.occurrences(start_date), 3))
