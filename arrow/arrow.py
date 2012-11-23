from .timezone import TimeZone

from datetime import datetime, timedelta, tzinfo
from dateutil import tz as _tz

import time, calendar

def arrow(date=None, tz=None):
    def _tz_now(tzinfo):

        date = datetime.utcnow()
        date = date.replace(tzinfo=_tz.tzutc())

        return date.astimezone(tzinfo)

    date_expr = None
    tz_expr = None

    if date is None:
        if tz is None:
            date_expr = datetime.utcnow()
            tz_expr = TimeZone(_tz.tzutc(), date_expr)

        else:
            tz_expr = TimeZone(tz, datetime.utcnow())
            date_expr = _tz_now(tz_expr.tzinfo)

    else:
        if tz is None:
            try:
                tz_expr = TimeZone(date, datetime.utcnow())
                date_expr = _tz_now(tz_expr.tzinfo)
            except:
                date_expr = date
                tz_expr = None

        else:
            date_expr = date
            tz_expr = tz

    return Arrow(date_expr, tz_expr)


class Arrow(object):

    def __init__(self, date, tz=None):

        if tz is None:
            tz = _tz.tzutc()

        self._datetime, self._timezone = self._parse(date, tz)

    def __eq__(self, other):

        eq = False

        if isinstance(other, Arrow) and self._datetime == other._datetime:
            self_tzoffset = self._timezone.tzinfo.utcoffset(self._datetime)
            other_tzoffset = other._timezone.tzinfo.utcoffset(other._datetime)

            eq = self_tzoffset == other_tzoffset

        return eq

    def __repr__(self):
        return '{0}({1})'.format(self.__class__.__name__, self.__str__())

    def __str__(self):

        time_str = time.strftime('%x %X', self._datetime.timetuple())

        return '{0}.{1} {2}'.format(time_str, self._datetime.microsecond,
            str(self._timezone))

    @staticmethod
    def _parse(dt_expr, tz_expr):

        _datetime = Arrow._try_parse_timestamp(dt_expr, tz_expr)

        if _datetime is None:

            if isinstance(dt_expr, datetime):
                _datetime = dt_expr

        if _datetime is None:
            raise ValueError('Could not recognize datetime')

        timezone = TimeZone(tz_expr, _datetime)
        _datetime = _datetime.replace(tzinfo=timezone.tzinfo)

        return _datetime, timezone

    @staticmethod
    def _try_parse_timestamp(dt_expr, timezone):

        _datetime = None

        try:
            dt_expr = float(dt_expr)

            _datetime = datetime.utcfromtimestamp(dt_expr)
            timezone = TimeZone(timezone, _datetime)

            if not timezone.utc:
                _datetime = _datetime.replace(tzinfo=_tz.tzutc()).astimezone(timezone.tzinfo)

        except:
            pass

        return _datetime

    @property
    def datetime(self):
        return self._datetime

    @property
    def timestamp(self):
        return calendar.timegm(self._datetime.utctimetuple())

    @property
    def tz(self):
        return self._timezone

    def to(self, tz):

        time_zone = TimeZone(tz, self._datetime)

        _datetime = self._datetime.astimezone(time_zone.tzinfo)

        return Arrow(_datetime, time_zone)

    def utc(self):
        return self.to(_tz.tzutc())


