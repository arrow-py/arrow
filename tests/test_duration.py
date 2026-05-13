from datetime import timedelta

import pytest

import arrow
from arrow.duration import Duration


class TestDurationParse:
    def test_full_duration(self):
        d = Duration.parse("P1Y2M3DT4H5M6S")
        assert d.years == 1
        assert d.months == 2
        assert d.days == 3
        assert d.hours == 4
        assert d.minutes == 5
        assert d.seconds == 6

    def test_date_only(self):
        d = Duration.parse("P1Y2M3D")
        assert d.years == 1
        assert d.months == 2
        assert d.days == 3
        assert d.hours == 0
        assert d.minutes == 0
        assert d.seconds == 0

    def test_time_only(self):
        d = Duration.parse("PT4H5M6S")
        assert d.years == 0
        assert d.months == 0
        assert d.days == 0
        assert d.hours == 4
        assert d.minutes == 5
        assert d.seconds == 6

    def test_weeks(self):
        d = Duration.parse("P2W")
        assert d.weeks == 2
        assert d.days == 0

    def test_days_only(self):
        d = Duration.parse("P30D")
        assert d.days == 30

    def test_hours_only(self):
        d = Duration.parse("PT12H")
        assert d.hours == 12

    def test_minutes_only(self):
        d = Duration.parse("PT30M")
        assert d.minutes == 30

    def test_seconds_only(self):
        d = Duration.parse("PT45S")
        assert d.seconds == 45

    def test_fractional_seconds(self):
        d = Duration.parse("PT1.5S")
        assert d.seconds == 1.5

    def test_fractional_hours(self):
        d = Duration.parse("PT0.5H")
        assert d.hours == 0.5

    def test_years_months(self):
        d = Duration.parse("P1Y6M")
        assert d.years == 1
        assert d.months == 6

    def test_invalid_empty(self):
        with pytest.raises(ValueError):
            Duration.parse("")

    def test_invalid_no_p(self):
        with pytest.raises(ValueError):
            Duration.parse("1Y2M3D")

    def test_invalid_only_p(self):
        with pytest.raises(ValueError):
            Duration.parse("P")

    def test_invalid_only_pt(self):
        with pytest.raises(ValueError):
            Duration.parse("PT")

    def test_invalid_garbage(self):
        with pytest.raises(ValueError):
            Duration.parse("not a duration")


class TestDurationFormat:
    def test_full_format(self):
        d = Duration(years=1, months=2, days=3, hours=4, minutes=5, seconds=6)
        assert str(d) == "P1Y2M3DT4H5M6S"

    def test_date_only_format(self):
        d = Duration(years=1, months=2, days=3)
        assert str(d) == "P1Y2M3D"

    def test_time_only_format(self):
        d = Duration(hours=4, minutes=5, seconds=6)
        assert str(d) == "PT4H5M6S"

    def test_weeks_format(self):
        d = Duration(weeks=2)
        assert str(d) == "P2W"

    def test_zero_duration(self):
        d = Duration()
        assert str(d) == "P0D"

    def test_roundtrip(self):
        cases = [
            "P1Y2M3DT4H5M6S",
            "P3D",
            "PT12H",
            "P1Y6M",
            "P2W",
            "PT30M",
            "PT45S",
            "P1Y",
        ]
        for case in cases:
            assert str(Duration.parse(case)) == case

    def test_isoformat_method(self):
        d = Duration(days=5, hours=3)
        assert d.isoformat() == "P5DT3H"


