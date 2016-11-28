# -*- coding: utf-8 -*-
from __future__ import absolute_import

import sys

# python 2.6 / 2.7 definitions for total_seconds function.

def _total_seconds_27(td): # pragma: no cover
    return td.total_seconds()

def _total_seconds_26(td):
    return (td.microseconds + (td.seconds + td.days * 24 * 3600) * 1e6) / 1e6


# get version info and assign correct total_seconds function.

version = '{0}.{1}.{2}'.format(*sys.version_info[:3])

if version < '2.7': # pragma: no cover
    total_seconds = _total_seconds_26
else: # pragma: no cover
    total_seconds = _total_seconds_27

def is_timestamp(value):
    if type(value) == bool:
        return False
    try:
        float(value)
        return True
    except:
        return False

# python 2.7 / 3.0+ definitions for isstr function.

try: # pragma: no cover
    basestring

    def isstr(s):
        return isinstance(s, basestring)

except NameError: #pragma: no cover

    def isstr(s):
        return isinstance(s, str)


__all__ = ['total_seconds', 'is_timestamp', 'isstr']
