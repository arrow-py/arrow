# -*- coding: utf-8 -*-
from __future__ import absolute_import

import calendar
import re
from dateutil import tz as dateutil_tz
from arrow import util, locales, formats

class FormatError(RuntimeError):
    pass

class DateTimeFormatter(object):

    _FORMAT_RE = re.compile('(YYY?Y?|MM?M?M?|DD?D?D?|d?dd?d?|HH?|hh?|mm?|ss?|SS?S?S?S?S?|ZZ?|a|A|X)')

    def __init__(self, locale='en_us'):

        self.locale = locales.get_locale(locale)

    def format(cls, dt, fmt):
        if isinstance(fmt, formats.Format):
            if fmt is formats.rfc2822:
                return DateTimeFormatter.format_rfc2822(dt)
            else:
                raise FormatError("Output format is undefined for format '{0}'".format(fmt.name))
        else:
            return cls._FORMAT_RE.sub(lambda m: cls._format_token(dt, m.group(0)), fmt)


    def format_rfc2822(dt):
        """Given a zone-aware datetime.datetime, format an RFC2822-compliant date string.

        Can't do this with email.utils.formatdate because it can't handle timezones!
        Can't use datetime.datetime.strftime because it won't use the C locale!"""
        rfc2822_day_names = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        rfc2822_month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                               'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

        tz_offset = dt.tzinfo.utcoffset(dt)
        tz_offset_seconds = tz_offset.days * 86400 + tz_offset.seconds

        if tz_offset_seconds < 0:
          sign = '-'
          tz_offset_seconds = -tz_offset_seconds
        else:
          sign = '+'

        tz_offset_minutes = tz_offset_seconds / 60
        tz_offset_hours = tz_offset_minutes % 60

        return "%s, %d %s %04d %02d:%02d:%02d %s%02d%02d" % (
          rfc2822_day_names[dt.weekday()],
          dt.day,
          rfc2822_month_names[dt.month - 1],
          dt.year,
          dt.hour,
          dt.minute,
          dt.second,
          sign,
          tz_offset_minutes / 60,
          tz_offset_minutes % 60
        )

    def _format_token(self, dt, token):

        if token == 'YYYY':
            return '{0:04d}'.format(dt.year)
        if token == 'YY':
            return '{0:04d}'.format(dt.year)[2:]

        if token == 'MMMM':
            return self.locale.month_name(dt.month)
        if token == 'MMM':
            return self.locale.month_abbreviation(dt.month)
        if token == 'MM':
            return '{0:02d}'.format(dt.month)
        if token == 'M':
            return str(dt.month)

        if token == 'DDDD':
            return '{0:03d}'.format(dt.timetuple().tm_yday)
        if token == 'DDD':
            return str(dt.timetuple().tm_yday)
        if token == 'DD':
            return '{0:02d}'.format(dt.day)
        if token == 'D':
            return str(dt.day)

        if token == 'dddd':
            return self.locale.day_name(dt.isoweekday())
        if token == 'ddd':
            return self.locale.day_abbreviation(dt.isoweekday())
        if token == 'd':
            return str(dt.isoweekday())

        if token == 'HH':
            return '{0:02d}'.format(dt.hour)
        if token == 'H':
            return str(dt.hour)
        if token == 'hh':
            return '{0:02d}'.format(dt.hour if 0 < dt.hour < 13 else abs(dt.hour - 12))
        if token == 'h':
            return str(dt.hour if 0 < dt.hour < 13 else abs(dt.hour - 12))

        if token == 'mm':
            return '{0:02d}'.format(dt.minute)
        if token == 'm':
            return str(dt.minute)

        if token == 'ss':
            return '{0:02d}'.format(dt.second)
        if token == 's':
            return str(dt.second)

        if token == 'SSSSSS':
            return str(dt.microsecond)
        if token == 'SSSSS':
            return str(int(dt.microsecond / 10))
        if token == 'SSSS':
            return str(int(dt.microsecond / 100))
        if token == 'SSS':
            return str(int(dt.microsecond / 1000))
        if token == 'SS':
            return str(int(dt.microsecond / 10000))
        if token == 'S':
            return str(int(dt.microsecond / 100000))

        if token == 'X':
            return str(calendar.timegm(dt.utctimetuple()))

        if token in ['ZZ', 'Z']:
            separator = ':' if token == 'ZZ' else ''
            tz = dateutil_tz.tzutc() if dt.tzinfo is None else dt.tzinfo
            total_minutes = int(util.total_seconds(tz.utcoffset(dt)) / 60)

            sign = '+' if total_minutes > 0 else '-'
            total_minutes = abs(total_minutes)
            hour, minute = divmod(total_minutes, 60)

            return '{0}{1:02d}{2}{3:02d}'.format(sign, hour, separator, minute)

        if token in ('a', 'A'):
            return self.locale.meridian(dt.hour, token)

