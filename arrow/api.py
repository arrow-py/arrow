# -*- coding: utf-8 -*-
"""
Provides the default implementation of :class:`ArrowFactory <arrow.factory.ArrowFactory>`
methods for use as a module API.

"""

from __future__ import absolute_import

from arrow.factory import ArrowFactory

# internal default factory.
_factory = ArrowFactory()


def get(*args, **kwargs):
    """Calls the default :class:`ArrowFactory <arrow.factory.ArrowFactory>` ``get`` method."""

    return _factory.get(*args, **kwargs)


get.__doc__ = _factory.get.__doc__


def utcnow():
    """Calls the default :class:`ArrowFactory <arrow.factory.ArrowFactory>` ``utcnow`` method."""

    return _factory.utcnow()


utcnow.__doc__ = _factory.utcnow.__doc__


def now(tz=None):
    """Calls the default :class:`ArrowFactory <arrow.factory.ArrowFactory>` ``now`` method."""

    return _factory.now(tz)


now.__doc__ = _factory.now.__doc__


def factory(type):
    """Returns an :class:`.ArrowFactory` for the specified :class:`Arrow <arrow.arrow.Arrow>`
    or derived type.

    :param type: the type, :class:`Arrow <arrow.arrow.Arrow>` or derived.

    """

    return ArrowFactory(type)


__all__ = ["get", "utcnow", "now", "factory"]
