# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from chai import Chai

from arrow import arrow, locales


class ModuleTests(Chai):
    def test_get_locale(self):

        mock_locales = self.mock(locales, "_locales")
        mock_locale_cls = self.mock()
        mock_locale = self.mock()

        self.expect(mock_locales.get).args("name").returns(mock_locale_cls)
        self.expect(mock_locale_cls).returns(mock_locale)

        result = locales.get_locale("name")

        self.assertEqual(result, mock_locale)

    def test_locales(self):

        self.assertTrue(len(locales._locales) > 0)


class LocaleTests(Chai):
    def setUp(self):
        super(LocaleTests, self).setUp()

        self.locale = locales.EnglishLocale()

    def test_format_timeframe(self):

        self.assertEqual(self.locale._format_timeframe("hours", 2), "2 hours")
        self.assertEqual(self.locale._format_timeframe("hour", 0), "an hour")

    def test_format_relative_now(self):

        result = self.locale._format_relative("just now", "now", 0)

        self.assertEqual(result, "just now")

    def test_format_relative_past(self):

        result = self.locale._format_relative("an hour", "hour", 1)

        self.assertEqual(result, "in an hour")

    def test_format_relative_future(self):

        result = self.locale._format_relative("an hour", "hour", -1)

        self.assertEqual(result, "an hour ago")

    def test_ordinal_number(self):
        self.assertEqual(self.locale.ordinal_number(0), "0th")
        self.assertEqual(self.locale.ordinal_number(1), "1st")
        self.assertEqual(self.locale.ordinal_number(2), "2nd")
        self.assertEqual(self.locale.ordinal_number(3), "3rd")
        self.assertEqual(self.locale.ordinal_number(4), "4th")
        self.assertEqual(self.locale.ordinal_number(10), "10th")
        self.assertEqual(self.locale.ordinal_number(11), "11th")
        self.assertEqual(self.locale.ordinal_number(12), "12th")
        self.assertEqual(self.locale.ordinal_number(13), "13th")
        self.assertEqual(self.locale.ordinal_number(14), "14th")
        self.assertEqual(self.locale.ordinal_number(21), "21st")
        self.assertEqual(self.locale.ordinal_number(22), "22nd")
        self.assertEqual(self.locale.ordinal_number(23), "23rd")
        self.assertEqual(self.locale.ordinal_number(24), "24th")

        self.assertEqual(self.locale.ordinal_number(100), "100th")
        self.assertEqual(self.locale.ordinal_number(101), "101st")
        self.assertEqual(self.locale.ordinal_number(102), "102nd")
        self.assertEqual(self.locale.ordinal_number(103), "103rd")
        self.assertEqual(self.locale.ordinal_number(104), "104th")
        self.assertEqual(self.locale.ordinal_number(110), "110th")
        self.assertEqual(self.locale.ordinal_number(111), "111th")
        self.assertEqual(self.locale.ordinal_number(112), "112th")
        self.assertEqual(self.locale.ordinal_number(113), "113th")
        self.assertEqual(self.locale.ordinal_number(114), "114th")
        self.assertEqual(self.locale.ordinal_number(121), "121st")
        self.assertEqual(self.locale.ordinal_number(122), "122nd")
        self.assertEqual(self.locale.ordinal_number(123), "123rd")
        self.assertEqual(self.locale.ordinal_number(124), "124th")

    def test_meridian_invalid_token(self):
        self.assertEqual(self.locale.meridian(7, None), None)
        self.assertEqual(self.locale.meridian(7, "B"), None)
        self.assertEqual(self.locale.meridian(7, "NONSENSE"), None)


class EnglishLocaleTests(Chai):
    def setUp(self):
        super(EnglishLocaleTests, self).setUp()

        self.locale = locales.EnglishLocale()

    def test_describe(self):
        self.assertEqual(self.locale.describe("now", only_distance=True), "instantly")
        self.assertEqual(self.locale.describe("now", only_distance=False), "just now")


class ItalianLocalesTests(Chai):
    def test_ordinal_number(self):
        locale = locales.ItalianLocale()

        self.assertEqual(locale.ordinal_number(1), "1º")


