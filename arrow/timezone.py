from datetime import datetime, timedelta, tzinfo
from dateutil import tz

class TimeZone(object):

    def __init__(self, time_zone=None):

        if time_zone is None:
            time_zone = tz.tzutc()

        self._tzinfo = self._get_tzinfo(time_zone)

    def __str__(self):

        minutes = self.utcoffset.total_seconds() / 60.0
        hours = minutes / 60.0
        minutes = minutes - hours * 60

        offset_str = '{0:+03g}:{1:02g}'.format(hours, minutes)

        return '{0} ({1})'.format(offset_str, self.name)

    def __repr__(self):
        return '{0}({1})'.format(self.__class__.__name__, self.__str__())

    @staticmethod
    def _get_tzinfo(tz_expr):

        _tzinfo = None

        if isinstance(tz_expr, TimeZone):
            _tzinfo = tz_expr.tzinfo

        elif isinstance(tz_expr, str):
            _tzinfo = tz.gettz() if tz_expr == 'local' else tz.gettz(tz_expr)

        elif isinstance(tz_expr, tzinfo):
            _tzinfo = tz_expr

        elif isinstance(tz_expr, timedelta):
            _tzinfo = tz.tzoffset(None, tz_expr.total_seconds())

        if _tzinfo is None:
            raise Exception('Could not recognize time zone')

        return _tzinfo

    @property
    def name(self):

        try:
            dt = datetime.now(self._tzinfo)
            return self._tzinfo.tzname(dt)

        except:
            return None

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
