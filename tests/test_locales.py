import pytest

from arrow import arrow, locales


class TestLocaleValidation:
    """Validate locales to ensure that translations are valid and complete"""

    @classmethod
    def setup_class(cls):
        cls.locales = locales._locales

    def test_locale_validation(self):

        for _, locale_cls in self.locales.items():
            # 7 days + 1 spacer to allow for 1-indexing of months
            assert len(locale_cls.day_names) == 8
            assert locale_cls.day_names[0] == ""
            # ensure that all string from index 1 onward are valid (not blank or None)
            assert all(locale_cls.day_names[1:])

            assert len(locale_cls.day_abbreviations) == 8
            assert locale_cls.day_abbreviations[0] == ""
            assert all(locale_cls.day_abbreviations[1:])

            # 12 months + 1 spacer to allow for 1-indexing of months
            assert len(locale_cls.month_names) == 13
            assert locale_cls.month_names[0] == ""
            assert all(locale_cls.month_names[1:])

            assert len(locale_cls.month_abbreviations) == 13
            assert locale_cls.month_abbreviations[0] == ""
            assert all(locale_cls.month_abbreviations[1:])

            assert len(locale_cls.names) > 0
            assert locale_cls.past is not None
            assert locale_cls.future is not None


class TestModule:
    def test_get_locale(self, mocker):
        mock_locale = mocker.Mock()
        mock_locale_cls = mocker.Mock()
        mock_locale_cls.return_value = mock_locale

        with pytest.raises(ValueError):
            arrow.locales.get_locale("locale_name")

        cls_dict = arrow.locales._locales
        mocker.patch.dict(cls_dict, {"locale_name": mock_locale_cls})

        result = arrow.locales.get_locale("locale_name")

        assert result == mock_locale

    def test_locales(self):

        assert len(locales._locales) > 0


class TestLocale:
    @classmethod
    def setup_class(cls):
        cls.locale = locales.EnglishLocale()

    def test_format_timeframe(self):

        assert self.locale._format_timeframe("hours", 2) == "2 hours"
        assert self.locale._format_timeframe("hour", 0) == "an hour"

    def test_format_relative_now(self):

        result = self.locale._format_relative("just now", "now", 0)

        assert result == "just now"

    def test_format_relative_past(self):

        result = self.locale._format_relative("an hour", "hour", 1)

        assert result == "in an hour"

    def test_format_relative_future(self):

        result = self.locale._format_relative("an hour", "hour", -1)

        assert result == "an hour ago"

    def test_ordinal_number(self):
        assert self.locale.ordinal_number(0) == "0th"
        assert self.locale.ordinal_number(1) == "1st"
        assert self.locale.ordinal_number(2) == "2nd"
        assert self.locale.ordinal_number(3) == "3rd"
        assert self.locale.ordinal_number(4) == "4th"
        assert self.locale.ordinal_number(10) == "10th"
        assert self.locale.ordinal_number(11) == "11th"
        assert self.locale.ordinal_number(12) == "12th"
        assert self.locale.ordinal_number(13) == "13th"
        assert self.locale.ordinal_number(14) == "14th"
        assert self.locale.ordinal_number(21) == "21st"
        assert self.locale.ordinal_number(22) == "22nd"
        assert self.locale.ordinal_number(23) == "23rd"
        assert self.locale.ordinal_number(24) == "24th"

        assert self.locale.ordinal_number(100) == "100th"
        assert self.locale.ordinal_number(101) == "101st"
        assert self.locale.ordinal_number(102) == "102nd"
        assert self.locale.ordinal_number(103) == "103rd"
        assert self.locale.ordinal_number(104) == "104th"
        assert self.locale.ordinal_number(110) == "110th"
        assert self.locale.ordinal_number(111) == "111th"
        assert self.locale.ordinal_number(112) == "112th"
        assert self.locale.ordinal_number(113) == "113th"
        assert self.locale.ordinal_number(114) == "114th"
        assert self.locale.ordinal_number(121) == "121st"
        assert self.locale.ordinal_number(122) == "122nd"
        assert self.locale.ordinal_number(123) == "123rd"
        assert self.locale.ordinal_number(124) == "124th"

    def test_meridian_invalid_token(self):
        assert self.locale.meridian(7, None) is None
        assert self.locale.meridian(7, "B") is None
        assert self.locale.meridian(7, "NONSENSE") is None


class TestEnglishLocale:
    @classmethod
    def setup_class(cls):
        cls.locale = locales.EnglishLocale()

    def test_describe(self):
        assert self.locale.describe("now", only_distance=True) == "instantly"
        assert self.locale.describe("now", only_distance=False) == "just now"


