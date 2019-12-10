# -*- coding: utf-8 -*-

from datetime import datetime
from typing import ClassVar, Pattern

from arrow import _basestring
from arrow.locales import Locale


class DateTimeFormatter(object):
    _FORMAT_RE: ClassVar[Pattern[str]] = ...

    locale: Locale

    def __init__(self, locale: _basestring = "en_us") -> None:
        ...

    def format(cls, dt: datetime, fmt: _basestring) -> _basestring:
        ...

    def _format_token(self, dt: datetime, token: _basestring) -> _basestring:
        ...
