"""
Provides the :class:`Arrow <arrow.arrow.Arrow>` class, an enhanced ``datetime``
replacement.

"""
# from __future__ import annotations

import calendar
import sys
from datetime import date, datetime, time, timedelta
from datetime import tzinfo as dt_tzinfo
from math import trunc
from time import struct_time
from typing import Any, Iterator, List, Optional, Tuple, Union

from dateutil import tz as dateutil_tz
from dateutil.relativedelta import relativedelta
from dateutil.tz.tz import tzfile, tzlocal, tzutc

from arrow import formatter, locales, parser, util
from arrow.locales import Locale


class Arrow:
    """An :class:`Arrow <arrow.arrow.Arrow>` object.

    Implements the ``datetime`` interface, behaving as an aware ``datetime`` while implementing
    additional functionality.

    :param year: the calendar year.
    :param month: the calendar month.
    :param day: the calendar day.
    :param hour: (optional) the hour. Defaults to 0.
    :param minute: (optional) the minute, Defaults to 0.
    :param second: (optional) the second, Defaults to 0.
    :param microsecond: (optional) the microsecond. Defaults 0.
    :param tzinfo: (optional) A timezone expression.  Defaults to UTC.

    .. _tz-expr:

    Recognized timezone expressions:

        - A ``tzinfo`` object.
        - A ``str`` describing a timezone, similar to 'US/Pacific', or 'Europe/Berlin'.
        - A ``str`` in ISO 8601 style, as in '+07:00'.
        - A ``str``, one of the following:  'local', 'utc', 'UTC'.

    Usage::

        >>> import arrow
        >>> arrow.Arrow(2013, 5, 5, 12, 30, 45)
        <Arrow [2013-05-05T12:30:45+00:00]>

    """

    resolution = datetime.resolution
    min: "Arrow"
    max: "Arrow"

    _ATTRS = ["year", "month", "day", "hour", "minute", "second", "microsecond"]
    _ATTRS_PLURAL = [f"{a}s" for a in _ATTRS]
    _MONTHS_PER_QUARTER = 3
    _SECS_PER_MINUTE = float(60)
    _SECS_PER_HOUR = float(60 * 60)
    _SECS_PER_DAY = float(60 * 60 * 24)
    _SECS_PER_WEEK = float(60 * 60 * 24 * 7)
    _SECS_PER_MONTH = float(60 * 60 * 24 * 30.5)
    _SECS_PER_YEAR = float(60 * 60 * 24 * 365.25)

    def __init__(
        self,
        year: int,
        month: int,
        day: int,
        hour: int = 0,
        minute: int = 0,
        second: int = 0,
        microsecond: int = 0,
        tzinfo: Optional[Union["dt_tzinfo", tzfile]] = None,
    ) -> None:
        if tzinfo is None:
            tzinfo = dateutil_tz.tzutc()
        # detect that tzinfo is a pytz object (issue #626)
        elif (
            isinstance(tzinfo, dt_tzinfo)
            and hasattr(tzinfo, "localize")
            and hasattr(tzinfo, "zone")
            and tzinfo.zone
        ):
            tzinfo = parser.TzinfoParser.parse(tzinfo.zone)
        elif util.isstr(tzinfo):
            tzinfo = parser.TzinfoParser.parse(tzinfo)

        self._datetime = datetime(
            year, month, day, hour, minute, second, microsecond, tzinfo
        )

    # factories: single object, both original and from datetime.

    @classmethod
    def now(
        cls, tzinfo: Optional[Union[tzfile, tzlocal, "dt_tzinfo"]] = None
    ) -> "Arrow":  # tzinfo is type tzinfo
        """Constructs an :class:`Arrow <arrow.arrow.Arrow>` object, representing "now" in the given
        timezone.

        :param tzinfo: (optional) a ``tzinfo`` object. Defaults to local time.

        Usage::

            >>> arrow.now('Asia/Baku')
            <Arrow [2019-01-24T20:26:31.146412+04:00]>

        """

        if tzinfo is None:
            tzinfo = dateutil_tz.tzlocal()
        dt = datetime.now(tzinfo)

        return cls(
            dt.year,
            dt.month,
            dt.day,
            dt.hour,
            dt.minute,
            dt.second,
            dt.microsecond,
            dt.tzinfo,
        )

    @classmethod
    def utcnow(cls) -> "Arrow":
        """ Constructs an :class:`Arrow <arrow.arrow.Arrow>` object, representing "now" in UTC
        time.

        Usage::

            >>> arrow.utcnow()
            <Arrow [2019-01-24T16:31:40.651108+00:00]>

        """

        dt = datetime.now(dateutil_tz.tzutc())

        return cls(
            dt.year,
            dt.month,
            dt.day,
            dt.hour,
            dt.minute,
            dt.second,
            dt.microsecond,
            dt.tzinfo,
        )

    @classmethod
    def fromtimestamp(
        cls, timestamp: Union[float, str], tzinfo: Optional[Any] = None
    ) -> "Arrow":
        """ Constructs an :class:`Arrow <arrow.arrow.Arrow>` object from a timestamp, converted to
        the given timezone.

        :param timestamp: an ``int`` or ``float`` timestamp, or a ``str`` that converts to either.
        :param tzinfo: (optional) a ``tzinfo`` object.  Defaults to local time.
        """

        if tzinfo is None:
            tzinfo = dateutil_tz.tzlocal()
        elif util.isstr(tzinfo):
            tzinfo = parser.TzinfoParser.parse(tzinfo)

        if not util.is_timestamp(timestamp):
            raise ValueError(f"The provided timestamp '{timestamp}' is invalid.")

        dt = datetime.fromtimestamp(float(timestamp), tzinfo)

        return cls(
            dt.year,
            dt.month,
            dt.day,
            dt.hour,
            dt.minute,
            dt.second,
            dt.microsecond,
            dt.tzinfo,
        )

    @classmethod
    def utcfromtimestamp(cls, timestamp: Union[float, str]) -> "Arrow":
        """Constructs an :class:`Arrow <arrow.arrow.Arrow>` object from a timestamp, in UTC time.

        :param timestamp: an ``int`` or ``float`` timestamp, or a ``str`` that converts to either.

        """

        if not util.is_timestamp(timestamp):
            raise ValueError(f"The provided timestamp '{timestamp}' is invalid.")

        dt = datetime.utcfromtimestamp(float(timestamp))

        return cls(
            dt.year,
            dt.month,
            dt.day,
            dt.hour,
            dt.minute,
            dt.second,
            dt.microsecond,
            dateutil_tz.tzutc(),
        )

    @classmethod
    def fromdatetime(cls, dt: Union[datetime, "Arrow"], tzinfo: Any = None) -> "Arrow":
        """ Constructs an :class:`Arrow <arrow.arrow.Arrow>` object from a ``datetime`` and
        optional replacement timezone.

        :param dt: the ``datetime``
        :param tzinfo: (optional) A :ref:`timezone expression <tz-expr>`.  Defaults to ``dt``'s
            timezone, or UTC if naive.

        If you only want to replace the timezone of naive datetimes::

            >>> dt
            datetime.datetime(2013, 5, 5, 0, 0, tzinfo=tzutc())
            >>> arrow.Arrow.fromdatetime(dt, dt.tzinfo or 'US/Pacific')
            <Arrow [2013-05-05T00:00:00+00:00]>

        """

        if tzinfo is None:
            if dt.tzinfo is None:
                tzinfo = dateutil_tz.tzutc()
            else:
                tzinfo = dt.tzinfo

        return cls(
            dt.year,
            dt.month,
            dt.day,
            dt.hour,
            dt.minute,
            dt.second,
            dt.microsecond,
            tzinfo,
        )

    @classmethod
    def fromdate(
        cls, date: date, tzinfo: Optional[Union[dt_tzinfo, tzfile, str, None]] = None
    ) -> "Arrow":
        """ Constructs an :class:`Arrow <arrow.arrow.Arrow>` object from a ``date`` and optional
        replacement timezone.  Time values are set to 0.

        :param date: the ``date``
        :param tzinfo: (optional) A :ref:`timezone expression <tz-expr>`.  Defaults to UTC.
        """

        if tzinfo is None:
            tzinfo = dateutil_tz.tzutc()

        return cls(date.year, date.month, date.day, tzinfo=tzinfo)

    @classmethod
    def strptime(
        cls, date_str: str, fmt: str, tzinfo: Optional[Union[tzfile, dt_tzinfo]] = None
    ) -> "Arrow":
        """ Constructs an :class:`Arrow <arrow.arrow.Arrow>` object from a date string and format,
        in the style of ``datetime.strptime``.  Optionally replaces the parsed timezone.

        :param date_str: the date string.
        :param fmt: the format string.
        :param tzinfo: (optional) A :ref:`timezone expression <tz-expr>`.  Defaults to the parsed
            timezone if ``fmt`` contains a timezone directive, otherwise UTC.

        Usage::

            >>> arrow.Arrow.strptime('20-01-2019 15:49:10', '%d-%m-%Y %H:%M:%S')
            <Arrow [2019-01-20T15:49:10+00:00]>

        """

        dt = datetime.strptime(date_str, fmt)
        if tzinfo is None:
            tzinfo = dt.tzinfo

        return cls(
            dt.year,
            dt.month,
            dt.day,
            dt.hour,
            dt.minute,
            dt.second,
            dt.microsecond,
            tzinfo,
        )

    # factories: ranges and spans

    @classmethod
    def range(
        cls,
        frame: str,
        start: Union["Arrow", datetime],
        end: Optional[Union["Arrow", datetime]] = None,
        tz: Optional[Union[None, tzfile, str]] = None,
        limit: Optional[int] = None,
    ) -> Union[Iterator[Union[Iterator, Iterator["Arrow"]]], "Arrow"]:
        """ Returns an iterator of :class:`Arrow <arrow.arrow.Arrow>` objects, representing
        points in time between two inputs.

        :param frame: The timeframe.  Can be any ``datetime`` property (day, hour, minute...).
        :param start: A datetime expression, the start of the range.
        :param end: (optional) A datetime expression, the end of the range.
        :param tz: (optional) A :ref:`timezone expression <tz-expr>`.  Defaults to
            ``start``'s timezone, or UTC if ``start`` is naive.
        :param limit: (optional) A maximum number of tuples to return.

        **NOTE**: The ``end`` or ``limit`` must be provided.  Call with ``end`` alone to
        return the entire range.  Call with ``limit`` alone to return a maximum # of results from
        the start.  Call with both to cap a range at a maximum # of results.

        **NOTE**: ``tz`` internally **replaces** the timezones of both ``start`` and ``end`` before
        iterating.  As such, either call with naive objects and ``tz``, or aware objects from the
        same timezone and no ``tz``.

        Supported frame values: year, quarter, month, week, day, hour, minute, second.

        Recognized datetime expressions:

            - An :class:`Arrow <arrow.arrow.Arrow>` object.
            - A ``datetime`` object.

        Usage::

            >>> start = datetime(2013, 5, 5, 12, 30)
            >>> end = datetime(2013, 5, 5, 17, 15)
            >>> for r in arrow.Arrow.range('hour', start, end):
            ...     print(repr(r))
            ...
            <Arrow [2013-05-05T12:30:00+00:00]>
            <Arrow [2013-05-05T13:30:00+00:00]>
            <Arrow [2013-05-05T14:30:00+00:00]>
            <Arrow [2013-05-05T15:30:00+00:00]>
            <Arrow [2013-05-05T16:30:00+00:00]>

        **NOTE**: Unlike Python's ``range``, ``end`` *may* be included in the returned iterator::

            >>> start = datetime(2013, 5, 5, 12, 30)
            >>> end = datetime(2013, 5, 5, 13, 30)
            >>> for r in arrow.Arrow.range('hour', start, end):
            ...     print(repr(r))
            ...
            <Arrow [2013-05-05T12:30:00+00:00]>
            <Arrow [2013-05-05T13:30:00+00:00]>

        """

        _, frame_relative, relative_steps = cls._get_frames(frame)

        tzinfo = cls._get_tzinfo(start.tzinfo if tz is None else tz)

        _start: Union["Arrow", datetime] = cls._get_datetime(start).replace(
            tzinfo=tzinfo
        )
        _end, limit = cls._get_iteration_params(end, limit)
        __end = cls._get_datetime(_end).replace(tzinfo=tzinfo)

        current: Union["Arrow", datetime] = cls.fromdatetime(_start)
        i = 0

        while current <= __end and i < limit:
            i += 1
            yield current

            values = [getattr(current, f) for f in cls._ATTRS]
            current = cls(*values, tzinfo=tzinfo) + relativedelta(
                **{frame_relative: relative_steps}
            )

    @classmethod
    def span_range(
        cls,
        frame: str,
        start: datetime,
        end: datetime,
        tz: Optional[str] = None,
        limit: Optional[Any] = None,
        bounds: str = "[)",
    ) -> Iterator:
        """ Returns an iterator of tuples, each :class:`Arrow <arrow.arrow.Arrow>` objects,
        representing a series of timespans between two inputs.

        :param frame: The timeframe.  Can be any ``datetime`` property (day, hour, minute...).
        :param start: A datetime expression, the start of the range.
        :param end: (optional) A datetime expression, the end of the range.
        :param tz: (optional) A :ref:`timezone expression <tz-expr>`.  Defaults to
            ``start``'s timezone, or UTC if ``start`` is naive.
        :param limit: (optional) A maximum number of tuples to return.
        :param bounds: (optional) a ``str`` of either '()', '(]', '[)', or '[]' that specifies
            whether to include or exclude the start and end values in each span in the range. '(' excludes
            the start, '[' includes the start, ')' excludes the end, and ']' includes the end.
            If the bounds are not specified, the default bound '[)' is used.

        **NOTE**: The ``end`` or ``limit`` must be provided.  Call with ``end`` alone to
        return the entire range.  Call with ``limit`` alone to return a maximum # of results from
        the start.  Call with both to cap a range at a maximum # of results.

        **NOTE**: ``tz`` internally **replaces** the timezones of both ``start`` and ``end`` before
        iterating.  As such, either call with naive objects and ``tz``, or aware objects from the
        same timezone and no ``tz``.

        Supported frame values: year, quarter, month, week, day, hour, minute, second.

        Recognized datetime expressions:

            - An :class:`Arrow <arrow.arrow.Arrow>` object.
            - A ``datetime`` object.

        **NOTE**: Unlike Python's ``range``, ``end`` will *always* be included in the returned
        iterator of timespans.

        Usage:

            >>> start = datetime(2013, 5, 5, 12, 30)
            >>> end = datetime(2013, 5, 5, 17, 15)
            >>> for r in arrow.Arrow.span_range('hour', start, end):
            ...     print(r)
            ...
            (<Arrow [2013-05-05T12:00:00+00:00]>, <Arrow [2013-05-05T12:59:59.999999+00:00]>)
            (<Arrow [2013-05-05T13:00:00+00:00]>, <Arrow [2013-05-05T13:59:59.999999+00:00]>)
            (<Arrow [2013-05-05T14:00:00+00:00]>, <Arrow [2013-05-05T14:59:59.999999+00:00]>)
            (<Arrow [2013-05-05T15:00:00+00:00]>, <Arrow [2013-05-05T15:59:59.999999+00:00]>)
            (<Arrow [2013-05-05T16:00:00+00:00]>, <Arrow [2013-05-05T16:59:59.999999+00:00]>)
            (<Arrow [2013-05-05T17:00:00+00:00]>, <Arrow [2013-05-05T17:59:59.999999+00:00]>)

        """

        tzinfo: dt_tzinfo = cls._get_tzinfo(start.tzinfo if tz is None else tz)
        _start: Union[datetime, Arrow] = cls.fromdatetime(start, tzinfo).span(frame)[0]
        _range: Union[
            Iterator[Union[Iterator[Any], Iterator[Arrow]]], Arrow
        ] = cls.range(frame, _start, end, tz, limit)
        return (r.span(frame, bounds=bounds) for r in _range)

    @classmethod
    def interval(
        cls,
        frame: str,
        start: datetime,
        end: datetime,
        interval: int = 1,
        tz: Optional[Any] = None,
        bounds: str = "[)",
    ) -> Iterator[Union[Iterator, Iterator[Tuple["Arrow", "Arrow"]]]]:
        """ Returns an iterator of tuples, each :class:`Arrow <arrow.arrow.Arrow>` objects,
        representing a series of intervals between two inputs.

        :param frame: The timeframe.  Can be any ``datetime`` property (day, hour, minute...).
        :param start: A datetime expression, the start of the range.
        :param end: (optional) A datetime expression, the end of the range.
        :param interval: (optional) Time interval for the given time frame.
        :param tz: (optional) A timezone expression.  Defaults to UTC.
        :param bounds: (optional) a ``str`` of either '()', '(]', '[)', or '[]' that specifies
            whether to include or exclude the start and end values in the intervals. '(' excludes
            the start, '[' includes the start, ')' excludes the end, and ']' includes the end.
            If the bounds are not specified, the default bound '[)' is used.

        Supported frame values: year, quarter, month, week, day, hour, minute, second

        Recognized datetime expressions:

            - An :class:`Arrow <arrow.arrow.Arrow>` object.
            - A ``datetime`` object.

        Recognized timezone expressions:

            - A ``tzinfo`` object.
            - A ``str`` describing a timezone, similar to 'US/Pacific', or 'Europe/Berlin'.
            - A ``str`` in ISO 8601 style, as in '+07:00'.
            - A ``str``, one of the following:  'local', 'utc', 'UTC'.

        Usage:

            >>> start = datetime(2013, 5, 5, 12, 30)
            >>> end = datetime(2013, 5, 5, 17, 15)
            >>> for r in arrow.Arrow.interval('hour', start, end, 2):
            ...     print r
            ...
            (<Arrow [2013-05-05T12:00:00+00:00]>, <Arrow [2013-05-05T13:59:59.999999+00:00]>)
            (<Arrow [2013-05-05T14:00:00+00:00]>, <Arrow [2013-05-05T15:59:59.999999+00:00]>)
            (<Arrow [2013-05-05T16:00:00+00:00]>, <Arrow [2013-05-05T17:59:59.999999+00:0]>)
        """
        if interval < 1:
            raise ValueError("interval has to be a positive integer")

        spanRange = iter(cls.span_range(frame, start, end, tz, bounds=bounds))
        while True:
            try:
                intvlStart, intvlEnd = next(spanRange)
                for _ in range(interval - 1):
                    _, intvlEnd = next(spanRange)
                yield intvlStart, intvlEnd
            except StopIteration:
                return

    # representations

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} [{self.__str__()}]>"

    def __str__(self) -> str:
        return self._datetime.isoformat()

    def __format__(self, formatstr: str) -> str:

        if len(formatstr) > 0:
            return self.format(formatstr)

        return str(self)

    def __hash__(self) -> int:
        return self._datetime.__hash__()

    # attributes & properties

    def __getattr__(self, name: str) -> int:

        if name == "week":
            return self.isocalendar()[1]

        if name == "quarter":
            return int((self.month - 1) / self._MONTHS_PER_QUARTER) + 1

        if not name.startswith("_"):
            value = getattr(self._datetime, name, None)

            if value is not None:
                return value

        return object.__getattribute__(self, name)

    @property
    def tzinfo(self) -> Any:
        """ Gets the ``tzinfo`` of the :class:`Arrow <arrow.arrow.Arrow>` object.

        Usage::

            >>> arw=arrow.utcnow()
            >>> arw.tzinfo
            tzutc()

        """

        return self._datetime.tzinfo

    @tzinfo.setter
    def tzinfo(self, tzinfo: Optional[Any]) -> None:
        """ Sets the ``tzinfo`` of the :class:`Arrow <arrow.arrow.Arrow>` object. """

        self._datetime = self._datetime.replace(tzinfo=tzinfo)

    @property
    def datetime(self) -> datetime:
        """ Returns a datetime representation of the :class:`Arrow <arrow.arrow.Arrow>` object.

        Usage::

            >>> arw=arrow.utcnow()
            >>> arw.datetime
            datetime.datetime(2019, 1, 24, 16, 35, 27, 276649, tzinfo=tzutc())

        """

        return self._datetime

    @property
    def naive(self) -> datetime:
        """ Returns a naive datetime representation of the :class:`Arrow <arrow.arrow.Arrow>`
        object.

        Usage::

            >>> nairobi = arrow.now('Africa/Nairobi')
            >>> nairobi
            <Arrow [2019-01-23T19:27:12.297999+03:00]>
            >>> nairobi.naive
            datetime.datetime(2019, 1, 23, 19, 27, 12, 297999)

        """

        return self._datetime.replace(tzinfo=None)

    @property
    def timestamp(self) -> int:
        """ Returns a timestamp representation of the :class:`Arrow <arrow.arrow.Arrow>` object, in
        UTC time.

        Usage::

            >>> arrow.utcnow().timestamp
            1548260567

        """

        return calendar.timegm(self._datetime.utctimetuple())

    @property
    def float_timestamp(self) -> float:
        """ Returns a floating-point representation of the :class:`Arrow <arrow.arrow.Arrow>`
        object, in UTC time.

        Usage::

            >>> arrow.utcnow().float_timestamp
            1548260516.830896

        """

        return self.timestamp + float(self.microsecond) / 1000000

    # mutation and duplication.

    def clone(self) -> "Arrow":
        """ Returns a new :class:`Arrow <arrow.arrow.Arrow>` object, cloned from the current one.

        Usage:

            >>> arw = arrow.utcnow()
            >>> cloned = arw.clone()

        """

        return self.fromdatetime(self._datetime)

    def replace(self, **kwargs: Any) -> "Arrow":
        """ Returns a new :class:`Arrow <arrow.arrow.Arrow>` object with attributes updated
        according to inputs.

        Use property names to set their value absolutely::

            >>> import arrow
            >>> arw = arrow.utcnow()
            >>> arw
            <Arrow [2013-05-11T22:27:34.787885+00:00]>
            >>> arw.replace(year=2014, month=6)
            <Arrow [2014-06-11T22:27:34.787885+00:00]>

        You can also replace the timezone without conversion, using a
        :ref:`timezone expression <tz-expr>`::

            >>> arw.replace(tzinfo=tz.tzlocal())
            <Arrow [2013-05-11T22:27:34.787885-07:00]>

        """

        absolute_kwargs = {}

        for key, value in kwargs.items():

            if key in self._ATTRS:
                absolute_kwargs[key] = value
            elif key in ["week", "quarter"]:
                raise AttributeError(f"setting absolute {key} is not supported")
            elif key != "tzinfo":
                raise AttributeError(f'unknown attribute: "{key}"')

        current = self._datetime.replace(**absolute_kwargs)

        tzinfo = kwargs.get("tzinfo")

        if tzinfo is not None:
            tzinfo = self._get_tzinfo(tzinfo)
            current = current.replace(tzinfo=tzinfo)

        return self.fromdatetime(current)

    def shift(self, **kwargs: Any) -> "Arrow":
        """ Returns a new :class:`Arrow <arrow.arrow.Arrow>` object with attributes updated
        according to inputs.

        Use pluralized property names to relatively shift their current value:

        >>> import arrow
        >>> arw = arrow.utcnow()
        >>> arw
        <Arrow [2013-05-11T22:27:34.787885+00:00]>
        >>> arw.shift(years=1, months=-1)
        <Arrow [2014-04-11T22:27:34.787885+00:00]>

        Day-of-the-week relative shifting can use either Python's weekday numbers
        (Monday = 0, Tuesday = 1 .. Sunday = 6) or using dateutil.relativedelta's
        day instances (MO, TU .. SU).  When using weekday numbers, the returned
        date will always be greater than or equal to the starting date.

        Using the above code (which is a Saturday) and asking it to shift to Saturday:

        >>> arw.shift(weekday=5)
        <Arrow [2013-05-11T22:27:34.787885+00:00]>

        While asking for a Monday:

        >>> arw.shift(weekday=0)
        <Arrow [2013-05-13T22:27:34.787885+00:00]>

        """

        relative_kwargs = {}
        additional_attrs = ["weeks", "quarters", "weekday"]

        for key, value in kwargs.items():

            if key in self._ATTRS_PLURAL or key in additional_attrs:
                relative_kwargs[key] = value
            else:
                raise AttributeError(
                    f"Invalid shift time frame. Please select one of the following: {', '.join(self._ATTRS_PLURAL + additional_attrs)}."
                )

        # core datetime does not support quarters, translate to months.
        relative_kwargs.setdefault("months", 0)
        relative_kwargs["months"] += (
            relative_kwargs.pop("quarters", 0) * self._MONTHS_PER_QUARTER
        )

        current = self._datetime + relativedelta(**relative_kwargs)

        return self.fromdatetime(current)

    def to(self, tz: Union[tzutc, str]) -> "Arrow":
        """ Returns a new :class:`Arrow <arrow.arrow.Arrow>` object, converted
        to the target timezone.

        :param tz: A :ref:`timezone expression <tz-expr>`.

        Usage::

            >>> utc = arrow.utcnow()
            >>> utc
            <Arrow [2013-05-09T03:49:12.311072+00:00]>

            >>> utc.to('US/Pacific')
            <Arrow [2013-05-08T20:49:12.311072-07:00]>

            >>> utc.to(tz.tzlocal())
            <Arrow [2013-05-08T20:49:12.311072-07:00]>

            >>> utc.to('-07:00')
            <Arrow [2013-05-08T20:49:12.311072-07:00]>

            >>> utc.to('local')
            <Arrow [2013-05-08T20:49:12.311072-07:00]>

            >>> utc.to('local').to('utc')
            <Arrow [2013-05-09T03:49:12.311072+00:00]>

        """

        if not isinstance(tz, dt_tzinfo):
            tz = parser.TzinfoParser.parse(tz)

        dt = self._datetime.astimezone(tz)

        return self.__class__(
            dt.year,
            dt.month,
            dt.day,
            dt.hour,
            dt.minute,
            dt.second,
            dt.microsecond,
            dt.tzinfo,
        )

    @classmethod
    def _validate_bounds(cls, bounds: str) -> None:
        if bounds != "()" and bounds != "(]" and bounds != "[)" and bounds != "[]":
            raise AttributeError(
                'Invalid bounds. Please select between "()", "(]", "[)", or "[]".'
            )

    def span(
        self, frame: str, count: int = 1, bounds: str = "[)"
    ) -> Tuple["Arrow", "Arrow"]:
        """ Returns two new :class:`Arrow <arrow.arrow.Arrow>` objects, representing the timespan
        of the :class:`Arrow <arrow.arrow.Arrow>` object in a given timeframe.

        :param frame: the timeframe.  Can be any ``datetime`` property (day, hour, minute...).
        :param count: (optional) the number of frames to span.
        :param bounds: (optional) a ``str`` of either '()', '(]', '[)', or '[]' that specifies
            whether to include or exclude the start and end values in the span. '(' excludes
            the start, '[' includes the start, ')' excludes the end, and ']' includes the end.
            If the bounds are not specified, the default bound '[)' is used.

        Supported frame values: year, quarter, month, week, day, hour, minute, second.

        Usage::

            >>> arrow.utcnow()
            <Arrow [2013-05-09T03:32:36.186203+00:00]>

            >>> arrow.utcnow().span('hour')
            (<Arrow [2013-05-09T03:00:00+00:00]>, <Arrow [2013-05-09T03:59:59.999999+00:00]>)

            >>> arrow.utcnow().span('day')
            (<Arrow [2013-05-09T00:00:00+00:00]>, <Arrow [2013-05-09T23:59:59.999999+00:00]>)

            >>> arrow.utcnow().span('day', count=2)
            (<Arrow [2013-05-09T00:00:00+00:00]>, <Arrow [2013-05-10T23:59:59.999999+00:00]>)

            >>> arrow.utcnow().span('day', bounds='[]')
            (<Arrow [2013-05-09T00:00:00+00:00]>, <Arrow [2013-05-10T00:00:00+00:00]>)

        """

        self._validate_bounds(bounds)

        frame_absolute, frame_relative, relative_steps = self._get_frames(frame)

        if frame_absolute == "week":
            attr = "day"
        elif frame_absolute == "quarter":
            attr = "month"
        else:
            attr = frame_absolute

        index = self._ATTRS.index(attr)
        frames = self._ATTRS[: index + 1]

        values = [getattr(self, f) for f in frames]

        for _ in range(3 - len(values)):
            values.append(1)

        floor = self.__class__(*values, tzinfo=self.tzinfo)

        if frame_absolute == "week":
            floor = floor + relativedelta(days=-(self.isoweekday() - 1))
        elif frame_absolute == "quarter":
            floor = floor + relativedelta(months=-((self.month - 1) % 3))

        ceil = floor + relativedelta(**{frame_relative: count * relative_steps})

        if bounds[0] == "(":
            floor += relativedelta(microseconds=1)

        if bounds[1] == ")":
            ceil += relativedelta(microseconds=-1)

        return floor, ceil

    def floor(self, frame: str) -> "Arrow":
        """ Returns a new :class:`Arrow <arrow.arrow.Arrow>` object, representing the "floor"
        of the timespan of the :class:`Arrow <arrow.arrow.Arrow>` object in a given timeframe.
        Equivalent to the first element in the 2-tuple returned by
        :func:`span <arrow.arrow.Arrow.span>`.

        :param frame: the timeframe.  Can be any ``datetime`` property (day, hour, minute...).

        Usage::

            >>> arrow.utcnow().floor('hour')
            <Arrow [2013-05-09T03:00:00+00:00]>
        """

        return self.span(frame)[0]

    def ceil(self, frame: str) -> "Arrow":
        """ Returns a new :class:`Arrow <arrow.arrow.Arrow>` object, representing the "ceiling"
        of the timespan of the :class:`Arrow <arrow.arrow.Arrow>` object in a given timeframe.
        Equivalent to the second element in the 2-tuple returned by
        :func:`span <arrow.arrow.Arrow.span>`.

        :param frame: the timeframe.  Can be any ``datetime`` property (day, hour, minute...).

        Usage::

            >>> arrow.utcnow().ceil('hour')
            <Arrow [2013-05-09T03:59:59.999999+00:00]>
        """

        return self.span(frame)[1]

    # string output and formatting.

    def format(self, fmt: str = "YYYY-MM-DD HH:mm:ssZZ", locale: str = "en_us") -> str:
        """ Returns a string representation of the :class:`Arrow <arrow.arrow.Arrow>` object,
        formatted according to a format string.

        :param fmt: the format string.

        Usage::

            >>> arrow.utcnow().format('YYYY-MM-DD HH:mm:ss ZZ')
            '2013-05-09 03:56:47 -00:00'

            >>> arrow.utcnow().format('X')
            '1368071882'

            >>> arrow.utcnow().format('MMMM DD, YYYY')
            'May 09, 2013'

            >>> arrow.utcnow().format()
            '2013-05-09 03:56:47 -00:00'

        """

        return formatter.DateTimeFormatter(locale).format(self._datetime, fmt)

    def humanize(
        self,
        other: Optional[Union["Arrow", date]] = None,
        locale_code: str = "en_us",
        only_distance: bool = False,
        granularity: Union[List[str], str] = "auto",
    ) -> str:
        """ Returns a localized, humanized representation of a relative difference in time.

        :param other: (optional) an :class:`Arrow <arrow.arrow.Arrow>` or ``datetime`` object.
            Defaults to now in the current :class:`Arrow <arrow.arrow.Arrow>` object's timezone.
        :param locale_code: (optional) a ``str`` specifying a locale.  Defaults to 'en_us'.
        :param only_distance: (optional) returns only time difference eg: "11 seconds" without "in" or "ago" part.
        :param granularity: (optional) defines the precision of the output. Set it to strings 'second', 'minute',
                           'hour', 'day', 'week', 'month' or 'year' or a list of any combination of these strings

        Usage::

            >>> earlier = arrow.utcnow().shift(hours=-2)
            >>> earlier.humanize()
            '2 hours ago'

            >>> later = earlier.shift(hours=4)
            >>> later.humanize(earlier)
            'in 4 hours'

        """

        locale_name: str = locale_code
        locale: Locale = locales.get_locale(locale_name)

        if other is None:
            utc = datetime.utcnow().replace(tzinfo=dateutil_tz.tzutc())
            dt = utc.astimezone(self._datetime.tzinfo)

        elif isinstance(other, Arrow):
            dt = other._datetime

        elif isinstance(other, datetime):
            if other.tzinfo is None:
                dt = other.replace(tzinfo=self._datetime.tzinfo)
            else:
                dt = other.astimezone(self._datetime.tzinfo)

        else:
            raise TypeError(
                f"Invalid 'other' argument of type '{type(other).__name__}'. "
                "Argument must be of type None, Arrow, or datetime."
            )

        if isinstance(granularity, list) and len(granularity) == 1:
            granularity = granularity[0]

        delta: float = int(round(util.total_seconds(self._datetime - dt)))
        sign = -1 if delta < 0 else 1
        diff = abs(delta)
        delta = diff
        days: float
        weeks: float
        years: float
        try:
            if granularity == "auto":
                if diff < 10:
                    return locale.describe("now", only_distance=only_distance)

                if diff < 45:
                    seconds = sign * delta
                    return locale.describe(
                        "seconds", seconds, only_distance=only_distance
                    )

                elif diff < 90:
                    return locale.describe("minute", sign, only_distance=only_distance)
                elif diff < 2700:
                    minutes = sign * int(max(delta / 60, 2))
                    return locale.describe(
                        "minutes", minutes, only_distance=only_distance
                    )

                elif diff < 5400:
                    return locale.describe("hour", sign, only_distance=only_distance)
                elif diff < 79200:
                    hours = sign * int(max(delta / 3600, 2))
                    return locale.describe("hours", hours, only_distance=only_distance)

                # anything less than 48 hours should be 1 day
                elif diff < 172800:
                    return locale.describe("day", sign, only_distance=only_distance)
                elif diff < 554400:
                    days = sign * int(max(delta / 86400, 2))
                    return locale.describe("days", days, only_distance=only_distance)

                elif diff < 907200:
                    return locale.describe("week", sign, only_distance=only_distance)
                elif diff < 2419200:
                    weeks = sign * int(max(delta / 604800, 2))
                    return locale.describe("weeks", weeks, only_distance=only_distance)

                elif diff < 3888000:
                    return locale.describe("month", sign, only_distance=only_distance)
                elif diff < 29808000:
                    self_months = self._datetime.year * 12 + self._datetime.month
                    other_months = dt.year * 12 + dt.month

                    months = sign * int(max(abs(other_months - self_months), 2))

                    return locale.describe(
                        "months", months, only_distance=only_distance
                    )

                elif diff < 47260800:
                    return locale.describe("year", sign, only_distance=only_distance)
                else:
                    years = sign * int(max(delta / 31536000, 2))
                    return locale.describe("years", years, only_distance=only_distance)

            elif util.isstr(granularity):
                if granularity == "second":
                    delta = sign * delta
                    if abs(delta) < 2:
                        return locale.describe("now", only_distance=only_distance)
                elif granularity == "minute":
                    delta = sign * delta / self._SECS_PER_MINUTE
                elif granularity == "hour":
                    delta = sign * delta / self._SECS_PER_HOUR
                elif granularity == "day":
                    delta = sign * delta / self._SECS_PER_DAY
                elif granularity == "week":
                    delta = sign * delta / self._SECS_PER_WEEK
                elif granularity == "month":
                    delta = sign * delta / self._SECS_PER_MONTH
                elif granularity == "year":
                    delta = sign * delta / self._SECS_PER_YEAR
                else:
                    raise AttributeError(
                        "Invalid level of granularity. Please select between 'second', 'minute', 'hour', 'day', 'week', 'month' or 'year'"
                    )

                if trunc(abs(delta)) != 1:
                    granularity += "s"
                return locale.describe(granularity, delta, only_distance=only_distance)

            else:
                timeframes = []
                if "year" in granularity:
                    years = sign * delta / self._SECS_PER_YEAR
                    delta %= self._SECS_PER_YEAR
                    timeframes.append(["year", years])

                if "month" in granularity:
                    months = sign * delta / self._SECS_PER_MONTH
                    delta %= self._SECS_PER_MONTH
                    timeframes.append(["month", months])

                if "week" in granularity:
                    weeks = sign * delta / self._SECS_PER_WEEK
                    delta %= self._SECS_PER_WEEK
                    timeframes.append(["week", weeks])

                if "day" in granularity:
                    days = sign * delta / self._SECS_PER_DAY
                    delta %= self._SECS_PER_DAY
                    timeframes.append(["day", days])

                if "hour" in granularity:
                    hours = sign * delta / self._SECS_PER_HOUR
                    delta %= self._SECS_PER_HOUR
                    timeframes.append(["hour", hours])

                if "minute" in granularity:
                    minutes = sign * delta / self._SECS_PER_MINUTE
                    delta %= self._SECS_PER_MINUTE
                    timeframes.append(["minute", minutes])

                if "second" in granularity:
                    seconds = sign * delta
                    timeframes.append(["second", seconds])

                if len(timeframes) < len(granularity):
                    raise AttributeError(
                        "Invalid level of granularity. "
                        "Please select between 'second', 'minute', 'hour', 'day', 'week', 'month' or 'year'."
                    )

                for tf in timeframes:
                    # Make granularity plural if the delta is not equal to 1
                    if trunc(abs(tf[1])) != 1:
                        tf[0] += "s"
                return locale.describe_multi(timeframes, only_distance=only_distance)

        except KeyError as e:
            raise ValueError(
                f"Humanization of the {e} granularity is not currently translated in the '{locale_name}' locale. "
                "Please consider making a contribution to this locale."
            )

    # query functions

    def is_between(
        self, start: Union["Arrow"], end: Union["Arrow"], bounds: str = "[]",
    ) -> bool:
        """ Returns a boolean denoting whether the specified date and time is between
        the start and end dates and times.

        :param start: an :class:`Arrow <arrow.arrow.Arrow>` object.
        :param end: an :class:`Arrow <arrow.arrow.Arrow>` object.
        :param bounds: (optional) a ``str`` of either '()', '(]', '[)', or '[]' that specifies
            whether to include or exclude the start and end values in the range. '(' excludes
            the start, '[' includes the start, ')' excludes the end, and ']' includes the end.
            If the bounds are not specified, the default bound '()' is used.

        Usage::

            >>> start = arrow.get(datetime(2013, 5, 5, 12, 30, 10))
            >>> end = arrow.get(datetime(2013, 5, 5, 12, 30, 36))
            >>> arrow.get(datetime(2013, 5, 5, 12, 30, 27)).is_between(start, end)
            True

            >>> start = arrow.get(datetime(2013, 5, 5))
            >>> end = arrow.get(datetime(2013, 5, 8))
            >>> arrow.get(datetime(2013, 5, 8)).is_between(start, end, '[]')
            True

            >>> start = arrow.get(datetime(2013, 5, 5))
            >>> end = arrow.get(datetime(2013, 5, 8))
            >>> arrow.get(datetime(2013, 5, 8)).is_between(start, end, '[)')
            False

        """

        self._validate_bounds(bounds)

        if not isinstance(start, Arrow):
            raise TypeError(f"Can't parse start date argument type of '{type(start)}'")

        if not isinstance(end, Arrow):
            raise TypeError(f"Can't parse end date argument type of '{type(end)}'")

        include_start = bounds[0] == "["
        include_end = bounds[1] == "]"

        target_timestamp = self.float_timestamp
        start_timestamp = start.float_timestamp
        end_timestamp = end.float_timestamp

        if include_start and include_end:
            return (
                target_timestamp >= start_timestamp
                and target_timestamp <= end_timestamp
            )
        elif include_start and not include_end:
            return (
                target_timestamp >= start_timestamp and target_timestamp < end_timestamp
            )
        elif not include_start and include_end:
            return (
                target_timestamp > start_timestamp and target_timestamp <= end_timestamp
            )
        else:
            return (
                target_timestamp > start_timestamp and target_timestamp < end_timestamp
            )

    # math

    def __add__(self, other: Union[timedelta, relativedelta, int]) -> Union["Arrow"]:

        if isinstance(other, (timedelta, relativedelta)):
            return self.fromdatetime(self._datetime + other, self._datetime.tzinfo)

        return NotImplemented

    def __radd__(self, other: timedelta) -> "Arrow":
        return self.__add__(other)

    def __sub__(self, other: Any) -> Union["Arrow", timedelta]:

        if isinstance(other, (timedelta, relativedelta)):
            return self.fromdatetime(self._datetime - other, self._datetime.tzinfo)

        elif isinstance(other, datetime):
            return self._datetime - other

        elif isinstance(other, Arrow):
            return self._datetime - other._datetime

        return NotImplemented

    def __rsub__(self, other: Any) -> Any:  # TODO Check typing  # TODO Check typing

        if isinstance(other, datetime):
            return other - self._datetime

        return NotImplemented

    # comparisons

    def __eq__(self, other: Any) -> bool:  # TODO Check typing

        if not isinstance(other, (Arrow, datetime)):
            return False

        return self._datetime == self._get_datetime(other)

    def __ne__(self, other: Any) -> bool:  # TODO Check typing

        if not isinstance(other, (Arrow, datetime)):
            return True

        return not self.__eq__(other)

    def __gt__(self, other: Any) -> Any:  # TODO Check typing  # TODO Check typing

        if not isinstance(other, (Arrow, datetime)):
            return NotImplemented

        return self._datetime > self._get_datetime(other)

    def __ge__(self, other: Any) -> Any:  # TODO Check typing  # TODO Check typing

        if not isinstance(other, (Arrow, datetime)):
            return NotImplemented

        return self._datetime >= self._get_datetime(other)

    def __lt__(self, other: Any) -> Any:  # TODO Check typing  # TODO Check typing

        if not isinstance(other, (Arrow, datetime)):
            return NotImplemented

        return self._datetime < self._get_datetime(other)

    def __le__(self, other: Any) -> Any:  # TODO Check typing  # TODO Check typing

        if not isinstance(other, (Arrow, datetime)):
            return NotImplemented

        return self._datetime <= self._get_datetime(other)

    def __cmp__(self, other):
        if sys.version_info[0] < 3:  # pragma: no cover
            if not isinstance(other, (Arrow, datetime)):
                raise TypeError(f"can't compare '{type(self)}' to '{type(other)}'")

    # datetime methods

    def date(self) -> date:
        """ Returns a ``date`` object with the same year, month and day.

        Usage::

            >>> arrow.utcnow().date()
            datetime.date(2019, 1, 23)

        """

        return self._datetime.date()

    def time(self) -> time:
        """ Returns a ``time`` object with the same hour, minute, second, microsecond.

        Usage::

            >>> arrow.utcnow().time()
            datetime.time(12, 15, 34, 68352)

        """

        return self._datetime.time()

    def timetz(self) -> time:
        """ Returns a ``time`` object with the same hour, minute, second, microsecond and
        tzinfo.

        Usage::

            >>> arrow.utcnow().timetz()
            datetime.time(12, 5, 18, 298893, tzinfo=tzutc())

        """

        return self._datetime.timetz()

    def astimezone(self, tz: tzfile) -> datetime:
        """ Returns a ``datetime`` object, converted to the specified timezone.

        :param tz: a ``tzinfo`` object.

        Usage::

            >>> pacific=arrow.now('US/Pacific')
            >>> nyc=arrow.now('America/New_York').tzinfo
            >>> pacific.astimezone(nyc)
            datetime.datetime(2019, 1, 20, 10, 24, 22, 328172, tzinfo=tzfile('/usr/share/zoneinfo/America/New_York'))

        """

        return self._datetime.astimezone(tz)

    def utcoffset(self) -> timedelta:
        """ Returns a ``timedelta`` object representing the whole number of minutes difference from
        UTC time.

        Usage::

            >>> arrow.now('US/Pacific').utcoffset()
            datetime.timedelta(-1, 57600)

        """

        return self._datetime.utcoffset()

    def dst(self) -> timedelta:
        """ Returns the daylight savings time adjustment.

        Usage::

            >>> arrow.utcnow().dst()
            datetime.timedelta(0)

        """

        return self._datetime.dst()

    def timetuple(self) -> struct_time:
        """ Returns a ``time.struct_time``, in the current timezone.

        Usage::

            >>> arrow.utcnow().timetuple()
            time.struct_time(tm_year=2019, tm_mon=1, tm_mday=20, tm_hour=15, tm_min=17, tm_sec=8, tm_wday=6, tm_yday=20, tm_isdst=0)

        """

        return self._datetime.timetuple()

    def utctimetuple(self) -> struct_time:
        """ Returns a ``time.struct_time``, in UTC time.

        Usage::

            >>> arrow.utcnow().utctimetuple()
            time.struct_time(tm_year=2019, tm_mon=1, tm_mday=19, tm_hour=21, tm_min=41, tm_sec=7, tm_wday=5, tm_yday=19, tm_isdst=0)

        """

        return self._datetime.utctimetuple()

    def toordinal(self) -> int:
        """ Returns the proleptic Gregorian ordinal of the date.

        Usage::

            >>> arrow.utcnow().toordinal()
            737078

        """

        return self._datetime.toordinal()

    def weekday(self) -> int:
        """ Returns the day of the week as an integer (0-6).

        Usage::

            >>> arrow.utcnow().weekday()
            5

        """

        return self._datetime.weekday()

    def isoweekday(self) -> int:
        """ Returns the ISO day of the week as an integer (1-7).

        Usage::

            >>> arrow.utcnow().isoweekday()
            6

        """

        return self._datetime.isoweekday()

    def isocalendar(self) -> Tuple[int, int, int]:
        """ Returns a 3-tuple, (ISO year, ISO week number, ISO weekday).

        Usage::

            >>> arrow.utcnow().isocalendar()
            (2019, 3, 6)

        """

        return self._datetime.isocalendar()

    def isoformat(self, sep: str = "T") -> str:
        """Returns an ISO 8601 formatted representation of the date and time.

        Usage::

            >>> arrow.utcnow().isoformat()
            '2019-01-19T18:30:52.442118+00:00'

        """

        return self._datetime.isoformat(sep)

    def ctime(self) -> str:
        """ Returns a ctime formatted representation of the date and time.

        Usage::

            >>> arrow.utcnow().ctime()
            'Sat Jan 19 18:26:50 2019'

        """

        return self._datetime.ctime()

    def strftime(self, format: str) -> str:
        """ Formats in the style of ``datetime.strftime``.

        :param format: the format string.

        Usage::

            >>> arrow.utcnow().strftime('%d-%m-%Y %H:%M:%S')
            '23-01-2019 12:28:17'

        """

        return self._datetime.strftime(format)

    def for_json(self) -> str:
        """Serializes for the ``for_json`` protocol of simplejson.

        Usage::

            >>> arrow.utcnow().for_json()
            '2019-01-19T18:25:36.760079+00:00'

        """

        return self.isoformat()

    # internal tools.

    @staticmethod
    def _get_tzinfo(tz_expr: Any) -> Union[tzfile, tzutc]:

        if tz_expr is None:
            return dateutil_tz.tzutc()
        if isinstance(tz_expr, dt_tzinfo):
            return tz_expr
        else:
            try:
                return parser.TzinfoParser.parse(tz_expr)
            except parser.ParserError:
                raise ValueError(f"'{tz_expr}' not recognized as a timezone")

    @classmethod
    def _get_datetime(cls, expr: Any) -> "datetime":
        """Get datetime object for a specified expression."""
        if isinstance(expr, Arrow):
            return expr.datetime
        elif isinstance(expr, datetime):
            return expr
        elif util.is_timestamp(expr):
            timestamp = float(expr)
            return cls.utcfromtimestamp(timestamp).datetime
        else:
            raise ValueError(f"'{expr}' not recognized as a datetime or timestamp.")

    @classmethod
    def _get_frames(cls, name: str) -> Tuple[str, str, int]:

        if name in cls._ATTRS:
            return name, f"{name}s", 1
        elif name[-1] == "s" and name[:-1] in cls._ATTRS:
            return name[:-1], name, 1
        elif name in ["week", "weeks"]:
            return "week", "weeks", 1
        elif name in ["quarter", "quarters"]:
            return "quarter", "months", 3

        supported = ", ".join(
            [
                "year(s)",
                "month(s)",
                "day(s)",
                "hour(s)",
                "minute(s)",
                "second(s)",
                "microsecond(s)",
                "week(s)",
                "quarter(s)",
            ]
        )
        raise AttributeError(
            f"range/span over frame {name} not supported. Supported frames: {supported}"
        )

    @classmethod
    def _get_iteration_params(cls, end: Any, limit: Optional[int]) -> Tuple[Any, int]:

        if end is None:

            if limit is None:
                raise ValueError("one of 'end' or 'limit' is required")

            return cls.max, limit

        else:
            if limit is None:
                return end, sys.maxsize
            return end, limit


Arrow.min = Arrow.fromdatetime(datetime.min)
Arrow.max = Arrow.fromdatetime(datetime.max)
