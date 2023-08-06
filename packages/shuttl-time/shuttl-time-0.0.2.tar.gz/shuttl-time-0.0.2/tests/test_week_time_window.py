from datetime import datetime

import pytest

from shuttl_time.time_window import TimeWindow
from shuttl_time.weekday import WeekDay
from tests.factories import (
    week_time_dm,
    mt_in_utc,
    mt_in_time_zone,
    week_time_window_dm,
    time_zone,
)


class TestSlotWindowCreation:
    def test_throws_assertion_error_if_slots_belong_to_different_timezones(self):
        with pytest.raises(AssertionError):
            week_time_1 = week_time_dm(
                day_of_week=WeekDay.MONDAY, start_time=mt_in_time_zone(900)
            )
            week_time_2 = week_time_dm(
                day_of_week=WeekDay.TUESDAY, start_time=mt_in_utc(900)
            )
            week_time_window_dm(week_time_1, week_time_2)

    def test_throws_assertion_error_if_start_is_greater_than_end(self):
        with pytest.raises(AssertionError):
            week_time_1 = week_time_dm(
                day_of_week=WeekDay.MONDAY, start_time=mt_in_time_zone(900)
            )
            week_time_2 = week_time_dm(
                day_of_week=WeekDay.TUESDAY, start_time=mt_in_time_zone(900)
            )
            week_time_window_dm(start=week_time_2, end=week_time_1)

    def test_successful_creation(self):
        week_time_1 = week_time_dm(
            day_of_week=WeekDay.MONDAY, start_time=mt_in_time_zone(900)
        )
        week_time_2 = week_time_dm(
            day_of_week=WeekDay.TUESDAY, start_time=mt_in_time_zone(900)
        )
        assert week_time_window_dm(week_time_1, week_time_2)