class TestDurationArithmetic:
    def test_add_durations(self):
        d1 = Duration(years=1, months=2)
        d2 = Duration(years=3, days=5)
        result = d1 + d2
        assert result.years == 4
        assert result.months == 2
        assert result.days == 5

    def test_sub_durations(self):
        d1 = Duration(years=3, months=6)
        d2 = Duration(years=1, months=2)
        result = d1 - d2
        assert result.years == 2
        assert result.months == 4

    def test_negate(self):
        d = Duration(years=1, months=2)
        neg = -d
        assert neg.years == -1
        assert neg.months == -2

    def test_add_to_arrow(self):
        arw = arrow.get("2020-01-01")
        d = Duration(years=1, months=2)
        result = arw + d
        assert result.year == 2021
        assert result.month == 3
        assert result.day == 1

    def test_add_days_to_arrow(self):
        arw = arrow.get("2020-01-01")
        d = Duration(days=31)
        result = arw + d
        assert result.year == 2020
        assert result.month == 2
        assert result.day == 1

    def test_add_time_to_arrow(self):
        arw = arrow.get("2020-01-01T00:00:00")
        d = Duration(hours=25, minutes=30)
        result = arw + d
        assert result.day == 2
        assert result.hour == 1
        assert result.minute == 30


class TestDurationEquality:
    def test_equal(self):
        d1 = Duration(years=1, months=2)
        d2 = Duration(years=1, months=2)
        assert d1 == d2

    def test_not_equal(self):
        d1 = Duration(years=1)
        d2 = Duration(years=2)
        assert d1 != d2

    def test_hash(self):
        d1 = Duration(years=1, months=2)
        d2 = Duration(years=1, months=2)
        assert hash(d1) == hash(d2)
        s = {d1, d2}
        assert len(s) == 1


class TestDurationConversions:
    def test_to_timedelta(self):
        d = Duration(days=5, hours=3, minutes=30)
        td = d.to_timedelta()
        assert td == timedelta(days=5, hours=3, minutes=30)

    def test_to_relativedelta(self):
        d = Duration(years=1, months=2, days=3)
        rd = d.to_relativedelta()
        assert rd.years == 1
        assert rd.months == 2
        assert rd.days == 3

    def test_from_timedelta(self):
        td = timedelta(days=5, hours=3, minutes=30, seconds=15)
        d = Duration.from_timedelta(td)
        assert d.days == 5
        assert d.hours == 3
        assert d.minutes == 30
        assert d.seconds == 15
        assert d.years == 0
        assert d.months == 0


class TestDurationRepr:
    def test_repr_full(self):
        d = Duration(years=1, months=2, days=3, hours=4, minutes=5, seconds=6)
        assert (
            repr(d)
            == "Duration(years=1, months=2, days=3, hours=4, minutes=5, seconds=6)"
        )

    def test_repr_empty(self):
        d = Duration()
        assert repr(d) == "Duration()"

    def test_repr_partial(self):
        d = Duration(days=5, hours=3)
        assert repr(d) == "Duration(days=5, hours=3)"


class TestDurationNotImplemented:
    def test_eq_non_duration(self):
        d = Duration(years=1)
        assert d.__eq__("not a duration") is NotImplemented

    def test_add_non_duration(self):
        d = Duration(years=1)
        assert d.__add__("not a duration") is NotImplemented

    def test_radd_non_arrow(self):
        d = Duration(years=1)
        assert d.__radd__("not an arrow") is NotImplemented

    def test_sub_non_duration(self):
        d = Duration(years=1)
        assert d.__sub__("not a duration") is NotImplemented


class TestDurationFromTimedelta:
    def test_from_timedelta_with_microseconds(self):
        td = timedelta(days=1, seconds=30, microseconds=500000)
        d = Duration.from_timedelta(td)
        assert d.days == 1
        assert d.seconds == 30.5

    def test_to_timedelta_with_years_months(self):
        d = Duration(years=1, months=6)
        td = d.to_timedelta()
        expected_days = 1 * 365.25 + 6 * 30.44
        assert td == timedelta(days=expected_days)


class TestDurationFormatNum:
    def test_format_fractional_value(self):
        d = Duration(seconds=1.5)
        assert str(d) == "PT1.5S"

    def test_format_whole_float(self):
        d = Duration(seconds=2.0)
        assert str(d) == "PT2S"


class TestDurationImport:
    def test_importable_from_arrow(self):
        from arrow import Duration as D

        assert D is Duration
