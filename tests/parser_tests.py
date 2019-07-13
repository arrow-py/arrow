# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import calendar
import time
from datetime import datetime

from chai import Chai
from dateutil import tz

from arrow import parser
from arrow.parser import DateTimeParser, ParserError


class DateTimeParserTests(Chai):
    def setUp(self):
        super(DateTimeParserTests, self).setUp()

        self.parser = parser.DateTimeParser()

    def test_parse_multiformat(self):

        mock_datetime = self.mock()

        self.expect(self.parser.parse).args("str", "fmt_a").raises(ParserError)
        self.expect(self.parser.parse).args("str", "fmt_b").returns(mock_datetime)

        result = self.parser._parse_multiformat("str", ["fmt_a", "fmt_b"])

        self.assertEqual(result, mock_datetime)

    def test_parse_multiformat_all_fail(self):

        self.expect(self.parser.parse).args("str", "fmt_a").raises(ParserError)
        self.expect(self.parser.parse).args("str", "fmt_b").raises(ParserError)

        with self.assertRaises(ParserError):
            self.parser._parse_multiformat("str", ["fmt_a", "fmt_b"])

    def test_parse_multiformat_unself_expected_fail(self):
        class UnselfExpectedError(Exception):
            pass

        self.expect(self.parser.parse).args("str", "fmt_a").raises(UnselfExpectedError)

        with self.assertRaises(UnselfExpectedError):
            self.parser._parse_multiformat("str", ["fmt_a", "fmt_b"])

    def test_parse_token_nonsense(self):
        parts = {}
        self.parser._parse_token("NONSENSE", "1900", parts)
        self.assertEqual(parts, {})

    def test_parse_token_invalid_meridians(self):
        parts = {}
        self.parser._parse_token("A", "a..m", parts)
        self.assertEqual(parts, {})
        self.parser._parse_token("a", "p..m", parts)
        self.assertEqual(parts, {})

    def test_parser_no_caching(self):

        self.expect(parser.DateTimeParser, "_generate_pattern_re").args("fmt_a").times(
            100
        )
        self.parser = parser.DateTimeParser(cache_size=0)
        for _ in range(100):
            self.parser._generate_pattern_re("fmt_a")

    def test_parser_1_line_caching(self):

        self.expect(parser.DateTimeParser, "_generate_pattern_re").args("fmt_a").times(
            1
        )
        self.parser = parser.DateTimeParser(cache_size=1)
        for _ in range(100):
            self.parser._generate_pattern_re("fmt_a")

        self.expect(parser.DateTimeParser, "_generate_pattern_re").args("fmt_b").times(
            1
        )
        for _ in range(100):
            self.parser._generate_pattern_re("fmt_a")
        self.parser._generate_pattern_re("fmt_b")

        self.expect(parser.DateTimeParser, "_generate_pattern_re").args("fmt_a").times(
            1
        )
        for _ in range(100):
            self.parser._generate_pattern_re("fmt_a")

    def test_parser_multiple_line_caching(self):

        self.expect(parser.DateTimeParser, "_generate_pattern_re").args("fmt_a").times(
            1
        )
        self.parser = parser.DateTimeParser(cache_size=2)
        for _ in range(100):
            self.parser._generate_pattern_re("fmt_a")

        self.expect(parser.DateTimeParser, "_generate_pattern_re").args("fmt_b").times(
            1
        )
        for _ in range(100):
            self.parser._generate_pattern_re("fmt_a")
        self.parser._generate_pattern_re("fmt_b")

        self.expect(parser.DateTimeParser, "_generate_pattern_re").args("fmt_a").times(
            0
        )
        for _ in range(100):
            self.parser._generate_pattern_re("fmt_a")


