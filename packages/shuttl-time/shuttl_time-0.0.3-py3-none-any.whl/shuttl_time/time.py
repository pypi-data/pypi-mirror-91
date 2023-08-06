from datetime import datetime, timedelta, date
from typing import Optional

import pytz


def time_now() -> datetime:
    return pytz.utc.localize(datetime.utcnow())


def from_iso_format(d: str, tz: pytz = pytz.utc) -> datetime:
    return datetime.fromisoformat(d).astimezone(tz)


def maybe_datetime_from_iso_format(d: str, tz: pytz = pytz.utc) -> Optional[datetime]:
    return datetime.fromisoformat(d).astimezone(tz) if d else None


def date_from_iso_format(d: str, tz: pytz = pytz.utc) -> date:
    time = datetime.fromisoformat(d).astimezone(tz) + timedelta(hours=12)
    return time.date()


def maybe_date_from_iso_format(d: str, tz: pytz = pytz.utc) -> Optional[date]:
    time = datetime.fromisoformat(d).astimezone(tz) + timedelta(hours=12) if d else None
    return time.date() if time else None
