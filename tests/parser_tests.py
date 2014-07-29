from chai import Chai
from datetime import datetime
from dateutil import tz
import calendar
import time

from arrow import parser

class DateTimeParserTests(Chai):

    def setUp(self):
        super(DateTimeParserTests, self).setUp()

        self.parser = parser.DateTimeParser()

    def test_parse_multiformat(self):

        mock_datetime = mock()

        expect(self.parser.parse).args('str', 'fmt_a').raises(Exception)
        expect(self.parser.parse).args('str', 'fmt_b').returns(mock_datetime)

        result = self.parser._parse_multiformat('str', ['fmt_a', 'fmt_b'])

        assertEqual(result, mock_datetime)

    def test_parse_multiformat_all_fail(self):

        expect(self.parser.parse).args('str', 'fmt_a').raises(Exception)
        expect(self.parser.parse).args('str', 'fmt_b').raises(Exception)

        with assertRaises(Exception):
            self.parser._parse_multiformat('str', ['fmt_a', 'fmt_b'])


class DateTimeParserParseTests(Chai):

    def setUp(self):
        super(DateTimeParserParseTests, self).setUp()

        self.parser = parser.DateTimeParser()

    def test_parse_list(self):

        expect(self.parser._parse_multiformat).args('str', ['fmt_a', 'fmt_b']).returns('result')

        result = self.parser.parse('str', ['fmt_a', 'fmt_b'])

        assertEqual(result, 'result')

    def test_parse_unrecognized_token(self):

        mock_input_re_map = mock(parser.DateTimeParser, '_INPUT_RE_MAP')

        expect(mock_input_re_map.__getitem__).args('YYYY').raises(KeyError)

        with assertRaises(parser.ParserError):
            self.parser.parse('2013-01-01', 'YYYY-MM-DD')

    def test_parse_parse_no_match(self):

        with assertRaises(parser.ParserError):
            self.parser.parse('01-01', 'YYYY-MM-DD')

    def test_parse_separators(self):

        with assertRaises(parser.ParserError):
            self.parser.parse('1403549231', 'YYYY-MM-DD')

    def test_parse_numbers(self):

        expected = datetime(2012, 1, 1, 12, 5, 10)
        assertEqual(self.parser.parse('2012-01-01 12:05:10', 'YYYY-MM-DD HH:mm:ss'), expected)

    def test_parse_year_two_digit(self):

        expected = datetime(1979, 1, 1, 12, 5, 10)
        assertEqual(self.parser.parse('79-01-01 12:05:10', 'YY-MM-DD HH:mm:ss'), expected)

    def test_parse_timestamp(self):

        tz_utc = tz.tzutc()
        timestamp = int(time.time())
        expected = datetime.fromtimestamp(timestamp, tz=tz_utc)
        assertEqual(self.parser.parse(str(timestamp), 'X'), expected)

    def test_parse_names(self):

        expected = datetime(2012, 1, 1)

        assertEqual(self.parser.parse('January 1, 2012', 'MMMM D, YYYY'), expected)
        assertEqual(self.parser.parse('Jan 1, 2012', 'MMM D, YYYY'), expected)

    def test_parse_pm(self):

        expected = datetime(1, 1, 1, 13, 0, 0)
        assertEqual(self.parser.parse('1 pm', 'H a'), expected)

        expected = datetime(1, 1, 1, 1, 0, 0)
        assertEqual(self.parser.parse('1 am', 'H A'), expected)

        expected = datetime(1, 1, 1, 0, 0, 0)
        assertEqual(self.parser.parse('12 am', 'H A'), expected)

        expected = datetime(1, 1, 1, 12, 0, 0)
        assertEqual(self.parser.parse('12 pm', 'H A'), expected)

    def test_parse_tz(self):

        expected = datetime(2013, 1, 1, tzinfo=tz.tzoffset(None, -7 * 3600))
        assertEqual(self.parser.parse('2013-01-01 -07:00', 'YYYY-MM-DD ZZ'), expected)

    def test_parse_subsecond(self):

        expected = datetime(2013, 1, 1, 12, 30, 45, 900000)
        assertEqual(self.parser.parse('2013-01-01 12:30:45:9', 'YYYY-MM-DD HH:mm:ss:S'), expected)

        expected = datetime(2013, 1, 1, 12, 30, 45, 990000)
        assertEqual(self.parser.parse('2013-01-01 12:30:45:99', 'YYYY-MM-DD HH:mm:ss:SS'), expected)

        expected = datetime(2013, 1, 1, 12, 30, 45, 999000)
        assertEqual(self.parser.parse('2013-01-01 12:30:45:999', 'YYYY-MM-DD HH:mm:ss:SSS'), expected)

        expected = datetime(2013, 1, 1, 12, 30, 45, 999900)
        assertEqual(self.parser.parse('2013-01-01 12:30:45:9999', 'YYYY-MM-DD HH:mm:ss:SSSS'), expected)

        expected = datetime(2013, 1, 1, 12, 30, 45, 999990)
        assertEqual(self.parser.parse('2013-01-01 12:30:45:99999', 'YYYY-MM-DD HH:mm:ss:SSSSS'), expected)

        expected = datetime(2013, 1, 1, 12, 30, 45, 999999)
        assertEqual(self.parser.parse('2013-01-01 12:30:45:999999', 'YYYY-MM-DD HH:mm:ss:SSSSSS'), expected)

    def test_map_lookup_keyerror(self):

        with assertRaises(parser.ParserError):
            parser.DateTimeParser._map_lookup({'a': '1'}, 'b')

    def test_try_timestamp(self):

        assertEqual(parser.DateTimeParser._try_timestamp('1.1'), 1.1)
        assertEqual(parser.DateTimeParser._try_timestamp('1'), 1)
        assertEqual(parser.DateTimeParser._try_timestamp('abc'), None)


