# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import calendar
import os
import time
from datetime import datetime

import pytest
from dateutil import tz

import arrow
from arrow import formatter, parser
from arrow.constants import MAX_TIMESTAMP_US
from arrow.parser import DateTimeParser, ParserError, ParserMatchError

from .utils import make_full_tz_list


@pytest.mark.usefixtures("dt_parser")
class TestDateTimeParser:
    def test_parse_multiformat(self, mocker):
        mocker.patch(
            "arrow.parser.DateTimeParser.parse",
            string="str",
            fmt="fmt_a",
            side_effect=parser.ParserError,
        )

        with pytest.raises(parser.ParserError):
            self.parser._parse_multiformat("str", ["fmt_a"])

        mock_datetime = mocker.Mock()
        mocker.patch(
            "arrow.parser.DateTimeParser.parse",
            string="str",
            fmt="fmt_b",
            return_value=mock_datetime,
        )

        result = self.parser._parse_multiformat("str", ["fmt_a", "fmt_b"])
        assert result == mock_datetime

    def test_parse_multiformat_all_fail(self, mocker):
        mocker.patch(
            "arrow.parser.DateTimeParser.parse",
            string="str",
            fmt="fmt_a",
            side_effect=parser.ParserError,
        )

        mocker.patch(
            "arrow.parser.DateTimeParser.parse",
            string="str",
            fmt="fmt_b",
            side_effect=parser.ParserError,
        )

        with pytest.raises(parser.ParserError):
            self.parser._parse_multiformat("str", ["fmt_a", "fmt_b"])

    def test_parse_multiformat_unself_expected_fail(self, mocker):
        class UnselfExpectedError(Exception):
            pass

        mocker.patch(
            "arrow.parser.DateTimeParser.parse",
            string="str",
            fmt="fmt_a",
            side_effect=UnselfExpectedError,
        )

        with pytest.raises(UnselfExpectedError):
            self.parser._parse_multiformat("str", ["fmt_a", "fmt_b"])

    def test_parse_token_nonsense(self):
        parts = {}
        self.parser._parse_token("NONSENSE", "1900", parts)
        assert parts == {}

    def test_parse_token_invalid_meridians(self):
        parts = {}
        self.parser._parse_token("A", "a..m", parts)
        assert parts == {}
        self.parser._parse_token("a", "p..m", parts)
        assert parts == {}

    def test_parser_no_caching(self, mocker):

        mocked_parser = mocker.patch(
            "arrow.parser.DateTimeParser._generate_pattern_re", fmt="fmt_a"
        )
        self.parser = parser.DateTimeParser(cache_size=0)
        for _ in range(100):
            self.parser._generate_pattern_re("fmt_a")
        assert mocked_parser.call_count == 100

    def test_parser_1_line_caching(self, mocker):
        mocked_parser = mocker.patch("arrow.parser.DateTimeParser._generate_pattern_re")
        self.parser = parser.DateTimeParser(cache_size=1)

        for _ in range(100):
            self.parser._generate_pattern_re(fmt="fmt_a")
        assert mocked_parser.call_count == 1
        assert mocked_parser.call_args_list[0] == mocker.call(fmt="fmt_a")

        for _ in range(100):
            self.parser._generate_pattern_re(fmt="fmt_b")
        assert mocked_parser.call_count == 2
        assert mocked_parser.call_args_list[1] == mocker.call(fmt="fmt_b")

        for _ in range(100):
            self.parser._generate_pattern_re(fmt="fmt_a")
        assert mocked_parser.call_count == 3
        assert mocked_parser.call_args_list[2] == mocker.call(fmt="fmt_a")

    def test_parser_multiple_line_caching(self, mocker):
        mocked_parser = mocker.patch("arrow.parser.DateTimeParser._generate_pattern_re")
        self.parser = parser.DateTimeParser(cache_size=2)

        for _ in range(100):
            self.parser._generate_pattern_re(fmt="fmt_a")
        assert mocked_parser.call_count == 1
        assert mocked_parser.call_args_list[0] == mocker.call(fmt="fmt_a")

        for _ in range(100):
            self.parser._generate_pattern_re(fmt="fmt_b")
        assert mocked_parser.call_count == 2
        assert mocked_parser.call_args_list[1] == mocker.call(fmt="fmt_b")

        # fmt_a and fmt_b are in the cache, so no new calls should be made
        for _ in range(100):
            self.parser._generate_pattern_re(fmt="fmt_a")
        for _ in range(100):
            self.parser._generate_pattern_re(fmt="fmt_b")
        assert mocked_parser.call_count == 2
        assert mocked_parser.call_args_list[0] == mocker.call(fmt="fmt_a")
        assert mocked_parser.call_args_list[1] == mocker.call(fmt="fmt_b")

    def test_YY_and_YYYY_format_list(self):

        assert self.parser.parse("15/01/19", ["DD/MM/YY", "DD/MM/YYYY"]) == datetime(
            2019, 1, 15
        )

        # Regression test for issue #580
        assert self.parser.parse("15/01/2019", ["DD/MM/YY", "DD/MM/YYYY"]) == datetime(
            2019, 1, 15
        )

        assert (
            self.parser.parse(
                "15/01/2019T04:05:06.789120Z",
                ["D/M/YYThh:mm:ss.SZ", "D/M/YYYYThh:mm:ss.SZ"],
            )
            == datetime(2019, 1, 15, 4, 5, 6, 789120, tzinfo=tz.tzutc())
        )

    # regression test for issue #447
    def test_timestamp_format_list(self):
        # should not match on the "X" token
        assert (
            self.parser.parse(
                "15 Jul 2000",
                ["MM/DD/YYYY", "YYYY-MM-DD", "X", "DD-MMMM-YYYY", "D MMM YYYY"],
            )
            == datetime(2000, 7, 15)
        )

        with pytest.raises(ParserError):
            self.parser.parse("15 Jul", "X")


