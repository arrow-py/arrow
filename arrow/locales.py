# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import inspect
import sys
from math import trunc


def get_locale(name):
    """Returns an appropriate :class:`Locale <arrow.locales.Locale>`
    corresponding to an inpute locale name.

    :param name: the name of the locale.

    """

    locale_cls = _locales.get(name.lower())

    if locale_cls is None:
        raise ValueError("Unsupported locale '{}'".format(name))

    return locale_cls()


# base locale type.


class Locale(object):
    """ Represents locale-specific data and functionality. """

    names = []

    timeframes = {
        "now": "",
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

    meridians = {"am": "", "pm": "", "AM": "", "PM": ""}

    past = None
    future = None

    month_names = []
    month_abbreviations = []

    day_names = []
    day_abbreviations = []

    ordinal_day_re = r"(\d+)"

    def __init__(self):

        self._month_name_to_ordinal = None

    def describe(self, timeframe, delta=0, only_distance=False):
        """ Describes a delta within a timeframe in plain language.

        :param timeframe: a string representing a timeframe.
        :param delta: a quantity representing a delta in a timeframe.
        :param only_distance: return only distance eg: "11 seconds" without "in" or "ago" keywords
        """

        humanized = self._format_timeframe(timeframe, delta)
        if not only_distance:
            humanized = self._format_relative(humanized, timeframe, delta)

        return humanized

    def day_name(self, day):
        """ Returns the day name for a specified day of the week.

        :param day: the ``int`` day of the week (1-7).

        """

        return self.day_names[day]

    def day_abbreviation(self, day):
        """ Returns the day abbreviation for a specified day of the week.

        :param day: the ``int`` day of the week (1-7).

        """

        return self.day_abbreviations[day]

    def month_name(self, month):
        """ Returns the month name for a specified month of the year.

        :param month: the ``int`` month of the year (1-12).

        """

        return self.month_names[month]

    def month_abbreviation(self, month):
        """ Returns the month abbreviation for a specified month of the year.

        :param month: the ``int`` month of the year (1-12).

        """

        return self.month_abbreviations[month]

    def month_number(self, name):
        """ Returns the month number for a month specified by name or abbreviation.

        :param name: the month name or abbreviation.

        """

        if self._month_name_to_ordinal is None:
            self._month_name_to_ordinal = self._name_to_ordinal(self.month_names)
            self._month_name_to_ordinal.update(
                self._name_to_ordinal(self.month_abbreviations)
            )

        return self._month_name_to_ordinal.get(name)

    def year_full(self, year):
        """  Returns the year for specific locale if available

        :param name: the ``int`` year (4-digit)
        """
        return "{:04d}".format(year)

    def year_abbreviation(self, year):
        """ Returns the year for specific locale if available

        :param name: the ``int`` year (4-digit)
        """
        return "{:04d}".format(year)[2:]

    def meridian(self, hour, token):
        """ Returns the meridian indicator for a specified hour and format token.

        :param hour: the ``int`` hour of the day.
        :param token: the format token.
        """

        if token == "a":
            return self.meridians["am"] if hour < 12 else self.meridians["pm"]
        if token == "A":
            return self.meridians["AM"] if hour < 12 else self.meridians["PM"]

    def ordinal_number(self, n):
        """ Returns the ordinal format of a given integer

        :param n: an integer
        """
        return self._ordinal_number(n)

    def _ordinal_number(self, n):
        return "{}".format(n)

    def _name_to_ordinal(self, lst):
        return dict(map(lambda i: (i[1].lower(), i[0] + 1), enumerate(lst[1:])))

    def _format_timeframe(self, timeframe, delta):
        return self.timeframes[timeframe].format(trunc(abs(delta)))

    def _format_relative(self, humanized, timeframe, delta):

        if timeframe == "now":
            return humanized

        direction = self.past if delta < 0 else self.future

        return direction.format(humanized)


# base locale type implementations.


class EnglishLocale(Locale):

    names = [
        "en",
        "en_us",
        "en_gb",
        "en_au",
        "en_be",
        "en_jp",
        "en_za",
        "en_ca",
        "en_ph",
    ]

    past = "{0} ago"
    future = "in {0}"

    timeframes = {
        "now": "just now",
        "seconds": "seconds",
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

    def _ordinal_number(self, n):
        if n % 100 not in (11, 12, 13):
            remainder = abs(n) % 10
            if remainder == 1:
                return "{}st".format(n)
            elif remainder == 2:
                return "{}nd".format(n)
            elif remainder == 3:
                return "{}rd".format(n)
        return "{}th".format(n)

    def describe(self, timeframe, delta=0, only_distance=False):
        """ Describes a delta within a timeframe in plain language.

        :param timeframe: a string representing a timeframe.
        :param delta: a quantity representing a delta in a timeframe.
        :param only_distance: return only distance eg: "11 seconds" without "in" or "ago" keywords
        """

        humanized = super(EnglishLocale, self).describe(timeframe, delta, only_distance)
        if only_distance and timeframe == "now":
            humanized = "instantly"

        return humanized


class ItalianLocale(Locale):
    names = ["it", "it_it"]
    past = "{0} fa"
    future = "tra {0}"

    timeframes = {
        "now": "adesso",
        "seconds": "qualche secondo",
        "minute": "un minuto",
        "minutes": "{0} minuti",
        "hour": "un'ora",
        "hours": "{0} ore",
        "day": "un giorno",
        "days": "{0} giorni",
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

    def _ordinal_number(self, n):
        return "{}º".format(n)


class SpanishLocale(Locale):
    names = ["es", "es_es"]
    past = "hace {0}"
    future = "en {0}"

    timeframes = {
        "now": "ahora",
        "seconds": "segundos",
        "minute": "un minuto",
        "minutes": "{0} minutos",
        "hour": "una hora",
        "hours": "{0} horas",
        "day": "un día",
        "days": "{0} días",
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

    def _ordinal_number(self, n):
        return "{}º".format(n)


class FrenchLocale(Locale):
    names = ["fr", "fr_fr"]
    past = "il y a {0}"
    future = "dans {0}"

    timeframes = {
        "now": "maintenant",
        "seconds": "quelques secondes",
        "minute": "une minute",
        "minutes": "{0} minutes",
        "hour": "une heure",
        "hours": "{0} heures",
        "day": "un jour",
        "days": "{0} jours",
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

    def _ordinal_number(self, n):
        if abs(n) == 1:
            return "{}er".format(n)
        return "{}e".format(n)


class GreekLocale(Locale):

    names = ["el", "el_gr"]

    past = "{0} πριν"
    future = "σε {0}"

    timeframes = {
        "now": "τώρα",
        "seconds": "δευτερόλεπτα",
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

    names = ["ja", "ja_jp"]

    past = "{0}前"
    future = "{0}後"

    timeframes = {
        "now": "現在",
        "seconds": "数秒",
        "minute": "1分",
        "minutes": "{0}分",
        "hour": "1時間",
        "hours": "{0}時間",
        "day": "1日",
        "days": "{0}日",
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

    names = ["sv", "sv_se"]

    past = "för {0} sen"
    future = "om {0}"

    timeframes = {
        "now": "just nu",
        "seconds": "några sekunder",
        "minute": "en minut",
        "minutes": "{0} minuter",
        "hour": "en timme",
        "hours": "{0} timmar",
        "day": "en dag",
        "days": "{0} dagar",
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

    names = ["fi", "fi_fi"]

    # The finnish grammar is very complex, and its hard to convert
    # 1-to-1 to something like English.

    past = "{0} sitten"
    future = "{0} kuluttua"

    timeframes = {
        "now": ["juuri nyt", "juuri nyt"],
        "seconds": ["muutama sekunti", "muutaman sekunnin"],
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

    def _format_timeframe(self, timeframe, delta):
        return (
            self.timeframes[timeframe][0].format(abs(delta)),
            self.timeframes[timeframe][1].format(abs(delta)),
        )

    def _format_relative(self, humanized, timeframe, delta):
        if timeframe == "now":
            return humanized[0]

        direction = self.past if delta < 0 else self.future
        which = 0 if delta < 0 else 1

        return direction.format(humanized[which])

    def _ordinal_number(self, n):
        return "{}.".format(n)


class ChineseCNLocale(Locale):

    names = ["zh", "zh_cn"]

    past = "{0}前"
    future = "{0}后"

    timeframes = {
        "now": "刚才",
        "seconds": "几秒",
        "minute": "1分钟",
        "minutes": "{0}分钟",
        "hour": "1小时",
        "hours": "{0}小时",
        "day": "1天",
        "days": "{0}天",
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

    names = ["zh_tw"]

    past = "{0}前"
    future = "{0}後"

    timeframes = {
        "now": "剛才",
        "seconds": "幾秒",
        "minute": "1分鐘",
        "minutes": "{0}分鐘",
        "hour": "1小時",
        "hours": "{0}小時",
        "day": "1天",
        "days": "{0}天",
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

    day_names = ["", "周一", "周二", "周三", "周四", "周五", "周六", "周日"]
    day_abbreviations = ["", "一", "二", "三", "四", "五", "六", "日"]


class KoreanLocale(Locale):

    names = ["ko", "ko_kr"]

    past = "{0} 전"
    future = "{0} 후"

    timeframes = {
        "now": "지금",
        "seconds": "몇 초",
        "minute": "1분",
        "minutes": "{0}분",
        "hour": "1시간",
        "hours": "{0}시간",
        "day": "1일",
        "days": "{0}일",
        "month": "1개월",
        "months": "{0}개월",
        "year": "1년",
        "years": "{0}년",
    }

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


# derived locale types & implementations.
class DutchLocale(Locale):

    names = ["nl", "nl_nl"]

    past = "{0} geleden"
    future = "over {0}"

    timeframes = {
        "now": "nu",
        "seconds": "seconden",
        "minute": "een minuut",
        "minutes": "{0} minuten",
        "hour": "een uur",
        "hours": "{0} uur",
        "day": "een dag",
        "days": "{0} dagen",
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
    def _format_timeframe(self, timeframe, delta):

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

    names = ["be", "be_by"]

    past = "{0} таму"
    future = "праз {0}"

    timeframes = {
        "now": "зараз",
        "seconds": "некалькі секунд",
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

    names = ["pl", "pl_pl"]

    past = "{0} temu"
    future = "za {0}"

    timeframes = {
        "now": "teraz",
        "seconds": "kilka sekund",
        "minute": "minutę",
        "minutes": ["{0} minut", "{0} minuty", "{0} minut"],
        "hour": "godzina",
        "hours": ["{0} godzin", "{0} godziny", "{0} godzin"],
        "day": "dzień",
        "days": ["{0} dzień", "{0} dni", "{0} dni"],
        "month": "miesiąc",
        "months": ["{0} miesiąc", "{0} miesiące", "{0} miesięcy"],
        "year": "rok",
        "years": ["{0} rok", "{0} lata", "{0} lat"],
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

    names = ["ru", "ru_ru"]

    past = "{0} назад"
    future = "через {0}"

    timeframes = {
        "now": "сейчас",
        "seconds": "несколько секунд",
        "minute": "минуту",
        "minutes": ["{0} минуту", "{0} минуты", "{0} минут"],
        "hour": "час",
        "hours": ["{0} час", "{0} часа", "{0} часов"],
        "day": "день",
        "days": ["{0} день", "{0} дня", "{0} дней"],
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

    names = ["af", "af_nl"]

    past = "{0} gelede"
    future = "in {0}"

    timeframes = {
        "now": "nou",
        "seconds": "sekondes",
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

    names = ["bg", "bg_BG"]

    past = "{0} назад"
    future = "напред {0}"

    timeframes = {
        "now": "сега",
        "seconds": "няколко секунди",
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

    names = ["ua", "uk_ua"]

    past = "{0} тому"
    future = "за {0}"

    timeframes = {
        "now": "зараз",
        "seconds": "кілька секунд",
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
    names = ["mk", "mk_mk"]

    past = "пред {0}"
    future = "за {0}"

    timeframes = {
        "now": "сега",
        "seconds": "секунди",
        "minute": "една минута",
        "minutes": ["{0} минута", "{0} минути", "{0} минути"],
        "hour": "еден саат",
        "hours": ["{0} саат", "{0} саати", "{0} саати"],
        "day": "еден ден",
        "days": ["{0} ден", "{0} дена", "{0} дена"],
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
        "Јан.",
        " Фев.",
        " Мар.",
        " Апр.",
        " Мај",
        " Јун.",
        " Јул.",
        " Авг.",
        " Септ.",
        " Окт.",
        " Ноем.",
        " Декем.",
    ]

    day_names = [
        "",
        "Понеделник",
        " Вторник",
        " Среда",
        " Четврток",
        " Петок",
        " Сабота",
        " Недела",
    ]
    day_abbreviations = [
        "",
        "Пон.",
        " Вт.",
        " Сре.",
        " Чет.",
        " Пет.",
        " Саб.",
        " Нед.",
    ]


class DeutschBaseLocale(Locale):

    past = "vor {0}"
    future = "in {0}"

    timeframes = {
        "now": "gerade eben",
        "seconds": "Sekunden",
        "minute": "einer Minute",
        "minutes": "{0} Minuten",
        "hour": "einer Stunde",
        "hours": "{0} Stunden",
        "day": "einem Tag",
        "days": "{0} Tagen",
        "month": "einem Monat",
        "months": "{0} Monaten",
        "year": "einem Jahr",
        "years": "{0} Jahren",
    }

    timeframes_only_distance = timeframes.copy()
    timeframes_only_distance["minute"] = "eine Minute"
    timeframes_only_distance["hour"] = "eine Stunde"
    timeframes_only_distance["day"] = "ein Tag"
    timeframes_only_distance["month"] = "ein Monat"
    timeframes_only_distance["year"] = "ein Jahr"

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

    def _ordinal_number(self, n):
        return "{}.".format(n)

    def describe(self, timeframe, delta=0, only_distance=False):
        """ Describes a delta within a timeframe in plain language.

        :param timeframe: a string representing a timeframe.
        :param delta: a quantity representing a delta in a timeframe.
        :param only_distance: return only distance eg: "11 seconds" without "in" or "ago" keywords
        """

        humanized = self.timeframes_only_distance[timeframe].format(trunc(abs(delta)))

        if not only_distance:
            humanized = self._format_timeframe(timeframe, delta)
            humanized = self._format_relative(humanized, timeframe, delta)

        return humanized


class GermanLocale(DeutschBaseLocale, Locale):

    names = ["de", "de_de"]


class AustrianLocale(DeutschBaseLocale, Locale):

    names = ["de_at"]

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

    names = ["nb", "nb_no"]

    past = "for {0} siden"
    future = "om {0}"

    timeframes = {
        "now": "nå nettopp",
        "seconds": "noen sekunder",
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

    names = ["nn", "nn_no"]

    past = "for {0} sidan"
    future = "om {0}"

    timeframes = {
        "now": "no nettopp",
        "seconds": "nokre sekund",
        "minute": "ett minutt",
        "minutes": "{0} minutt",
        "hour": "ein time",
        "hours": "{0} timar",
        "day": "ein dag",
        "days": "{0} dagar",
        "month": "en månad",
        "months": "{0} månader",
        "year": "eit år",
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
    names = ["pt", "pt_pt"]

    past = "há {0}"
    future = "em {0}"

    timeframes = {
        "now": "agora",
        "seconds": "segundos",
        "minute": "um minuto",
        "minutes": "{0} minutos",
        "hour": "uma hora",
        "hours": "{0} horas",
        "day": "um dia",
        "days": "{0} dias",
        "month": "um mês",
        "months": "{0} meses",
        "year": "um ano",
        "years": "{0} anos",
    }

    month_names = [
        "",
        "janeiro",
        "fevereiro",
        "março",
        "abril",
        "maio",
        "junho",
        "julho",
        "agosto",
        "setembro",
        "outubro",
        "novembro",
        "dezembro",
    ]
    month_abbreviations = [
        "",
        "jan",
        "fev",
        "mar",
        "abr",
        "maio",
        "jun",
        "jul",
        "ago",
        "set",
        "out",
        "nov",
        "dez",
    ]

    day_names = [
        "",
        "segunda-feira",
        "terça-feira",
        "quarta-feira",
        "quinta-feira",
        "sexta-feira",
        "sábado",
        "domingo",
    ]
    day_abbreviations = ["", "seg", "ter", "qua", "qui", "sex", "sab", "dom"]


class BrazilianPortugueseLocale(PortugueseLocale):
    names = ["pt_br"]

    past = "faz {0}"

    future = "em {0}"

    timeframes = {
        "now": "agora",
        "seconds": "segundos",
        "minute": "um minuto",
        "minutes": "{0} minutos",
        "hour": "uma hora",
        "hours": "{0} horas",
        "day": "um dia",
        "days": "{0} dias",
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


class TagalogLocale(Locale):

    names = ["tl", "tl_ph"]

    past = "nakaraang {0}"
    future = "{0} mula ngayon"

    timeframes = {
        "now": "ngayon lang",
        "seconds": "segundo",
        "minute": "isang minuto",
        "minutes": "{0} minuto",
        "hour": "isang oras",
        "hours": "{0} oras",
        "day": "isang araw",
        "days": "{0} araw",
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

    def _ordinal_number(self, n):
        return "ika-{}".format(n)


class VietnameseLocale(Locale):

    names = ["vi", "vi_vn"]

    past = "{0} trước"
    future = "{0} nữa"

    timeframes = {
        "now": "hiện tại",
        "seconds": "giây",
        "minute": "một phút",
        "minutes": "{0} phút",
        "hour": "một giờ",
        "hours": "{0} giờ",
        "day": "một ngày",
        "days": "{0} ngày",
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

    names = ["tr", "tr_tr"]

    past = "{0} önce"
    future = "{0} sonra"

    timeframes = {
        "now": "şimdi",
        "seconds": "saniye",
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

    names = ["az", "az_az"]

    past = "{0} əvvəl"
    future = "{0} sonra"

    timeframes = {
        "now": "indi",
        "seconds": "saniyə",
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
        "ar_ae",
        "ar_bh",
        "ar_dj",
        "ar_eg",
        "ar_eh",
        "ar_er",
        "ar_km",
        "ar_kw",
        "ar_ly",
        "ar_om",
        "ar_qa",
        "ar_sa",
        "ar_sd",
        "ar_so",
        "ar_ss",
        "ar_td",
        "ar_ye",
    ]

    past = "منذ {0}"
    future = "خلال {0}"

    timeframes = {
        "now": "الآن",
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

    def _format_timeframe(self, timeframe, delta):
        form = self.timeframes[timeframe]
        delta = abs(delta)
        if isinstance(form, dict):
            if delta == 2:
                form = form["double"]
            elif delta > 2 and delta <= 10:
                form = form["ten"]
            else:
                form = form["higher"]

        return form.format(delta)


class LevantArabicLocale(ArabicLocale):
    names = ["ar_iq", "ar_jo", "ar_lb", "ar_ps", "ar_sy"]
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
    names = ["ar_tn", "ar_dz"]
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
    names = ["ar_mr"]
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
    names = ["ar_ma"]
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
    def _format_timeframe(self, timeframe, delta):

        timeframe = self.timeframes[timeframe]
        if delta < 0:
            timeframe = timeframe[0]
        elif delta > 0:
            timeframe = timeframe[1]

        return timeframe.format(abs(delta))

    names = ["is", "is_is"]

    past = "fyrir {0} síðan"
    future = "eftir {0}"

    timeframes = {
        "now": "rétt í þessu",
        "seconds": ("nokkrum sekúndum", "nokkrar sekúndur"),
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

    names = ["da", "da_dk"]

    past = "for {0} siden"
    future = "efter {0}"

    timeframes = {
        "now": "lige nu",
        "seconds": "et par sekunder",
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
        "seconds": "സെക്കന്റ്‌",
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
        "seconds": "सेकंड्",
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
        "फ़र",
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
    names = ["cs", "cs_cz"]

    timeframes = {
        "now": "Teď",
        "seconds": {"past": "{0} sekundami", "future": ["{0} sekundy", "{0} sekund"]},
        "minute": {"past": "minutou", "future": "minutu", "zero": "{0} minut"},
        "minutes": {"past": "{0} minutami", "future": ["{0} minuty", "{0} minut"]},
        "hour": {"past": "hodinou", "future": "hodinu", "zero": "{0} hodin"},
        "hours": {"past": "{0} hodinami", "future": ["{0} hodiny", "{0} hodin"]},
        "day": {"past": "dnem", "future": "den", "zero": "{0} dnů"},
        "days": {"past": "{0} dny", "future": ["{0} dny", "{0} dnů"]},
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

    def _format_timeframe(self, timeframe, delta):
        """Czech aware time frame format function, takes into account
        the differences between past and future forms."""
        form = self.timeframes[timeframe]
        if isinstance(form, dict):
            if delta == 0:
                form = form["zero"]  # And *never* use 0 in the singular!
            elif delta > 0:
                form = form["future"]
            else:
                form = form["past"]
        delta = abs(delta)

        if isinstance(form, list):
            if 2 <= delta % 10 <= 4 and (delta % 100 < 10 or delta % 100 >= 20):
                form = form[0]
            else:
                form = form[1]

        return form.format(delta)


class SlovakLocale(Locale):
    names = ["sk", "sk_sk"]

    timeframes = {
        "now": "Teraz",
        "seconds": {"past": "pár sekundami", "future": ["{0} sekundy", "{0} sekúnd"]},
        "minute": {"past": "minútou", "future": "minútu", "zero": "{0} minút"},
        "minutes": {"past": "{0} minútami", "future": ["{0} minúty", "{0} minút"]},
        "hour": {"past": "hodinou", "future": "hodinu", "zero": "{0} hodín"},
        "hours": {"past": "{0} hodinami", "future": ["{0} hodiny", "{0} hodín"]},
        "day": {"past": "dňom", "future": "deň", "zero": "{0} dní"},
        "days": {"past": "{0} dňami", "future": ["{0} dni", "{0} dní"]},
        "month": {"past": "mesiacom", "future": "mesiac", "zero": "{0} mesiacov"},
        "months": {"past": "{0} mesiacmi", "future": ["{0} mesiace", "{0} mesiacov"]},
        "year": {"past": "rokom", "future": "rok", "zero": "{0} rokov"},
        "years": {"past": "{0} rokmi", "future": ["{0} roky", "{0} rokov"]},
    }

    past = "Pred {0}"
    future = "O {0}"

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

    def _format_timeframe(self, timeframe, delta):
        """Slovak aware time frame format function, takes into account
        the differences between past and future forms."""
        form = self.timeframes[timeframe]
        if isinstance(form, dict):
            if delta == 0:
                form = form["zero"]  # And *never* use 0 in the singular!
            elif delta > 0:
                form = form["future"]
            else:
                form = form["past"]
        delta = abs(delta)

        if isinstance(form, list):
            if 2 <= delta % 10 <= 4 and (delta % 100 < 10 or delta % 100 >= 20):
                form = form[0]
            else:
                form = form[1]

        return form.format(delta)


class FarsiLocale(Locale):

    names = ["fa", "fa_ir"]

    past = "{0} قبل"
    future = "در {0}"

    timeframes = {
        "now": "اکنون",
        "seconds": "ثانیه",
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

    names = ["he", "he_IL"]

    past = "לפני {0}"
    future = "בעוד {0}"

    timeframes = {
        "now": "הרגע",
        "seconds": "שניות",
        "minute": "דקה",
        "minutes": "{0} דקות",
        "hour": "שעה",
        "hours": "{0} שעות",
        "2-hours": "שעתיים",
        "day": "יום",
        "days": "{0} ימים",
        "2-days": "יומיים",
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

    def _format_timeframe(self, timeframe, delta):
        """Hebrew couple of <timeframe> aware"""
        couple = "2-{}".format(timeframe)
        if abs(delta) == 2 and couple in self.timeframes:
            return self.timeframes[couple].format(abs(delta))
        else:
            return self.timeframes[timeframe].format(abs(delta))


class MarathiLocale(Locale):

    names = ["mr"]

    past = "{0} आधी"
    future = "{0} नंतर"

    timeframes = {
        "now": "सद्य",
        "seconds": "सेकंद",
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


def _map_locales():

    locales = {}

    for _, cls in inspect.getmembers(sys.modules[__name__], inspect.isclass):
        if issubclass(cls, Locale):  # pragma: no branch
            for name in cls.names:
                locales[name.lower()] = cls

    return locales


class CatalanLocale(Locale):
    names = ["ca", "ca_es", "ca_ad", "ca_fr", "ca_it"]
    past = "Fa {0}"
    future = "En {0}"

    timeframes = {
        "now": "Ara mateix",
        "seconds": "segons",
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
        "Gener",
        "Febrer",
        "Març",
        "Abril",
        "Maig",
        "Juny",
        "Juliol",
        "Agost",
        "Setembre",
        "Octubre",
        "Novembre",
        "Desembre",
    ]
    month_abbreviations = [
        "",
        "Gener",
        "Febrer",
        "Març",
        "Abril",
        "Maig",
        "Juny",
        "Juliol",
        "Agost",
        "Setembre",
        "Octubre",
        "Novembre",
        "Desembre",
    ]
    day_names = [
        "",
        "Dilluns",
        "Dimarts",
        "Dimecres",
        "Dijous",
        "Divendres",
        "Dissabte",
        "Diumenge",
    ]
    day_abbreviations = [
        "",
        "Dilluns",
        "Dimarts",
        "Dimecres",
        "Dijous",
        "Divendres",
        "Dissabte",
        "Diumenge",
    ]


class BasqueLocale(Locale):
    names = ["eu", "eu_eu"]
    past = "duela {0}"
    future = "{0}"  # I don't know what's the right phrase in Basque for the future.

    timeframes = {
        "now": "Orain",
        "seconds": "segundu",
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

    names = ["hu", "hu_hu"]

    past = "{0} ezelőtt"
    future = "{0} múlva"

    timeframes = {
        "now": "éppen most",
        "seconds": {"past": "másodpercekkel", "future": "pár másodperc"},
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

    def _format_timeframe(self, timeframe, delta):
        form = self.timeframes[timeframe]

        if isinstance(form, dict):
            if delta > 0:
                form = form["future"]
            else:
                form = form["past"]

        return form.format(abs(delta))


class EsperantoLocale(Locale):
    names = ["eo", "eo_xx"]
    past = "antaŭ {0}"
    future = "post {0}"

    timeframes = {
        "now": "nun",
        "seconds": "kelkaj sekundoj",
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

    def _ordinal_number(self, n):
        return "{}a".format(n)


class ThaiLocale(Locale):

    names = ["th", "th_th"]

    past = "{0}{1}ที่ผ่านมา"
    future = "ในอีก{1}{0}"

    timeframes = {
        "now": "ขณะนี้",
        "seconds": "ไม่กี่วินาที",
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

    def year_full(self, year):
        """Thai always use Buddhist Era (BE) which is CE + 543"""
        year += self.BE_OFFSET
        return "{:04d}".format(year)

    def year_abbreviation(self, year):
        """Thai always use Buddhist Era (BE) which is CE + 543"""
        year += self.BE_OFFSET
        return "{:04d}".format(year)[2:]

    def _format_relative(self, humanized, timeframe, delta):
        """Thai normally doesn't have any space between words"""
        if timeframe == "now":
            return humanized
        space = "" if timeframe == "seconds" else " "
        direction = self.past if delta < 0 else self.future

        return direction.format(humanized, space)


class BengaliLocale(Locale):

    names = ["bn", "bn_bd", "bn_in"]

    past = "{0} আগে"
    future = "{0} পরে"

    timeframes = {
        "now": "এখন",
        "seconds": "সেকেন্ড",
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
        "ফেব্রুয়ারি",
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

    def _ordinal_number(self, n):
        if n > 10 or n == 0:
            return "{}তম".format(n)
        if n in [1, 5, 7, 8, 9, 10]:
            return "{}ম".format(n)
        if n in [2, 3]:
            return "{}য়".format(n)
        if n == 4:
            return "{}র্থ".format(n)
        if n == 6:
            return "{}ষ্ঠ".format(n)


class RomanshLocale(Locale):

    names = ["rm", "rm_ch"]

    past = "avant {0}"
    future = "en {0}"

    timeframes = {
        "now": "en quest mument",
        "seconds": "secundas",
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


class SwissLocale(Locale):

    names = ["de", "de_ch"]

    past = "vor {0}"
    future = "in {0}"

    timeframes = {
        "now": "gerade eben",
        "seconds": "Sekunden",
        "minute": "einer Minute",
        "minutes": "{0} Minuten",
        "hour": "einer Stunde",
        "hours": "{0} Stunden",
        "day": "einem Tag",
        "days": "{0} Tagen",
        "month": "einem Monat",
        "months": "{0} Monaten",
        "year": "einem Jahr",
        "years": "{0} Jahren",
    }

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


class RomanianLocale(Locale):
    names = ["ro", "ro_ro"]

    past = "{0} în urmă"
    future = "peste {0}"

    timeframes = {
        "now": "acum",
        "seconds": "câteva secunde",
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
    names = ["sl", "sl_si"]

    past = "pred {0}"
    future = "čez {0}"

    timeframes = {
        "now": "zdaj",
        "seconds": "sekund",
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

    names = ["id", "id_id"]

    past = "{0} yang lalu"
    future = "dalam {0}"

    timeframes = {
        "now": "baru saja",
        "seconds": "detik",
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
    names = ["ne", "ne_np"]

    past = "{0} पहिले"
    future = "{0} पछी"

    timeframes = {
        "now": "अहिले",
        "seconds": "सेकण्ड",
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

    timeframes = {
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

    def _format_timeframe(self, timeframe, delta):
        form = self.timeframes[timeframe]
        if delta > 0:
            form = form["future"]
        else:
            form = form["past"]
        return form.format(abs(delta))


_locales = _map_locales()
