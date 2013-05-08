from datetime import datetime, timedelta, tzinfo
from dateutil import tz as dateutil_tz
from dateutil.relativedelta import relativedelta
import calendar

import parser
import formatter
import locales


class Arrow(object):
    '''An :class:`Arrow <arrow.Arrow>` object.

    Implements the datetime iterface, behaving as an aware datetime while implementing
    additional functionality.

    :param year: calendar year
    :param month: calendar month
    :param day: calendar day
    :param hour: hour, default 0
    :param minute: minute, default 0
    :param second: second, default 0
    :param microsecond: microsecond, default 0
    :param tzinfo: tzinfo struct, default None

    If tzinfo is None, it is assumed to be UTC on creation.

    Usage::

        >>> import arrow
        >>> arw = arrow.Arrow(2013, 5, 5, 12, 30, 45)
        >>> arw
        <Arrow [2013-05-05T12:30:45+00:00]>
    '''

    min = datetime.min
    max = datetime.max
    resolution = datetime.resolution

    _ATTRS = ['year', 'month', 'day', 'hour', 'minute', 'second', 'microsecond']
    _ATTRS_PLURAL = ['{0}s'.format(a) for a in _ATTRS]

    def __init__(self, year, month, day, hour=0, minute=0, second=0, microsecond=0,

        tzinfo=None):

        tzinfo = tzinfo or dateutil_tz.tzutc()

        self._datetime = datetime(year, month, day, hour, minute, second,
            microsecond, tzinfo)


    # other constructors.

    @classmethod
    def now(cls, tzinfo=None):
        '''Constructs an :class:`Arrow <arrow.Arrow>` object, representing "now".

        :param tzinfo: (optional) a tzinfo struct. Defaults to local time.
        '''

        utc = datetime.utcnow().replace(tzinfo=dateutil_tz.tzutc())
        dt = utc.astimezone(dateutil_tz.tzlocal() if tzinfo is None else tzinfo)

        return Arrow(dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second,
            dt.microsecond, dt.tzinfo)

    @classmethod
    def utcnow(cls):
        '''Constructs an :class:`Arrow <arrow.Arrow>` object, representing "now" in UTC time.
        '''

        dt = datetime.utcnow()

        return Arrow(dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second,
            dt.microsecond, dateutil_tz.tzutc())

    @classmethod
    def fromtimestamp(cls, timestamp, tzinfo=None):
        '''Constructs an :class:`Arrow <arrow.Arrow>` object from a timestamp.

        :param timestamp: an integer or floating-point timestamp.
        :param tzinfo: (optional) a tzinfo struct.  Defaults to local time.
        '''

        tzinfo = tzinfo or dateutil_tz.tzlocal()
        dt = datetime.fromtimestamp(timestamp, tzinfo)

        return Arrow(dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second,
            dt.microsecond, tzinfo)

    @classmethod
    def utcfromtimestamp(cls, timestamp):
        '''Constructs an :class:`Arrow <arrow.Arrow>` object from a timestamp, in UTC time.

        :param timestamp: an integer or floating-point timestamp.
        '''

        dt = datetime.utcfromtimestamp(timestamp)

        return Arrow(dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second,
            dt.microsecond, dateutil_tz.tzutc())

    @classmethod
    def fromdatetime(cls, dt, tzinfo=None):

        tzinfo = tzinfo or dt.tzinfo or dateutil_tz.tzutc()

        return Arrow(dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second,
            dt.microsecond, tzinfo)

    @classmethod
    def strptime(cls, date_str, fmt, tzinfo=None):

        dt = datetime.strptime(date_str, fmt)
        tzinfo = tzinfo or dt.tzinfo

        return Arrow(dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second,
            dt.microsecond, tzinfo)


    # representations

    def __repr__(self):

        dt = self._datetime
        attrs = ', '.join([str(i) for i in [dt.year, dt.month, dt.day, dt.hour, dt.minute,
            dt.second, dt.microsecond]])

        return '<Arrow [{0}]>'.format(self.__str__())

    def __str__(self):
        return self._datetime.isoformat()

    def __format__(self, formatstr):
        return self.format(formatstr)

    def __hash__(self):
        return self._datetime.__hash__()


    # attributes & properties

    def __getattr__(self, name):

        n_single, n_plural = self._get_property_names(name)

        if n_single is not None:
            return getattr(self._datetime, n_single)

        return object.__getattribute__(self, name)

    def __setattr__(self, name, value):

        n_single, n_plural = self._get_property_names(name)

        if n_single is not None:
            delta = value - getattr(self._datetime, n_single)
            self._datetime += relativedelta(**{n_plural: delta})

        else:
            object.__setattr__(self, name, value)

    @classmethod
    def _get_property_names(cls, name):

        if name in cls._ATTRS:
            return name, '{0}s'.format(name)

        if name in cls._ATTRS_PLURAL:
            return name[:-1], name

        return None, None

    @property
    def tzinfo(self):
        return self._datetime.tzinfo

    @tzinfo.setter
    def tzinfo(self, _tzinfo):
        self._datetime = self._datetime.replace(tzinfo=_tzinfo)

    @property
    def datetime(self):
        ''' Returns a datetime representation of the :class:`Arrow <arrow.Arrow>` object.
        '''
        return self._datetime

    @property
    def naive(self):
        ''' Returns a naive datetime representation of the :class:`Arrow <arrow.Arrow>` object.
        '''

        return self._datetime.replace(tzinfo=None)

    @property
    def timestamp(self, cast=int):
        ''' Returns a timestamp representation of the :class:`Arrow <arrow.Arrow>` object.

        :param cast: (optional).  A function with which to cast the timestamp.  Defaults to int.
        '''

        return cast(calendar.timegm(self._datetime.utctimetuple()))


    # math

    def __add__(self, other):

        if isinstance(other, timedelta):
            return Arrow.fromdatetime(self._datetime + other, self._datetime.tzinfo)

        raise NotImplementedError()

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):

        if isinstance(other, timedelta):
            return Arrow.fromdatetime(self._datetime - other, self._datetime.tzinfo)

        elif isinstance(other, datetime):
            return self._datetime - other

        elif isinstance(other, Arrow):
            return self._datetime - other._datetime

        raise NotImplementedError()

    def __rsub__(self, other):
        return self.__sub__(other)


    # comparisons

    def _cmp_convert(self, other):
        return other._datetime if isinstance(other, Arrow) else other

    def __eq__(self, other):

        if not isinstance(other, (Arrow, datetime)):
            return False

        other = self._cmp_convert(other)

        return self._datetime == self._cmp_convert(other)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __gt__(self, other):

        if not isinstance(other, (Arrow, datetime)):
            return False

        return self._datetime > self._cmp_convert(other)

    def __ge__(self, other):

        if not isinstance(other, (Arrow, datetime)):
            return False

        return self._datetime >= self._cmp_convert(other)

    def __lt__(self, other):

        if not isinstance(other, (Arrow, datetime)):
            return False

        return self._datetime < self._cmp_convert(other)

    def __le__(self, other):

        if not isinstance(other, (Arrow, datetime)):
            return False

        return self._datetime <= self._cmp_convert(other)


    # datetime methods

    def date(self):
        '''Implementes **datetime**.date(), returning the **date** part.
        '''
        return self._datetime.date()

    def time(self):
        return self._datetime.time()

    def timetz(self):
        return self._datetime.timetz()

    def astimezone(self, tz):
        return self._datetime.astimezone(tz)

    def utcoffset(self):
        return self._datetime.utcoffset()

    def dst(self):
        return self._datetime.dst()

    def timetuple(self):
        return self._datetime.timetuple()

    def utctimetuple(self):
        return self._datetime.utctimetuple()

    def toordinal(self):
        return self._datetime.toordinal()

    def weekday(self):
        return self._datetime.weekday()

    def isoweekday(self):
        return self._datetime.isoweekday()

    def isocalendar(self):
        return self._datetime.isocalendar()

    def isoformat(self, sep='T'):
        return self._datetime.isoformat(sep)

    def ctime(self):
        return self._datetime.ctime()

    def strftime(self, format):
        return self._datetime.strftime(format)


    # NEW

    def clone(self):
        return Arrow.fromdatetime(self._datetime)

    def to(self, tz):

        if not isinstance(tz, tzinfo):
            tz = parser.TzinfoParser.parse(tz)

        dt = self._datetime.astimezone(tz)

        return Arrow(dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second,
            dt.microsecond, tz)

    def span(self, frame):

        f_single, f_plural = self._get_property_names(frame)

        if f_single is None:
            raise AttributeError()

        index = self._ATTRS.index(f_single)
        frames = self._ATTRS[:index + 1]
        values = [getattr(self._datetime, f) for f in frames]

        for i in range(3 - len(values)):
            values.append(1)

        floor = datetime(*values, tzinfo=self._datetime.tzinfo)

        ceil = floor + relativedelta(**{f_plural: 1})
        ceil = ceil + relativedelta(microseconds=-1)

        return Arrow.fromdatetime(floor), Arrow.fromdatetime(ceil)

    def floor(self, frame):
        return self.span(frame)[0]

    def ceil(self, frame):
        return self.span(frame)[1]

    def format(self, fmt):
        return formatter.DateTimeFormatter.format(self._datetime, fmt)

    def humanize(self, other=None, locale='english'):

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

        local_dict = getattr(locales, locale, None)
        if local_dict is None:
            raise ValueError('Invalid language {0}'.format(locale))

        delta = int((self._datetime - dt).total_seconds())
        past = delta < 0
        delta = abs(delta)

        if delta < 10:
            return local_dict['now']

        if delta < 45:
            expr = local_dict['seconds']

        elif delta < 90:
            expr = local_dict['minute']
        elif delta < 2700:
            minutes = max(delta / 60, 2)
            expr = local_dict['minutes'].format(minutes)

        elif delta < 5400:
            expr = local_dict['hour']
        elif delta < 79200:
            hours = max(delta / 3600, 2)
            expr = local_dict['hours'].format(hours)

        elif delta < 129600:
            expr = local_dict['day']
        elif delta < 2160000:
            days = max(delta / 86400, 2)
            expr = local_dict['days'].format(days)

        elif delta < 3888000:
            expr = local_dict['month']
        elif delta < 29808000:
            months = max(abs(dt.month - self._datetime.month), 2)
            expr = local_dict['months'].format(months)

        elif delta < 47260800:
            expr = local_dict['year']
        else:
            years = max(delta / 31536000, 2)
            expr = local_dict['years'].format(years)

        return local_dict['past'].format(expr) if past else local_dict['future'].format(expr)
