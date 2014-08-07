# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals

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

    meridians = {
        'am': '',
        'pm': '',
        'AM': '',
        'PM': '',
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

    def meridian(self, hour, token):
        ''' Returns the meridian indicator for a specified hour and format token.

        :param hour: the ``int`` hour of the day.
        :param token: the format token.
        '''

        if token == 'a':
            return self.meridians['am'] if hour < 12 else self.meridians['pm']
        if token == 'A':
            return self.meridians['AM'] if hour < 12 else self.meridians['PM']


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

    meridians = {
        'am': 'am',
        'pm': 'pm',
        'AM': 'AM',
        'PM': 'PM',
    }

    month_names = ['', 'January', 'February', 'March', 'April', 'May', 'June', 'July',
        'August', 'September', 'October', 'November', 'December']
    month_abbreviations = ['', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug',
        'Sep', 'Oct', 'Nov', 'Dec']

    day_names = ['', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    day_abbreviations = ['', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']


class ItalianLocale(Locale):
    names = ['it', 'it_it']
    past = '{0} fa'
    future = 'tra {0}'

    timeframes = {
        'now': 'adesso',
        'seconds': 'qualche secondo',
        'minute': 'un minuto',
        'minutes': '{0} minuti',
        'hour': 'un\'ora',
        'hours': '{0} ore',
        'day': 'un giorno',
        'days': '{0} giorni',
        'month': 'un mese',
        'months': '{0} mesi',
        'year': 'un anno',
        'years': '{0} anni',
    }

    month_names = ['', 'Gennaio', 'Febbraio', 'Marzo', 'Aprile', 'Maggio', 'Giugno', 'Luglio',
        'Agosto', 'Settembre', 'Ottobre', 'Novembre', 'Dicembre']
    month_abbreviations = ['', 'Gen', 'Feb', 'Mar', 'Apr', 'Mag', 'Giu', 'Lug', 'Ago',
        'Set', 'Ott', 'Nov', 'Dic']

    day_names = ['', 'Lunedì', 'Martedì', 'Mercoledì', 'Giovedì', 'Venerdì', 'Sabato', 'Domenica']
    day_abbreviations = ['', 'Lun', 'Mar', 'Mer', 'Gio', 'Ven', 'Sab', 'Dom']

class SpanishLocale(Locale):
    names = ['es', 'es_es']
    past = 'hace {0}'
    future = 'en {0}'

    timeframes = {
        'now': 'ahora',
        'seconds': 'segundos',
        'minute': 'un minuto',
        'minutes': '{0} minutos',
        'hour': 'una hora',
        'hours': '{0} horas',
        'day': 'un día',
        'days': '{0} días',
        'month': 'un mes',
        'months': '{0} meses',
        'year': 'un año',
        'years': '{0} años',
    }

    month_names = ['', 'Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio',
        'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
    month_abbreviations = ['', 'Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago',
        'Sep', 'Oct', 'Nov', 'Dic']

    day_names = ['', 'Lunes', 'Martes', 'Miercoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
    day_abbreviations = ['', 'Lun', 'Mar', 'Mie', 'Jue', 'Vie', 'Sab', 'Dom']


class FrenchLocale(Locale):
    names = ['fr', 'fr_fr']
    past = 'il y a {0}'
    future = 'dans {0}'

    timeframes = {
        'now': 'maintenant',
        'seconds': 'quelques secondes',
        'minute': 'une minute',
        'minutes': '{0} minutes',
        'hour': 'une heure',
        'hours': '{0} heures',
        'day': 'un jour',
        'days': '{0} jours',
        'month': 'un mois',
        'months': '{0} mois',
        'year': 'un an',
        'years': '{0} ans',
    }

    month_names = ['', 'Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin', 'Juillet',
        'Août', 'Septembre', 'Octobre', 'Novembre', 'Décembre']
    month_abbreviations = ['', 'Janv', 'Févr', 'Mars', 'Avr', 'Mai', 'Juin', 'Juil', 'Août',
        'Sept', 'Oct', 'Nov', 'Déc']

    day_names = ['', 'Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi', 'Dimanche']
    day_abbreviations = ['', 'Lun', 'Mar', 'Mer', 'Jeu', 'Ven', 'Sam', 'Dim']


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

    day_names = ['', 'Δευτέρα', 'Τρίτη', 'Τετάρτη', 'Πέμπτη', 'Παρασκευή', 'Σάββατο', 'Κυριακή']
    day_abbreviations = ['', 'Δευ', 'Τρι', 'Τετ', 'Πεμ', 'Παρ', 'Σαβ', 'Κυρ']


class JapaneseLocale(Locale):

    names = ['ja', 'ja_jp']

    past = '{0}前'
    future = '{0}後'

    timeframes = {
        'now': '現在',
        'seconds': '秒',
        'minute': '1分',
        'minutes': '{0}分',
        'hour': '1時間',
        'hours': '{0}時間',
        'day': '1日',
        'days': '{0}日',
        'month': '1ヶ月',
        'months': '{0}ヶ月',
        'year': '1年',
        'years': '{0}年',
    }

    month_names = ['', '1月', '2月', '3月', '4月', '5月', '6月', '7月', '8月',
        '9月', '10月', '11月', '12月']
    month_abbreviations = ['', ' 1', ' 2', ' 3', ' 4', ' 5', ' 6', ' 7', ' 8',
        ' 9', '10', '11', '12']

    day_names = ['', '月曜日', '火曜日', '水曜日', '木曜日', '金曜日', '土曜日', '日曜日']
    day_abbreviations = ['', '月', '火', '水', '木', '金', '土', '日']


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

    day_names = ['', 'Måndag', 'Tisdag', 'Onsdag', 'Torsdag', 'Fredag', 'Lördag', 'Söndag']
    day_abbreviations = ['', 'Mån', 'Tis', 'Ons', 'Tor', 'Fre', 'Lör', 'Sön']


class FinnishLocale(Locale):

    names = ['fi', 'fi_fi']

    # The finnish grammar is very complex, and its hard to convert
    # 1-to-1 to something like English.

    past = '{0} sitten'
    future = '{0} kuluttua'

    timeframes = {
        'now': 'juuri nyt',
        'seconds': 'muutama sekunti',
        'minute': 'minuutti',
        'minutes': '{0} minuuttia',
        'hour': 'tunti',
        'hours': '{0} tuntia',
        'day': 'päivä',
        'days': '{0} päivää',
        'month': 'kuukausi',
        'months': '{0} kuukautta',
        'year': 'vuosi',
        'years': '{0} vuotta',
    }

    # Months and days are lowercase in Finnish
    month_names = ['', 'tammikuu', 'helmikuu', 'maaliskuu', 'huhtikuu',
                       'toukokuu', 'kesäkuu', 'heinäkuu', 'elokuu',
                       'syyskuu', 'lokakuu', 'marraskuu', 'joulukuu']

    month_abbreviations = ['', 'tammi', 'helmi', 'maalis', 'huhti',
                               'touko', 'kesä', 'heinä', 'elo',
                               'syys', 'loka', 'marras', 'joulu']

    day_names = ['', 'maanantai', 'tiistai', 'keskiviikko', 'torstai',
                     'perjantai', 'lauantai', 'sunnuntai']

    day_abbreviations = ['', 'ma', 'ti', 'ke', 'to', 'pe', 'la', 'su']


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

    day_names = ['', '星期一', '星期二', '星期三', '星期四', '星期五', '星期六', '星期日']
    day_abbreviations = ['', '一', '二', '三', '四', '五', '六', '日']


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

    day_names = ['', '周一', '周二', '周三', '周四', '周五', '周六', '周日']
    day_abbreviations = ['', '一', '二', '三', '四', '五', '六', '日']


class KoreanLocale(Locale):

    names = ['ko', 'ko_kr']

    past = '{0} 전'
    future = '{0} 후'

    timeframes = {
        'now': '지금',
        'seconds': '몇초',
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

    day_names = ['', '월요일', '화요일', '수요일', '목요일', '금요일', '토요일', '일요일']
    day_abbreviations = ['', '월', '화', '수', '목', '금', '토', '일']


# derived locale types & implementations.
class DutchLocale(Locale):

    names = ['nl', 'nl_nl']

    past = '{0} geleden'
    future = 'over {0}'

    timeframes = {
        'now': 'nu',
        'seconds': 'seconden',
        'minute': 'een minuut',
        'minutes': '{0} minuten',
        'hour': 'een uur',
        'hours': '{0} uren',
        'day': 'een dag',
        'days': '{0} dagen',
        'month': 'een maand',
        'months': '{0} maanden',
        'year': 'een jaar',
        'years': '{0} jaren',
    }

    # In Dutch names of months and days are not starting with a capital letter
    # like in the English language.
    month_names = ['', 'januari', 'februari', 'maart', 'april', 'mei', 'juni', 'juli',
        'augustus', 'september', 'oktober', 'november', 'december']
    month_abbreviations = ['', 'jan', 'feb', 'maa', 'apr', 'mei', 'jun', 'jul', 'aug',
        'sep', 'okt', 'nov', 'dec']

    day_names = ['', 'maandag', 'dinsdag', 'woensdag', 'donderdag', 'vrijdag', 'zaterdag', 'zondag']
    day_abbreviations = ['', 'ma', 'di', 'wo', 'do', 'vr', 'za', 'zo']


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


class PolishLocale(SlavicBaseLocale):

    names = ['pl', 'pl_pl']

    past = '{0} temu'
    future = 'za {0}'

    timeframes = {
        'now': 'teraz',
        'seconds': 'kilka sekund',
        'minute': 'minutę',
        'minutes': ['{0} minut', '{0} minuty', '{0} minut'],
        'hour': 'godzina',
        'hours': ['{0} godzin', '{0} godziny', '{0} godzin'],
        'day': 'dzień',
        'days': ['{0} dzień', '{0} dni', '{0} dni'],
        'month': 'miesiąc',
        'months': ['{0} miesiąc', '{0} miesiące', '{0} miesięcy'],
        'year': 'rok',
        'years': ['{0} rok', '{0} lata', '{0} lat'],
    }

    month_names = ['', 'Styczeń', 'Luty', 'Marzec', 'Kwiecień', 'Maj',
        'Czerwiec', 'Lipiec', 'Sierpień', 'Wrzesień', 'Październik',
        'Listopad', 'Grudzień']
    month_abbreviations = ['', 'sty', 'lut', 'mar', 'kwi', 'maj', 'cze', 'lip',
        'sie', 'wrz', 'paź', 'lis', 'gru']

    day_names = ['', 'Poniedziałek', 'Wtorek', 'Środa', 'Czwartek', 'Piątek',
        'Sobota', 'Niedziela']
    day_abbreviations = ['', 'Pn', 'Wt', 'Śr', 'Czw', 'Pt', 'So', 'Nd']


class RussianLocale(SlavicBaseLocale):

    names = ['ru', 'ru_ru']

    past = '{0} назад'
    future = 'через {0}'

    timeframes = {
        'now': 'сейчас',
        'seconds': 'несколько секунд',
        'minute': 'минуту',
        'minutes': ['{0} минуту', '{0} минуты', '{0} минут'],
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

    day_names = ['', 'понедельник', 'вторник', 'среда', 'четверг', 'пятница',
        'суббота', 'воскресенье']
    day_abbreviations = ['', 'пн', 'вт', 'ср', 'чт', 'пт', 'сб', 'вс']


class UkrainianLocale(SlavicBaseLocale):

    names = ['ua', 'uk_ua']

    past = '{0} тому'
    future = 'за {0}'

    timeframes = {
        'now': 'зараз',
        'seconds': 'кілька секунд',
        'minute': 'хвилину',
        'minutes': ['{0} хвилину', '{0} хвилини', '{0} хвилин'],
        'hour': 'годину',
        'hours': ['{0} годину', '{0} години', '{0} годин'],
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

    day_names = ['', 'понеділок', 'вівторок', 'середа', 'четвер', 'п\'ятниця', 'субота', 'неділя']
    day_abbreviations = ['', 'пн', 'вт', 'ср', 'чт', 'пт', 'сб', 'нд']


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
        'Okt', 'Nov', 'Dez'
    ]

    day_names = [
       '', 'Montag', 'Dienstag', 'Mittwoch', 'Donnerstag', 'Freitag',
       'Samstag', 'Sonntag'
    ]

    day_abbreviations = ['', 'Mo', 'Di', 'Mi', 'Do', 'Fr', 'Sa', 'So']


class AustriaLocale(Locale):

    names = ['de', 'de_at']

    past = 'vor {0}'
    future = 'in {0}'

    timeframes = {
            'now': 'gerade eben',
            'seconds':  'Sekunden',
            'minute': 'einer Minute',
            'minutes': '{0} Minuten',
            'hour': 'einer Stunde',
            'hours': '{0} Stunden',
            'day': 'einem Tag',
            'days': '{0} Tage',
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
            'Okt', 'Nov', 'Dez'
        ]

    day_names = [
            '', 'Montag', 'Dienstag', 'Mittwoch', 'Donnerstag', 'Freitag',
            'Samstag', 'Sonntag'
        ]

    day_abbreviations = [
            '', 'Mo', 'Di', 'Mi', 'Do', 'Fr', 'Sa', 'So'
        ]

class NorwegianLocale(Locale):

    names = ['nb', 'nb_no']

    past = 'for {0} siden'
    future = 'om {0}'

    timeframes = {
        'now': 'nå nettopp',
        'seconds': 'noen sekunder',
        'minute': 'ett minutt',
        'minutes': '{0} minutter',
        'hour': 'en time',
        'hours': '{0} timer',
        'day': 'en dag',
        'days': '{0} dager',
        'month': 'en måned',
        'months': '{0} måneder',
        'year': 'ett år',
        'years': '{0} år',
    }

    month_names = ['', 'januar', 'februar', 'mars', 'april', 'mai', 'juni',
                   'juli', 'august', 'september', 'oktober', 'november',
                   'desember']
    month_abbreviations = ['', 'jan', 'feb', 'mar', 'apr', 'mai', 'jun', 'jul',
                           'aug', 'sep', 'okt', 'nov', 'des']

    day_names = ['', 'mandag', 'tirsdag', 'onsdag', 'torsdag', 'fredag',
                 'lørdag', 'søndag']
    day_abbreviations = ['', 'ma', 'ti', 'on', 'to', 'fr', 'lø', 'sø']


class NewNorwegianLocale(Locale):

    names = ['nn', 'nn_no']

    past = 'for {0} sidan'
    future = 'om {0}'

    timeframes = {
        'now': 'no nettopp',
        'seconds': 'nokre sekund',
        'minute': 'ett minutt',
        'minutes': '{0} minutt',
        'hour': 'ein time',
        'hours': '{0} timar',
        'day': 'ein dag',
        'days': '{0} dagar',
        'month': 'en månad',
        'months': '{0} månader',
        'year': 'eit år',
        'years': '{0} år',
    }

    month_names = ['', 'januar', 'februar', 'mars', 'april', 'mai', 'juni',
                   'juli', 'august', 'september', 'oktober', 'november',
                   'desember']
    month_abbreviations = ['', 'jan', 'feb', 'mar', 'apr', 'mai', 'jun', 'jul',
                           'aug', 'sep', 'okt', 'nov', 'des']

    day_names = ['', 'måndag', 'tysdag', 'onsdag', 'torsdag', 'fredag',
                 'laurdag', 'sundag']
    day_abbreviations = ['', 'må', 'ty', 'on', 'to', 'fr', 'la', 'su']


class PortugueseLocale(Locale):
    names = ['pt', 'pt_pt']
    
    past = 'há {0}'
    future = 'em {0}'

    timeframes = {
        'now': 'agora',
        'seconds': 'segundos',
        'minute': 'um minuto',
        'minutes': '{0} minutos',
        'hour': 'uma hora',
        'hours': '{0} horas',
        'day': 'um dia',
        'days': '{0} dias',
        'month': 'um mês',
        'months': '{0} meses',
        'year': 'um ano',
        'years': '{0} anos',
    }

    month_names = ['', 'Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho',
        'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']
    month_abbreviations = ['', 'Jan', 'Fev', 'Mar', 'Abr', 'Maio', 'Jun', 'Jul', 'Ago',
        'Set', 'Out', 'Nov', 'Dez']

    day_names = ['', 'Segunda-feira', 'Terça-feira', 'Quarta-feira', 'Quinta-feira', 'Sexta-feira',
        'Sábado', 'Domingo']
    day_abbreviations = ['', 'Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sab', 'Dom']
    
    
class BrazilianPortugueseLocale(PortugueseLocale):
    names = ['pt_br']
    
    past = 'fazem {0}'


class TagalogLocale(Locale):

    names = ['tl']

    past = 'nakaraang {0}'
    future = '{0} mula ngayon'

    timeframes = {
        'now': 'ngayon lang',
        'seconds': 'segundo',
        'minute': 'isang minuto',
        'minutes': '{0} minuto',
        'hour': 'isang oras',
        'hours': '{0} oras',
        'day': 'isang araw',
        'days': '{0} araw',
        'month': 'isang buwan',
        'months': '{0} buwan',
        'year': 'isang taon',
        'years': '{0} taon',
    }

    month_names = ['', 'Enero', 'Pebrero', 'Marso', 'Abril', 'Mayo', 'Hunyo', 'Hulyo',
        'Agosto', 'Setyembre', 'Oktubre', 'Nobyembre', 'Disyembre']
    month_abbreviations = ['', 'Ene', 'Peb', 'Mar', 'Abr', 'May', 'Hun', 'Hul', 'Ago',
        'Set', 'Okt', 'Nob', 'Dis']

    day_names = ['', 'Lunes', 'Martes', 'Miyerkules', 'Huwebes', 'Biyernes', 'Sabado', 'Linggo']
    day_abbreviations = ['', 'Lun', 'Mar', 'Miy', 'Huw', 'Biy', 'Sab', 'Lin']


class VietnameseLocale(Locale):

    names = ['vi', 'vi_vn']

    past = '{0} trước'
    future = '{0} nữa'

    timeframes = {
        'now': 'hiện tại',
        'seconds': 'giây',
        'minute': 'một phút',
        'minutes': '{0} phút',
        'hour': 'một giờ',
        'hours': '{0} giờ',
        'day': 'một ngày',
        'days': '{0} ngày',
        'month': 'một tháng',
        'months': '{0} tháng',
        'year': 'một năm',
        'years': '{0} năm',
    }

    month_names = ['', 'Tháng Một', 'Tháng Hai', 'Tháng Ba', 'Tháng Tư', 'Tháng Năm', 'Tháng Sáu', 'Tháng Bảy',
        'Tháng Tám', 'Tháng Chín', 'Tháng Mười', 'Tháng Mười Một', 'Tháng Mười Hai']
    month_abbreviations = ['', 'Tháng 1', 'Tháng 2', 'Tháng 3', 'Tháng 4', 'Tháng 5', 'Tháng 6', 'Tháng 7', 'Tháng 8',
        'Tháng 9', 'Tháng 10', 'Tháng 11', 'Tháng 12']

    day_names = ['', 'Thứ Hai', 'Thứ Ba', 'Thứ Tư', 'Thứ Năm', 'Thứ Sáu', 'Thứ Bảy', 'Chủ Nhật']
    day_abbreviations = ['', 'Thứ 2', 'Thứ 3', 'Thứ 4', 'Thứ 5', 'Thứ 6', 'Thứ 7', 'CN']


class TurkishLocale(Locale):

    names = ['tr', 'tr_TR']

    past = '{0} önce'
    future = '{0} sonra'

    timeframes = {
        'now': 'şimdi',
        'seconds': 'saniye',
        'minute': 'bir dakika',
        'minutes': '{0} dakika',
        'hour': 'bir saat',
        'hours': '{0} saat',
        'day': 'bir gün',
        'days': '{0} gün',
        'month': 'bir ay',
        'months': '{0} ay',
        'year': 'a yıl',
        'years': '{0} yıl',
    }

    month_names = ['', 'Ocak', 'Şubat', 'Mart', 'Nisan', 'Mayıs', 'Haziran', 'Temmuz',
        'Ağustos', 'Eylül', 'Ekim', 'Kasım', 'Aralık']
    month_abbreviations = ['', 'Oca', 'Şub', 'Mar', 'Nis', 'May', 'Haz', 'Tem', 'Ağu',
        'Eyl', 'Eki', 'Kas', 'Ara']

    day_names = ['', 'Pazartesi', 'Salı', 'Çarşamba', 'Perşembe', 'Cuma', 'Cumartesi', 'Pazar']
    day_abbreviations = ['', 'Pzt', 'Sal', 'Çar', 'Per', 'Cum', 'Cmt', 'Paz']


class ArabicLocale(Locale):

    names = ['ar', 'ar_EG']

    past = 'منذ {0}'
    future = 'خلال {0}'

    timeframes = {
        'now': 'الآن',
        'seconds': 'ثوان',
        'minute': 'دقيقة',
        'minutes': '{0} دقائق',
        'hour': 'ساعة',
        'hours': '{0} ساعات',
        'day': 'يوم',
        'days': '{0} أيام',
        'month': 'شهر',
        'months': '{0} شهور',
        'year': 'سنة',
        'years': '{0} سنوات',
    }

    month_names = ['', 'يناير', 'فبراير', 'مارس', 'أبريل', 'مايو', 'يونيو', 'يوليو',
        'أغسطس', 'سبتمبر', 'أكتوبر', 'نوفمبر', 'ديسمبر']
    month_abbreviations = ['', 'يناير', 'فبراير', 'مارس', 'أبريل', 'مايو', 'يونيو', 'يوليو',
        'أغسطس', 'سبتمبر', 'أكتوبر', 'نوفمبر', 'ديسمبر']

    day_names = ['', 'الاثنين', 'الثلاثاء', 'الأربعاء', 'الخميس', 'الجمعة', 'السبت', 'الأحد']
    day_abbreviations = ['', 'اثنين', 'ثلاثاء', 'أربعاء', 'خميس', 'جمعة', 'سبت', 'أحد']


class IcelandicLocale(Locale):

    def _format_timeframe(self, timeframe, delta):

        timeframe = self.timeframes[timeframe]
        if delta < 0:
            timeframe = timeframe[0]
        elif delta > 0:
            timeframe = timeframe[1]

        return timeframe.format(abs(delta))

    names = ['is', 'is_is']

    past = 'fyrir {0} síðan'
    future = 'eftir {0}'

    timeframes = {
        'now':     'rétt í þessu',
        'seconds': ('nokkrum sekúndum', 'nokkrar sekúndur'),
        'minute':  ('einni mínútu', 'eina mínútu'),
        'minutes': ('{0} mínútum', '{0} mínútur'),
        'hour':    ('einum tíma', 'einn tíma'),
        'hours':   ('{0} tímum', '{0} tíma'),
        'day':     ('einum degi', 'einn dag'),
        'days':    ('{0} dögum', '{0} daga'),
        'month':   ('einum mánuði', 'einn mánuð'),
        'months':  ('{0} mánuðum', '{0} mánuði'),
        'year':    ('einu ári', 'eitt ár'),
        'years':   ('{0} árum', '{0} ár'),
    }

    meridians = {
        'am': 'f.h.',
        'pm': 'e.h.',
        'AM': 'f.h.',
        'PM': 'e.h.',
    }

    month_names = ['', 'janúar', 'febrúar', 'mars', 'apríl', 'maí', 'júní',
        'júlí', 'ágúst', 'september', 'október', 'nóvember', 'desember']
    month_abbreviations = ['', 'jan', 'feb', 'mar', 'apr', 'maí', 'jún',
        'júl', 'ágú', 'sep', 'okt', 'nóv', 'des']

    day_names = ['', 'mánudagur', 'þriðjudagur', 'miðvikudagur', 'fimmtudagur',
        'föstudagur', 'laugardagur', 'sunnudagur']
    day_abbreviations = ['', 'mán', 'þri', 'mið', 'fim', 'fös', 'lau', 'sun']


class DanishLocale(Locale):

    names = ['da', 'da_dk']

    past = 'for {0} siden'
    future = 'efter {0}'

    timeframes = {
        'now':     'lige nu',
        'seconds': 'et par sekunder',
        'minute':  'et minut',
        'minutes': '{0} minutter',
        'hour':    'en time',
        'hours':   '{0} timer',
        'day':     'en dag',
        'days':    '{0} dage',
        'month':   'en måned',
        'months':  '{0} måneder',
        'year':    'et år',
        'years':   '{0} år',
    }

    month_names = ['', 'januar', 'februar', 'marts', 'april', 'maj', 'juni',
        'juli', 'august', 'september', 'oktober', 'november', 'december']
    month_abbreviations = ['', 'jan', 'feb', 'mar', 'apr', 'maj', 'jun',
        'jul', 'aug', 'sep', 'okt', 'nov', 'dec']

    day_names = ['', 'mandag', 'tirsdag', 'onsdag', 'torsdag', 'fredag',
        'lørdag', 'søndag']
    day_abbreviations = ['', 'man', 'tir', 'ons', 'tor', 'fre', 'lør', 'søn']


class MalayalamLocale(Locale):

    names = ['ml']

    past = '{0} മുമ്പ്'
    future = '{0} ശേഷം'

    timeframes = {
        'now': 'ഇപ്പോൾ',
        'seconds': 'സെക്കന്റ്‌',
        'minute': 'ഒരു മിനിറ്റ്',
        'minutes': '{0} മിനിറ്റ്',
        'hour': 'ഒരു മണിക്കൂർ',
        'hours': '{0} മണിക്കൂർ',
        'day': 'ഒരു ദിവസം ',
        'days': '{0} ദിവസം ',
        'month': 'ഒരു മാസം ',
        'months': '{0} മാസം ',
        'year': 'ഒരു വർഷം ',
        'years': '{0} വർഷം ',
    }

    meridians = {
        'am': 'രാവിലെ',
        'pm': 'ഉച്ചക്ക് ശേഷം',
        'AM': 'രാവിലെ',
        'PM': 'ഉച്ചക്ക് ശേഷം',
    }

    month_names = ['', 'ജനുവരി', 'ഫെബ്രുവരി', 'മാർച്ച്‌', 'ഏപ്രിൽ ', 'മെയ്‌ ', 'ജൂണ്‍', 'ജൂലൈ',
                   'ഓഗസ്റ്റ്‌', 'സെപ്റ്റംബർ', 'ഒക്ടോബർ', 'നവംബർ', 'ഡിസംബർ']
    month_abbreviations = ['', 'ജനു', 'ഫെബ് ', 'മാർ', 'ഏപ്രിൽ', 'മേയ്', 'ജൂണ്‍', 'ജൂലൈ', 'ഓഗസ്റ',
                           'സെപ്റ്റ', 'ഒക്ടോ', 'നവം', 'ഡിസം']

    day_names = ['', 'തിങ്കള്‍', 'ചൊവ്വ', 'ബുധന്‍', 'വ്യാഴം', 'വെള്ളി', 'ശനി', 'ഞായര്‍']
    day_abbreviations = ['', 'തിങ്കള്‍', 'ചൊവ്വ', 'ബുധന്‍', 'വ്യാഴം', 'വെള്ളി', 'ശനി', 'ഞായര്‍']


class HindiLocale(Locale):

    names = ['hi']

    past = '{0} पहले'
    future = '{0} बाद'

    timeframes = {
        'now': 'अभि',
        'seconds': 'सेकंड्',
        'minute': 'एक मिनट ',
        'minutes': '{0} मिनट ',
        'hour': 'एक घंट',
        'hours': '{0} घंटे',
        'day': 'एक दिन',
        'days': '{0} दिन',
        'month': 'एक माह ',
        'months': '{0} महीने ',
        'year': 'एक वर्ष ',
        'years': '{0} साल ',
    }

    meridians = {
        'am': 'सुबह',
        'pm': 'शाम',
        'AM': 'सुबह',
        'PM': 'शाम',
    }

    month_names = ['', 'जनवरी', 'फ़रवरी', 'मार्च', 'अप्रैल ', 'मई', 'जून', 'जुलाई',
                   'आगस्त', 'सितम्बर', 'अकतूबर', 'नवेम्बर', 'दिसम्बर']
    month_abbreviations = ['', 'जन', 'फ़र', 'मार्च', 'अप्रै', 'मई', 'जून', 'जुलाई', 'आग',
                           'सित', 'अकत', 'नवे', 'दिस']

    day_names = ['', 'सोमवार', 'मंगलवार', 'बुधवार', 'गुरुवार', 'शुक्रवार', 'शनिवार', 'रविवार']
    day_abbreviations = ['', 'सोम', 'मंगल', 'बुध', 'गुरुवार', 'शुक्र', 'शनि', 'रवि']

class CzechLocale(Locale):
    names = ['cs', 'cs_cz']

    timeframes = {
        'now': 'Teď',
        'seconds': {
            'past': '{0} sekundami',
            'future': ['{0} sekundy', '{0} sekund']
        },
        'minute': {'past': 'minutou', 'future': 'minutu', 'zero': '{0} minut'},
        'minutes': {
            'past': '{0} minutami',
            'future': ['{0} minuty', '{0} minut']
        },
        'hour': {'past': 'hodinou', 'future': 'hodinu', 'zero': '{0} hodin'},
        'hours': {
            'past': '{0} hodinami',
            'future': ['{0} hodiny', '{0} hodin']
        },
        'day': {'past': 'dnem', 'future': 'den', 'zero': '{0} dnů'},
        'days': {
            'past': '{0} dny',
            'future': ['{0} dny', '{0} dnů']
        },
        'month': {'past': 'měsícem', 'future': 'měsíc', 'zero': '{0} měsíců'},
        'months': {
            'past': '{0} měsíci',
            'future': ['{0} měsíce', '{0} měsíců']
        },
        'year': {'past': 'rokem', 'future': 'rok', 'zero': '{0} let'},
        'years': {
            'past': '{0} lety',
            'future': ['{0} roky', '{0} let']
        }
    }

    past = 'Před {0}'
    future = 'Za {0}'

    month_names = ['Leden', 'Únor', 'Březen', 'Duben', 'Květen', 'Červen',
        'Červenec', 'Srpen', 'Září', 'Říjen', 'Listopad', 'Prosinec']
    month_abbreviations = ['Led', 'Úno', 'Bře', 'Dub', 'Kvě', 'Čvn', 'Čvc',
        'Srp', 'Zář', 'Říj', 'Lis', 'Pro']

    day_names = ['Pondělí', 'Úterý', 'Středa', 'Čtvrtek', 'Pátek',
        'Sobota', 'Neděle']
    day_abbreviations = ['Po', 'Út', 'St', 'Čt', 'Pá', 'So', 'Ne']


    def _format_timeframe(self, timeframe, delta):
        '''Czech aware time frame format function, takes into account the differences between past and future forms.'''
        form = self.timeframes[timeframe]
        if isinstance(form, dict):
            if delta == 0:
                form = form['zero'] # And *never* use 0 in the singular!
            elif delta > 0:
                form = form['future']
            else:
                form = form['past']
        delta = abs(delta)  

        if isinstance(form, list):
            if 2 <= delta % 10 <= 4 and (delta % 100 < 10 or delta % 100 >= 20):
                form = form[0]
            else:
                form = form[1]

        return form.format(delta)

class FarsiLocale(Locale):

    names = ['fa', 'fa_ir']

    past = '{0} قبل'
    future = 'در {0}'

    timeframes = {
        'now': 'اکنون',
        'seconds': 'ثانیه',
        'minute': 'یک دقیقه',
        'minutes': '{0} دقیقه',
        'hour': 'یک ساعت',
        'hours': '{0} ساعت',
        'day': 'یک روز',
        'days': '{0} روز',
        'month': 'یک ماه',
        'months': '{0} ماه',
        'year': 'یک سال',
        'years': '{0} سال',
    }

    meridians = {
        'am': 'قبل از ظهر',
        'pm': 'بعد از ظهر',
        'AM': 'قبل از ظهر',
        'PM': 'بعد از ظهر',
    }

    month_names = ['', 'January', 'February', 'March', 'April', 'May', 'June', 'July',
        'August', 'September', 'October', 'November', 'December']
    month_abbreviations = ['', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug',
        'Sep', 'Oct', 'Nov', 'Dec']

    day_names = ['', 'دو شنبه', 'سه شنبه', 'چهارشنبه', 'پنجشنبه', 'جمعه', 'شنبه', 'یکشنبه']
    day_abbreviations = ['', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']


def _map_locales():

    locales = {}

    for cls_name, cls in inspect.getmembers(sys.modules[__name__], inspect.isclass):
        if issubclass(cls, Locale):
            for name in cls.names:
                locales[name] = cls  

    return locales

_locales = _map_locales()
