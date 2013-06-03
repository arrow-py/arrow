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

    names = []

    timeframes = {
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
    }

    past = None
    future = None

    month_names = []
    month_abbreviations = []

    day_names = []
    day_abbreviations = []

    def __init__(self):

        self._month_name_to_ordinal = None

    def describe(self, timeframe, delta=0):
        ''' Describes a delta within a timeframe in plain language.

        :param timeframe: a string representing a timeframe.
        :param delta: a quantity representing a delta in a timeframe.

        '''

        humanized = self._format_timeframe(timeframe, delta)
        humanized = self._format_relative(humanized, timeframe, delta)

        return humanized

    def day_name(self, day):
        ''' Returns the day name for a specified day of the week.

        :param day: the ``int`` day of the week (1-7).

        '''

        return self.day_names[day]

    def day_abbreviation(self, day):
        ''' Returns the day abbreviation for a specified day of the week.

        :param day: the ``int`` day of the week (1-7).

        '''

        return self.day_abbreviations[day]

    def month_name(self, month):
        ''' Returns the month name for a specified month of the year.

        :param month: the ``int`` month of the year (1-12).

        '''

        return self.month_names[month]

    def month_abbreviation(self, month):
        ''' Returns the month abbreviation for a specified month of the year.

        :param month: the ``int`` month of the year (1-12).

        '''

        return self.month_abbreviations[month]

    def month_number(self, name):
        ''' Returns the month number for a month specified by name or abbreviation.

        :param name: the month name or abbreviation.

        '''

        if self._month_name_to_ordinal is None:
            self._month_name_to_ordinal = self._name_to_ordinal(self.month_names)
            self._month_name_to_ordinal.update(self._name_to_ordinal(self.month_abbreviations))

        return self._month_name_to_ordinal.get(name)


    def _name_to_ordinal(self, lst):
        return dict(map(lambda i: (i[1], i[0] + 1), enumerate(lst[1:])))

    def _format_timeframe(self, timeframe, delta):

        return self.timeframes[timeframe].format(abs(delta))

    def _format_relative(self, humanized, timeframe, delta):

        if timeframe == 'now':
            return humanized

        direction = self.past if delta < 0 else self.future

        return direction.format(humanized)


# base locale type implementations.

