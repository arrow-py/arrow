# -*- coding: utf-8 -*-
from __future__ import absolute_import

from datetime import timedelta
import sys


def _total_seconds_27(td): # pragma: no cover
    return td.total_seconds()


def _total_seconds_26(td):
    return (td.microseconds + (td.seconds + td.days * 24 * 3600) * 1e6) / 1e6


version = '{0}.{1}.{2}'.format(*sys.version_info[:3])

if version < '2.7': # pragma: no cover
    total_seconds = _total_seconds_26
else: # pragma: no cover
    total_seconds = _total_seconds_27


# Generate a Python 2.x or 3.x compatible function 
# for checking if an arg is a string
try:
    basestring  # attempt to evaluate basestring
    def isstr(s):
        return isinstance(s, basestring)
except NameError:
    def isstr(s):
        return isinstance(s, str)


__all__ = ['total_seconds', 'isstr']
