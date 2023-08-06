from dataclasses import dataclass
from datetime import datetime, timedelta
from functools import total_ordering
from typing import Generator

import pytz

from shuttl_time.time_window import TimeWindow
from shuttl_time.military_time import MilitaryTime
from shuttl_time.week_time import WeekTime
from shuttl_time.time import time_now
from shuttl_time.weekday import WeekDay


@total_ordering
@dataclass(frozen=True)
class WeekTimeWindow:
    start: WeekTime
    end: WeekTime

    def __lt__(self, window: "WeekTimeWindow") -> bool:
        return self.start < window.start

    def __contains__(self, slot: WeekTime) -> bool:
        return self.start <= slot <= self.end

    def __post_init__(self):
        assert self.start.tz == self.end.tz
        assert self.start <= self.end

    @classmethod
    def from_dict(cls, dikt: dict) -> "WeekTimeWindow":
        return cls(
            start=WeekTime.from_dict(dikt["start"]), end=WeekTime.from_dict(dikt["end"])
        )

    @property
    def tz(self) -> pytz.timezone:
        return self.start.tz

    @property
    def start_time(self) -> MilitaryTime:
        return self.start.start_time

    @property
    def start_day_of_week(self) -> WeekDay:
        return self.start.day_of_week

    @property
    def end_time(self) -> MilitaryTime:
        return self.end.start_time

    @property
    def end_day_of_week(self) -> WeekDay:
        return self.end.day_of_week

    def occurrences(self, date: datetime = None) -> Generator[TimeWindow, None, None]:
        def _next_week_occurrence(date_time: datetime) -> datetime:
            return date_time + timedelta(days=7)

        dt = date or time_now()
        dt = dt.astimezone(self.tz)
        window = self._first_occurrence_from(dt)
        while True:
            yield window
            window = TimeWindow(
                from_date=_next_week_occurrence(window.from_date),
                to_date=_next_week_occurrence(window.to_date),
            )

    def _first_occurrence_from(self, dt: datetime) -> TimeWindow:
        def _previous_week_occurrence(date_time: datetime) -> datetime:
            return date_time - timedelta(days=7)

        start_date = next(self.start.occurrences(dt))
        end_date = next(self.end.occurrences(dt))

        if start_date > end_date:
            start_date = _previous_week_occurrence(date_time=start_date)

        return TimeWindow(
            from_date=self.start_time.combine(start_date.date()),
            to_date=self.end_time.combine(end_date.date()),
        )