class EnglishLocale(Locale):

    names = ['en', 'en_us']

    past = '{0} ago'
    future = 'in {0}'

    timeframes = {
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

    month_names = ['', 'January', 'February', 'March', 'April', 'May', 'June', 'July',
        'August', 'September', 'October', 'November', 'December']
    month_abbreviations = ['', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug',
        'Sep', 'Oct', 'Nov', 'Dec']

    day_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    day_abbreviations = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']


class GreekLocale(Locale):

    names = ['el', 'el_gr']

    past = '{0} πριν'
    future = 'σε {0}'

    timeframes = {
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

    month_names = ['', 'Ιανουαρίου', 'Φεβρουαρίου', 'Μαρτίου', 'Απριλίου', 'Μαΐου', 'Ιουνίου',
        'Ιουλίου', 'Αυγούστου', 'Σεπτεμβρίου', 'Οκτωβρίου', 'Νοεμβρίου', 'Δεκεμβρίου']
    month_abbreviations = ['', 'Ιαν', 'Φεβ', 'Μαρ', 'Απρ', 'Μαϊ', 'Ιον', 'Ιολ', 'Αυγ',
        'Σεπ', 'Οκτ', 'Νοε', 'Δεκ']

    day_names = ['Δευτέρα', 'Τρίτη', 'Τετάρτη', 'Πέμπτη', 'Παρασκευή', 'Σάββατο', 'Κυριακή']
    day_abbreviations = ['Δευ', 'Τρι', 'Τετ', 'Πεμ', 'Παρ', 'Σαβ', 'Κυρ']

class SwedishLocale(Locale):

    names = ['sv', 'sv_se']

    past = 'för {0} sen'
    future = 'om {0}'

    timeframes = {
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

    month_names = ['', 'Januari', 'Februari', 'Mars', 'April', 'Maj', 'Juni', 'Juli',
        'Augusti', 'September', 'Oktober', 'November', 'December']
    month_abbreviations = ['', 'Jan', 'Feb', 'Mar', 'Apr', 'Maj', 'Jun', 'Jul',
        'Aug', 'Sep', 'Okt', 'Nov', 'Dec']

    day_names = ['Måndag', 'Tisdag', 'Onsdag', 'Torsdag', 'Fredag', 'Lördag', 'Söndag']
    day_abbreviations = ['Mån', 'Tis', 'Ons', 'Tor', 'Fre', 'Lör', 'Sön']


class ChineseCNLocale(Locale):

    names = ['zh', 'zh_cn']

    past = '{0}前'
    future = '{0}后'

    timeframes = {
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

    month_names = ['', '一月', '二月', '三月', '四月', '五月', '六月', '七月',
        '八月', '九月', '十月', '十一月', '十二月']
    month_abbreviations = ['', ' 1', ' 2', ' 3', ' 4', ' 5', ' 6', ' 7', ' 8',
        ' 9', '10', '11', '12']

    day_names = ['星期一', '星期二', '星期三', '星期四', '星期五', '星期六', '星期日']
    day_abbreviations = ['一', '二', '三', '四', '五', '六', '日']

class ChineseTWLocale(Locale):

    names = ['zh_tw']

    past = '{0}前'
    future = '{0}後'

    timeframes = {
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

    month_names = ['', '1月', '2月', '3月', '4月', '5月', '6月', '7月', '8月',
        '9月', '10月', '11月', '12月']
    month_abbreviations = ['', ' 1', ' 2', ' 3', ' 4', ' 5', ' 6', ' 7', ' 8',
        ' 9', '10', '11', '12']

    day_names = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
    day_abbreviations = ['一', '二', '三', '四', '五', '六', '日']


class KoreanLocale(Locale):

    names = ['ko', 'ko_kr']

    past = '{0} 전'
    future = '{0} 후'

    timeframes = {
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

    month_names = ['', '1월', '2월', '3월', '4월', '5월', '6월', '7월', '8월',
        '9월', '10월', '11월', '12월']
    month_abbreviations = ['', ' 1', ' 2', ' 3', ' 4', ' 5', ' 6', ' 7', ' 8',
        ' 9', '10', '11', '12']

    day_names = ['월요일', '화요일', '수요일', '목요일', '금요일', '토요일', '일요일']
    day_abbreviations = ['월', '화', '수', '목', '금', '토', '일']


# derived locale types & implementations.

class BaseRussianLocale(Locale):

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


class RussianLocale(BaseRussianLocale):

    names = ['ru', 'ru_ru']

    past = '{0} назад'
    future = 'через {0}'

    timeframes = {
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

    month_names = ['', 'января', 'февраля', 'марта', 'апреля', 'мая', 'июня',
        'июля', 'августа', 'сентября', 'октября', 'ноября', 'декабря']
    month_abbreviations = ['', 'янв', 'фев', 'мар', 'апр', 'май', 'июн', 'июл',
        'авг', 'сен', 'окт', 'ноя', 'дек']

    day_names = ['понедельник', 'вторник', 'среда', 'четверг', 'пятница',
        'суббота', 'воскресенье']
    day_abbreviations = ['пн', 'вт', 'ср', 'чт', 'пт', 'сб', 'вс']


class UkrainianLocale(BaseRussianLocale):

    names = ['ua', 'uk_ua']

    past = '{0} тому'
    future = 'за {0}'

    timeframes = {
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

    month_names = ['', 'січня', 'лютого', 'березня', 'квітня', 'травня', 'червня',
        'липня', 'серпня', 'вересня', 'жовтня', 'листопада', 'грудня']
    month_abbreviations = ['', 'січ', 'лют', 'бер', 'кві', 'тра', 'чер', 'лип', 'сер',
        'вер', 'жов', 'лис', 'гру']

    day_names = ['понеділок', 'вівторок', 'середа', 'четвер', 'п\'ятниця', 'субота', 'неділя']
    day_abbreviations = ['пн', 'вт', 'ср', 'чт', 'пт', 'сб', 'нд']


class GermanLocale(Locale):

    names = ['de', 'de_de']

    past = 'vor {0}'
    future = 'in {0}'

    timeframes = {
        'now': 'gerade eben',
        'seconds': 'Sekunden',
        'minute': 'einer Minute',
        'minutes': '{0} Minuten',
        'hour': 'einer Stunde',
        'hours': '{0} Stunden',
        'day': 'einem Tag',
        'days': '{0} Tagen',
        'month': 'einem Monat',
        'months': '{0} Monaten',
        'year': 'einem Jahr',
        'years': '{0} Jahren',
    }

    month_names = [
        '', 'Januar', 'Februar', 'März', 'April', 'Mai', 'Juni', 'Juli',
        'August', 'September', 'Oktober', 'November', 'Dezember'
    ]
    month_abbreviations = [
        '', 'Jan', 'Feb', 'Mär', 'Apr', 'Mai', 'Jun', 'Jul', 'Aug', 'Sep',
        'Oct', 'Nov', 'Dez'
    ]

    day_names = [
        'Montag', 'Dienstag', 'Mittwoch', 'Donnerstag', 'Freitag', 'Samstag',
        'Sonntag'
    ]
    day_abbreviations = ['Mo', 'Di', 'Mi', 'Do', 'Fr', 'Sa', 'So']


def _map_locales():

    locales = {}

    for cls_name, cls in inspect.getmembers(sys.modules[__name__], inspect.isclass):
        if issubclass(cls, Locale):
            for name in cls.names:
                locales[name] = cls

    return locales

_locales = _map_locales()

