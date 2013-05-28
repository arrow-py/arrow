# -*- coding: utf-8 -*-
from __future__ import absolute_import

import calendar
import inspect
import sys


def get_locale(name):
    '''Returns an appropriate :class:`Locale <locale.Locale>` corresponding
    to an inpute locale name.

    :param name: the name of the locale.

    '''

    locale_cls = _locales.get(name.lower())

    if locale_cls is None:
        raise ValueError('Unsupported locale \'{0}\''.format(name))

    return locale_cls()


# base locale type.

class Locale(object):
    ''' Represents locale-specific data and functionality. '''

    _names = []

    _intervals = {
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

    _past = None
    _future = None

    _month_names = []
    _month_abbreviations = []

    _day_names = []
    _day_abbreviations = []

    def __init__(self):

        self._day_name_to_ordinal = None
        self._month_name_to_ordinal = None

    def describe(self, timeframe, delta=0):
        '''Formats a quantity of units of time into a humanized string.

        :param timeframe: a string representing a humanizing timeframe.
        :param delta: a quantity representing a delta in a timeframe.

        '''

        humanized = self._format_timeframe(timeframe, delta)
        humanized = self._format_relative(humanized, timeframe, delta)

        return humanized

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

    def _format_timeframe(self, timeframe, delta):

        return self._intervals[timeframe].format(abs(delta))

    def _format_relative(self, humanized, timeframe, delta):

        if timeframe == 'now':
            return humanized

        direction = self._past if delta < 0 else self._future

        return direction.format(humanized)


# base locale type implementations.

class EnglishLocale(Locale):

    _names = ['en', 'en_us']

    _past = '{0} ago'
    _future = 'in {0}'

    _intervals = {
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
    }


class GreekLocale(Locale):

    _names = ['el']

    _past = '{0} πριν'
    _future = 'σε {0}'

    _intervals = {
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
    }


class SwedishLocale(Locale):

    _names = ['sv', 'sv_se']

    _past = 'för {0} sen'
    _future = 'om {0}'

    _intervals = {
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
    }


class ChineseCNLocale(Locale):

    _names = ['zh', 'zh_cn']

    _past = '{0}前'
    _future = '{0}后'

    _intervals = {
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
    }


class ChineseTWLocale(Locale):

    _names = ['zh_tw']

    _past = '{0}前'
    _future = '{0}後'

    _intervals = {
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
    }


class KoreanLocale(Locale):

    _names = ['ko', 'ko_kr']

    _past = '{0} 전'
    _future = '{0} 후'

    _intervals = {
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
    }


# derived locale types & implementations.

class BaseRussianLocale(Locale):

    def _format_timeframe(self, timeframe, delta):

        form = self._intervals[timeframe]
        delta = abs(delta)

        if isinstance(form, list):

            if delta % 10 == 1 and delta % 100 != 11:
                form = form[0]
            elif 2 <= delta % 10 <= 4 and (delta % 100 < 10 or delta % 100 >= 20):
                form = form[1]
            else:
                form = form[2]

        return form.format(delta)


class RussianLocale(BaseRussianLocale):

    _names = ['ru', 'ru_ru']

    _past = '{0} назад'
    _future = 'через {0}'

    _intervals = {
        'now': 'сейчас',
        'seconds': 'несколько секунд',
        'minute': 'минуту',
        'minutes': ['{0} минута', '{0} минуты', '{0} минут'],
        'hour': 'час',
        'hours': ['{0} час', '{0} часа', '{0} часов'],
        'day': 'день',
        'days': ['{0} день', '{0} дня', '{0} дней'],
        'month': 'месяц',
        'months': ['{0} месяц', '{0} месяца', '{0} месяцев'],
        'year': 'год',
        'years': ['{0} год', '{0} года', '{0} лет'],
    }


class UkrainianLocale(BaseRussianLocale):

    _names = ['ua', 'uk_ua']

    _past = '{0} тому'
    _future = 'за {0}'

    _intervals = {
        'now': 'зараз',
        'seconds': 'кілька секунд',
        'minute': 'хвилину',
        'minutes': ['{0} хвилина', '{0} хвилини', '{0} хвилин'],
        'hour': 'годину',
        'hours': ['{0} година', '{0} години', '{0} годин'],
        'day': 'день',
        'days': ['{0} день', '{0} дні', '{0} днів'],
        'month': 'місяць',
        'months': ['{0} місяць', '{0} місяці', '{0} місяців'],
        'year': 'рік',
        'years': ['{0} рік', '{0} роки', '{0} років'],
    }

def _map_locales():

    locales = {}

    for cls_name, cls in inspect.getmembers(sys.modules[__name__], inspect.isclass):
        if issubclass(cls, Locale):
            for name in cls._names:
                locales[name] = cls

    return locales

_locales = _map_locales()