class DateTimeParserRegexTests(Chai):

    def setUp(self):
        super(DateTimeParserRegexTests, self).setUp()

        self.format_regex = parser.DateTimeParser._FORMAT_RE

    def test_format_year(self):

        assertEqual(self.format_regex.findall('YYYY-YY'), ['YYYY', 'YY'])

    def test_format_month(self):

        assertEqual(self.format_regex.findall('MMMM-MMM-MM-M'), ['MMMM', 'MMM', 'MM', 'M'])

    def test_format_day(self):

        assertEqual(self.format_regex.findall('DDDD-DDD-DD-D'), ['DDDD', 'DDD', 'DD', 'D'])

    def test_format_hour(self):

        assertEqual(self.format_regex.findall('HH-H-hh-h'), ['HH', 'H', 'hh', 'h'])

    def test_format_minute(self):

        assertEqual(self.format_regex.findall('mm-m'), ['mm', 'm'])

    def test_format_second(self):

        assertEqual(self.format_regex.findall('ss-s'), ['ss', 's'])

    def test_format_subsecond(self):

        assertEqual(self.format_regex.findall('SSSSSS-SSSSS-SSSS-SSS-SS-S'),
                ['SSSSSS', 'SSSSS', 'SSSS', 'SSS', 'SS', 'S'])

    def test_format_tz(self):

        assertEqual(self.format_regex.findall('ZZ-Z'), ['ZZ', 'Z'])

    def test_format_am_pm(self):

        assertEqual(self.format_regex.findall('A-a'), ['A', 'a'])

    def test_format_timestamp(self):

        assertEqual(self.format_regex.findall('X'), ['X'])

    def test_month_names(self):

        text = '_'.join(calendar.month_name[1:])

        result = parser.DateTimeParser._INPUT_RE_MAP['MMMM'].findall(text)

        assertEqual(result, calendar.month_name[1:])

    def test_month_abbreviations(self):

        text = '_'.join(calendar.month_abbr[1:])

        result = parser.DateTimeParser._INPUT_RE_MAP['MMM'].findall(text)

        assertEqual(result, calendar.month_abbr[1:])

    def test_digits(self):

        assertEqual(parser.DateTimeParser._TWO_DIGIT_RE.findall('12-3-45'), ['12', '45'])
        assertEqual(parser.DateTimeParser._FOUR_DIGIT_RE.findall('1234-56'), ['1234'])
        assertEqual(parser.DateTimeParser._ONE_OR_TWO_DIGIT_RE.findall('4-56'), ['4', '56'])


