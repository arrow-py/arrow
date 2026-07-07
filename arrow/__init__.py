import datetime

from ._version import __version__
from .api import get, now, utcnow
from .arrow import Arrow
from .factory import ArrowFactory
from .formatter import (
    FORMAT_ATOM,
    FORMAT_COOKIE,
    FORMAT_RFC822,
    FORMAT_RFC850,
    FORMAT_RFC1036,
    FORMAT_RFC1123,
    FORMAT_RFC2822,
    FORMAT_RFC3339,
    FORMAT_RFC3339_STRICT,
    FORMAT_RSS,
    FORMAT_W3C,
)
from .parser import ParserError, TzinfoParser


def timezone(tzinfo_string: str) -> datetime.tzinfo:
    """Return a :class:`datetime.timezone` object for the given timezone string.

    This function wraps the existing TzinfoParser to provide a convenient
    interface for creating timezone objects from strings.

    :param tzinfo_string: The timezone string to parse, e.g. "US/Pacific",
        "UTC", "+05:30".
    :returns: The parsed datetime timezone object.
    :rtype: datetime.timezone
    :raises ParserError: If the timezone string cannot be parsed.

    .. code-block:: python

        >>> import arrow
        >>> arrow.timezone("US/Pacific")
        tzfile('/usr/share/zoneinfo/US/Pacific')
        >>> arrow.timezone("UTC")
        datetime.timezone.utc
    """
    return TzinfoParser.parse(tzinfo_string)

# https://mypy.readthedocs.io/en/stable/command_line.html#cmdoption-mypy-no-implicit-reexport
# Mypy with --strict or --no-implicit-reexport requires an explicit reexport.
__all__ = [
    "__version__",
    "get",
    "now",
    "utcnow",
    "Arrow",
    "ArrowFactory",
    "FORMAT_ATOM",
    "FORMAT_COOKIE",
    "FORMAT_RFC822",
    "FORMAT_RFC850",
    "FORMAT_RFC1036",
    "FORMAT_RFC1123",
    "FORMAT_RFC2822",
    "FORMAT_RFC3339",
    "FORMAT_RFC3339_STRICT",
    "FORMAT_RSS",
    "FORMAT_W3C",
    "ParserError",
    "timezone",
]