class TestItalianLocales:
    def test_ordinal_number(self):
        locale = locales.ItalianLocale()

        assert locale.ordinal_number(1) == "1º"


class TestSpanishLocales:
    def test_ordinal_number(self):
        locale = locales.SpanishLocale()

        assert locale.ordinal_number(1) == "1º"

    def test_format_timeframe(self):
        locale = locales.SpanishLocale()
        assert locale._format_timeframe("now", 0) == "ahora"
        assert locale._format_timeframe("seconds", 1) == "1 segundos"
        assert locale._format_timeframe("seconds", 3) == "3 segundos"
        assert locale._format_timeframe("seconds", 30) == "30 segundos"
        assert locale._format_timeframe("minute", 1) == "un minuto"
        assert locale._format_timeframe("minutes", 4) == "4 minutos"
        assert locale._format_timeframe("minutes", 40) == "40 minutos"
        assert locale._format_timeframe("hour", 1) == "una hora"
        assert locale._format_timeframe("hours", 5) == "5 horas"
        assert locale._format_timeframe("hours", 23) == "23 horas"
        assert locale._format_timeframe("day", 1) == "un día"
        assert locale._format_timeframe("days", 6) == "6 días"
        assert locale._format_timeframe("days", 12) == "12 días"
        assert locale._format_timeframe("week", 1) == "una semana"
        assert locale._format_timeframe("weeks", 2) == "2 semanas"
        assert locale._format_timeframe("weeks", 3) == "3 semanas"
        assert locale._format_timeframe("month", 1) == "un mes"
        assert locale._format_timeframe("months", 7) == "7 meses"
        assert locale._format_timeframe("months", 11) == "11 meses"
        assert locale._format_timeframe("year", 1) == "un año"
        assert locale._format_timeframe("years", 8) == "8 años"
        assert locale._format_timeframe("years", 12) == "12 años"

        assert locale._format_timeframe("now", 0) == "ahora"
        assert locale._format_timeframe("seconds", -1) == "1 segundos"
        assert locale._format_timeframe("seconds", -9) == "9 segundos"
        assert locale._format_timeframe("seconds", -12) == "12 segundos"
        assert locale._format_timeframe("minute", -1) == "un minuto"
        assert locale._format_timeframe("minutes", -2) == "2 minutos"
        assert locale._format_timeframe("minutes", -10) == "10 minutos"
        assert locale._format_timeframe("hour", -1) == "una hora"
        assert locale._format_timeframe("hours", -3) == "3 horas"
        assert locale._format_timeframe("hours", -11) == "11 horas"
        assert locale._format_timeframe("day", -1) == "un día"
        assert locale._format_timeframe("days", -2) == "2 días"
        assert locale._format_timeframe("days", -12) == "12 días"
        assert locale._format_timeframe("week", -1) == "una semana"
        assert locale._format_timeframe("weeks", -2) == "2 semanas"
        assert locale._format_timeframe("weeks", -3) == "3 semanas"
        assert locale._format_timeframe("month", -1) == "un mes"
        assert locale._format_timeframe("months", -3) == "3 meses"
        assert locale._format_timeframe("months", -13) == "13 meses"
        assert locale._format_timeframe("year", -1) == "un año"
        assert locale._format_timeframe("years", -4) == "4 años"
        assert locale._format_timeframe("years", -14) == "14 años"


class TestFrenchLocales:
    def test_ordinal_number(self):
        locale = locales.FrenchLocale()

        assert locale.ordinal_number(1) == "1er"
        assert locale.ordinal_number(2) == "2e"


class TestRussianLocales:
    def test_plurals2(self):

        locale = locales.RussianLocale()

        assert locale._format_timeframe("hours", 0) == "0 часов"
        assert locale._format_timeframe("hours", 1) == "1 час"
        assert locale._format_timeframe("hours", 2) == "2 часа"
        assert locale._format_timeframe("hours", 4) == "4 часа"
        assert locale._format_timeframe("hours", 5) == "5 часов"
        assert locale._format_timeframe("hours", 21) == "21 час"
        assert locale._format_timeframe("hours", 22) == "22 часа"
        assert locale._format_timeframe("hours", 25) == "25 часов"

        # feminine grammatical gender should be tested separately
        assert locale._format_timeframe("minutes", 0) == "0 минут"
        assert locale._format_timeframe("minutes", 1) == "1 минуту"
        assert locale._format_timeframe("minutes", 2) == "2 минуты"
        assert locale._format_timeframe("minutes", 4) == "4 минуты"
        assert locale._format_timeframe("minutes", 5) == "5 минут"
        assert locale._format_timeframe("minutes", 21) == "21 минуту"
        assert locale._format_timeframe("minutes", 22) == "22 минуты"
        assert locale._format_timeframe("minutes", 25) == "25 минут"