class DateTimeParserParseTests(Chai):
    def setUp(self):
        super(DateTimeParserParseTests, self).setUp()

        self.parser = parser.DateTimeParser()

    def test_parse_list(self):

        self.expect(self.parser._parse_multiformat).args(
            "str", ["fmt_a", "fmt_b"]
        ).returns("result")

        result = self.parser.parse("str", ["fmt_a", "fmt_b"])

        self.assertEqual(result, "result")

    def test_parse_unrecognized_token(self):

        mock_input_re_map = self.mock(self.parser, "_input_re_map")

        self.expect(mock_input_re_map.__getitem__).args("YYYY").raises(KeyError)

        with self.assertRaises(parser.ParserError):
            self.parser.parse("2013-01-01", "YYYY-MM-DD")

    def test_parse_parse_no_match(self):

        with self.assertRaises(parser.ParserError):
            self.parser.parse("01-01", "YYYY-MM-DD")

    def test_parse_separators(self):

        with self.assertRaises(parser.ParserError):
            self.parser.parse("1403549231", "YYYY-MM-DD")

    def test_parse_numbers(self):

        self.expected = datetime(2012, 1, 1, 12, 5, 10)
        self.assertEqual(
            self.parser.parse("2012-01-01 12:05:10", "YYYY-MM-DD HH:mm:ss"),
            self.expected,
        )

    def test_parse_year_two_digit(self):

        self.expected = datetime(1979, 1, 1, 12, 5, 10)
        self.assertEqual(
            self.parser.parse("79-01-01 12:05:10", "YY-MM-DD HH:mm:ss"), self.expected
        )

    def test_parse_timestamp(self):

        tz_utc = tz.tzutc()
        timestamp = int(time.time())
        self.expected = datetime.fromtimestamp(timestamp, tz=tz_utc)
        self.assertEqual(self.parser.parse(str(timestamp), "X"), self.expected)

    def test_parse_names(self):

        self.expected = datetime(2012, 1, 1)

        self.assertEqual(
            self.parser.parse("January 1, 2012", "MMMM D, YYYY"), self.expected
        )
        self.assertEqual(self.parser.parse("Jan 1, 2012", "MMM D, YYYY"), self.expected)

    def test_parse_pm(self):

        self.expected = datetime(1, 1, 1, 13, 0, 0)
        self.assertEqual(self.parser.parse("1 pm", "H a"), self.expected)
        self.assertEqual(self.parser.parse("1 pm", "h a"), self.expected)

        self.expected = datetime(1, 1, 1, 1, 0, 0)
        self.assertEqual(self.parser.parse("1 am", "H A"), self.expected)
        self.assertEqual(self.parser.parse("1 am", "h A"), self.expected)

        self.expected = datetime(1, 1, 1, 0, 0, 0)
        self.assertEqual(self.parser.parse("12 am", "H A"), self.expected)
        self.assertEqual(self.parser.parse("12 am", "h A"), self.expected)

        self.expected = datetime(1, 1, 1, 12, 0, 0)
        self.assertEqual(self.parser.parse("12 pm", "H A"), self.expected)
        self.assertEqual(self.parser.parse("12 pm", "h A"), self.expected)

    def test_parse_tz_hours_only(self):
        self.expected = datetime(2025, 10, 17, 5, 30, 10, tzinfo=tz.tzoffset(None, 0))
        parsed = self.parser.parse("2025-10-17 05:30:10+00", "YYYY-MM-DD HH:mm:ssZ")
        self.assertEqual(parsed, self.expected)

    def test_parse_tz_zz(self):

        self.expected = datetime(2013, 1, 1, tzinfo=tz.tzoffset(None, -7 * 3600))
        self.assertEqual(
            self.parser.parse("2013-01-01 -07:00", "YYYY-MM-DD ZZ"), self.expected
        )

    def test_parse_tz_name_zzz(self):
        for tz_name in (
            # best solution would be to test on every available tz name from
            # the tz database but it is actualy tricky to retrieve them from
            # dateutil so here is short list that should match all
            # naming patterns/conventions in used tz databaze
            "Africa/Tripoli",
            "America/Port_of_Spain",
            "Australia/LHI",
            "Etc/GMT-11",
            "Etc/GMT0",
            "Etc/UCT",
            "Etc/GMT+9",
            "GMT+0",
            "CST6CDT",
            "GMT-0",
            "W-SU",
        ):
            self.expected = datetime(2013, 1, 1, tzinfo=tz.gettz(tz_name))
            self.assertEqual(
                self.parser.parse("2013-01-01 %s" % tz_name, "YYYY-MM-DD ZZZ"),
                self.expected,
            )

        # note that offsets are not timezones
        with self.assertRaises(ParserError):
            self.parser.parse("2013-01-01 +1000", "YYYY-MM-DD ZZZ")

    def test_parse_subsecond(self):

        self.expected = datetime(2013, 1, 1, 12, 30, 45, 900000)
        self.assertEqual(
            self.parser.parse("2013-01-01 12:30:45.9", "YYYY-MM-DD HH:mm:ss.S"),
            self.expected,
        )
        self.assertEqual(self.parser.parse_iso("2013-01-01 12:30:45.9"), self.expected)

        self.expected = datetime(2013, 1, 1, 12, 30, 45, 980000)
        self.assertEqual(
            self.parser.parse("2013-01-01 12:30:45.98", "YYYY-MM-DD HH:mm:ss.SS"),
            self.expected,
        )
        self.assertEqual(self.parser.parse_iso("2013-01-01 12:30:45.98"), self.expected)

        self.expected = datetime(2013, 1, 1, 12, 30, 45, 987000)
        self.assertEqual(
            self.parser.parse("2013-01-01 12:30:45.987", "YYYY-MM-DD HH:mm:ss.SSS"),
            self.expected,
        )
        self.assertEqual(
            self.parser.parse_iso("2013-01-01 12:30:45.987"), self.expected
        )

        self.expected = datetime(2013, 1, 1, 12, 30, 45, 987600)
        self.assertEqual(
            self.parser.parse("2013-01-01 12:30:45.9876", "YYYY-MM-DD HH:mm:ss.SSSS"),
            self.expected,
        )
        self.assertEqual(
            self.parser.parse_iso("2013-01-01 12:30:45.9876"), self.expected
        )

        self.expected = datetime(2013, 1, 1, 12, 30, 45, 987650)
        self.assertEqual(
            self.parser.parse("2013-01-01 12:30:45.98765", "YYYY-MM-DD HH:mm:ss.SSSSS"),
            self.expected,
        )
        self.assertEqual(
            self.parser.parse_iso("2013-01-01 12:30:45.98765"), self.expected
        )

        self.expected = datetime(2013, 1, 1, 12, 30, 45, 987654)
        self.assertEqual(
            self.parser.parse(
                "2013-01-01 12:30:45.987654", "YYYY-MM-DD HH:mm:ss.SSSSSS"
            ),
            self.expected,
        )
        self.assertEqual(
            self.parser.parse_iso("2013-01-01 12:30:45.987654"), self.expected
        )

    def test_parse_subsecond_rounding(self):
        self.expected = datetime(2013, 1, 1, 12, 30, 45, 987654)
        format = "YYYY-MM-DD HH:mm:ss.S"

        # round up
        string = "2013-01-01 12:30:45.9876539"
        self.assertEqual(self.parser.parse(string, format), self.expected)
        self.assertEqual(self.parser.parse_iso(string), self.expected)

        # round down
        string = "2013-01-01 12:30:45.98765432"
        self.assertEqual(self.parser.parse(string, format), self.expected)
        # import pudb; pudb.set_trace()
        self.assertEqual(self.parser.parse_iso(string), self.expected)

        # round half-up
        string = "2013-01-01 12:30:45.987653521"
        self.assertEqual(self.parser.parse(string, format), self.expected)
        self.assertEqual(self.parser.parse_iso(string), self.expected)

        # round half-down
        string = "2013-01-01 12:30:45.9876545210"
        self.assertEqual(self.parser.parse(string, format), self.expected)
        self.assertEqual(self.parser.parse_iso(string), self.expected)

    def test_map_lookup_keyerror(self):

        with self.assertRaises(parser.ParserError):
            parser.DateTimeParser._map_lookup({"a": "1"}, "b")

    def test_try_timestamp(self):

        self.assertEqual(parser.DateTimeParser._try_timestamp("1.1"), 1.1)
        self.assertEqual(parser.DateTimeParser._try_timestamp("1"), 1)
        self.assertEqual(parser.DateTimeParser._try_timestamp("abc"), None)


