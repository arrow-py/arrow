# -*- coding: utf-8 -*-
from __future__ import absolute_import

import functools
import sys
import warnings

def total_seconds(td):  # pragma: no cover
    return td.total_seconds()


def is_timestamp(value):
    if type(value) == bool:
        return False
    try:
        float(value)
        return True
    except:
        return False


# Python 2.7 / 3.0+ definitions for isstr function.

try:  # pragma: no cover
    basestring

    def isstr(s):
        return isinstance(s, basestring)

except NameError:  # pragma: no cover

    def isstr(s):
        return isinstance(s, str)


class list_to_iter_shim(list):
    ''' A temporary shim for functions that currently return a list but that will, after a
    deprecation period, return an iteratator.
    '''

    def __init__(self, iterable=(), **kwargs):
        ''' Equivalent to list(iterable).  warn_text will be emitted on all non-iterator operations.
        '''
        self._warn_text = kwargs.pop('warn_text', None) or 'this object will be converted to an iterator in a future release'
        self._iter_count = 0
        list.__init__(self, iterable, **kwargs)

    def _warn(self):
        warnings.warn(self._warn_text, DeprecationWarning)

    def __iter__(self):
        self._iter_count += 1
        if self._iter_count > 1:
            self._warn()
        return list.__iter__(self)

    def _wrap_method(name):
        list_func = getattr(list, name)
        def wrapper(self, *args, **kwargs):
            self._warn()
            return list_func(self, *args, **kwargs)
        return wrapper

    __contains__ = _wrap_method('__contains__')
    __add__ = _wrap_method('__add__')
    __mul__ = _wrap_method('__mul__')
    __getitem__ = _wrap_method('__getitem__')
    # Ideally, we would throw warnings from  __len__, but list(x) calls len(x)
    index = _wrap_method('index')
    count = _wrap_method('count')
    __setitem__ = _wrap_method('__setitem__')
    __delitem__ = _wrap_method('__delitem__')
    append = _wrap_method('append')
    if sys.version_info.major >= 3:  # pragma: no cover
        clear = _wrap_method('clear')
        copy = _wrap_method('copy')
    extend = _wrap_method('extend')
    __iadd__ = _wrap_method('__iadd__')
    __imul__ = _wrap_method('__imul__')
    insert = _wrap_method('insert')
    pop = _wrap_method('pop')
    remove = _wrap_method('remove')
    reverse = _wrap_method('reverse')
    sort = _wrap_method('sort')

    del _wrap_method


def list_to_iter_deprecation(f):
    warn_text = '{0}() will return an iterator in a future release, convert to list({0}())'.format(f.__name__)
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        return list_to_iter_shim(f(*args, **kwargs), warn_text=warn_text)
    return wrapper


__all__ = ['total_seconds', 'is_timestamp', 'isstr', 'list_to_iter_shim', 'list_to_iter_deprecation']
