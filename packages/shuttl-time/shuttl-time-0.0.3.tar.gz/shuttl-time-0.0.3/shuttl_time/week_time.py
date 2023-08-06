from dataclasses import dataclass
from datetime import datetime, timedelta, time
from functools import total_ordering

import pytz

from shuttl_time.military_time import MilitaryTime
from shuttl_time.time import time_now
from shuttl_time.weekday import WeekDay


@total_ordering
@dataclass(frozen=True)
class WeekTime:
    day_of_week: WeekDay
    start_time: MilitaryTime

    def __lt__(self, other: "WeekTime") -> bool:
        if self.day_of_week == other.day_of_week:
            return self.start_time < other.start_time
        return self.day_of_week < other.day_of_week

    @classmethod
    def from_dict(cls, dikt: dict) -> "WeekTime":
        return cls(
            day_of_week=WeekDay(dikt["day_of_week"]),
            start_time=MilitaryTime(
                time=int(dikt["start_time"]["time"]),
                tz=pytz.timezone(dikt["start_time"]["timezone"]),
            ),
        )

    @classmethod
    def from_dt(cls, dt: datetime) -> "WeekTime":
        weekday = WeekDay.extract_from_datetime(dt)
        mt = MilitaryTime.extract_from_datetime(dt)

        return cls(weekday, mt)

    @property
    def tz(self) -> pytz.timezone:
        return self.start_time.tz

    @property
    def tz_unaware_time(self) -> time:
        return self.start_time.tz_unaware_time()

    def occurrences(self, date: datetime = None):
        dt = date or time_now()
        dt = dt.astimezone(self.tz)
        dt = self._first_occurrence_from(dt)
        while True:
            yield dt
            dt = self._next_week_occurence(dt)

    def _first_occurrence_from(self, dt: datetime) -> datetime:
        days_ahead = self.day_of_week - WeekDay.extract_from_datetime(dt)

        if days_ahead == 0:
            if self.start_time >= MilitaryTime.extract_from_datetime(dt):
                days_ahead = 0
            else:
                days_ahead = 7

        dt += timedelta(days=days_ahead)
        return self.start_time.combine(dt.date())

    def _next_week_occurence(self, dt: datetime) -> datetime:
        return dt + timedelta(days=7)
