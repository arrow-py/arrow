# -*- coding: utf-8 -*-
from __future__ import absolute_import

import calendar
import re

from dateutil import tz as dateutil_tz

from arrow import locales, util


class DateTimeFormatter(object):

    # This pattern matches characters enclosed in square brackets are matched as
    # an atomic group. For more info on atomic groups and how to they are
    # emulated in Python's re library, see https://stackoverflow.com/a/13577411/2701578

    _FORMAT_RE = re.compile(
        r"(\[(?:(?=(?P<literal>[^]]))(?P=literal))*\]|YYY?Y?|MM?M?M?|Do|DD?D?D?|d?dd?d?|HH?|hh?|mm?|ss?|SS?S?S?S?S?|ZZ?Z?|a|A|X|W)"
    )

    def __init__(self, locale="en_us"):

        self.locale = locales.get_locale(locale)

    def format(cls, dt, fmt):

        return cls._FORMAT_RE.sub(lambda m: cls._format_token(dt, m.group(0)), fmt)

    def _format_token(self, dt, token):

        if token and token.startswith("[") and token.endswith("]"):
            return token[1:-1]

        if token == "YYYY":
            return self.locale.year_full(dt.year)
        if token == "YY":
            return self.locale.year_abbreviation(dt.year)

        if token == "MMMM":
            return self.locale.month_name(dt.month)
        if token == "MMM":
            return self.locale.month_abbreviation(dt.month)
        if token == "MM":
            return "{:02d}".format(dt.month)
        if token == "M":
            return str(dt.month)

        if token == "DDDD":
            return "{:03d}".format(dt.timetuple().tm_yday)
        if token == "DDD":
            return str(dt.timetuple().tm_yday)
        if token == "DD":
            return "{:02d}".format(dt.day)
        if token == "D":
            return str(dt.day)

        if token == "Do":
            return self.locale.ordinal_number(dt.day)

        if token == "dddd":
            return self.locale.day_name(dt.isoweekday())
        if token == "ddd":
            return self.locale.day_abbreviation(dt.isoweekday())
        if token == "d":
            return str(dt.isoweekday())

        if token == "HH":
            return "{:02d}".format(dt.hour)
        if token == "H":
            return str(dt.hour)
        if token == "hh":
            return "{:02d}".format(dt.hour if 0 < dt.hour < 13 else abs(dt.hour - 12))
        if token == "h":
            return str(dt.hour if 0 < dt.hour < 13 else abs(dt.hour - 12))

        if token == "mm":
            return "{:02d}".format(dt.minute)
        if token == "m":
            return str(dt.minute)

        if token == "ss":
            return "{:02d}".format(dt.second)
        if token == "s":
            return str(dt.second)

        if token == "SSSSSS":
            return str("{:06d}".format(int(dt.microsecond)))
        if token == "SSSSS":
            return str("{:05d}".format(int(dt.microsecond / 10)))
        if token == "SSSS":
            return str("{:04d}".format(int(dt.microsecond / 100)))
        if token == "SSS":
            return str("{:03d}".format(int(dt.microsecond / 1000)))
        if token == "SS":
            return str("{:02d}".format(int(dt.microsecond / 10000)))
        if token == "S":
            return str(int(dt.microsecond / 100000))

        if token == "X":
            return str(calendar.timegm(dt.utctimetuple()))

        if token == "ZZZ":
            return dt.tzname()

        if token in ["ZZ", "Z"]:
            separator = ":" if token == "ZZ" else ""
            tz = dateutil_tz.tzutc() if dt.tzinfo is None else dt.tzinfo
            total_minutes = int(util.total_seconds(tz.utcoffset(dt)) / 60)

            sign = "+" if total_minutes >= 0 else "-"
            total_minutes = abs(total_minutes)
            hour, minute = divmod(total_minutes, 60)

            return "{}{:02d}{}{:02d}".format(sign, hour, separator, minute)

        if token in ("a", "A"):
            return self.locale.meridian(dt.hour, token)

        if token == "W":
            year, week, day = dt.isocalendar()
            return "{}-W{:02d}-{}".format(year, week, day)

    # COOKIE FORMAT: 'Thursday, 25-Dec-1975 14:15:16 EST'
    def _format_cookie(self, dt):
        # Date information
        weekday = self._format_token(dt, "dddd")
        day = self._format_token(dt, "DD")
        month = self._format_token(dt, "MMM")
        year = self._format_token(dt, "YYYY")

        # Time information
        hour = self._format_token(dt, "HH")
        minute = self._format_token(dt, "mm")
        second = self._format_token(dt, "ss")
        timezone = self._format_token(dt, "ZZZ")

        return "{}, {}-{}-{} {}:{}:{} {}".format(
            weekday, day, month, year, hour, minute, second, timezone
        )

    # rfc822 FORMAT: 'Thu, 25 Dec 75 14:15:16 -0500'
    def _format_rfc822(self, dt):
        # Date information
        weekday = self._format_token(dt, "ddd")
        day = self._format_token(dt, "DD")
        month = self._format_token(dt, "MMM")
        year = self._format_token(dt, "YY")

        # Time info
        hour = self._format_token(dt, "HH")
        minute = self._format_token(dt, "mm")
        second = self._format_token(dt, "ss")
        timezone = self._format_token(dt, "Z")

        return "{}, {} {} {} {}:{}:{} {}".format(
            weekday, day, month, year, hour, minute, second, timezone
        )

    # rfc850 FORMAT: 'Thursday, 25-Dec-75 14:15:16 EST'
    def _format_rfc850(self, dt):
        # Date information
        weekday = self._format_token(dt, "dddd")
        day = self._format_token(dt, "DD")
        month = self._format_token(dt, "MMM")
        year = self._format_token(dt, "YY")

        # Time information
        hour = self._format_token(dt, "HH")
        minute = self._format_token(dt, "mm")
        second = self._format_token(dt, "ss")
        timezone = self._format_token(dt, "ZZZ")

        return "{}, {}-{}-{} {}:{}:{} {}".format(
            weekday, day, month, year, hour, minute, second, timezone
        )

    #  rfc1036 FORMAT: 'Thu, 25 Dec 75 14:15:16 -0500'
    def _format_rfc1036(self, dt):
        # Date information
        weekday = self._format_token(dt, "ddd")
        day = self._format_token(dt, "DD")
        month = self._format_token(dt, "MMM")
        year = self._format_token(dt, "YY")

        # Time info
        hour = self._format_token(dt, "HH")
        minute = self._format_token(dt, "mm")
        second = self._format_token(dt, "ss")
        timezone = self._format_token(dt, "Z")

        return "{}, {} {} {} {}:{}:{} {}".format(
            weekday, day, month, year, hour, minute, second, timezone
        )