class TestSlotWindowOccurrences:
    def test_when_week_time_window_starts_and_ends_on_same_day_and_dt_lies_before_week_time_window_starts(
        self,
    ):
        sw = week_time_window_dm(
            start=week_time_dm(
                day_of_week=WeekDay.MONDAY, start_time=mt_in_time_zone(900)
            ),
            end=week_time_dm(
                day_of_week=WeekDay.MONDAY, start_time=mt_in_time_zone(1100)
            ),
        )
        time_before_window_starts = time_zone.localize(
            datetime(year=2020, month=12, day=21, hour=8)
        )
        occurrences = sw.occurrences(time_before_window_starts)
        assert next(occurrences) == TimeWindow(
            from_date=time_zone.localize(datetime(year=2020, month=12, day=21, hour=9)),
            to_date=time_zone.localize(datetime(year=2020, month=12, day=21, hour=11)),
        )
        assert next(occurrences) == TimeWindow(
            from_date=time_zone.localize(datetime(year=2020, month=12, day=28, hour=9)),
            to_date=time_zone.localize(datetime(year=2020, month=12, day=28, hour=11)),
        )

    def test_when_week_time_window_starts_and_ends_on_same_day_and_dt_lies_in_week_time_window(
        self,
    ):
        sw = week_time_window_dm(
            start=week_time_dm(
                day_of_week=WeekDay.MONDAY, start_time=mt_in_time_zone(900)
            ),
            end=week_time_dm(
                day_of_week=WeekDay.MONDAY, start_time=mt_in_time_zone(1100)
            ),
        )
        time_between_week_time_window = time_zone.localize(
            datetime(year=2020, month=12, day=21, hour=10)
        )
        occurrences = sw.occurrences(time_between_week_time_window)
        assert next(occurrences) == TimeWindow(
            from_date=time_zone.localize(datetime(year=2020, month=12, day=21, hour=9)),
            to_date=time_zone.localize(datetime(year=2020, month=12, day=21, hour=11)),
        )
        assert next(occurrences) == TimeWindow(
            from_date=time_zone.localize(datetime(year=2020, month=12, day=28, hour=9)),
            to_date=time_zone.localize(datetime(year=2020, month=12, day=28, hour=11)),
        )

    def test_when_week_time_window_starts_and_ends_on_same_day_and_dt_lies_after_week_time_window_ends(
        self,
    ):
        sw = week_time_window_dm(
            start=week_time_dm(
                day_of_week=WeekDay.MONDAY, start_time=mt_in_time_zone(900)
            ),
            end=week_time_dm(
                day_of_week=WeekDay.MONDAY, start_time=mt_in_time_zone(1100)
            ),
        )
        time_after_week_time_window = time_zone.localize(
            datetime(year=2020, month=12, day=14, hour=12)
        )
        occurrences = sw.occurrences(time_after_week_time_window)
        assert next(occurrences) == TimeWindow(
            from_date=time_zone.localize(datetime(year=2020, month=12, day=21, hour=9)),
            to_date=time_zone.localize(datetime(year=2020, month=12, day=21, hour=11)),
        )
        assert next(occurrences) == TimeWindow(
            from_date=time_zone.localize(datetime(year=2020, month=12, day=28, hour=9)),
            to_date=time_zone.localize(datetime(year=2020, month=12, day=28, hour=11)),
        )

    def test_when_week_time_window_starts_and_ends_on_different_days_and_dt_lies_before_week_time_window_starts(
        self,
    ):
        sw = week_time_window_dm(
            start=week_time_dm(
                day_of_week=WeekDay.TUESDAY, start_time=mt_in_time_zone(900)
            ),
            end=week_time_dm(
                day_of_week=WeekDay.FRIDAY, start_time=mt_in_time_zone(1100)
            ),
        )
        time_before_window_starts = time_zone.localize(
            datetime(year=2020, month=12, day=14, hour=8)
        )
        occurrences = sw.occurrences(time_before_window_starts)
        assert next(occurrences) == TimeWindow(
            from_date=time_zone.localize(datetime(year=2020, month=12, day=15, hour=9)),
            to_date=time_zone.localize(datetime(year=2020, month=12, day=18, hour=11)),
        )
        assert next(occurrences) == TimeWindow(
            from_date=time_zone.localize(datetime(year=2020, month=12, day=22, hour=9)),
            to_date=time_zone.localize(datetime(year=2020, month=12, day=25, hour=11)),
        )

    def test_when_week_time_window_starts_and_ends_on_different_days_and_dt_lies_in_week_time_window(
        self,
    ):
        sw = week_time_window_dm(
            start=week_time_dm(
                day_of_week=WeekDay.TUESDAY, start_time=mt_in_time_zone(900)
            ),
            end=week_time_dm(
                day_of_week=WeekDay.FRIDAY, start_time=mt_in_time_zone(1100)
            ),
        )
        time_in_week_time_window = time_zone.localize(
            datetime(year=2020, month=12, day=15, hour=10)
        )
        occurrences = sw.occurrences(time_in_week_time_window)
        assert next(occurrences) == TimeWindow(
            from_date=time_zone.localize(datetime(year=2020, month=12, day=15, hour=9)),
            to_date=time_zone.localize(datetime(year=2020, month=12, day=18, hour=11)),
        )
        assert next(occurrences) == TimeWindow(
            from_date=time_zone.localize(datetime(year=2020, month=12, day=22, hour=9)),
            to_date=time_zone.localize(datetime(year=2020, month=12, day=25, hour=11)),
        )

    def test_when_week_time_window_starts_and_ends_on_different_days_and_dt_lies_in_week_time_window_with_weekday_same_as_week_time_window_end(
        self,
    ):
        sw = week_time_window_dm(
            start=week_time_dm(
                day_of_week=WeekDay.TUESDAY, start_time=mt_in_time_zone(900)
            ),
            end=week_time_dm(
                day_of_week=WeekDay.FRIDAY, start_time=mt_in_time_zone(1100)
            ),
        )
        time_in_week_time_window_with_same_weekday_as_end_day = time_zone.localize(
            datetime(year=2020, month=12, day=11, hour=10)
        )
        occurrences = sw.occurrences(
            time_in_week_time_window_with_same_weekday_as_end_day
        )
        assert next(occurrences) == TimeWindow(
            from_date=time_zone.localize(datetime(year=2020, month=12, day=8, hour=9)),
            to_date=time_zone.localize(datetime(year=2020, month=12, day=11, hour=11)),
        )
        assert next(occurrences) == TimeWindow(
            from_date=time_zone.localize(datetime(year=2020, month=12, day=15, hour=9)),
            to_date=time_zone.localize(datetime(year=2020, month=12, day=18, hour=11)),
        )

    def test_when_week_time_window_starts_and_ends_on_different_days_and_dt_lies_after_week_time_window_ends(
        self,
    ):
        sw = week_time_window_dm(
            start=week_time_dm(
                day_of_week=WeekDay.TUESDAY, start_time=mt_in_time_zone(900)
            ),
            end=week_time_dm(
                day_of_week=WeekDay.FRIDAY, start_time=mt_in_time_zone(1100)
            ),
        )
        time_after_week_time_window_ends = time_zone.localize(
            datetime(year=2020, month=12, day=12, hour=12)
        )
        occurrences = sw.occurrences(time_after_week_time_window_ends)

        assert next(occurrences) == TimeWindow(
            from_date=time_zone.localize(datetime(year=2020, month=12, day=15, hour=9)),
            to_date=time_zone.localize(datetime(year=2020, month=12, day=18, hour=11)),
        )
        assert next(occurrences) == TimeWindow(
            from_date=time_zone.localize(datetime(year=2020, month=12, day=22, hour=9)),
            to_date=time_zone.localize(datetime(year=2020, month=12, day=25, hour=11)),
        )

    def test_when_week_time_window_starts_and_ends_on_different_days_and_dt_lies_after_week_time_window_ends_but_is_on_same_weekday(
        self,
    ):
        sw = week_time_window_dm(
            start=week_time_dm(
                day_of_week=WeekDay.TUESDAY, start_time=mt_in_time_zone(900)
            ),
            end=week_time_dm(
                day_of_week=WeekDay.FRIDAY, start_time=mt_in_time_zone(1100)
            ),
        )
        time_after_week_time_window_ends_same_day_as_slot_end_day = time_zone.localize(
            datetime(year=2020, month=12, day=15, hour=12)
        )
        occurrences = sw.occurrences(
            time_after_week_time_window_ends_same_day_as_slot_end_day
        )
        assert next(occurrences) == TimeWindow(
            from_date=time_zone.localize(datetime(year=2020, month=12, day=15, hour=9)),
            to_date=time_zone.localize(datetime(year=2020, month=12, day=18, hour=11)),
        )
        assert next(occurrences) == TimeWindow(
            from_date=time_zone.localize(datetime(year=2020, month=12, day=22, hour=9)),
            to_date=time_zone.localize(datetime(year=2020, month=12, day=25, hour=11)),
        )