class SpanishLocalesTests(Chai):
    def test_ordinal_number(self):
        locale = locales.SpanishLocale()

        self.assertEqual(locale.ordinal_number(1), "1º")


class FrenchLocalesTests(Chai):
    def test_ordinal_number(self):
        locale = locales.FrenchLocale()

        self.assertEqual(locale.ordinal_number(1), "1er")
        self.assertEqual(locale.ordinal_number(2), "2e")


class RussianLocalesTests(Chai):
    def test_plurals2(self):

        locale = locales.RussianLocale()

        self.assertEqual(locale._format_timeframe("hours", 0), "0 часов")
        self.assertEqual(locale._format_timeframe("hours", 1), "1 час")
        self.assertEqual(locale._format_timeframe("hours", 2), "2 часа")
        self.assertEqual(locale._format_timeframe("hours", 4), "4 часа")
        self.assertEqual(locale._format_timeframe("hours", 5), "5 часов")
        self.assertEqual(locale._format_timeframe("hours", 21), "21 час")
        self.assertEqual(locale._format_timeframe("hours", 22), "22 часа")
        self.assertEqual(locale._format_timeframe("hours", 25), "25 часов")

        # feminine grammatical gender should be tested separately
        self.assertEqual(locale._format_timeframe("minutes", 0), "0 минут")
        self.assertEqual(locale._format_timeframe("minutes", 1), "1 минуту")
        self.assertEqual(locale._format_timeframe("minutes", 2), "2 минуты")
        self.assertEqual(locale._format_timeframe("minutes", 4), "4 минуты")
        self.assertEqual(locale._format_timeframe("minutes", 5), "5 минут")
        self.assertEqual(locale._format_timeframe("minutes", 21), "21 минуту")
        self.assertEqual(locale._format_timeframe("minutes", 22), "22 минуты")
        self.assertEqual(locale._format_timeframe("minutes", 25), "25 минут")


class PolishLocalesTests(Chai):
    def test_plurals(self):

        locale = locales.PolishLocale()

        self.assertEqual(locale._format_timeframe("hours", 0), "0 godzin")
        self.assertEqual(locale._format_timeframe("hours", 1), "1 godzin")
        self.assertEqual(locale._format_timeframe("hours", 2), "2 godziny")
        self.assertEqual(locale._format_timeframe("hours", 4), "4 godziny")
        self.assertEqual(locale._format_timeframe("hours", 5), "5 godzin")
        self.assertEqual(locale._format_timeframe("hours", 21), "21 godzin")
        self.assertEqual(locale._format_timeframe("hours", 22), "22 godziny")
        self.assertEqual(locale._format_timeframe("hours", 25), "25 godzin")


class IcelandicLocalesTests(Chai):
    def setUp(self):
        super(IcelandicLocalesTests, self).setUp()

        self.locale = locales.IcelandicLocale()

    def test_format_timeframe(self):

        self.assertEqual(self.locale._format_timeframe("minute", -1), "einni mínútu")
        self.assertEqual(self.locale._format_timeframe("minute", 1), "eina mínútu")

        self.assertEqual(self.locale._format_timeframe("hours", -2), "2 tímum")
        self.assertEqual(self.locale._format_timeframe("hours", 2), "2 tíma")
        self.assertEqual(self.locale._format_timeframe("now", 0), "rétt í þessu")


class MalayalamLocaleTests(Chai):
    def setUp(self):
        super(MalayalamLocaleTests, self).setUp()

        self.locale = locales.MalayalamLocale()

    def test_format_timeframe(self):

        self.assertEqual(self.locale._format_timeframe("hours", 2), "2 മണിക്കൂർ")
        self.assertEqual(self.locale._format_timeframe("hour", 0), "ഒരു മണിക്കൂർ")

    def test_format_relative_now(self):

        result = self.locale._format_relative("ഇപ്പോൾ", "now", 0)

        self.assertEqual(result, "ഇപ്പോൾ")

    def test_format_relative_past(self):

        result = self.locale._format_relative("ഒരു മണിക്കൂർ", "hour", 1)
        self.assertEqual(result, "ഒരു മണിക്കൂർ ശേഷം")

    def test_format_relative_future(self):

        result = self.locale._format_relative("ഒരു മണിക്കൂർ", "hour", -1)
        self.assertEqual(result, "ഒരു മണിക്കൂർ മുമ്പ്")


