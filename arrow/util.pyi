# -*- coding: utf-8 -*-

from datetime import date, datetime, timedelta, tzinfo

from typing import Any, Optional, SupportsFloat


def total_seconds(td: timedelta) -> float:
    ...


def is_timestamp(value: Any) -> bool:
    ...


def windows_datetime_from_timestamp(timestamp: SupportsFloat, tz: Optional[tzinfo] = None) -> datetime:
    ...


def safe_utcfromtimestamp(timestamp: float) -> datetime:
    ...


def safe_fromtimestamp(timestamp: float, tz: Optional[tzinfo] = None) -> datetime:
    ...


def iso_to_gregorian(iso_year: int, iso_week: int, iso_day: int) -> date:
    ...


def isstr(s: Any) -> bool:
    ...


__all__ = [
    "total_seconds",
    "is_timestamp",
    "isstr",
    "iso_to_gregorian",
    "windows_datetime_from_timestamp",
    "safe_utcfromtimestamp",
    "safe_fromtimestamp",
]
