# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import datetime

from chai import Chai

from arrow import locales
from arrow.api import now
from arrow import arrow

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

    def test_format_relative_now(self):

        result = self.locale._format_relative('just now', 'now', 0)

        assertEqual(result, 'just now')

    def test_format_relative_past(self):

        result = self.locale._format_relative('an hour', 'hour', 1)

        assertEqual(result, 'in an hour')

    def test_format_relative_future(self):

        result = self.locale._format_relative('an hour', 'hour', -1)

        assertEqual(result, 'an hour ago')

    def test_ordinal_number(self):
        assertEqual(self.locale.ordinal_number(0), '0th')
        assertEqual(self.locale.ordinal_number(1), '1st')
        assertEqual(self.locale.ordinal_number(2), '2nd')
        assertEqual(self.locale.ordinal_number(3), '3rd')
        assertEqual(self.locale.ordinal_number(4), '4th')
        assertEqual(self.locale.ordinal_number(10), '10th')
        assertEqual(self.locale.ordinal_number(11), '11th')
        assertEqual(self.locale.ordinal_number(12), '12th')
        assertEqual(self.locale.ordinal_number(13), '13th')
        assertEqual(self.locale.ordinal_number(14), '14th')
        assertEqual(self.locale.ordinal_number(21), '21st')
        assertEqual(self.locale.ordinal_number(22), '22nd')
        assertEqual(self.locale.ordinal_number(23), '23rd')
        assertEqual(self.locale.ordinal_number(24), '24th')

        assertEqual(self.locale.ordinal_number(100), '100th')
        assertEqual(self.locale.ordinal_number(101), '101st')
        assertEqual(self.locale.ordinal_number(102), '102nd')
        assertEqual(self.locale.ordinal_number(103), '103rd')
        assertEqual(self.locale.ordinal_number(104), '104th')
        assertEqual(self.locale.ordinal_number(110), '110th')
        assertEqual(self.locale.ordinal_number(111), '111th')
        assertEqual(self.locale.ordinal_number(112), '112th')
        assertEqual(self.locale.ordinal_number(113), '113th')
        assertEqual(self.locale.ordinal_number(114), '114th')
        assertEqual(self.locale.ordinal_number(121), '121st')
        assertEqual(self.locale.ordinal_number(122), '122nd')
        assertEqual(self.locale.ordinal_number(123), '123rd')
        assertEqual(self.locale.ordinal_number(124), '124th')

    def test_meridian_invalid_token(self):
        assertEqual(self.locale.meridian(7, None), None)
        assertEqual(self.locale.meridian(7, 'B'), None)
        assertEqual(self.locale.meridian(7, 'NONSENSE'), None)


class ItalianLocalesTests(Chai):

    def test_ordinal_number(self):
        locale = locales.ItalianLocale()

        assertEqual(locale.ordinal_number(1), '1°')


class SpanishLocalesTests(Chai):

    def test_ordinal_number(self):
        locale = locales.SpanishLocale()

        assertEqual(locale.ordinal_number(1), '1°')


class FrenchLocalesTests(Chai):

    def test_ordinal_number(self):
        locale = locales.FrenchLocale()

        assertEqual(locale.ordinal_number(1), '1er')
        assertEqual(locale.ordinal_number(2), '2e')


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
        assertEqual(self.locale._format_timeframe('now', 0), 'rétt í þessu')


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

class BengaliLocaleTests(Chai):

    def test_ordinal_number(self):
        locale = locales.BengaliLocale()

        assertEqual(locale.ordinal_number(-1), '-1')
        assertEqual(locale.ordinal_number(0), '0তম')
        assertEqual(locale.ordinal_number(1), '1ম')
        assertEqual(locale.ordinal_number(2), '2য়')
        assertEqual(locale.ordinal_number(4), '4র্থ')
        assertEqual(locale.ordinal_number(6), '6ষ্ঠ')
        assertEqual(locale.ordinal_number(11), '11তম')

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
        assertEqual(self.locale._format_timeframe('hours', 5), '5 hodin')
        assertEqual(self.locale._format_timeframe('hour', 0), '0 hodin')
        assertEqual(self.locale._format_timeframe('hours', -2), '2 hodinami')
        assertEqual(self.locale._format_timeframe('hours', -5), '5 hodinami')
        assertEqual(self.locale._format_timeframe('now', 0), 'Teď')

    def test_format_relative_now(self):

        result = self.locale._format_relative('Teď', 'now', 0)
        assertEqual(result, 'Teď')

    def test_format_relative_future(self):

        result = self.locale._format_relative('hodinu', 'hour', 1)
        assertEqual(result, 'Za hodinu')

    def test_format_relative_past(self):

        result = self.locale._format_relative('hodinou', 'hour', -1)
        assertEqual(result, 'Před hodinou')