class HindiLocaleTests(Chai):
    def setUp(self):
        super(HindiLocaleTests, self).setUp()

        self.locale = locales.HindiLocale()

    def test_format_timeframe(self):

        self.assertEqual(self.locale._format_timeframe("hours", 2), "2 घंटे")
        self.assertEqual(self.locale._format_timeframe("hour", 0), "एक घंटा")

    def test_format_relative_now(self):

        result = self.locale._format_relative("अभी", "now", 0)

        self.assertEqual(result, "अभी")

    def test_format_relative_past(self):

        result = self.locale._format_relative("एक घंटा", "hour", 1)
        self.assertEqual(result, "एक घंटा बाद")

    def test_format_relative_future(self):

        result = self.locale._format_relative("एक घंटा", "hour", -1)
        self.assertEqual(result, "एक घंटा पहले")


class CzechLocaleTests(Chai):
    def setUp(self):
        super(CzechLocaleTests, self).setUp()

        self.locale = locales.CzechLocale()

    def test_format_timeframe(self):

        self.assertEqual(self.locale._format_timeframe("hours", 2), "2 hodiny")
        self.assertEqual(self.locale._format_timeframe("hours", 5), "5 hodin")
        self.assertEqual(self.locale._format_timeframe("hour", 0), "0 hodin")
        self.assertEqual(self.locale._format_timeframe("hours", -2), "2 hodinami")
        self.assertEqual(self.locale._format_timeframe("hours", -5), "5 hodinami")
        self.assertEqual(self.locale._format_timeframe("now", 0), "Teď")

    def test_format_relative_now(self):

        result = self.locale._format_relative("Teď", "now", 0)
        self.assertEqual(result, "Teď")

    def test_format_relative_future(self):

        result = self.locale._format_relative("hodinu", "hour", 1)
        self.assertEqual(result, "Za hodinu")

    def test_format_relative_past(self):

        result = self.locale._format_relative("hodinou", "hour", -1)
        self.assertEqual(result, "Před hodinou")


class SlovakLocaleTests(Chai):
    def setUp(self):
        super(SlovakLocaleTests, self).setUp()

        self.locale = locales.SlovakLocale()

    def test_format_timeframe(self):

        self.assertEqual(self.locale._format_timeframe("hours", 2), "2 hodiny")
        self.assertEqual(self.locale._format_timeframe("hours", 5), "5 hodín")
        self.assertEqual(self.locale._format_timeframe("hour", 0), "0 hodín")
        self.assertEqual(self.locale._format_timeframe("hours", -2), "2 hodinami")
        self.assertEqual(self.locale._format_timeframe("hours", -5), "5 hodinami")
        self.assertEqual(self.locale._format_timeframe("now", 0), "Teraz")

    def test_format_relative_now(self):

        result = self.locale._format_relative("Teraz", "now", 0)
        self.assertEqual(result, "Teraz")

    def test_format_relative_future(self):

        result = self.locale._format_relative("hodinu", "hour", 1)
        self.assertEqual(result, "O hodinu")

    def test_format_relative_past(self):

        result = self.locale._format_relative("hodinou", "hour", -1)
        self.assertEqual(result, "Pred hodinou")


class BulgarianLocaleTests(Chai):
    def test_plurals2(self):

        locale = locales.BulgarianLocale()

        self.assertEqual(locale._format_timeframe("hours", 0), "0 часа")
        self.assertEqual(locale._format_timeframe("hours", 1), "1 час")
        self.assertEqual(locale._format_timeframe("hours", 2), "2 часа")
        self.assertEqual(locale._format_timeframe("hours", 4), "4 часа")
        self.assertEqual(locale._format_timeframe("hours", 5), "5 часа")
        self.assertEqual(locale._format_timeframe("hours", 21), "21 час")
        self.assertEqual(locale._format_timeframe("hours", 22), "22 часа")
        self.assertEqual(locale._format_timeframe("hours", 25), "25 часа")

        # feminine grammatical gender should be tested separately
        self.assertEqual(locale._format_timeframe("minutes", 0), "0 минути")
        self.assertEqual(locale._format_timeframe("minutes", 1), "1 минута")
        self.assertEqual(locale._format_timeframe("minutes", 2), "2 минути")
        self.assertEqual(locale._format_timeframe("minutes", 4), "4 минути")
        self.assertEqual(locale._format_timeframe("minutes", 5), "5 минути")
        self.assertEqual(locale._format_timeframe("minutes", 21), "21 минута")
        self.assertEqual(locale._format_timeframe("minutes", 22), "22 минути")
        self.assertEqual(locale._format_timeframe("minutes", 25), "25 минути")


