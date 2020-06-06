import datetime as dt
from datetime import date, datetime, timedelta
from typing import Any, Union


def total_seconds(td: timedelta) -> float:
    """Get total seconds for timedelta."""
    return td.total_seconds()


def is_timestamp(value: Any) -> bool:
    """Check if value is a valid timestamp."""
    if isinstance(value, bool):
        return False
    if not (
        isinstance(value, int) or isinstance(value, float) or isinstance(value, str)
    ):
        return False
    try:
        float(value)
        return True
    except ValueError:
        return False


# Credit to https://stackoverflow.com/a/1700069
def iso_to_gregorian(
    iso_year: datetime, iso_week: int, iso_day: int
) -> Union[date, datetime]:
    """Converts an ISO week date tuple into a datetime object."""

    if not 1 <= iso_week <= 53:
        raise ValueError("ISO Calendar week value must be between 1-53.")

    if not 1 <= iso_day <= 7:
        raise ValueError("ISO Calendar day value must be between 1-7")

    # The first week of the year always contains 4 Jan.
    fourth_jan = dt.date(iso_year, 1, 4)
    delta = dt.timedelta(fourth_jan.isoweekday() - 1)
    year_start = fourth_jan - delta
    gregorian = year_start + dt.timedelta(days=iso_day - 1, weeks=iso_week - 1)

    return gregorian


# Python 2.7 / 3.0+ definitions for isstr function.

try:  # pragma: no cover
    basestring

    def isstr(s):
        return isinstance(s, basestring)  # noqa: F821


except NameError:  # pragma: no cover

    def isstr(s: Any) -> bool:
        return isinstance(s, str)


__all__ = ["total_seconds", "is_timestamp", "isstr", "iso_to_gregorian"]
