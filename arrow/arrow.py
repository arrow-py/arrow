# -*- coding: utf-8 -*-
'''
Provides the :class:`Arrow <arrow.arrow.Arrow>` class, an enhanced ``datetime``
replacement.

'''

from __future__ import absolute_import

from datetime import datetime, timedelta, tzinfo
from dateutil import tz as dateutil_tz
from dateutil.relativedelta import relativedelta
import calendar
import sys

from arrow import util, locales, parser, formatter


class Arrow(object):
    '''An :class:`Arrow <arrow.arrow.Arrow>` object.

    Implements the ``datetime`` interface, behaving as an aware ``datetime`` while implementing
    additional functionality.

    :param year: the calendar year.
    :param month: the calendar month.
    :param day: the calendar day.
    :param hour: (optional) the hour. Defaults to 0.
    :param minute: (optional) the minute, Defaults to 0.
    :param second: (optional) the second, Defaults to 0.
    :param microsecond: (optional) the microsecond. Defaults 0.
    :param tzinfo: (optional) the ``tzinfo`` object.  Defaults to ``None``.

    If tzinfo is None, it is assumed to be UTC on creation.

    Usage::

        >>> import arrow
        >>> arrow.Arrow(2013, 5, 5, 12, 30, 45)
        <Arrow [2013-05-05T12:30:45+00:00]>

    '''

    resolution = datetime.resolution

    _ATTRS = ['year', 'month', 'day', 'hour', 'minute', 'second', 'microsecond']
    _ATTRS_PLURAL = ['{0}s'.format(a) for a in _ATTRS]

    def __init__(self, year, month, day, hour=0, minute=0, second=0, microsecond=0,
                 tzinfo=None):

        if util.isstr(tzinfo):
            tzinfo = parser.TzinfoParser.parse(tzinfo)
        tzinfo = tzinfo or dateutil_tz.tzutc()

        self._datetime = datetime(year, month, day, hour, minute, second,
            microsecond, tzinfo)


    # factories: single object, both original and from datetime.

    @classmethod
    def now(cls, tzinfo=None):
        '''Constructs an :class:`Arrow <arrow.arrow.Arrow>` object, representing "now".

        :param tzinfo: (optional) a ``tzinfo`` object. Defaults to local time.

        '''

        utc = datetime.utcnow().replace(tzinfo=dateutil_tz.tzutc())
        dt = utc.astimezone(dateutil_tz.tzlocal() if tzinfo is None else tzinfo)

        return cls(dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second,
            dt.microsecond, dt.tzinfo)

    @classmethod
    def utcnow(cls):
        ''' Constructs an :class:`Arrow <arrow.arrow.Arrow>` object, representing "now" in UTC
        time.

        '''

        dt = datetime.utcnow()

        return cls(dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second,
            dt.microsecond, dateutil_tz.tzutc())

    @classmethod
    def fromtimestamp(cls, timestamp, tzinfo=None):
        ''' Constructs an :class:`Arrow <arrow.arrow.Arrow>` object from a timestamp.

        :param timestamp: an ``int`` or ``float`` timestamp, or a ``str`` that converts to either.
        :param tzinfo: (optional) a ``tzinfo`` object.  Defaults to local time.

        '''

        tzinfo = tzinfo or dateutil_tz.tzlocal()
        timestamp = cls._get_timestamp_from_input(timestamp)
        dt = datetime.fromtimestamp(timestamp, tzinfo)

        return cls(dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second,
            dt.microsecond, tzinfo)

    @classmethod
    def utcfromtimestamp(cls, timestamp):
        '''Constructs an :class:`Arrow <arrow.arrow.Arrow>` object from a timestamp, in UTC time.

        :param timestamp: an ``int`` or ``float`` timestamp, or a ``str`` that converts to either.

        '''

        timestamp = cls._get_timestamp_from_input(timestamp)
        dt = datetime.utcfromtimestamp(timestamp)

        return cls(dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second,
            dt.microsecond, dateutil_tz.tzutc())

    @classmethod
    def fromdatetime(cls, dt, tzinfo=None):
        ''' Constructs an :class:`Arrow <arrow.arrow.Arrow>` object from a ``datetime`` and optional
        ``tzinfo`` object.

        :param dt: the ``datetime``
        :param tzinfo: (optional) a ``tzinfo`` object.  Defaults to UTC.

        '''

        tzinfo = tzinfo or dt.tzinfo or dateutil_tz.tzutc()

        return cls(dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second,
            dt.microsecond, tzinfo)

    @classmethod
    def fromdate(cls, date, tzinfo=None):
        ''' Constructs an :class:`Arrow <arrow.arrow.Arrow>` object from a ``date`` and optional
        ``tzinfo`` object.  Time values are set to 0.

        :param date: the ``date``
        :param tzinfo: (optional) a ``tzinfo`` object.  Defaults to UTC.
        '''

        tzinfo = tzinfo or dateutil_tz.tzutc()

        return cls(date.year, date.month, date.day, tzinfo=tzinfo)

    @classmethod
    def strptime(cls, date_str, fmt, tzinfo=None):
        ''' Constructs an :class:`Arrow <arrow.arrow.Arrow>` object from a date string and format,
        in the style of ``datetime.strptime``.

        :param date_str: the date string.
        :param fmt: the format string.
        :param tzinfo: (optional) an optional ``tzinfo``
        '''

        dt = datetime.strptime(date_str, fmt)
        tzinfo = tzinfo or dt.tzinfo

        return cls(dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second,
            dt.microsecond, tzinfo)


    # factories: ranges and spans

    @classmethod
    def range(cls, frame, start, end=None, tz=None, limit=None):
        ''' Returns an array of :class:`Arrow <arrow.arrow.Arrow>` objects, representing
        an iteration of time between two inputs.

        :param frame: the timeframe.  Can be any ``datetime`` property (day, hour, minute...).
        :param start: A datetime expression, the start of the range.
        :param end: (optional) A datetime expression, the end of the range.
        :param tz: (optional) A timezone expression.  Defaults to UTC.
        :param limit: (optional) A maximum number of tuples to return.

        **NOTE**: the **end** or **limit** must be provided.  Call with **end** alone to
        return the entire range, with **limit** alone to return a maximum # of results from the
        start, and with both to cap a range at a maximum # of results.

        Recognized datetime expressions:

            - An :class:`Arrow <arrow.arrow.Arrow>` object.
            - A ``datetime`` object.

        Recognized timezone expressions:

            - A ``tzinfo`` object.
            - A ``str`` describing a timezone, similar to 'US/Pacific', or 'Europe/Berlin'.
            - A ``str`` in ISO-8601 style, as in '+07:00'.
            - A ``str``, one of the following:  'local', 'utc', 'UTC'.

        Usage:

            >>> start = datetime(2013, 5, 5, 12, 30)
            >>> end = datetime(2013, 5, 5, 17, 15)
            >>> for r in arrow.Arrow.range('hour', start, end):
            ...     print repr(r)
            ...
            <Arrow [2013-05-05T12:30:00+00:00]>
            <Arrow [2013-05-05T13:30:00+00:00]>
            <Arrow [2013-05-05T14:30:00+00:00]>
            <Arrow [2013-05-05T15:30:00+00:00]>
            <Arrow [2013-05-05T16:30:00+00:00]>

        '''

        frame_relative = cls._get_frames(frame)[1]
        tzinfo = cls._get_tzinfo(start.tzinfo if tz is None else tz)

        start = cls._get_datetime(start).replace(tzinfo=tzinfo)
        end, limit = cls._get_iteration_params(end, limit)
        end = cls._get_datetime(end).replace(tzinfo=tzinfo)

        current = cls.fromdatetime(start)
        results = []

        while current <= end and len(results) < limit:
            results.append(current)

            values = [getattr(current, f) for f in cls._ATTRS]
            current = cls(*values, tzinfo=tzinfo) + relativedelta(**{frame_relative: 1})

        return results


    @classmethod
    def span_range(cls, frame, start, end, tz=None, limit=None):
        ''' Returns an array of tuples, each :class:`Arrow <arrow.arrow.Arrow>` objects,
        representing a series of timespans between two inputs.

        :param frame: the timeframe.  Can be any ``datetime`` property (day, hour, minute...).
        :param start: A datetime expression, the start of the range.
        :param end: (optional) A datetime expression, the end of the range.
        :param tz: (optional) A timezone expression.  Defaults to UTC.
        :param limit: (optional) A maximum number of tuples to return.

        **NOTE**: the **end** or **limit** must be provided.  Call with **end** alone to
        return the entire range, with **limit** alone to return a maximum # of results from the
        start, and with both to cap a range at a maximum # of results.

        Recognized datetime expressions:

            - An :class:`Arrow <arrow.arrow.Arrow>` object.
            - A ``datetime`` object.

        Recognized timezone expressions:

            - A ``tzinfo`` object.
            - A ``str`` describing a timezone, similar to 'US/Pacific', or 'Europe/Berlin'.
            - A ``str`` in ISO-8601 style, as in '+07:00'.
            - A ``str``, one of the following:  'local', 'utc', 'UTC'.

        Usage:

            >>> start = datetime(2013, 5, 5, 12, 30)
            >>> end = datetime(2013, 5, 5, 17, 15)
            >>> for r in arrow.Arrow.span_range('hour', start, end):
            ...     print r
            ...
            (<Arrow [2013-05-05T12:00:00+00:00]>, <Arrow [2013-05-05T12:59:59.999999+00:00]>)
            (<Arrow [2013-05-05T13:00:00+00:00]>, <Arrow [2013-05-05T13:59:59.999999+00:00]>)
            (<Arrow [2013-05-05T14:00:00+00:00]>, <Arrow [2013-05-05T14:59:59.999999+00:00]>)
            (<Arrow [2013-05-05T15:00:00+00:00]>, <Arrow [2013-05-05T15:59:59.999999+00:00]>)
            (<Arrow [2013-05-05T16:00:00+00:00]>, <Arrow [2013-05-05T16:59:59.999999+00:00]>)

        '''

        _range = cls.range(frame, start, end, tz, limit)
        return [r.span(frame) for r in _range]


    # representations

    def __repr__(self):

        dt = self._datetime
        attrs = ', '.join([str(i) for i in [dt.year, dt.month, dt.day, dt.hour, dt.minute,
            dt.second, dt.microsecond]])

        return '<{0} [{1}]>'.format(self.__class__.__name__, self.__str__())

    def __str__(self):
        return self._datetime.isoformat()

    def __format__(self, formatstr):

        if len(formatstr) > 0:
            return self.format(formatstr)

        return str(self)

    def __hash__(self):
        return self._datetime.__hash__()


    # attributes & properties

    def __getattr__(self, name):

        if name == 'week':
            return self.isocalendar()[1]

        if not name.startswith('_'):
            value = getattr(self._datetime, name, None)

            if value is not None:
                return value

        return object.__getattribute__(self, name)

    @property
    def tzinfo(self):
        ''' Gets the ``tzinfo`` of the :class:`Arrow <arrow.arrow.Arrow>` object. '''

        return self._datetime.tzinfo

    @tzinfo.setter
    def tzinfo(self, tzinfo):
        ''' Sets the ``tzinfo`` of the :class:`Arrow <arrow.arrow.Arrow>` object. '''

        self._datetime = self._datetime.replace(tzinfo=tzinfo)

    @property
    def datetime(self):
        ''' Returns a datetime representation of the :class:`Arrow <arrow.arrow.Arrow>` object. '''

        return self._datetime

    @property
    def naive(self):
        ''' Returns a naive datetime representation of the :class:`Arrow <arrow.arrow.Arrow>` object. '''

        return self._datetime.replace(tzinfo=None)

    @property
    def timestamp(self):
        ''' Returns a timestamp representation of the :class:`Arrow <arrow.arrow.Arrow>` object. '''

        return calendar.timegm(self._datetime.utctimetuple())

    @property
    def float_timestamp(self):
        ''' Returns a floating-point representation of the :class:`Arrow <arrow.arrow.Arrow>` object. '''

        return self.timestamp + float(self.microsecond) / 1000000


    # mutation and duplication.

    def clone(self):
        ''' Returns a new :class:`Arrow <arrow.arrow.Arrow>` object, cloned from the current one.

        Usage:

            >>> arw = arrow.utcnow()
            >>> cloned = arw.clone()

        '''

        return self.fromdatetime(self._datetime)

    def replace(self, **kwargs):
        ''' Returns a new :class:`Arrow <arrow.arrow.Arrow>` object with attributes updated
        according to inputs.

        Use single property names to set their value absolutely:

        >>> import arrow
        >>> arw = arrow.utcnow()
        >>> arw
        <Arrow [2013-05-11T22:27:34.787885+00:00]>
        >>> arw.replace(year=2014, month=6)
        <Arrow [2014-06-11T22:27:34.787885+00:00]>

        Use plural property names to shift their current value relatively:

        >>> arw.replace(years=1, months=-1)
        <Arrow [2014-04-11T22:27:34.787885+00:00]>

        You can also provide a tzimezone expression can also be replaced:

        >>> arw.replace(tzinfo=tz.tzlocal())
        <Arrow [2013-05-11T22:27:34.787885-07:00]>

        Recognized timezone expressions:

            - A ``tzinfo`` object.
            - A ``str`` describing a timezone, similar to 'US/Pacific', or 'Europe/Berlin'.
            - A ``str`` in ISO-8601 style, as in '+07:00'.
            - A ``str``, one of the following:  'local', 'utc', 'UTC'.

        '''

        absolute_kwargs = {}
        relative_kwargs = {}

        for key, value in kwargs.items():

            if key in self._ATTRS:
                absolute_kwargs[key] = value
            elif key in self._ATTRS_PLURAL or key == 'weeks':
                relative_kwargs[key] = value
            elif key == 'week':
                raise AttributeError('setting absolute week is not supported')
            elif key !='tzinfo':
                raise AttributeError()

        current = self._datetime.replace(**absolute_kwargs)
        current += relativedelta(**relative_kwargs)

        tzinfo = kwargs.get('tzinfo')

        if tzinfo is not None:
            tzinfo = self._get_tzinfo(tzinfo)
            current = current.replace(tzinfo=tzinfo)

        return self.fromdatetime(current)

    def to(self, tz):
        ''' Returns a new :class:`Arrow <arrow.arrow.Arrow>` object, converted to the target
        timezone.

        :param tz: an expression representing a timezone.

        Recognized timezone expressions:

            - A ``tzinfo`` object.
            - A ``str`` describing a timezone, similar to 'US/Pacific', or 'Europe/Berlin'.
            - A ``str`` in ISO-8601 style, as in '+07:00'.
            - A ``str``, one of the following:  'local', 'utc', 'UTC'.

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

        '''

        if not isinstance(tz, tzinfo):
            tz = parser.TzinfoParser.parse(tz)

        dt = self._datetime.astimezone(tz)

        return self.__class__(dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second,
            dt.microsecond, tz)

    def span(self, frame):
        ''' Returns two new :class:`Arrow <arrow.arrow.Arrow>` objects, representing the timespan
        of the :class:`Arrow <arrow.arrow.Arrow>` object in a given timeframe.

        :param frame: the timeframe.  Can be any ``datetime`` property (day, hour, minute...).

        Usage::

            >>> arrow.utcnow()
            <Arrow [2013-05-09T03:32:36.186203+00:00]>

            >>> arrow.utcnow().span('hour')
            (<Arrow [2013-05-09T03:00:00+00:00]>, <Arrow [2013-05-09T03:59:59.999999+00:00]>)

            >>> arrow.utcnow().span('day')
            (<Arrow [2013-05-09T00:00:00+00:00]>, <Arrow [2013-05-09T23:59:59.999999+00:00]>)

        '''

        frame_absolute, frame_relative = self._get_frames(frame)

        index = self._ATTRS.index('day' if frame_absolute == 'week' else frame_absolute)
        frames = self._ATTRS[:index + 1]

        values = [getattr(self, f) for f in frames]

        for i in range(3 - len(values)):
            values.append(1)

        floor = self.__class__(*values, tzinfo=self.tzinfo)

        if frame_absolute == 'week':
            floor = floor + relativedelta(days=-(self.isoweekday() - 1))

        ceil = floor + relativedelta(**{frame_relative: 1}) + relativedelta(microseconds=-1)

        return floor, ceil

    def floor(self, frame):
        ''' Returns a new :class:`Arrow <arrow.arrow.Arrow>` object, representing the "floor"
        of the timespan of the :class:`Arrow <arrow.arrow.Arrow>` object in a given timeframe.
        Equivalent to the first element in the 2-tuple returned by
        :func:`span <arrow.arrow.Arrow.span>`.

        :param frame: the timeframe.  Can be any ``datetime`` property (day, hour, minute...).

        Usage::

            >>> arrow.utcnow().ceil('hour')
            <Arrow [2013-05-09T03:00:00+00:00]>
        '''

        return self.span(frame)[0]

    def ceil(self, frame):
        ''' Returns a new :class:`Arrow <arrow.arrow.Arrow>` object, representing the "ceiling"
        of the timespan of the :class:`Arrow <arrow.arrow.Arrow>` object in a given timeframe.
        Equivalent to the second element in the 2-tuple returned by
        :func:`span <arrow.arrow.Arrow.span>`.

        :param frame: the timeframe.  Can be any ``datetime`` property (day, hour, minute...).

        Usage::

            >>> arrow.utcnow().ceil('hour')
            <Arrow [2013-05-09T03:59:59.999999+00:00]>
        '''

        return self.span(frame)[1]


    # string output and formatting.

    def format(self, fmt, locale='en_us'):
        ''' Returns a string representation of the :class:`Arrow <arrow.arrow.Arrow>` object,
        formatted according to a format string.

        :param fmt: the format string.

        Usage::

            >>> arrow.utcnow().format('YYYY-MM-DD HH:mm:ss ZZ')
            '2013-05-09 03:56:47 -00:00'

            >>> arrow.utcnow().format('X')
            '1368071882'

            >>> arrow.utcnow().format('MMMM DD, YYYY')
            'May 09, 2013'
        '''

        return formatter.DateTimeFormatter(locale).format(self._datetime, fmt)


    def humanize(self, other=None, locale='en_us'):
        ''' Returns a localized, humanized representation of a relative difference in time.

        :param other: (optional) an :class:`Arrow <arrow.arrow.Arrow>` or ``datetime`` object.
            Defaults to now in the current :class:`Arrow <arrow.arrow.Arrow>` object's timezone.
        :param locale: (optional) a ``str`` specifying a locale.  Defaults to 'en_us'.

        Usage::

            >>> earlier = arrow.utcnow().replace(hours=-2)
            >>> earlier.humanize()
            '2 hours ago'

            >>> later = later = earlier.replace(hours=4)
            >>> later.humanize(earlier)
            'in 4 hours'

        '''

        locale = locales.get_locale(locale)

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
            raise TypeError()

        delta = int(util.total_seconds(self._datetime - dt))
        sign = -1 if delta < 0 else 1
        diff = abs(delta)
        delta = diff

        if diff < 10:
            return locale.describe('now')

        if diff < 45:
            return locale.describe('seconds', sign)

        elif diff < 90:
            return locale.describe('minute', sign)
        elif diff < 2700:
            minutes = sign * int(max(delta / 60, 2))
            return locale.describe('minutes', minutes)

        elif diff < 5400:
            return locale.describe('hour', sign)
        elif diff < 79200:
            hours = sign * int(max(delta / 3600, 2))
            return locale.describe('hours', hours)

        elif diff < 129600:
            return locale.describe('day', sign)
        elif diff < 2160000:
            days = sign * int(max(delta / 86400, 2))
            return locale.describe('days', days)

        elif diff < 3888000:
            return locale.describe('month', sign)
        elif diff < 29808000:
            self_months = self._datetime.year * 12 + self._datetime.month
            other_months = dt.year * 12 + dt.month
            months = sign * abs(other_months - self_months)

            return locale.describe('months', months)

        elif diff < 47260800:
            return locale.describe('year', sign)
        else:
            years = sign * int(max(delta / 31536000, 2))
            return locale.describe('years', years)


    # math

    def __add__(self, other):

        if isinstance(other, (timedelta, relativedelta)):
            return self.fromdatetime(self._datetime + other, self._datetime.tzinfo)

        raise NotImplementedError()

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):

        if isinstance(other, timedelta):
            return self.fromdatetime(self._datetime - other, self._datetime.tzinfo)

        elif isinstance(other, datetime):
            return self._datetime - other

        elif isinstance(other, Arrow):
            return self._datetime - other._datetime

        raise NotImplementedError()

    def __rsub__(self, other):
        return self.__sub__(other)


    # comparisons

    def __eq__(self, other):

        if not isinstance(other, (Arrow, datetime)):
            return False

        other = self._get_datetime(other)

        return self._datetime == self._get_datetime(other)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __gt__(self, other):

        if not isinstance(other, (Arrow, datetime)):
            return False

        return self._datetime > self._get_datetime(other)

    def __ge__(self, other):

        if not isinstance(other, (Arrow, datetime)):
            return False

        return self._datetime >= self._get_datetime(other)

    def __lt__(self, other):

        if not isinstance(other, (Arrow, datetime)):
            return False

        return self._datetime < self._get_datetime(other)

    def __le__(self, other):

        if not isinstance(other, (Arrow, datetime)):
            return False

        return self._datetime <= self._get_datetime(other)


    # datetime methods

    def date(self):
        ''' Returns a ``date`` object with the same year, month and day. '''

        return self._datetime.date()

    def time(self):
        ''' Returns a ``time`` object with the same hour, minute, second, microsecond. '''

        return self._datetime.time()

    def timetz(self):
        ''' Returns a ``time`` object with the same hour, minute, second, microsecond and tzinfo. '''

        return self._datetime.timetz()

    def astimezone(self, tz):
        ''' Returns a ``datetime`` object, adjusted to the specified tzinfo.

        :param tz: a ``tzinfo`` object.

        '''

        return self._datetime.astimezone(tz)

    def utcoffset(self):
        ''' Returns a ``timedelta`` object representing the whole number of minutes difference from UTC time. '''

        return self._datetime.utcoffset()

    def dst(self):
        ''' Returns the daylight savings time adjustment. '''
        return self._datetime.dst()

    def timetuple(self):
        ''' Returns a ``time.struct_time``, in the current timezone. '''

        return self._datetime.timetuple()

    def utctimetuple(self):
        ''' Returns a ``time.struct_time``, in UTC time. '''

        return self._datetime.utctimetuple()

    def toordinal(self):
        ''' Returns the proleptic Gregorian ordinal of the date. '''

        return self._datetime.toordinal()

    def weekday(self):
        ''' Returns the day of the week as an integer (0-6). '''

        return self._datetime.weekday()

    def isoweekday(self):
        ''' Returns the ISO day of the week as an integer (1-7). '''

        return self._datetime.isoweekday()

    def isocalendar(self):
        ''' Returns a 3-tuple, (ISO year, ISO week number, ISO weekday). '''

        return self._datetime.isocalendar()

    def isoformat(self, sep='T'):
        '''Returns an ISO 8601 formatted representation of the date and time. '''

        return self._datetime.isoformat(sep)

    def ctime(self):
        ''' Returns a ctime formatted representation of the date and time. '''

        return self._datetime.ctime()

    def strftime(self, format):
        ''' Formats in the style of ``datetime.strptime``.

        :param format: the format string.

        '''

        return self._datetime.strftime(format)


    # internal tools.

    @classmethod
    def _get_tzinfo(cls, tz_expr):

        if tz_expr is None:
            return dateutil_tz.tzutc()
        if isinstance(tz_expr, tzinfo):
            return tz_expr
        else:
            try:
                return parser.TzinfoParser.parse(tz_expr)
            except parser.ParserError:
                raise ValueError('\'{0}\' not recognized as a timezone')

    @classmethod
    def _get_datetime(cls, expr):

        if isinstance(expr, Arrow):
            return expr.datetime

        if isinstance(expr, datetime):
            return expr

        try:
            expr = float(expr)
            return cls.utcfromtimestamp(expr).datetime
        except:
            raise ValueError('\'{0}\' not recognized as a timestamp or datetime')

    @classmethod
    def _get_frames(cls, name):

        if name in cls._ATTRS:
            return name, '{0}s'.format(name)

        elif name in ['week', 'weeks']:
            return 'week', 'weeks'

        raise AttributeError()

    @classmethod
    def _get_iteration_params(cls, end, limit):

        if end is None:

            if limit is None:
                raise Exception('one of \'end\' or \'limit\' is required')

            return cls.max, limit

        else:
            return end, sys.maxsize

    @classmethod
    def _get_timestamp_from_input(cls, timestamp):

        try:
            return float(timestamp)
        except:
            raise ValueError('cannot parse \'{0}\' as a timestamp'.format(timestamp))

Arrow.min = Arrow.fromdatetime(datetime.min)
Arrow.max = Arrow.fromdatetime(datetime.max)
