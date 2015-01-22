# -*- coding: utf-8 -*-
from __future__ import absolute_import

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


def astimezone(date, tz):
    ''' Returns a ``datetime`` object, adjusted to the specified tzinfo.

        :param date: a ``datetime`` object.
        :param tz: a ``tzinfo`` object.

    '''

    date = date.astimezone(tz)

    if hasattr(tz, 'normalize'):
        # A pytz function
        # See http://pytz.sourceforge.net/#introduction
        date = tz.normalize(date)

    return date


__all__ = ['total_seconds', 'isstr', 'astimezone']