class DateTimeParserRegexTests(Chai):
    def setUp(self):
        super(DateTimeParserRegexTests, self).setUp()

        self.format_regex = parser.DateTimeParser._FORMAT_RE

    def test_format_year(self):

        self.assertEqual(self.format_regex.findall("YYYY-YY"), ["YYYY", "YY"])

    def test_format_month(self):

        self.assertEqual(
            self.format_regex.findall("MMMM-MMM-MM-M"), ["MMMM", "MMM", "MM", "M"]
        )

    def test_format_day(self):

        self.assertEqual(
            self.format_regex.findall("DDDD-DDD-DD-D"), ["DDDD", "DDD", "DD", "D"]
        )

    def test_format_hour(self):

        self.assertEqual(self.format_regex.findall("HH-H-hh-h"), ["HH", "H", "hh", "h"])

    def test_format_minute(self):

        self.assertEqual(self.format_regex.findall("mm-m"), ["mm", "m"])

    def test_format_second(self):

        self.assertEqual(self.format_regex.findall("ss-s"), ["ss", "s"])

    def test_format_subsecond(self):

        self.assertEqual(
            self.format_regex.findall("SSSSSS-SSSSS-SSSS-SSS-SS-S"),
            ["SSSSSS", "SSSSS", "SSSS", "SSS", "SS", "S"],
        )

    def test_format_tz(self):

        self.assertEqual(self.format_regex.findall("ZZ-Z"), ["ZZ", "Z"])

    def test_format_am_pm(self):

        self.assertEqual(self.format_regex.findall("A-a"), ["A", "a"])

    def test_format_timestamp(self):

        self.assertEqual(self.format_regex.findall("X"), ["X"])

    def test_month_names(self):
        p = parser.DateTimeParser("en_us")

        text = "_".join(calendar.month_name[1:])

        result = p._input_re_map["MMMM"].findall(text)

        self.assertEqual(result, calendar.month_name[1:])

    def test_month_abbreviations(self):
        p = parser.DateTimeParser("en_us")

        text = "_".join(calendar.month_abbr[1:])

        result = p._input_re_map["MMM"].findall(text)

        self.assertEqual(result, calendar.month_abbr[1:])

    def test_digits(self):

        self.assertEqual(
            parser.DateTimeParser._TWO_DIGIT_RE.findall("12-3-45"), ["12", "45"]
        )
        self.assertEqual(
            parser.DateTimeParser._FOUR_DIGIT_RE.findall("1234-56"), ["1234"]
        )
        self.assertEqual(
            parser.DateTimeParser._ONE_OR_TWO_DIGIT_RE.findall("4-56"), ["4", "56"]
        )


