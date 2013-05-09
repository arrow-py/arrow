# -*- coding: utf-8 -*-
from abc import abstractmethod


class _Locale(object):
    @abstractmethod
    def format_humanize(self, time_delta, time_unit, past):
        """
        Format string to humanise
        :param time_delta: int, representing time_delta, if negative - then it's in past
        :param time_unit: str, representing time_unit of measurement
        :param past: bool flag, showing if this interval in the past
        :return: formatted string with humanized info
        """
        pass


class _BasicLocale(_Locale):
    """
    Locale for languages without complex plurals handling logic
    All you need - just define intervals dict
    """
    intervals = {
        'now': '',
        'seconds': '',
        'minute': '',
        'minutes': '',
        'hour': '',
        'hours': '',
        'day': '',
        'days': '',
        'month': '',
        'months': '',
        'year': '',
        'years': '',

        'past': '',
        'future': '',
    }

    def format_humanize(self, time_delta, time_unit, past):
        """
        Format string to humanise
        :param time_delta: int, representing time_delta, if negative - then it's in past
        :param time_unit: str, representing time_unit of measurement
        :param past: bool flag, showing if this interval in the past
        :return: formatted string with humanized info
        """
        if time_unit == "now":
            return _English.intervals[time_unit]

        if time_delta == 0:
            expr = _English.intervals[time_unit]
        else:
            expr = _English.intervals[time_unit].format(time_delta)
        return _English.intervals['past'].format(expr) if past else _English.intervals['future'].format(expr)


class _English(_BasicLocale):

    intervals = {
        'now': 'just now',
        'seconds': 'seconds',
        'minute': 'a minute',
        'minutes': '{0} minutes',
        'hour': 'an hour',
        'hours': '{0} hours',
        'day': 'a day',
        'days': '{0} days',
        'month': 'a month',
        'months': '{0} months',
        'year': 'a year',
        'years': '{0} years',

        'past': '{0} ago',
        'future': 'in {0}',
    }

class GreekLocale(_BasicLocale):

    intervals = {
        'now': 'τώρα',
        'seconds': 'δευτερόλεπτα',
        'minute': 'ένα λεπτό',
        'minutes': '{0} λεπτά',
        'hour': 'μια ώρα',
        'hours': '{0} ώρες',
        'day': 'μια μέρα',
        'days': '{0} μέρες',
        'month': 'ένα μήνα',
        'months': '{0} μήνες',
        'year': 'ένα χρόνο',
        'years': '{0} χρόνια',

        'past': '{0} πριν',
        'future': 'σε {0}',
    }


class _Russian(_Locale):
    intervals = {
        'now': 'сейчас',
        'seconds': 'несколько секунд',
        'minute': 'минуту',
        'minutes': ['минута', 'минуты', 'минут'],
        'hour': 'час',
        'hours': ['час', 'часа', 'часов'],
        'day': 'день',
        'days': ['день', 'дня', 'дней'],
        'month': 'месяц',
        'months': ['месяц', 'месяца', 'месяцев'],
        'year': 'год',
        'years': ['год', 'года', 'лет'],

        'past': '{0} назад',
        'future': 'через {0}',
    }

    def _chose_plural(self, num, plurals):
        """
        Chose correct plural form fur russian nouns
        :param num: numerator, used with nouns
        :param plurals: three plural forms of nouns
        :return: correct plural form
        """
        if num % 10 == 1 and num % 100 != 11:
            return plurals[0]
        elif 2 <= num % 10 <= 4 and (num % 100 < 10 or num % 100 >= 20):
            return plurals[1]
        else:
            return plurals[2]

    def format_humanize(self, time_delta, time_unit, past):
        """
        Format string to humanise
        :param time_delta: int, representing time_delta, if negative - then it's in past
        :param time_unit: str, representing time_unit of measurement
        :param past: bool flag, showing if this interval in the past
        :return: formatted string with humanized info
        """
        if time_unit == "now":
            return _Russian.intervals[time_unit]

        if time_delta == 0:
            expr = _Russian.intervals[time_unit]
        else:
            plural = self._chose_plural(time_delta, _Russian.intervals[time_unit])
            expr = "{0} {1}".format(time_delta, plural)
        return _Russian.intervals['past'].format(expr) if past else _Russian.intervals['future'].format(expr)


available_locales = {
    'en': _English,
    'en_us': _English,
    'ru': _Russian,
    'ru_ru': _Russian,
}

def get_locale_by_name(locale_name):
    """
    Return corresponding locale by it's name
    :param locale_name: str with desired locale name
    :return: Locale instance for given language
    """
    locale_name = locale_name.lower()
    if locale_name not in available_locales:
        raise ValueError('Invalid language {0}'.format(locale_name))

    return available_locales[locale_name]()