class TestPolishLocales:
    def test_plurals(self):

        locale = locales.PolishLocale()

        assert locale._format_timeframe("hours", 0) == "0 godzin"
        assert locale._format_timeframe("hours", 1) == "1 godzin"
        assert locale._format_timeframe("hours", 2) == "2 godziny"
        assert locale._format_timeframe("hours", 4) == "4 godziny"
        assert locale._format_timeframe("hours", 5) == "5 godzin"
        assert locale._format_timeframe("hours", 21) == "21 godzin"
        assert locale._format_timeframe("hours", 22) == "22 godziny"
        assert locale._format_timeframe("hours", 25) == "25 godzin"


class TestIcelandicLocales:
    @classmethod
    def setup_class(cls):
        cls.locale = locales.IcelandicLocale()

    def test_format_timeframe(self):

        assert self.locale._format_timeframe("minute", -1) == "einni mínútu"
        assert self.locale._format_timeframe("minute", 1) == "eina mínútu"

        assert self.locale._format_timeframe("hours", -2) == "2 tímum"
        assert self.locale._format_timeframe("hours", 2) == "2 tíma"
        assert self.locale._format_timeframe("now", 0) == "rétt í þessu"


class TestMalayalamLocale:
    @classmethod
    def setup_class(cls):
        cls.locale = locales.MalayalamLocale()

    def test_format_timeframe(self):

        assert self.locale._format_timeframe("hours", 2) == "2 മണിക്കൂർ"
        assert self.locale._format_timeframe("hour", 0) == "ഒരു മണിക്കൂർ"

    def test_format_relative_now(self):

        result = self.locale._format_relative("ഇപ്പോൾ", "now", 0)

        assert result == "ഇപ്പോൾ"

    def test_format_relative_past(self):

        result = self.locale._format_relative("ഒരു മണിക്കൂർ", "hour", 1)
        assert result == "ഒരു മണിക്കൂർ ശേഷം"

    def test_format_relative_future(self):

        result = self.locale._format_relative("ഒരു മണിക്കൂർ", "hour", -1)
        assert result == "ഒരു മണിക്കൂർ മുമ്പ്"


class TestHindiLocale:
    @classmethod
    def setup_class(cls):
        cls.locale = locales.HindiLocale()

    def test_format_timeframe(self):

        assert self.locale._format_timeframe("hours", 2) == "2 घंटे"
        assert self.locale._format_timeframe("hour", 0) == "एक घंटा"

    def test_format_relative_now(self):

        result = self.locale._format_relative("अभी", "now", 0)

        assert result == "अभी"

    def test_format_relative_past(self):

        result = self.locale._format_relative("एक घंटा", "hour", 1)
        assert result == "एक घंटा बाद"

    def test_format_relative_future(self):

        result = self.locale._format_relative("एक घंटा", "hour", -1)
        assert result == "एक घंटा पहले"


class TestCzechLocale:
    @classmethod
    def setup_class(cls):
        cls.locale = locales.CzechLocale()

    def test_format_timeframe(self):

        assert self.locale._format_timeframe("hours", 2) == "2 hodiny"
        assert self.locale._format_timeframe("hours", 5) == "5 hodin"
        assert self.locale._format_timeframe("hour", 0) == "0 hodin"
        assert self.locale._format_timeframe("hours", -2) == "2 hodinami"
        assert self.locale._format_timeframe("hours", -5) == "5 hodinami"
        assert self.locale._format_timeframe("now", 0) == "Teď"

    def test_format_relative_now(self):

        result = self.locale._format_relative("Teď", "now", 0)
        assert result == "Teď"

    def test_format_relative_future(self):

        result = self.locale._format_relative("hodinu", "hour", 1)
        assert result == "Za hodinu"

    def test_format_relative_past(self):

        result = self.locale._format_relative("hodinou", "hour", -1)
        assert result == "Před hodinou"


class TestSlovakLocale:
    @classmethod
    def setup_class(cls):
        cls.locale = locales.SlovakLocale()

    def test_format_timeframe(self):

        assert self.locale._format_timeframe("hours", 2) == "2 hodiny"
        assert self.locale._format_timeframe("hours", 5) == "5 hodín"
        assert self.locale._format_timeframe("hour", 0) == "0 hodín"
        assert self.locale._format_timeframe("hours", -2) == "2 hodinami"
        assert self.locale._format_timeframe("hours", -5) == "5 hodinami"
        assert self.locale._format_timeframe("now", 0) == "Teraz"

    def test_format_relative_now(self):

        result = self.locale._format_relative("Teraz", "now", 0)
        assert result == "Teraz"

    def test_format_relative_future(self):

        result = self.locale._format_relative("hodinu", "hour", 1)
        assert result == "O hodinu"

    def test_format_relative_past(self):

        result = self.locale._format_relative("hodinou", "hour", -1)
        assert result == "Pred hodinou"


