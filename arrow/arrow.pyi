# -*- coding: utf-8 -*-


import datetime as dt
from datetime import timedelta
from time import struct_time
from typing import (
    Any, ClassVar, Generator, List, Literal, Optional, SupportsFloat, Tuple, Type, TypeVar, Union, overload
)

from dateutil.relativedelta import relativedelta

from arrow import _basestring, _tzinfo_exp

_AT = TypeVar('_AT', bound='Arrow')

_T_ATTRS = Literal['year', 'month', 'day', 'hour', 'minute', 'second', 'microsecond']
_T_ATTRS_PLURAL = Literal['years', 'months', 'days', 'hours', 'minutes', 'seconds', 'microseconds']
_T_FRAMES = Literal[_T_ATTRS, 'week', 'weeks', 'quarter', 'quarters']

_BOUNDS = Literal['[)', '()', '(]', '[]']

_GRANULARITY = Literal['auto', 'second', 'minute', 'hour', 'week', 'month', 'year']

_V = TypeVar('_V')
_W = TypeVar('_W')


class Arrow(object):
    resolution: ClassVar[timedelta] = ...

    _ATTRS: ClassVar[List[str]] = ...
    _ATTRS_PLURAL: ClassVar[List[str]] = ...
    _MONTHS_PER_QUARTER: ClassVar[int] = 3

    min: ClassVar[Arrow] = ...
    max: ClassVar[Arrow] = ...

    _datetime: dt.datetime

    def __init__(
            self,
            year: int,
            month: int,
            day: int,
            hour: int = 0,
            minute: int = 0,
            second: int = 0,
            microsecond: int = 0,
            tzinfo: Optional[_tzinfo_exp] = None
    ) -> None:
        ...

    # factories: single object, both original and from datetime.

    @classmethod
    def now(cls: Type[_AT], tzinfo: Optional[dt.tzinfo] = None) -> _AT:
        ...

    @classmethod
    def utcnow(cls: Type[_AT]) -> _AT:
        ...

    @classmethod
    def fromtimestamp(cls: Type[_AT], timestamp: Union[int, float, str], tzinfo: Optional[dt.tzinfo] = None) -> _AT:
        ...

    @classmethod
    def utcfromtimestamp(cls: Type[_AT], timestamp: Union[int, float, str]) -> _AT:
        ...

    @classmethod
    def fromdatetime(cls: Type[_AT], dt: dt.datetime, tzinfo: Optional[_tzinfo_exp] = None) -> _AT:
        ...

    @classmethod
    def fromdate(cls: Type[_AT], date: dt.date, tzinfo: Optional[_tzinfo_exp] = None) -> _AT:
        ...

    @classmethod
    def strptime(cls: Type[_AT], date_str: _basestring, fmt: _basestring, tzinfo: Optional[_tzinfo_exp] = None) -> _AT:
        ...

    # factories: ranges and spans

    @classmethod
    def range(
            cls: Type[_AT],
            frame: _T_ATTRS,
            start: dt.datetime,
            end: Optional[dt.datetime] = None,
            tz: Optional[_tzinfo_exp] = None,
            limit: Optional[int] = None
    ) -> Generator[_AT, None, None]:
        ...

    @classmethod
    def span_range(
            cls: Type[_AT],
            frame: _T_ATTRS,
            start: dt.datetime,
            end: dt.datetime,
            tz: Optional[_tzinfo_exp] = None,
            limit: Optional[int] = None,
            bounds: _BOUNDS = '[)'
    ) -> Generator[Tuple[_AT, _AT], None, None]:
        ...

    @classmethod
    def interval(
            cls: Type[_AT],
            frame: _T_ATTRS,
            start: dt.datetime,
            end: dt.datetime,
            interval: int = 1,
            tz: Optional[_tzinfo_exp] = None,
            bounds: _BOUNDS = '[)'
    ) -> Generator[Tuple[_AT, _AT], None, None]:
        ...

    # representations

    def __repr__(self) -> str:
        ...

    def __str__(self) -> str:
        ...

    def __format__(self, formatstr: _basestring) -> str:
        ...

    def __hash__(self) -> int:
        ...

    # attributes & properties

    def __getattr__(self, name: _basestring) -> Any:
        ...

    @property
    def tzinfo(self) -> dt.tzinfo:
        ...

    @tzinfo.setter
    def tzinfo(self, tzinfo: Optional[dt.tzinfo]) -> None:
        ...

    @property
    def datetime(self) -> dt.datetime:
        ...

    @property
    def naive(self) -> dt.datetime:
        ...

    @property
    def timestamp(self) -> int:
        ...

    @property
    def float_timestamp(self) -> float:
        ...

    # mutation and duplication.

    def clone(self: _AT) -> _AT:
        ...

    def replace(
            self: _AT,
            *,
            year: int, month: int, day: int, hour: int, minute: int, second: int, microsecond: int, tzinfo: _tzinfo_exp
    ) -> _AT:
        ...

    def shift(
            self: _AT,
            *,
            years: int, months: int, days: int, hours: int, minutes: int,
            seconds: int, microseconds: int, weeks: int, quarters: int, weekday: int
    ) -> _AT:
        ...

    def to(self: _AT, tz: _tzinfo_exp) -> _AT:
        ...

    @classmethod
    def _validate_bounds(cls, bounds: _BOUNDS) -> None:
        ...

    def span(self: _AT, frame: _T_FRAMES, count: int = 1, bounds: _BOUNDS = '[)') -> Tuple[_AT, _AT]:
        ...

    def floor(self: _AT, frame: _T_FRAMES) -> _AT:
        ...

    def ceil(self: _AT, frame: _T_FRAMES) -> _AT:
        ...

    # string output and formatting.

    def format(self, fmt: _basestring = 'YYYY-MM-DD HH:mm:ssZZ', locale: _basestring = 'en_us') -> _basestring:
        ...

    def humanize(
            self,
            other: Optional[Arrow] = None,
            locale: _basestring = 'en_us',
            only_distance: bool = False,
            granularity: _GRANULARITY = 'auto'
    ) -> _basestring:
        ...

    # query functions

    def is_between(self, start: Arrow, end: Arrow, bounds: _BOUNDS = '()') -> bool:
        ...

    # math

    def __add__(self: _AT, other: Union[timedelta, relativedelta]) -> _AT:
        ...

    def __radd__(self: _AT, other: Union[timedelta, relativedelta]) -> _AT:
        ...

    @overload
    def __sub__(self, other: Union[timedelta, relativedelta]) -> _AT:
        ...

    @overload
    def __sub__(self, other: Union[dt.datetime, Arrow]) -> timedelta:
        ...

    def __rsub__(self, other: dt.datetime) -> timedelta:
        ...

    # comparisons

    def __eq__(self, other: Any) -> bool:
        ...

    def __ne__(self, other: Any) -> bool:
        ...

    def __gt__(self, other: Union[Arrow, dt.datetime]) -> bool:
        ...

    def __ge__(self, other: Union[Arrow, dt.datetime]) -> bool:
        ...

    def __lt__(self, other: Union[Arrow, dt.datetime]) -> bool:
        ...

    def __le__(self, other: Union[Arrow, dt.datetime]) -> bool:
        ...

    def __cmp__(self, other: Union[Arrow, dt.datetime]) -> None:
        ...

    # datetime methods

    def date(self) -> dt.date:
        ...

    def time(self) -> dt.time:
        ...

    def timetz(self) -> dt.time:
        ...

    def astimezone(self, tz: Optional[dt.tzinfo]) -> dt.datetime:
        ...

    def utcoffset(self) -> Optional[timedelta]:
        ...

    def dst(self) -> Optional[timedelta]:
        ...

    def timetuple(self) -> struct_time:
        ...

    def utctimetuple(self) -> struct_time:
        ...

    def toordinal(self) -> int:
        ...

    def weekday(self) -> int:
        ...

    def isoweekday(self) -> int:
        ...

    def isocalendar(self) -> Tuple[int, int, int]:
        ...

    def isoformat(self, sep: str = 'T') -> str:
        ...

    def ctime(self) -> str:
        ...

    def strftime(self, format: _basestring) -> str:
        ...

    def for_json(self) -> str:
        ...

    # internal tools.

    @staticmethod
    def _get_tzinfo(tz_expr: _tzinfo_exp) -> dt.tzinfo:
        ...

    @classmethod
    def _get_datetime(cls, expr: Union[Arrow, dt.datetime, SupportsFloat]) -> dt.datetime:
        ...

    @classmethod
    def _get_frames(cls, name: _T_FRAMES) -> Tuple[_basestring, str, int]:
        ...

    @classmethod
    def _get_iteration_params(cls, end: Optional[_V], limit: Optional[_W]) -> Tuple[Union[_V, Arrow], Union[int, _W]]:
        ...
