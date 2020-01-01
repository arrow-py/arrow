# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import re
from datetime import datetime, timedelta

from dateutil import tz

from arrow import locales
from arrow.constants import MAX_TIMESTAMP, MAX_TIMESTAMP_MS, MAX_TIMESTAMP_US

try:
    from functools import lru_cache
except ImportError:  # pragma: no cover
    from backports.functools_lru_cache import lru_cache  # pragma: no cover


class ParserError(ValueError):
    pass


# Allows for ParserErrors to be propagated from _build_datetime()
# when day_of_year errors occur.
# Before this, the ParserErrors were caught by the try/except in
# _parse_multiformat() and the appropriate error message was not
# transmitted to the user.
class ParserMatchError(ParserError):
    pass


class DateTimeParser(object):

    _FORMAT_RE = re.compile(
        r"(YYY?Y?|MM?M?M?|Do|DD?D?D?|d?d?d?d|HH?|hh?|mm?|ss?|S+|ZZ?Z?|a|A|x|X)"
    )
    _ESCAPE_RE = re.compile(r"\[[^\[\]]*\]")

    _ONE_OR_TWO_DIGIT_RE = re.compile(r"\d{1,2}")
    _ONE_OR_TWO_OR_THREE_DIGIT_RE = re.compile(r"\d{1,3}")
    _ONE_OR_MORE_DIGIT_RE = re.compile(r"\d+")
    _TWO_DIGIT_RE = re.compile(r"\d{2}")
    _THREE_DIGIT_RE = re.compile(r"\d{3}")
    _FOUR_DIGIT_RE = re.compile(r"\d{4}")
    _TZ_Z_RE = re.compile(r"([\+\-])(\d{2})(?:(\d{2}))?|Z")
    _TZ_ZZ_RE = re.compile(r"([\+\-])(\d{2})(?:\:(\d{2}))?|Z")
    _TZ_NAME_RE = re.compile(r"\w[\w+\-/]+")
    # NOTE: timestamps cannot be parsed from natural language strings (by removing the ^...$) because it will
    # break cases like "15 Jul 2000" and a format list (see issue #447)
    _TIMESTAMP_RE = re.compile(r"^\-?\d+\.?\d+$")
    _TIMESTAMP_EXPANDED_RE = re.compile(r"^\-?\d+$")
    _TIME_RE = re.compile(r"^(\d{2})(?:\:?(\d{2}))?(?:\:?(\d{2}))?(?:([\.\,])(\d+))?$")

    _BASE_INPUT_RE_MAP = {
        "YYYY": _FOUR_DIGIT_RE,
        "YY": _TWO_DIGIT_RE,
        "MM": _TWO_DIGIT_RE,
        "M": _ONE_OR_TWO_DIGIT_RE,
        "DDDD": _THREE_DIGIT_RE,
        "DDD": _ONE_OR_TWO_OR_THREE_DIGIT_RE,
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
        "x": _TIMESTAMP_EXPANDED_RE,
        "ZZZ": _TZ_NAME_RE,
        "ZZ": _TZ_ZZ_RE,
        "Z": _TZ_Z_RE,
        "S": _ONE_OR_MORE_DIGIT_RE,
    }

    SEPARATORS = ["-", "/", "."]

    def __init__(self, locale="en_us", cache_size=0):

        self.locale = locales.get_locale(locale)
        self._input_re_map = self._BASE_INPUT_RE_MAP.copy()
        self._input_re_map.update(
            {
                "MMMM": self._generate_choice_re(
                    self.locale.month_names[1:], re.IGNORECASE
                ),
                "MMM": self._generate_choice_re(
                    self.locale.month_abbreviations[1:], re.IGNORECASE
                ),
                "Do": re.compile(self.locale.ordinal_day_re),
                "dddd": self._generate_choice_re(
                    self.locale.day_names[1:], re.IGNORECASE
                ),
                "ddd": self._generate_choice_re(
                    self.locale.day_abbreviations[1:], re.IGNORECASE
                ),
                "d": re.compile(r"[1-7]"),
                "a": self._generate_choice_re(
                    (self.locale.meridians["am"], self.locale.meridians["pm"])
                ),
                # note: 'A' token accepts both 'am/pm' and 'AM/PM' formats to
                # ensure backwards compatibility of this token
                "A": self._generate_choice_re(self.locale.meridians.values()),
            }
        )
        if cache_size > 0:
            self._generate_pattern_re = lru_cache(maxsize=cache_size)(
                self._generate_pattern_re
            )

    # TODO: since we support more than ISO 8601, we should rename this function
    # IDEA: break into multiple functions
    def parse_iso(self, datetime_string):
        # TODO: add a flag to normalize whitespace (useful in logs, ref issue #421)
        has_space_divider = " " in datetime_string
        has_t_divider = "T" in datetime_string

        num_spaces = datetime_string.count(" ")
        if has_space_divider and num_spaces != 1 or has_t_divider and num_spaces > 0:
            raise ParserError(
                "Expected an ISO 8601-like string, but was given '{}'. Try passing in a format string to resolve this.".format(
                    datetime_string
                )
            )

        has_time = has_space_divider or has_t_divider
        has_tz = False

        # date formats (ISO 8601 and others) to test against
        # NOTE: YYYYMM is omitted to avoid confusion with YYMMDD (no longer part of ISO 8601, but is still often used)
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
            "YYYY-DDDD",
            "YYYYDDDD",
            "YYYY-MM",
            "YYYY/MM",
            "YYYY.MM",
            "YYYY",
        ]

        if has_time:

            if has_space_divider:
                date_string, time_string = datetime_string.split(" ", 1)
            else:
                date_string, time_string = datetime_string.split("T", 1)

            time_parts = re.split(r"[\+\-Z]", time_string, 1, re.IGNORECASE)

            time_components = self._TIME_RE.match(time_parts[0])

            if time_components is None:
                raise ParserError(
                    "Invalid time component provided. Please specify a format or provide a valid time component in the basic or extended ISO 8601 time format."
                )

            (
                hours,
                minutes,
                seconds,
                subseconds_sep,
                subseconds,
            ) = time_components.groups()

            has_tz = len(time_parts) == 2
            has_minutes = minutes is not None
            has_seconds = seconds is not None
            has_subseconds = subseconds is not None

            is_basic_time_format = ":" not in time_parts[0]
            tz_format = "Z"

            # use 'ZZ' token instead since tz offset is present in non-basic format
            if has_tz and ":" in time_parts[1]:
                tz_format = "ZZ"

            time_sep = "" if is_basic_time_format else ":"

            if has_subseconds:
                time_string = "HH{time_sep}mm{time_sep}ss{subseconds_sep}S".format(
                    time_sep=time_sep, subseconds_sep=subseconds_sep
                )
            elif has_seconds:
                time_string = "HH{time_sep}mm{time_sep}ss".format(time_sep=time_sep)
            elif has_minutes:
                time_string = "HH{time_sep}mm".format(time_sep=time_sep)
            else:
                time_string = "HH"

            if has_space_divider:
                formats = ["{} {}".format(f, time_string) for f in formats]
            else:
                formats = ["{}T{}".format(f, time_string) for f in formats]

        if has_time and has_tz:
            # Add "Z" or "ZZ" to the format strings to indicate to
            # _parse_token() that a timezone needs to be parsed
            formats = ["{}{}".format(f, tz_format) for f in formats]

        return self._parse_multiformat(datetime_string, formats)

    def parse(self, datetime_string, fmt):

        if isinstance(fmt, list):
            return self._parse_multiformat(datetime_string, fmt)

        fmt_tokens, fmt_pattern_re = self._generate_pattern_re(fmt)

        match = fmt_pattern_re.search(datetime_string)

        if match is None:
            raise ParserMatchError(
                "Failed to match '{}' when parsing '{}'".format(fmt, datetime_string)
            )

        parts = {}
        for token in fmt_tokens:
            if token == "Do":
                value = match.group("value")
            else:
                value = match.group(token)
            self._parse_token(token, value, parts)

        return self._build_datetime(parts)

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
        # TODO: allow users to specify the number of digits to parse
        escaped_fmt = re.sub(r"S+", "S", escaped_fmt)

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
        # Certain punctuation before or after the target pattern such as
        # "1998-09-12," is permitted. For the full list of valid punctuation,
        # see the documentation.

        starting_word_boundary = (
            r"(?<!\S\S)"  # Don't have two consecutive non-whitespace characters. This ensures that we allow cases like .11.25.2019 but not 1.11.25.2019 (for pattern MM.DD.YYYY)
            r"(?<![^\,\.\;\:\?\!\"\'\`\[\]\{\}\(\)<>\s])"  # This is the list of punctuation that is ok before the pattern (i.e. "It can't not be these characters before the pattern")
            r"(\b|^)"  # The \b is to block cases like 1201912 but allow 201912 for pattern YYYYMM. The ^ was necessary to allow a negative number through i.e. before epoch numbers
        )
        ending_word_boundary = (
            r"(?=[\,\.\;\:\?\!\"\'\`\[\]\{\}\(\)\<\>]?"  # Positive lookahead stating that these punctuation marks can appear after the pattern at most 1 time
            r"(?!\S))"  # Don't allow any non-whitespace character after the punctuation
        )
        bounded_fmt_pattern = r"{}{}{}".format(
            starting_word_boundary, final_fmt_pattern, ending_word_boundary
        )

        return tokens, re.compile(bounded_fmt_pattern, flags=re.IGNORECASE)

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

        elif token in ["DDDD", "DDD"]:
            parts["day_of_year"] = int(value)

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
            # IDEA: add nanosecond support somehow? Need datetime support for it first.
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
            parts["timestamp"] = float(value)

        elif token == "x":
            parts["expanded_timestamp"] = int(value)

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

        if timestamp is not None:
            return datetime.fromtimestamp(timestamp, tz=tz.tzutc())

        expanded_timestamp = parts.get("expanded_timestamp")

        if expanded_timestamp is not None:

            if expanded_timestamp > MAX_TIMESTAMP:
                if expanded_timestamp < MAX_TIMESTAMP_MS:
                    expanded_timestamp /= 1000.0
                elif expanded_timestamp < MAX_TIMESTAMP_US:
                    expanded_timestamp /= 1000000.0
                else:
                    raise ValueError(
                        "The specified timestamp '{}' is too large.".format(
                            expanded_timestamp
                        )
                    )

            return datetime.fromtimestamp(expanded_timestamp, tz=tz.tzutc())

        day_of_year = parts.get("day_of_year")

        if day_of_year is not None:
            year = parts.get("year")
            month = parts.get("month")
            if year is None:
                raise ParserError(
                    "Year component is required with the DDD and DDDD tokens."
                )

            if month is not None:
                raise ParserError(
                    "Month component is not allowed with the DDD and DDDD tokens."
                )

            date_string = "{}-{}".format(year, day_of_year)
            try:
                dt = datetime.strptime(date_string, "%Y-%j")
            except ValueError:
                raise ParserError(
                    "The provided day of year '{}' is invalid.".format(day_of_year)
                )

            parts["year"] = dt.year
            parts["month"] = dt.month
            parts["day"] = dt.day

        am_pm = parts.get("am_pm")
        hour = parts.get("hour", 0)

        if am_pm == "pm" and hour < 12:
            hour += 12
        elif am_pm == "am" and hour == 12:
            hour = 0

        # Support for midnight at the end of day
        if hour == 24:
            if parts.get("minute", 0) != 0:
                raise ParserError("Midnight at the end of day must not contain minutes")
            if parts.get("second", 0) != 0:
                raise ParserError("Midnight at the end of day must not contain seconds")
            if parts.get("microsecond", 0) != 0:
                raise ParserError(
                    "Midnight at the end of day must not contain microseconds"
                )
            hour = 0
            day_increment = 1
        else:
            day_increment = 0

        # account for rounding up to 1000000
        microsecond = parts.get("microsecond", 0)
        if microsecond == 1000000:
            microsecond = 0
            second_increment = 1
        else:
            second_increment = 0

        increment = timedelta(days=day_increment, seconds=second_increment)

        return (
            datetime(
                year=parts.get("year", 1),
                month=parts.get("month", 1),
                day=parts.get("day", 1),
                hour=hour,
                minute=parts.get("minute", 0),
                second=parts.get("second", 0),
                microsecond=microsecond,
                tzinfo=parts.get("tzinfo"),
            )
            + increment
        )

    def _parse_multiformat(self, string, formats):

        _datetime = None

        for fmt in formats:
            try:
                _datetime = self.parse(string, fmt)
                break
            except ParserMatchError:
                pass

        if _datetime is None:
            raise ParserError(
                "Could not match input '{}' to any of the following formats: {}".format(
                    string, ", ".join(formats)
                )
            )

        return _datetime

    # generates a capture group of choices separated by an OR operator
    @staticmethod
    def _generate_choice_re(choices, flags=0):
        return re.compile(r"({})".format("|".join(choices)), flags=flags)


class TzinfoParser(object):
    _TZINFO_RE = re.compile(r"^([\+\-])?(\d{2})(?:\:?(\d{2}))?$")

    @classmethod
    def parse(cls, tzinfo_string):

        tzinfo = None

        if tzinfo_string == "local":
            tzinfo = tz.tzlocal()

        elif tzinfo_string in ["utc", "UTC", "Z"]:
            tzinfo = tz.tzutc()

        else:

            iso_match = cls._TZINFO_RE.match(tzinfo_string)

            if iso_match:
                sign, hours, minutes = iso_match.groups()
                if minutes is None:
                    minutes = 0
                seconds = int(hours) * 3600 + int(minutes) * 60

                if sign == "-":
                    seconds *= -1

                tzinfo = tz.tzoffset(None, seconds)

            else:
                tzinfo = tz.gettz(tzinfo_string)

        if tzinfo is None:
            raise ParserError(
                'Could not parse timezone expression "{}"'.format(tzinfo_string)
            )

        return tzinfo