class TestBulgarianLocale:
    def test_plurals2(self):

        locale = locales.BulgarianLocale()

        assert locale._format_timeframe("hours", 0) == "0 часа"
        assert locale._format_timeframe("hours", 1) == "1 час"
        assert locale._format_timeframe("hours", 2) == "2 часа"
        assert locale._format_timeframe("hours", 4) == "4 часа"
        assert locale._format_timeframe("hours", 5) == "5 часа"
        assert locale._format_timeframe("hours", 21) == "21 час"
        assert locale._format_timeframe("hours", 22) == "22 часа"
        assert locale._format_timeframe("hours", 25) == "25 часа"

        # feminine grammatical gender should be tested separately
        assert locale._format_timeframe("minutes", 0) == "0 минути"
        assert locale._format_timeframe("minutes", 1) == "1 минута"
        assert locale._format_timeframe("minutes", 2) == "2 минути"
        assert locale._format_timeframe("minutes", 4) == "4 минути"
        assert locale._format_timeframe("minutes", 5) == "5 минути"
        assert locale._format_timeframe("minutes", 21) == "21 минута"
        assert locale._format_timeframe("minutes", 22) == "22 минути"
        assert locale._format_timeframe("minutes", 25) == "25 минути"


class TestMacedonianLocale:
    def test_plurals_mk(self):

        locale = locales.MacedonianLocale()

        # time
        assert locale._format_relative("сега", "now", 0) == "сега"

        # Hours
        assert locale._format_timeframe("hours", 0) == "0 саати"
        assert locale._format_timeframe("hours", 1) == "1 саат"
        assert locale._format_timeframe("hours", 2) == "2 саати"
        assert locale._format_timeframe("hours", 4) == "4 саати"
        assert locale._format_timeframe("hours", 5) == "5 саати"
        assert locale._format_timeframe("hours", 21) == "21 саат"
        assert locale._format_timeframe("hours", 22) == "22 саати"
        assert locale._format_timeframe("hours", 25) == "25 саати"

        # Minutes
        assert locale._format_timeframe("minutes", 0) == "0 минути"
        assert locale._format_timeframe("minutes", 1) == "1 минута"
        assert locale._format_timeframe("minutes", 2) == "2 минути"
        assert locale._format_timeframe("minutes", 4) == "4 минути"
        assert locale._format_timeframe("minutes", 5) == "5 минути"
        assert locale._format_timeframe("minutes", 21) == "21 минута"
        assert locale._format_timeframe("minutes", 22) == "22 минути"
        assert locale._format_timeframe("minutes", 25) == "25 минути"


class TestHebrewLocale:
    def test_couple_of_timeframe(self):
        locale = locales.HebrewLocale()

        assert locale._format_timeframe("hours", 2) == "שעתיים"
        assert locale._format_timeframe("months", 2) == "חודשיים"
        assert locale._format_timeframe("days", 2) == "יומיים"
        assert locale._format_timeframe("years", 2) == "שנתיים"

        assert locale._format_timeframe("hours", 3) == "3 שעות"
        assert locale._format_timeframe("months", 4) == "4 חודשים"
        assert locale._format_timeframe("days", 3) == "3 ימים"
        assert locale._format_timeframe("years", 5) == "5 שנים"


class TestMarathiLocale:
    @classmethod
    def setup_class(cls):
        cls.locale = locales.MarathiLocale()

    def test_dateCoreFunctionality(self):
        dt = arrow.Arrow(2015, 4, 11, 17, 30, 00)
        assert self.locale.month_name(dt.month) == "एप्रिल"
        assert self.locale.month_abbreviation(dt.month) == "एप्रि"
        assert self.locale.day_name(dt.isoweekday()) == "शनिवार"
        assert self.locale.day_abbreviation(dt.isoweekday()) == "शनि"

    def test_format_timeframe(self):
        assert self.locale._format_timeframe("hours", 2) == "2 तास"
        assert self.locale._format_timeframe("hour", 0) == "एक तास"

    def test_format_relative_now(self):
        result = self.locale._format_relative("सद्य", "now", 0)
        assert result == "सद्य"

    def test_format_relative_past(self):
        result = self.locale._format_relative("एक तास", "hour", 1)
        assert result == "एक तास नंतर"

    def test_format_relative_future(self):
        result = self.locale._format_relative("एक तास", "hour", -1)
        assert result == "एक तास आधी"

    # Not currently implemented
    def test_ordinal_number(self):
        assert self.locale.ordinal_number(1) == "1"


