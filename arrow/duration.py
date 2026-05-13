"""
Provides the :class:`Duration <arrow.duration.Duration>` class for ISO 8601
duration parsing, formatting, and arithmetic with Arrow objects.

ISO 8601 durations follow the format: P[n]Y[n]M[n]DT[n]H[n]M[n]S

Examples:
    P1Y2M3DT4H5M6S -> 1 year, 2 months, 3 days, 4 hours, 5 minutes, 6 seconds
    P3D            -> 3 days
    PT12H          -> 12 hours
    P1Y6M          -> 1 year, 6 months
    P0.5Y          -> 0.5 years
"""

import re
from datetime import timedelta
from typing import Optional, Union

from dateutil.relativedelta import relativedelta

_ISO8601_DURATION_RE = re.compile(
    r"^P"
    r"(?:(?P<years>\d+(?:\.\d+)?)Y)?"
    r"(?:(?P<months>\d+(?:\.\d+)?)M)?"
    r"(?:(?P<weeks>\d+(?:\.\d+)?)W)?"
    r"(?:(?P<days>\d+(?:\.\d+)?)D)?"
    r"(?:T"
    r"(?:(?P<hours>\d+(?:\.\d+)?)H)?"
    r"(?:(?P<minutes>\d+(?:\.\d+)?)M)?"
    r"(?:(?P<seconds>\d+(?:\.\d+)?)S)?"
    r")?$"
)


