# -*- coding: utf-8 -*-
from __future__ import absolute_import
import locale
from datetime import timedelta
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


# python 2.7 / 3.0+ definitions for isstr function.

try: # pragma: no cover
    basestring

    def isstr(s):
        return isinstance(s, basestring)

except NameError: #pragma: no cover

    def isstr(s):
        return isinstance(s, str)

try: # pragma: no cover
    unicode

    def locale_str(native_str):
        if not isinstance(native_str, unicode):
            native_str = native_str.decode(locale.getpreferredencoding(False))
        return native_str
except NameError: #pragma: no cover
    def locale_str(native_str):
        assert not isinstance(native_str, bytes)
        return native_str

__all__ = ['total_seconds', 'isstr']