class TestFinnishLocale:
    @classmethod
    def setup_class(cls):
        cls.locale = locales.FinnishLocale()

    def test_format_timeframe(self):
        assert self.locale._format_timeframe("hours", 2) == ("2 tuntia", "2 tunnin")
        assert self.locale._format_timeframe("hour", 0) == ("tunti", "tunnin")

    def test_format_relative_now(self):
        result = self.locale._format_relative(["juuri nyt", "juuri nyt"], "now", 0)
        assert result == "juuri nyt"

    def test_format_relative_past(self):
        result = self.locale._format_relative(["tunti", "tunnin"], "hour", 1)
        assert result == "tunnin kuluttua"

    def test_format_relative_future(self):
        result = self.locale._format_relative(["tunti", "tunnin"], "hour", -1)
        assert result == "tunti sitten"

    def test_ordinal_number(self):
        assert self.locale.ordinal_number(1) == "1."


class TestGermanLocale:
    @classmethod
    def setup_class(cls):
        cls.locale = locales.GermanLocale()

    def test_ordinal_number(self):
        assert self.locale.ordinal_number(1) == "1."

    def test_define(self):
        assert self.locale.describe("minute", only_distance=True) == "eine Minute"
        assert self.locale.describe("minute", only_distance=False) == "in einer Minute"
        assert self.locale.describe("hour", only_distance=True) == "eine Stunde"
        assert self.locale.describe("hour", only_distance=False) == "in einer Stunde"
        assert self.locale.describe("day", only_distance=True) == "ein Tag"
        assert self.locale.describe("day", only_distance=False) == "in einem Tag"
        assert self.locale.describe("month", only_distance=True) == "ein Monat"
        assert self.locale.describe("month", only_distance=False) == "in einem Monat"
        assert self.locale.describe("year", only_distance=True) == "ein Jahr"
        assert self.locale.describe("year", only_distance=False) == "in einem Jahr"


class TestHungarianLocale:
    @classmethod
    def setup_class(cls):
        cls.locale = locales.HungarianLocale()

    def test_format_timeframe(self):
        assert self.locale._format_timeframe("hours", 2) == "2 óra"
        assert self.locale._format_timeframe("hour", 0) == "egy órával"
        assert self.locale._format_timeframe("hours", -2) == "2 órával"
        assert self.locale._format_timeframe("now", 0) == "éppen most"


class TestEsperantoLocale:
    @classmethod
    def setup_class(cls):
        cls.locale = locales.EsperantoLocale()

    def test_format_timeframe(self):
        assert self.locale._format_timeframe("hours", 2) == "2 horoj"
        assert self.locale._format_timeframe("hour", 0) == "un horo"
        assert self.locale._format_timeframe("hours", -2) == "2 horoj"
        assert self.locale._format_timeframe("now", 0) == "nun"

    def test_ordinal_number(self):
        assert self.locale.ordinal_number(1) == "1a"


class TestThaiLocale:
    @classmethod
    def setup_class(cls):
        cls.locale = locales.ThaiLocale()

    def test_year_full(self):
        assert self.locale.year_full(2015) == "2558"

    def test_year_abbreviation(self):
        assert self.locale.year_abbreviation(2015) == "58"

    def test_format_relative_now(self):
        result = self.locale._format_relative("ขณะนี้", "now", 0)
        assert result == "ขณะนี้"

    def test_format_relative_past(self):
        result = self.locale._format_relative("1 ชั่วโมง", "hour", 1)
        assert result == "ในอีก 1 ชั่วโมง"
        result = self.locale._format_relative("{0} ชั่วโมง", "hours", 2)
        assert result == "ในอีก {0} ชั่วโมง"
        result = self.locale._format_relative("ไม่กี่วินาที", "seconds", 42)
        assert result == "ในอีกไม่กี่วินาที"

    def test_format_relative_future(self):
        result = self.locale._format_relative("1 ชั่วโมง", "hour", -1)
        assert result == "1 ชั่วโมง ที่ผ่านมา"


class TestBengaliLocale:
    @classmethod
    def setup_class(cls):
        cls.locale = locales.BengaliLocale()

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
        assert result0 == "0তম"
        assert result1 == "1ম"
        assert result3 == "3য়"
        assert result4 == "4র্থ"
        assert result5 == "5ম"
        assert result6 == "6ষ্ঠ"
        assert result10 == "10ম"
        assert result11 == "11তম"
        assert result42 == "42তম"
        assert self.locale._ordinal_number(-1) is None