class HebrewLocaleTests(Chai):
    def test_couple_of_timeframe(self):
        locale = locales.HebrewLocale()

        self.assertEqual(locale._format_timeframe("hours", 2), "שעתיים")
        self.assertEqual(locale._format_timeframe("months", 2), "חודשיים")
        self.assertEqual(locale._format_timeframe("days", 2), "יומיים")
        self.assertEqual(locale._format_timeframe("years", 2), "שנתיים")

        self.assertEqual(locale._format_timeframe("hours", 3), "3 שעות")
        self.assertEqual(locale._format_timeframe("months", 4), "4 חודשים")
        self.assertEqual(locale._format_timeframe("days", 3), "3 ימים")
        self.assertEqual(locale._format_timeframe("years", 5), "5 שנים")


class MarathiLocaleTests(Chai):
    def setUp(self):
        super(MarathiLocaleTests, self).setUp()

        self.locale = locales.MarathiLocale()

    def test_dateCoreFunctionality(self):
        dt = arrow.Arrow(2015, 4, 11, 17, 30, 00)
        self.assertEqual(self.locale.month_name(dt.month), "एप्रिल")
        self.assertEqual(self.locale.month_abbreviation(dt.month), "एप्रि")
        self.assertEqual(self.locale.day_name(dt.isoweekday()), "शनिवार")
        self.assertEqual(self.locale.day_abbreviation(dt.isoweekday()), "शनि")

    def test_format_timeframe(self):
        self.assertEqual(self.locale._format_timeframe("hours", 2), "2 तास")
        self.assertEqual(self.locale._format_timeframe("hour", 0), "एक तास")

    def test_format_relative_now(self):
        result = self.locale._format_relative("सद्य", "now", 0)
        self.assertEqual(result, "सद्य")

    def test_format_relative_past(self):
        result = self.locale._format_relative("एक तास", "hour", 1)
        self.assertEqual(result, "एक तास नंतर")

    def test_format_relative_future(self):
        result = self.locale._format_relative("एक तास", "hour", -1)
        self.assertEqual(result, "एक तास आधी")

    # Not currently implemented
    def test_ordinal_number(self):
        self.assertEqual(self.locale.ordinal_number(1), "1")


class FinnishLocaleTests(Chai):
    def setUp(self):
        super(FinnishLocaleTests, self).setUp()

        self.locale = locales.FinnishLocale()

    def test_format_timeframe(self):
        self.assertEqual(
            self.locale._format_timeframe("hours", 2), ("2 tuntia", "2 tunnin")
        )
        self.assertEqual(self.locale._format_timeframe("hour", 0), ("tunti", "tunnin"))

    def test_format_relative_now(self):
        result = self.locale._format_relative(["juuri nyt", "juuri nyt"], "now", 0)
        self.assertEqual(result, "juuri nyt")

    def test_format_relative_past(self):
        result = self.locale._format_relative(["tunti", "tunnin"], "hour", 1)
        self.assertEqual(result, "tunnin kuluttua")

    def test_format_relative_future(self):
        result = self.locale._format_relative(["tunti", "tunnin"], "hour", -1)
        self.assertEqual(result, "tunti sitten")

    def test_ordinal_number(self):
        self.assertEqual(self.locale.ordinal_number(1), "1.")


