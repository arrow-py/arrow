"""Provides internationalization for arrow in over 60 languages and dialects."""

import sys
from math import trunc
from typing import (
    Any,
    ClassVar,
    Dict,
    List,
    Mapping,
    Optional,
    Sequence,
    Tuple,
    Type,
    Union,
    cast,
)

if sys.version_info < (3, 8):  # pragma: no cover
    from typing_extensions import Literal
else:
    from typing import Literal  # pragma: no cover

TimeFrameLiteral = Literal[
    "now",
    "second",
    "seconds",
    "minute",
    "minutes",
    "hour",
    "hours",
    "day",
    "days",
    "week",
    "weeks",
    "month",
    "months",
    "year",
    "years",
    "2-hours",
    "2-days",
    "2-weeks",
    "2-months",
    "2-years",
]

_TimeFrameElements = Union[
    str, Sequence[str], Mapping[str, str], Mapping[str, Sequence[str]]
]


_locale_map: Dict[str, Type["Locale"]] = dict()


def get_locale(name: str) -> "Locale":
    """Returns an appropriate :class:`Locale <arrow.locales.Locale>`
    corresponding to an input locale name.

    :param name: the name of the locale.

    """

    normalized_locale_name = name.lower().replace("_", "-")
    locale_cls = _locale_map.get(normalized_locale_name)

    if locale_cls is None:
        raise ValueError(f"Unsupported locale {normalized_locale_name!r}.")

    return locale_cls()


def get_locale_by_class_name(name: str) -> "Locale":
    """Returns an appropriate :class:`Locale <arrow.locales.Locale>`
    corresponding to an locale class name.

    :param name: the name of the locale class.

    """
    locale_cls: Optional[Type[Locale]] = globals().get(name)

    if locale_cls is None:
        raise ValueError(f"Unsupported locale {name!r}.")

    return locale_cls()


class Locale:
    """ Represents locale-specific data and functionality. """

    names: ClassVar[List[str]] = []

    timeframes: ClassVar[Mapping[TimeFrameLiteral, _TimeFrameElements]] = {
        "now": "",
        "second": "",
        "seconds": "",
        "minute": "",
        "minutes": "",
        "hour": "",
        "hours": "",
        "day": "",
        "days": "",
        "week": "",
        "weeks": "",
        "month": "",
        "months": "",
        "year": "",
        "years": "",
    }

    meridians: ClassVar[Dict[str, str]] = {"am": "", "pm": "", "AM": "", "PM": ""}

    past: ClassVar[str]
    future: ClassVar[str]
    and_word: ClassVar[Optional[str]] = None

    month_names: ClassVar[List[str]] = []
    month_abbreviations: ClassVar[List[str]] = []

    day_names: ClassVar[List[str]] = []
    day_abbreviations: ClassVar[List[str]] = []

    ordinal_day_re: ClassVar[str] = r"(\d+)"

    _month_name_to_ordinal: Optional[Dict[str, int]]

    def __init_subclass__(cls, **kwargs: Any) -> None:
        for locale_name in cls.names:
            if locale_name in _locale_map:
                raise LookupError(f"Duplicated locale name: {locale_name}")

            _locale_map[locale_name.lower().replace("_", "-")] = cls

    def __init__(self) -> None:

        self._month_name_to_ordinal = None

    def describe(
        self,
        timeframe: TimeFrameLiteral,
        delta: Union[float, int] = 0,
        only_distance: bool = False,
    ) -> str:
        """Describes a delta within a timeframe in plain language.

        :param timeframe: a string representing a timeframe.
        :param delta: a quantity representing a delta in a timeframe.
        :param only_distance: return only distance eg: "11 seconds" without "in" or "ago" keywords
        """

        humanized = self._format_timeframe(timeframe, delta)
        if not only_distance:
            humanized = self._format_relative(humanized, timeframe, delta)

        return humanized

    def describe_multi(
        self,
        timeframes: Sequence[Tuple[TimeFrameLiteral, Union[int, float]]],
        only_distance: bool = False,
    ) -> str:
        """Describes a delta within multiple timeframes in plain language.

        :param timeframes: a list of string, quantity pairs each representing a timeframe and delta.
        :param only_distance: return only distance eg: "2 hours and 11 seconds" without "in" or "ago" keywords
        """

        parts = [
            self._format_timeframe(timeframe, delta) for timeframe, delta in timeframes
        ]
        if self.and_word:
            parts.insert(-1, self.and_word)
        humanized = " ".join(parts)

        if not only_distance:
            humanized = self._format_relative(humanized, *timeframes[-1])

        return humanized

    def day_name(self, day: int) -> str:
        """Returns the day name for a specified day of the week.

        :param day: the ``int`` day of the week (1-7).

        """

        return self.day_names[day]

    def day_abbreviation(self, day: int) -> str:
        """Returns the day abbreviation for a specified day of the week.

        :param day: the ``int`` day of the week (1-7).

        """

        return self.day_abbreviations[day]

    def month_name(self, month: int) -> str:
        """Returns the month name for a specified month of the year.

        :param month: the ``int`` month of the year (1-12).

        """

        return self.month_names[month]

    def month_abbreviation(self, month: int) -> str:
        """Returns the month abbreviation for a specified month of the year.

        :param month: the ``int`` month of the year (1-12).

        """

        return self.month_abbreviations[month]

    def month_number(self, name: str) -> Optional[int]:
        """Returns the month number for a month specified by name or abbreviation.

        :param name: the month name or abbreviation.

        """

        if self._month_name_to_ordinal is None:
            self._month_name_to_ordinal = self._name_to_ordinal(self.month_names)
            self._month_name_to_ordinal.update(
                self._name_to_ordinal(self.month_abbreviations)
            )

        return self._month_name_to_ordinal.get(name)

    def year_full(self, year: int) -> str:
        """Returns the year for specific locale if available

        :param year: the ``int`` year (4-digit)
        """
        return f"{year:04d}"

    def year_abbreviation(self, year: int) -> str:
        """Returns the year for specific locale if available

        :param year: the ``int`` year (4-digit)
        """
        return f"{year:04d}"[2:]

    def meridian(self, hour: int, token: Any) -> Optional[str]:
        """Returns the meridian indicator for a specified hour and format token.

        :param hour: the ``int`` hour of the day.
        :param token: the format token.
        """

        if token == "a":
            return self.meridians["am"] if hour < 12 else self.meridians["pm"]
        if token == "A":
            return self.meridians["AM"] if hour < 12 else self.meridians["PM"]
        return None

    def ordinal_number(self, n: int) -> str:
        """Returns the ordinal format of a given integer

        :param n: an integer
        """
        return self._ordinal_number(n)

    def _ordinal_number(self, n: int) -> str:
        return f"{n}"

    def _name_to_ordinal(self, lst: Sequence[str]) -> Dict[str, int]:
        return {elem.lower(): i for i, elem in enumerate(lst[1:], 1)}

    def _format_timeframe(
        self, timeframe: TimeFrameLiteral, delta: Union[float, int]
    ) -> str:
        # TODO: remove cast
        return cast(str, self.timeframes[timeframe]).format(trunc(abs(delta)))

    def _format_relative(
        self,
        humanized: str,
        timeframe: TimeFrameLiteral,
        delta: Union[float, int],
    ) -> str:

        if timeframe == "now":
            return humanized

        direction = self.past if delta < 0 else self.future

        return direction.format(humanized)