class TestSwissLocale:
    @classmethod
    def setup_class(cls):
        cls.locale = locales.SwissLocale()

    def test_ordinal_number(self):
        dt = arrow.Arrow(2015, 4, 11, 17, 30, 00)

        assert self.locale._format_timeframe("minute", 1) == "einer Minute"
        assert self.locale._format_timeframe("hour", 1) == "einer Stunde"
        assert self.locale.day_abbreviation(dt.isoweekday()) == "Sa"


class TestRomanianLocale:
    @classmethod
    def setup_class(cls):
        cls.locale = locales.RomanianLocale()

    def test_timeframes(self):

        assert self.locale._format_timeframe("hours", 2) == "2 ore"
        assert self.locale._format_timeframe("months", 2) == "2 luni"

        assert self.locale._format_timeframe("days", 2) == "2 zile"
        assert self.locale._format_timeframe("years", 2) == "2 ani"

        assert self.locale._format_timeframe("hours", 3) == "3 ore"
        assert self.locale._format_timeframe("months", 4) == "4 luni"
        assert self.locale._format_timeframe("days", 3) == "3 zile"
        assert self.locale._format_timeframe("years", 5) == "5 ani"

    def test_relative_timeframes(self):
        assert self.locale._format_relative("acum", "now", 0) == "acum"
        assert self.locale._format_relative("o oră", "hour", 1) == "peste o oră"
        assert self.locale._format_relative("o oră", "hour", -1) == "o oră în urmă"
        assert self.locale._format_relative("un minut", "minute", 1) == "peste un minut"
        assert (
            self.locale._format_relative("un minut", "minute", -1) == "un minut în urmă"
        )
        assert (
            self.locale._format_relative("câteva secunde", "seconds", -1)
            == "câteva secunde în urmă"
        )
        assert (
            self.locale._format_relative("câteva secunde", "seconds", 1)
            == "peste câteva secunde"
        )
        assert self.locale._format_relative("o zi", "day", -1) == "o zi în urmă"
        assert self.locale._format_relative("o zi", "day", 1) == "peste o zi"


class TestArabicLocales:
    @classmethod
    def setup_class(cls):
        cls.locale = locales.ArabicLocale()

    def test_timeframes(self):

        # single
        assert self.locale._format_timeframe("minute", 1) == "دقيقة"
        assert self.locale._format_timeframe("hour", 1) == "ساعة"
        assert self.locale._format_timeframe("day", 1) == "يوم"
        assert self.locale._format_timeframe("month", 1) == "شهر"
        assert self.locale._format_timeframe("year", 1) == "سنة"

        # double
        assert self.locale._format_timeframe("minutes", 2) == "دقيقتين"
        assert self.locale._format_timeframe("hours", 2) == "ساعتين"
        assert self.locale._format_timeframe("days", 2) == "يومين"
        assert self.locale._format_timeframe("months", 2) == "شهرين"
        assert self.locale._format_timeframe("years", 2) == "سنتين"

        # up to ten
        assert self.locale._format_timeframe("minutes", 3) == "3 دقائق"
        assert self.locale._format_timeframe("hours", 4) == "4 ساعات"
        assert self.locale._format_timeframe("days", 5) == "5 أيام"
        assert self.locale._format_timeframe("months", 6) == "6 أشهر"
        assert self.locale._format_timeframe("years", 10) == "10 سنوات"

        # more than ten
        assert self.locale._format_timeframe("minutes", 11) == "11 دقيقة"
        assert self.locale._format_timeframe("hours", 19) == "19 ساعة"
        assert self.locale._format_timeframe("months", 24) == "24 شهر"
        assert self.locale._format_timeframe("days", 50) == "50 يوم"
        assert self.locale._format_timeframe("years", 115) == "115 سنة"


class TestNepaliLocale:
    @classmethod
    def setup_class(cls):
        cls.locale = locales.NepaliLocale()

    def test_format_timeframe(self):
        assert self.locale._format_timeframe("hours", 3) == "3 घण्टा"
        assert self.locale._format_timeframe("hour", 0) == "एक घण्टा"

    def test_format_relative_now(self):
        result = self.locale._format_relative("अहिले", "now", 0)
        assert result == "अहिले"

    def test_format_relative_future(self):
        result = self.locale._format_relative("एक घण्टा", "hour", 1)
        assert result == "एक घण्टा पछी"

    def test_format_relative_past(self):
        result = self.locale._format_relative("एक घण्टा", "hour", -1)
        assert result == "एक घण्टा पहिले"