class GermanLocaleTests(Chai):
    def setUp(self):
        super(GermanLocaleTests, self).setUp()

        self.locale = locales.GermanLocale()

    def test_ordinal_number(self):
        self.assertEqual(self.locale.ordinal_number(1), "1.")

    def test_define(self):
        self.assertEqual(
            self.locale.describe("minute", only_distance=True), "eine Minute"
        )
        self.assertEqual(
            self.locale.describe("minute", only_distance=False), "in einer Minute"
        )
        self.assertEqual(
            self.locale.describe("hour", only_distance=True), "eine Stunde"
        )
        self.assertEqual(
            self.locale.describe("hour", only_distance=False), "in einer Stunde"
        )
        self.assertEqual(self.locale.describe("day", only_distance=True), "ein Tag")
        self.assertEqual(
            self.locale.describe("day", only_distance=False), "in einem Tag"
        )
        self.assertEqual(self.locale.describe("month", only_distance=True), "ein Monat")
        self.assertEqual(
            self.locale.describe("month", only_distance=False), "in einem Monat"
        )
        self.assertEqual(self.locale.describe("year", only_distance=True), "ein Jahr")
        self.assertEqual(
            self.locale.describe("year", only_distance=False), "in einem Jahr"
        )


class HungarianLocaleTests(Chai):
    def setUp(self):
        super(HungarianLocaleTests, self).setUp()

        self.locale = locales.HungarianLocale()

    def test_format_timeframe(self):
        self.assertEqual(self.locale._format_timeframe("hours", 2), "2 óra")
        self.assertEqual(self.locale._format_timeframe("hour", 0), "egy órával")
        self.assertEqual(self.locale._format_timeframe("hours", -2), "2 órával")
        self.assertEqual(self.locale._format_timeframe("now", 0), "éppen most")


class EsperantoLocaleTests(Chai):
    def setUp(self):
        super(EsperantoLocaleTests, self).setUp()

        self.locale = locales.EsperantoLocale()

    def test_format_timeframe(self):
        self.assertEqual(self.locale._format_timeframe("hours", 2), "2 horoj")
        self.assertEqual(self.locale._format_timeframe("hour", 0), "un horo")
        self.assertEqual(self.locale._format_timeframe("hours", -2), "2 horoj")
        self.assertEqual(self.locale._format_timeframe("now", 0), "nun")

    def test_ordinal_number(self):
        self.assertEqual(self.locale.ordinal_number(1), "1a")


class ThaiLocaleTests(Chai):
    def setUp(self):
        super(ThaiLocaleTests, self).setUp()

        self.locale = locales.ThaiLocale()

    def test_year_full(self):
        self.assertEqual(self.locale.year_full(2015), "2558")

    def test_year_abbreviation(self):
        self.assertEqual(self.locale.year_abbreviation(2015), "58")

    def test_format_relative_now(self):
        result = self.locale._format_relative("ขณะนี้", "now", 0)
        self.assertEqual(result, "ขณะนี้")

    def test_format_relative_past(self):
        result = self.locale._format_relative("1 ชั่วโมง", "hour", 1)
        self.assertEqual(result, "ในอีก 1 ชั่วโมง")
        result = self.locale._format_relative("{0} ชั่วโมง", "hours", 2)
        self.assertEqual(result, "ในอีก {0} ชั่วโมง")
        result = self.locale._format_relative("ไม่กี่วินาที", "seconds", 42)
        self.assertEqual(result, "ในอีกไม่กี่วินาที")

    def test_format_relative_future(self):
        result = self.locale._format_relative("1 ชั่วโมง", "hour", -1)
        self.assertEqual(result, "1 ชั่วโมง ที่ผ่านมา")


class BengaliLocaleTests(Chai):
    def setUp(self):
        super(BengaliLocaleTests, self).setUp()

        self.locale = locales.BengaliLocale()

    def test_ordinal_number(self):
        result0 = self.locale._ordinal_number(0)
        result1 = self.locale._ordinal_number(1)
        result3 = self.locale._ordinal_number(3)
        result4 = self.locale._ordinal_number(4)
        result5 = self.locale._ordinal_number(5)
        result6 = self.locale._ordinal_number(6)
        result10 = self.locale._ordinal_number(10)
        result11 = self.locale._ordinal_number(11)
        result42 = self.locale._ordinal_number(42)
        self.assertEqual(result0, "0তম")
        self.assertEqual(result1, "1ম")
        self.assertEqual(result3, "3য়")
        self.assertEqual(result4, "4র্থ")
        self.assertEqual(result5, "5ম")
        self.assertEqual(result6, "6ষ্ঠ")
        self.assertEqual(result10, "10ম")
        self.assertEqual(result11, "11তম")
        self.assertEqual(result42, "42তম")
        self.assertEqual(self.locale._ordinal_number(-1), None)


