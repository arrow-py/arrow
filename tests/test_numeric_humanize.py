"""Regression tests for numeric singular output in Arrow.humanize()."""

import pytest

import arrow


@pytest.fixture
def reference():
    return arrow.get(2024, 1, 10, 12, 0, 0)


def test_humanize_numeric_singular_past(reference):
    past = reference.shift(hours=-1)
    assert past.humanize(reference, numeric=True) == "1 hour ago"
    assert past.humanize(reference) == "an hour ago"


def test_humanize_numeric_singular_future(reference):
    future = reference.shift(minutes=1)
    assert future.humanize(reference, numeric=True) == "in 1 minute"
    assert future.humanize(reference, only_distance=True, numeric=True) == "1 minute"


@pytest.mark.parametrize(
    "shift, granularity, expected",
    [
        ({"seconds": 2}, "second", "in 2 seconds"),
        ({"minutes": 1}, "minute", "in 1 minute"),
        ({"hours": 1}, "hour", "in 1 hour"),
        ({"days": 1}, "day", "in 1 day"),
        ({"weeks": 1}, "week", "in 1 week"),
        ({"months": 1}, "month", "in 1 month"),
        ({"days": 92}, "quarter", "in 1 quarter"),
        ({"years": 1}, "year", "in 1 year"),
    ],
)
def test_humanize_numeric_explicit_granularity(reference, shift, granularity, expected):
    future = reference.shift(**shift)
    assert future.humanize(reference, granularity=granularity, numeric=True) == expected


def test_humanize_numeric_multi_granularity(reference):
    future = reference.shift(hours=1, minutes=6)
    assert (
        future.humanize(reference, granularity=["hour", "minute"], numeric=True)
        == "in 1 hour and 6 minutes"
    )
    assert (
        future.humanize(reference, granularity=["hour", "minute"])
        == "in an hour and 6 minutes"
    )


def test_humanize_numeric_multi_with_two_singular_values(reference):
    future = reference.shift(hours=1, minutes=1)
    assert (
        future.humanize(reference, granularity=["hour", "minute"], numeric=True)
        == "in 1 hour and 1 minute"
    )


def test_humanize_numeric_english_variant(reference):
    future = reference.shift(hours=1)
    assert future.humanize(reference, locale="en-gb", numeric=True) == "in 1 hour"


def test_humanize_numeric_other_locales_unchanged(reference):
    future = reference.shift(hours=1)
    assert future.humanize(reference, locale="fr", numeric=True) == future.humanize(
        reference, locale="fr"
    )


def test_humanize_numeric_now_unchanged(reference):
    assert reference.humanize(reference, numeric=True) == "just now"
