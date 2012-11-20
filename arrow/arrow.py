from timezone import TimeZone

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
            tz_expr = TimeZone(_tz.tzutc())

        else:
            tz_expr = TimeZone(tz)
            date_expr = _tz_now(tz_expr.tzinfo)

    else:
        if tz is None:
            try:
                tz_expr = TimeZone(date)
                date_expr = _tz_now(tz_expr.tzinfo)
            except:
                date_expr = date
                tz_expr = TimeZone(_tz.tzutc())

        else:
            date_expr = date
            tz_expr = tz

    return Arrow(date_expr, tz_expr)


class Arrow(object):

    def __init__(self, date, tz='UTC'):

        self._timezone = TimeZone(tz)
        self._datetime = self._get_datetime(date, self._timezone)

    def __repr__(self):
        return '{0}({1})'.format(self.__class__.__name__, self.__str__())

    def __str__(self):

        time_str = time.strftime('%x %X', self._datetime.timetuple())

        return '{0}.{1} {2}'.format(time_str, self._datetime.microsecond,
            str(self._timezone))

    @staticmethod
    def _get_datetime(dt_expr, time_zone):

        _datetime = None

        if isinstance(dt_expr, int):
            dt_expr = float(dt_expr)

        if isinstance(dt_expr, str):
            try:
                dt_expr = float(dt_expr)
            except:
                pass

        if isinstance(dt_expr, float):
            if time_zone.utc:
                _datetime = datetime.utcfromtimestamp(dt_expr)
            else:
                _datetime = datetime.fromtimestamp(dt_expr)

        elif isinstance(dt_expr, datetime):
            _datetime = dt_expr

        if _datetime is None:
            raise RuntimeError('Could not recognize datetime')

        return _datetime.replace(tzinfo=time_zone.tzinfo)

    @property
    def datetime(self):
        return self._datetime

    @property
    def timestamp(self):

        if self._timezone.utc:
            return calendar.timegm(self._datetime.utctimetuple())
        else:
            return time.mktime(self._datetime.timetuple())

    @property
    def tz(self):
        return self._timezone

    def to(self, tz):

        time_zone = TimeZone(tz)
        _datetime = self._datetime.astimezone(time_zone.tzinfo)

        return Arrow(_datetime, time_zone)

    def utc(self):
        return self.to('UTC')