@pytest.mark.usefixtures("dt_parser")
class TestDateTimeParserParse:
    def test_parse_list(self, mocker):

        mocker.patch(
            "arrow.parser.DateTimeParser._parse_multiformat",
            string="str",
            formats=["fmt_a", "fmt_b"],
            return_value="result",
        )

        result = self.parser.parse("str", ["fmt_a", "fmt_b"])
        assert result == "result"

    def test_parse_unrecognized_token(self, mocker):

        mocker.patch.dict("arrow.parser.DateTimeParser._BASE_INPUT_RE_MAP")
        del arrow.parser.DateTimeParser._BASE_INPUT_RE_MAP["YYYY"]

        # need to make another local parser to apply patch changes
        _parser = parser.DateTimeParser()
        with pytest.raises(parser.ParserError):
            _parser.parse("2013-01-01", "YYYY-MM-DD")

    def test_parse_parse_no_match(self):

        with pytest.raises(ParserError):
            self.parser.parse("01-01", "YYYY-MM-DD")

    def test_parse_separators(self):

        with pytest.raises(ParserError):
            self.parser.parse("1403549231", "YYYY-MM-DD")

    def test_parse_numbers(self):

        self.expected = datetime(2012, 1, 1, 12, 5, 10)
        assert (
            self.parser.parse("2012-01-01 12:05:10", "YYYY-MM-DD HH:mm:ss")
            == self.expected
        )

    def test_parse_year_two_digit(self):

        self.expected = datetime(1979, 1, 1, 12, 5, 10)
        assert (
            self.parser.parse("79-01-01 12:05:10", "YY-MM-DD HH:mm:ss") == self.expected
        )

    def test_parse_timestamp(self):

        tz_utc = tz.tzutc()
        int_timestamp = int(time.time())
        self.expected = datetime.fromtimestamp(int_timestamp, tz=tz_utc)
        assert self.parser.parse("{:d}".format(int_timestamp), "X") == self.expected

        float_timestamp = time.time()
        self.expected = datetime.fromtimestamp(float_timestamp, tz=tz_utc)
        assert self.parser.parse("{:f}".format(float_timestamp), "X") == self.expected

        # test handling of ns timestamp (arrow will round to 6 digits regardless)
        self.expected = datetime.fromtimestamp(float_timestamp, tz=tz_utc)
        assert (
            self.parser.parse("{:f}123".format(float_timestamp), "X") == self.expected
        )

        # test ps timestamp (arrow will round to 6 digits regardless)
        self.expected = datetime.fromtimestamp(float_timestamp, tz=tz_utc)
        assert (
            self.parser.parse("{:f}123456".format(float_timestamp), "X")
            == self.expected
        )

        # NOTE: negative timestamps cannot be handled by datetime on Window
        # Must use timedelta to handle them. ref: https://stackoverflow.com/questions/36179914
        if os.name != "nt":
            # regression test for issue #662
            negative_int_timestamp = -int_timestamp
            self.expected = datetime.fromtimestamp(negative_int_timestamp, tz=tz_utc)
            assert (
                self.parser.parse("{:d}".format(negative_int_timestamp), "X")
                == self.expected
            )

            negative_float_timestamp = -float_timestamp
            self.expected = datetime.fromtimestamp(negative_float_timestamp, tz=tz_utc)
            assert (
                self.parser.parse("{:f}".format(negative_float_timestamp), "X")
                == self.expected
            )

        # NOTE: timestamps cannot be parsed from natural language strings (by removing the ^...$) because it will
        # break cases like "15 Jul 2000" and a format list (see issue #447)
        with pytest.raises(ParserError):
            natural_lang_string = "Meet me at {} at the restaurant.".format(
                float_timestamp
            )
            self.parser.parse(natural_lang_string, "X")

        with pytest.raises(ParserError):
            self.parser.parse("1565982019.", "X")

        with pytest.raises(ParserError):
            self.parser.parse(".1565982019", "X")

    def test_parse_expanded_timestamp(self):
        # test expanded timestamps that include milliseconds
        # and microseconds as multiples rather than decimals
        # requested in issue #357

        tz_utc = tz.tzutc()
        timestamp = 1569982581.413132
        timestamp_milli = int(round(timestamp * 1000))
        timestamp_micro = int(round(timestamp * 1000000))

        # "x" token should parse integer timestamps below MAX_TIMESTAMP normally
        self.expected = datetime.fromtimestamp(int(timestamp), tz=tz_utc)
        assert self.parser.parse("{:d}".format(int(timestamp)), "x") == self.expected

        self.expected = datetime.fromtimestamp(round(timestamp, 3), tz=tz_utc)
        assert self.parser.parse("{:d}".format(timestamp_milli), "x") == self.expected

        self.expected = datetime.fromtimestamp(timestamp, tz=tz_utc)
        assert self.parser.parse("{:d}".format(timestamp_micro), "x") == self.expected

        # anything above max µs timestamp should fail
        with pytest.raises(ValueError):
            self.parser.parse("{:d}".format(int(MAX_TIMESTAMP_US) + 1), "x")

        # floats are not allowed with the "x" token
        with pytest.raises(ParserMatchError):
            self.parser.parse("{:f}".format(timestamp), "x")

    def test_parse_names(self):

        self.expected = datetime(2012, 1, 1)

        assert self.parser.parse("January 1, 2012", "MMMM D, YYYY") == self.expected
        assert self.parser.parse("Jan 1, 2012", "MMM D, YYYY") == self.expected

    def test_parse_pm(self):

        self.expected = datetime(1, 1, 1, 13, 0, 0)
        assert self.parser.parse("1 pm", "H a") == self.expected
        assert self.parser.parse("1 pm", "h a") == self.expected

        self.expected = datetime(1, 1, 1, 1, 0, 0)
        assert self.parser.parse("1 am", "H A") == self.expected
        assert self.parser.parse("1 am", "h A") == self.expected

        self.expected = datetime(1, 1, 1, 0, 0, 0)
        assert self.parser.parse("12 am", "H A") == self.expected
        assert self.parser.parse("12 am", "h A") == self.expected

        self.expected = datetime(1, 1, 1, 12, 0, 0)
        assert self.parser.parse("12 pm", "H A") == self.expected
        assert self.parser.parse("12 pm", "h A") == self.expected

    def test_parse_tz_hours_only(self):

        self.expected = datetime(2025, 10, 17, 5, 30, 10, tzinfo=tz.tzoffset(None, 0))
        parsed = self.parser.parse("2025-10-17 05:30:10+00", "YYYY-MM-DD HH:mm:ssZ")
        assert parsed == self.expected

    def test_parse_tz_zz(self):

        self.expected = datetime(2013, 1, 1, tzinfo=tz.tzoffset(None, -7 * 3600))
        assert self.parser.parse("2013-01-01 -07:00", "YYYY-MM-DD ZZ") == self.expected

    @pytest.mark.parametrize("full_tz_name", make_full_tz_list())
    def test_parse_tz_name_zzz(self, full_tz_name):

        self.expected = datetime(2013, 1, 1, tzinfo=tz.gettz(full_tz_name))
        assert (
            self.parser.parse("2013-01-01 {}".format(full_tz_name), "YYYY-MM-DD ZZZ")
            == self.expected
        )

        # note that offsets are not timezones
        with pytest.raises(ParserError):
            self.parser.parse("2013-01-01 12:30:45.9+1000", "YYYY-MM-DDZZZ")

        with pytest.raises(ParserError):
            self.parser.parse("2013-01-01 12:30:45.9+10:00", "YYYY-MM-DDZZZ")

        with pytest.raises(ParserError):
            self.parser.parse("2013-01-01 12:30:45.9-10", "YYYY-MM-DDZZZ")

    def test_parse_subsecond(self):
        self.expected = datetime(2013, 1, 1, 12, 30, 45, 900000)
        assert (
            self.parser.parse("2013-01-01 12:30:45.9", "YYYY-MM-DD HH:mm:ss.S")
            == self.expected
        )

        self.expected = datetime(2013, 1, 1, 12, 30, 45, 980000)
        assert (
            self.parser.parse("2013-01-01 12:30:45.98", "YYYY-MM-DD HH:mm:ss.SS")
            == self.expected
        )

        self.expected = datetime(2013, 1, 1, 12, 30, 45, 987000)
        assert (
            self.parser.parse("2013-01-01 12:30:45.987", "YYYY-MM-DD HH:mm:ss.SSS")
            == self.expected
        )

        self.expected = datetime(2013, 1, 1, 12, 30, 45, 987600)
        assert (
            self.parser.parse("2013-01-01 12:30:45.9876", "YYYY-MM-DD HH:mm:ss.SSSS")
            == self.expected
        )

        self.expected = datetime(2013, 1, 1, 12, 30, 45, 987650)
        assert (
            self.parser.parse("2013-01-01 12:30:45.98765", "YYYY-MM-DD HH:mm:ss.SSSSS")
            == self.expected
        )

        self.expected = datetime(2013, 1, 1, 12, 30, 45, 987654)
        assert (
            self.parser.parse(
                "2013-01-01 12:30:45.987654", "YYYY-MM-DD HH:mm:ss.SSSSSS"
            )
            == self.expected
        )

    def test_parse_subsecond_rounding(self):
        self.expected = datetime(2013, 1, 1, 12, 30, 45, 987654)
        datetime_format = "YYYY-MM-DD HH:mm:ss.S"

        # round up
        string = "2013-01-01 12:30:45.9876539"
        assert self.parser.parse(string, datetime_format) == self.expected
        assert self.parser.parse_iso(string) == self.expected

        # round down
        string = "2013-01-01 12:30:45.98765432"
        assert self.parser.parse(string, datetime_format) == self.expected
        assert self.parser.parse_iso(string) == self.expected

        # round half-up
        string = "2013-01-01 12:30:45.987653521"
        assert self.parser.parse(string, datetime_format) == self.expected
        assert self.parser.parse_iso(string) == self.expected

        # round half-down
        string = "2013-01-01 12:30:45.9876545210"
        assert self.parser.parse(string, datetime_format) == self.expected
        assert self.parser.parse_iso(string) == self.expected

    # overflow (zero out the subseconds and increment the seconds)
    # regression tests for issue #636
    def test_parse_subsecond_rounding_overflow(self):
        datetime_format = "YYYY-MM-DD HH:mm:ss.S"

        self.expected = datetime(2013, 1, 1, 12, 30, 46)
        string = "2013-01-01 12:30:45.9999995"
        assert self.parser.parse(string, datetime_format) == self.expected
        assert self.parser.parse_iso(string) == self.expected

        self.expected = datetime(2013, 1, 1, 12, 31, 0)
        string = "2013-01-01 12:30:59.9999999"
        assert self.parser.parse(string, datetime_format) == self.expected
        assert self.parser.parse_iso(string) == self.expected

        self.expected = datetime(2013, 1, 2, 0, 0, 0)
        string = "2013-01-01 23:59:59.9999999"
        assert self.parser.parse(string, datetime_format) == self.expected
        assert self.parser.parse_iso(string) == self.expected

        # 6 digits should remain unrounded
        self.expected = datetime(2013, 1, 1, 12, 30, 45, 999999)
        string = "2013-01-01 12:30:45.999999"
        assert self.parser.parse(string, datetime_format) == self.expected
        assert self.parser.parse_iso(string) == self.expected

    # Regression tests for issue #560
    def test_parse_long_year(self):
        with pytest.raises(ParserError):
            self.parser.parse("09 January 123456789101112", "DD MMMM YYYY")

        with pytest.raises(ParserError):
            self.parser.parse("123456789101112 09 January", "YYYY DD MMMM")

        with pytest.raises(ParserError):
            self.parser.parse("68096653015/01/19", "YY/M/DD")

    def test_parse_with_extra_words_at_start_and_end_invalid(self):
        input_format_pairs = [
            ("blah2016", "YYYY"),
            ("blah2016blah", "YYYY"),
            ("2016blah", "YYYY"),
            ("2016-05blah", "YYYY-MM"),
            ("2016-05-16blah", "YYYY-MM-DD"),
            ("2016-05-16T04:05:06.789120blah", "YYYY-MM-DDThh:mm:ss.S"),
            ("2016-05-16T04:05:06.789120ZblahZ", "YYYY-MM-DDThh:mm:ss.SZ"),
            ("2016-05-16T04:05:06.789120Zblah", "YYYY-MM-DDThh:mm:ss.SZ"),
            ("2016-05-16T04:05:06.789120blahZ", "YYYY-MM-DDThh:mm:ss.SZ"),
        ]

        for pair in input_format_pairs:
            with pytest.raises(ParserError):
                self.parser.parse(pair[0], pair[1])

    def test_parse_with_extra_words_at_start_and_end_valid(self):
        # Spaces surrounding the parsable date are ok because we
        # allow the parsing of natural language input. Additionally, a single
        # character of specific punctuation before or after the date is okay.
        # See docs for full list of valid punctuation.

        assert self.parser.parse("blah 2016 blah", "YYYY") == datetime(2016, 1, 1)

        assert self.parser.parse("blah 2016", "YYYY") == datetime(2016, 1, 1)

        assert self.parser.parse("2016 blah", "YYYY") == datetime(2016, 1, 1)

        # test one additional space along with space divider
        assert self.parser.parse(
            "blah 2016-05-16 04:05:06.789120", "YYYY-MM-DD hh:mm:ss.S"
        ) == datetime(2016, 5, 16, 4, 5, 6, 789120)

        assert self.parser.parse(
            "2016-05-16 04:05:06.789120 blah", "YYYY-MM-DD hh:mm:ss.S"
        ) == datetime(2016, 5, 16, 4, 5, 6, 789120)

        # test one additional space along with T divider
        assert self.parser.parse(
            "blah 2016-05-16T04:05:06.789120", "YYYY-MM-DDThh:mm:ss.S"
        ) == datetime(2016, 5, 16, 4, 5, 6, 789120)

        assert self.parser.parse(
            "2016-05-16T04:05:06.789120 blah", "YYYY-MM-DDThh:mm:ss.S"
        ) == datetime(2016, 5, 16, 4, 5, 6, 789120)

        assert (
            self.parser.parse(
                "Meet me at 2016-05-16T04:05:06.789120 at the restaurant.",
                "YYYY-MM-DDThh:mm:ss.S",
            )
            == datetime(2016, 5, 16, 4, 5, 6, 789120)
        )

        assert (
            self.parser.parse(
                "Meet me at 2016-05-16 04:05:06.789120 at the restaurant.",
                "YYYY-MM-DD hh:mm:ss.S",
            )
            == datetime(2016, 5, 16, 4, 5, 6, 789120)
        )

    # regression test for issue #701
    # tests cases of a partial match surrounded by punctuation
    # for the list of valid punctuation, see documentation
    def test_parse_with_punctuation_fences(self):
        assert self.parser.parse(
            "Meet me at my house on Halloween (2019-31-10)", "YYYY-DD-MM"
        ) == datetime(2019, 10, 31)

        assert self.parser.parse(
            "Monday, 9. September 2019, 16:15-20:00", "dddd, D. MMMM YYYY"
        ) == datetime(2019, 9, 9)

        assert self.parser.parse("A date is 11.11.2011.", "DD.MM.YYYY") == datetime(
            2011, 11, 11
        )

        with pytest.raises(ParserMatchError):
            self.parser.parse("11.11.2011.1 is not a valid date.", "DD.MM.YYYY")

        with pytest.raises(ParserMatchError):
            self.parser.parse(
                "This date has too many punctuation marks following it (11.11.2011).",
                "DD.MM.YYYY",
            )

    def test_parse_with_leading_and_trailing_whitespace(self):
        assert self.parser.parse("      2016", "YYYY") == datetime(2016, 1, 1)

        assert self.parser.parse("2016      ", "YYYY") == datetime(2016, 1, 1)

        assert self.parser.parse("      2016      ", "YYYY") == datetime(2016, 1, 1)

        assert self.parser.parse(
            "      2016-05-16 04:05:06.789120      ", "YYYY-MM-DD hh:mm:ss.S"
        ) == datetime(2016, 5, 16, 4, 5, 6, 789120)

        assert self.parser.parse(
            "      2016-05-16T04:05:06.789120      ", "YYYY-MM-DDThh:mm:ss.S"
        ) == datetime(2016, 5, 16, 4, 5, 6, 789120)

    def test_parse_YYYY_DDDD(self):
        assert self.parser.parse("1998-136", "YYYY-DDDD") == datetime(1998, 5, 16)

        assert self.parser.parse("1998-006", "YYYY-DDDD") == datetime(1998, 1, 6)

        with pytest.raises(ParserError):
            self.parser.parse("1998-456", "YYYY-DDDD")

    def test_parse_YYYY_DDD(self):
        assert self.parser.parse("1998-6", "YYYY-DDD") == datetime(1998, 1, 6)

        assert self.parser.parse("1998-136", "YYYY-DDD") == datetime(1998, 5, 16)

        with pytest.raises(ParserError):
            self.parser.parse("1998-756", "YYYY-DDD")

    # month cannot be passed with DDD and DDDD tokens
    def test_parse_YYYY_MM_DDDD(self):
        with pytest.raises(ParserError):
            self.parser.parse("2015-01-009", "YYYY-MM-DDDD")

    # year is required with the DDD and DDDD tokens
    def test_parse_DDD_only(self):
        with pytest.raises(ParserError):
            self.parser.parse("5", "DDD")

    def test_parse_DDDD_only(self):
        with pytest.raises(ParserError):
            self.parser.parse("145", "DDDD")

    def test_parse_ddd_and_dddd(self):
        fr_parser = parser.DateTimeParser("fr")

        # Day of week should be ignored when a day is passed
        # 2019-10-17 is a Thursday, so we know day of week
        # is ignored if the same date is outputted
        expected = datetime(2019, 10, 17)
        assert self.parser.parse("Tue 2019-10-17", "ddd YYYY-MM-DD") == expected
        assert fr_parser.parse("mar 2019-10-17", "ddd YYYY-MM-DD") == expected
        assert self.parser.parse("Tuesday 2019-10-17", "dddd YYYY-MM-DD") == expected
        assert fr_parser.parse("mardi 2019-10-17", "dddd YYYY-MM-DD") == expected

        # Get first Tuesday after epoch
        expected = datetime(1970, 1, 6)
        assert self.parser.parse("Tue", "ddd") == expected
        assert fr_parser.parse("mar", "ddd") == expected
        assert self.parser.parse("Tuesday", "dddd") == expected
        assert fr_parser.parse("mardi", "dddd") == expected

        # Get first Tuesday in 2020
        expected = datetime(2020, 1, 7)
        assert self.parser.parse("Tue 2020", "ddd YYYY") == expected
        assert fr_parser.parse("mar 2020", "ddd YYYY") == expected
        assert self.parser.parse("Tuesday 2020", "dddd YYYY") == expected
        assert fr_parser.parse("mardi 2020", "dddd YYYY") == expected

        # Get first Tuesday in February 2020
        expected = datetime(2020, 2, 4)
        assert self.parser.parse("Tue 02 2020", "ddd MM YYYY") == expected
        assert fr_parser.parse("mar 02 2020", "ddd MM YYYY") == expected
        assert self.parser.parse("Tuesday 02 2020", "dddd MM YYYY") == expected
        assert fr_parser.parse("mardi 02 2020", "dddd MM YYYY") == expected

        # Get first Tuesday in February after epoch
        expected = datetime(1970, 2, 3)
        assert self.parser.parse("Tue 02", "ddd MM") == expected
        assert fr_parser.parse("mar 02", "ddd MM") == expected
        assert self.parser.parse("Tuesday 02", "dddd MM") == expected
        assert fr_parser.parse("mardi 02", "dddd MM") == expected

        # Times remain intact
        expected = datetime(2020, 2, 4, 10, 25, 54, 123456, tz.tzoffset(None, -3600))
        assert (
            self.parser.parse(
                "Tue 02 2020 10:25:54.123456-01:00", "ddd MM YYYY HH:mm:ss.SZZ"
            )
            == expected
        )
        assert (
            fr_parser.parse(
                "mar 02 2020 10:25:54.123456-01:00", "ddd MM YYYY HH:mm:ss.SZZ"
            )
            == expected
        )
        assert (
            self.parser.parse(
                "Tuesday 02 2020 10:25:54.123456-01:00", "dddd MM YYYY HH:mm:ss.SZZ"
            )
            == expected
        )
        assert (
            fr_parser.parse(
                "mardi 02 2020 10:25:54.123456-01:00", "dddd MM YYYY HH:mm:ss.SZZ"
            )
            == expected
        )

    def test_parse_ddd_and_dddd_ignore_case(self):
        # Regression test for issue #851
        expected = datetime(2019, 6, 24)
        assert (
            self.parser.parse("MONDAY, June 24, 2019", "dddd, MMMM DD, YYYY")
            == expected
        )

    def test_parse_ddd_and_dddd_then_format(self):
        # Regression test for issue #446
        arw_formatter = formatter.DateTimeFormatter()
        assert arw_formatter.format(self.parser.parse("Mon", "ddd"), "ddd") == "Mon"
        assert (
            arw_formatter.format(self.parser.parse("Monday", "dddd"), "dddd")
            == "Monday"
        )
        assert arw_formatter.format(self.parser.parse("Tue", "ddd"), "ddd") == "Tue"
        assert (
            arw_formatter.format(self.parser.parse("Tuesday", "dddd"), "dddd")
            == "Tuesday"
        )
        assert arw_formatter.format(self.parser.parse("Wed", "ddd"), "ddd") == "Wed"
        assert (
            arw_formatter.format(self.parser.parse("Wednesday", "dddd"), "dddd")
            == "Wednesday"
        )
        assert arw_formatter.format(self.parser.parse("Thu", "ddd"), "ddd") == "Thu"
        assert (
            arw_formatter.format(self.parser.parse("Thursday", "dddd"), "dddd")
            == "Thursday"
        )
        assert arw_formatter.format(self.parser.parse("Fri", "ddd"), "ddd") == "Fri"
        assert (
            arw_formatter.format(self.parser.parse("Friday", "dddd"), "dddd")
            == "Friday"
        )
        assert arw_formatter.format(self.parser.parse("Sat", "ddd"), "ddd") == "Sat"
        assert (
            arw_formatter.format(self.parser.parse("Saturday", "dddd"), "dddd")
            == "Saturday"
        )
        assert arw_formatter.format(self.parser.parse("Sun", "ddd"), "ddd") == "Sun"
        assert (
            arw_formatter.format(self.parser.parse("Sunday", "dddd"), "dddd")
            == "Sunday"
        )

    def test_parse_HH_24(self):
        assert self.parser.parse(
            "2019-10-30T24:00:00", "YYYY-MM-DDTHH:mm:ss"
        ) == datetime(2019, 10, 31, 0, 0, 0, 0)
        assert self.parser.parse("2019-10-30T24:00", "YYYY-MM-DDTHH:mm") == datetime(
            2019, 10, 31, 0, 0, 0, 0
        )
        assert self.parser.parse("2019-10-30T24", "YYYY-MM-DDTHH") == datetime(
            2019, 10, 31, 0, 0, 0, 0
        )
        assert self.parser.parse(
            "2019-10-30T24:00:00.0", "YYYY-MM-DDTHH:mm:ss.S"
        ) == datetime(2019, 10, 31, 0, 0, 0, 0)
        assert self.parser.parse(
            "2019-10-31T24:00:00", "YYYY-MM-DDTHH:mm:ss"
        ) == datetime(2019, 11, 1, 0, 0, 0, 0)
        assert self.parser.parse(
            "2019-12-31T24:00:00", "YYYY-MM-DDTHH:mm:ss"
        ) == datetime(2020, 1, 1, 0, 0, 0, 0)
        assert self.parser.parse(
            "2019-12-31T23:59:59.9999999", "YYYY-MM-DDTHH:mm:ss.S"
        ) == datetime(2020, 1, 1, 0, 0, 0, 0)

        with pytest.raises(ParserError):
            self.parser.parse("2019-12-31T24:01:00", "YYYY-MM-DDTHH:mm:ss")

        with pytest.raises(ParserError):
            self.parser.parse("2019-12-31T24:00:01", "YYYY-MM-DDTHH:mm:ss")

        with pytest.raises(ParserError):
            self.parser.parse("2019-12-31T24:00:00.1", "YYYY-MM-DDTHH:mm:ss.S")

        with pytest.raises(ParserError):
            self.parser.parse("2019-12-31T24:00:00.999999", "YYYY-MM-DDTHH:mm:ss.S")

    def test_parse_W(self):

        assert self.parser.parse("2011-W05-4", "W") == datetime(2011, 2, 3)
        assert self.parser.parse("2011W054", "W") == datetime(2011, 2, 3)
        assert self.parser.parse("2011-W05", "W") == datetime(2011, 1, 31)
        assert self.parser.parse("2011W05", "W") == datetime(2011, 1, 31)
        assert self.parser.parse("2011-W05-4T14:17:01", "WTHH:mm:ss") == datetime(
            2011, 2, 3, 14, 17, 1
        )
        assert self.parser.parse("2011W054T14:17:01", "WTHH:mm:ss") == datetime(
            2011, 2, 3, 14, 17, 1
        )
        assert self.parser.parse("2011-W05T14:17:01", "WTHH:mm:ss") == datetime(
            2011, 1, 31, 14, 17, 1
        )
        assert self.parser.parse("2011W05T141701", "WTHHmmss") == datetime(
            2011, 1, 31, 14, 17, 1
        )
        assert self.parser.parse("2011W054T141701", "WTHHmmss") == datetime(
            2011, 2, 3, 14, 17, 1
        )

        bad_formats = [
            "201W22",
            "1995-W1-4",
            "2001-W34-90",
            "2001--W34",
            "2011-W03--3",
            "thstrdjtrsrd676776r65",
            "2002-W66-1T14:17:01",
            "2002-W23-03T14:17:01",
        ]

        for fmt in bad_formats:
            with pytest.raises(ParserError):
                self.parser.parse(fmt, "W")

    def test_parse_normalize_whitespace(self):
        assert self.parser.parse(
            "Jun 1 2005  1:33PM", "MMM D YYYY H:mmA", normalize_whitespace=True
        ) == datetime(2005, 6, 1, 13, 33)

        with pytest.raises(ParserError):
            self.parser.parse("Jun 1 2005  1:33PM", "MMM D YYYY H:mmA")

        assert (
            self.parser.parse(
                "\t 2013-05-05  T \n   12:30:45\t123456 \t \n",
                "YYYY-MM-DD T HH:mm:ss S",
                normalize_whitespace=True,
            )
            == datetime(2013, 5, 5, 12, 30, 45, 123456)
        )

        with pytest.raises(ParserError):
            self.parser.parse(
                "\t 2013-05-05  T \n   12:30:45\t123456 \t \n",
                "YYYY-MM-DD T HH:mm:ss S",
            )

        assert self.parser.parse(
            "  \n Jun   1\t 2005\n ", "MMM D YYYY", normalize_whitespace=True
        ) == datetime(2005, 6, 1)

        with pytest.raises(ParserError):
            self.parser.parse("  \n Jun   1\t 2005\n ", "MMM D YYYY")


