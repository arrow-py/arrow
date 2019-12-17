# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from typing import (
    Any, ClassVar, Dict, List, Literal, Optional, SupportsAbs, SupportsFloat, Text, Type, TypedDict
)


def get_locale(name: Text) -> Locale: ...


# base locale type.

_TimeFrames = Literal[
    'now', 'seconds', 'minute', 'minutes', 'hour', 'hours', 'day',
    'days', 'week', 'weeks', 'month', 'months', 'year', 'years'
]


class _TimeFrameDict(TypedDict):
    now: Text
    seconds: Text
    minute: Text
    minutes: Text
    hour: Text
    hours: Text
    day: Text
    days: Text
    week: Text
    weeks: Text
    month: Text
    months: Text
    year: Text
    years: Text


class _Meridians(TypedDict):
    am: Text
    pm: Text
    AM: Text
    PM: Text


class Locale(object):
    names: ClassVar[List[Text]] = ...

    timeframes: ClassVar[_TimeFrameDict] = ...
    meridians: ClassVar[_Meridians] = ...

    past: Text = ...
    future: Text = ...
    and_word: Text = ...

    month_names: ClassVar[List[Text]] = ...
    month_abbreviations: ClassVar[List[Text]] = ...

    day_names: ClassVar[List[Text]] = ...
    day_abbreviations: ClassVar[List[Text]] = ...

    ordinal_day_re: ClassVar[Text] = ...

    _month_name_to_ordinal: Optional[Dict[Text, int]]

    def __init__(self) -> None:
        ...

    def describe(
            self,
            timeframe: _TimeFrames,
            delta: SupportsAbs[SupportsFloat] = 0,
            only_distance: bool = False
    ) -> Text:
        ...

    def describe_multi(self, timeframes: List[_TimeFrames], only_distance: bool = False) -> Text:
        ...

    def day_name(self, day: int) -> Text:
        ...

    def day_abbreviation(self, day: int) -> Text:
        ...

    def month_name(self, month: int) -> Text:
        ...

    def month_abbreviation(self, month: int) -> Text:
        ...

    def month_number(self, name: Text) -> Optional[int]:
        ...

    def year_full(self, year: int) -> Text:
        ...

    def year_abbreviation(self, year: int) -> Text:
        ...

    def meridian(self, hour: int, token: Any) -> Optional[Text]:
        ...

    def ordinal_number(self, n: int) -> Text:
        ...

    def _ordinal_number(self, n: int) -> Text:
        ...

    def _name_to_ordinal(self, lst: List[Text]) -> Dict[Text, int]:
        ...

    def _format_timeframe(self, timeframe: _TimeFrames, delta: SupportsAbs[SupportsFloat]) -> Text:
        ...

    def _format_relative(self, humanized: Text, timeframe: _TimeFrames, delta: SupportsAbs[SupportsFloat]) -> Text:
        ...


# base locale type implementations.


class EnglishLocale(Locale):
    ...


class ItalianLocale(Locale):
    ...


class SpanishLocale(Locale):
    ...


class FrenchLocale(Locale):
    ...


class GreekLocale(Locale):
    ...


class JapaneseLocale(Locale):
    ...


class SwedishLocale(Locale):
    ...


class FinnishLocale(Locale):
    ...


class ChineseCNLocale(Locale):
    ...


class ChineseTWLocale(Locale):
    ...


class KoreanLocale(Locale):
    ...


# derived locale types & implementations.
class DutchLocale(Locale):
    ...


class SlavicBaseLocale(Locale):
    ...


class BelarusianLocale(SlavicBaseLocale):
    ...


class PolishLocale(SlavicBaseLocale):
    ...


class RussianLocale(SlavicBaseLocale):
    ...


class AfrikaansLocale(Locale):
    ...


class BulgarianLocale(SlavicBaseLocale):
    ...


class UkrainianLocale(SlavicBaseLocale):
    ...


class MacedonianLocale(SlavicBaseLocale):
    ...


class DeutschBaseLocale(Locale):
    timeframes_only_distance: ClassVar[_TimeFrameDict] = ...


class GermanLocale(DeutschBaseLocale, Locale):
    ...


class AustrianLocale(DeutschBaseLocale, Locale):
    ...


class NorwegianLocale(Locale):
    ...


class NewNorwegianLocale(Locale):
    ...


class PortugueseLocale(Locale):
    ...


class BrazilianPortugueseLocale(PortugueseLocale):
    ...


class TagalogLocale(Locale):
    ...


class VietnameseLocale(Locale):
    ...


class TurkishLocale(Locale):
    ...


class AzerbaijaniLocale(Locale):
    ...


class ArabicLocale(Locale):
    ...


class LevantArabicLocale(ArabicLocale):
    ...


class AlgeriaTunisiaArabicLocale(ArabicLocale):
    ...


class MauritaniaArabicLocale(ArabicLocale):
    ...


class MoroccoArabicLocale(ArabicLocale):
    ...


class IcelandicLocale(Locale):
    ...


class DanishLocale(Locale):
    ...


class MalayalamLocale(Locale):
    ...


class HindiLocale(Locale):
    ...


class CzechLocale(Locale):
    ...


class SlovakLocale(Locale):
    ...


class FarsiLocale(Locale):
    ...


class HebrewLocale(Locale):
    ...


class MarathiLocale(Locale):
    ...


def _map_locales() -> Dict[Text, Type[Locale]]: ...


class CatalanLocale(Locale):
    ...


class BasqueLocale(Locale):
    ...


class HungarianLocale(Locale):
    ...


class EsperantoLocale(Locale):
    ...


class ThaiLocale(Locale):
    BE_OFFSET: int = ...


class BengaliLocale(Locale):
    ...


class RomanshLocale(Locale):
    ...


class SwissLocale(Locale):
    ...


class RomanianLocale(Locale):
    ...


class SlovenianLocale(Locale):
    ...


class IndonesianLocale(Locale):
    ...


class NepaliLocale(Locale):
    ...


class EstonianLocale(Locale):
    ...


_locales: Dict[Text, Type[Locale]] = ...
