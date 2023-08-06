from dataclasses import dataclass
from datetime import datetime, time, date, tzinfo, timedelta
from functools import total_ordering

tz_datetime = datetime


class TimezoneNotFound(Exception):
    pass


class TimezoneMismatch(Exception):
    pass


@total_ordering
@dataclass(frozen=True)
class MilitaryTime:
    time: int
    tz: tzinfo

    def __post_init__(self):
        hr, min = divmod(self.time, 100)
        assert 0 <= min < 60
        assert 0 <= hr < 24

    @property
    def hr(self) -> int:
        return divmod(self.time, 100)[0]

    @property
    def min(self) -> int:
        return divmod(self.time, 100)[1]

    @classmethod
    def from_hr_min(cls, hr: int, min: int, tzinfo: tzinfo) -> "MilitaryTime":
        return cls(time=hr * 100 + min, tz=tzinfo)

    @classmethod
    def extract_from_datetime(cls, dt: datetime) -> "MilitaryTime":
        if not dt.tzinfo:
            raise TimezoneNotFound("No timezone present in datatime object")

        return cls.from_hr_min(dt.hour, dt.minute, dt.tzinfo)

    def __str__(self) -> str:
        return f"{self.hr:02}{self.min:02}:{self.tz.zone}"

    def __add__(self, other: timedelta) -> "MilitaryTime":
        other_min = (other.total_seconds() // 60) % 60
        other_hrs = (other.total_seconds()) // 3600
        additional_hrs = (self.min + other_min) // 60

        min = (self.min + other_min) % 60
        hr = (self.hr + other_hrs + additional_hrs) % 24
        return MilitaryTime.from_hr_min(hr, min, self.tz)

    def __sub__(self, other: timedelta) -> "MilitaryTime":
        other_min = (other.total_seconds() // 60) % 60
        other_hrs = (other.total_seconds()) // 3600
        additional_hrs = (self.min - other_min) // 60

        min = (self.min - other_min) % 60
        hr = (self.hr - other_hrs + additional_hrs) % 24
        return MilitaryTime.from_hr_min(hr, min, self.tz)

    def __eq__(self, other: "MilitaryTime") -> bool:
        return self.time == other.time and self.tz.zone == other.tz.zone

    def __lt__(self, other: "MilitaryTime") -> bool:
        if self.tz.zone != other.tz.zone:
            raise TimezoneMismatch(
                f"Recieved different timezones as {self.tz.zone} and {other.tz.zone}"
            )

        return (self.hr * 100, self.min) < (other.hr * 100, other.min)

    def to_time(self, tzinfo: tzinfo) -> time:
        return time(hour=self.hr, minute=self.min, tzinfo=tzinfo)

    def tz_unaware_time(self) -> time:
        return time(hour=self.hr, minute=self.min)

    def combine(self, dt: date) -> datetime:
        return self.tz.localize(datetime.combine(dt, self.tz_unaware_time()))