@pytest.mark.usefixtures("dt_parser_regex")
class TestDateTimeParserRegex:
    def test_format_year(self):

        assert self.format_regex.findall("YYYY-YY") == ["YYYY", "YY"]

    def test_format_month(self):

        assert self.format_regex.findall("MMMM-MMM-MM-M") == ["MMMM", "MMM", "MM", "M"]

    def test_format_day(self):

        assert self.format_regex.findall("DDDD-DDD-DD-D") == ["DDDD", "DDD", "DD", "D"]

    def test_format_hour(self):

        assert self.format_regex.findall("HH-H-hh-h") == ["HH", "H", "hh", "h"]

    def test_format_minute(self):

        assert self.format_regex.findall("mm-m") == ["mm", "m"]

    def test_format_second(self):

        assert self.format_regex.findall("ss-s") == ["ss", "s"]

    def test_format_subsecond(self):

        assert self.format_regex.findall("SSSSSS-SSSSS-SSSS-SSS-SS-S") == [
            "SSSSSS",
            "SSSSS",
            "SSSS",
            "SSS",
            "SS",
            "S",
        ]

    def test_format_tz(self):

        assert self.format_regex.findall("ZZZ-ZZ-Z") == ["ZZZ", "ZZ", "Z"]

    def test_format_am_pm(self):

        assert self.format_regex.findall("A-a") == ["A", "a"]

    def test_format_timestamp(self):

        assert self.format_regex.findall("X") == ["X"]

    def test_format_timestamp_milli(self):

        assert self.format_regex.findall("x") == ["x"]

    def test_escape(self):

        escape_regex = parser.DateTimeParser._ESCAPE_RE

        assert escape_regex.findall("2018-03-09 8 [h] 40 [hello]") == ["[h]", "[hello]"]

    def test_month_names(self):
        p = parser.DateTimeParser("en_us")

        text = "_".join(calendar.month_name[1:])

        result = p._input_re_map["MMMM"].findall(text)

        assert result == calendar.month_name[1:]

    def test_month_abbreviations(self):
        p = parser.DateTimeParser("en_us")

        text = "_".join(calendar.month_abbr[1:])

        result = p._input_re_map["MMM"].findall(text)

        assert result == calendar.month_abbr[1:]

    def test_digits(self):

        assert parser.DateTimeParser._ONE_OR_TWO_DIGIT_RE.findall("4-56") == ["4", "56"]
        assert parser.DateTimeParser._ONE_OR_TWO_OR_THREE_DIGIT_RE.findall(
            "4-56-789"
        ) == ["4", "56", "789"]
        assert parser.DateTimeParser._ONE_OR_MORE_DIGIT_RE.findall(
            "4-56-789-1234-12345"
        ) == ["4", "56", "789", "1234", "12345"]
        assert parser.DateTimeParser._TWO_DIGIT_RE.findall("12-3-45") == ["12", "45"]
        assert parser.DateTimeParser._THREE_DIGIT_RE.findall("123-4-56") == ["123"]
        assert parser.DateTimeParser._FOUR_DIGIT_RE.findall("1234-56") == ["1234"]

    def test_tz(self):
        tz_z_re = parser.DateTimeParser._TZ_Z_RE
        assert tz_z_re.findall("-0700") == [("-", "07", "00")]
        assert tz_z_re.findall("+07") == [("+", "07", "")]
        assert tz_z_re.search("15/01/2019T04:05:06.789120Z") is not None
        assert tz_z_re.search("15/01/2019T04:05:06.789120") is None

        tz_zz_re = parser.DateTimeParser._TZ_ZZ_RE
        assert tz_zz_re.findall("-07:00") == [("-", "07", "00")]
        assert tz_zz_re.findall("+07") == [("+", "07", "")]
        assert tz_zz_re.search("15/01/2019T04:05:06.789120Z") is not None
        assert tz_zz_re.search("15/01/2019T04:05:06.789120") is None

        tz_name_re = parser.DateTimeParser._TZ_NAME_RE
        assert tz_name_re.findall("Europe/Warsaw") == ["Europe/Warsaw"]
        assert tz_name_re.findall("GMT") == ["GMT"]

    def test_timestamp(self):
        timestamp_re = parser.DateTimeParser._TIMESTAMP_RE
        assert timestamp_re.findall("1565707550.452729") == ["1565707550.452729"]
        assert timestamp_re.findall("-1565707550.452729") == ["-1565707550.452729"]
        assert timestamp_re.findall("-1565707550") == ["-1565707550"]
        assert timestamp_re.findall("1565707550") == ["1565707550"]
        assert timestamp_re.findall("1565707550.") == []
        assert timestamp_re.findall(".1565707550") == []

    def test_timestamp_milli(self):
        timestamp_expanded_re = parser.DateTimeParser._TIMESTAMP_EXPANDED_RE
        assert timestamp_expanded_re.findall("-1565707550") == ["-1565707550"]
        assert timestamp_expanded_re.findall("1565707550") == ["1565707550"]
        assert timestamp_expanded_re.findall("1565707550.452729") == []
        assert timestamp_expanded_re.findall("1565707550.") == []
        assert timestamp_expanded_re.findall(".1565707550") == []

    def test_time(self):
        time_re = parser.DateTimeParser._TIME_RE
        time_seperators = [":", ""]

        for sep in time_seperators:
            assert time_re.findall("12") == [("12", "", "", "", "")]
            assert time_re.findall("12{sep}35".format(sep=sep)) == [
                ("12", "35", "", "", "")
            ]
            assert time_re.findall("12{sep}35{sep}46".format(sep=sep)) == [
                ("12", "35", "46", "", "")
            ]
            assert time_re.findall("12{sep}35{sep}46.952313".format(sep=sep)) == [
                ("12", "35", "46", ".", "952313")
            ]
            assert time_re.findall("12{sep}35{sep}46,952313".format(sep=sep)) == [
                ("12", "35", "46", ",", "952313")
            ]

        assert time_re.findall("12:") == []
        assert time_re.findall("12:35:46.") == []
        assert time_re.findall("12:35:46,") == []


