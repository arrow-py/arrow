from datetime import datetime, timedelta, tzinfo
from dateutil import tz

import re

class TimeZone(object):

    tz_re = re.compile(r'(\+|\-)([0-9]{1,2}):([0-9]{1,2})')

    def __init__(self, time_zone=None):

        if time_zone is None:
            time_zone = tz.tzutc()

        self._tzinfo = self._get_tzinfo(time_zone)

    def __str__(self):

        minutes = self.utcoffset.total_seconds() / 60.0
        hours = int(minutes / 60)
        minutes = minutes - hours * 60

        offset_str = '{0:+03g}:{1:02g}'.format(hours, abs(minutes))

        return '{0} ({1})'.format(offset_str, self.name)

    def __repr__(self):
        return '{0}({1})'.format(self.__class__.__name__, self.__str__())

    @staticmethod
    def _get_tzinfo(tz_expr):

        _tzinfo = None

        if isinstance(tz_expr, TimeZone):
            _tzinfo = tz_expr.tzinfo

        elif isinstance(tz_expr, str):
            _tzinfo = TimeZone._get_tzinfo_str(tz_expr)

        elif isinstance(tz_expr, tzinfo):
            _tzinfo = tz_expr

        elif isinstance(tz_expr, timedelta):
            _tzinfo = tz.tzoffset(None, tz_expr.total_seconds())

        if _tzinfo is None:
            raise Exception('Could not recognize time zone')

        return _tzinfo

    @staticmethod
    def _get_tzinfo_str(tz_expr):

        if tz_expr == 'local':
           return tz.gettz()

        re_match = TimeZone.tz_re.match(tz_expr)

        if re_match:
            sign, hours, minutes = re_match.groups()
            seconds = int(hours) * 3600 + int(minutes) * 60

            if sign == '-':
                seconds *= -1

            return tz.tzoffset(None, seconds)

        else:
            return tz.gettz(tz_expr)

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