class DateTimeParserISOTests(Chai):
    def setUp(self):
        super(DateTimeParserISOTests, self).setUp()

        self.parser = parser.DateTimeParser("en_us")

    def test_YYYY(self):

        self.assertEqual(self.parser.parse_iso("2013"), datetime(2013, 1, 1))

    def test_YYYY_MM(self):

        for separator in DateTimeParser.SEPARATORS:
            self.assertEqual(
                self.parser.parse_iso(separator.join(("2013", "02"))),
                datetime(2013, 2, 1),
            )

    def test_YYYY_MM_DD(self):

        for separator in DateTimeParser.SEPARATORS:
            self.assertEqual(
                self.parser.parse_iso(separator.join(("2013", "02", "03"))),
                datetime(2013, 2, 3),
            )

    def test_YYYY_MM_DDTHH_mmZ(self):

        self.assertEqual(
            self.parser.parse_iso("2013-02-03T04:05+01:00"),
            datetime(2013, 2, 3, 4, 5, tzinfo=tz.tzoffset(None, 3600)),
        )

    def test_YYYY_MM_DDTHH_mm(self):

        self.assertEqual(
            self.parser.parse_iso("2013-02-03T04:05"), datetime(2013, 2, 3, 4, 5)
        )

    def test_YYYY_MM_DDTHH_mm_ssZ(self):

        self.assertEqual(
            self.parser.parse_iso("2013-02-03T04:05:06+01:00"),
            datetime(2013, 2, 3, 4, 5, 6, tzinfo=tz.tzoffset(None, 3600)),
        )

    def test_YYYY_MM_DDTHH_mm_ss(self):

        self.assertEqual(
            self.parser.parse_iso("2013-02-03T04:05:06"), datetime(2013, 2, 3, 4, 5, 6)
        )

    def test_YYYY_MM_DD_HH_mmZ(self):

        self.assertEqual(
            self.parser.parse_iso("2013-02-03 04:05+01:00"),
            datetime(2013, 2, 3, 4, 5, tzinfo=tz.tzoffset(None, 3600)),
        )

    def test_YYYY_MM_DD_HH_mm(self):

        self.assertEqual(
            self.parser.parse_iso("2013-02-03 04:05"), datetime(2013, 2, 3, 4, 5)
        )

    def test_YYYY_MM_DD_HH_mm_ssZ(self):

        self.assertEqual(
            self.parser.parse_iso("2013-02-03 04:05:06+01:00"),
            datetime(2013, 2, 3, 4, 5, 6, tzinfo=tz.tzoffset(None, 3600)),
        )

    def test_YYYY_MM_DD_HH_mm_ss(self):

        self.assertEqual(
            self.parser.parse_iso("2013-02-03 04:05:06"), datetime(2013, 2, 3, 4, 5, 6)
        )

    def test_YYYY_MM_DDTHH_mm_ss_S(self):

        self.assertEqual(
            self.parser.parse_iso("2013-02-03T04:05:06.7"),
            datetime(2013, 2, 3, 4, 5, 6, 700000),
        )

        self.assertEqual(
            self.parser.parse_iso("2013-02-03T04:05:06.78"),
            datetime(2013, 2, 3, 4, 5, 6, 780000),
        )

        self.assertEqual(
            self.parser.parse_iso("2013-02-03T04:05:06.789"),
            datetime(2013, 2, 3, 4, 5, 6, 789000),
        )

        self.assertEqual(
            self.parser.parse_iso("2013-02-03T04:05:06.7891"),
            datetime(2013, 2, 3, 4, 5, 6, 789100),
        )

        self.assertEqual(
            self.parser.parse_iso("2013-02-03T04:05:06.78912"),
            datetime(2013, 2, 3, 4, 5, 6, 789120),
        )

        # ISO 8601:2004(E), ISO, 2004-12-01, 4.2.2.4 ... the decimal fraction
        # shall be divided from the integer part by the decimal sign specified
        # in ISO 31-0, i.e. the comma [,] or full stop [.]. Of these, the comma
        # is the preferred sign.
        self.assertEqual(
            self.parser.parse_iso("2013-02-03T04:05:06,789123678"),
            datetime(2013, 2, 3, 4, 5, 6, 789124),
        )

        # there is no limit on the number of decimal places
        self.assertEqual(
            self.parser.parse_iso("2013-02-03T04:05:06.789123678"),
            datetime(2013, 2, 3, 4, 5, 6, 789124),
        )

    def test_YYYY_MM_DDTHH_mm_ss_SZ(self):

        self.assertEqual(
            self.parser.parse_iso("2013-02-03T04:05:06.7+01:00"),
            datetime(2013, 2, 3, 4, 5, 6, 700000, tzinfo=tz.tzoffset(None, 3600)),
        )

        self.assertEqual(
            self.parser.parse_iso("2013-02-03T04:05:06.78+01:00"),
            datetime(2013, 2, 3, 4, 5, 6, 780000, tzinfo=tz.tzoffset(None, 3600)),
        )

        self.assertEqual(
            self.parser.parse_iso("2013-02-03T04:05:06.789+01:00"),
            datetime(2013, 2, 3, 4, 5, 6, 789000, tzinfo=tz.tzoffset(None, 3600)),
        )

        self.assertEqual(
            self.parser.parse_iso("2013-02-03T04:05:06.7891+01:00"),
            datetime(2013, 2, 3, 4, 5, 6, 789100, tzinfo=tz.tzoffset(None, 3600)),
        )

        self.assertEqual(
            self.parser.parse_iso("2013-02-03T04:05:06.78912+01:00"),
            datetime(2013, 2, 3, 4, 5, 6, 789120, tzinfo=tz.tzoffset(None, 3600)),
        )

        # Properly parse string with Z timezone
        self.assertEqual(
            self.parser.parse_iso("2013-02-03T04:05:06.78912Z"),
            datetime(2013, 2, 3, 4, 5, 6, 789120),
        )

    def test_gnu_date(self):
        """
        regression tests for parsing output from GNU date(1)
        """
        # date -Ins
        self.assertEqual(
            self.parser.parse_iso("2016-11-16T09:46:30,895636557-0800"),
            datetime(
                2016, 11, 16, 9, 46, 30, 895636, tzinfo=tz.tzoffset(None, -3600 * 8)
            ),
        )

        # date --rfc-3339=ns
        self.assertEqual(
            self.parser.parse_iso("2016-11-16 09:51:14.682141526-08:00"),
            datetime(
                2016, 11, 16, 9, 51, 14, 682142, tzinfo=tz.tzoffset(None, -3600 * 8)
            ),
        )

    def test_isoformat(self):

        dt = datetime.utcnow()

        self.assertEqual(self.parser.parse_iso(dt.isoformat()), dt)