@pytest.mark.usefixtures("dt_parser")
class TestDateTimeParserISO:
    def test_YYYY(self):

        assert self.parser.parse_iso("2013") == datetime(2013, 1, 1)

    def test_YYYY_DDDD(self):
        assert self.parser.parse_iso("1998-136") == datetime(1998, 5, 16)

        assert self.parser.parse_iso("1998-006") == datetime(1998, 1, 6)

        with pytest.raises(ParserError):
            self.parser.parse_iso("1998-456")

        # 2016 is a leap year, so Feb 29 exists (leap day)
        assert self.parser.parse_iso("2016-059") == datetime(2016, 2, 28)
        assert self.parser.parse_iso("2016-060") == datetime(2016, 2, 29)
        assert self.parser.parse_iso("2016-061") == datetime(2016, 3, 1)

        # 2017 is not a leap year, so Feb 29 does not exist
        assert self.parser.parse_iso("2017-059") == datetime(2017, 2, 28)
        assert self.parser.parse_iso("2017-060") == datetime(2017, 3, 1)
        assert self.parser.parse_iso("2017-061") == datetime(2017, 3, 2)

        # Since 2016 is a leap year, the 366th day falls in the same year
        assert self.parser.parse_iso("2016-366") == datetime(2016, 12, 31)

        # Since 2017 is not a leap year, the 366th day falls in the next year
        assert self.parser.parse_iso("2017-366") == datetime(2018, 1, 1)

    def test_YYYY_DDDD_HH_mm_ssZ(self):

        assert self.parser.parse_iso("2013-036 04:05:06+01:00") == datetime(
            2013, 2, 5, 4, 5, 6, tzinfo=tz.tzoffset(None, 3600)
        )

        assert self.parser.parse_iso("2013-036 04:05:06Z") == datetime(
            2013, 2, 5, 4, 5, 6, tzinfo=tz.tzutc()
        )

    def test_YYYY_MM_DDDD(self):
        with pytest.raises(ParserError):
            self.parser.parse_iso("2014-05-125")

    def test_YYYY_MM(self):

        for separator in DateTimeParser.SEPARATORS:
            assert self.parser.parse_iso(separator.join(("2013", "02"))) == datetime(
                2013, 2, 1
            )

    def test_YYYY_MM_DD(self):

        for separator in DateTimeParser.SEPARATORS:
            assert self.parser.parse_iso(
                separator.join(("2013", "02", "03"))
            ) == datetime(2013, 2, 3)

    def test_YYYY_MM_DDTHH_mmZ(self):

        assert self.parser.parse_iso("2013-02-03T04:05+01:00") == datetime(
            2013, 2, 3, 4, 5, tzinfo=tz.tzoffset(None, 3600)
        )

    def test_YYYY_MM_DDTHH_mm(self):

        assert self.parser.parse_iso("2013-02-03T04:05") == datetime(2013, 2, 3, 4, 5)

    def test_YYYY_MM_DDTHH(self):

        assert self.parser.parse_iso("2013-02-03T04") == datetime(2013, 2, 3, 4)

    def test_YYYY_MM_DDTHHZ(self):

        assert self.parser.parse_iso("2013-02-03T04+01:00") == datetime(
            2013, 2, 3, 4, tzinfo=tz.tzoffset(None, 3600)
        )

    def test_YYYY_MM_DDTHH_mm_ssZ(self):

        assert self.parser.parse_iso("2013-02-03T04:05:06+01:00") == datetime(
            2013, 2, 3, 4, 5, 6, tzinfo=tz.tzoffset(None, 3600)
        )

    def test_YYYY_MM_DDTHH_mm_ss(self):

        assert self.parser.parse_iso("2013-02-03T04:05:06") == datetime(
            2013, 2, 3, 4, 5, 6
        )

    def test_YYYY_MM_DD_HH_mmZ(self):

        assert self.parser.parse_iso("2013-02-03 04:05+01:00") == datetime(
            2013, 2, 3, 4, 5, tzinfo=tz.tzoffset(None, 3600)
        )

    def test_YYYY_MM_DD_HH_mm(self):

        assert self.parser.parse_iso("2013-02-03 04:05") == datetime(2013, 2, 3, 4, 5)

    def test_YYYY_MM_DD_HH(self):

        assert self.parser.parse_iso("2013-02-03 04") == datetime(2013, 2, 3, 4)

    def test_invalid_time(self):

        with pytest.raises(ParserError):
            self.parser.parse_iso("2013-02-03T")

        with pytest.raises(ParserError):
            self.parser.parse_iso("2013-02-03 044")

        with pytest.raises(ParserError):
            self.parser.parse_iso("2013-02-03 04:05:06.")

    def test_YYYY_MM_DD_HH_mm_ssZ(self):

        assert self.parser.parse_iso("2013-02-03 04:05:06+01:00") == datetime(
            2013, 2, 3, 4, 5, 6, tzinfo=tz.tzoffset(None, 3600)
        )

    def test_YYYY_MM_DD_HH_mm_ss(self):

        assert self.parser.parse_iso("2013-02-03 04:05:06") == datetime(
            2013, 2, 3, 4, 5, 6
        )

    def test_YYYY_MM_DDTHH_mm_ss_S(self):

        assert self.parser.parse_iso("2013-02-03T04:05:06.7") == datetime(
            2013, 2, 3, 4, 5, 6, 700000
        )

        assert self.parser.parse_iso("2013-02-03T04:05:06.78") == datetime(
            2013, 2, 3, 4, 5, 6, 780000
        )

        assert self.parser.parse_iso("2013-02-03T04:05:06.789") == datetime(
            2013, 2, 3, 4, 5, 6, 789000
        )

        assert self.parser.parse_iso("2013-02-03T04:05:06.7891") == datetime(
            2013, 2, 3, 4, 5, 6, 789100
        )

        assert self.parser.parse_iso("2013-02-03T04:05:06.78912") == datetime(
            2013, 2, 3, 4, 5, 6, 789120
        )

        # ISO 8601:2004(E), ISO, 2004-12-01, 4.2.2.4 ... the decimal fraction
        # shall be divided from the integer part by the decimal sign specified
        # in ISO 31-0, i.e. the comma [,] or full stop [.]. Of these, the comma
        # is the preferred sign.
        assert self.parser.parse_iso("2013-02-03T04:05:06,789123678") == datetime(
            2013, 2, 3, 4, 5, 6, 789124
        )

        # there is no limit on the number of decimal places
        assert self.parser.parse_iso("2013-02-03T04:05:06.789123678") == datetime(
            2013, 2, 3, 4, 5, 6, 789124
        )

    def test_YYYY_MM_DDTHH_mm_ss_SZ(self):

        assert self.parser.parse_iso("2013-02-03T04:05:06.7+01:00") == datetime(
            2013, 2, 3, 4, 5, 6, 700000, tzinfo=tz.tzoffset(None, 3600)
        )

        assert self.parser.parse_iso("2013-02-03T04:05:06.78+01:00") == datetime(
            2013, 2, 3, 4, 5, 6, 780000, tzinfo=tz.tzoffset(None, 3600)
        )

        assert self.parser.parse_iso("2013-02-03T04:05:06.789+01:00") == datetime(
            2013, 2, 3, 4, 5, 6, 789000, tzinfo=tz.tzoffset(None, 3600)
        )

        assert self.parser.parse_iso("2013-02-03T04:05:06.7891+01:00") == datetime(
            2013, 2, 3, 4, 5, 6, 789100, tzinfo=tz.tzoffset(None, 3600)
        )

        assert self.parser.parse_iso("2013-02-03T04:05:06.78912+01:00") == datetime(
            2013, 2, 3, 4, 5, 6, 789120, tzinfo=tz.tzoffset(None, 3600)
        )

        assert self.parser.parse_iso("2013-02-03 04:05:06.78912Z") == datetime(
            2013, 2, 3, 4, 5, 6, 789120, tzinfo=tz.tzutc()
        )

    def test_W(self):

        assert self.parser.parse_iso("2011-W05-4") == datetime(2011, 2, 3)

        assert self.parser.parse_iso("2011-W05-4T14:17:01") == datetime(
            2011, 2, 3, 14, 17, 1
        )

        assert self.parser.parse_iso("2011W054") == datetime(2011, 2, 3)

        assert self.parser.parse_iso("2011W054T141701") == datetime(
            2011, 2, 3, 14, 17, 1
        )

    def test_invalid_Z(self):

        with pytest.raises(ParserError):
            self.parser.parse_iso("2013-02-03T04:05:06.78912z")

        with pytest.raises(ParserError):
            self.parser.parse_iso("2013-02-03T04:05:06.78912zz")

        with pytest.raises(ParserError):
            self.parser.parse_iso("2013-02-03T04:05:06.78912Zz")

        with pytest.raises(ParserError):
            self.parser.parse_iso("2013-02-03T04:05:06.78912ZZ")

        with pytest.raises(ParserError):
            self.parser.parse_iso("2013-02-03T04:05:06.78912+Z")

        with pytest.raises(ParserError):
            self.parser.parse_iso("2013-02-03T04:05:06.78912-Z")

        with pytest.raises(ParserError):
            self.parser.parse_iso("2013-02-03T04:05:06.78912 Z")

    def test_parse_subsecond(self):
        self.expected = datetime(2013, 1, 1, 12, 30, 45, 900000)
        assert self.parser.parse_iso("2013-01-01 12:30:45.9") == self.expected

        self.expected = datetime(2013, 1, 1, 12, 30, 45, 980000)
        assert self.parser.parse_iso("2013-01-01 12:30:45.98") == self.expected

        self.expected = datetime(2013, 1, 1, 12, 30, 45, 987000)
        assert self.parser.parse_iso("2013-01-01 12:30:45.987") == self.expected

        self.expected = datetime(2013, 1, 1, 12, 30, 45, 987600)
        assert self.parser.parse_iso("2013-01-01 12:30:45.9876") == self.expected

        self.expected = datetime(2013, 1, 1, 12, 30, 45, 987650)
        assert self.parser.parse_iso("2013-01-01 12:30:45.98765") == self.expected

        self.expected = datetime(2013, 1, 1, 12, 30, 45, 987654)
        assert self.parser.parse_iso("2013-01-01 12:30:45.987654") == self.expected

        # use comma as subsecond separator
        self.expected = datetime(2013, 1, 1, 12, 30, 45, 987654)
        assert self.parser.parse_iso("2013-01-01 12:30:45,987654") == self.expected

    def test_gnu_date(self):
        """Regression tests for parsing output from GNU date."""
        # date -Ins
        assert self.parser.parse_iso("2016-11-16T09:46:30,895636557-0800") == datetime(
            2016, 11, 16, 9, 46, 30, 895636, tzinfo=tz.tzoffset(None, -3600 * 8)
        )

        # date --rfc-3339=ns
        assert self.parser.parse_iso("2016-11-16 09:51:14.682141526-08:00") == datetime(
            2016, 11, 16, 9, 51, 14, 682142, tzinfo=tz.tzoffset(None, -3600 * 8)
        )

    def test_isoformat(self):

        dt = datetime.utcnow()

        assert self.parser.parse_iso(dt.isoformat()) == dt

    def test_parse_iso_normalize_whitespace(self):
        assert self.parser.parse_iso(
            "2013-036 \t  04:05:06Z", normalize_whitespace=True
        ) == datetime(2013, 2, 5, 4, 5, 6, tzinfo=tz.tzutc())

        with pytest.raises(ParserError):
            self.parser.parse_iso("2013-036 \t  04:05:06Z")

        assert self.parser.parse_iso(
            "\t 2013-05-05T12:30:45.123456 \t \n", normalize_whitespace=True
        ) == datetime(2013, 5, 5, 12, 30, 45, 123456)

        with pytest.raises(ParserError):
            self.parser.parse_iso("\t 2013-05-05T12:30:45.123456 \t \n")

    def test_parse_iso_with_leading_and_trailing_whitespace(self):
        datetime_string = "    2016-11-15T06:37:19.123456"
        with pytest.raises(ParserError):
            self.parser.parse_iso(datetime_string)

        datetime_string = "    2016-11-15T06:37:19.123456     "
        with pytest.raises(ParserError):
            self.parser.parse_iso(datetime_string)

        datetime_string = "2016-11-15T06:37:19.123456 "
        with pytest.raises(ParserError):
            self.parser.parse_iso(datetime_string)

        datetime_string = "2016-11-15T 06:37:19.123456"
        with pytest.raises(ParserError):
            self.parser.parse_iso(datetime_string)

        # leading whitespace
        datetime_string = "    2016-11-15 06:37:19.123456"
        with pytest.raises(ParserError):
            self.parser.parse_iso(datetime_string)

        # trailing whitespace
        datetime_string = "2016-11-15 06:37:19.123456    "
        with pytest.raises(ParserError):
            self.parser.parse_iso(datetime_string)

        datetime_string = "    2016-11-15 06:37:19.123456    "
        with pytest.raises(ParserError):
            self.parser.parse_iso(datetime_string)

        # two dividing spaces
        datetime_string = "2016-11-15  06:37:19.123456"
        with pytest.raises(ParserError):
            self.parser.parse_iso(datetime_string)

    def test_parse_iso_with_extra_words_at_start_and_end_invalid(self):
        test_inputs = [
            "blah2016",
            "blah2016blah",
            "blah 2016 blah",
            "blah 2016",
            "2016 blah",
            "blah 2016-05-16 04:05:06.789120",
            "2016-05-16 04:05:06.789120 blah",
            "blah 2016-05-16T04:05:06.789120",
            "2016-05-16T04:05:06.789120 blah",
            "2016blah",
            "2016-05blah",
            "2016-05-16blah",
            "2016-05-16T04:05:06.789120blah",
            "2016-05-16T04:05:06.789120ZblahZ",
            "2016-05-16T04:05:06.789120Zblah",
            "2016-05-16T04:05:06.789120blahZ",
            "Meet me at 2016-05-16T04:05:06.789120 at the restaurant.",
            "Meet me at 2016-05-16 04:05:06.789120 at the restaurant.",
        ]

        for ti in test_inputs:
            with pytest.raises(ParserError):
                self.parser.parse_iso(ti)

    def test_iso8601_basic_format(self):
        assert self.parser.parse_iso("20180517") == datetime(2018, 5, 17)

        assert self.parser.parse_iso("20180517T10") == datetime(2018, 5, 17, 10)

        assert self.parser.parse_iso("20180517T105513.843456") == datetime(
            2018, 5, 17, 10, 55, 13, 843456
        )

        assert self.parser.parse_iso("20180517T105513Z") == datetime(
            2018, 5, 17, 10, 55, 13, tzinfo=tz.tzutc()
        )

        assert self.parser.parse_iso("20180517T105513.843456-0700") == datetime(
            2018, 5, 17, 10, 55, 13, 843456, tzinfo=tz.tzoffset(None, -25200)
        )

        assert self.parser.parse_iso("20180517T105513-0700") == datetime(
            2018, 5, 17, 10, 55, 13, tzinfo=tz.tzoffset(None, -25200)
        )

        assert self.parser.parse_iso("20180517T105513-07") == datetime(
            2018, 5, 17, 10, 55, 13, tzinfo=tz.tzoffset(None, -25200)
        )

        # ordinal in basic format: YYYYDDDD
        assert self.parser.parse_iso("1998136") == datetime(1998, 5, 16)

        # timezone requires +- seperator
        with pytest.raises(ParserError):
            self.parser.parse_iso("20180517T1055130700")

        with pytest.raises(ParserError):
            self.parser.parse_iso("20180517T10551307")

        # too many digits in date
        with pytest.raises(ParserError):
            self.parser.parse_iso("201860517T105513Z")

        # too many digits in time
        with pytest.raises(ParserError):
            self.parser.parse_iso("20180517T1055213Z")

    def test_midnight_end_day(self):
        assert self.parser.parse_iso("2019-10-30T24:00:00") == datetime(
            2019, 10, 31, 0, 0, 0, 0
        )
        assert self.parser.parse_iso("2019-10-30T24:00") == datetime(
            2019, 10, 31, 0, 0, 0, 0
        )
        assert self.parser.parse_iso("2019-10-30T24:00:00.0") == datetime(
            2019, 10, 31, 0, 0, 0, 0
        )
        assert self.parser.parse_iso("2019-10-31T24:00:00") == datetime(
            2019, 11, 1, 0, 0, 0, 0
        )
        assert self.parser.parse_iso("2019-12-31T24:00:00") == datetime(
            2020, 1, 1, 0, 0, 0, 0
        )
        assert self.parser.parse_iso("2019-12-31T23:59:59.9999999") == datetime(
            2020, 1, 1, 0, 0, 0, 0
        )

        with pytest.raises(ParserError):
            self.parser.parse_iso("2019-12-31T24:01:00")

        with pytest.raises(ParserError):
            self.parser.parse_iso("2019-12-31T24:00:01")

        with pytest.raises(ParserError):
            self.parser.parse_iso("2019-12-31T24:00:00.1")

        with pytest.raises(ParserError):
            self.parser.parse_iso("2019-12-31T24:00:00.999999")


