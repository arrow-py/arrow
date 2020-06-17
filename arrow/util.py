import datetime as dt
import numbers
from datetime import date, datetime, timedelta
from typing import Any, Union

from arrow.constants import MAX_TIMESTAMP, MAX_TIMESTAMP_MS, MAX_TIMESTAMP_US


def total_seconds(td: timedelta) -> float:
    """Get total seconds for timedelta."""
    return td.total_seconds()


def is_timestamp(value: Any) -> bool:
    """Check if value is a valid timestamp."""
    if isinstance(value, bool):
        return False
    if not (
        isinstance(value, numbers.Integral)
        or isinstance(value, float)
        or isinstance(value, str)
    ):
        return False
    try:
        float(value)
        return True
    except ValueError:
        return False


def normalize_timestamp(timestamp):
    """Normalize millisecond and microsecond timestamps into normal timestamps."""
    if timestamp > MAX_TIMESTAMP:
        if timestamp < MAX_TIMESTAMP_MS:
            timestamp /= 1e3
        elif timestamp < MAX_TIMESTAMP_US:
            timestamp /= 1e6
        else:
            raise ValueError(f"The specified timestamp '{timestamp}' is too large.")
    return timestamp


# Credit to https://stackoverflow.com/a/1700069
def iso_to_gregorian(
    iso_year: int, iso_week: int, iso_day: int
) -> Union[date, datetime]:
    """Converts an ISO week date tuple into a datetime object."""

    if not 1 <= iso_week <= 53:
        raise ValueError("ISO Calendar week value must be between 1-53.")

    if not 1 <= iso_day <= 7:
        raise ValueError("ISO Calendar day value must be between 1-7")

    # The first week of the year always contains 4 Jan.
    fourth_jan: date = dt.date(iso_year, 1, 4)
    delta: timedelta = dt.timedelta(fourth_jan.isoweekday() - 1)
    year_start: date = fourth_jan - delta
    gregorian = year_start + dt.timedelta(days=iso_day - 1, weeks=iso_week - 1)

    return gregorian


__all__ = ["total_seconds", "is_timestamp", "iso_to_gregorian"]