class TzinfoParserTests(Chai):
    def setUp(self):
        super(TzinfoParserTests, self).setUp()

        self.parser = parser.TzinfoParser()

    def test_parse_local(self):

        self.assertEqual(self.parser.parse("local"), tz.tzlocal())

    def test_parse_utc(self):

        self.assertEqual(self.parser.parse("utc"), tz.tzutc())
        self.assertEqual(self.parser.parse("UTC"), tz.tzutc())

    def test_parse_iso(self):

        self.assertEqual(self.parser.parse("01:00"), tz.tzoffset(None, 3600))
        self.assertEqual(self.parser.parse("+01:00"), tz.tzoffset(None, 3600))
        self.assertEqual(self.parser.parse("-01:00"), tz.tzoffset(None, -3600))

    def test_parse_str(self):

        self.assertEqual(self.parser.parse("US/Pacific"), tz.gettz("US/Pacific"))

    def test_parse_fails(self):

        with self.assertRaises(parser.ParserError):
            self.parser.parse("fail")


class DateTimeParserMonthNameTests(Chai):
    def setUp(self):
        super(DateTimeParserMonthNameTests, self).setUp()

        self.parser = parser.DateTimeParser("en_us")

    def test_shortmonth_capitalized(self):

        self.assertEqual(
            self.parser.parse("2013-Jan-01", "YYYY-MMM-DD"), datetime(2013, 1, 1)
        )

    def test_shortmonth_allupper(self):

        self.assertEqual(
            self.parser.parse("2013-JAN-01", "YYYY-MMM-DD"), datetime(2013, 1, 1)
        )

    def test_shortmonth_alllower(self):

        self.assertEqual(
            self.parser.parse("2013-jan-01", "YYYY-MMM-DD"), datetime(2013, 1, 1)
        )

    def test_month_capitalized(self):

        self.assertEqual(
            self.parser.parse("2013-January-01", "YYYY-MMMM-DD"), datetime(2013, 1, 1)
        )

    def test_month_allupper(self):

        self.assertEqual(
            self.parser.parse("2013-JANUARY-01", "YYYY-MMMM-DD"), datetime(2013, 1, 1)
        )

    def test_month_alllower(self):

        self.assertEqual(
            self.parser.parse("2013-january-01", "YYYY-MMMM-DD"), datetime(2013, 1, 1)
        )

    def test_localized_month_name(self):
        parser_ = parser.DateTimeParser("fr_fr")

        self.assertEqual(
            parser_.parse("2013-Janvier-01", "YYYY-MMMM-DD"), datetime(2013, 1, 1)
        )

    def test_localized_month_abbreviation(self):
        parser_ = parser.DateTimeParser("it_it")

        self.assertEqual(
            parser_.parse("2013-Gen-01", "YYYY-MMM-DD"), datetime(2013, 1, 1)
        )