@pytest.mark.usefixtures("tzinfo_parser")
class TestTzinfoParser:
    def test_parse_local(self):

        assert self.parser.parse("local") == tz.tzlocal()

    def test_parse_utc(self):

        assert self.parser.parse("utc") == tz.tzutc()
        assert self.parser.parse("UTC") == tz.tzutc()

    def test_parse_iso(self):

        assert self.parser.parse("01:00") == tz.tzoffset(None, 3600)
        assert self.parser.parse("11:35") == tz.tzoffset(None, 11 * 3600 + 2100)
        assert self.parser.parse("+01:00") == tz.tzoffset(None, 3600)
        assert self.parser.parse("-01:00") == tz.tzoffset(None, -3600)

        assert self.parser.parse("0100") == tz.tzoffset(None, 3600)
        assert self.parser.parse("+0100") == tz.tzoffset(None, 3600)
        assert self.parser.parse("-0100") == tz.tzoffset(None, -3600)

        assert self.parser.parse("01") == tz.tzoffset(None, 3600)
        assert self.parser.parse("+01") == tz.tzoffset(None, 3600)
        assert self.parser.parse("-01") == tz.tzoffset(None, -3600)

    def test_parse_str(self):

        assert self.parser.parse("US/Pacific") == tz.gettz("US/Pacific")

    def test_parse_fails(self):

        with pytest.raises(parser.ParserError):
            self.parser.parse("fail")


