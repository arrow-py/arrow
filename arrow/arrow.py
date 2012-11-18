from datetime import datetime, timedelta, tzinfo

import time, calendar

from dateutil import tz

class TimeZone(object):

    def __init__(self, time_zone=tz.tzutc()):
        self._tzinfo = self._get_tzinfo(time_zone)

    def __repr__(self):
        return '{0}({1}, {2})'.format(self.__class__.__name__, 
            self.name, self.utcoffset)

    def __str__(self):
        return self.__repr__()

    @staticmethod
    def _get_tzinfo(tz_expr):

        _tz_info = None

        if isinstance(tz_expr, str):
            if tz_expr == 'local':
                tz_expr = None

            _tz_info = tz.gettz(tz_expr)

        elif isinstance(tz_expr, tzinfo):
            _tz_info = tz_expr

        elif isinstance(tz_expr, timedelta):
            _tz_info = tz.tzoffset(None, tz_expr.total_seconds())

        if _tz_info is None:
            raise Exception('Could not recognize time zone')

        return _tz_info

    @property
    def name(self):
        dt = datetime.now(self._tzinfo)
        return self._tzinfo.tzname(dt)

    @property
    def utcoffset(self):
        dt = datetime.now(self._tzinfo)
        return self._tzinfo.utcoffset(dt)

    @property
    def utc(self):
        return self.utcoffset.total_seconds() == 0.0

    @property
    def tzinfo(self):
        return self._tzinfo

class Arrow(object):

    def __init__(self, date=None, tz='UTC'):

        self._time_zone = TimeZone(tz)
        self._datetime = self._get_datetime(date, self._time_zone)

    @staticmethod
    def _get_datetime(dt_expr, time_zone):

        _datetime = None

        if dt_expr is None:
            dt_expr = datetime.utcnow()

        if isinstance(dt_expr, str):
            try:
                dt_expr = float(dt_expr)
            except:
                raise NotImplementedError('String parsing coming soon')

        if isinstance(dt_expr, int):
            dt_expr = float(dt_expr)

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
    def datetime(self, tz=None):

        time_zone = self._time_zone if tz is None else TimeZone(tz)
        return self._datetime.astimezone(time_zone.tzinfo)

    @property
    def timestamp(self):

        if self._time_zone.utc:
            return calendar.timegm(self._datetime.utctimetuple())
        else:
            return time.mktime(self._datetime.timetuple())
