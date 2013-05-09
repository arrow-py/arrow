# -*- coding: utf-8 -*-


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

    def format_humanize(self, quantity, unit, past):
        '''Formats a quantity of units of time into a humanized string.

        :param quantity: int, representing the number of time units.
        :param unit: str, representing the unit of time being humanized.
        :param past: bool flag, describing whether this represents a time in the past or future.
        '''

        raise NotImplementedError()


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


class RussianLocale(Locale):

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


available_locales = {
    'en': EnglishLocale,
    'en_us': EnglishLocale,
    'ru': RussianLocale,
    'ru_ru': RussianLocale,
    'el': GreekLocale
}