@pytest.mark.usefixtures("dt_parser")
class TestDateTimeParserMonthName:
    def test_shortmonth_capitalized(self):

        assert self.parser.parse("2013-Jan-01", "YYYY-MMM-DD") == datetime(2013, 1, 1)

    def test_shortmonth_allupper(self):

        assert self.parser.parse("2013-JAN-01", "YYYY-MMM-DD") == datetime(2013, 1, 1)

    def test_shortmonth_alllower(self):

        assert self.parser.parse("2013-jan-01", "YYYY-MMM-DD") == datetime(2013, 1, 1)

    def test_month_capitalized(self):

        assert self.parser.parse("2013-January-01", "YYYY-MMMM-DD") == datetime(
            2013, 1, 1
        )

    def test_month_allupper(self):

        assert self.parser.parse("2013-JANUARY-01", "YYYY-MMMM-DD") == datetime(
            2013, 1, 1
        )

    def test_month_alllower(self):

        assert self.parser.parse("2013-january-01", "YYYY-MMMM-DD") == datetime(
            2013, 1, 1
        )

    def test_localized_month_name(self):
        parser_ = parser.DateTimeParser("fr_fr")

        assert parser_.parse("2013-Janvier-01", "YYYY-MMMM-DD") == datetime(2013, 1, 1)

    def test_localized_month_abbreviation(self):
        parser_ = parser.DateTimeParser("it_it")

        assert parser_.parse("2013-Gen-01", "YYYY-MMM-DD") == datetime(2013, 1, 1)