class EnglishLocale(Locale):

    names = [
        "en",
        "en-us",
        "en-gb",
        "en-au",
        "en-be",
        "en-jp",
        "en-za",
        "en-ca",
        "en-ph",
    ]

    past = "{0} ago"
    future = "in {0}"
    and_word = "and"

    timeframes = {
        "now": "just now",
        "second": "a second",
        "seconds": "{0} seconds",
        "minute": "a minute",
        "minutes": "{0} minutes",
        "hour": "an hour",
        "hours": "{0} hours",
        "day": "a day",
        "days": "{0} days",
        "week": "a week",
        "weeks": "{0} weeks",
        "month": "a month",
        "months": "{0} months",
        "year": "a year",
        "years": "{0} years",
    }

    meridians = {"am": "am", "pm": "pm", "AM": "AM", "PM": "PM"}

    month_names = [
        "",
        "January",
        "February",
        "March",
        "April",
        "May",
        "June",
        "July",
        "August",
        "September",
        "October",
        "November",
        "December",
    ]
    month_abbreviations = [
        "",
        "Jan",
        "Feb",
        "Mar",
        "Apr",
        "May",
        "Jun",
        "Jul",
        "Aug",
        "Sep",
        "Oct",
        "Nov",
        "Dec",
    ]

    day_names = [
        "",
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
    ]
    day_abbreviations = ["", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

    ordinal_day_re = r"((?P<value>[2-3]?1(?=st)|[2-3]?2(?=nd)|[2-3]?3(?=rd)|[1-3]?[04-9](?=th)|1[1-3](?=th))(st|nd|rd|th))"

    def _ordinal_number(self, n: int) -> str:
        if n % 100 not in (11, 12, 13):
            remainder = abs(n) % 10
            if remainder == 1:
                return f"{n}st"
            elif remainder == 2:
                return f"{n}nd"
            elif remainder == 3:
                return f"{n}rd"
        return f"{n}th"

    def describe(
        self,
        timeframe: TimeFrameLiteral,
        delta: Union[int, float] = 0,
        only_distance: bool = False,
    ) -> str:
        """Describes a delta within a timeframe in plain language.

        :param timeframe: a string representing a timeframe.
        :param delta: a quantity representing a delta in a timeframe.
        :param only_distance: return only distance eg: "11 seconds" without "in" or "ago" keywords
        """

        humanized = super().describe(timeframe, delta, only_distance)
        if only_distance and timeframe == "now":
            humanized = "instantly"

        return humanized


class ItalianLocale(Locale):
    names = ["it", "it-it"]
    past = "{0} fa"
    future = "tra {0}"
    and_word = "e"

    timeframes = {
        "now": "adesso",
        "second": "un secondo",
        "seconds": "{0} qualche secondo",
        "minute": "un minuto",
        "minutes": "{0} minuti",
        "hour": "un'ora",
        "hours": "{0} ore",
        "day": "un giorno",
        "days": "{0} giorni",
        "week": "una settimana,",
        "weeks": "{0} settimane",
        "month": "un mese",
        "months": "{0} mesi",
        "year": "un anno",
        "years": "{0} anni",
    }

    month_names = [
        "",
        "gennaio",
        "febbraio",
        "marzo",
        "aprile",
        "maggio",
        "giugno",
        "luglio",
        "agosto",
        "settembre",
        "ottobre",
        "novembre",
        "dicembre",
    ]
    month_abbreviations = [
        "",
        "gen",
        "feb",
        "mar",
        "apr",
        "mag",
        "giu",
        "lug",
        "ago",
        "set",
        "ott",
        "nov",
        "dic",
    ]

    day_names = [
        "",
        "lunedì",
        "martedì",
        "mercoledì",
        "giovedì",
        "venerdì",
        "sabato",
        "domenica",
    ]
    day_abbreviations = ["", "lun", "mar", "mer", "gio", "ven", "sab", "dom"]

    ordinal_day_re = r"((?P<value>[1-3]?[0-9](?=[ºª]))[ºª])"

    def _ordinal_number(self, n: int) -> str:
        return f"{n}º"


class SpanishLocale(Locale):
    names = ["es", "es-es"]
    past = "hace {0}"
    future = "en {0}"
    and_word = "y"

    timeframes = {
        "now": "ahora",
        "second": "un segundo",
        "seconds": "{0} segundos",
        "minute": "un minuto",
        "minutes": "{0} minutos",
        "hour": "una hora",
        "hours": "{0} horas",
        "day": "un día",
        "days": "{0} días",
        "week": "una semana",
        "weeks": "{0} semanas",
        "month": "un mes",
        "months": "{0} meses",
        "year": "un año",
        "years": "{0} años",
    }

    meridians = {"am": "am", "pm": "pm", "AM": "AM", "PM": "PM"}

    month_names = [
        "",
        "enero",
        "febrero",
        "marzo",
        "abril",
        "mayo",
        "junio",
        "julio",
        "agosto",
        "septiembre",
        "octubre",
        "noviembre",
        "diciembre",
    ]
    month_abbreviations = [
        "",
        "ene",
        "feb",
        "mar",
        "abr",
        "may",
        "jun",
        "jul",
        "ago",
        "sep",
        "oct",
        "nov",
        "dic",
    ]

    day_names = [
        "",
        "lunes",
        "martes",
        "miércoles",
        "jueves",
        "viernes",
        "sábado",
        "domingo",
    ]
    day_abbreviations = ["", "lun", "mar", "mie", "jue", "vie", "sab", "dom"]

    ordinal_day_re = r"((?P<value>[1-3]?[0-9](?=[ºª]))[ºª])"

    def _ordinal_number(self, n: int) -> str:
        return f"{n}º"


class FrenchBaseLocale(Locale):

    past = "il y a {0}"
    future = "dans {0}"
    and_word = "et"

    timeframes = {
        "now": "maintenant",
        "second": "une seconde",
        "seconds": "{0} secondes",
        "minute": "une minute",
        "minutes": "{0} minutes",
        "hour": "une heure",
        "hours": "{0} heures",
        "day": "un jour",
        "days": "{0} jours",
        "week": "une semaine",
        "weeks": "{0} semaines",
        "month": "un mois",
        "months": "{0} mois",
        "year": "un an",
        "years": "{0} ans",
    }

    month_names = [
        "",
        "janvier",
        "février",
        "mars",
        "avril",
        "mai",
        "juin",
        "juillet",
        "août",
        "septembre",
        "octobre",
        "novembre",
        "décembre",
    ]

    day_names = [
        "",
        "lundi",
        "mardi",
        "mercredi",
        "jeudi",
        "vendredi",
        "samedi",
        "dimanche",
    ]
    day_abbreviations = ["", "lun", "mar", "mer", "jeu", "ven", "sam", "dim"]

    ordinal_day_re = (
        r"((?P<value>\b1(?=er\b)|[1-3]?[02-9](?=e\b)|[1-3]1(?=e\b))(er|e)\b)"
    )

    def _ordinal_number(self, n: int) -> str:
        if abs(n) == 1:
            return f"{n}er"
        return f"{n}e"


class FrenchLocale(FrenchBaseLocale, Locale):

    names = ["fr", "fr-fr"]

    month_abbreviations = [
        "",
        "janv",
        "févr",
        "mars",
        "avr",
        "mai",
        "juin",
        "juil",
        "août",
        "sept",
        "oct",
        "nov",
        "déc",
    ]


class FrenchCanadianLocale(FrenchBaseLocale, Locale):

    names = ["fr-ca"]

    month_abbreviations = [
        "",
        "janv",
        "févr",
        "mars",
        "avr",
        "mai",
        "juin",
        "juill",
        "août",
        "sept",
        "oct",
        "nov",
        "déc",
    ]


class GreekLocale(Locale):

    names = ["el", "el-gr"]

    past = "{0} πριν"
    future = "σε {0}"
    and_word = "και"

    timeframes = {
        "now": "τώρα",
        "second": "ένα δεύτερο",
        "seconds": "{0} δευτερόλεπτα",
        "minute": "ένα λεπτό",
        "minutes": "{0} λεπτά",
        "hour": "μία ώρα",
        "hours": "{0} ώρες",
        "day": "μία μέρα",
        "days": "{0} μέρες",
        "month": "ένα μήνα",
        "months": "{0} μήνες",
        "year": "ένα χρόνο",
        "years": "{0} χρόνια",
    }

    month_names = [
        "",
        "Ιανουαρίου",
        "Φεβρουαρίου",
        "Μαρτίου",
        "Απριλίου",
        "Μαΐου",
        "Ιουνίου",
        "Ιουλίου",
        "Αυγούστου",
        "Σεπτεμβρίου",
        "Οκτωβρίου",
        "Νοεμβρίου",
        "Δεκεμβρίου",
    ]
    month_abbreviations = [
        "",
        "Ιαν",
        "Φεβ",
        "Μαρ",
        "Απρ",
        "Μαϊ",
        "Ιον",
        "Ιολ",
        "Αυγ",
        "Σεπ",
        "Οκτ",
        "Νοε",
        "Δεκ",
    ]

    day_names = [
        "",
        "Δευτέρα",
        "Τρίτη",
        "Τετάρτη",
        "Πέμπτη",
        "Παρασκευή",
        "Σάββατο",
        "Κυριακή",
    ]
    day_abbreviations = ["", "Δευ", "Τρι", "Τετ", "Πεμ", "Παρ", "Σαβ", "Κυρ"]


class JapaneseLocale(Locale):

    names = ["ja", "ja-jp"]

    past = "{0}前"
    future = "{0}後"
    and_word = ""

    timeframes = {
        "now": "現在",
        "second": "1秒",
        "seconds": "{0}秒",
        "minute": "1分",
        "minutes": "{0}分",
        "hour": "1時間",
        "hours": "{0}時間",
        "day": "1日",
        "days": "{0}日",
        "week": "1週間",
        "weeks": "{0}週間",
        "month": "1ヶ月",
        "months": "{0}ヶ月",
        "year": "1年",
        "years": "{0}年",
    }

    month_names = [
        "",
        "1月",
        "2月",
        "3月",
        "4月",
        "5月",
        "6月",
        "7月",
        "8月",
        "9月",
        "10月",
        "11月",
        "12月",
    ]
    month_abbreviations = [
        "",
        " 1",
        " 2",
        " 3",
        " 4",
        " 5",
        " 6",
        " 7",
        " 8",
        " 9",
        "10",
        "11",
        "12",
    ]

    day_names = ["", "月曜日", "火曜日", "水曜日", "木曜日", "金曜日", "土曜日", "日曜日"]
    day_abbreviations = ["", "月", "火", "水", "木", "金", "土", "日"]


class SwedishLocale(Locale):

    names = ["sv", "sv-se"]

    past = "för {0} sen"
    future = "om {0}"
    and_word = "och"

    timeframes = {
        "now": "just nu",
        "second": "en sekund",
        "seconds": "{0} sekunder",
        "minute": "en minut",
        "minutes": "{0} minuter",
        "hour": "en timme",
        "hours": "{0} timmar",
        "day": "en dag",
        "days": "{0} dagar",
        "week": "en vecka",
        "weeks": "{0} veckor",
        "month": "en månad",
        "months": "{0} månader",
        "year": "ett år",
        "years": "{0} år",
    }

    month_names = [
        "",
        "januari",
        "februari",
        "mars",
        "april",
        "maj",
        "juni",
        "juli",
        "augusti",
        "september",
        "oktober",
        "november",
        "december",
    ]
    month_abbreviations = [
        "",
        "jan",
        "feb",
        "mar",
        "apr",
        "maj",
        "jun",
        "jul",
        "aug",
        "sep",
        "okt",
        "nov",
        "dec",
    ]

    day_names = [
        "",
        "måndag",
        "tisdag",
        "onsdag",
        "torsdag",
        "fredag",
        "lördag",
        "söndag",
    ]
    day_abbreviations = ["", "mån", "tis", "ons", "tor", "fre", "lör", "sön"]


class FinnishLocale(Locale):

    names = ["fi", "fi-fi"]

    # The finnish grammar is very complex, and its hard to convert
    # 1-to-1 to something like English.

    past = "{0} sitten"
    future = "{0} kuluttua"

    timeframes: ClassVar[Mapping[TimeFrameLiteral, List[str]]] = {
        "now": ["juuri nyt", "juuri nyt"],
        "second": ["sekunti", "sekunti"],
        "seconds": ["{0} muutama sekunti", "{0} muutaman sekunnin"],
        "minute": ["minuutti", "minuutin"],
        "minutes": ["{0} minuuttia", "{0} minuutin"],
        "hour": ["tunti", "tunnin"],
        "hours": ["{0} tuntia", "{0} tunnin"],
        "day": ["päivä", "päivä"],
        "days": ["{0} päivää", "{0} päivän"],
        "month": ["kuukausi", "kuukauden"],
        "months": ["{0} kuukautta", "{0} kuukauden"],
        "year": ["vuosi", "vuoden"],
        "years": ["{0} vuotta", "{0} vuoden"],
    }

    # Months and days are lowercase in Finnish
    month_names = [
        "",
        "tammikuu",
        "helmikuu",
        "maaliskuu",
        "huhtikuu",
        "toukokuu",
        "kesäkuu",
        "heinäkuu",
        "elokuu",
        "syyskuu",
        "lokakuu",
        "marraskuu",
        "joulukuu",
    ]

    month_abbreviations = [
        "",
        "tammi",
        "helmi",
        "maalis",
        "huhti",
        "touko",
        "kesä",
        "heinä",
        "elo",
        "syys",
        "loka",
        "marras",
        "joulu",
    ]

    day_names = [
        "",
        "maanantai",
        "tiistai",
        "keskiviikko",
        "torstai",
        "perjantai",
        "lauantai",
        "sunnuntai",
    ]

    day_abbreviations = ["", "ma", "ti", "ke", "to", "pe", "la", "su"]

    # TODO: Fix return type
    def _format_timeframe(self, timeframe: TimeFrameLiteral, delta: Union[float, int]) -> Tuple[str, str]:  # type: ignore
        return (
            self.timeframes[timeframe][0].format(abs(delta)),
            self.timeframes[timeframe][1].format(abs(delta)),
        )

    def _format_relative(
        self,
        humanized: str,
        timeframe: TimeFrameLiteral,
        delta: Union[float, int],
    ) -> str:
        if timeframe == "now":
            return humanized[0]

        direction = self.past if delta < 0 else self.future
        which = 0 if delta < 0 else 1

        return direction.format(humanized[which])

    def _ordinal_number(self, n: int) -> str:
        return f"{n}."


class ChineseCNLocale(Locale):

    names = ["zh", "zh-cn"]

    past = "{0}前"
    future = "{0}后"

    timeframes = {
        "now": "刚才",
        "second": "一秒",
        "seconds": "{0}秒",
        "minute": "1分钟",
        "minutes": "{0}分钟",
        "hour": "1小时",
        "hours": "{0}小时",
        "day": "1天",
        "days": "{0}天",
        "week": "一周",
        "weeks": "{0}周",
        "month": "1个月",
        "months": "{0}个月",
        "year": "1年",
        "years": "{0}年",
    }

    month_names = [
        "",
        "一月",
        "二月",
        "三月",
        "四月",
        "五月",
        "六月",
        "七月",
        "八月",
        "九月",
        "十月",
        "十一月",
        "十二月",
    ]
    month_abbreviations = [
        "",
        " 1",
        " 2",
        " 3",
        " 4",
        " 5",
        " 6",
        " 7",
        " 8",
        " 9",
        "10",
        "11",
        "12",
    ]

    day_names = ["", "星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]
    day_abbreviations = ["", "一", "二", "三", "四", "五", "六", "日"]


class ChineseTWLocale(Locale):

    names = ["zh-tw"]

    past = "{0}前"
    future = "{0}後"
    and_word = "和"

    timeframes = {
        "now": "剛才",
        "second": "1秒",
        "seconds": "{0}秒",
        "minute": "1分鐘",
        "minutes": "{0}分鐘",
        "hour": "1小時",
        "hours": "{0}小時",
        "day": "1天",
        "days": "{0}天",
        "week": "1週",
        "weeks": "{0}週",
        "month": "1個月",
        "months": "{0}個月",
        "year": "1年",
        "years": "{0}年",
    }

    month_names = [
        "",
        "1月",
        "2月",
        "3月",
        "4月",
        "5月",
        "6月",
        "7月",
        "8月",
        "9月",
        "10月",
        "11月",
        "12月",
    ]
    month_abbreviations = [
        "",
        " 1",
        " 2",
        " 3",
        " 4",
        " 5",
        " 6",
        " 7",
        " 8",
        " 9",
        "10",
        "11",
        "12",
    ]

    day_names = ["", "週一", "週二", "週三", "週四", "週五", "週六", "週日"]
    day_abbreviations = ["", "一", "二", "三", "四", "五", "六", "日"]


class HongKongLocale(Locale):

    names = ["zh-hk"]

    past = "{0}前"
    future = "{0}後"

    timeframes = {
        "now": "剛才",
        "second": "1秒",
        "seconds": "{0}秒",
        "minute": "1分鐘",
        "minutes": "{0}分鐘",
        "hour": "1小時",
        "hours": "{0}小時",
        "day": "1天",
        "days": "{0}天",
        "week": "1星期",
        "weeks": "{0}星期",
        "month": "1個月",
        "months": "{0}個月",
        "year": "1年",
        "years": "{0}年",
    }

    month_names = [
        "",
        "1月",
        "2月",
        "3月",
        "4月",
        "5月",
        "6月",
        "7月",
        "8月",
        "9月",
        "10月",
        "11月",
        "12月",
    ]
    month_abbreviations = [
        "",
        " 1",
        " 2",
        " 3",
        " 4",
        " 5",
        " 6",
        " 7",
        " 8",
        " 9",
        "10",
        "11",
        "12",
    ]

    day_names = ["", "星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]
    day_abbreviations = ["", "一", "二", "三", "四", "五", "六", "日"]


class KoreanLocale(Locale):

    names = ["ko", "ko-kr"]

    past = "{0} 전"
    future = "{0} 후"

    timeframes = {
        "now": "지금",
        "second": "1초",
        "seconds": "{0}초",
        "minute": "1분",
        "minutes": "{0}분",
        "hour": "한시간",
        "hours": "{0}시간",
        "day": "하루",
        "days": "{0}일",
        "week": "1주",
        "weeks": "{0}주",
        "month": "한달",
        "months": "{0}개월",
        "year": "1년",
        "years": "{0}년",
    }

    special_dayframes = {
        -3: "그끄제",
        -2: "그제",
        -1: "어제",
        1: "내일",
        2: "모레",
        3: "글피",
        4: "그글피",
    }

    special_yearframes = {-2: "제작년", -1: "작년", 1: "내년", 2: "내후년"}

    month_names = [
        "",
        "1월",
        "2월",
        "3월",
        "4월",
        "5월",
        "6월",
        "7월",
        "8월",
        "9월",
        "10월",
        "11월",
        "12월",
    ]
    month_abbreviations = [
        "",
        " 1",
        " 2",
        " 3",
        " 4",
        " 5",
        " 6",
        " 7",
        " 8",
        " 9",
        "10",
        "11",
        "12",
    ]

    day_names = ["", "월요일", "화요일", "수요일", "목요일", "금요일", "토요일", "일요일"]
    day_abbreviations = ["", "월", "화", "수", "목", "금", "토", "일"]

    def _ordinal_number(self, n: int) -> str:
        ordinals = ["0", "첫", "두", "세", "네", "다섯", "여섯", "일곱", "여덟", "아홉", "열"]
        if n < len(ordinals):
            return f"{ordinals[n]}번째"
        return f"{n}번째"

    def _format_relative(
        self,
        humanized: str,
        timeframe: TimeFrameLiteral,
        delta: Union[float, int],
    ) -> str:
        if timeframe in ("day", "days"):
            special = self.special_dayframes.get(int(delta))
            if special:
                return special
        elif timeframe in ("year", "years"):
            special = self.special_yearframes.get(int(delta))
            if special:
                return special

        return super()._format_relative(humanized, timeframe, delta)


# derived locale types & implementations.
class DutchLocale(Locale):

    names = ["nl", "nl-nl"]

    past = "{0} geleden"
    future = "over {0}"

    timeframes = {
        "now": "nu",
        "second": "een seconde",
        "seconds": "{0} seconden",
        "minute": "een minuut",
        "minutes": "{0} minuten",
        "hour": "een uur",
        "hours": "{0} uur",
        "day": "een dag",
        "days": "{0} dagen",
        "week": "een week",
        "weeks": "{0} weken",
        "month": "een maand",
        "months": "{0} maanden",
        "year": "een jaar",
        "years": "{0} jaar",
    }

    # In Dutch names of months and days are not starting with a capital letter
    # like in the English language.
    month_names = [
        "",
        "januari",
        "februari",
        "maart",
        "april",
        "mei",
        "juni",
        "juli",
        "augustus",
        "september",
        "oktober",
        "november",
        "december",
    ]
    month_abbreviations = [
        "",
        "jan",
        "feb",
        "mrt",
        "apr",
        "mei",
        "jun",
        "jul",
        "aug",
        "sep",
        "okt",
        "nov",
        "dec",
    ]

    day_names = [
        "",
        "maandag",
        "dinsdag",
        "woensdag",
        "donderdag",
        "vrijdag",
        "zaterdag",
        "zondag",
    ]
    day_abbreviations = ["", "ma", "di", "wo", "do", "vr", "za", "zo"]


class SlavicBaseLocale(Locale):
    timeframes: ClassVar[Mapping[TimeFrameLiteral, Union[str, List[str]]]]

    def _format_timeframe(
        self, timeframe: TimeFrameLiteral, delta: Union[float, int]
    ) -> str:
        form = self.timeframes[timeframe]
        delta = abs(delta)

        if isinstance(form, list):
            if delta % 10 == 1 and delta % 100 != 11:
                form = form[0]
            elif 2 <= delta % 10 <= 4 and (delta % 100 < 10 or delta % 100 >= 20):
                form = form[1]
            else:
                form = form[2]

        return form.format(delta)


class BelarusianLocale(SlavicBaseLocale):

    names = ["be", "be-by"]

    past = "{0} таму"
    future = "праз {0}"

    timeframes: ClassVar[Mapping[TimeFrameLiteral, Union[str, List[str]]]] = {
        "now": "зараз",
        "second": "секунду",
        "seconds": "{0} некалькі секунд",
        "minute": "хвіліну",
        "minutes": ["{0} хвіліну", "{0} хвіліны", "{0} хвілін"],
        "hour": "гадзіну",
        "hours": ["{0} гадзіну", "{0} гадзіны", "{0} гадзін"],
        "day": "дзень",
        "days": ["{0} дзень", "{0} дні", "{0} дзён"],
        "month": "месяц",
        "months": ["{0} месяц", "{0} месяцы", "{0} месяцаў"],
        "year": "год",
        "years": ["{0} год", "{0} гады", "{0} гадоў"],
    }

    month_names = [
        "",
        "студзеня",
        "лютага",
        "сакавіка",
        "красавіка",
        "траўня",
        "чэрвеня",
        "ліпеня",
        "жніўня",
        "верасня",
        "кастрычніка",
        "лістапада",
        "снежня",
    ]
    month_abbreviations = [
        "",
        "студ",
        "лют",
        "сак",
        "крас",
        "трав",
        "чэрв",
        "ліп",
        "жнів",
        "вер",
        "каст",
        "ліст",
        "снеж",
    ]

    day_names = [
        "",
        "панядзелак",
        "аўторак",
        "серада",
        "чацвер",
        "пятніца",
        "субота",
        "нядзеля",
    ]
    day_abbreviations = ["", "пн", "ат", "ср", "чц", "пт", "сб", "нд"]


class PolishLocale(SlavicBaseLocale):

    names = ["pl", "pl-pl"]

    past = "{0} temu"
    future = "za {0}"

    # The nouns should be in genitive case (Polish: "dopełniacz")
    # in order to correctly form `past` & `future` expressions.
    timeframes: ClassVar[Mapping[TimeFrameLiteral, Union[str, List[str]]]] = {
        "now": "teraz",
        "second": "sekundę",
        "seconds": ["{0} sekund", "{0} sekundy", "{0} sekund"],
        "minute": "minutę",
        "minutes": ["{0} minut", "{0} minuty", "{0} minut"],
        "hour": "godzinę",
        "hours": ["{0} godzin", "{0} godziny", "{0} godzin"],
        "day": "dzień",
        "days": "{0} dni",
        "week": "tydzień",
        "weeks": ["{0} tygodni", "{0} tygodnie", "{0} tygodni"],
        "month": "miesiąc",
        "months": ["{0} miesięcy", "{0} miesiące", "{0} miesięcy"],
        "year": "rok",
        "years": ["{0} lat", "{0} lata", "{0} lat"],
    }

    month_names = [
        "",
        "styczeń",
        "luty",
        "marzec",
        "kwiecień",
        "maj",
        "czerwiec",
        "lipiec",
        "sierpień",
        "wrzesień",
        "październik",
        "listopad",
        "grudzień",
    ]
    month_abbreviations = [
        "",
        "sty",
        "lut",
        "mar",
        "kwi",
        "maj",
        "cze",
        "lip",
        "sie",
        "wrz",
        "paź",
        "lis",
        "gru",
    ]

    day_names = [
        "",
        "poniedziałek",
        "wtorek",
        "środa",
        "czwartek",
        "piątek",
        "sobota",
        "niedziela",
    ]
    day_abbreviations = ["", "Pn", "Wt", "Śr", "Czw", "Pt", "So", "Nd"]


class RussianLocale(SlavicBaseLocale):

    names = ["ru", "ru-ru"]

    past = "{0} назад"
    future = "через {0}"

    timeframes: ClassVar[Mapping[TimeFrameLiteral, Union[str, List[str]]]] = {
        "now": "сейчас",
        "second": "Второй",
        "seconds": "{0} несколько секунд",
        "minute": "минуту",
        "minutes": ["{0} минуту", "{0} минуты", "{0} минут"],
        "hour": "час",
        "hours": ["{0} час", "{0} часа", "{0} часов"],
        "day": "день",
        "days": ["{0} день", "{0} дня", "{0} дней"],
        "week": "неделю",
        "weeks": ["{0} неделю", "{0} недели", "{0} недель"],
        "month": "месяц",
        "months": ["{0} месяц", "{0} месяца", "{0} месяцев"],
        "year": "год",
        "years": ["{0} год", "{0} года", "{0} лет"],
    }

    month_names = [
        "",
        "января",
        "февраля",
        "марта",
        "апреля",
        "мая",
        "июня",
        "июля",
        "августа",
        "сентября",
        "октября",
        "ноября",
        "декабря",
    ]
    month_abbreviations = [
        "",
        "янв",
        "фев",
        "мар",
        "апр",
        "май",
        "июн",
        "июл",
        "авг",
        "сен",
        "окт",
        "ноя",
        "дек",
    ]

    day_names = [
        "",
        "понедельник",
        "вторник",
        "среда",
        "четверг",
        "пятница",
        "суббота",
        "воскресенье",
    ]
    day_abbreviations = ["", "пн", "вт", "ср", "чт", "пт", "сб", "вс"]


class AfrikaansLocale(Locale):

    names = ["af", "af-nl"]

    past = "{0} gelede"
    future = "in {0}"

    timeframes = {
        "now": "nou",
        "second": "n sekonde",
        "seconds": "{0} sekondes",
        "minute": "minuut",
        "minutes": "{0} minute",
        "hour": "uur",
        "hours": "{0} ure",
        "day": "een dag",
        "days": "{0} dae",
        "month": "een maand",
        "months": "{0} maande",
        "year": "een jaar",
        "years": "{0} jaar",
    }

    month_names = [
        "",
        "Januarie",
        "Februarie",
        "Maart",
        "April",
        "Mei",
        "Junie",
        "Julie",
        "Augustus",
        "September",
        "Oktober",
        "November",
        "Desember",
    ]
    month_abbreviations = [
        "",
        "Jan",
        "Feb",
        "Mrt",
        "Apr",
        "Mei",
        "Jun",
        "Jul",
        "Aug",
        "Sep",
        "Okt",
        "Nov",
        "Des",
    ]

    day_names = [
        "",
        "Maandag",
        "Dinsdag",
        "Woensdag",
        "Donderdag",
        "Vrydag",
        "Saterdag",
        "Sondag",
    ]
    day_abbreviations = ["", "Ma", "Di", "Wo", "Do", "Vr", "Za", "So"]


class BulgarianLocale(SlavicBaseLocale):

    names = ["bg", "bg-bg"]

    past = "{0} назад"
    future = "напред {0}"

    timeframes: ClassVar[Mapping[TimeFrameLiteral, Union[str, List[str]]]] = {
        "now": "сега",
        "second": "секунда",
        "seconds": "{0} няколко секунди",
        "minute": "минута",
        "minutes": ["{0} минута", "{0} минути", "{0} минути"],
        "hour": "час",
        "hours": ["{0} час", "{0} часа", "{0} часа"],
        "day": "ден",
        "days": ["{0} ден", "{0} дни", "{0} дни"],
        "month": "месец",
        "months": ["{0} месец", "{0} месеца", "{0} месеца"],
        "year": "година",
        "years": ["{0} година", "{0} години", "{0} години"],
    }

    month_names = [
        "",
        "януари",
        "февруари",
        "март",
        "април",
        "май",
        "юни",
        "юли",
        "август",
        "септември",
        "октомври",
        "ноември",
        "декември",
    ]
    month_abbreviations = [
        "",
        "ян",
        "февр",
        "март",
        "апр",
        "май",
        "юни",
        "юли",
        "авг",
        "септ",
        "окт",
        "ноем",
        "дек",
    ]

    day_names = [
        "",
        "понеделник",
        "вторник",
        "сряда",
        "четвъртък",
        "петък",
        "събота",
        "неделя",
    ]
    day_abbreviations = ["", "пон", "вт", "ср", "четв", "пет", "съб", "нед"]


class UkrainianLocale(SlavicBaseLocale):

    names = ["ua", "uk-ua"]

    past = "{0} тому"
    future = "за {0}"

    timeframes: ClassVar[Mapping[TimeFrameLiteral, Union[str, List[str]]]] = {
        "now": "зараз",
        "second": "секунда",
        "seconds": "{0} кілька секунд",
        "minute": "хвилину",
        "minutes": ["{0} хвилину", "{0} хвилини", "{0} хвилин"],
        "hour": "годину",
        "hours": ["{0} годину", "{0} години", "{0} годин"],
        "day": "день",
        "days": ["{0} день", "{0} дні", "{0} днів"],
        "month": "місяць",
        "months": ["{0} місяць", "{0} місяці", "{0} місяців"],
        "year": "рік",
        "years": ["{0} рік", "{0} роки", "{0} років"],
    }

    month_names = [
        "",
        "січня",
        "лютого",
        "березня",
        "квітня",
        "травня",
        "червня",
        "липня",
        "серпня",
        "вересня",
        "жовтня",
        "листопада",
        "грудня",
    ]
    month_abbreviations = [
        "",
        "січ",
        "лют",
        "бер",
        "квіт",
        "трав",
        "черв",
        "лип",
        "серп",
        "вер",
        "жовт",
        "лист",
        "груд",
    ]

    day_names = [
        "",
        "понеділок",
        "вівторок",
        "середа",
        "четвер",
        "п’ятниця",
        "субота",
        "неділя",
    ]
    day_abbreviations = ["", "пн", "вт", "ср", "чт", "пт", "сб", "нд"]


class MacedonianLocale(SlavicBaseLocale):
    names = ["mk", "mk-mk"]

    past = "пред {0}"
    future = "за {0}"

    timeframes: ClassVar[Mapping[TimeFrameLiteral, Union[str, List[str]]]] = {
        "now": "сега",
        "second": "една секунда",
        "seconds": ["{0} секунда", "{0} секунди", "{0} секунди"],
        "minute": "една минута",
        "minutes": ["{0} минута", "{0} минути", "{0} минути"],
        "hour": "еден саат",
        "hours": ["{0} саат", "{0} саати", "{0} саати"],
        "day": "еден ден",
        "days": ["{0} ден", "{0} дена", "{0} дена"],
        "week": "една недела",
        "weeks": ["{0} недела", "{0} недели", "{0} недели"],
        "month": "еден месец",
        "months": ["{0} месец", "{0} месеци", "{0} месеци"],
        "year": "една година",
        "years": ["{0} година", "{0} години", "{0} години"],
    }

    meridians = {"am": "дп", "pm": "пп", "AM": "претпладне", "PM": "попладне"}

    month_names = [
        "",
        "Јануари",
        "Февруари",
        "Март",
        "Април",
        "Мај",
        "Јуни",
        "Јули",
        "Август",
        "Септември",
        "Октомври",
        "Ноември",
        "Декември",
    ]
    month_abbreviations = [
        "",
        "Јан",
        "Фев",
        "Мар",
        "Апр",
        "Мај",
        "Јун",
        "Јул",
        "Авг",
        "Септ",
        "Окт",
        "Ноем",
        "Декем",
    ]

    day_names = [
        "",
        "Понеделник",
        "Вторник",
        "Среда",
        "Четврток",
        "Петок",
        "Сабота",
        "Недела",
    ]
    day_abbreviations = [
        "",
        "Пон",
        "Вт",
        "Сре",
        "Чет",
        "Пет",
        "Саб",
        "Нед",
    ]


class GermanBaseLocale(Locale):

    past = "vor {0}"
    future = "in {0}"
    and_word = "und"

    timeframes = {
        "now": "gerade eben",
        "second": "einer Sekunde",
        "seconds": "{0} Sekunden",
        "minute": "einer Minute",
        "minutes": "{0} Minuten",
        "hour": "einer Stunde",
        "hours": "{0} Stunden",
        "day": "einem Tag",
        "days": "{0} Tagen",
        "week": "einer Woche",
        "weeks": "{0} Wochen",
        "month": "einem Monat",
        "months": "{0} Monaten",
        "year": "einem Jahr",
        "years": "{0} Jahren",
    }

    timeframes_only_distance = timeframes.copy()
    timeframes_only_distance["second"] = "eine Sekunde"
    timeframes_only_distance["minute"] = "eine Minute"
    timeframes_only_distance["hour"] = "eine Stunde"
    timeframes_only_distance["day"] = "ein Tag"
    timeframes_only_distance["days"] = "{0} Tage"
    timeframes_only_distance["week"] = "eine Woche"
    timeframes_only_distance["month"] = "ein Monat"
    timeframes_only_distance["months"] = "{0} Monate"
    timeframes_only_distance["year"] = "ein Jahr"
    timeframes_only_distance["years"] = "{0} Jahre"

    month_names = [
        "",
        "Januar",
        "Februar",
        "März",
        "April",
        "Mai",
        "Juni",
        "Juli",
        "August",
        "September",
        "Oktober",
        "November",
        "Dezember",
    ]

    month_abbreviations = [
        "",
        "Jan",
        "Feb",
        "Mär",
        "Apr",
        "Mai",
        "Jun",
        "Jul",
        "Aug",
        "Sep",
        "Okt",
        "Nov",
        "Dez",
    ]

    day_names = [
        "",
        "Montag",
        "Dienstag",
        "Mittwoch",
        "Donnerstag",
        "Freitag",
        "Samstag",
        "Sonntag",
    ]

    day_abbreviations = ["", "Mo", "Di", "Mi", "Do", "Fr", "Sa", "So"]

    def _ordinal_number(self, n: int) -> str:
        return f"{n}."

    def describe(
        self,
        timeframe: TimeFrameLiteral,
        delta: Union[int, float] = 0,
        only_distance: bool = False,
    ) -> str:
        """Describes a delta within a timeframe in plain language.

        :param timeframe: a string representing a timeframe.
        :param delta: a quantity representing a delta in a timeframe.
        :param only_distance: return only distance eg: "11 seconds" without "in" or "ago" keywords
        """

        if not only_distance:
            return super().describe(timeframe, delta, only_distance)

        # German uses a different case without 'in' or 'ago'
        humanized = self.timeframes_only_distance[timeframe].format(trunc(abs(delta)))

        return humanized


class GermanLocale(GermanBaseLocale, Locale):

    names = ["de", "de-de"]


class SwissLocale(GermanBaseLocale, Locale):

    names = ["de-ch"]


class AustrianLocale(GermanBaseLocale, Locale):

    names = ["de-at"]

    month_names = [
        "",
        "Jänner",
        "Februar",
        "März",
        "April",
        "Mai",
        "Juni",
        "Juli",
        "August",
        "September",
        "Oktober",
        "November",
        "Dezember",
    ]


class NorwegianLocale(Locale):

    names = ["nb", "nb-no"]

    past = "for {0} siden"
    future = "om {0}"

    timeframes = {
        "now": "nå nettopp",
        "second": "ett sekund",
        "seconds": "{0} sekunder",
        "minute": "ett minutt",
        "minutes": "{0} minutter",
        "hour": "en time",
        "hours": "{0} timer",
        "day": "en dag",
        "days": "{0} dager",
        "month": "en måned",
        "months": "{0} måneder",
        "year": "ett år",
        "years": "{0} år",
    }

    month_names = [
        "",
        "januar",
        "februar",
        "mars",
        "april",
        "mai",
        "juni",
        "juli",
        "august",
        "september",
        "oktober",
        "november",
        "desember",
    ]
    month_abbreviations = [
        "",
        "jan",
        "feb",
        "mar",
        "apr",
        "mai",
        "jun",
        "jul",
        "aug",
        "sep",
        "okt",
        "nov",
        "des",
    ]

    day_names = [
        "",
        "mandag",
        "tirsdag",
        "onsdag",
        "torsdag",
        "fredag",
        "lørdag",
        "søndag",
    ]
    day_abbreviations = ["", "ma", "ti", "on", "to", "fr", "lø", "sø"]


class NewNorwegianLocale(Locale):

    names = ["nn", "nn-no"]

    past = "for {0} sidan"
    future = "om {0}"

    timeframes = {
        "now": "no nettopp",
        "second": "eitt sekund",
        "seconds": "{0} sekund",
        "minute": "eitt minutt",
        "minutes": "{0} minutt",
        "hour": "ein time",
        "hours": "{0} timar",
        "day": "ein dag",
        "days": "{0} dagar",
        "month": "en månad",
        "months": "{0} månader",
        "year": "eitt år",
        "years": "{0} år",
    }

    month_names = [
        "",
        "januar",
        "februar",
        "mars",
        "april",
        "mai",
        "juni",
        "juli",
        "august",
        "september",
        "oktober",
        "november",
        "desember",
    ]
    month_abbreviations = [
        "",
        "jan",
        "feb",
        "mar",
        "apr",
        "mai",
        "jun",
        "jul",
        "aug",
        "sep",
        "okt",
        "nov",
        "des",
    ]

    day_names = [
        "",
        "måndag",
        "tysdag",
        "onsdag",
        "torsdag",
        "fredag",
        "laurdag",
        "sundag",
    ]
    day_abbreviations = ["", "må", "ty", "on", "to", "fr", "la", "su"]


class PortugueseLocale(Locale):
    names = ["pt", "pt-pt"]

    past = "há {0}"
    future = "em {0}"
    and_word = "e"

    timeframes = {
        "now": "agora",
        "second": "um segundo",
        "seconds": "{0} segundos",
        "minute": "um minuto",
        "minutes": "{0} minutos",
        "hour": "uma hora",
        "hours": "{0} horas",
        "day": "um dia",
        "days": "{0} dias",
        "week": "uma semana",
        "weeks": "{0} semanas",
        "month": "um mês",
        "months": "{0} meses",
        "year": "um ano",
        "years": "{0} anos",
    }

    month_names = [
        "",
        "Janeiro",
        "Fevereiro",
        "Março",
        "Abril",
        "Maio",
        "Junho",
        "Julho",
        "Agosto",
        "Setembro",
        "Outubro",
        "Novembro",
        "Dezembro",
    ]
    month_abbreviations = [
        "",
        "Jan",
        "Fev",
        "Mar",
        "Abr",
        "Mai",
        "Jun",
        "Jul",
        "Ago",
        "Set",
        "Out",
        "Nov",
        "Dez",
    ]

    day_names = [
        "",
        "Segunda-feira",
        "Terça-feira",
        "Quarta-feira",
        "Quinta-feira",
        "Sexta-feira",
        "Sábado",
        "Domingo",
    ]
    day_abbreviations = ["", "Seg", "Ter", "Qua", "Qui", "Sex", "Sab", "Dom"]


class BrazilianPortugueseLocale(PortugueseLocale):
    names = ["pt-br"]

    past = "faz {0}"


class TagalogLocale(Locale):

    names = ["tl", "tl-ph"]

    past = "nakaraang {0}"
    future = "{0} mula ngayon"

    timeframes = {
        "now": "ngayon lang",
        "second": "isang segundo",
        "seconds": "{0} segundo",
        "minute": "isang minuto",
        "minutes": "{0} minuto",
        "hour": "isang oras",
        "hours": "{0} oras",
        "day": "isang araw",
        "days": "{0} araw",
        "week": "isang linggo",
        "weeks": "{0} linggo",
        "month": "isang buwan",
        "months": "{0} buwan",
        "year": "isang taon",
        "years": "{0} taon",
    }

    month_names = [
        "",
        "Enero",
        "Pebrero",
        "Marso",
        "Abril",
        "Mayo",
        "Hunyo",
        "Hulyo",
        "Agosto",
        "Setyembre",
        "Oktubre",
        "Nobyembre",
        "Disyembre",
    ]
    month_abbreviations = [
        "",
        "Ene",
        "Peb",
        "Mar",
        "Abr",
        "May",
        "Hun",
        "Hul",
        "Ago",
        "Set",
        "Okt",
        "Nob",
        "Dis",
    ]

    day_names = [
        "",
        "Lunes",
        "Martes",
        "Miyerkules",
        "Huwebes",
        "Biyernes",
        "Sabado",
        "Linggo",
    ]
    day_abbreviations = ["", "Lun", "Mar", "Miy", "Huw", "Biy", "Sab", "Lin"]

    meridians = {"am": "nu", "pm": "nh", "AM": "ng umaga", "PM": "ng hapon"}

    def _ordinal_number(self, n: int) -> str:
        return f"ika-{n}"


class VietnameseLocale(Locale):

    names = ["vi", "vi-vn"]

    past = "{0} trước"
    future = "{0} nữa"

    timeframes = {
        "now": "hiện tại",
        "second": "một giây",
        "seconds": "{0} giây",
        "minute": "một phút",
        "minutes": "{0} phút",
        "hour": "một giờ",
        "hours": "{0} giờ",
        "day": "một ngày",
        "days": "{0} ngày",
        "week": "một tuần",
        "weeks": "{0} tuần",
        "month": "một tháng",
        "months": "{0} tháng",
        "year": "một năm",
        "years": "{0} năm",
    }

    month_names = [
        "",
        "Tháng Một",
        "Tháng Hai",
        "Tháng Ba",
        "Tháng Tư",
        "Tháng Năm",
        "Tháng Sáu",
        "Tháng Bảy",
        "Tháng Tám",
        "Tháng Chín",
        "Tháng Mười",
        "Tháng Mười Một",
        "Tháng Mười Hai",
    ]
    month_abbreviations = [
        "",
        "Tháng 1",
        "Tháng 2",
        "Tháng 3",
        "Tháng 4",
        "Tháng 5",
        "Tháng 6",
        "Tháng 7",
        "Tháng 8",
        "Tháng 9",
        "Tháng 10",
        "Tháng 11",
        "Tháng 12",
    ]

    day_names = [
        "",
        "Thứ Hai",
        "Thứ Ba",
        "Thứ Tư",
        "Thứ Năm",
        "Thứ Sáu",
        "Thứ Bảy",
        "Chủ Nhật",
    ]
    day_abbreviations = ["", "Thứ 2", "Thứ 3", "Thứ 4", "Thứ 5", "Thứ 6", "Thứ 7", "CN"]


class TurkishLocale(Locale):

    names = ["tr", "tr-tr"]

    past = "{0} önce"
    future = "{0} sonra"

    timeframes = {
        "now": "şimdi",
        "second": "bir saniye",
        "seconds": "{0} saniye",
        "minute": "bir dakika",
        "minutes": "{0} dakika",
        "hour": "bir saat",
        "hours": "{0} saat",
        "day": "bir gün",
        "days": "{0} gün",
        "month": "bir ay",
        "months": "{0} ay",
        "year": "yıl",
        "years": "{0} yıl",
    }

    month_names = [
        "",
        "Ocak",
        "Şubat",
        "Mart",
        "Nisan",
        "Mayıs",
        "Haziran",
        "Temmuz",
        "Ağustos",
        "Eylül",
        "Ekim",
        "Kasım",
        "Aralık",
    ]
    month_abbreviations = [
        "",
        "Oca",
        "Şub",
        "Mar",
        "Nis",
        "May",
        "Haz",
        "Tem",
        "Ağu",
        "Eyl",
        "Eki",
        "Kas",
        "Ara",
    ]

    day_names = [
        "",
        "Pazartesi",
        "Salı",
        "Çarşamba",
        "Perşembe",
        "Cuma",
        "Cumartesi",
        "Pazar",
    ]
    day_abbreviations = ["", "Pzt", "Sal", "Çar", "Per", "Cum", "Cmt", "Paz"]


class AzerbaijaniLocale(Locale):

    names = ["az", "az-az"]

    past = "{0} əvvəl"
    future = "{0} sonra"

    timeframes = {
        "now": "indi",
        "second": "saniyə",
        "seconds": "{0} saniyə",
        "minute": "bir dəqiqə",
        "minutes": "{0} dəqiqə",
        "hour": "bir saat",
        "hours": "{0} saat",
        "day": "bir gün",
        "days": "{0} gün",
        "month": "bir ay",
        "months": "{0} ay",
        "year": "il",
        "years": "{0} il",
    }

    month_names = [
        "",
        "Yanvar",
        "Fevral",
        "Mart",
        "Aprel",
        "May",
        "İyun",
        "İyul",
        "Avqust",
        "Sentyabr",
        "Oktyabr",
        "Noyabr",
        "Dekabr",
    ]
    month_abbreviations = [
        "",
        "Yan",
        "Fev",
        "Mar",
        "Apr",
        "May",
        "İyn",
        "İyl",
        "Avq",
        "Sen",
        "Okt",
        "Noy",
        "Dek",
    ]

    day_names = [
        "",
        "Bazar ertəsi",
        "Çərşənbə axşamı",
        "Çərşənbə",
        "Cümə axşamı",
        "Cümə",
        "Şənbə",
        "Bazar",
    ]
    day_abbreviations = ["", "Ber", "Çax", "Çər", "Cax", "Cüm", "Şnb", "Bzr"]


class ArabicLocale(Locale):
    names = [
        "ar",
        "ar-ae",
        "ar-bh",
        "ar-dj",
        "ar-eg",
        "ar-eh",
        "ar-er",
        "ar-km",
        "ar-kw",
        "ar-ly",
        "ar-om",
        "ar-qa",
        "ar-sa",
        "ar-sd",
        "ar-so",
        "ar-ss",
        "ar-td",
        "ar-ye",
    ]

    past = "منذ {0}"
    future = "خلال {0}"

    timeframes: ClassVar[Mapping[TimeFrameLiteral, Union[str, Mapping[str, str]]]] = {
        "now": "الآن",
        "second": "ثانية",
        "seconds": {"double": "ثانيتين", "ten": "{0} ثوان", "higher": "{0} ثانية"},
        "minute": "دقيقة",
        "minutes": {"double": "دقيقتين", "ten": "{0} دقائق", "higher": "{0} دقيقة"},
        "hour": "ساعة",
        "hours": {"double": "ساعتين", "ten": "{0} ساعات", "higher": "{0} ساعة"},
        "day": "يوم",
        "days": {"double": "يومين", "ten": "{0} أيام", "higher": "{0} يوم"},
        "month": "شهر",
        "months": {"double": "شهرين", "ten": "{0} أشهر", "higher": "{0} شهر"},
        "year": "سنة",
        "years": {"double": "سنتين", "ten": "{0} سنوات", "higher": "{0} سنة"},
    }

    month_names = [
        "",
        "يناير",
        "فبراير",
        "مارس",
        "أبريل",
        "مايو",
        "يونيو",
        "يوليو",
        "أغسطس",
        "سبتمبر",
        "أكتوبر",
        "نوفمبر",
        "ديسمبر",
    ]
    month_abbreviations = [
        "",
        "يناير",
        "فبراير",
        "مارس",
        "أبريل",
        "مايو",
        "يونيو",
        "يوليو",
        "أغسطس",
        "سبتمبر",
        "أكتوبر",
        "نوفمبر",
        "ديسمبر",
    ]

    day_names = [
        "",
        "الإثنين",
        "الثلاثاء",
        "الأربعاء",
        "الخميس",
        "الجمعة",
        "السبت",
        "الأحد",
    ]
    day_abbreviations = ["", "إثنين", "ثلاثاء", "أربعاء", "خميس", "جمعة", "سبت", "أحد"]

    def _format_timeframe(
        self, timeframe: TimeFrameLiteral, delta: Union[float, int]
    ) -> str:
        form = self.timeframes[timeframe]
        delta = abs(delta)
        if isinstance(form, Mapping):
            if delta == 2:
                form = form["double"]
            elif 2 < delta <= 10:
                form = form["ten"]
            else:
                form = form["higher"]

        return form.format(delta)


class LevantArabicLocale(ArabicLocale):
    names = ["ar-iq", "ar-jo", "ar-lb", "ar-ps", "ar-sy"]
    month_names = [
        "",
        "كانون الثاني",
        "شباط",
        "آذار",
        "نيسان",
        "أيار",
        "حزيران",
        "تموز",
        "آب",
        "أيلول",
        "تشرين الأول",
        "تشرين الثاني",
        "كانون الأول",
    ]
    month_abbreviations = [
        "",
        "كانون الثاني",
        "شباط",
        "آذار",
        "نيسان",
        "أيار",
        "حزيران",
        "تموز",
        "آب",
        "أيلول",
        "تشرين الأول",
        "تشرين الثاني",
        "كانون الأول",
    ]


class AlgeriaTunisiaArabicLocale(ArabicLocale):
    names = ["ar-tn", "ar-dz"]
    month_names = [
        "",
        "جانفي",
        "فيفري",
        "مارس",
        "أفريل",
        "ماي",
        "جوان",
        "جويلية",
        "أوت",
        "سبتمبر",
        "أكتوبر",
        "نوفمبر",
        "ديسمبر",
    ]
    month_abbreviations = [
        "",
        "جانفي",
        "فيفري",
        "مارس",
        "أفريل",
        "ماي",
        "جوان",
        "جويلية",
        "أوت",
        "سبتمبر",
        "أكتوبر",
        "نوفمبر",
        "ديسمبر",
    ]


class MauritaniaArabicLocale(ArabicLocale):
    names = ["ar-mr"]
    month_names = [
        "",
        "يناير",
        "فبراير",
        "مارس",
        "إبريل",
        "مايو",
        "يونيو",
        "يوليو",
        "أغشت",
        "شتمبر",
        "أكتوبر",
        "نوفمبر",
        "دجمبر",
    ]
    month_abbreviations = [
        "",
        "يناير",
        "فبراير",
        "مارس",
        "إبريل",
        "مايو",
        "يونيو",
        "يوليو",
        "أغشت",
        "شتمبر",
        "أكتوبر",
        "نوفمبر",
        "دجمبر",
    ]


class MoroccoArabicLocale(ArabicLocale):
    names = ["ar-ma"]
    month_names = [
        "",
        "يناير",
        "فبراير",
        "مارس",
        "أبريل",
        "ماي",
        "يونيو",
        "يوليوز",
        "غشت",
        "شتنبر",
        "أكتوبر",
        "نونبر",
        "دجنبر",
    ]
    month_abbreviations = [
        "",
        "يناير",
        "فبراير",
        "مارس",
        "أبريل",
        "ماي",
        "يونيو",
        "يوليوز",
        "غشت",
        "شتنبر",
        "أكتوبر",
        "نونبر",
        "دجنبر",
    ]


class IcelandicLocale(Locale):
    def _format_timeframe(
        self, timeframe: TimeFrameLiteral, delta: Union[float, int]
    ) -> str:
        form = self.timeframes[timeframe]
        if delta < 0:
            form = form[0]
        elif delta > 0:
            form = form[1]
            # FIXME: handle when delta is 0

        return form.format(abs(delta))  # type: ignore

    names = ["is", "is-is"]

    past = "fyrir {0} síðan"
    future = "eftir {0}"

    timeframes: ClassVar[Mapping[TimeFrameLiteral, Union[Tuple[str, str], str]]] = {
        "now": "rétt í þessu",
        "second": ("sekúndu", "sekúndu"),
        "seconds": ("{0} nokkrum sekúndum", "nokkrar sekúndur"),
        "minute": ("einni mínútu", "eina mínútu"),
        "minutes": ("{0} mínútum", "{0} mínútur"),
        "hour": ("einum tíma", "einn tíma"),
        "hours": ("{0} tímum", "{0} tíma"),
        "day": ("einum degi", "einn dag"),
        "days": ("{0} dögum", "{0} daga"),
        "month": ("einum mánuði", "einn mánuð"),
        "months": ("{0} mánuðum", "{0} mánuði"),
        "year": ("einu ári", "eitt ár"),
        "years": ("{0} árum", "{0} ár"),
    }

    meridians = {"am": "f.h.", "pm": "e.h.", "AM": "f.h.", "PM": "e.h."}

    month_names = [
        "",
        "janúar",
        "febrúar",
        "mars",
        "apríl",
        "maí",
        "júní",
        "júlí",
        "ágúst",
        "september",
        "október",
        "nóvember",
        "desember",
    ]
    month_abbreviations = [
        "",
        "jan",
        "feb",
        "mar",
        "apr",
        "maí",
        "jún",
        "júl",
        "ágú",
        "sep",
        "okt",
        "nóv",
        "des",
    ]

    day_names = [
        "",
        "mánudagur",
        "þriðjudagur",
        "miðvikudagur",
        "fimmtudagur",
        "föstudagur",
        "laugardagur",
        "sunnudagur",
    ]
    day_abbreviations = ["", "mán", "þri", "mið", "fim", "fös", "lau", "sun"]


class DanishLocale(Locale):

    names = ["da", "da-dk"]

    past = "for {0} siden"
    future = "efter {0}"
    and_word = "og"

    timeframes = {
        "now": "lige nu",
        "second": "et sekund",
        "seconds": "{0} et par sekunder",
        "minute": "et minut",
        "minutes": "{0} minutter",
        "hour": "en time",
        "hours": "{0} timer",
        "day": "en dag",
        "days": "{0} dage",
        "month": "en måned",
        "months": "{0} måneder",
        "year": "et år",
        "years": "{0} år",
    }

    month_names = [
        "",
        "januar",
        "februar",
        "marts",
        "april",
        "maj",
        "juni",
        "juli",
        "august",
        "september",
        "oktober",
        "november",
        "december",
    ]
    month_abbreviations = [
        "",
        "jan",
        "feb",
        "mar",
        "apr",
        "maj",
        "jun",
        "jul",
        "aug",
        "sep",
        "okt",
        "nov",
        "dec",
    ]

    day_names = [
        "",
        "mandag",
        "tirsdag",
        "onsdag",
        "torsdag",
        "fredag",
        "lørdag",
        "søndag",
    ]
    day_abbreviations = ["", "man", "tir", "ons", "tor", "fre", "lør", "søn"]


class MalayalamLocale(Locale):

    names = ["ml"]

    past = "{0} മുമ്പ്"
    future = "{0} ശേഷം"

    timeframes = {
        "now": "ഇപ്പോൾ",
        "second": "ഒരു നിമിഷം",
        "seconds": "{0} സെക്കന്റ്‌",
        "minute": "ഒരു മിനിറ്റ്",
        "minutes": "{0} മിനിറ്റ്",
        "hour": "ഒരു മണിക്കൂർ",
        "hours": "{0} മണിക്കൂർ",
        "day": "ഒരു ദിവസം ",
        "days": "{0} ദിവസം ",
        "month": "ഒരു മാസം ",
        "months": "{0} മാസം ",
        "year": "ഒരു വർഷം ",
        "years": "{0} വർഷം ",
    }

    meridians = {
        "am": "രാവിലെ",
        "pm": "ഉച്ചക്ക് ശേഷം",
        "AM": "രാവിലെ",
        "PM": "ഉച്ചക്ക് ശേഷം",
    }

    month_names = [
        "",
        "ജനുവരി",
        "ഫെബ്രുവരി",
        "മാർച്ച്‌",
        "ഏപ്രിൽ ",
        "മെയ്‌ ",
        "ജൂണ്‍",
        "ജൂലൈ",
        "ഓഗസ്റ്റ്‌",
        "സെപ്റ്റംബർ",
        "ഒക്ടോബർ",
        "നവംബർ",
        "ഡിസംബർ",
    ]
    month_abbreviations = [
        "",
        "ജനു",
        "ഫെബ് ",
        "മാർ",
        "ഏപ്രിൽ",
        "മേയ്",
        "ജൂണ്‍",
        "ജൂലൈ",
        "ഓഗസ്റ",
        "സെപ്റ്റ",
        "ഒക്ടോ",
        "നവം",
        "ഡിസം",
    ]

    day_names = ["", "തിങ്കള്‍", "ചൊവ്വ", "ബുധന്‍", "വ്യാഴം", "വെള്ളി", "ശനി", "ഞായര്‍"]
    day_abbreviations = [
        "",
        "തിങ്കള്‍",
        "ചൊവ്വ",
        "ബുധന്‍",
        "വ്യാഴം",
        "വെള്ളി",
        "ശനി",
        "ഞായര്‍",
    ]


class HindiLocale(Locale):

    names = ["hi"]

    past = "{0} पहले"
    future = "{0} बाद"

    timeframes = {
        "now": "अभी",
        "second": "एक पल",
        "seconds": "{0} सेकंड्",
        "minute": "एक मिनट ",
        "minutes": "{0} मिनट ",
        "hour": "एक घंटा",
        "hours": "{0} घंटे",
        "day": "एक दिन",
        "days": "{0} दिन",
        "month": "एक माह ",
        "months": "{0} महीने ",
        "year": "एक वर्ष ",
        "years": "{0} साल ",
    }

    meridians = {"am": "सुबह", "pm": "शाम", "AM": "सुबह", "PM": "शाम"}

    month_names = [
        "",
        "जनवरी",
        "फरवरी",
        "मार्च",
        "अप्रैल ",
        "मई",
        "जून",
        "जुलाई",
        "अगस्त",
        "सितंबर",
        "अक्टूबर",
        "नवंबर",
        "दिसंबर",
    ]
    month_abbreviations = [
        "",
        "जन",
        "फ़र",
        "मार्च",
        "अप्रै",
        "मई",
        "जून",
        "जुलाई",
        "आग",
        "सित",
        "अकत",
        "नवे",
        "दिस",
    ]

    day_names = [
        "",
        "सोमवार",
        "मंगलवार",
        "बुधवार",
        "गुरुवार",
        "शुक्रवार",
        "शनिवार",
        "रविवार",
    ]
    day_abbreviations = ["", "सोम", "मंगल", "बुध", "गुरुवार", "शुक्र", "शनि", "रवि"]


class CzechLocale(Locale):
    names = ["cs", "cs-cz"]

    timeframes: ClassVar[
        Mapping[TimeFrameLiteral, Union[Mapping[str, Union[List[str], str]], str]]
    ] = {
        "now": "Teď",
        "second": {"past": "vteřina", "future": "vteřina", "zero": "vteřina"},
        "seconds": {"past": "{0} sekundami", "future": ["{0} sekundy", "{0} sekund"]},
        "minute": {"past": "minutou", "future": "minutu", "zero": "{0} minut"},
        "minutes": {"past": "{0} minutami", "future": ["{0} minuty", "{0} minut"]},
        "hour": {"past": "hodinou", "future": "hodinu", "zero": "{0} hodin"},
        "hours": {"past": "{0} hodinami", "future": ["{0} hodiny", "{0} hodin"]},
        "day": {"past": "dnem", "future": "den", "zero": "{0} dnů"},
        "days": {"past": "{0} dny", "future": ["{0} dny", "{0} dnů"]},
        "week": {"past": "týdnem", "future": "týden", "zero": "{0} týdnů"},
        "weeks": {"past": "{0} týdny", "future": ["{0} týdny", "{0} týdnů"]},
        "month": {"past": "měsícem", "future": "měsíc", "zero": "{0} měsíců"},
        "months": {"past": "{0} měsíci", "future": ["{0} měsíce", "{0} měsíců"]},
        "year": {"past": "rokem", "future": "rok", "zero": "{0} let"},
        "years": {"past": "{0} lety", "future": ["{0} roky", "{0} let"]},
    }

    past = "Před {0}"
    future = "Za {0}"

    month_names = [
        "",
        "leden",
        "únor",
        "březen",
        "duben",
        "květen",
        "červen",
        "červenec",
        "srpen",
        "září",
        "říjen",
        "listopad",
        "prosinec",
    ]
    month_abbreviations = [
        "",
        "led",
        "úno",
        "bře",
        "dub",
        "kvě",
        "čvn",
        "čvc",
        "srp",
        "zář",
        "říj",
        "lis",
        "pro",
    ]

    day_names = [
        "",
        "pondělí",
        "úterý",
        "středa",
        "čtvrtek",
        "pátek",
        "sobota",
        "neděle",
    ]
    day_abbreviations = ["", "po", "út", "st", "čt", "pá", "so", "ne"]

    def _format_timeframe(
        self, timeframe: TimeFrameLiteral, delta: Union[float, int]
    ) -> str:
        """Czech aware time frame format function, takes into account
        the differences between past and future forms."""
        abs_delta = abs(delta)
        form = self.timeframes[timeframe]

        if isinstance(form, str):
            return form.format(abs_delta)

        if delta == 0:
            key = "zero"  # And *never* use 0 in the singular!
        elif delta > 0:
            key = "future"
        else:
            key = "past"
        form: Union[List[str], str] = form[key]

        if isinstance(form, list):
            if 2 <= abs_delta % 10 <= 4 and (
                abs_delta % 100 < 10 or abs_delta % 100 >= 20
            ):
                form = form[0]
            else:
                form = form[1]

        return form.format(abs_delta)


class SlovakLocale(Locale):
    names = ["sk", "sk-sk"]

    timeframes: ClassVar[
        Mapping[TimeFrameLiteral, Union[Mapping[str, Union[List[str], str]], str]]
    ] = {
        "now": "Teraz",
        "second": {"past": "sekundou", "future": "sekundu", "zero": "{0} sekúnd"},
        "seconds": {"past": "{0} sekundami", "future": ["{0} sekundy", "{0} sekúnd"]},
        "minute": {"past": "minútou", "future": "minútu", "zero": "{0} minút"},
        "minutes": {"past": "{0} minútami", "future": ["{0} minúty", "{0} minút"]},
        "hour": {"past": "hodinou", "future": "hodinu", "zero": "{0} hodín"},
        "hours": {"past": "{0} hodinami", "future": ["{0} hodiny", "{0} hodín"]},
        "day": {"past": "dňom", "future": "deň", "zero": "{0} dní"},
        "days": {"past": "{0} dňami", "future": ["{0} dni", "{0} dní"]},
        "week": {"past": "týždňom", "future": "týždeň", "zero": "{0} týždňov"},
        "weeks": {"past": "{0} týždňami", "future": ["{0} týždne", "{0} týždňov"]},
        "month": {"past": "mesiacom", "future": "mesiac", "zero": "{0} mesiacov"},
        "months": {"past": "{0} mesiacmi", "future": ["{0} mesiace", "{0} mesiacov"]},
        "year": {"past": "rokom", "future": "rok", "zero": "{0} rokov"},
        "years": {"past": "{0} rokmi", "future": ["{0} roky", "{0} rokov"]},
    }

    past = "Pred {0}"
    future = "O {0}"
    and_word = "a"

    month_names = [
        "",
        "január",
        "február",
        "marec",
        "apríl",
        "máj",
        "jún",
        "júl",
        "august",
        "september",
        "október",
        "november",
        "december",
    ]
    month_abbreviations = [
        "",
        "jan",
        "feb",
        "mar",
        "apr",
        "máj",
        "jún",
        "júl",
        "aug",
        "sep",
        "okt",
        "nov",
        "dec",
    ]

    day_names = [
        "",
        "pondelok",
        "utorok",
        "streda",
        "štvrtok",
        "piatok",
        "sobota",
        "nedeľa",
    ]
    day_abbreviations = ["", "po", "ut", "st", "št", "pi", "so", "ne"]

    def _format_timeframe(
        self, timeframe: TimeFrameLiteral, delta: Union[float, int]
    ) -> str:
        """Slovak aware time frame format function, takes into account
        the differences between past and future forms."""
        abs_delta = abs(delta)
        form = self.timeframes[timeframe]

        if isinstance(form, str):
            return form.format(abs_delta)

        if delta == 0:
            key = "zero"  # And *never* use 0 in the singular!
        elif delta > 0:
            key = "future"
        else:
            key = "past"
        form: Union[List[str], str] = form[key]

        if isinstance(form, list):
            if 2 <= abs_delta % 10 <= 4 and (
                abs_delta % 100 < 10 or abs_delta % 100 >= 20
            ):
                form = form[0]
            else:
                form = form[1]

        return form.format(abs_delta)


class FarsiLocale(Locale):

    names = ["fa", "fa-ir"]

    past = "{0} قبل"
    future = "در {0}"

    timeframes = {
        "now": "اکنون",
        "second": "یک لحظه",
        "seconds": "{0} ثانیه",
        "minute": "یک دقیقه",
        "minutes": "{0} دقیقه",
        "hour": "یک ساعت",
        "hours": "{0} ساعت",
        "day": "یک روز",
        "days": "{0} روز",
        "month": "یک ماه",
        "months": "{0} ماه",
        "year": "یک سال",
        "years": "{0} سال",
    }

    meridians = {
        "am": "قبل از ظهر",
        "pm": "بعد از ظهر",
        "AM": "قبل از ظهر",
        "PM": "بعد از ظهر",
    }

    month_names = [
        "",
        "January",
        "February",
        "March",
        "April",
        "May",
        "June",
        "July",
        "August",
        "September",
        "October",
        "November",
        "December",
    ]
    month_abbreviations = [
        "",
        "Jan",
        "Feb",
        "Mar",
        "Apr",
        "May",
        "Jun",
        "Jul",
        "Aug",
        "Sep",
        "Oct",
        "Nov",
        "Dec",
    ]

    day_names = [
        "",
        "دو شنبه",
        "سه شنبه",
        "چهارشنبه",
        "پنجشنبه",
        "جمعه",
        "شنبه",
        "یکشنبه",
    ]
    day_abbreviations = ["", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]


class HebrewLocale(Locale):

    names = ["he", "he-il"]

    past = "לפני {0}"
    future = "בעוד {0}"
    and_word = "ו"

    timeframes = {
        "now": "הרגע",
        "second": "שנייה",
        "seconds": "{0} שניות",
        "minute": "דקה",
        "minutes": "{0} דקות",
        "hour": "שעה",
        "hours": "{0} שעות",
        "2-hours": "שעתיים",
        "day": "יום",
        "days": "{0} ימים",
        "2-days": "יומיים",
        "week": "שבוע",
        "weeks": "{0} שבועות",
        "2-weeks": "שבועיים",
        "month": "חודש",
        "months": "{0} חודשים",
        "2-months": "חודשיים",
        "year": "שנה",
        "years": "{0} שנים",
        "2-years": "שנתיים",
    }

    meridians = {
        "am": 'לפנ"צ',
        "pm": 'אחר"צ',
        "AM": "לפני הצהריים",
        "PM": "אחרי הצהריים",
    }

    month_names = [
        "",
        "ינואר",
        "פברואר",
        "מרץ",
        "אפריל",
        "מאי",
        "יוני",
        "יולי",
        "אוגוסט",
        "ספטמבר",
        "אוקטובר",
        "נובמבר",
        "דצמבר",
    ]
    month_abbreviations = [
        "",
        "ינו׳",
        "פבר׳",
        "מרץ",
        "אפר׳",
        "מאי",
        "יוני",
        "יולי",
        "אוג׳",
        "ספט׳",
        "אוק׳",
        "נוב׳",
        "דצמ׳",
    ]

    day_names = ["", "שני", "שלישי", "רביעי", "חמישי", "שישי", "שבת", "ראשון"]
    day_abbreviations = ["", "ב׳", "ג׳", "ד׳", "ה׳", "ו׳", "ש׳", "א׳"]

    def _format_timeframe(
        self, timeframe: TimeFrameLiteral, delta: Union[float, int]
    ) -> str:
        """Hebrew couple of <timeframe> aware"""
        couple = f"2-{timeframe}"
        single = timeframe.rstrip("s")
        if abs(delta) == 2 and couple in self.timeframes:
            key = couple
        elif abs(delta) == 1 and single in self.timeframes:
            key = single
        else:
            key = timeframe

        return self.timeframes[key].format(trunc(abs(delta)))

    def describe_multi(
        self,
        timeframes: Sequence[Tuple[TimeFrameLiteral, Union[int, float]]],
        only_distance: bool = False,
    ) -> str:
        """Describes a delta within multiple timeframes in plain language.
        In Hebrew, the and word behaves a bit differently.

        :param timeframes: a list of string, quantity pairs each representing a timeframe and delta.
        :param only_distance: return only distance eg: "2 hours and 11 seconds" without "in" or "ago" keywords
        """

        humanized = ""
        for index, (timeframe, delta) in enumerate(timeframes):
            last_humanized = self._format_timeframe(timeframe, delta)
            if index == 0:
                humanized = last_humanized
            elif index == len(timeframes) - 1:  # Must have at least 2 items
                humanized += " " + self.and_word
                if last_humanized[0].isdecimal():
                    humanized += "־"
                humanized += last_humanized
            else:  # Don't add for the last one
                humanized += ", " + last_humanized

        if not only_distance:
            humanized = self._format_relative(humanized, timeframe, delta)

        return humanized


class MarathiLocale(Locale):

    names = ["mr"]

    past = "{0} आधी"
    future = "{0} नंतर"

    timeframes = {
        "now": "सद्य",
        "second": "एक सेकंद",
        "seconds": "{0} सेकंद",
        "minute": "एक मिनिट ",
        "minutes": "{0} मिनिट ",
        "hour": "एक तास",
        "hours": "{0} तास",
        "day": "एक दिवस",
        "days": "{0} दिवस",
        "month": "एक महिना ",
        "months": "{0} महिने ",
        "year": "एक वर्ष ",
        "years": "{0} वर्ष ",
    }

    meridians = {"am": "सकाळ", "pm": "संध्याकाळ", "AM": "सकाळ", "PM": "संध्याकाळ"}

    month_names = [
        "",
        "जानेवारी",
        "फेब्रुवारी",
        "मार्च",
        "एप्रिल",
        "मे",
        "जून",
        "जुलै",
        "अॉगस्ट",
        "सप्टेंबर",
        "अॉक्टोबर",
        "नोव्हेंबर",
        "डिसेंबर",
    ]
    month_abbreviations = [
        "",
        "जान",
        "फेब्रु",
        "मार्च",
        "एप्रि",
        "मे",
        "जून",
        "जुलै",
        "अॉग",
        "सप्टें",
        "अॉक्टो",
        "नोव्हें",
        "डिसें",
    ]

    day_names = [
        "",
        "सोमवार",
        "मंगळवार",
        "बुधवार",
        "गुरुवार",
        "शुक्रवार",
        "शनिवार",
        "रविवार",
    ]
    day_abbreviations = ["", "सोम", "मंगळ", "बुध", "गुरु", "शुक्र", "शनि", "रवि"]


class CatalanLocale(Locale):
    names = ["ca", "ca-es", "ca-ad", "ca-fr", "ca-it"]
    past = "Fa {0}"
    future = "En {0}"
    and_word = "i"

    timeframes = {
        "now": "Ara mateix",
        "second": "un segon",
        "seconds": "{0} segons",
        "minute": "1 minut",
        "minutes": "{0} minuts",
        "hour": "una hora",
        "hours": "{0} hores",
        "day": "un dia",
        "days": "{0} dies",
        "month": "un mes",
        "months": "{0} mesos",
        "year": "un any",
        "years": "{0} anys",
    }

    month_names = [
        "",
        "gener",
        "febrer",
        "març",
        "abril",
        "maig",
        "juny",
        "juliol",
        "agost",
        "setembre",
        "octubre",
        "novembre",
        "desembre",
    ]
    month_abbreviations = [
        "",
        "gen.",
        "febr.",
        "març",
        "abr.",
        "maig",
        "juny",
        "jul.",
        "ag.",
        "set.",
        "oct.",
        "nov.",
        "des.",
    ]
    day_names = [
        "",
        "dilluns",
        "dimarts",
        "dimecres",
        "dijous",
        "divendres",
        "dissabte",
        "diumenge",
    ]
    day_abbreviations = [
        "",
        "dl.",
        "dt.",
        "dc.",
        "dj.",
        "dv.",
        "ds.",
        "dg.",
    ]


class BasqueLocale(Locale):
    names = ["eu", "eu-eu"]
    past = "duela {0}"
    future = "{0}"  # I don't know what's the right phrase in Basque for the future.

    timeframes = {
        "now": "Orain",
        "second": "segundo bat",
        "seconds": "{0} segundu",
        "minute": "minutu bat",
        "minutes": "{0} minutu",
        "hour": "ordu bat",
        "hours": "{0} ordu",
        "day": "egun bat",
        "days": "{0} egun",
        "month": "hilabete bat",
        "months": "{0} hilabet",
        "year": "urte bat",
        "years": "{0} urte",
    }

    month_names = [
        "",
        "urtarrilak",
        "otsailak",
        "martxoak",
        "apirilak",
        "maiatzak",
        "ekainak",
        "uztailak",
        "abuztuak",
        "irailak",
        "urriak",
        "azaroak",
        "abenduak",
    ]
    month_abbreviations = [
        "",
        "urt",
        "ots",
        "mar",
        "api",
        "mai",
        "eka",
        "uzt",
        "abu",
        "ira",
        "urr",
        "aza",
        "abe",
    ]
    day_names = [
        "",
        "astelehena",
        "asteartea",
        "asteazkena",
        "osteguna",
        "ostirala",
        "larunbata",
        "igandea",
    ]
    day_abbreviations = ["", "al", "ar", "az", "og", "ol", "lr", "ig"]


class HungarianLocale(Locale):

    names = ["hu", "hu-hu"]

    past = "{0} ezelőtt"
    future = "{0} múlva"

    timeframes: ClassVar[Mapping[TimeFrameLiteral, Union[str, Mapping[str, str]]]] = {
        "now": "éppen most",
        "second": {"past": "egy második", "future": "egy második"},
        "seconds": {"past": "{0} másodpercekkel", "future": "{0} pár másodperc"},
        "minute": {"past": "egy perccel", "future": "egy perc"},
        "minutes": {"past": "{0} perccel", "future": "{0} perc"},
        "hour": {"past": "egy órával", "future": "egy óra"},
        "hours": {"past": "{0} órával", "future": "{0} óra"},
        "day": {"past": "egy nappal", "future": "egy nap"},
        "days": {"past": "{0} nappal", "future": "{0} nap"},
        "month": {"past": "egy hónappal", "future": "egy hónap"},
        "months": {"past": "{0} hónappal", "future": "{0} hónap"},
        "year": {"past": "egy évvel", "future": "egy év"},
        "years": {"past": "{0} évvel", "future": "{0} év"},
    }

    month_names = [
        "",
        "január",
        "február",
        "március",
        "április",
        "május",
        "június",
        "július",
        "augusztus",
        "szeptember",
        "október",
        "november",
        "december",
    ]
    month_abbreviations = [
        "",
        "jan",
        "febr",
        "márc",
        "ápr",
        "máj",
        "jún",
        "júl",
        "aug",
        "szept",
        "okt",
        "nov",
        "dec",
    ]

    day_names = [
        "",
        "hétfő",
        "kedd",
        "szerda",
        "csütörtök",
        "péntek",
        "szombat",
        "vasárnap",
    ]
    day_abbreviations = ["", "hét", "kedd", "szer", "csüt", "pént", "szom", "vas"]

    meridians = {"am": "de", "pm": "du", "AM": "DE", "PM": "DU"}

    def _format_timeframe(
        self, timeframe: TimeFrameLiteral, delta: Union[float, int]
    ) -> str:
        form = self.timeframes[timeframe]

        if isinstance(form, Mapping):
            if delta > 0:
                form = form["future"]
            else:
                form = form["past"]

        return form.format(abs(delta))


class EsperantoLocale(Locale):
    names = ["eo", "eo-xx"]
    past = "antaŭ {0}"
    future = "post {0}"

    timeframes = {
        "now": "nun",
        "second": "sekundo",
        "seconds": "{0} kelkaj sekundoj",
        "minute": "unu minuto",
        "minutes": "{0} minutoj",
        "hour": "un horo",
        "hours": "{0} horoj",
        "day": "unu tago",
        "days": "{0} tagoj",
        "month": "unu monato",
        "months": "{0} monatoj",
        "year": "unu jaro",
        "years": "{0} jaroj",
    }

    month_names = [
        "",
        "januaro",
        "februaro",
        "marto",
        "aprilo",
        "majo",
        "junio",
        "julio",
        "aŭgusto",
        "septembro",
        "oktobro",
        "novembro",
        "decembro",
    ]
    month_abbreviations = [
        "",
        "jan",
        "feb",
        "mar",
        "apr",
        "maj",
        "jun",
        "jul",
        "aŭg",
        "sep",
        "okt",
        "nov",
        "dec",
    ]

    day_names = [
        "",
        "lundo",
        "mardo",
        "merkredo",
        "ĵaŭdo",
        "vendredo",
        "sabato",
        "dimanĉo",
    ]
    day_abbreviations = ["", "lun", "mar", "mer", "ĵaŭ", "ven", "sab", "dim"]

    meridians = {"am": "atm", "pm": "ptm", "AM": "ATM", "PM": "PTM"}

    ordinal_day_re = r"((?P<value>[1-3]?[0-9](?=a))a)"

    def _ordinal_number(self, n: int) -> str:
        return f"{n}a"


class ThaiLocale(Locale):

    names = ["th", "th-th"]

    past = "{0}{1}ที่ผ่านมา"
    future = "ในอีก{1}{0}"

    timeframes = {
        "now": "ขณะนี้",
        "second": "วินาที",
        "seconds": "{0} ไม่กี่วินาที",
        "minute": "1 นาที",
        "minutes": "{0} นาที",
        "hour": "1 ชั่วโมง",
        "hours": "{0} ชั่วโมง",
        "day": "1 วัน",
        "days": "{0} วัน",
        "month": "1 เดือน",
        "months": "{0} เดือน",
        "year": "1 ปี",
        "years": "{0} ปี",
    }

    month_names = [
        "",
        "มกราคม",
        "กุมภาพันธ์",
        "มีนาคม",
        "เมษายน",
        "พฤษภาคม",
        "มิถุนายน",
        "กรกฎาคม",
        "สิงหาคม",
        "กันยายน",
        "ตุลาคม",
        "พฤศจิกายน",
        "ธันวาคม",
    ]
    month_abbreviations = [
        "",
        "ม.ค.",
        "ก.พ.",
        "มี.ค.",
        "เม.ย.",
        "พ.ค.",
        "มิ.ย.",
        "ก.ค.",
        "ส.ค.",
        "ก.ย.",
        "ต.ค.",
        "พ.ย.",
        "ธ.ค.",
    ]

    day_names = ["", "จันทร์", "อังคาร", "พุธ", "พฤหัสบดี", "ศุกร์", "เสาร์", "อาทิตย์"]
    day_abbreviations = ["", "จ", "อ", "พ", "พฤ", "ศ", "ส", "อา"]

    meridians = {"am": "am", "pm": "pm", "AM": "AM", "PM": "PM"}

    BE_OFFSET = 543

    def year_full(self, year: int) -> str:
        """Thai always use Buddhist Era (BE) which is CE + 543"""
        year += self.BE_OFFSET
        return f"{year:04d}"

    def year_abbreviation(self, year: int) -> str:
        """Thai always use Buddhist Era (BE) which is CE + 543"""
        year += self.BE_OFFSET
        return f"{year:04d}"[2:]

    def _format_relative(
        self,
        humanized: str,
        timeframe: TimeFrameLiteral,
        delta: Union[float, int],
    ) -> str:
        """Thai normally doesn't have any space between words"""
        if timeframe == "now":
            return humanized
        space = "" if timeframe == "seconds" else " "
        direction = self.past if delta < 0 else self.future

        return direction.format(humanized, space)


class BengaliLocale(Locale):

    names = ["bn", "bn-bd", "bn-in"]

    past = "{0} আগে"
    future = "{0} পরে"

    timeframes = {
        "now": "এখন",
        "second": "একটি দ্বিতীয়",
        "seconds": "{0} সেকেন্ড",
        "minute": "এক মিনিট",
        "minutes": "{0} মিনিট",
        "hour": "এক ঘণ্টা",
        "hours": "{0} ঘণ্টা",
        "day": "এক দিন",
        "days": "{0} দিন",
        "month": "এক মাস",
        "months": "{0} মাস ",
        "year": "এক বছর",
        "years": "{0} বছর",
    }

    meridians = {"am": "সকাল", "pm": "বিকাল", "AM": "সকাল", "PM": "বিকাল"}

    month_names = [
        "",
        "জানুয়ারি",
        "ফেব্রুয়ারি",
        "মার্চ",
        "এপ্রিল",
        "মে",
        "জুন",
        "জুলাই",
        "আগস্ট",
        "সেপ্টেম্বর",
        "অক্টোবর",
        "নভেম্বর",
        "ডিসেম্বর",
    ]
    month_abbreviations = [
        "",
        "জানু",
        "ফেব",
        "মার্চ",
        "এপ্রি",
        "মে",
        "জুন",
        "জুল",
        "অগা",
        "সেপ্ট",
        "অক্টো",
        "নভে",
        "ডিসে",
    ]

    day_names = [
        "",
        "সোমবার",
        "মঙ্গলবার",
        "বুধবার",
        "বৃহস্পতিবার",
        "শুক্রবার",
        "শনিবার",
        "রবিবার",
    ]
    day_abbreviations = ["", "সোম", "মঙ্গল", "বুধ", "বৃহঃ", "শুক্র", "শনি", "রবি"]

    def _ordinal_number(self, n: int) -> str:
        if n > 10 or n == 0:
            return f"{n}তম"
        if n in [1, 5, 7, 8, 9, 10]:
            return f"{n}ম"
        if n in [2, 3]:
            return f"{n}য়"
        if n == 4:
            return f"{n}র্থ"
        if n == 6:
            return f"{n}ষ্ঠ"


class RomanshLocale(Locale):

    names = ["rm", "rm-ch"]

    past = "avant {0}"
    future = "en {0}"

    timeframes = {
        "now": "en quest mument",
        "second": "in secunda",
        "seconds": "{0} secundas",
        "minute": "ina minuta",
        "minutes": "{0} minutas",
        "hour": "in'ura",
        "hours": "{0} ura",
        "day": "in di",
        "days": "{0} dis",
        "month": "in mais",
        "months": "{0} mais",
        "year": "in onn",
        "years": "{0} onns",
    }

    month_names = [
        "",
        "schaner",
        "favrer",
        "mars",
        "avrigl",
        "matg",
        "zercladur",
        "fanadur",
        "avust",
        "settember",
        "october",
        "november",
        "december",
    ]

    month_abbreviations = [
        "",
        "schan",
        "fav",
        "mars",
        "avr",
        "matg",
        "zer",
        "fan",
        "avu",
        "set",
        "oct",
        "nov",
        "dec",
    ]

    day_names = [
        "",
        "glindesdi",
        "mardi",
        "mesemna",
        "gievgia",
        "venderdi",
        "sonda",
        "dumengia",
    ]

    day_abbreviations = ["", "gli", "ma", "me", "gie", "ve", "so", "du"]


class RomanianLocale(Locale):
    names = ["ro", "ro-ro"]

    past = "{0} în urmă"
    future = "peste {0}"
    and_word = "și"

    timeframes = {
        "now": "acum",
        "second": "o secunda",
        "seconds": "{0} câteva secunde",
        "minute": "un minut",
        "minutes": "{0} minute",
        "hour": "o oră",
        "hours": "{0} ore",
        "day": "o zi",
        "days": "{0} zile",
        "month": "o lună",
        "months": "{0} luni",
        "year": "un an",
        "years": "{0} ani",
    }

    month_names = [
        "",
        "ianuarie",
        "februarie",
        "martie",
        "aprilie",
        "mai",
        "iunie",
        "iulie",
        "august",
        "septembrie",
        "octombrie",
        "noiembrie",
        "decembrie",
    ]
    month_abbreviations = [
        "",
        "ian",
        "febr",
        "mart",
        "apr",
        "mai",
        "iun",
        "iul",
        "aug",
        "sept",
        "oct",
        "nov",
        "dec",
    ]

    day_names = [
        "",
        "luni",
        "marți",
        "miercuri",
        "joi",
        "vineri",
        "sâmbătă",
        "duminică",
    ]
    day_abbreviations = ["", "Lun", "Mar", "Mie", "Joi", "Vin", "Sâm", "Dum"]


class SlovenianLocale(Locale):
    names = ["sl", "sl-si"]

    past = "pred {0}"
    future = "čez {0}"
    and_word = "in"

    timeframes = {
        "now": "zdaj",
        "second": "sekundo",
        "seconds": "{0} sekund",
        "minute": "minuta",
        "minutes": "{0} minutami",
        "hour": "uro",
        "hours": "{0} ur",
        "day": "dan",
        "days": "{0} dni",
        "month": "mesec",
        "months": "{0} mesecev",
        "year": "leto",
        "years": "{0} let",
    }

    meridians = {"am": "", "pm": "", "AM": "", "PM": ""}

    month_names = [
        "",
        "Januar",
        "Februar",
        "Marec",
        "April",
        "Maj",
        "Junij",
        "Julij",
        "Avgust",
        "September",
        "Oktober",
        "November",
        "December",
    ]

    month_abbreviations = [
        "",
        "Jan",
        "Feb",
        "Mar",
        "Apr",
        "Maj",
        "Jun",
        "Jul",
        "Avg",
        "Sep",
        "Okt",
        "Nov",
        "Dec",
    ]

    day_names = [
        "",
        "Ponedeljek",
        "Torek",
        "Sreda",
        "Četrtek",
        "Petek",
        "Sobota",
        "Nedelja",
    ]

    day_abbreviations = ["", "Pon", "Tor", "Sre", "Čet", "Pet", "Sob", "Ned"]


class IndonesianLocale(Locale):

    names = ["id", "id-id"]

    past = "{0} yang lalu"
    future = "dalam {0}"
    and_word = "dan"

    timeframes = {
        "now": "baru saja",
        "second": "1 sebentar",
        "seconds": "{0} detik",
        "minute": "1 menit",
        "minutes": "{0} menit",
        "hour": "1 jam",
        "hours": "{0} jam",
        "day": "1 hari",
        "days": "{0} hari",
        "month": "1 bulan",
        "months": "{0} bulan",
        "year": "1 tahun",
        "years": "{0} tahun",
    }

    meridians = {"am": "", "pm": "", "AM": "", "PM": ""}

    month_names = [
        "",
        "Januari",
        "Februari",
        "Maret",
        "April",
        "Mei",
        "Juni",
        "Juli",
        "Agustus",
        "September",
        "Oktober",
        "November",
        "Desember",
    ]

    month_abbreviations = [
        "",
        "Jan",
        "Feb",
        "Mar",
        "Apr",
        "Mei",
        "Jun",
        "Jul",
        "Ags",
        "Sept",
        "Okt",
        "Nov",
        "Des",
    ]

    day_names = ["", "Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]

    day_abbreviations = [
        "",
        "Senin",
        "Selasa",
        "Rabu",
        "Kamis",
        "Jumat",
        "Sabtu",
        "Minggu",
    ]


class NepaliLocale(Locale):
    names = ["ne", "ne-np"]

    past = "{0} पहिले"
    future = "{0} पछी"

    timeframes = {
        "now": "अहिले",
        "second": "एक सेकेन्ड",
        "seconds": "{0} सेकण्ड",
        "minute": "मिनेट",
        "minutes": "{0} मिनेट",
        "hour": "एक घण्टा",
        "hours": "{0} घण्टा",
        "day": "एक दिन",
        "days": "{0} दिन",
        "month": "एक महिना",
        "months": "{0} महिना",
        "year": "एक बर्ष",
        "years": "बर्ष",
    }

    meridians = {"am": "पूर्वाह्न", "pm": "अपरान्ह", "AM": "पूर्वाह्न", "PM": "अपरान्ह"}

    month_names = [
        "",
        "जनवरी",
        "फेब्रुअरी",
        "मार्च",
        "एप्रील",
        "मे",
        "जुन",
        "जुलाई",
        "अगष्ट",
        "सेप्टेम्बर",
        "अक्टोबर",
        "नोवेम्बर",
        "डिसेम्बर",
    ]
    month_abbreviations = [
        "",
        "जन",
        "फेब",
        "मार्च",
        "एप्रील",
        "मे",
        "जुन",
        "जुलाई",
        "अग",
        "सेप",
        "अक्ट",
        "नोव",
        "डिस",
    ]

    day_names = [
        "",
        "सोमवार",
        "मंगलवार",
        "बुधवार",
        "बिहिवार",
        "शुक्रवार",
        "शनिवार",
        "आइतवार",
    ]

    day_abbreviations = ["", "सोम", "मंगल", "बुध", "बिहि", "शुक्र", "शनि", "आइत"]


class EstonianLocale(Locale):
    names = ["ee", "et"]

    past = "{0} tagasi"
    future = "{0} pärast"
    and_word = "ja"

    timeframes: ClassVar[Mapping[TimeFrameLiteral, Mapping[str, str]]] = {
        "now": {"past": "just nüüd", "future": "just nüüd"},
        "second": {"past": "üks sekund", "future": "ühe sekundi"},
        "seconds": {"past": "{0} sekundit", "future": "{0} sekundi"},
        "minute": {"past": "üks minut", "future": "ühe minuti"},
        "minutes": {"past": "{0} minutit", "future": "{0} minuti"},
        "hour": {"past": "tund aega", "future": "tunni aja"},
        "hours": {"past": "{0} tundi", "future": "{0} tunni"},
        "day": {"past": "üks päev", "future": "ühe päeva"},
        "days": {"past": "{0} päeva", "future": "{0} päeva"},
        "month": {"past": "üks kuu", "future": "ühe kuu"},
        "months": {"past": "{0} kuud", "future": "{0} kuu"},
        "year": {"past": "üks aasta", "future": "ühe aasta"},
        "years": {"past": "{0} aastat", "future": "{0} aasta"},
    }

    month_names = [
        "",
        "Jaanuar",
        "Veebruar",
        "Märts",
        "Aprill",
        "Mai",
        "Juuni",
        "Juuli",
        "August",
        "September",
        "Oktoober",
        "November",
        "Detsember",
    ]
    month_abbreviations = [
        "",
        "Jan",
        "Veb",
        "Mär",
        "Apr",
        "Mai",
        "Jun",
        "Jul",
        "Aug",
        "Sep",
        "Okt",
        "Nov",
        "Dets",
    ]

    day_names = [
        "",
        "Esmaspäev",
        "Teisipäev",
        "Kolmapäev",
        "Neljapäev",
        "Reede",
        "Laupäev",
        "Pühapäev",
    ]
    day_abbreviations = ["", "Esm", "Teis", "Kolm", "Nelj", "Re", "Lau", "Püh"]

    def _format_timeframe(
        self, timeframe: TimeFrameLiteral, delta: Union[float, int]
    ) -> str:
        form = self.timeframes[timeframe]
        if delta > 0:
            _form = form["future"]
        else:
            _form = form["past"]
        return _form.format(abs(delta))


class LatvianLocale(Locale):

    names = ["lv", "lv-lv"]

    past = "pirms {0}"
    future = "pēc {0}"
    and_word = "un"

    timeframes: ClassVar[Mapping[TimeFrameLiteral, Union[str, Mapping[str, str]]]] = {
        "now": "tagad",
        "second": "sekundes",
        "seconds": "{0} sekundēm",
        "minute": "minūtes",
        "minutes": "{0} minūtēm",
        "hour": "stundas",
        "hours": "{0} stundām",
        "day": "dienas",
        "days": "{0} dienām",
        "week": "nedēļas",
        "weeks": "{0} nedēļām",
        "month": "mēneša",
        "months": "{0} mēnešiem",
        "year": "gada",
        "years": "{0} gadiem",
    }

    month_names = [
        "",
        "janvāris",
        "februāris",
        "marts",
        "aprīlis",
        "maijs",
        "jūnijs",
        "jūlijs",
        "augusts",
        "septembris",
        "oktobris",
        "novembris",
        "decembris",
    ]

    month_abbreviations = [
        "",
        "jan",
        "feb",
        "marts",
        "apr",
        "maijs",
        "jūnijs",
        "jūlijs",
        "aug",
        "sept",
        "okt",
        "nov",
        "dec",
    ]

    day_names = [
        "",
        "pirmdiena",
        "otrdiena",
        "trešdiena",
        "ceturtdiena",
        "piektdiena",
        "sestdiena",
        "svētdiena",
    ]

    day_abbreviations = [
        "",
        "pi",
        "ot",
        "tr",
        "ce",
        "pi",
        "se",
        "sv",
    ]


class SwahiliLocale(Locale):

    names = [
        "sw",
        "sw-ke",
        "sw-tz",
    ]

    past = "{0} iliyopita"
    future = "muda wa {0}"
    and_word = "na"

    timeframes = {
        "now": "sasa hivi",
        "second": "sekunde",
        "seconds": "sekunde {0}",
        "minute": "dakika moja",
        "minutes": "dakika {0}",
        "hour": "saa moja",
        "hours": "saa {0}",
        "day": "siku moja",
        "days": "siku {0}",
        "week": "wiki moja",
        "weeks": "wiki {0}",
        "month": "mwezi moja",
        "months": "miezi {0}",
        "year": "mwaka moja",
        "years": "miaka {0}",
    }

    meridians = {"am": "asu", "pm": "mch", "AM": "ASU", "PM": "MCH"}

    month_names = [
        "",
        "Januari",
        "Februari",
        "Machi",
        "Aprili",
        "Mei",
        "Juni",
        "Julai",
        "Agosti",
        "Septemba",
        "Oktoba",
        "Novemba",
        "Desemba",
    ]
    month_abbreviations = [
        "",
        "Jan",
        "Feb",
        "Mac",
        "Apr",
        "Mei",
        "Jun",
        "Jul",
        "Ago",
        "Sep",
        "Okt",
        "Nov",
        "Des",
    ]

    day_names = [
        "",
        "Jumatatu",
        "Jumanne",
        "Jumatano",
        "Alhamisi",
        "Ijumaa",
        "Jumamosi",
        "Jumapili",
    ]
    day_abbreviations = [
        "",
        "Jumatatu",
        "Jumanne",
        "Jumatano",
        "Alhamisi",
        "Ijumaa",
        "Jumamosi",
        "Jumapili",
    ]


class CroatianLocale(Locale):

    names = ["hr", "hr-hr"]

    past = "prije {0}"
    future = "za {0}"
    and_word = "i"

    timeframes: ClassVar[Mapping[TimeFrameLiteral, Union[str, Mapping[str, str]]]] = {
        "now": "upravo sad",
        "second": "sekundu",
        "seconds": {"double": "{0} sekunde", "higher": "{0} sekundi"},
        "minute": "minutu",
        "minutes": {"double": "{0} minute", "higher": "{0} minuta"},
        "hour": "sat",
        "hours": {"double": "{0} sata", "higher": "{0} sati"},
        "day": "jedan dan",
        "days": {"double": "{0} dana", "higher": "{0} dana"},
        "week": "tjedan",
        "weeks": {"double": "{0} tjedna", "higher": "{0} tjedana"},
        "month": "mjesec",
        "months": {"double": "{0} mjeseca", "higher": "{0} mjeseci"},
        "year": "godinu",
        "years": {"double": "{0} godine", "higher": "{0} godina"},
    }

    month_names = [
        "",
        "siječanj",
        "veljača",
        "ožujak",
        "travanj",
        "svibanj",
        "lipanj",
        "srpanj",
        "kolovoz",
        "rujan",
        "listopad",
        "studeni",
        "prosinac",
    ]

    month_abbreviations = [
        "",
        "siječ",
        "velj",
        "ožuj",
        "trav",
        "svib",
        "lip",
        "srp",
        "kol",
        "ruj",
        "list",
        "stud",
        "pros",
    ]

    day_names = [
        "",
        "ponedjeljak",
        "utorak",
        "srijeda",
        "četvrtak",
        "petak",
        "subota",
        "nedjelja",
    ]

    day_abbreviations = [
        "",
        "po",
        "ut",
        "sr",
        "če",
        "pe",
        "su",
        "ne",
    ]

    def _format_timeframe(
        self, timeframe: TimeFrameLiteral, delta: Union[float, int]
    ) -> str:
        form = self.timeframes[timeframe]
        delta = abs(delta)
        if isinstance(form, Mapping):
            if 1 < delta <= 4:
                form = form["double"]
            else:
                form = form["higher"]

        return form.format(delta)


class LatinLocale(Locale):

    names = ["la", "la-va"]

    past = "ante {0}"
    future = "in {0}"
    and_word = "et"

    timeframes: ClassVar[Mapping[TimeFrameLiteral, Union[str, Mapping[str, str]]]] = {
        "now": "nunc",
        "second": "secundum",
        "seconds": "{0} secundis",
        "minute": "minutam",
        "minutes": "{0} minutis",
        "hour": "horam",
        "hours": "{0} horas",
        "day": "diem",
        "days": "{0} dies",
        "week": "hebdomadem",
        "weeks": "{0} hebdomades",
        "month": "mensem",
        "months": "{0} mensis",
        "year": "annum",
        "years": "{0} annos",
    }

    month_names = [
        "",
        "Ianuarius",
        "Februarius",
        "Martius",
        "Aprilis",
        "Maius",
        "Iunius",
        "Iulius",
        "Augustus",
        "September",
        "October",
        "November",
        "December",
    ]

    month_abbreviations = [
        "",
        "Ian",
        "Febr",
        "Mart",
        "Apr",
        "Mai",
        "Iun",
        "Iul",
        "Aug",
        "Sept",
        "Oct",
        "Nov",
        "Dec",
    ]

    day_names = [
        "",
        "dies Lunae",
        "dies Martis",
        "dies Mercurii",
        "dies Iovis",
        "dies Veneris",
        "dies Saturni",
        "dies Solis",
    ]

    day_abbreviations = [
        "",
        "dies Lunae",
        "dies Martis",
        "dies Mercurii",
        "dies Iovis",
        "dies Veneris",
        "dies Saturni",
        "dies Solis",
    ]


class LithuanianLocale(Locale):

    names = ["lt", "lt-lt"]

    past = "prieš {0}"
    future = "po {0}"
    and_word = "ir"

    timeframes: ClassVar[Mapping[TimeFrameLiteral, Union[str, Mapping[str, str]]]] = {
        "now": "dabar",
        "second": "sekundės",
        "seconds": "{0} sekundžių",
        "minute": "minutės",
        "minutes": "{0} minučių",
        "hour": "valandos",
        "hours": "{0} valandų",
        "day": "dieną",
        "days": "{0} dienų",
        "week": "savaitės",
        "weeks": "{0} savaičių",
        "month": "mėnesio",
        "months": "{0} mėnesių",
        "year": "metų",
        "years": "{0} metų",
    }

    month_names = [
        "",
        "sausis",
        "vasaris",
        "kovas",
        "balandis",
        "gegužė",
        "birželis",
        "liepa",
        "rugpjūtis",
        "rugsėjis",
        "spalis",
        "lapkritis",
        "gruodis",
    ]

    month_abbreviations = [
        "",
        "saus",
        "vas",
        "kovas",
        "bal",
        "geg",
        "birž",
        "liepa",
        "rugp",
        "rugs",
        "spalis",
        "lapkr",
        "gr",
    ]

    day_names = [
        "",
        "pirmadienis",
        "antradienis",
        "trečiadienis",
        "ketvirtadienis",
        "penktadienis",
        "šeštadienis",
        "sekmadienis",
    ]

    day_abbreviations = [
        "",
        "pi",
        "an",
        "tr",
        "ke",
        "pe",
        "še",
        "se",
    ]


class MalayLocale(Locale):

    names = ["ms", "ms-my", "ms-bn"]

    past = "{0} yang lalu"
    future = "dalam {0}"
    and_word = "dan"

    timeframes: ClassVar[Mapping[TimeFrameLiteral, Union[str, Mapping[str, str]]]] = {
        "now": "sekarang",
        "second": "saat",
        "seconds": "{0} saat",
        "minute": "minit",
        "minutes": "{0} minit",
        "hour": "jam",
        "hours": "{0} jam",
        "day": "hari",
        "days": "{0} hari",
        "week": "minggu",
        "weeks": "{0} minggu",
        "month": "bulan",
        "months": "{0} bulan",
        "year": "tahun",
        "years": "{0} tahun",
    }

    month_names = [
        "",
        "Januari",
        "Februari",
        "Mac",
        "April",
        "Mei",
        "Jun",
        "Julai",
        "Ogos",
        "September",
        "Oktober",
        "November",
        "Disember",
    ]

    month_abbreviations = [
        "",
        "Jan.",
        "Feb.",
        "Mac",
        "Apr.",
        "Mei",
        "Jun",
        "Julai",
        "Og.",
        "Sept.",
        "Okt.",
        "Nov.",
        "Dis.",
    ]

    day_names = [
        "",
        "Isnin",
        "Selasa",
        "Rabu",
        "Khamis",
        "Jumaat",
        "Sabtu",
        "Ahad ",
    ]

    day_abbreviations = [
        "",
        "Isnin",
        "Selasa",
        "Rabu",
        "Khamis",
        "Jumaat",
        "Sabtu",
        "Ahad ",
    ]