class SwissLocaleTests(Chai):
    def setUp(self):
        super(SwissLocaleTests, self).setUp()

        self.locale = locales.SwissLocale()

    def test_ordinal_number(self):
        dt = arrow.Arrow(2015, 4, 11, 17, 30, 00)

        self.assertEqual(self.locale._format_timeframe("minute", 1), "einer Minute")
        self.assertEqual(self.locale._format_timeframe("hour", 1), "einer Stunde")
        self.assertEqual(self.locale.day_abbreviation(dt.isoweekday()), "Sa")


class RomanianLocaleTests(Chai):
    def setUp(self):
        super(RomanianLocaleTests, self).setUp()

        self.locale = locales.RomanianLocale()

    def test_timeframes(self):

        self.assertEqual(self.locale._format_timeframe("hours", 2), "2 ore")
        self.assertEqual(self.locale._format_timeframe("months", 2), "2 luni")

        self.assertEqual(self.locale._format_timeframe("days", 2), "2 zile")
        self.assertEqual(self.locale._format_timeframe("years", 2), "2 ani")

        self.assertEqual(self.locale._format_timeframe("hours", 3), "3 ore")
        self.assertEqual(self.locale._format_timeframe("months", 4), "4 luni")
        self.assertEqual(self.locale._format_timeframe("days", 3), "3 zile")
        self.assertEqual(self.locale._format_timeframe("years", 5), "5 ani")

    def test_relative_timeframes(self):
        self.assertEqual(self.locale._format_relative("acum", "now", 0), "acum")
        self.assertEqual(
            self.locale._format_relative("o oră", "hour", 1), "peste o oră"
        )
        self.assertEqual(
            self.locale._format_relative("o oră", "hour", -1), "o oră în urmă"
        )
        self.assertEqual(
            self.locale._format_relative("un minut", "minute", 1), "peste un minut"
        )
        self.assertEqual(
            self.locale._format_relative("un minut", "minute", -1), "un minut în urmă"
        )
        self.assertEqual(
            self.locale._format_relative("câteva secunde", "seconds", -1),
            "câteva secunde în urmă",
        )
        self.assertEqual(
            self.locale._format_relative("câteva secunde", "seconds", 1),
            "peste câteva secunde",
        )
        self.assertEqual(
            self.locale._format_relative("o zi", "day", -1), "o zi în urmă"
        )
        self.assertEqual(self.locale._format_relative("o zi", "day", 1), "peste o zi")


class ArabicLocalesTest(Chai):
    def setUp(self):
        super(ArabicLocalesTest, self).setUp()

        self.locale = locales.ArabicLocale()

    def test_timeframes(self):

        # single
        self.assertEqual(self.locale._format_timeframe("minute", 1), "دقيقة")
        self.assertEqual(self.locale._format_timeframe("hour", 1), "ساعة")
        self.assertEqual(self.locale._format_timeframe("day", 1), "يوم")
        self.assertEqual(self.locale._format_timeframe("month", 1), "شهر")
        self.assertEqual(self.locale._format_timeframe("year", 1), "سنة")

        # double
        self.assertEqual(self.locale._format_timeframe("minutes", 2), "دقيقتين")
        self.assertEqual(self.locale._format_timeframe("hours", 2), "ساعتين")
        self.assertEqual(self.locale._format_timeframe("days", 2), "يومين")
        self.assertEqual(self.locale._format_timeframe("months", 2), "شهرين")
        self.assertEqual(self.locale._format_timeframe("years", 2), "سنتين")

        # up to ten
        self.assertEqual(self.locale._format_timeframe("minutes", 3), "3 دقائق")
        self.assertEqual(self.locale._format_timeframe("hours", 4), "4 ساعات")
        self.assertEqual(self.locale._format_timeframe("days", 5), "5 أيام")
        self.assertEqual(self.locale._format_timeframe("months", 6), "6 أشهر")
        self.assertEqual(self.locale._format_timeframe("years", 10), "10 سنوات")

        # more than ten
        self.assertEqual(self.locale._format_timeframe("minutes", 11), "11 دقيقة")
        self.assertEqual(self.locale._format_timeframe("hours", 19), "19 ساعة")
        self.assertEqual(self.locale._format_timeframe("months", 24), "24 شهر")
        self.assertEqual(self.locale._format_timeframe("days", 50), "50 يوم")
        self.assertEqual(self.locale._format_timeframe("years", 115), "115 سنة")


