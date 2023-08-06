import pytest
from pytz import timezone, utc
from datetime import datetime, time, date, timedelta

from shuttl_time.military_time import MilitaryTime, TimezoneMismatch
from shuttl_time.time import (
    time_now,
    maybe_datetime_from_iso_format,
    maybe_date_from_iso_format,
)
from shuttl_time.time_window import TimeWindow
from shuttl_time.weekday import WeekDay
from tests.factories import time_zone as IST_TIMEZONE


def _mt_ist(time: int) -> MilitaryTime:
    return MilitaryTime(time, IST_TIMEZONE)


@pytest.mark.parametrize("hr,min", [(1, 20), (23, 59), (0, 0)])
def test_military_time_constructor(hr: int, min: int):
    mt = MilitaryTime.from_hr_min(hr, min, IST_TIMEZONE)
    assert hr == mt.hr
    assert min == mt.min
    assert IST_TIMEZONE.zone == mt.tz.zone


@pytest.mark.parametrize("hr,min", [(24, 00), (12, 61)])
def test_military_time_constructor_fails_when_hr_or_min_are_out_of_range(
    hr: int, min: int
):
    with pytest.raises(AssertionError):
        MilitaryTime.from_hr_min(hr, min, IST_TIMEZONE)


@pytest.mark.parametrize(
    "mta,mtr",
    [
        (_mt_ist(1320) + timedelta(hours=1, minutes=20), _mt_ist(1440)),
        (_mt_ist(1320) + timedelta(hours=0, minutes=40), _mt_ist(1400)),
    ],
)
def test_military_time_add(mta: MilitaryTime, mtr: MilitaryTime):
    assert mtr == mta


@pytest.mark.parametrize(
    "mts,mtr",
    [
        (_mt_ist(1320) - timedelta(hours=1, minutes=20), _mt_ist(1200)),
        (_mt_ist(1320) - timedelta(hours=0, minutes=40), _mt_ist(1240)),
    ],
)
def test_military_time_sub(mts: MilitaryTime, mtr: MilitaryTime):
    assert mtr == mts


def test_military_time_inequality():
    assert _mt_ist(1000) != _mt_ist(900)


def test_weekday_eq():
    assert WeekDay.MONDAY == WeekDay.MONDAY


@pytest.mark.parametrize(
    "first,snd", [(WeekDay.MONDAY, WeekDay.TUESDAY), (WeekDay.MONDAY, WeekDay.SUNDAY)]
)
def test_weekday_lt(first: WeekDay, snd: WeekDay):
    assert first < snd


def test_weekday_extract_from_datetime():
    dt = datetime(year=2019, month=1, day=1)
    assert WeekDay.TUESDAY == WeekDay.extract_from_datetime(dt)


def test_weekday_extract_from_date():
    dt = datetime(year=2019, month=1, day=1)
    assert WeekDay.TUESDAY == WeekDay.extract_from_date(dt.date())


def test_military_time_with_timezone():
    assert _mt_ist(900) != MilitaryTime(900, timezone("America/Sao_Paulo"))


def test_military_time_sort():
    source_times = [_mt_ist(r) for r in range(2300, 1, -100)]
    assert sorted(source_times) == [_mt_ist(r) for r in range(100, 2400, 100)]


def test_military_time_compare_lt():
    assert _mt_ist(100) < _mt_ist(150)


def test_military_time_compare_gt():
    assert _mt_ist(1000) > _mt_ist(150)


def test_military_time_compare_gte():
    assert _mt_ist(150) >= _mt_ist(150)
    assert _mt_ist(1000) >= _mt_ist(150)


def test_military_time_compare_lte():
    assert _mt_ist(150) <= _mt_ist(150)
    assert _mt_ist(100) <= _mt_ist(150)


def test_military_time_compare_timezone_mismatch():
    with pytest.raises(TimezoneMismatch):
        _mt_ist(100) < MilitaryTime(100, timezone("America/Sao_Paulo"))


def test_military_time_combining_with_date():
    d = date(year=2019, month=1, day=1)
    actual = _mt_ist(1000).combine(d)
    dt = IST_TIMEZONE.localize(datetime(year=2019, month=1, day=1, hour=10, minute=00))

    assert actual == dt


def test_weekday_str_conversion():
    assert str(WeekDay.SUNDAY) == "SUNDAY"


def test_hash_of_military_times():
    assert 2 == len({_mt_ist(900), _mt_ist(1000)})


def test_hash_of_same_military_time():
    assert 1 == len({_mt_ist(900), _mt_ist(900)})


def test_mt_in_list():
    assert _mt_ist(900) in [_mt_ist(900), _mt_ist(1000)]


def test_mt_not_in_list():
    assert _mt_ist(910) not in [_mt_ist(900), _mt_ist(1000)]


def test_tz_unaware_time():
    mt = _mt_ist(900)
    assert mt.tz_unaware_time() == time(hour=mt.hr, minute=mt.min)


def test_future_day():
    assert WeekDay.WEDNESDAY == WeekDay.MONDAY.get_day_after(num_of_days=2)
    assert WeekDay.SUNDAY == WeekDay.MONDAY.get_day_after(num_of_days=-1)
    assert WeekDay.MONDAY == WeekDay.SATURDAY.get_day_after(num_of_days=2)


@pytest.mark.parametrize(
    "first,second,result",
    [
        (WeekDay.WEDNESDAY, WeekDay.TUESDAY, 1),
        (WeekDay.WEDNESDAY, WeekDay.WEDNESDAY, 0),
        (WeekDay.WEDNESDAY, WeekDay.THURSDAY, 6),
    ],
)
def test_weekday_sub(first: WeekDay, second: WeekDay, result: int):
    assert first - second == result


def test_maybe_datetime_from_iso_format_happy():
    current_time = time_now()
    assert current_time == maybe_datetime_from_iso_format(current_time.isoformat())


def test_maybe_datetime_from_iso_format_handles_none():
    assert not maybe_datetime_from_iso_format(None)


def test_maybe_date_from_iso_format_happy():
    current_time = time_now()
    assert current_time.date() == maybe_date_from_iso_format(
        current_time.date().isoformat()
    )


def test_maybe_date_from_iso_format_handles_none():
    assert not maybe_date_from_iso_format(None)


def test_time_window_with_tz_unaware_time():
    with pytest.raises(AssertionError):
        TimeWindow(from_date=datetime(2020, 4, 9, 6, 30, 10))
        TimeWindow(
            datetime(2020, 4, 9, 9, 30, 10), datetime(2020, 4, 9, 9, 30, 10, tzinfo=utc)
        )


def test_time_window_with_invalid_to_from_time():
    with pytest.raises(AssertionError):
        TimeWindow(datetime(2020, 4, 9, 6, 30, 10), datetime(2020, 4, 9, 6, 30, 9))
