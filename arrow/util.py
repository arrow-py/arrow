# -*- coding: utf-8 -*-
from __future__ import absolute_import

from datetime import datetime


def total_seconds(td):  # pragma: no cover
    return td.total_seconds()


def is_timestamp(value):
    if isinstance(value, bool):
        return False
    try:
        datetime.fromtimestamp(value)
        return True
    except TypeError:
        return False


# Python 2.7 / 3.0+ definitions for isstr function.

try:  # pragma: no cover
    basestring

    def isstr(s):
        return isinstance(s, basestring)  # noqa: F821


except NameError:  # pragma: no cover

    def isstr(s):
        return isinstance(s, str)


__all__ = ["total_seconds", "is_timestamp", "isstr"]