@pytest.mark.usefixtures("dt_parser")
class TestDateTimeParserMeridians:
    def test_meridians_lowercase(self):
        assert self.parser.parse("2013-01-01 5am", "YYYY-MM-DD ha") == datetime(
            2013, 1, 1, 5
        )

        assert self.parser.parse("2013-01-01 5pm", "YYYY-MM-DD ha") == datetime(
            2013, 1, 1, 17
        )

    def test_meridians_capitalized(self):
        assert self.parser.parse("2013-01-01 5AM", "YYYY-MM-DD hA") == datetime(
            2013, 1, 1, 5
        )

        assert self.parser.parse("2013-01-01 5PM", "YYYY-MM-DD hA") == datetime(
            2013, 1, 1, 17
        )

    def test_localized_meridians_lowercase(self):
        parser_ = parser.DateTimeParser("hu_hu")
        assert parser_.parse("2013-01-01 5 de", "YYYY-MM-DD h a") == datetime(
            2013, 1, 1, 5
        )

        assert parser_.parse("2013-01-01 5 du", "YYYY-MM-DD h a") == datetime(
            2013, 1, 1, 17
        )

    def test_localized_meridians_capitalized(self):
        parser_ = parser.DateTimeParser("hu_hu")
        assert parser_.parse("2013-01-01 5 DE", "YYYY-MM-DD h A") == datetime(
            2013, 1, 1, 5
        )

        assert parser_.parse("2013-01-01 5 DU", "YYYY-MM-DD h A") == datetime(
            2013, 1, 1, 17
        )

    # regression test for issue #607
    def test_es_meridians(self):
        parser_ = parser.DateTimeParser("es")

        assert parser_.parse(
            "Junio 30, 2019 - 08:00 pm", "MMMM DD, YYYY - hh:mm a"
        ) == datetime(2019, 6, 30, 20, 0)

        with pytest.raises(ParserError):
            parser_.parse(
                "Junio 30, 2019 - 08:00 pasdfasdfm", "MMMM DD, YYYY - hh:mm a"
            )

    def test_fr_meridians(self):
        parser_ = parser.DateTimeParser("fr")

        # the French locale always uses a 24 hour clock, so it does not support meridians
        with pytest.raises(ParserError):
            parser_.parse("Janvier 30, 2019 - 08:00 pm", "MMMM DD, YYYY - hh:mm a")