class TestIndonesianLocale:
    @classmethod
    def setup_class(cls):
        cls.locale = locales.IndonesianLocale()

    def test_timeframes(self):
        assert self.locale._format_timeframe("hours", 2) == "2 jam"
        assert self.locale._format_timeframe("months", 2) == "2 bulan"

        assert self.locale._format_timeframe("days", 2) == "2 hari"
        assert self.locale._format_timeframe("years", 2) == "2 tahun"

        assert self.locale._format_timeframe("hours", 3) == "3 jam"
        assert self.locale._format_timeframe("months", 4) == "4 bulan"
        assert self.locale._format_timeframe("days", 3) == "3 hari"
        assert self.locale._format_timeframe("years", 5) == "5 tahun"

    def test_format_relative_now(self):
        assert self.locale._format_relative("baru saja", "now", 0) == "baru saja"

    def test_format_relative_past(self):
        assert self.locale._format_relative("1 jam", "hour", 1) == "dalam 1 jam"
        assert self.locale._format_relative("1 detik", "seconds", 1) == "dalam 1 detik"

    def test_format_relative_future(self):
        assert self.locale._format_relative("1 jam", "hour", -1) == "1 jam yang lalu"


class TestTagalogLocale:
    @classmethod
    def setup_class(cls):
        cls.locale = locales.TagalogLocale()

    def test_format_timeframe(self):

        assert self.locale._format_timeframe("minute", 1) == "isang minuto"
        assert self.locale._format_timeframe("hour", 1) == "isang oras"
        assert self.locale._format_timeframe("month", 1) == "isang buwan"
        assert self.locale._format_timeframe("year", 1) == "isang taon"

        assert self.locale._format_timeframe("seconds", 2) == "2 segundo"
        assert self.locale._format_timeframe("minutes", 3) == "3 minuto"
        assert self.locale._format_timeframe("hours", 4) == "4 oras"
        assert self.locale._format_timeframe("months", 5) == "5 buwan"
        assert self.locale._format_timeframe("years", 6) == "6 taon"

    def test_format_relative_now(self):
        assert self.locale._format_relative("ngayon lang", "now", 0) == "ngayon lang"

    def test_format_relative_past(self):
        assert self.locale._format_relative("2 oras", "hour", 2) == "2 oras mula ngayon"

    def test_format_relative_future(self):
        assert self.locale._format_relative("3 oras", "hour", -3) == "nakaraang 3 oras"

    def test_ordinal_number(self):
        assert self.locale.ordinal_number(0) == "ika-0"
        assert self.locale.ordinal_number(1) == "ika-1"
        assert self.locale.ordinal_number(2) == "ika-2"
        assert self.locale.ordinal_number(3) == "ika-3"
        assert self.locale.ordinal_number(10) == "ika-10"
        assert self.locale.ordinal_number(23) == "ika-23"
        assert self.locale.ordinal_number(100) == "ika-100"
        assert self.locale.ordinal_number(103) == "ika-103"
        assert self.locale.ordinal_number(114) == "ika-114"


class TestEstonianLocale:
    @classmethod
    def setup_class(cls):
        cls.locale = locales.EstonianLocale()

    def test_format_timeframe(self):
        assert self.locale._format_timeframe("now", 0) == "just nüüd"
        assert self.locale._format_timeframe("second", 1) == "ühe sekundi"
        assert self.locale._format_timeframe("seconds", 3) == "3 sekundi"
        assert self.locale._format_timeframe("seconds", 30) == "30 sekundi"
        assert self.locale._format_timeframe("minute", 1) == "ühe minuti"
        assert self.locale._format_timeframe("minutes", 4) == "4 minuti"
        assert self.locale._format_timeframe("minutes", 40) == "40 minuti"
        assert self.locale._format_timeframe("hour", 1) == "tunni aja"
        assert self.locale._format_timeframe("hours", 5) == "5 tunni"
        assert self.locale._format_timeframe("hours", 23) == "23 tunni"
        assert self.locale._format_timeframe("day", 1) == "ühe päeva"
        assert self.locale._format_timeframe("days", 6) == "6 päeva"
        assert self.locale._format_timeframe("days", 12) == "12 päeva"
        assert self.locale._format_timeframe("month", 1) == "ühe kuu"
        assert self.locale._format_timeframe("months", 7) == "7 kuu"
        assert self.locale._format_timeframe("months", 11) == "11 kuu"
        assert self.locale._format_timeframe("year", 1) == "ühe aasta"
        assert self.locale._format_timeframe("years", 8) == "8 aasta"
        assert self.locale._format_timeframe("years", 12) == "12 aasta"

        assert self.locale._format_timeframe("now", 0) == "just nüüd"
        assert self.locale._format_timeframe("second", -1) == "üks sekund"
        assert self.locale._format_timeframe("seconds", -9) == "9 sekundit"
        assert self.locale._format_timeframe("seconds", -12) == "12 sekundit"
        assert self.locale._format_timeframe("minute", -1) == "üks minut"
        assert self.locale._format_timeframe("minutes", -2) == "2 minutit"
        assert self.locale._format_timeframe("minutes", -10) == "10 minutit"
        assert self.locale._format_timeframe("hour", -1) == "tund aega"
        assert self.locale._format_timeframe("hours", -3) == "3 tundi"
        assert self.locale._format_timeframe("hours", -11) == "11 tundi"
        assert self.locale._format_timeframe("day", -1) == "üks päev"
        assert self.locale._format_timeframe("days", -2) == "2 päeva"
        assert self.locale._format_timeframe("days", -12) == "12 päeva"
        assert self.locale._format_timeframe("month", -1) == "üks kuu"
        assert self.locale._format_timeframe("months", -3) == "3 kuud"
        assert self.locale._format_timeframe("months", -13) == "13 kuud"
        assert self.locale._format_timeframe("year", -1) == "üks aasta"
        assert self.locale._format_timeframe("years", -4) == "4 aastat"
        assert self.locale._format_timeframe("years", -14) == "14 aastat"


