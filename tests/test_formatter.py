# -*- coding: utf-8 -*-
from datetime import datetime

import pytest
import pytz
from dateutil import tz as dateutil_tz

from arrow import (
    FORMAT_ATOM,
    FORMAT_COOKIE,
    FORMAT_RFC822,
    FORMAT_RFC850,
    FORMAT_RFC1036,
    FORMAT_RFC1123,
    FORMAT_RFC2822,
    FORMAT_RFC3339,
    FORMAT_RSS,
    FORMAT_W3C,
)

from .utils import make_full_tz_list


@pytest.mark.usefixtures("arrow_formatter")
class TestFormatterFormatToken:
    def test_format(self):

        dt = datetime(2013, 2, 5, 12, 32, 51)

        result = self.formatter.format(dt, "MM-DD-YYYY hh:mm:ss a")

        assert result == "02-05-2013 12:32:51 pm"

    def test_year(self):

        dt = datetime(2013, 1, 1)
        assert self.formatter._format_token(dt, "YYYY") == "2013"
        assert self.formatter._format_token(dt, "YY") == "13"

    def test_month(self):

        dt = datetime(2013, 1, 1)
        assert self.formatter._format_token(dt, "MMMM") == "January"
        assert self.formatter._format_token(dt, "MMM") == "Jan"
        assert self.formatter._format_token(dt, "MM") == "01"
        assert self.formatter._format_token(dt, "M") == "1"

    def test_day(self):

        dt = datetime(2013, 2, 1)
        assert self.formatter._format_token(dt, "DDDD") == "032"
        assert self.formatter._format_token(dt, "DDD") == "32"
        assert self.formatter._format_token(dt, "DD") == "01"
        assert self.formatter._format_token(dt, "D") == "1"
        assert self.formatter._format_token(dt, "Do") == "1st"

        assert self.formatter._format_token(dt, "dddd") == "Friday"
        assert self.formatter._format_token(dt, "ddd") == "Fri"
        assert self.formatter._format_token(dt, "d") == "5"

    def test_hour(self):

        dt = datetime(2013, 1, 1, 2)
        assert self.formatter._format_token(dt, "HH") == "02"
        assert self.formatter._format_token(dt, "H") == "2"

        dt = datetime(2013, 1, 1, 13)
        assert self.formatter._format_token(dt, "HH") == "13"
        assert self.formatter._format_token(dt, "H") == "13"

        dt = datetime(2013, 1, 1, 2)
        assert self.formatter._format_token(dt, "hh") == "02"
        assert self.formatter._format_token(dt, "h") == "2"

        dt = datetime(2013, 1, 1, 13)
        assert self.formatter._format_token(dt, "hh") == "01"
        assert self.formatter._format_token(dt, "h") == "1"

        # test that 12-hour time converts to '12' at midnight
        dt = datetime(2013, 1, 1, 0)
        assert self.formatter._format_token(dt, "hh") == "12"
        assert self.formatter._format_token(dt, "h") == "12"

    def test_minute(self):

        dt = datetime(2013, 1, 1, 0, 1)
        assert self.formatter._format_token(dt, "mm") == "01"
        assert self.formatter._format_token(dt, "m") == "1"

    def test_second(self):

        dt = datetime(2013, 1, 1, 0, 0, 1)
        assert self.formatter._format_token(dt, "ss") == "01"
        assert self.formatter._format_token(dt, "s") == "1"

    def test_sub_second(self):

        dt = datetime(2013, 1, 1, 0, 0, 0, 123456)
        assert self.formatter._format_token(dt, "SSSSSS") == "123456"
        assert self.formatter._format_token(dt, "SSSSS") == "12345"
        assert self.formatter._format_token(dt, "SSSS") == "1234"
        assert self.formatter._format_token(dt, "SSS") == "123"
        assert self.formatter._format_token(dt, "SS") == "12"
        assert self.formatter._format_token(dt, "S") == "1"

        dt = datetime(2013, 1, 1, 0, 0, 0, 2000)
        assert self.formatter._format_token(dt, "SSSSSS") == "002000"
        assert self.formatter._format_token(dt, "SSSSS") == "00200"
        assert self.formatter._format_token(dt, "SSSS") == "0020"
        assert self.formatter._format_token(dt, "SSS") == "002"
        assert self.formatter._format_token(dt, "SS") == "00"
        assert self.formatter._format_token(dt, "S") == "0"

    def test_timestamp(self):

        timestamp = 1588437009.8952794
        dt = datetime.utcfromtimestamp(timestamp)
        expected = str(int(timestamp))
        assert self.formatter._format_token(dt, "X") == expected

        # Must round because time.time() may return a float with greater
        # than 6 digits of precision
        expected = str(int(timestamp * 1000000))
        assert self.formatter._format_token(dt, "x") == expected

    def test_timezone(self):

        dt = datetime.utcnow().replace(tzinfo=dateutil_tz.gettz("US/Pacific"))

        result = self.formatter._format_token(dt, "ZZ")
        assert result == "-07:00" or result == "-08:00"

        result = self.formatter._format_token(dt, "Z")
        assert result == "-0700" or result == "-0800"

    @pytest.mark.parametrize("full_tz_name", make_full_tz_list())
    def test_timezone_formatter(self, full_tz_name):

        # This test will fail if we use "now" as date as soon as we change from/to DST
        dt = datetime(1986, 2, 14, tzinfo=pytz.timezone("UTC")).replace(
            tzinfo=dateutil_tz.gettz(full_tz_name)
        )
        abbreviation = dt.tzname()

        result = self.formatter._format_token(dt, "ZZZ")
        assert result == abbreviation

    def test_am_pm(self):

        dt = datetime(2012, 1, 1, 11)
        assert self.formatter._format_token(dt, "a") == "am"
        assert self.formatter._format_token(dt, "A") == "AM"

        dt = datetime(2012, 1, 1, 13)
        assert self.formatter._format_token(dt, "a") == "pm"
        assert self.formatter._format_token(dt, "A") == "PM"

    def test_week(self):
        dt = datetime(2017, 5, 19)
        assert self.formatter._format_token(dt, "W") == "2017-W20-5"

        # make sure week is zero padded when needed
        dt_early = datetime(2011, 1, 20)
        assert self.formatter._format_token(dt_early, "W") == "2011-W03-4"

    def test_nonsense(self):
        dt = datetime(2012, 1, 1, 11)
        assert self.formatter._format_token(dt, None) is None
        assert self.formatter._format_token(dt, "NONSENSE") is None

    def test_escape(self):

        assert (
            self.formatter.format(
                datetime(2015, 12, 10, 17, 9), "MMMM D, YYYY [at] h:mma"
            )
            == "December 10, 2015 at 5:09pm"
        )

        assert (
            self.formatter.format(
                datetime(2015, 12, 10, 17, 9), "[MMMM] M D, YYYY [at] h:mma"
            )
            == "MMMM 12 10, 2015 at 5:09pm"
        )

        assert (
            self.formatter.format(
                datetime(1990, 11, 25),
                "[It happened on] MMMM Do [in the year] YYYY [a long time ago]",
            )
            == "It happened on November 25th in the year 1990 a long time ago"
        )

        assert (
            self.formatter.format(
                datetime(1990, 11, 25),
                "[It happened on] MMMM Do [in the][ year] YYYY [a long time ago]",
            )
            == "It happened on November 25th in the year 1990 a long time ago"
        )

        assert (
            self.formatter.format(
                datetime(1, 1, 1), "[I'm][ entirely][ escaped,][ weee!]"
            )
            == "I'm entirely escaped, weee!"
        )

        # Special RegEx characters
        assert (
            self.formatter.format(
                datetime(2017, 12, 31, 2, 0), "MMM DD, YYYY |^${}().*+?<>-& h:mm A"
            )
            == "Dec 31, 2017 |^${}().*+?<>-& 2:00 AM"
        )

        # Escaping is atomic: brackets inside brackets are treated literally
        assert self.formatter.format(datetime(1, 1, 1), "[[[ ]]") == "[[ ]"