class HebrewLocaleTests(Chai):

    def test_couple_of_timeframe(self):
        locale = locales.HebrewLocale()

        assertEqual(locale._format_timeframe('hours', 2), 'שעתיים')
        assertEqual(locale._format_timeframe('months', 2), 'חודשיים')
        assertEqual(locale._format_timeframe('days', 2), 'יומיים')
        assertEqual(locale._format_timeframe('years', 2), 'שנתיים')

        assertEqual(locale._format_timeframe('hours', 3), '3 שעות')
        assertEqual(locale._format_timeframe('months', 4), '4 חודשים')
        assertEqual(locale._format_timeframe('days', 3), '3 ימים')
        assertEqual(locale._format_timeframe('years', 5), '5 שנים')


class MarathiLocaleTests(Chai):

    def setUp(self):
        super(MarathiLocaleTests, self).setUp()

        self.locale = locales.MarathiLocale()

    def test_dateCoreFunctionality(self):
        dt = arrow.Arrow(2015, 4, 11, 17, 30, 00)
        assertEqual (self.locale.month_name(dt.month),'एप्रिल')
        assertEqual (self.locale.month_abbreviation(dt.month),'एप्रि')
        assertEqual (self.locale.day_name(dt.isoweekday()),'शनिवार')
        assertEqual (self.locale.day_abbreviation(dt.isoweekday()), 'शनि')

    def test_format_timeframe(self):
        assertEqual(self.locale._format_timeframe('hours', 2), '2 तास')
        assertEqual(self.locale._format_timeframe('hour', 0), 'एक तास')

    def test_format_relative_now(self):
        result = self.locale._format_relative('सद्य', 'now', 0)
        assertEqual(result, 'सद्य')

    def test_format_relative_past(self):
        result = self.locale._format_relative('एक तास', 'hour', 1)
        assertEqual(result, 'एक तास नंतर')

    def test_format_relative_future(self):
        result = self.locale._format_relative('एक तास', 'hour', -1)
        assertEqual(result, 'एक तास आधी')

    # Not currently implemented
    def test_ordinal_number(self):
        assertEqual(self.locale.ordinal_number(1), '1')


class FinnishLocaleTests(Chai):

    def setUp(self):
        super(FinnishLocaleTests, self).setUp()

        self.locale = locales.FinnishLocale()

    def test_format_timeframe(self):
        assertEqual(self.locale._format_timeframe('hours', 2),
                    ('2 tuntia', '2 tunnin'))
        assertEqual(self.locale._format_timeframe('hour', 0),
                    ('tunti', 'tunnin'))

    def test_format_relative_now(self):
        result = self.locale._format_relative(['juuri nyt', 'juuri nyt'], 'now', 0)
        assertEqual(result, 'juuri nyt')

    def test_format_relative_past(self):
        result = self.locale._format_relative(['tunti', 'tunnin'], 'hour', 1)
        assertEqual(result, 'tunnin kuluttua')

    def test_format_relative_future(self):
        result = self.locale._format_relative(['tunti', 'tunnin'], 'hour', -1)
        assertEqual(result, 'tunti sitten')

    def test_ordinal_number(self):
        assertEqual(self.locale.ordinal_number(1), '1.')


class GermanLocaleTests(Chai):

    def setUp(self):
        super(GermanLocaleTests, self).setUp()

        self.locale = locales.GermanLocale()

    def test_ordinal_number(self):
        assertEqual(self.locale.ordinal_number(1), '1.')


class HungarianLocaleTests(Chai):

    def setUp(self):
        super(HungarianLocaleTests, self).setUp()

        self.locale = locales.HungarianLocale()

    def test_format_timeframe(self):
        assertEqual(self.locale._format_timeframe('hours', 2), '2 óra')
        assertEqual(self.locale._format_timeframe('hour', 0), 'egy órával')
        assertEqual(self.locale._format_timeframe('hours', -2), '2 órával')
        assertEqual(self.locale._format_timeframe('now', 0), 'éppen most')


class ThaiLocaleTests(Chai):

    def setUp(self):
        super(ThaiLocaleTests, self).setUp()

        self.locale = locales.ThaiLocale()

    def test_year_full(self):
        assertEqual(self.locale.year_full(2015), '2558')

    def test_year_abbreviation(self):
        assertEqual(self.locale.year_abbreviation(2015), '58')

    def test_format_relative_now(self):
        result = self.locale._format_relative('ขณะนี้', 'now', 0)
        assertEqual(result, 'ขณะนี้')

    def test_format_relative_past(self):
        result = self.locale._format_relative('1 ชั่วโมง', 'hour', 1)
        assertEqual(result, 'ในอีก 1 ชั่วโมง')
        result = self.locale._format_relative('{0} ชั่วโมง', 'hours', 2)
        assertEqual(result, 'ในอีก {0} ชั่วโมง')
        result = self.locale._format_relative('ไม่กี่วินาที', 'seconds', 42)
        assertEqual(result, 'ในอีกไม่กี่วินาที')

    def test_format_relative_future(self):
        result = self.locale._format_relative('1 ชั่วโมง', 'hour', -1)
        assertEqual(result, '1 ชั่วโมง ที่ผ่านมา')