class TestPortugueseLocale:
    @classmethod
    def setup_class(cls):
        cls.locale = locales.PortugueseLocale()

    def test_format_timeframe(self):
        assert self.locale._format_timeframe("now", 0) == "agora"
        assert self.locale._format_timeframe("second", 1) == "um segundo"
        assert self.locale._format_timeframe("seconds", 30) == "30 segundos"
        assert self.locale._format_timeframe("minute", 1) == "um minuto"
        assert self.locale._format_timeframe("minutes", 40) == "40 minutos"
        assert self.locale._format_timeframe("hour", 1) == "uma hora"
        assert self.locale._format_timeframe("hours", 23) == "23 horas"
        assert self.locale._format_timeframe("day", 1) == "um dia"
        assert self.locale._format_timeframe("days", 12) == "12 dias"
        assert self.locale._format_timeframe("month", 1) == "um mês"
        assert self.locale._format_timeframe("months", 11) == "11 meses"
        assert self.locale._format_timeframe("year", 1) == "um ano"
        assert self.locale._format_timeframe("years", 12) == "12 anos"


class TestBrazilianLocale:
    @classmethod
    def setup_class(cls):
        cls.locale = locales.BrazilianPortugueseLocale()

    def test_format_timeframe(self):
        assert self.locale._format_timeframe("now", 0) == "agora"
        assert self.locale._format_timeframe("second", 1) == "um segundo"
        assert self.locale._format_timeframe("seconds", 30) == "30 segundos"
        assert self.locale._format_timeframe("minute", 1) == "um minuto"
        assert self.locale._format_timeframe("minutes", 40) == "40 minutos"
        assert self.locale._format_timeframe("hour", 1) == "uma hora"
        assert self.locale._format_timeframe("hours", 23) == "23 horas"
        assert self.locale._format_timeframe("day", 1) == "um dia"
        assert self.locale._format_timeframe("days", 12) == "12 dias"
        assert self.locale._format_timeframe("month", 1) == "um mês"
        assert self.locale._format_timeframe("months", 11) == "11 meses"
        assert self.locale._format_timeframe("year", 1) == "um ano"
        assert self.locale._format_timeframe("years", 12) == "12 anos"


class TestHongKongLocale:
    @classmethod
    def setup_class(cls):
        cls.locale = locales.HongKongLocale()

    def test_format_timeframe(self):
        assert self.locale._format_timeframe("now", 0) == "剛才"
        assert self.locale._format_timeframe("second", 1) == "1秒"
        assert self.locale._format_timeframe("seconds", 30) == "30秒"
        assert self.locale._format_timeframe("minute", 1) == "1分鐘"
        assert self.locale._format_timeframe("minutes", 40) == "40分鐘"
        assert self.locale._format_timeframe("hour", 1) == "1小時"
        assert self.locale._format_timeframe("hours", 23) == "23小時"
        assert self.locale._format_timeframe("day", 1) == "1天"
        assert self.locale._format_timeframe("days", 12) == "12天"
        assert self.locale._format_timeframe("week", 1) == "1星期"
        assert self.locale._format_timeframe("weeks", 38) == "38星期"
        assert self.locale._format_timeframe("month", 1) == "1個月"
        assert self.locale._format_timeframe("months", 11) == "11個月"
        assert self.locale._format_timeframe("year", 1) == "1年"
        assert self.locale._format_timeframe("years", 12) == "12年"