@pytest.mark.usefixtures("dt_parser")
class TestDateTimeParserMonthOrdinalDay:
    def test_english(self):
        parser_ = parser.DateTimeParser("en_us")

        assert parser_.parse("January 1st, 2013", "MMMM Do, YYYY") == datetime(
            2013, 1, 1
        )
        assert parser_.parse("January 2nd, 2013", "MMMM Do, YYYY") == datetime(
            2013, 1, 2
        )
        assert parser_.parse("January 3rd, 2013", "MMMM Do, YYYY") == datetime(
            2013, 1, 3
        )
        assert parser_.parse("January 4th, 2013", "MMMM Do, YYYY") == datetime(
            2013, 1, 4
        )
        assert parser_.parse("January 11th, 2013", "MMMM Do, YYYY") == datetime(
            2013, 1, 11
        )
        assert parser_.parse("January 12th, 2013", "MMMM Do, YYYY") == datetime(
            2013, 1, 12
        )
        assert parser_.parse("January 13th, 2013", "MMMM Do, YYYY") == datetime(
            2013, 1, 13
        )
        assert parser_.parse("January 21st, 2013", "MMMM Do, YYYY") == datetime(
            2013, 1, 21
        )
        assert parser_.parse("January 31st, 2013", "MMMM Do, YYYY") == datetime(
            2013, 1, 31
        )

        with pytest.raises(ParserError):
            parser_.parse("January 1th, 2013", "MMMM Do, YYYY")

        with pytest.raises(ParserError):
            parser_.parse("January 11st, 2013", "MMMM Do, YYYY")

    def test_italian(self):
        parser_ = parser.DateTimeParser("it_it")

        assert parser_.parse("Gennaio 1º, 2013", "MMMM Do, YYYY") == datetime(
            2013, 1, 1
        )

    def test_spanish(self):
        parser_ = parser.DateTimeParser("es_es")

        assert parser_.parse("Enero 1º, 2013", "MMMM Do, YYYY") == datetime(2013, 1, 1)

    def test_french(self):
        parser_ = parser.DateTimeParser("fr_fr")

        assert parser_.parse("Janvier 1er, 2013", "MMMM Do, YYYY") == datetime(
            2013, 1, 1
        )

        assert parser_.parse("Janvier 2e, 2013", "MMMM Do, YYYY") == datetime(
            2013, 1, 2
        )

        assert parser_.parse("Janvier 11e, 2013", "MMMM Do, YYYY") == datetime(
            2013, 1, 11
        )


@pytest.mark.usefixtures("dt_parser")
class TestDateTimeParserSearchDate:
    def test_parse_search(self):

        assert self.parser.parse(
            "Today is 25 of September of 2003", "DD of MMMM of YYYY"
        ) == datetime(2003, 9, 25)

    def test_parse_search_with_numbers(self):

        assert self.parser.parse(
            "2000 people met the 2012-01-01 12:05:10", "YYYY-MM-DD HH:mm:ss"
        ) == datetime(2012, 1, 1, 12, 5, 10)

        assert self.parser.parse(
            "Call 01-02-03 on 79-01-01 12:05:10", "YY-MM-DD HH:mm:ss"
        ) == datetime(1979, 1, 1, 12, 5, 10)

    def test_parse_search_with_names(self):

        assert self.parser.parse("June was born in May 1980", "MMMM YYYY") == datetime(
            1980, 5, 1
        )

    def test_parse_search_locale_with_names(self):
        p = parser.DateTimeParser("sv_se")

        assert p.parse("Jan föddes den 31 Dec 1980", "DD MMM YYYY") == datetime(
            1980, 12, 31
        )

        assert p.parse("Jag föddes den 25 Augusti 1975", "DD MMMM YYYY") == datetime(
            1975, 8, 25
        )

    def test_parse_search_fails(self):

        with pytest.raises(parser.ParserError):
            self.parser.parse("Jag föddes den 25 Augusti 1975", "DD MMMM YYYY")

    def test_escape(self):

        format = "MMMM D, YYYY [at] h:mma"
        assert self.parser.parse(
            "Thursday, December 10, 2015 at 5:09pm", format
        ) == datetime(2015, 12, 10, 17, 9)

        format = "[MMMM] M D, YYYY [at] h:mma"
        assert self.parser.parse("MMMM 12 10, 2015 at 5:09pm", format) == datetime(
            2015, 12, 10, 17, 9
        )

        format = "[It happened on] MMMM Do [in the year] YYYY [a long time ago]"
        assert self.parser.parse(
            "It happened on November 25th in the year 1990 a long time ago", format
        ) == datetime(1990, 11, 25)

        format = "[It happened on] MMMM Do [in the][ year] YYYY [a long time ago]"
        assert self.parser.parse(
            "It happened on November 25th in the year 1990 a long time ago", format
        ) == datetime(1990, 11, 25)

        format = "[I'm][ entirely][ escaped,][ weee!]"
        assert self.parser.parse("I'm entirely escaped, weee!", format) == datetime(
            1, 1, 1
        )

        # Special RegEx characters
        format = "MMM DD, YYYY |^${}().*+?<>-& h:mm A"
        assert self.parser.parse(
            "Dec 31, 2017 |^${}().*+?<>-& 2:00 AM", format
        ) == datetime(2017, 12, 31, 2, 0)
