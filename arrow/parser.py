# -*- coding: utf-8 -*-
from __future__ import absolute_import

from datetime import datetime
from dateutil import tz

from arrow.const import MONTH_VALUE_NAME_MAP, MONTH_VALUE_ABBR_MAP

import calendar
import re


class ParserError(RuntimeError):
    pass


class DateTimeParser(object):

    _FORMAT_RE = re.compile('(YYY?Y?|MM?M?M?|DD?D?D?|HH?|hh?|mm?|ss?|SS?S?|ZZ?|a|A|X)')

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
        'mm': _TWO_DIGIT_RE,
        'm': _ONE_OR_TWO_DIGIT_RE,
        'ss': _TWO_DIGIT_RE,
        's': _ONE_OR_TWO_DIGIT_RE,
        'a': re.compile('(a|A|p|P)'),
        'A': re.compile('(am|AM|pm|PM)'),
        'X': re.compile('\d+'),
        'ZZ': _TZ_RE,
        'Z': _TZ_RE,
        'SSS': _ONE_TWO_OR_THREE_DIGIT_RE,
        'SS': _ONE_OR_TWO_DIGIT_RE,
        'S': re.compile('\d'),
    }

    @classmethod
    def parse(cls, string, fmt):

        if isinstance(fmt, list):
            return cls._parse_multiformat(string, fmt)

        tokens = cls._FORMAT_RE.findall(fmt)
        parts = {}

        for token in tokens:

            try:
                input_re = cls._INPUT_RE_MAP[token]
            except KeyError:
                raise ParserError('Unrecognized token \'{0}\''.format(token))

            match = input_re.search(string)

            if match:

                try:
                    # TODO value is not used ?
                    value = cls._parse_token(token, match.group(0), parts)
                except:
                    raise ParserError('Failed to parse value \'{0}\' for token \'{1}\''.format(
                        match.group(0), token))

                index = match.span(0)[1]
                string = string[index:]

            else:
                raise ParserError('Failed to match token \'{0}\''.format(token))

        return cls._build_datetime(parts)

    @classmethod
    def _parse_token(cls, token, value, parts):

        if token == 'YYYY':
            parts['year'] = int(value)
        elif token == 'YY':
            value = int(value)
            parts['year'] = 2000 + value if value > 68 else 1900 + value

        elif token == 'MMMM':
            parts['month'] = cls._map_lookup(MONTH_VALUE_NAME_MAP, value)
        elif token == 'MMM':
            parts['month'] = cls._map_lookup(MONTH_VALUE_ABBR_MAP, value)
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
            return datetime.fromtimestamp(timestamp)

        am_pm = parts.get('am_pm')
        hour = parts.get('hour', 0)

        if am_pm == 'pm' and hour < 13:
            hour += 12

        return datetime(year=parts.get('year', 1), month=parts.get('month', 1),
            day=parts.get('day', 1), hour=hour, minute=parts.get('minute', 0),
            second=parts.get('second', 0), microsecond=parts.get('microsecond', 0),
            tzinfo=parts.get('tzinfo'))

    @classmethod
    def _parse_multiformat(cls, string, formats):

        _datetime = None

        for fmt in formats:
            try:
                _datetime = cls.parse(string, fmt)
                break
            except:
                pass

        if _datetime is None:
            raise ParserError('Could not match input to any of {0}'.format(formats))

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