@pytest.mark.usefixtures("arrow_formatter", "time_1975_12_25")
class TestFormatterBuiltinFormats:
    def test_atom(self):
        assert (
            self.formatter.format(self.datetime, FORMAT_ATOM)
            == "1975-12-25 14:15:16-05:00"
        )

    def test_cookie(self):
        assert (
            self.formatter.format(self.datetime, FORMAT_COOKIE)
            == "Thursday, 25-Dec-1975 14:15:16 EST"
        )

    def test_rfc_822(self):
        assert (
            self.formatter.format(self.datetime, FORMAT_RFC822)
            == "Thu, 25 Dec 75 14:15:16 -0500"
        )

    def test_rfc_850(self):
        assert (
            self.formatter.format(self.datetime, FORMAT_RFC850)
            == "Thursday, 25-Dec-75 14:15:16 EST"
        )

    def test_rfc_1036(self):
        assert (
            self.formatter.format(self.datetime, FORMAT_RFC1036)
            == "Thu, 25 Dec 75 14:15:16 -0500"
        )

    def test_rfc_1123(self):
        assert (
            self.formatter.format(self.datetime, FORMAT_RFC1123)
            == "Thu, 25 Dec 1975 14:15:16 -0500"
        )

    def test_rfc_2822(self):
        assert (
            self.formatter.format(self.datetime, FORMAT_RFC2822)
            == "Thu, 25 Dec 1975 14:15:16 -0500"
        )

    def test_rfc3339(self):
        assert (
            self.formatter.format(self.datetime, FORMAT_RFC3339)
            == "1975-12-25 14:15:16-05:00"
        )

    def test_rss(self):
        assert (
            self.formatter.format(self.datetime, FORMAT_RSS)
            == "Thu, 25 Dec 1975 14:15:16 -0500"
        )

    def test_w3c(self):
        assert (
            self.formatter.format(self.datetime, FORMAT_W3C)
            == "1975-12-25 14:15:16-05:00"
        )
