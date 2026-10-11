"""Regression tests for Arrow humanize month/week boundary (candidate fix)."""

import pytest

import arrow

REFERENCE = arrow.get("2026-01-01T12:00:00+00:00")


@pytest.mark.parametrize(
    "days,expected",
    [
        (14, "in 2 weeks"),
        (15, "in 2 weeks"),
        (16, "in 2 weeks"),
        (21, "in 3 weeks"),
        (22, "in a month"),
    ],
)
def test_future_week_month_boundary(days, expected):
    assert REFERENCE.shift(days=days).humanize(REFERENCE) == expected


@pytest.mark.parametrize(
    "days,expected",
    [
        (16, "2 weeks ago"),
        (21, "3 weeks ago"),
        (22, "a month ago"),
    ],
)
def test_past_week_month_boundary(days, expected):
    assert REFERENCE.shift(days=-days).humanize(REFERENCE) == expected


def test_explicit_week_granularity_unchanged():
    assert (
        REFERENCE.shift(days=16).humanize(REFERENCE, granularity="week") == "in 2 weeks"
    )