class DateTimeParserMeridiansTests(Chai):
    def setUp(self):
        super(DateTimeParserMeridiansTests, self).setUp()

        self.parser = parser.DateTimeParser("en_us")

    def test_meridians_lowercase(self):
        self.assertEqual(
            self.parser.parse("2013-01-01 5am", "YYYY-MM-DD ha"),
            datetime(2013, 1, 1, 5),
        )

        self.assertEqual(
            self.parser.parse("2013-01-01 5pm", "YYYY-MM-DD ha"),
            datetime(2013, 1, 1, 17),
        )

    def test_meridians_capitalized(self):
        self.assertEqual(
            self.parser.parse("2013-01-01 5AM", "YYYY-MM-DD hA"),
            datetime(2013, 1, 1, 5),
        )

        self.assertEqual(
            self.parser.parse("2013-01-01 5PM", "YYYY-MM-DD hA"),
            datetime(2013, 1, 1, 17),
        )

    def test_localized_meridians_lowercase(self):
        parser_ = parser.DateTimeParser("hu_hu")
        self.assertEqual(
            parser_.parse("2013-01-01 5 de", "YYYY-MM-DD h a"), datetime(2013, 1, 1, 5)
        )

        self.assertEqual(
            parser_.parse("2013-01-01 5 du", "YYYY-MM-DD h a"), datetime(2013, 1, 1, 17)
        )

    def test_localized_meridians_capitalized(self):
        parser_ = parser.DateTimeParser("hu_hu")
        self.assertEqual(
            parser_.parse("2013-01-01 5 DE", "YYYY-MM-DD h A"), datetime(2013, 1, 1, 5)
        )

        self.assertEqual(
            parser_.parse("2013-01-01 5 DU", "YYYY-MM-DD h A"), datetime(2013, 1, 1, 17)
        )

    # regression check for https://github.com/crsmithdev/arrow/issues/607
    def test_es_meridians(self):
        parser_ = parser.DateTimeParser("es")

        self.assertEqual(
            parser_.parse("Junio 30, 2019 - 08:00 pm", "MMMM DD, YYYY - hh:mm a"),
            datetime(2019, 6, 30, 20, 0),
        )


