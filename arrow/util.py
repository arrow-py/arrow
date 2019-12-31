# -*- coding: utf-8 -*-
from __future__ import absolute_import

import datetime
from os import name as os_name

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


def windows_datetime_from_timestamp(timestamp, tz=None):
    """Computes datetime from timestamp. Supports negative timestamps on Windows platform."""

    positive_timestamp = abs(timestamp)
    seconds_after_epoch_dt = datetime.datetime.fromtimestamp(positive_timestamp, tz=tz)

    if tz is None:
        tz = dateutil.tz.tzlocal()

    seconds_after_epoch_dt = seconds_after_epoch_dt.replace(tzinfo=tz).astimezone(
        dateutil.tz.tzutc()
    )

    epoch_dt = datetime.datetime(1970, 1, 1, tzinfo=dateutil.tz.tzutc())
    if timestamp < 0:
        epoch_delta = epoch_dt - seconds_after_epoch_dt
    else:
        epoch_delta = seconds_after_epoch_dt - epoch_dt
    dt = epoch_dt + epoch_delta
    dt = dt.replace(tzinfo=dateutil.tz.tzutc())

    if tz == dateutil.tz.tzlocal():
        # astimezone(tzlocal()) fails on Windows, so we need to
        # fake the local timezone by (1) fetching the local tzname
        # and (2) forming a tzinfo object from that tzname
        local_tz = dateutil.tz.gettz(
            datetime.datetime.now(dateutil.tz.tzlocal()).tzname()
        )
        # return dt.astimezone(local_tz).replace(tzinfo=dateutil.tz.tzlocal())
        dt = dt.astimezone(local_tz).replace(tzinfo=dateutil.tz.tzlocal())
        return dt + dt.dst()

    dt = dt.astimezone(tz)
    return dt + dt.dst()


def safe_utcfromtimestamp(timestamp):
    """datetime.utcfromtimestamp alternative that supports negative timestamps on Windows platform."""
    if os_name == "nt" and timestamp < 0:
        return windows_datetime_from_timestamp(timestamp, dateutil.tz.tzutc())
    else:
        return datetime.datetime.utcfromtimestamp(timestamp)


def safe_fromtimestamp(timestamp, tz=None):
    """datetime.fromtimestamp alternative that supports negative timestamps on Windows platform."""
    if os_name == "nt" and timestamp < 0:
        return windows_datetime_from_timestamp(timestamp, tz)
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
    "windows_datetime_from_timestamp",
    "safe_utcfromtimestamp",
    "safe_fromtimestamp",
]
