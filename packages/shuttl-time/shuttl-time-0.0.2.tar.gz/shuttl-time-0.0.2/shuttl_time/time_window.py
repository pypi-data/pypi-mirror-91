from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Generator, Optional

import pytz

from shuttl_time.time import time_now


@dataclass(frozen=True)
class TimeDeltaWindow:
    lower: Optional[timedelta]
    upper: Optional[timedelta]

    @classmethod
    def from_minutes(cls, lower: int, upper: int) -> "TimeDeltaWindow":
        lower = timedelta(minutes=lower)
        upper = timedelta(minutes=upper)
        return cls(lower, upper)

    @classmethod
    def from_days(cls, lower: int, upper: int) -> "TimeDeltaWindow":
        lower = timedelta(days=lower)
        upper = timedelta(days=upper)
        return cls(lower, upper)


@dataclass(frozen=True)
class TimeWindow:
    from_date: Optional[datetime] = pytz.utc.localize(datetime.min)
    to_date: Optional[datetime] = pytz.utc.localize(datetime.max)

    def __post_init__(self):
        # from_date and to_date should either be tz aware or unaware
        assert bool(self.from_date.tzinfo) == bool(self.to_date.tzinfo)
        assert self.to_date.timestamp() >= self.from_date.timestamp()

    def __contains__(self, item: datetime) -> bool:
        return self.from_date <= item <= self.to_date

    def __str__(self) -> str:
        return f"{self.from_date.isoformat()} - {self.to_date.isoformat()}"

    def __hash__(self) -> hash:
        return hash((self.from_date, self.to_date))

    def intersects(self, other: "TimeWindow") -> bool:
        c1 = self.from_date in other or self.to_date in other
        c2 = other.from_date in self or other.to_date in self
        return c1 or c2

    def intersection(self, other: "TimeWindow") -> "TimeWindow":
        if not self.intersects(other):
            raise ValueError("No intersection possible")

        return TimeWindow(
            from_date=max(self.from_date, other.from_date),
            to_date=min(self.to_date, other.to_date),
        )

    def union(self, other: "TimeWindow") -> "TimeWindow":
        if not self.intersects(other):
            raise ValueError("No union possible")

        return TimeWindow(
            from_date=min(self.from_date, other.from_date),
            to_date=max(self.to_date, other.to_date),
        )

    @classmethod
    def around(cls, dt: datetime, td_window: TimeDeltaWindow) -> "TimeWindow":
        fr, to = None, None

        if td_window.lower is not None:
            fr = dt - td_window.lower

        if td_window.upper is not None:
            to = dt + td_window.upper

        return cls(fr, to)

    @classmethod
    def around_now(cls, td: timedelta) -> "TimeWindow":
        td_window = TimeDeltaWindow(td, td)
        return cls.around(time_now(), td_window)

    def dates(self) -> Generator[datetime, None, None]:
        return self.range(timedelta(days=1))

    def range(self, td: timedelta) -> Generator[datetime, None, None]:
        temp_date = self.from_date

        while temp_date <= self.to_date:
            yield temp_date
            temp_date += td