class DateTimeParserMonthOrdinalDayTests(Chai):
    def setUp(self):
        super(DateTimeParserMonthOrdinalDayTests, self).setUp()

        self.parser = parser.DateTimeParser("en_us")

    def test_english(self):
        parser_ = parser.DateTimeParser("en_us")

        self.assertEqual(
            parser_.parse("January 1st, 2013", "MMMM Do, YYYY"), datetime(2013, 1, 1)
        )
        self.assertEqual(
            parser_.parse("January 2nd, 2013", "MMMM Do, YYYY"), datetime(2013, 1, 2)
        )
        self.assertEqual(
            parser_.parse("January 3rd, 2013", "MMMM Do, YYYY"), datetime(2013, 1, 3)
        )
        self.assertEqual(
            parser_.parse("January 4th, 2013", "MMMM Do, YYYY"), datetime(2013, 1, 4)
        )
        self.assertEqual(
            parser_.parse("January 11th, 2013", "MMMM Do, YYYY"), datetime(2013, 1, 11)
        )
        self.assertEqual(
            parser_.parse("January 12th, 2013", "MMMM Do, YYYY"), datetime(2013, 1, 12)
        )
        self.assertEqual(
            parser_.parse("January 13th, 2013", "MMMM Do, YYYY"), datetime(2013, 1, 13)
        )
        self.assertEqual(
            parser_.parse("January 21st, 2013", "MMMM Do, YYYY"), datetime(2013, 1, 21)
        )
        self.assertEqual(
            parser_.parse("January 31st, 2013", "MMMM Do, YYYY"), datetime(2013, 1, 31)
        )

        with self.assertRaises(ParserError):
            parser_.parse("January 1th, 2013", "MMMM Do, YYYY")

        with self.assertRaises(ParserError):
            parser_.parse("January 11st, 2013", "MMMM Do, YYYY")

    def test_italian(self):
        parser_ = parser.DateTimeParser("it_it")

        self.assertEqual(
            parser_.parse("Gennaio 1º, 2013", "MMMM Do, YYYY"), datetime(2013, 1, 1)
        )

    def test_spanish(self):
        parser_ = parser.DateTimeParser("es_es")

        self.assertEqual(
            parser_.parse("Enero 1º, 2013", "MMMM Do, YYYY"), datetime(2013, 1, 1)
        )

    def test_french(self):
        parser_ = parser.DateTimeParser("fr_fr")

        self.assertEqual(
            parser_.parse("Janvier 1er, 2013", "MMMM Do, YYYY"), datetime(2013, 1, 1)
        )

        self.assertEqual(
            parser_.parse("Janvier 2e, 2013", "MMMM Do, YYYY"), datetime(2013, 1, 2)
        )

        self.assertEqual(
            parser_.parse("Janvier 11e, 2013", "MMMM Do, YYYY"), datetime(2013, 1, 11)
        )


