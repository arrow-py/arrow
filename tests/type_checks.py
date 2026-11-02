"""Static regression checks, validated by the mypy pre-commit hook."""

from datetime import timezone
from typing import List

import arrow
from arrow.factory import ArrowFactory


def check_get_constructor_overloads() -> List[arrow.Arrow]:
    factory = ArrowFactory()
    return [
        factory.get(2024, 6, 1),
        factory.get(year=2024, month=6, day=1),
        factory.get(2024, month=6, day=1, hour=12),
        factory.get(2024, 6, 1, 12, 30, 45, 123456, "UTC"),
        factory.get(2024, 6, 1, tzinfo=timezone.utc, fold=1),
        factory.get(year=2024, month=6, day=1, locale="en", normalize_whitespace=True),
        arrow.get(2024, 6, 1),
        arrow.get(year=2024, month=6, day=1),
        arrow.get(2024, month=6, day=1, hour=12),
        arrow.get(2024, 6, 1, 12, 30, 45, 123456, "UTC"),
        arrow.get(2024, 6, 1, tzinfo=timezone.utc, fold=1),
        arrow.get(year=2024, month=6, day=1, locale="en", normalize_whitespace=True),
    ]


def check_invalid_constructor_calls() -> None:
    factory = ArrowFactory()
    factory.get(year=2024, month=6)  # type: ignore[call-overload]
    factory.get(year=2024, month=6, day="1")  # type: ignore[call-overload]
    arrow.get(year=2024, month=6)  # type: ignore[call-overload]
    arrow.get(year=2024, month=6, day="1")  # type: ignore[call-overload]