class NepaliLocaleTests(Chai):
    def setUp(self):
        super(NepaliLocaleTests, self).setUp()

        self.locale = locales.NepaliLocale()

    def test_format_timeframe(self):
        self.assertEqual(self.locale._format_timeframe("hours", 3), "3 घण्टा")
        self.assertEqual(self.locale._format_timeframe("hour", 0), "एक घण्टा")

    def test_format_relative_now(self):
        result = self.locale._format_relative("अहिले", "now", 0)
        self.assertEqual(result, "अहिले")

    def test_format_relative_future(self):
        result = self.locale._format_relative("एक घण्टा", "hour", 1)
        self.assertEqual(result, "एक घण्टा पछी")

    def test_format_relative_past(self):
        result = self.locale._format_relative("एक घण्टा", "hour", -1)
        self.assertEqual(result, "एक घण्टा पहिले")


class IndonesianLocaleTests(Chai):
    def setUp(self):
        super(IndonesianLocaleTests, self).setUp()

        self.locale = locales.IndonesianLocale()

    def test_timeframes(self):
        self.assertEqual(self.locale._format_timeframe("hours", 2), "2 jam")
        self.assertEqual(self.locale._format_timeframe("months", 2), "2 bulan")

        self.assertEqual(self.locale._format_timeframe("days", 2), "2 hari")
        self.assertEqual(self.locale._format_timeframe("years", 2), "2 tahun")

        self.assertEqual(self.locale._format_timeframe("hours", 3), "3 jam")
        self.assertEqual(self.locale._format_timeframe("months", 4), "4 bulan")
        self.assertEqual(self.locale._format_timeframe("days", 3), "3 hari")
        self.assertEqual(self.locale._format_timeframe("years", 5), "5 tahun")

    def test_format_relative_now(self):
        self.assertEqual(
            self.locale._format_relative("baru saja", "now", 0), "baru saja"
        )

    def test_format_relative_past(self):
        self.assertEqual(
            self.locale._format_relative("1 jam", "hour", 1), "dalam 1 jam"
        )
        self.assertEqual(
            self.locale._format_relative("1 detik", "seconds", 1), "dalam 1 detik"
        )

    def test_format_relative_future(self):
        self.assertEqual(
            self.locale._format_relative("1 jam", "hour", -1), "1 jam yang lalu"
        )


class TagalogLocaleTests(Chai):
    def setUp(self):
        super(TagalogLocaleTests, self).setUp()

        self.locale = locales.TagalogLocale()

    def test_format_timeframe(self):

        self.assertEqual(self.locale._format_timeframe("minute", 1), "isang minuto")
        self.assertEqual(self.locale._format_timeframe("hour", 1), "isang oras")
        self.assertEqual(self.locale._format_timeframe("month", 1), "isang buwan")
        self.assertEqual(self.locale._format_timeframe("year", 1), "isang taon")

        self.assertEqual(self.locale._format_timeframe("seconds", 2), "segundo")
        self.assertEqual(self.locale._format_timeframe("minutes", 3), "3 minuto")
        self.assertEqual(self.locale._format_timeframe("hours", 4), "4 oras")
        self.assertEqual(self.locale._format_timeframe("months", 5), "5 buwan")
        self.assertEqual(self.locale._format_timeframe("years", 6), "6 taon")

    def test_format_relative_now(self):
        self.assertEqual(
            self.locale._format_relative("ngayon lang", "now", 0), "ngayon lang"
        )

    def test_format_relative_past(self):
        self.assertEqual(
            self.locale._format_relative("2 oras", "hour", 2), "2 oras mula ngayon"
        )

    def test_format_relative_future(self):
        self.assertEqual(
            self.locale._format_relative("3 oras", "hour", -3), "nakaraang 3 oras"
        )

    def test_ordinal_number(self):
        self.assertEqual(self.locale.ordinal_number(0), "ika-0")
        self.assertEqual(self.locale.ordinal_number(1), "ika-1")
        self.assertEqual(self.locale.ordinal_number(2), "ika-2")
        self.assertEqual(self.locale.ordinal_number(3), "ika-3")
        self.assertEqual(self.locale.ordinal_number(10), "ika-10")
        self.assertEqual(self.locale.ordinal_number(23), "ika-23")
        self.assertEqual(self.locale.ordinal_number(100), "ika-100")
        self.assertEqual(self.locale.ordinal_number(103), "ika-103")
        self.assertEqual(self.locale.ordinal_number(114), "ika-114")


