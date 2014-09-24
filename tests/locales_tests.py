# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from chai import Chai

from arrow import locales


class ModuleTests(Chai):

    def test_get_locale(self):

        mock_locales = mock(locales, '_locales')
        mock_locale_cls = mock()
        mock_locale = mock()

        expect(mock_locales.get).args('name').returns(mock_locale_cls)
        expect(mock_locale_cls).returns(mock_locale)

        result = locales.get_locale('name')

        assertEqual(result, mock_locale)

    def test_locales(self):

        assertTrue(len(locales._locales) > 0)


class LocaleTests(Chai):

    def setUp(self):
        super(LocaleTests, self).setUp()

        self.locale = locales.EnglishLocale()

    def test_format_timeframe(self):

        assertEqual(self.locale._format_timeframe('hours', 2), '2 hours')
        assertEqual(self.locale._format_timeframe('hour', 0), 'an hour')
        assertEqual(self.locale._format_timeframe('seconds', 20), '20 seconds')

    def test_format_relative_now(self):

        result = self.locale._format_relative('just now', 'now', 0)

        assertEqual(result, 'just now')

    def test_format_relative_past(self):

        result = self.locale._format_relative('an hour', 'hour', 1)

        assertEqual(result, 'in an hour')

    def test_format_relative_future(self):

        result = self.locale._format_relative('an hour', 'hour', -1)

        assertEqual(result, 'an hour ago')


class RussianLocalesTests(Chai):

    def test_plurals2(self):

        locale = locales.RussianLocale()

        assertEqual(locale._format_timeframe('hours', 0), '0 часов')
        assertEqual(locale._format_timeframe('hours', 1), '1 час')
        assertEqual(locale._format_timeframe('hours', 2), '2 часа')
        assertEqual(locale._format_timeframe('hours', 4), '4 часа')
        assertEqual(locale._format_timeframe('hours', 5), '5 часов')
        assertEqual(locale._format_timeframe('hours', 21), '21 час')
        assertEqual(locale._format_timeframe('hours', 22), '22 часа')
        assertEqual(locale._format_timeframe('hours', 25), '25 часов')

        # feminine grammatical gender should be tested separately
        assertEqual(locale._format_timeframe('minutes', 0), '0 минут')
        assertEqual(locale._format_timeframe('minutes', 1), '1 минуту')
        assertEqual(locale._format_timeframe('minutes', 2), '2 минуты')
        assertEqual(locale._format_timeframe('minutes', 4), '4 минуты')
        assertEqual(locale._format_timeframe('minutes', 5), '5 минут')
        assertEqual(locale._format_timeframe('minutes', 21), '21 минуту')
        assertEqual(locale._format_timeframe('minutes', 22), '22 минуты')
        assertEqual(locale._format_timeframe('minutes', 25), '25 минут')


class PolishLocalesTests(Chai):

    def test_plurals(self):

        locale = locales.PolishLocale()

        assertEqual(locale._format_timeframe('hours', 0), '0 godzin')
        assertEqual(locale._format_timeframe('hours', 1), '1 godzin')
        assertEqual(locale._format_timeframe('hours', 2), '2 godziny')
        assertEqual(locale._format_timeframe('hours', 4), '4 godziny')
        assertEqual(locale._format_timeframe('hours', 5), '5 godzin')
        assertEqual(locale._format_timeframe('hours', 21), '21 godzin')
        assertEqual(locale._format_timeframe('hours', 22), '22 godziny')
        assertEqual(locale._format_timeframe('hours', 25), '25 godzin')


class IcelandicLocalesTests(Chai):

    def setUp(self):
        super(IcelandicLocalesTests, self).setUp()

        self.locale = locales.IcelandicLocale()

    def test_format_timeframe(self):

        assertEqual(self.locale._format_timeframe('minute', -1), 'einni mínútu')
        assertEqual(self.locale._format_timeframe('minute', 1), 'eina mínútu')

        assertEqual(self.locale._format_timeframe('hours', -2), '2 tímum')
        assertEqual(self.locale._format_timeframe('hours', 2), '2 tíma')


class MalayalamLocaleTests(Chai):

    def setUp(self):
        super(MalayalamLocaleTests, self).setUp()

        self.locale = locales.MalayalamLocale()

    def test_format_timeframe(self):

        assertEqual(self.locale._format_timeframe('hours', 2), '2 മണിക്കൂർ')
        assertEqual(self.locale._format_timeframe('hour', 0), 'ഒരു മണിക്കൂർ')

    def test_format_relative_now(self):

        result = self.locale._format_relative('ഇപ്പോൾ', 'now', 0)

        assertEqual(result, 'ഇപ്പോൾ')

    def test_format_relative_past(self):

        result = self.locale._format_relative('ഒരു മണിക്കൂർ', 'hour', 1)
        assertEqual(result, 'ഒരു മണിക്കൂർ ശേഷം')

    def test_format_relative_future(self):

        result = self.locale._format_relative('ഒരു മണിക്കൂർ', 'hour', -1)
        assertEqual(result, 'ഒരു മണിക്കൂർ മുമ്പ്')


class HindiLocaleTests(Chai):

    def setUp(self):
        super(HindiLocaleTests, self).setUp()

        self.locale = locales.HindiLocale()

    def test_format_timeframe(self):

        assertEqual(self.locale._format_timeframe('hours', 2), '2 घंटे')
        assertEqual(self.locale._format_timeframe('hour', 0), 'एक घंट')

    def test_format_relative_now(self):

        result = self.locale._format_relative('अभि', 'now', 0)

        assertEqual(result, 'अभि')

    def test_format_relative_past(self):

        result = self.locale._format_relative('एक घंट', 'hour', 1)
        assertEqual(result, 'एक घंट बाद')

    def test_format_relative_future(self):

        result = self.locale._format_relative('एक घंट', 'hour', -1)
        assertEqual(result, 'एक घंट पहले')

class CzechLocaleTests(Chai):

    def setUp(self):
        super(CzechLocaleTests, self).setUp()

        self.locale = locales.CzechLocale()

    def test_format_timeframe(self):

        assertEqual(self.locale._format_timeframe('hours', 2), '2 hodiny')
        assertEqual(self.locale._format_timeframe('hour', 0), '0 hodin')

    def test_format_relative_now(self):

        result = self.locale._format_relative('Teď', 'now', 0)

        assertEqual(result, 'Teď')
    def test_format_relative_future(self):

        result = self.locale._format_relative('hodinu', 'hour', 1)
        assertEqual(result, 'Za hodinu')

    def test_format_relative_past(self):

        result = self.locale._format_relative('hodinou', 'hour', -1)
        assertEqual(result, 'Před hodinou')