class DateTimeParserISOTests(Chai):

    def setUp(self):
        super(DateTimeParserISOTests, self).setUp()

        self.parser = parser.DateTimeParser('en_us')

    def test_YYYY(self):

        assertEqual(
            self.parser.parse_iso('2013'),
            datetime(2013, 1, 1)
        )

    def test_YYYY_MM(self):

        assertEqual(
            self.parser.parse_iso('2013-02'),
            datetime(2013, 2, 1)
        )

    def test_YYYY_MM_DD(self):

        assertEqual(
            self.parser.parse_iso('2013-02-03'),
            datetime(2013, 2, 3)
        )

    def test_YYYY_MM_DDTHH_mmZ(self):

        assertEqual(
            self.parser.parse_iso('2013-02-03T04:05+01:00'),
            datetime(2013, 2, 3, 4, 5, tzinfo=tz.tzoffset(None, 3600))
        )

    def test_YYYY_MM_DDTHH_mm(self):

        assertEqual(
            self.parser.parse_iso('2013-02-03T04:05'),
            datetime(2013, 2, 3, 4, 5)
        )

    def test_YYYY_MM_DDTHH_mm_ssZ(self):

        assertEqual(
            self.parser.parse_iso('2013-02-03T04:05:06+01:00'),
            datetime(2013, 2, 3, 4, 5, 6, tzinfo=tz.tzoffset(None, 3600))
        )

    def test_YYYY_MM_DDTHH_mm_ss(self):

        assertEqual(
            self.parser.parse_iso('2013-02-03T04:05:06'),
            datetime(2013, 2, 3, 4, 5, 6)
        )

    def test_YYYY_MM_DD_HH_mmZ(self):

        assertEqual(
            self.parser.parse_iso('2013-02-03 04:05+01:00'),
            datetime(2013, 2, 3, 4, 5, tzinfo=tz.tzoffset(None, 3600))
        )

    def test_YYYY_MM_DD_HH_mm(self):

        assertEqual(
            self.parser.parse_iso('2013-02-03 04:05'),
            datetime(2013, 2, 3, 4, 5)
        )

    def test_YYYY_MM_DD_HH_mm_ssZ(self):

        assertEqual(
            self.parser.parse_iso('2013-02-03 04:05:06+01:00'),
            datetime(2013, 2, 3, 4, 5, 6, tzinfo=tz.tzoffset(None, 3600))
        )

    def test_YYYY_MM_DD_HH_mm_ss(self):

        assertEqual(
            self.parser.parse_iso('2013-02-03 04:05:06'),
            datetime(2013, 2, 3, 4, 5, 6)
        )

    def test_YYYY_MM_DDTHH_mm_ss_S(self):

        assertEqual(
            self.parser.parse_iso('2013-02-03T04:05:06.7'),
            datetime(2013, 2, 3, 4, 5, 6, 7)
        )

        assertEqual(
            self.parser.parse_iso('2013-02-03T04:05:06.78'),
            datetime(2013, 2, 3, 4, 5, 6, 78)
        )

        assertEqual(
            self.parser.parse_iso('2013-02-03T04:05:06.789'),
            datetime(2013, 2, 3, 4, 5, 6, 789)
        )

        assertEqual(
            self.parser.parse_iso('2013-02-03T04:05:06.7891'),
            datetime(2013, 2, 3, 4, 5, 6, 7891)
        )

        assertEqual(
            self.parser.parse_iso('2013-02-03T04:05:06.78912'),
            datetime(2013, 2, 3, 4, 5, 6, 78912)
        )

    def test_YYYY_MM_DDTHH_mm_ss_SZ(self):

        assertEqual(
            self.parser.parse_iso('2013-02-03T04:05:06.7+01:00'),
            datetime(2013, 2, 3, 4, 5, 6, 7, tzinfo=tz.tzoffset(None, 3600))
        )

        assertEqual(
            self.parser.parse_iso('2013-02-03T04:05:06.78+01:00'),
            datetime(2013, 2, 3, 4, 5, 6, 78, tzinfo=tz.tzoffset(None, 3600))
        )

        assertEqual(
            self.parser.parse_iso('2013-02-03T04:05:06.789+01:00'),
            datetime(2013, 2, 3, 4, 5, 6, 789, tzinfo=tz.tzoffset(None, 3600))
        )

        assertEqual(
            self.parser.parse_iso('2013-02-03T04:05:06.7891+01:00'),
            datetime(2013, 2, 3, 4, 5, 6, 7891, tzinfo=tz.tzoffset(None, 3600))
        )

        assertEqual(
            self.parser.parse_iso('2013-02-03T04:05:06.78912+01:00'),
            datetime(2013, 2, 3, 4, 5, 6, 78912, tzinfo=tz.tzoffset(None, 3600))
        )

    def test_isoformat(self):

        dt = datetime.utcnow()

        assertEqual(self.parser.parse_iso(dt.isoformat()), dt)


class TzinfoParserTests(Chai):

    def setUp(self):
        super(TzinfoParserTests, self).setUp()

        self.parser = parser.TzinfoParser()

    def test_parse_local(self):

        assertEqual(self.parser.parse('local'), tz.tzlocal())

    def test_parse_utc(self):

        assertEqual(self.parser.parse('utc'), tz.tzutc())
        assertEqual(self.parser.parse('UTC'), tz.tzutc())

    def test_parse_iso(self):

        assertEqual(self.parser.parse('01:00'), tz.tzoffset(None, 3600))
        assertEqual(self.parser.parse('+01:00'), tz.tzoffset(None, 3600))
        assertEqual(self.parser.parse('-01:00'), tz.tzoffset(None, -3600))

    def test_parse_str(self):

        assertEqual(self.parser.parse('US/Pacific'), tz.gettz('US/Pacific'))

    def test_parse_fails(self):

        with assertRaises(parser.ParserError):
            self.parser.parse('fail')
