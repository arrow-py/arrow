# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals

from datetime import datetime
from dateutil import tz
import re

try:
    from functools import lru_cache
except ImportError:  # pragma: no cover
    from backports.functools_lru_cache import lru_cache  # pragma: no cover

from arrow import locales


class ParserError(RuntimeError):
    pass


class DateTimeParser(object):

    _FORMAT_RE = re.compile('(YYY?Y?|MM?M?M?|Do|DD?D?D?|d?d?d?d|HH?|hh?|mm?|ss?|S+|ZZ?Z?|a|A|X)')
    _ESCAPE_RE = re.compile('\[[^\[\]]*\]')

    _ONE_OR_MORE_DIGIT_RE = re.compile('\d+')
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
        'S': _ONE_OR_MORE_DIGIT_RE,
    }

    MARKERS = ['YYYY', 'MM', 'DD']
    SEPARATORS = ['-', '/', '.']

    def __init__(self, locale='en_us', cache_size=0):

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
            'd': re.compile(r"[1-7]"),
            'a': self._choice_re(
                (self.locale.meridians['am'], self.locale.meridians['pm'])
            ),
            # note: 'A' token accepts both 'am/pm' and 'AM/PM' formats to
            # ensure backwards compatibility of this token
            'A': self._choice_re(self.locale.meridians.values())
        })
        if cache_size > 0:
            self._generate_pattern_re =\
                lru_cache(maxsize=cache_size)(self._generate_pattern_re)

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
            has_subseconds = re.search('[.,]', time_parts[0])

            if has_subseconds:
                formats = ['YYYY-MM-DDTHH:mm:ss%sS' % has_subseconds.group()]
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

    def _generate_pattern_re(self, fmt):

        # fmt is a string of tokens like 'YYYY-MM-DD'
        # we construct a new string by replacing each
        # token by its pattern:
        # 'YYYY-MM-DD' -> '(?P<YYYY>\d{4})-(?P<MM>\d{2})-(?P<DD>\d{2})'
        tokens = []
        offset = 0

        # Escape all special RegEx chars
        escaped_fmt = re.escape(fmt)

        # Extract the bracketed expressions to be reinserted later.
        escaped_fmt = re.sub(self._ESCAPE_RE, "#", escaped_fmt)
        # Any number of S is the same as one.
        escaped_fmt = re.sub('S+', 'S', escaped_fmt)
        escaped_data = re.findall(self._ESCAPE_RE, fmt)

        fmt_pattern = escaped_fmt

        for m in self._FORMAT_RE.finditer(escaped_fmt):
            token = m.group(0)
            try:
                input_re = self._input_re_map[token]
            except KeyError:
                raise ParserError('Unrecognized token \'{}\''.format(token))
            input_pattern = '(?P<{}>{})'.format(token, input_re.pattern)
            tokens.append(token)
            # a pattern doesn't have the same length as the token
            # it replaces! We keep the difference in the offset variable.
            # This works because the string is scanned left-to-right and matches
            # are returned in the order found by finditer.
            fmt_pattern = fmt_pattern[:m.start() + offset] + input_pattern + fmt_pattern[m.end() + offset:]
            offset += len(input_pattern) - (m.end() - m.start())

        final_fmt_pattern = ""
        a = fmt_pattern.split("\#")
        b = escaped_data

        # Due to the way Python splits, 'a' will always be longer
        for i in range(len(a)):
            final_fmt_pattern += a[i]
            if i < len(b):
                final_fmt_pattern += b[i][1:-1]

        return tokens, re.compile(final_fmt_pattern, flags=re.IGNORECASE)

    def parse(self, string, fmt):

        if isinstance(fmt, list):
            return self._parse_multiformat(string, fmt)

        fmt_tokens, fmt_pattern_re = self._generate_pattern_re(fmt)

        match = fmt_pattern_re.search(string)
        if match is None:
            raise ParserError('Failed to match \'{}\' when parsing \'{}\''
                              .format(fmt_pattern_re.pattern, string))
        parts = {}
        for token in fmt_tokens:
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

        elif token == 'S':
            # We have the *most significant* digits of an arbitrary-precision integer.
            # We want the six most significant digits as an integer, rounded.
            # FIXME: add nanosecond support somehow?
            value = value.ljust(7, str('0'))

            # floating-point (IEEE-754) defaults to half-to-even rounding
            seventh_digit = int(value[6])
            if seventh_digit == 5:
                rounding = int(value[5]) % 2
            elif seventh_digit > 5:
                rounding = 1
            else:
                rounding = 0

            parts['microsecond'] = int(value[:6]) + rounding

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
            except ParserError:
                pass

        if _datetime is None:
            raise ParserError('Could not match input to any of {} on \'{}\''.format(formats, string))

        return _datetime

    @staticmethod
    def _map_lookup(input_map, key):

        try:
            return input_map[key]
        except KeyError:
            raise ParserError('Could not match "{}" to {}'.format(key, input_map))

    @staticmethod
    def _try_timestamp(string):

        try:
            return float(string)
        except:
            return None

    @staticmethod
    def _choice_re(choices, flags=0):
        return re.compile('({})'.format('|'.join(choices)), flags=flags)


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
            raise ParserError('Could not parse timezone expression "{}"'.format(string))

        return tzinfo
