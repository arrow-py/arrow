# -*- coding: utf-8 -*-

from typing import Optional, Type, TypeVar

from arrow import _tzinfo_exp
from arrow.arrow import Arrow
from arrow.factory import ArrowFactory

# internal default factory.
_factory: ArrowFactory[Arrow] = ...


def get(*args, **kwargs) -> Arrow:
    ...


def utcnow() -> Arrow:
    ...


def now(tz: Optional[_tzinfo_exp] = None):
    ...


_AT = TypeVar('_AT', bound=Arrow)


def factory(type: Type[_AT]) -> ArrowFactory[_AT]:
    ...


__all__ = ["get", "utcnow", "now", "factory"]
