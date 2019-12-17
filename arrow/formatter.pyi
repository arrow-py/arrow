# -*- coding: utf-8 -*-

from datetime import datetime
from typing import ClassVar, Pattern, Optional

# noinspection PyUnresolvedReferences
from arrow import _basestring, locales, util
from arrow.locales import Locale


class DateTimeFormatter(object):
    _FORMAT_RE: ClassVar[Pattern[str]] = ...

    locale: Locale

    def __init__(self, locale: _basestring = "en_us") -> None:
        ...

    def format(cls, dt: datetime, fmt: _basestring) -> _basestring:
        ...

    def _format_token(self, dt: datetime, token: Optional[_basestring]) -> Optional[_basestring]:
        ...