class EstonianLocaleTests(Chai):
    def setUp(self):
        super(EstonianLocaleTests, self).setUp()

        self.locale = locales.EstonianLocale()

    def test_format_timeframe(self):
        self.assertEqual(self.locale._format_timeframe("now", 0), "just nüüd")
        self.assertEqual(self.locale._format_timeframe("second", 1), "ühe sekundi")
        self.assertEqual(self.locale._format_timeframe("seconds", 3), "3 sekundi")
        self.assertEqual(self.locale._format_timeframe("seconds", 30), "30 sekundi")
        self.assertEqual(self.locale._format_timeframe("minute", 1), "ühe minuti")
        self.assertEqual(self.locale._format_timeframe("minutes", 4), "4 minuti")
        self.assertEqual(self.locale._format_timeframe("minutes", 40), "40 minuti")
        self.assertEqual(self.locale._format_timeframe("hour", 1), "tunni aja")
        self.assertEqual(self.locale._format_timeframe("hours", 5), "5 tunni")
        self.assertEqual(self.locale._format_timeframe("hours", 23), "23 tunni")
        self.assertEqual(self.locale._format_timeframe("day", 1), "ühe päeva")
        self.assertEqual(self.locale._format_timeframe("days", 6), "6 päeva")
        self.assertEqual(self.locale._format_timeframe("days", 12), "12 päeva")
        self.assertEqual(self.locale._format_timeframe("month", 1), "ühe kuu")
        self.assertEqual(self.locale._format_timeframe("months", 7), "7 kuu")
        self.assertEqual(self.locale._format_timeframe("months", 11), "11 kuu")
        self.assertEqual(self.locale._format_timeframe("year", 1), "ühe aasta")
        self.assertEqual(self.locale._format_timeframe("years", 8), "8 aasta")
        self.assertEqual(self.locale._format_timeframe("years", 12), "12 aasta")

        self.assertEqual(self.locale._format_timeframe("now", 0), "just nüüd")
        self.assertEqual(self.locale._format_timeframe("second", -1), "üks sekund")
        self.assertEqual(self.locale._format_timeframe("seconds", -9), "9 sekundit")
        self.assertEqual(self.locale._format_timeframe("seconds", -12), "12 sekundit")
        self.assertEqual(self.locale._format_timeframe("minute", -1), "üks minut")
        self.assertEqual(self.locale._format_timeframe("minutes", -2), "2 minutit")
        self.assertEqual(self.locale._format_timeframe("minutes", -10), "10 minutit")
        self.assertEqual(self.locale._format_timeframe("hour", -1), "tund aega")
        self.assertEqual(self.locale._format_timeframe("hours", -3), "3 tundi")
        self.assertEqual(self.locale._format_timeframe("hours", -11), "11 tundi")
        self.assertEqual(self.locale._format_timeframe("day", -1), "üks päev")
        self.assertEqual(self.locale._format_timeframe("days", -2), "2 päeva")
        self.assertEqual(self.locale._format_timeframe("days", -12), "12 päeva")
        self.assertEqual(self.locale._format_timeframe("month", -1), "üks kuu")
        self.assertEqual(self.locale._format_timeframe("months", -3), "3 kuud")
        self.assertEqual(self.locale._format_timeframe("months", -13), "13 kuud")
        self.assertEqual(self.locale._format_timeframe("year", -1), "üks aasta")
        self.assertEqual(self.locale._format_timeframe("years", -4), "4 aastat")
        self.assertEqual(self.locale._format_timeframe("years", -14), "14 aastat")
