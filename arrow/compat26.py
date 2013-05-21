# -*- coding: utf-8 -*-

from datetime import timedelta


def _check(td):
    if td is None or not isinstance(td, timedelta):
        raise ValueError('"td" is not an instance of datetime.timedelta')


if hasattr(timedelta.__class__, 'total_seconds'):

    def get_total_seconds(td=None):
        _check(td)
        return td.total_seconds()

else:

    def get_total_seconds(td=None):
        _check(td)
        return (td.microseconds + (td.seconds + td.days * 24 * 3600) * 1e6) / 1e6

__all__ = ['get_total_seconds']