class Duration:
    """Represents an ISO 8601 duration.

    A duration consists of years, months, weeks, days, hours, minutes,
    and seconds. Unlike a :class:`datetime.timedelta`, a Duration can
    represent calendar-based intervals (years, months) that don't have
    a fixed number of days.

    Usage::

        >>> from arrow.duration import Duration
        >>> d = Duration.parse("P1Y2M3DT4H5M6S")
        >>> d.years
        1
        >>> d.months
        2
        >>> d.days
        3
        >>> d.hours
        4
        >>> d.minutes
        5
        >>> d.seconds
        6
        >>> str(d)
        'P1Y2M3DT4H5M6S'

    Durations can be applied to Arrow objects::

        >>> import arrow
        >>> arw = arrow.get("2020-01-01")
        >>> d = Duration.parse("P1Y2M")
        >>> arw + d
        <Arrow [2021-03-01T00:00:00+00:00]>

    """

    def __init__(
        self,
        years: Union[int, float] = 0,
        months: Union[int, float] = 0,
        weeks: Union[int, float] = 0,
        days: Union[int, float] = 0,
        hours: Union[int, float] = 0,
        minutes: Union[int, float] = 0,
        seconds: Union[int, float] = 0,
    ) -> None:
        self.years = years
        self.months = months
        self.weeks = weeks
        self.days = days
        self.hours = hours
        self.minutes = minutes
        self.seconds = seconds

    @classmethod
    def parse(cls, iso_string: str) -> "Duration":
        """Parse an ISO 8601 duration string into a Duration object.

        Parameters:
            iso_string: An ISO 8601 duration string (e.g., ``"P1Y2M3DT4H5M6S"``).

        Returns:
            A new :class:`Duration` instance.

        Raises:
            ValueError: If the string is not a valid ISO 8601 duration.
        """
        if not iso_string:
            raise ValueError("Duration string cannot be empty.")

        match = _ISO8601_DURATION_RE.match(iso_string)
        if not match:
            raise ValueError(f"Invalid ISO 8601 duration: {iso_string!r}")

        groups = match.groupdict()

        # At least one component must be present
        if all(v is None for v in groups.values()):
            raise ValueError(f"Invalid ISO 8601 duration: {iso_string!r}")

        def _to_num(val: Optional[str]) -> Union[int, float]:
            if val is None:
                return 0
            f = float(val)
            return int(f) if f == int(f) else f

        return cls(
            years=_to_num(groups["years"]),
            months=_to_num(groups["months"]),
            weeks=_to_num(groups["weeks"]),
            days=_to_num(groups["days"]),
            hours=_to_num(groups["hours"]),
            minutes=_to_num(groups["minutes"]),
            seconds=_to_num(groups["seconds"]),
        )

    @classmethod
    def from_timedelta(cls, td: timedelta) -> "Duration":
        """Create a Duration from a :class:`datetime.timedelta`.

        Note: Only days and seconds are preserved. Years and months
        cannot be inferred from a timedelta.
        """
        total_seconds = int(td.total_seconds())
        days, remainder = divmod(abs(total_seconds), 86400)
        hours, remainder = divmod(remainder, 3600)
        minutes, seconds = divmod(remainder, 60)

        # Handle sub-second precision
        microseconds = td.microseconds
        total_seconds_val: Union[int, float] = seconds
        if microseconds:
            total_seconds_val = seconds + microseconds / 1_000_000

        return cls(
            days=days,
            hours=hours,
            minutes=minutes,
            seconds=total_seconds_val,
        )

    def to_relativedelta(self) -> relativedelta:
        """Convert this Duration to a :class:`dateutil.relativedelta.relativedelta`.

        This is used internally for arithmetic with Arrow objects.
        """
        return relativedelta(
            years=int(self.years),
            months=int(self.months),
            weeks=int(self.weeks),
            days=int(self.days),
            hours=int(self.hours),
            minutes=int(self.minutes),
            seconds=int(self.seconds),
            microseconds=int((self.seconds - int(self.seconds)) * 1_000_000),
        )

    def to_timedelta(self) -> timedelta:
        """Convert to a :class:`datetime.timedelta`.

        Note: Years are approximated as 365.25 days and months as 30.44 days.
        For exact arithmetic, use :meth:`to_relativedelta` or apply the
        duration to an Arrow object directly.
        """
        total_days = (
            self.years * 365.25 + self.months * 30.44 + self.weeks * 7 + self.days
        )
        total_seconds = self.hours * 3600 + self.minutes * 60 + self.seconds
        return timedelta(days=total_days, seconds=total_seconds)

    def isoformat(self) -> str:
        """Format as an ISO 8601 duration string.

        Returns:
            An ISO 8601 duration string (e.g., ``"P1Y2M3DT4H5M6S"``).
        """
        date_parts = []
        time_parts = []

        if self.years:
            date_parts.append(f"{_format_num(self.years)}Y")
        if self.months:
            date_parts.append(f"{_format_num(self.months)}M")
        if self.weeks:
            date_parts.append(f"{_format_num(self.weeks)}W")
        if self.days:
            date_parts.append(f"{_format_num(self.days)}D")

        if self.hours:
            time_parts.append(f"{_format_num(self.hours)}H")
        if self.minutes:
            time_parts.append(f"{_format_num(self.minutes)}M")
        if self.seconds:
            time_parts.append(f"{_format_num(self.seconds)}S")

        result = "P" + "".join(date_parts)
        if time_parts:
            result += "T" + "".join(time_parts)

        # If everything is zero, return P0D
        if result == "P":
            result = "P0D"

        return result

    def __str__(self) -> str:
        return self.isoformat()

    def __repr__(self) -> str:
        parts = []
        for attr in ("years", "months", "weeks", "days", "hours", "minutes", "seconds"):
            val = getattr(self, attr)
            if val:
                parts.append(f"{attr}={val!r}")
        return f"Duration({', '.join(parts)})" if parts else "Duration()"

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Duration):
            return (
                self.years == other.years
                and self.months == other.months
                and self.weeks == other.weeks
                and self.days == other.days
                and self.hours == other.hours
                and self.minutes == other.minutes
                and self.seconds == other.seconds
            )
        return NotImplemented

    def __neg__(self) -> "Duration":
        return Duration(
            years=-self.years,
            months=-self.months,
            weeks=-self.weeks,
            days=-self.days,
            hours=-self.hours,
            minutes=-self.minutes,
            seconds=-self.seconds,
        )

    def __add__(self, other: object) -> Union["Duration", object]:
        if isinstance(other, Duration):
            return Duration(
                years=self.years + other.years,
                months=self.months + other.months,
                weeks=self.weeks + other.weeks,
                days=self.days + other.days,
                hours=self.hours + other.hours,
                minutes=self.minutes + other.minutes,
                seconds=self.seconds + other.seconds,
            )
        return NotImplemented

    def __radd__(self, other: object) -> object:
        # Support Arrow + Duration
        from arrow.arrow import Arrow

        if isinstance(other, Arrow):
            return other.shift(
                years=int(self.years),
                months=int(self.months),
                weeks=int(self.weeks),
                days=int(self.days),
                hours=int(self.hours),
                minutes=int(self.minutes),
                seconds=int(self.seconds),
            )
        return NotImplemented

    def __sub__(self, other: object) -> Union["Duration", object]:
        if isinstance(other, Duration):
            return self + (-other)
        return NotImplemented

    def __hash__(self) -> int:
        return hash(
            (
                self.years,
                self.months,
                self.weeks,
                self.days,
                self.hours,
                self.minutes,
                self.seconds,
            )
        )


def _format_num(val: Union[int, float]) -> str:
    """Format a number, dropping unnecessary decimal places."""
    if isinstance(val, float) and val == int(val):
        return str(int(val))
    return str(val)
