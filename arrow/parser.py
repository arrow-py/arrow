# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals

from datetime import datetime
from dateutil import tz
import re
from arrow import locales


class ParserError(RuntimeError):
    pass


class DateTimeParser(object):

    _FORMAT_RE = re.compile('(YYY?Y?|MM?M?M?|Do|DD?D?D?|d?d?d?d|HH?|hh?|mm?|ss?|SS?S?S?S?S?S?S?S?|ZZ?Z?|a|A|X)')
    _ESCAPE_RE = re.compile('\[[^\[\]]*\]')

    _ONE_THROUGH_NINE_DIGIT_RE = re.compile('\d{1,9}')
    _ONE_THROUGH_EIGHT_DIGIT_RE = re.compile('\d{1,8}')
    _ONE_THROUGH_SEVEN_DIGIT_RE = re.compile('\d{1,7}')
    _ONE_THROUGH_SIX_DIGIT_RE = re.compile('\d{1,6}')
    _ONE_THROUGH_FIVE_DIGIT_RE = re.compile('\d{1,5}')
    _ONE_THROUGH_FOUR_DIGIT_RE = re.compile('\d{1,4}')
    _ONE_TWO_OR_THREE_DIGIT_RE = re.compile('\d{1,3}')
    _ONE_OR_TWO_DIGIT_RE = re.compile('\d{1,2}')
    _FOUR_DIGIT_RE = re.compile('\d{4}')
    _TWO_DIGIT_RE = re.compile('\d{2}')
    _TZ_RE = re.compile('[+\-]?\d{2}:?(\d{2})?')
    _TZ_NAME_RE = re.compile('\w[\w+\-/]+')


    _BASE_INPUT_RE_MAP = {
        'YYYY': _FOUR_DIGIT_RE,
        'YY': _TWO_DIGIT_RE,
        'MM': _TWO_DIGIT_RE,
        'M': _ONE_OR_TWO_DIGIT_RE,
        'DD': _TWO_DIGIT_RE,
        'D': _ONE_OR_TWO_DIGIT_RE,
        'HH': _TWO_DIGIT_RE,
        'H': _ONE_OR_TWO_DIGIT_RE,
        'hh': _TWO_DIGIT_RE,
        'h': _ONE_OR_TWO_DIGIT_RE,
        'mm': _TWO_DIGIT_RE,
        'm': _ONE_OR_TWO_DIGIT_RE,
        'ss': _TWO_DIGIT_RE,
        's': _ONE_OR_TWO_DIGIT_RE,
        'X': re.compile('\d+'),
        'ZZZ': _TZ_NAME_RE,
        'ZZ': _TZ_RE,
        'Z': _TZ_RE,
        'SSSSSSSSS': _ONE_THROUGH_NINE_DIGIT_RE,
        'SSSSSSSS': _ONE_THROUGH_EIGHT_DIGIT_RE,
        'SSSSSSS': _ONE_THROUGH_SEVEN_DIGIT_RE,
        'SSSSSS': _ONE_THROUGH_SIX_DIGIT_RE,
        'SSSSS': _ONE_THROUGH_FIVE_DIGIT_RE,
        'SSSS': _ONE_THROUGH_FOUR_DIGIT_RE,
        'SSS': _ONE_TWO_OR_THREE_DIGIT_RE,
        'SS': _ONE_OR_TWO_DIGIT_RE,
        'S': re.compile('\d'),
    }

    MARKERS = ['YYYY', 'MM', 'DD']
    SEPARATORS = ['-', '/', '.']

    def __init__(self, locale='en_us'):

        self.locale = locales.get_locale(locale)
        self._input_re_map = self._BASE_INPUT_RE_MAP.copy()
        self._input_re_map.update({
            'MMMM': self._choice_re(self.locale.month_names[1:], re.IGNORECASE),
            'MMM': self._choice_re(self.locale.month_abbreviations[1:],
                                   re.IGNORECASE),
            'Do': re.compile(self.locale.ordinal_day_re),
            'dddd': self._choice_re(self.locale.day_names[1:], re.IGNORECASE),
            'ddd': self._choice_re(self.locale.day_abbreviations[1:],
                                   re.IGNORECASE),
            'd' : re.compile("[1-7]"),
            'a': self._choice_re(
                (self.locale.meridians['am'], self.locale.meridians['pm'])
            ),
            # note: 'A' token accepts both 'am/pm' and 'AM/PM' formats to
            # ensure backwards compatibility of this token
            'A': self._choice_re(self.locale.meridians.values())
        })

    def parse_iso(self, string):

        has_time = 'T' in string or ' ' in string.strip()
        space_divider = ' ' in string.strip()

        if has_time:
            if space_divider:
                date_string, time_string = string.split(' ', 1)
            else:
                date_string, time_string = string.split('T', 1)
            time_parts = re.split('[+-]', time_string, 1)
            has_tz = len(time_parts) > 1
            has_seconds = time_parts[0].count(':') > 1
            has_subseconds = '.' in time_parts[0]

            if has_subseconds:
                subseconds_token = 'S' * min(len(re.split('\D+', time_parts[0].split('.')[1], 1)[0]), 9)
                formats = ['YYYY-MM-DDTHH:mm:ss.%s' % subseconds_token]
            elif has_seconds:
                formats = ['YYYY-MM-DDTHH:mm:ss']
            else:
                formats = ['YYYY-MM-DDTHH:mm']
        else:
            has_tz = False
            # generate required formats: YYYY-MM-DD, YYYY-MM-DD, YYYY
            # using various separators: -, /, .
            l = len(self.MARKERS)
            formats = [separator.join(self.MARKERS[:l-i])
                        for i in range(l)
                        for separator in self.SEPARATORS]

        if has_time and has_tz:
            formats = [f + 'Z' for f in formats]

        if space_divider:
            formats = [item.replace('T', ' ', 1) for item in formats]

        return self._parse_multiformat(string, formats)

    def parse(self, string, fmt):

        if isinstance(fmt, list):
            return self._parse_multiformat(string, fmt)

        # fmt is a string of tokens like 'YYYY-MM-DD'
        # we construct a new string by replacing each
        # token by its pattern:
        # 'YYYY-MM-DD' -> '(?P<YYYY>\d{4})-(?P<MM>\d{2})-(?P<DD>\d{2})'
        tokens = []
        offset = 0

        # Extract the bracketed expressions to be reinserted later.
        escaped_fmt = re.sub(self._ESCAPE_RE, "#" , fmt)
        escaped_data = re.findall(self._ESCAPE_RE, fmt)

        fmt_pattern = escaped_fmt

        for m in self._FORMAT_RE.finditer(escaped_fmt):
            token = m.group(0)
            try:
                input_re = self._input_re_map[token]
            except KeyError:
                raise ParserError('Unrecognized token \'{0}\''.format(token))
            input_pattern = '(?P<{0}>{1})'.format(token, input_re.pattern)
            tokens.append(token)
            # a pattern doesn't have the same length as the token
            # it replaces! We keep the difference in the offset variable.
            # This works because the string is scanned left-to-right and matches
            # are returned in the order found by finditer.
            fmt_pattern = fmt_pattern[:m.start() + offset] + input_pattern + fmt_pattern[m.end() + offset:]
            offset += len(input_pattern) - (m.end() - m.start())

        final_fmt_pattern = ""
        a = fmt_pattern.split("#")
        b = escaped_data

        # Due to the way Python splits, 'a' will always be longer
        for i in range(len(a)):
            final_fmt_pattern += a[i]
            if i < len(b):
                final_fmt_pattern += b[i][1:-1]

        match = re.search(final_fmt_pattern, string, flags=re.IGNORECASE)
        if match is None:
            raise ParserError('Failed to match \'{0}\' when parsing \'{1}\''.format(final_fmt_pattern, string))
        parts = {}
        for token in tokens:
            if token == 'Do':
                value = match.group('value')
            else:
                value = match.group(token)
            self._parse_token(token, value, parts)
        return self._build_datetime(parts)

    def _parse_token(self, token, value, parts):

        if token == 'YYYY':
            parts['year'] = int(value)
        elif token == 'YY':
            value = int(value)
            parts['year'] = 1900 + value if value > 68 else 2000 + value

        elif token in ['MMMM', 'MMM']:
            parts['month'] = self.locale.month_number(value.lower())

        elif token in ['MM', 'M']:
            parts['month'] = int(value)

        elif token in ['DD', 'D']:
            parts['day'] = int(value)

        elif token in ['Do']:
            parts['day'] = int(value)

        elif token.upper() in ['HH', 'H']:
            parts['hour'] = int(value)

        elif token in ['mm', 'm']:
            parts['minute'] = int(value)

        elif token in ['ss', 's']:
            parts['second'] = int(value)

        elif token == 'SSSSSSSSS':
            parts['microsecond'] = int(value) // 1000
        elif token == 'SSSSSSSS':
            parts['microsecond'] = int(value) // 100
        elif token == 'SSSSSSS':
            parts['microsecond'] = int(value) // 10
        elif token == 'SSSSSS':
            parts['microsecond'] = int(value)
        elif token == 'SSSSS':
            parts['microsecond'] = int(value) * 10
        elif token == 'SSSS':
            parts['microsecond'] = int(value) * 100
        elif token == 'SSS':
            parts['microsecond'] = int(value) * 1000
        elif token == 'SS':
            parts['microsecond'] = int(value) * 10000
        elif token == 'S':
            parts['microsecond'] = int(value) * 100000

        elif token == 'X':
            parts['timestamp'] = int(value)

        elif token in ['ZZZ', 'ZZ', 'Z']:
            parts['tzinfo'] = TzinfoParser.parse(value)

        elif token in ['a', 'A']:
            if value in (
                    self.locale.meridians['am'],
                    self.locale.meridians['AM']
            ):
                parts['am_pm'] = 'am'
            elif value in (
                    self.locale.meridians['pm'],
                    self.locale.meridians['PM']
            ):
                parts['am_pm'] = 'pm'

    @staticmethod
    def _build_datetime(parts):

        timestamp = parts.get('timestamp')

        if timestamp:
            tz_utc = tz.tzutc()
            return datetime.fromtimestamp(timestamp, tz=tz_utc)

        am_pm = parts.get('am_pm')
        hour = parts.get('hour', 0)

        if am_pm == 'pm' and hour < 12:
            hour += 12
        elif am_pm == 'am' and hour == 12:
            hour = 0

        return datetime(year=parts.get('year', 1), month=parts.get('month', 1),
            day=parts.get('day', 1), hour=hour, minute=parts.get('minute', 0),
            second=parts.get('second', 0), microsecond=parts.get('microsecond', 0),
            tzinfo=parts.get('tzinfo'))

    def _parse_multiformat(self, string, formats):

        _datetime = None

        for fmt in formats:
            try:
                _datetime = self.parse(string, fmt)
                break
            except:
                pass

        if _datetime is None:
            raise ParserError('Could not match input to any of {0} on \'{1}\''.format(formats, string))

        return _datetime

    @staticmethod
    def _map_lookup(input_map, key):

        try:
            return input_map[key]
        except KeyError:
            raise ParserError('Could not match "{0}" to {1}'.format(key, input_map))

    @staticmethod
    def _try_timestamp(string):

        try:
            return float(string)
        except:
            return None

    @staticmethod
    def _choice_re(choices, flags=0):
        return re.compile('({0})'.format('|'.join(choices)), flags=flags)


class TzinfoParser(object):

    _TZINFO_RE = re.compile('([+\-])?(\d\d):?(\d\d)?')

    @classmethod
    def parse(cls, string):

        tzinfo = None

        if string == 'local':
            tzinfo = tz.tzlocal()

        elif string in ['utc', 'UTC']:
            tzinfo = tz.tzutc()

        else:

            iso_match = cls._TZINFO_RE.match(string)

            if iso_match:
                sign, hours, minutes = iso_match.groups()
                if minutes is None:
                    minutes = 0
                seconds = int(hours) * 3600 + int(minutes) * 60

                if sign == '-':
                    seconds *= -1

                tzinfo = tz.tzoffset(None, seconds)

            else:
                tzinfo = tz.gettz(string)

        if tzinfo is None:
            raise ParserError('Could not parse timezone expression "{0}"', string)

        return tzinfo
