from datetime import datetime, timedelta

import pytest
import pytz

from shuttl_time.time import time_now
from shuttl_time.time_window import TimeWindow
from tests.factories import time_zone


def test_contains_of_time_window():
    fr = datetime.utcnow().astimezone(pytz.utc)
    to = fr + timedelta(days=1)
    dt = fr + timedelta(hours=5)
    tw = TimeWindow(from_date=fr, to_date=to)

    assert dt in tw


def test_iterate_over_time_window_includes_last_value():
    dt_lower = datetime.utcnow()
    dt_upper = dt_lower + timedelta(days=3)

    tw = TimeWindow(from_date=dt_lower, to_date=dt_upper)
    assert dt_upper in list(tw.dates())


def test_contains_in_infinite_time_window():
    dt = datetime.utcnow().astimezone(pytz.utc)

    assert dt in TimeWindow()


def test_contains_when_not_in_range():
    fr = datetime.utcnow().astimezone(pytz.utc)
    to = fr + timedelta(days=1)
    dt = fr + timedelta(days=20)
    tw = TimeWindow(from_date=fr, to_date=to)

    assert dt not in tw


def test_time_window_equality():
    fr = datetime.utcnow().astimezone(pytz.utc)
    to = fr + timedelta(days=1)

    assert TimeWindow(fr, to) == TimeWindow(fr, to)


def test_string_representation():
    fr = time_zone.localize(datetime(2019, 1, 1, 1, 1, 1, 1))
    to = time_zone.localize(datetime(2019, 1, 2, 1, 1, 1, 1))
    time_window_string = (
        "2019-01-01T01:01:01.000001+05:30 - 2019-01-02T01:01:01.000001+05:30"
    )

    assert str(TimeWindow(fr, to)) == time_window_string


def test_cannot_set_time_window_if_to_date_is_less_than_from_date():
    dt = time_now()
    dtminus5 = dt - timedelta(days=5)
    with pytest.raises(AssertionError):
        TimeWindow(from_date=dt, to_date=dtminus5)


def test_cannot_set_values_after_instantiation():
    tw = TimeWindow()
    with pytest.raises(AttributeError):
        tw.from_date = datetime(2019, 1, 1)


def ist_dt(*args, **kwargs) -> datetime:
    return time_zone.localize(datetime(*args, **kwargs))


@pytest.mark.parametrize(
    "tw1,tw2",
    [
        (TimeWindow(), TimeWindow()),
        (TimeWindow(from_date=ist_dt(2019, 1, 1)), TimeWindow()),
        (
            TimeWindow(from_date=ist_dt(2019, 1, 1), to_date=ist_dt(2019, 2, 2)),
            TimeWindow(),
        ),
        (
            TimeWindow(),
            TimeWindow(from_date=ist_dt(2019, 1, 1), to_date=ist_dt(2019, 2, 2)),
        ),
        (
            TimeWindow(from_date=ist_dt(2019, 1, 1), to_date=ist_dt(2019, 2, 2)),
            TimeWindow(from_date=ist_dt(2019, 1, 30), to_date=ist_dt(2019, 3, 30)),
        ),
        (
            TimeWindow(from_date=ist_dt(2019, 1, 30), to_date=ist_dt(2019, 3, 30)),
            TimeWindow(from_date=ist_dt(2019, 1, 1), to_date=ist_dt(2019, 2, 2)),
        ),
    ],
)
def test_time_window_intersection(tw1: TimeWindow, tw2: TimeWindow):
    assert tw1.intersects(tw2)


@pytest.mark.parametrize(
    "tw1,tw2",
    [
        (
            TimeWindow(from_date=ist_dt(2019, 1, 1), to_date=ist_dt(2019, 2, 2)),
            TimeWindow(from_date=ist_dt(2019, 2, 10), to_date=ist_dt(2019, 3, 30)),
        )
    ],
)
def test_time_window_non_intersection(tw1: TimeWindow, tw2: TimeWindow):
    assert not tw1.intersects(tw2)


@pytest.mark.parametrize(
    "tw1,tw2",
    [
        (
            TimeWindow(from_date=ist_dt(2019, 1, 1), to_date=ist_dt(2019, 2, 2)),
            TimeWindow(from_date=ist_dt(2019, 2, 10), to_date=ist_dt(2019, 3, 30)),
        )
    ],
)
def test_intersection_raises_error_when_it_is_not_possible(
    tw1: TimeWindow, tw2: TimeWindow
):
    with pytest.raises(ValueError):
        tw1.intersection(tw2)


@pytest.mark.parametrize(
    "tw1,tw2",
    [
        (
            TimeWindow(from_date=ist_dt(2019, 1, 1), to_date=ist_dt(2019, 2, 2)),
            TimeWindow(from_date=ist_dt(2019, 2, 10), to_date=ist_dt(2019, 3, 30)),
        )
    ],
)
def test_union_raises_error_when_it_is_not_possible(tw1: TimeWindow, tw2: TimeWindow):
    with pytest.raises(ValueError):
        tw1.union(tw2)
