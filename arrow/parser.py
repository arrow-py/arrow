# -*- coding: utf-8 -*-
from __future__ import absolute_import

from datetime import datetime
from dateutil import tz

import calendar
import re

from arrow import locales


class ParserError(RuntimeError):
    pass


class DateTimeParser(object):

    _FORMAT_RE = re.compile('(YYY?Y?|MM?M?M?|DD?D?D?|HH?|hh?|mm?|ss?|SS?S?S?S?S?|ZZ?|a|A|X)')

    _ONE_THROUGH_SIX_DIGIT_RE = re.compile('\d{1,6}')
    _ONE_THROUGH_FIVE_DIGIT_RE = re.compile('\d{1,5}')
    _ONE_THROUGH_FOUR_DIGIT_RE = re.compile('\d{1,4}')
    _ONE_TWO_OR_THREE_DIGIT_RE = re.compile('\d{1,3}')
    _ONE_OR_TWO_DIGIT_RE = re.compile('\d{1,2}')
    _FOUR_DIGIT_RE = re.compile('\d{4}')
    _TWO_DIGIT_RE = re.compile('\d{2}')
    _TZ_RE = re.compile('[+\-]?\d{2}:?\d{2}')

    _INPUT_RE_MAP = {
        'YYYY': _FOUR_DIGIT_RE,
        'YY': _TWO_DIGIT_RE,
        'MMMM': re.compile('({0})'.format('|'.join(calendar.month_name[1:]))),
        'MMM': re.compile('({0})'.format('|'.join(calendar.month_abbr[1:]))),
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
        'a': re.compile('(a|A|p|P)'),
        'A': re.compile('(am|AM|pm|PM)'),
        'X': re.compile('\d+'),
        'ZZ': _TZ_RE,
        'Z': _TZ_RE,
        'SSSSSS': _ONE_THROUGH_SIX_DIGIT_RE,
        'SSSSS': _ONE_THROUGH_FIVE_DIGIT_RE,
        'SSSS': _ONE_THROUGH_FOUR_DIGIT_RE,
        'SSS': _ONE_TWO_OR_THREE_DIGIT_RE,
        'SS': _ONE_OR_TWO_DIGIT_RE,
        'S': re.compile('\d'),
    }

    def __init__(self, locale='en_us'):

        self.locale = locales.get_locale(locale)

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

        else:
            has_tz = has_seconds = has_subseconds = False

        if has_time:

            if has_subseconds:
                formats = ['YYYY-MM-DDTHH:mm:ss.SSSSSS']
            elif has_seconds:
                formats = ['YYYY-MM-DDTHH:mm:ss']
            else:
                formats = ['YYYY-MM-DDTHH:mm']

        else:
            formats = [
                'YYYY-MM-DD',
                'YYYY-MM',
                'YYYY',
            ]

        if has_time and has_tz:
            formats = [f + 'Z' for f in formats]

        if space_divider:
            formats = [item.replace('T', ' ', 1) for item in formats]

        return self._parse_multiformat(string, formats)

    def parse(self, string, fmt):

        if isinstance(fmt, list):
            return self._parse_multiformat(string, fmt)

        original_string = string
        tokens = self._FORMAT_RE.findall(fmt)
        token_values = []
        separators = self._parse_separators(fmt, tokens)
        parts = {}

        for token in tokens:

            try:
                input_re = self._INPUT_RE_MAP[token]
            except KeyError:
                raise ParserError('Unrecognized token \'{0}\''.format(token))

            match = input_re.search(string)

            if match:

                token_values.append(match.group(0))
                self._parse_token(token, match.group(0), parts)

                index = match.span(0)[1]
                string = string[index:]

            else:
                raise ParserError('Failed to match token \'{0}\' when parsing \'{1}\''.format(token, original_string))

        parsed = ''.join(self._interleave_lists(token_values, separators))
        if parsed not in original_string:
            raise ParserError('Failed to match format \'{0}\' when parsing \'{1}\''.format(fmt, original_string))

        return self._build_datetime(parts)

    def _interleave_lists(self, tokens, separators):

        joined = tokens + separators
        joined[::2] = tokens
        joined[1::2] = separators

        return joined

    def _parse_separators(self, fmt, tokens):

        separators = []

        for i in range(len(tokens) - 1):
            start_index = fmt.find(tokens[i]) + len(tokens[i])
            end_index = fmt.find(tokens[i + 1])
            separators.append(fmt[start_index:end_index])

        return separators

    def _parse_token(self, token, value, parts):

        if token == 'YYYY':
            parts['year'] = int(value)
        elif token == 'YY':
            value = int(value)
            parts['year'] = 1900 + value if value > 68 else 2000 + value

        elif token in ['MMMM', 'MMM']:
            parts['month'] = self.locale.month_number(value)
        elif token in ['MM', 'M']:
            parts['month'] = int(value)

        elif token in ['DD', 'D']:
            parts['day'] = int(value)

        elif token in ['HH', 'H']:
            parts['hour'] = int(value)

        elif token in ['mm', 'm']:
            parts['minute'] = int(value)

        elif token in ['ss', 's']:
            parts['second'] = int(value)

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

        elif token in ['ZZ', 'Z']:
            parts['tzinfo'] = TzinfoParser.parse(value)

        elif token in ['a', 'A']:
            if value in ['a', 'A', 'am', 'AM']:
                parts['am_pm'] = 'am'
            elif value in ['p', 'P', 'pm', 'PM']:
                parts['am_pm'] = 'pm'

    @classmethod
    def _build_datetime(cls, parts):

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

    @classmethod
    def _map_lookup(cls, input_map, key):

        try:
            return input_map[key]
        except KeyError:
            raise ParserError('Could not match "{0}" to {1}'.format(key, input_map))

    @classmethod
    def _try_timestamp(cls, string):

        try:
            return float(string)
        except:
            return None


class TzinfoParser(object):

    _TZINFO_RE = re.compile('([+\-])?(\d\d):?(\d\d)')

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
                seconds = int(hours) * 3600 + int(minutes) * 60

                if sign == '-':
                    seconds *= -1

                tzinfo = tz.tzoffset(None, seconds)

            else:
                tzinfo = tz.gettz(string)

        if tzinfo is None:
            raise ParserError('Could not parse timezone expression "{0}"', string)

        return tzinfo
