# -*- coding: utf-8 -*-
import time
from datetime import date, datetime

import pytest
from dateutil import tz

from arrow.parser import ParserError

from .utils import assert_datetime_equality


@pytest.mark.usefixtures("arrow_factory")
class TestGet:
    def test_no_args(self):

        assert_datetime_equality(
            self.factory.get(), datetime.utcnow().replace(tzinfo=tz.tzutc())
        )

    def test_timestamp_one_arg_no_arg(self):

        no_arg = self.factory.get(1406430900).timestamp
        one_arg = self.factory.get("1406430900", "X").timestamp

        assert no_arg == one_arg

    def test_one_arg_none(self):

        assert_datetime_equality(
            self.factory.get(None), datetime.utcnow().replace(tzinfo=tz.tzutc())
        )

    def test_struct_time(self):

        assert_datetime_equality(
            self.factory.get(time.gmtime()),
            datetime.utcnow().replace(tzinfo=tz.tzutc()),
        )

    def test_one_arg_timestamp(self):

        int_timestamp = int(time.time())
        timestamp_dt = datetime.utcfromtimestamp(int_timestamp).replace(
            tzinfo=tz.tzutc()
        )

        assert self.factory.get(int_timestamp) == timestamp_dt

        with pytest.raises(ParserError):
            self.factory.get(str(int_timestamp))

        float_timestamp = time.time()
        timestamp_dt = datetime.utcfromtimestamp(float_timestamp).replace(
            tzinfo=tz.tzutc()
        )

        assert self.factory.get(float_timestamp) == timestamp_dt

        with pytest.raises(ParserError):
            self.factory.get(str(float_timestamp))

        # Regression test for issue #216
        # Python 3 raises OverflowError, Python 2 raises ValueError
        timestamp = 99999999999999999999999999.99999999999999999999999999
        with pytest.raises((OverflowError, ValueError)):
            self.factory.get(timestamp)

    def test_one_arg_expanded_timestamp(self):

        millisecond_timestamp = 1591328104308
        microsecond_timestamp = 1591328104308505

        # Regression test for issue #796
        assert self.factory.get(millisecond_timestamp) == datetime.utcfromtimestamp(
            1591328104.308
        ).replace(tzinfo=tz.tzutc())
        assert self.factory.get(microsecond_timestamp) == datetime.utcfromtimestamp(
            1591328104.308505
        ).replace(tzinfo=tz.tzutc())

    def test_one_arg_timestamp_with_tzinfo(self):

        timestamp = time.time()
        timestamp_dt = datetime.fromtimestamp(timestamp, tz=tz.tzutc()).astimezone(
            tz.gettz("US/Pacific")
        )
        timezone = tz.gettz("US/Pacific")

        assert_datetime_equality(
            self.factory.get(timestamp, tzinfo=timezone), timestamp_dt
        )

    def test_one_arg_arrow(self):

        arw = self.factory.utcnow()
        result = self.factory.get(arw)

        assert arw == result

    def test_one_arg_datetime(self):

        dt = datetime.utcnow().replace(tzinfo=tz.tzutc())

        assert self.factory.get(dt) == dt

    def test_one_arg_date(self):

        d = date.today()
        dt = datetime(d.year, d.month, d.day, tzinfo=tz.tzutc())

        assert self.factory.get(d) == dt

    def test_one_arg_tzinfo(self):

        self.expected = (
            datetime.utcnow()
            .replace(tzinfo=tz.tzutc())
            .astimezone(tz.gettz("US/Pacific"))
        )

        assert_datetime_equality(
            self.factory.get(tz.gettz("US/Pacific")), self.expected
        )

    # regression test for issue #658
    def test_one_arg_dateparser_datetime(self):
        dateparser = pytest.importorskip("dateparser")
        expected = datetime(1990, 1, 1).replace(tzinfo=tz.tzutc())
        # dateparser outputs: datetime.datetime(1990, 1, 1, 0, 0, tzinfo=<StaticTzInfo 'UTC\+00:00'>)
        parsed_date = dateparser.parse("1990-01-01T00:00:00+00:00")
        dt_output = self.factory.get(parsed_date)._datetime.replace(tzinfo=tz.tzutc())
        assert dt_output == expected

    def test_kwarg_tzinfo(self):

        self.expected = (
            datetime.utcnow()
            .replace(tzinfo=tz.tzutc())
            .astimezone(tz.gettz("US/Pacific"))
        )

        assert_datetime_equality(
            self.factory.get(tzinfo=tz.gettz("US/Pacific")), self.expected
        )

    def test_kwarg_tzinfo_string(self):

        self.expected = (
            datetime.utcnow()
            .replace(tzinfo=tz.tzutc())
            .astimezone(tz.gettz("US/Pacific"))
        )

        assert_datetime_equality(self.factory.get(tzinfo="US/Pacific"), self.expected)

        with pytest.raises(ParserError):
            self.factory.get(tzinfo="US/PacificInvalidTzinfo")

    def test_kwarg_normalize_whitespace(self):
        result = self.factory.get(
            "Jun 1 2005  1:33PM",
            "MMM D YYYY H:mmA",
            tzinfo=tz.tzutc(),
            normalize_whitespace=True,
        )
        assert result._datetime == datetime(2005, 6, 1, 13, 33, tzinfo=tz.tzutc())

        result = self.factory.get(
            "\t 2013-05-05T12:30:45.123456 \t \n",
            tzinfo=tz.tzutc(),
            normalize_whitespace=True,
        )
        assert result._datetime == datetime(
            2013, 5, 5, 12, 30, 45, 123456, tzinfo=tz.tzutc()
        )

    def test_one_arg_iso_str(self):

        dt = datetime.utcnow()

        assert_datetime_equality(
            self.factory.get(dt.isoformat()), dt.replace(tzinfo=tz.tzutc())
        )

    def test_one_arg_iso_calendar(self):

        pairs = [
            (datetime(2004, 1, 4), (2004, 1, 7)),
            (datetime(2008, 12, 30), (2009, 1, 2)),
            (datetime(2010, 1, 2), (2009, 53, 6)),
            (datetime(2000, 2, 29), (2000, 9, 2)),
            (datetime(2005, 1, 1), (2004, 53, 6)),
            (datetime(2010, 1, 4), (2010, 1, 1)),
            (datetime(2010, 1, 3), (2009, 53, 7)),
            (datetime(2003, 12, 29), (2004, 1, 1)),
        ]

        for pair in pairs:
            dt, iso = pair
            assert self.factory.get(iso) == self.factory.get(dt)

        with pytest.raises(TypeError):
            self.factory.get((2014, 7, 1, 4))

        with pytest.raises(TypeError):
            self.factory.get((2014, 7))

        with pytest.raises(ValueError):
            self.factory.get((2014, 70, 1))

        with pytest.raises(ValueError):
            self.factory.get((2014, 7, 10))

    def test_one_arg_other(self):

        with pytest.raises(TypeError):
            self.factory.get(object())

    def test_one_arg_bool(self):

        with pytest.raises(TypeError):
            self.factory.get(False)

        with pytest.raises(TypeError):
            self.factory.get(True)

    def test_two_args_datetime_tzinfo(self):

        result = self.factory.get(datetime(2013, 1, 1), tz.gettz("US/Pacific"))

        assert result._datetime == datetime(2013, 1, 1, tzinfo=tz.gettz("US/Pacific"))

    def test_two_args_datetime_tz_str(self):

        result = self.factory.get(datetime(2013, 1, 1), "US/Pacific")

        assert result._datetime == datetime(2013, 1, 1, tzinfo=tz.gettz("US/Pacific"))

    def test_two_args_date_tzinfo(self):

        result = self.factory.get(date(2013, 1, 1), tz.gettz("US/Pacific"))

        assert result._datetime == datetime(2013, 1, 1, tzinfo=tz.gettz("US/Pacific"))

    def test_two_args_date_tz_str(self):

        result = self.factory.get(date(2013, 1, 1), "US/Pacific")

        assert result._datetime == datetime(2013, 1, 1, tzinfo=tz.gettz("US/Pacific"))

    def test_two_args_datetime_other(self):

        with pytest.raises(TypeError):
            self.factory.get(datetime.utcnow(), object())

    def test_two_args_date_other(self):

        with pytest.raises(TypeError):
            self.factory.get(date.today(), object())

    def test_two_args_str_str(self):

        result = self.factory.get("2013-01-01", "YYYY-MM-DD")

        assert result._datetime == datetime(2013, 1, 1, tzinfo=tz.tzutc())

    def test_two_args_str_tzinfo(self):

        result = self.factory.get("2013-01-01", tzinfo=tz.gettz("US/Pacific"))

        assert_datetime_equality(
            result._datetime, datetime(2013, 1, 1, tzinfo=tz.gettz("US/Pacific"))
        )

    def test_two_args_twitter_format(self):

        # format returned by twitter API for created_at:
        twitter_date = "Fri Apr 08 21:08:54 +0000 2016"
        result = self.factory.get(twitter_date, "ddd MMM DD HH:mm:ss Z YYYY")

        assert result._datetime == datetime(2016, 4, 8, 21, 8, 54, tzinfo=tz.tzutc())

    def test_two_args_str_list(self):

        result = self.factory.get("2013-01-01", ["MM/DD/YYYY", "YYYY-MM-DD"])

        assert result._datetime == datetime(2013, 1, 1, tzinfo=tz.tzutc())

    def test_two_args_unicode_unicode(self):

        result = self.factory.get(u"2013-01-01", u"YYYY-MM-DD")

        assert result._datetime == datetime(2013, 1, 1, tzinfo=tz.tzutc())

    def test_two_args_other(self):

        with pytest.raises(TypeError):
            self.factory.get(object(), object())

    def test_three_args_with_tzinfo(self):

        timefmt = "YYYYMMDD"
        d = "20150514"

        assert self.factory.get(d, timefmt, tzinfo=tz.tzlocal()) == datetime(
            2015, 5, 14, tzinfo=tz.tzlocal()
        )

    def test_three_args(self):

        assert self.factory.get(2013, 1, 1) == datetime(2013, 1, 1, tzinfo=tz.tzutc())

    def test_full_kwargs(self):

        assert (
            self.factory.get(
                year=2016,
                month=7,
                day=14,
                hour=7,
                minute=16,
                second=45,
                microsecond=631092,
            )
            == datetime(2016, 7, 14, 7, 16, 45, 631092, tzinfo=tz.tzutc())
        )

    def test_three_kwargs(self):

        assert self.factory.get(year=2016, month=7, day=14) == datetime(
            2016, 7, 14, 0, 0, tzinfo=tz.tzutc()
        )

    def test_tzinfo_string_kwargs(self):
        result = self.factory.get("2019072807", "YYYYMMDDHH", tzinfo="UTC")
        assert result._datetime == datetime(2019, 7, 28, 7, 0, 0, 0, tzinfo=tz.tzutc())

    def test_insufficient_kwargs(self):

        with pytest.raises(TypeError):
            self.factory.get(year=2016)

        with pytest.raises(TypeError):
            self.factory.get(year=2016, month=7)

    def test_locale(self):
        result = self.factory.get("2010", "YYYY", locale="ja")
        assert result._datetime == datetime(2010, 1, 1, 0, 0, 0, 0, tzinfo=tz.tzutc())

        # regression test for issue #701
        result = self.factory.get(
            "Montag, 9. September 2019, 16:15-20:00", "dddd, D. MMMM YYYY", locale="de"
        )
        assert result._datetime == datetime(2019, 9, 9, 0, 0, 0, 0, tzinfo=tz.tzutc())

    def test_locale_kwarg_only(self):
        res = self.factory.get(locale="ja")
        assert res.tzinfo == tz.tzutc()

    def test_locale_with_tzinfo(self):
        res = self.factory.get(locale="ja", tzinfo=tz.gettz("Asia/Tokyo"))
        assert res.tzinfo == tz.gettz("Asia/Tokyo")


@pytest.mark.usefixtures("arrow_factory")
class TestUtcNow:
    def test_utcnow(self):

        assert_datetime_equality(
            self.factory.utcnow()._datetime,
            datetime.utcnow().replace(tzinfo=tz.tzutc()),
        )


@pytest.mark.usefixtures("arrow_factory")
class TestNow:
    def test_no_tz(self):

        assert_datetime_equality(self.factory.now(), datetime.now(tz.tzlocal()))

    def test_tzinfo(self):

        assert_datetime_equality(
            self.factory.now(tz.gettz("EST")), datetime.now(tz.gettz("EST"))
        )

    def test_tz_str(self):

        assert_datetime_equality(self.factory.now("EST"), datetime.now(tz.gettz("EST")))
