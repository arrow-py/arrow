# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

from datetime import datetime, tzinfo
from typing import (
    AnyStr, ClassVar, Iterable, List, Literal, Pattern, Sequence, SupportsFloat,
    SupportsIndex, SupportsInt, Text, Tuple, TypedDict, Union, overload
)

from arrow import _basestring
from arrow.locales import Locale


class ParserError(ValueError):
    ...


class ParserMatchError(ParserError):
    ...


class _BaseInputReMap(TypedDict, total=False):
    YYYY: Pattern[Text]
    YY: Pattern[Text]
    MM: Pattern[Text]
    M: Pattern[Text]
    DDDD: Pattern[Text]
    DDD: Pattern[Text]
    DD: Pattern[Text]
    D: Pattern[Text]
    HH: Pattern[Text]
    H: Pattern[Text]
    hh: Pattern[Text]
    h: Pattern[Text]
    mm: Pattern[Text]
    m: Pattern[Text]
    ss: Pattern[Text]
    s: Pattern[Text]
    X: Pattern[Text]
    x: Pattern[Text]
    ZZZ: Pattern[Text]
    ZZ: Pattern[Text]
    Z: Pattern[Text]
    S: Pattern[Text]

    MMMM: Pattern[Text]
    MMM: Pattern[Text]
    Do: Pattern[Text]
    dddd: Pattern[Text]
    ddd: Pattern[Text]
    d: Pattern[Text]
    a: Pattern[Text]
    A: Pattern[Text]


class _Parts(TypedDict, total=False):
    year: int
    month: int
    day_of_year: int
    day: int
    hour: int
    minute: int
    second: int
    microsecond: int
    timestamp: float
    expanded_timestamp: int
    tzinfo: tzinfo
    am_pm: Union[Literal['am'], Literal['pm']]


class DateTimeParser(object):
    _FORMAT_RE: ClassVar[Pattern[Text]] = ...
    _ESCAPE_RE: ClassVar[Pattern[Text]] = ...

    _ONE_OR_TWO_DIGIT_RE: ClassVar[Pattern[Text]] = ...
    _ONE_OR_TWO_OR_THREE_DIGIT_RE: ClassVar[Pattern[Text]] = ...
    _ONE_OR_MORE_DIGIT_RE: ClassVar[Pattern[Text]] = ...
    _TWO_DIGIT_RE: ClassVar[Pattern[Text]] = ...
    _THREE_DIGIT_RE: ClassVar[Pattern[Text]] = ...
    _FOUR_DIGIT_RE: ClassVar[Pattern[Text]] = ...
    _TZ_Z_RE: ClassVar[Pattern[Text]] = ...
    _TZ_ZZ_RE: ClassVar[Pattern[Text]] = ...
    _TZ_NAME_RE: ClassVar[Pattern[Text]] = ...
    _TIMESTAMP_RE: ClassVar[Pattern[Text]] = ...
    _TIMESTAMP_EXPANDED_RE: ClassVar[Pattern[Text]] = ...
    _TIME_RE: ClassVar[Pattern[Text]] = ...

    _BASE_INPUT_RE_MAP: ClassVar[_BaseInputReMap] = ...
    SEPARATORS: ClassVar[List[Text]] = ...

    locale: Locale
    _input_re_map: _BaseInputReMap

    def __init__(self, locale: _basestring = "en_us", cache_size: int = 0) -> None:
        ...

    def parse_iso(self, datetime_string: _basestring) -> datetime:
        ...

    def parse(self, datetime_string: _basestring, fmt: Union[_basestring, Sequence[_basestring]]) -> datetime:
        ...

    def _generate_pattern_re(self, fmt: _basestring) -> Tuple[List[_basestring], Pattern[Text]]:
        ...

    @overload
    def _parse_token(
            self,
            token: Union[
                Literal['YYYY'],
                Literal['YY'],
                Literal['MM'],
                Literal['M'],
                Literal['DDDD'],
                Literal['DDD'],
                Literal['DD'],
                Literal['D'],
                Literal['Do'],
                Literal['HH'], Literal['Hh'], Literal['hH'], Literal['hh'],
                Literal['h'], Literal['H'],
                Literal['mm'],
                Literal['m'],
                Literal['ss'],
                Literal['s'],
                Literal['x'],
            ],
            value: Union[AnyStr, SupportsInt, SupportsIndex],
            parts: _Parts
    ) -> None:
        ...

    @overload
    def _parse_token(
            self,
            token: Literal['X'],
            value: Union[SupportsFloat, SupportsIndex, AnyStr, bytearray],
            parts: _Parts
    ) -> None:
        ...

    @overload
    def _parse_token(
            self,
            token: Union[Literal['MMMM'], Literal['MMM']],
            value: AnyStr,
            parts: _Parts
    ) -> None:
        ...

    @overload
    def _parse_token(
            self,
            token: Union[Literal['S'], Literal['a'], Literal['A'], Literal['ZZZ'], Literal['ZZ'], Literal['Z']],
            value: _basestring,
            parts: _Parts
    ) -> None:
        ...

    @staticmethod
    def _build_datetime(parts: _Parts) -> datetime:
        ...

    def _parse_multiformat(self, string: _basestring, formats: Sequence[_basestring]) -> datetime:
        ...

    # generates a capture group of choices separated by an OR operator
    @staticmethod
    def _generate_choice_re(choices: Iterable[_basestring], flags: int = 0) -> Pattern[Text]:
        ...


class TzinfoParser(object):
    _TZINFO_RE: ClassVar[Pattern[Text]] = ...

    @classmethod
    def parse(cls, tzinfo_string: _basestring) -> tzinfo:
        ...