class DateTimeParserSearchDateTests(Chai):
    def setUp(self):
        super(DateTimeParserSearchDateTests, self).setUp()
        self.parser = parser.DateTimeParser()

    def test_parse_search(self):

        self.assertEqual(
            self.parser.parse("Today is 25 of September of 2003", "DD of MMMM of YYYY"),
            datetime(2003, 9, 25),
        )

    def test_parse_search_with_numbers(self):

        self.assertEqual(
            self.parser.parse(
                "2000 people met the 2012-01-01 12:05:10", "YYYY-MM-DD HH:mm:ss"
            ),
            datetime(2012, 1, 1, 12, 5, 10),
        )

        self.assertEqual(
            self.parser.parse(
                "Call 01-02-03 on 79-01-01 12:05:10", "YY-MM-DD HH:mm:ss"
            ),
            datetime(1979, 1, 1, 12, 5, 10),
        )

    def test_parse_search_with_names(self):

        self.assertEqual(
            self.parser.parse("June was born in May 1980", "MMMM YYYY"),
            datetime(1980, 5, 1),
        )

    def test_parse_search_locale_with_names(self):
        p = parser.DateTimeParser("sv_se")

        self.assertEqual(
            p.parse("Jan föddes den 31 Dec 1980", "DD MMM YYYY"), datetime(1980, 12, 31)
        )

        self.assertEqual(
            p.parse("Jag föddes den 25 Augusti 1975", "DD MMMM YYYY"),
            datetime(1975, 8, 25),
        )

    def test_parse_search_fails(self):

        with self.assertRaises(parser.ParserError):
            self.parser.parse("Jag föddes den 25 Augusti 1975", "DD MMMM YYYY")

    def test_escape(self):

        format = "MMMM D, YYYY [at] h:mma"
        self.assertEqual(
            self.parser.parse("Thursday, December 10, 2015 at 5:09pm", format),
            datetime(2015, 12, 10, 17, 9),
        )

        format = "[MMMM] M D, YYYY [at] h:mma"
        self.assertEqual(
            self.parser.parse("MMMM 12 10, 2015 at 5:09pm", format),
            datetime(2015, 12, 10, 17, 9),
        )

        format = "[It happened on] MMMM Do [in the year] YYYY [a long time ago]"
        self.assertEqual(
            self.parser.parse(
                "It happened on November 25th in the year 1990 a long time ago", format
            ),
            datetime(1990, 11, 25),
        )

        format = "[It happened on] MMMM Do [in the][ year] YYYY [a long time ago]"
        self.assertEqual(
            self.parser.parse(
                "It happened on November 25th in the year 1990 a long time ago", format
            ),
            datetime(1990, 11, 25),
        )

        format = "[I'm][ entirely][ escaped,][ weee!]"
        self.assertEqual(
            self.parser.parse("I'm entirely escaped, weee!", format), datetime(1, 1, 1)
        )

        # Special RegEx characters
        format = "MMM DD, YYYY |^${}().*+?<>-& h:mm A"
        self.assertEqual(
            self.parser.parse("Dec 31, 2017 |^${}().*+?<>-& 2:00 AM", format),
            datetime(2017, 12, 31, 2, 0),
        )
