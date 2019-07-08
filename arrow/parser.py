# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import re
import warnings
from datetime import datetime

from dateutil import tz

from arrow import locales

try:
    from functools import lru_cache
except ImportError:  # pragma: no cover
    from backports.functools_lru_cache import lru_cache  # pragma: no cover


class ParserError(RuntimeError):
    pass


class GetParseWarning(DeprecationWarning):
    """Raised when arrow.get() is passed a string with no formats and matches incorrectly
    on one of the default formats.

    e.g.
    arrow.get('blabla2016') -> <Arrow [2016-01-01T00:00:00+00:00]>
    arrow.get('13/4/2045') -> <Arrow [2045-01-01T00:00:00+00:00]>

    In version 0.15.0 this warning will become a ParserError.
    """


warnings.simplefilter("default", GetParseWarning)


class DateTimeParser(object):

    _FORMAT_RE = re.compile(
        r"(YYY?Y?|MM?M?M?|Do|DD?D?D?|d?d?d?d|HH?|hh?|mm?|ss?|S+|ZZ?Z?|a|A|X)"
    )
    _ESCAPE_RE = re.compile(r"\[[^\[\]]*\]")

    _ONE_OR_MORE_DIGIT_RE = re.compile(r"\d+")
    _ONE_OR_TWO_DIGIT_RE = re.compile(r"\d{1,2}")
    _FOUR_DIGIT_RE = re.compile(r"\d{4}")
    _TWO_DIGIT_RE = re.compile(r"\d{2}")
    _TZ_RE = re.compile(r"[+\-]?\d{2}:?(\d{2})?|Z")
    _TZ_NAME_RE = re.compile(r"\w[\w+\-/]+")
    _TIMESTAMP_RE = re.compile(r"\d+")

    _BASE_INPUT_RE_MAP = {
        "YYYY": _FOUR_DIGIT_RE,
        "YY": _TWO_DIGIT_RE,
        "MM": _TWO_DIGIT_RE,
        "M": _ONE_OR_TWO_DIGIT_RE,
        "DD": _TWO_DIGIT_RE,
        "D": _ONE_OR_TWO_DIGIT_RE,
        "HH": _TWO_DIGIT_RE,
        "H": _ONE_OR_TWO_DIGIT_RE,
        "hh": _TWO_DIGIT_RE,
        "h": _ONE_OR_TWO_DIGIT_RE,
        "mm": _TWO_DIGIT_RE,
        "m": _ONE_OR_TWO_DIGIT_RE,
        "ss": _TWO_DIGIT_RE,
        "s": _ONE_OR_TWO_DIGIT_RE,
        "X": _TIMESTAMP_RE,
        "ZZZ": _TZ_NAME_RE,
        "ZZ": _TZ_RE,
        "Z": _TZ_RE,
        "S": _ONE_OR_MORE_DIGIT_RE,
    }

    SEPARATORS = ["-", "/", "."]

    def __init__(self, locale="en_us", cache_size=0):

        self.locale = locales.get_locale(locale)
        self._input_re_map = self._BASE_INPUT_RE_MAP.copy()
        self._input_re_map.update(
            {
                "MMMM": self._choice_re(self.locale.month_names[1:], re.IGNORECASE),
                "MMM": self._choice_re(
                    self.locale.month_abbreviations[1:], re.IGNORECASE
                ),
                "Do": re.compile(self.locale.ordinal_day_re),
                "dddd": self._choice_re(self.locale.day_names[1:], re.IGNORECASE),
                "ddd": self._choice_re(
                    self.locale.day_abbreviations[1:], re.IGNORECASE
                ),
                "d": re.compile(r"[1-7]"),
                "a": self._choice_re(
                    (self.locale.meridians["am"], self.locale.meridians["pm"])
                ),
                # note: 'A' token accepts both 'am/pm' and 'AM/PM' formats to
                # ensure backwards compatibility of this token
                "A": self._choice_re(self.locale.meridians.values()),
            }
        )
        if cache_size > 0:
            self._generate_pattern_re = lru_cache(maxsize=cache_size)(
                self._generate_pattern_re
            )

    # TODO: since we support more than ISO-8601, we should rename this function
    def parse_iso(self, string):
        # TODO: account for more than 1 space like arrow.get("     2016")
        # string = string.strip()

        has_space_divider = " " in string and len(string.strip().split(" ")) == 2

        has_time = "T" in string or has_space_divider
        space_divider = " " in string.strip()

        has_tz = False

        if has_time:
            if space_divider:
                date_string, time_string = string.split(" ", 1)
            else:
                date_string, time_string = string.split("T", 1)

            # TODO: understand why we are not accounting for Z directly
            # currently Z is ignored entirely but fromdatetime defaults to UTC, see arrow.py L196
            # '2013-02-03T04:05:06.78912Z'
            time_parts = re.split("[+-]", time_string, 1)
            colon_count = time_parts[0].count(":")

            # TODO "20160504T010203Z" parses incorrectly, time part is HH only, due to Z changing len
            is_basic_time_format = colon_count == 0

            has_tz = len(time_parts) > 1
            has_hours = len(time_string) == 2
            has_minutes = colon_count == 1 or len(time_string) == 4
            has_seconds = colon_count == 2 or len(time_string) == 6
            has_subseconds = re.search("[.,]", time_parts[0])

            if has_subseconds:
                time_string = "HH:mm:ss{}S".format(has_subseconds.group())
            elif has_seconds:
                time_string = "HH:mm:ss"
            elif has_minutes:
                time_string = "HH:mm"
            elif has_hours:
                time_string = "HH"
            else:
                # TODO: add tests for new conditional cases
                raise ValueError("No valid time component provided.")

            if is_basic_time_format:
                time_string = time_string.replace(":", "")

        # IDEA reduced set of date formats for basic

        # TODO: add tests for all the new formats, especially basic format
        # required date formats to test against
        formats = [
            "YYYY-MM-DD",
            "YYYY-M-DD",
            "YYYY-M-D",
            "YYYY/MM/DD",
            "YYYY/M/DD",
            "YYYY/M/D",
            "YYYY.MM.DD",
            "YYYY.M.DD",
            "YYYY.M.D",
            "YYYYMMDD",
            "YYYY-MM",
            "YYYY/MM",
            "YYYY.MM",
            "YYYY",
            # "YY", this is not a good format to try by default?
        ]

        if has_time:
            formats = ["{}T{}".format(f, time_string) for f in formats]

        if has_time and has_tz:
            # Add "Z" to format strings to indicate to _parse_tokens
            # that a timezone needs to be parsed
            formats = ["{}Z".format(f) for f in formats]

        if space_divider:
            formats = [item.replace("T", " ", 1) for item in formats]

        return self._parse_multiformat(string, formats, True)

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
        escaped_fmt = re.sub("S+", "S", escaped_fmt)
        escaped_data = re.findall(self._ESCAPE_RE, fmt)

        fmt_pattern = escaped_fmt

        for m in self._FORMAT_RE.finditer(escaped_fmt):
            token = m.group(0)
            try:
                input_re = self._input_re_map[token]
            except KeyError:
                raise ParserError("Unrecognized token '{}'".format(token))
            input_pattern = "(?P<{}>{})".format(token, input_re.pattern)
            tokens.append(token)
            # a pattern doesn't have the same length as the token
            # it replaces! We keep the difference in the offset variable.
            # This works because the string is scanned left-to-right and matches
            # are returned in the order found by finditer.
            fmt_pattern = (
                fmt_pattern[: m.start() + offset]
                + input_pattern
                + fmt_pattern[m.end() + offset :]
            )
            offset += len(input_pattern) - (m.end() - m.start())

        final_fmt_pattern = ""
        split_fmt = fmt_pattern.split(r"\#")

        # Due to the way Python splits, 'split_fmt' will always be longer
        for i in range(len(split_fmt)):
            final_fmt_pattern += split_fmt[i]
            if i < len(escaped_data):
                final_fmt_pattern += escaped_data[i][1:-1]

        # Wrap final_fmt_pattern in a custom word boundary to strictly
        # match the formatting pattern and filter out date and time formats
        # that include junk such as: blah1998-09-12 blah, blah 1998-09-12blah,
        # blah1998-09-12blah. The custom word boundary matches every character
        # that is not a whitespace character to allow for searching for a date
        # and time string in a natural language sentence. Therefore, searching
        # for a string of the form YYYY-MM-DD in "blah 1998-09-12 blah" will
        # work properly.
        # Reference: https://stackoverflow.com/q/14232931/3820660
        starting_word_boundary = r"(?<![\S])"
        ending_word_boundary = r"(?![\S])"
        final_fmt_pattern = r"{}{}Z?{}".format(
            starting_word_boundary, final_fmt_pattern, ending_word_boundary
        )

        return tokens, re.compile(final_fmt_pattern, flags=re.IGNORECASE)

    def parse(self, string, fmt, from_parse_iso=False):

        if isinstance(fmt, list):
            return self._parse_multiformat(string, fmt)

        fmt_tokens, fmt_pattern_re = self._generate_pattern_re(fmt)

        match = fmt_pattern_re.search(string)
        if match is None:
            raise ParserError(
                "Failed to match '{}' when parsing '{}'".format(
                    fmt_pattern_re.pattern, string
                )
            )

        parts = {}
        for token in fmt_tokens:
            if token == "Do":
                value = match.group("value")
            else:
                value = match.group(token)
            self._parse_token(token, value, parts)

        return self._build_datetime(parts)

    def _parse_token(self, token, value, parts):

        if token == "YYYY":
            parts["year"] = int(value)

        elif token == "YY":
            value = int(value)
            parts["year"] = 1900 + value if value > 68 else 2000 + value

        elif token in ["MMMM", "MMM"]:
            parts["month"] = self.locale.month_number(value.lower())

        elif token in ["MM", "M"]:
            parts["month"] = int(value)

        elif token in ["DD", "D"]:
            parts["day"] = int(value)

        elif token in ["Do"]:
            parts["day"] = int(value)

        elif token.upper() in ["HH", "H"]:
            parts["hour"] = int(value)

        elif token in ["mm", "m"]:
            parts["minute"] = int(value)

        elif token in ["ss", "s"]:
            parts["second"] = int(value)

        elif token == "S":
            # We have the *most significant* digits of an arbitrary-precision integer.
            # We want the six most significant digits as an integer, rounded.
            # FIXME: add nanosecond support somehow?
            value = value.ljust(7, str("0"))

            # floating-point (IEEE-754) defaults to half-to-even rounding
            seventh_digit = int(value[6])
            if seventh_digit == 5:
                rounding = int(value[5]) % 2
            elif seventh_digit > 5:
                rounding = 1
            else:
                rounding = 0

            parts["microsecond"] = int(value[:6]) + rounding

        elif token == "X":
            parts["timestamp"] = int(value)

        elif token in ["ZZZ", "ZZ", "Z"]:
            parts["tzinfo"] = TzinfoParser.parse(value)

        elif token in ["a", "A"]:
            if value in (self.locale.meridians["am"], self.locale.meridians["AM"]):
                parts["am_pm"] = "am"
            elif value in (self.locale.meridians["pm"], self.locale.meridians["PM"]):
                parts["am_pm"] = "pm"

    @staticmethod
    def _build_datetime(parts):

        timestamp = parts.get("timestamp")

        if timestamp:
            tz_utc = tz.tzutc()
            return datetime.fromtimestamp(timestamp, tz=tz_utc)

        am_pm = parts.get("am_pm")
        hour = parts.get("hour", 0)

        if am_pm == "pm" and hour < 12:
            hour += 12
        elif am_pm == "am" and hour == 12:
            hour = 0

        return datetime(
            year=parts.get("year", 1),
            month=parts.get("month", 1),
            day=parts.get("day", 1),
            hour=hour,
            minute=parts.get("minute", 0),
            second=parts.get("second", 0),
            microsecond=parts.get("microsecond", 0),
            tzinfo=parts.get("tzinfo"),
        )

    def _parse_multiformat(self, string, formats, from_parse_iso=False):

        _datetime = None

        for fmt in formats:
            try:
                _datetime = self.parse(string, fmt, from_parse_iso)
                break
            except ParserError:
                pass

        if _datetime is None:
            raise ParserError(
                "Could not match input '{}' to any of the supported formats: {}".format(
                    string, ", ".join(formats)
                )
            )

        return _datetime

    @staticmethod
    def _choice_re(choices, flags=0):
        return re.compile(r"({})".format("|".join(choices)), flags=flags)


class TzinfoParser(object):

    _TZINFO_RE = re.compile(r"([+\-])?(\d\d):?(\d\d)?")

    @classmethod
    def parse(cls, string):

        tzinfo = None

        if string == "local":
            tzinfo = tz.tzlocal()

        elif string in ["utc", "UTC", "Z"]:
            tzinfo = tz.tzutc()

        else:

            iso_match = cls._TZINFO_RE.match(string)

            if iso_match:
                sign, hours, minutes = iso_match.groups()
                if minutes is None:
                    minutes = 0
                seconds = int(hours) * 3600 + int(minutes) * 60

                if sign == "-":
                    seconds *= -1

                tzinfo = tz.tzoffset(None, seconds)

            else:
                tzinfo = tz.gettz(string)

        if tzinfo is None:
            raise ParserError('Could not parse timezone expression "{}"'.format(string))

        return tzinfo
