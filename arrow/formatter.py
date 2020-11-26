import re

from dateutil import tz as dateutil_tz

from arrow import locales

FORMAT_ATOM = "YYYY-MM-DD HH:mm:ssZZ"
FORMAT_COOKIE = "dddd, DD-MMM-YYYY HH:mm:ss ZZZ"
FORMAT_RFC822 = "ddd, DD MMM YY HH:mm:ss Z"
FORMAT_RFC850 = "dddd, DD-MMM-YY HH:mm:ss ZZZ"
FORMAT_RFC1036 = "ddd, DD MMM YY HH:mm:ss Z"
FORMAT_RFC1123 = "ddd, DD MMM YYYY HH:mm:ss Z"
FORMAT_RFC2822 = "ddd, DD MMM YYYY HH:mm:ss Z"
FORMAT_RFC3339 = "YYYY-MM-DD HH:mm:ssZZ"
FORMAT_RSS = "ddd, DD MMM YYYY HH:mm:ss Z"
FORMAT_W3C = "YYYY-MM-DD HH:mm:ssZZ"


class DateTimeFormatter:

    # This pattern matches characters enclosed in square brackets are matched as
    # an atomic group. For more info on atomic groups and how to they are
    # emulated in Python's re library, see https://stackoverflow.com/a/13577411/2701578

    _FORMAT_RE = re.compile(
        r"(\[(?:(?=(?P<literal>[^]]))(?P=literal))*\]|YYY?Y?|MM?M?M?|Do|DD?D?D?|d?dd?d?|HH?|hh?|mm?|ss?|SS?S?S?S?S?|ZZ?Z?|a|A|X|x|W)"
    )

    def __init__(self, locale="en_us"):

        self.locale = locales.get_locale(locale)

    def format(cls, dt, fmt):

        return cls._FORMAT_RE.sub(lambda m: cls._format_token(dt, m.group(0)), fmt)

    def _format_token(self, dt, token):

        if token and token.startswith("[") and token.endswith("]"):
            return token[1:-1]

        if token == "YYYY":
            return self.locale.year_full(dt.year)
        if token == "YY":
            return self.locale.year_abbreviation(dt.year)

        if token == "MMMM":
            return self.locale.month_name(dt.month)
        if token == "MMM":
            return self.locale.month_abbreviation(dt.month)
        if token == "MM":
            return f"{dt.month:02d}"
        if token == "M":
            return str(dt.month)

        if token == "DDDD":
            return f"{dt.timetuple().tm_yday:03d}"
        if token == "DDD":
            return str(dt.timetuple().tm_yday)
        if token == "DD":
            return f"{dt.day:02d}"
        if token == "D":
            return str(dt.day)

        if token == "Do":
            return self.locale.ordinal_number(dt.day)

        if token == "dddd":
            return self.locale.day_name(dt.isoweekday())
        if token == "ddd":
            return self.locale.day_abbreviation(dt.isoweekday())
        if token == "d":
            return str(dt.isoweekday())

        if token == "HH":
            return f"{dt.hour:02d}"
        if token == "H":
            return str(dt.hour)
        if token == "hh":
            return "{:02d}".format(dt.hour if 0 < dt.hour < 13 else abs(dt.hour - 12))
        if token == "h":
            return str(dt.hour if 0 < dt.hour < 13 else abs(dt.hour - 12))

        if token == "mm":
            return f"{dt.minute:02d}"
        if token == "m":
            return str(dt.minute)

        if token == "ss":
            return f"{dt.second:02d}"
        if token == "s":
            return str(dt.second)

        if token == "SSSSSS":
            return str("{:06d}".format(int(dt.microsecond)))
        if token == "SSSSS":
            return str("{:05d}".format(int(dt.microsecond / 10)))
        if token == "SSSS":
            return str("{:04d}".format(int(dt.microsecond / 100)))
        if token == "SSS":
            return str("{:03d}".format(int(dt.microsecond / 1000)))
        if token == "SS":
            return str("{:02d}".format(int(dt.microsecond / 10000)))
        if token == "S":
            return str(int(dt.microsecond / 100000))

        if token == "X":
            return str(dt.timestamp())

        if token == "x":
            return str(int(dt.timestamp() * 1000000))

        if token == "ZZZ":
            return dt.tzname()

        if token in ["ZZ", "Z"]:
            separator = ":" if token == "ZZ" else ""
            tz = dateutil_tz.tzutc() if dt.tzinfo is None else dt.tzinfo
            total_minutes = int(tz.utcoffset(dt).total_seconds() / 60)

            sign = "+" if total_minutes >= 0 else "-"
            total_minutes = abs(total_minutes)
            hour, minute = divmod(total_minutes, 60)

            return f"{sign}{hour:02d}{separator}{minute:02d}"

        if token in ("a", "A"):
            return self.locale.meridian(dt.hour, token)

        if token == "W":
            year, week, day = dt.isocalendar()
            return f"{year}-W{week:02d}-{day}"
