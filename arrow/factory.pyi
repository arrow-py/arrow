# -*- coding: utf-8 -*-

from datetime import date, datetime, tzinfo as dt_tzinfo
from time import struct_time

from typing import Any, Generic, List, Optional, Tuple, Type, TypeVar, Union, overload

from arrow import _basestring, _tzinfo_exp
from arrow.arrow import Arrow

_AT = TypeVar('_AT', bound=Arrow)


class ArrowFactory(Generic[_AT], object):
    type: Type[_AT]

    def __init__(self, type: Type[_AT] = ...) -> None:
        ...

    @overload
    def get(self, tzinfo: Optional[dt_tzinfo] = None, **kwargs: Any) -> _AT:
        ...

    @overload
    def get(self, obj: Union[Arrow, datetime, date, struct_time], /, **kwargs: Any) -> _AT:
        ...

    @overload
    def get(self, timestamp: Union[int, float, _basestring], /, **kwargs: Any) -> _AT:
        ...

    @overload
    def get(self, iso_calendar: Tuple[int, int, int], /, **kwargs: Any) -> _AT:
        ...

    @overload
    def get(self, obj: Union[date, datetime], tz: _tzinfo_exp, /, **kwargs: Any) -> _AT:
        ...

    @overload
    def get(self, timestamp: _basestring, fmt: Union[_basestring, List[_basestring]], /, **kwargs: Any) -> _AT:
        ...

    @overload
    def get(self, *args: Any, **kwargs: Any) -> _AT:
        ...

    def utcnow(self) -> _AT:
        ...

    def now(self, tz: Optional[_tzinfo_exp] = None) -> _AT:
        ...
