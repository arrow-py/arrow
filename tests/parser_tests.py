from chai import Chai
from datetime import datetime
from dateutil import tz
import calendar
import time

from arrow import parser

class DateTimeParserTests(Chai):

    def setUp(self):
        super(DateTimeParserTests, self).setUp()

        self.parse = parser.DateTimeParser.parse

    def test_parse_multiformat(self):

        mock_datetime = mock()

        expect(parser.DateTimeParser.parse).args('str', 'fmt_a').raises(Exception)
        expect(parser.DateTimeParser.parse).args('str', 'fmt_b').returns(mock_datetime)

        result = parser.DateTimeParser._parse_multiformat('str', ['fmt_a', 'fmt_b'])

        assertEqual(result, mock_datetime)

    def test_parse_multiformat_all_fail(self):

        expect(parser.DateTimeParser.parse).args('str', 'fmt_a').raises(Exception)
        expect(parser.DateTimeParser.parse).args('str', 'fmt_b').raises(Exception)

        with assertRaises(Exception):
            parser.DateTimeParser._parse_multiformat('str', ['fmt_a', 'fmt_b'])


class DateTimeParserParseTests(Chai):

    def setUp(self):
        super(DateTimeParserParseTests, self).setUp()

        self.parse = parser.DateTimeParser.parse

    def test_parse_list(self):

        expect(parser.DateTimeParser._parse_multiformat).args('str', ['fmt_a', 'fmt_b']).returns('result')

        result = self.parse('str', ['fmt_a', 'fmt_b'])

        assertEqual(result, 'result')

    def test_parse_unrecognized_token(self):

        mock_input_re_map = mock(parser.DateTimeParser, '_INPUT_RE_MAP')

        expect(mock_input_re_map.__getitem__).args('YYYY').raises(KeyError)

        with assertRaises(parser.ParserError):
            self.parse('2013-01-01', 'YYYY-MM-DD')

    def test_parse_parse_token_error(self):

        expect(parser.DateTimeParser._parse_token).args('YYYY', '2013').raises(Exception)

        with assertRaises(parser.ParserError):
            self.parse('2013-01-01', 'YYYY-MM-DD')

    def test_parse_parse_no_match(self):

        with assertRaises(parser.ParserError):
            self.parse('01-01', 'YYYY-MM-DD')

    def test_parse_numbers(self):

        expected = datetime(2012, 1, 1, 12, 5, 10)
        assertEqual(self.parse('2012-01-01 12:05:10', 'YYYY-MM-DD HH:mm:ss'), expected)

    def test_parse_year_two_digit(self):

        expected = datetime(1955, 1, 1, 12, 5, 10)
        assertEqual(self.parse('55-01-01 12:05:10', 'YY-MM-DD HH:mm:ss'), expected)

    def test_parse_timestamp(self):

        timestamp = int(time.time())
        expected = datetime.fromtimestamp(timestamp)
        assertEqual(self.parse(str(timestamp), 'X'), expected)

    def test_parse_names(self):

        expected = datetime(2012, 1, 1)
        assertEqual(self.parse('January 1, 2012', 'MMMM D, YYYY'), expected)

    def test_parse_pm(self):

        expected = datetime(1, 1, 1, 13, 0, 0)
        assertEqual(self.parse('1 pm', 'H a'), expected)

        expected = datetime(1, 1, 1, 13, 0, 0)
        assertEqual(self.parse('13 pm', 'H a'), expected)

    def test_parse_subsecond(self):

        expected = datetime(2013, 1, 1, 12, 30, 45, 900000)
        assertEqual(self.parse('2013-01-01 12:30:45:9', 'YYYY-MM-DD HH:mm:ss:S'), expected)

        expected = datetime(2013, 1, 1, 12, 30, 45, 990000)
        assertEqual(self.parse('2013-01-01 12:30:45:99', 'YYYY-MM-DD HH:mm:ss:SS'), expected)

        expected = datetime(2013, 1, 1, 12, 30, 45, 999000)
        assertEqual(self.parse('2013-01-01 12:30:45:999', 'YYYY-MM-DD HH:mm:ss:SSS'), expected)

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

        assertEqual(self.format_regex.findall('SSS-SS-S'), ['SSS', 'SS', 'S'])

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


class TzinfoParserTests(Chai):

    def setUp(self):
        super(TzinfoParserTests, self).setUp()

        self.parse = parser.TzinfoParser.parse

    def test_parse_local(self):

        assertEqual(self.parse('local'), tz.tzlocal())

    def test_parse_utc(self):

        assertEqual(self.parse('utc'), tz.tzutc())
        assertEqual(self.parse('UTC'), tz.tzutc())

    def test_parse_iso(self):

        assertEqual(self.parse('01:00'), tz.tzoffset(None, 3600))
        assertEqual(self.parse('+01:00'), tz.tzoffset(None, 3600))
        assertEqual(self.parse('-01:00'), tz.tzoffset(None, -3600))

    def test_parse_str(self):

        assertEqual(self.parse('PDT'), tz.gettz('PDT'))

    def test_parse_fails(self):

        with assertRaises(parser.ParserError):
            self.parse('fail')
