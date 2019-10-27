# -*- coding: utf-8 -*-
from __future__ import absolute_import

import datetime
import math
import os
import time

import dateutil


def total_seconds(td):  # pragma: no cover
    return td.total_seconds()


def is_timestamp(value):
    """Check if value is a valid timestamp."""
    if isinstance(value, bool):
        return False
    if not (
        isinstance(value, int) or isinstance(value, float) or isinstance(value, str)
    ):
        return False
    try:
        float(value)
        return True
    except ValueError:
        return False


def datetime_from_timestamp(timestamp, tz=None):
    """Computes datetime from timestamp. Supports negative timestamps on Windows platform."""
    sec_frac, sec = math.modf(timestamp)
    dt = datetime.datetime(1970, 1, 1, tzinfo=dateutil.tz.tzutc()) + datetime.timedelta(
        seconds=sec, microseconds=sec_frac * 1e6
    )
    if tz is None:
        tz = dateutil.tz.tzlocal()
    if tz == dateutil.tz.tzlocal():
        # because datetime.astimezone does not work on Windows for tzlocal() and dates before the 1970-01-01
        # take timestamp from appropriate time of the year, because of daylight saving time changes
        ts = time.mktime(dt.replace(year=1970).timetuple())
        dt += datetime.datetime.fromtimestamp(ts) - datetime.datetime.utcfromtimestamp(
            ts
        )
        return dt.replace(tzinfo=dateutil.tz.tzlocal())
    else:
        return dt.astimezone(tz)


def safe_utcfromtimestamp(timestamp, os_name=os.name):
    """ datetime.utcfromtimestamp alternative which supports negatvie timestamps on Windows platform."""
    if os_name == "nt" and timestamp < 0:
        return datetime_from_timestamp(timestamp, dateutil.tz.tzutc())
    else:
        return datetime.datetime.utcfromtimestamp(timestamp)


def safe_fromtimestamp(timestamp, tz=None, os_name=os.name):
    """ datetime.fromtimestamp alternative which supports negatvie timestamps on Windows platform."""
    if os_name == "nt" and timestamp < 0:
        return datetime_from_timestamp(timestamp, tz)
    else:
        return datetime.datetime.fromtimestamp(timestamp, tz)


# Credit to https://stackoverflow.com/a/1700069
def iso_to_gregorian(iso_year, iso_week, iso_day):
    """Converts an ISO week date tuple into a datetime object."""

    if not 1 <= iso_week <= 53:
        raise ValueError("ISO Calendar week value must be between 1-53.")

    if not 1 <= iso_day <= 7:
        raise ValueError("ISO Calendar day value must be between 1-7")

    # The first week of the year always contains 4 Jan.
    fourth_jan = datetime.date(iso_year, 1, 4)
    delta = datetime.timedelta(fourth_jan.isoweekday() - 1)
    year_start = fourth_jan - delta
    gregorian = year_start + datetime.timedelta(days=iso_day - 1, weeks=iso_week - 1)

    return gregorian


# Python 2.7 / 3.0+ definitions for isstr function.

try:  # pragma: no cover
    basestring

    def isstr(s):
        return isinstance(s, basestring)  # noqa: F821


except NameError:  # pragma: no cover

    def isstr(s):
        return isinstance(s, str)


__all__ = [
    "total_seconds",
    "is_timestamp",
    "isstr",
    "iso_to_gregorian",
    "datetime_from_timestamp",
    "safe_utcfromtimestamp",
    "safe_fromtimestamp",
]
