# -*- coding: utf-8 -*-

from datetime import date, datetime, tzinfo as dt_tzinfo
from time import struct_time
from typing import Any, List, Optional, Tuple, Type, TypeVar, Union, overload

from arrow import _basestring, _tzinfo_exp
from arrow.arrow import Arrow as _Arrow
from arrow.factory import ArrowFactory

# internal default factory.
_factory: ArrowFactory[_Arrow] = ...


@overload
def get(tzinfo: Optional[dt_tzinfo] = None, **kwargs: Any) -> _Arrow:
    ...


@overload
def get(obj: Union[_Arrow, datetime, date, struct_time], /, **kwargs: Any) -> _Arrow:
    ...


@overload
def get(timestamp: Union[int, float, _basestring], /, **kwargs: Any) -> _Arrow:
    ...


@overload
def get(iso_calendar: Tuple[int, int, int], /, **kwargs: Any) -> _Arrow:
    ...


@overload
def get(obj: Union[date, datetime], tz: _tzinfo_exp, /, **kwargs: Any) -> _Arrow:
    ...


@overload
def get(timestamp: _basestring, fmt: Union[_basestring, List[_basestring]], /, **kwargs: Any) -> _Arrow:
    ...


@overload
def get(*args: Any, **kwargs: Any) -> _Arrow:
    ...


def utcnow() -> _Arrow:
    ...


def now(tz: Optional[_tzinfo_exp] = None) -> _Arrow:
    ...


_AT = TypeVar('_AT', bound=_Arrow)


def factory(type: Type[_AT]) -> ArrowFactory[_AT]:
    ...


__all__ = ['get', 'utcnow', 'now', 'factory']
