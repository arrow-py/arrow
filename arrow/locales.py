# -*- coding: utf-8 -*-
from __future__ import absolute_import

import calendar


def get_locale_by_name(locale_name):
    '''Returns an appropriate :class:`Locale <locale.Locale>` corresponding
    to an inpute locale name.

    :param locale_name: the name of the locale.
    '''

    locale_name = locale_name.lower()
    locale_cls = available_locales.get(locale_name)

    if locale_cls is None:
        raise ValueError('Unsupported locale \'{0}\''.format(locale_name))

    return locale_cls()


class Locale(object):

    def __init__(self):

        self._day_name_to_ordinal = None
        self._month_name_to_ordinal = None

    def format_humanize(self, quantity, unit, past):
        '''Formats a quantity of units of time into a humanized string.

        :param quantity: int, representing the number of time units.
        :param unit: str, representing the unit of time being humanized.
        :param past: bool flag, describing whether this represents a time in the past or future.
        '''

        raise NotImplementedError()

    def month_name(self, num):
        return calendar.month_name[num]

    def month_abbr(self, num):
        return calendar.month_abbr[num]

    def month_number(self, name):

        if self._month_name_to_ordinal is None:
            self._month_name_to_ordinal = self._name_to_ordinal(calendar.month_name)
            self._month_name_to_ordinal.update(self._name_to_ordinal(calendar.month_abbr))

        return self._month_name_to_ordinal.get(name)

    def day_name(self, num):
        return calendar.day_name[num]

    def day_abbr(self, num):
        return calendar.day_abbr[num]

    def _name_to_ordinal(self, lst):
        return dict(map(lambda i: (i[1], i[0] + 1), enumerate(lst[1:])))


class BasicLocale(Locale):
    '''Base class for locales with no complex plurality logic.
    '''

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

    def format_humanize(self, quantity, unit, past):
        '''Formats a quantity of units of time into a humanized string.

        :param quantity: int, representing the number of time units.
        :param unit: str, representing the unit of time being humanized.
        :param past: bool flag, describing whether this represents a time in the past or future.
        '''

        if unit == 'now':
            return self.intervals[unit]

        if quantity == 0:
            expr = self.intervals[unit]
        else:
            expr = self.intervals[unit].format(quantity)

        direction = self.intervals['past'] if past else self.intervals['future']

        return direction.format(expr)


class EnglishLocale(BasicLocale):

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


class GreekLocale(BasicLocale):

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


class SwedishLocale(BasicLocale):

    intervals = {
        'now': 'just nu',
        'seconds': 'några sekunder',
        'minute': 'en minut',
        'minutes': '{0} minuter',
        'hour': 'en timme',
        'hours': '{0} timmar',
        'day': 'en dag',
        'days': '{0} dagar',
        'month': 'en månad',
        'months': '{0} månader',
        'year': 'ett år',
        'years': '{0} år',

        'past': 'för {0} sen',
        'future': 'om {0}',
    }


class PluralChangingLocale(Locale):

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

    def _chose_plural(self, num, plurals):
        '''Selects the correct plural form for russian nouns.

        :param num: numerator, used with nouns.
        :param plurals: the three plural forms of a noun.
        '''

        if num % 10 == 1 and num % 100 != 11:
            return plurals[0]
        elif 2 <= num % 10 <= 4 and (num % 100 < 10 or num % 100 >= 20):
            return plurals[1]
        else:
            return plurals[2]

    def format_humanize(self, quantity, unit, past):
        '''Formats a quantity of units of time into a humanized string.

        :param quantity: int, representing the number of time units.
        :param unit: str, representing the unit of time being humanized.
        :param past: bool flag, describing whether this represents a time in the past or future.
        '''

        if unit == 'now':
            return self.intervals[unit]

        if quantity == 0:
            expr = self.intervals[unit]
        else:
            plural = self._chose_plural(quantity, self.intervals[unit])
            expr = "{0} {1}".format(quantity, plural)

        return self.intervals['past'].format(expr) if past else self.intervals['future'].format(expr)


class RussianLocale(PluralChangingLocale):
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


class UkrainianLocale(PluralChangingLocale):
    intervals = {
        'now': 'зараз',
        'seconds': 'кілька секунд',
        'minute': 'хвилину',
        'minutes': ['хвилина', 'хвилини', 'хвилин'],
        'hour': 'годину',
        'hours': ['година', 'години', 'годин'],
        'day': 'день',
        'days': ['день', 'дні', 'днів'],
        'month': 'місяць',
        'months': ['місяць', 'місяці', 'місяців'],
        'year': 'рік',
        'years': ['рік', 'роки', 'років'],

        'past': '{0} тому',
        'future': 'за {0}',
    }


class ChineseCNLocale(BasicLocale):

    intervals = {
        'now': '刚才',
        'seconds': '秒',
        'minute': '1分钟',
        'minutes': '{0}分钟',
        'hour': '1小时',
        'hours': '{0}小时',
        'day': '1天',
        'days': '{0}天',
        'month': '1个月',
        'months': '{0}个月',
        'year': '1年',
        'years': '{0}年',

        'past': '{0}前',
        'future': '{0}后',
    }


class ChineseTWLocale(BasicLocale):

    intervals = {
        'now': '剛才',
        'seconds': '秒',
        'minute': '1分鐘',
        'minutes': '{0}分鐘',
        'hour': '1小時',
        'hours': '{0}小時',
        'day': '1天',
        'days': '{0}天',
        'month': '1個月',
        'months': '{0}個月',
        'year': '1年',
        'years': '{0}年',

        'past': '{0}前',
        'future': '{0}後',
    }


class KoreanLocale(BasicLocale):

    intervals = {
        'now': '현재',
        'seconds': '초',
        'minute': '일 분',
        'minutes': '{0}분',
        'hour': '1시간',
        'hours': '{0}시간',
        'day': '1일',
        'days': '{0}일',
        'month': '1개월',
        'months': '{0}개월',
        'year': '1년',
        'years': '{0}년',
        'past': '{0} 전',
        'future': '{0} 후',
    }


available_locales = {
    'en': EnglishLocale,
    'en_us': EnglishLocale,
    'ru': RussianLocale,
    'ru_ru': RussianLocale,
    'el': GreekLocale,
    'zh': ChineseCNLocale,
    'zh_cn': ChineseCNLocale,
    'zh_tw': ChineseTWLocale,
    'ko': KoreanLocale,
    'ko_kr': KoreanLocale,
    'sv': SwedishLocale,
    'sv_se': SwedishLocale,
    'ua': UkrainianLocale,
    'uk_ua': UkrainianLocale,
}
