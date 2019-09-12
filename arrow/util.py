# -*- coding: utf-8 -*-
from __future__ import absolute_import

import datetime


def total_seconds(td):  # pragma: no cover
    return td.total_seconds()


def is_timestamp(value):
    if isinstance(value, bool):
        return False
    try:
        datetime.datetime.fromtimestamp(value)
        return True
    except TypeError:
        return False


# Credit to https://stackoverflow.com/a/1700069
def iso_to_gregorian(iso_year, iso_week, iso_day):
    """Converts an iso weekday tuple into a datetime object."""

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


__all__ = ["total_seconds", "is_timestamp", "isstr", "iso_to_gregorian"]
