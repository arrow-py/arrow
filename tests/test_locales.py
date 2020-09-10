# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import pytest

from arrow import arrow, locales


@pytest.mark.usefixtures("lang_locales")
class TestLocaleValidation:
    """Validate locales to ensure that translations are valid and complete"""

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

    def test_get_locale_by_class_name(self, mocker):
        mock_locale_cls = mocker.Mock()
        mock_locale_obj = mock_locale_cls.return_value = mocker.Mock()

        globals_fn = mocker.Mock()
        globals_fn.return_value = {"NonExistentLocale": mock_locale_cls}

        with pytest.raises(ValueError):
            arrow.locales.get_locale_by_class_name("NonExistentLocale")

        mocker.patch.object(locales, "globals", globals_fn)
        result = arrow.locales.get_locale_by_class_name("NonExistentLocale")

        mock_locale_cls.assert_called_once_with()
        assert result == mock_locale_obj

    def test_locales(self):

        assert len(locales._locales) > 0


@pytest.mark.usefixtures("lang_locale")
class TestEnglishLocale:
    def test_describe(self):
        assert self.locale.describe("now", only_distance=True) == "instantly"
        assert self.locale.describe("now", only_distance=False) == "just now"

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


@pytest.mark.usefixtures("lang_locale")
class TestItalianLocale:
    def test_ordinal_number(self):
        assert self.locale.ordinal_number(1) == "1º"


@pytest.mark.usefixtures("lang_locale")
class TestSpanishLocale:
    def test_ordinal_number(self):
        assert self.locale.ordinal_number(1) == "1º"

    def test_format_timeframe(self):
        assert self.locale._format_timeframe("now", 0) == "ahora"
        assert self.locale._format_timeframe("seconds", 1) == "1 segundos"
        assert self.locale._format_timeframe("seconds", 3) == "3 segundos"
        assert self.locale._format_timeframe("seconds", 30) == "30 segundos"
        assert self.locale._format_timeframe("minute", 1) == "un minuto"
        assert self.locale._format_timeframe("minutes", 4) == "4 minutos"
        assert self.locale._format_timeframe("minutes", 40) == "40 minutos"
        assert self.locale._format_timeframe("hour", 1) == "una hora"
        assert self.locale._format_timeframe("hours", 5) == "5 horas"
        assert self.locale._format_timeframe("hours", 23) == "23 horas"
        assert self.locale._format_timeframe("day", 1) == "un día"
        assert self.locale._format_timeframe("days", 6) == "6 días"
        assert self.locale._format_timeframe("days", 12) == "12 días"
        assert self.locale._format_timeframe("week", 1) == "una semana"
        assert self.locale._format_timeframe("weeks", 2) == "2 semanas"
        assert self.locale._format_timeframe("weeks", 3) == "3 semanas"
        assert self.locale._format_timeframe("month", 1) == "un mes"
        assert self.locale._format_timeframe("months", 7) == "7 meses"
        assert self.locale._format_timeframe("months", 11) == "11 meses"
        assert self.locale._format_timeframe("year", 1) == "un año"
        assert self.locale._format_timeframe("years", 8) == "8 años"
        assert self.locale._format_timeframe("years", 12) == "12 años"

        assert self.locale._format_timeframe("now", 0) == "ahora"
        assert self.locale._format_timeframe("seconds", -1) == "1 segundos"
        assert self.locale._format_timeframe("seconds", -9) == "9 segundos"
        assert self.locale._format_timeframe("seconds", -12) == "12 segundos"
        assert self.locale._format_timeframe("minute", -1) == "un minuto"
        assert self.locale._format_timeframe("minutes", -2) == "2 minutos"
        assert self.locale._format_timeframe("minutes", -10) == "10 minutos"
        assert self.locale._format_timeframe("hour", -1) == "una hora"
        assert self.locale._format_timeframe("hours", -3) == "3 horas"
        assert self.locale._format_timeframe("hours", -11) == "11 horas"
        assert self.locale._format_timeframe("day", -1) == "un día"
        assert self.locale._format_timeframe("days", -2) == "2 días"
        assert self.locale._format_timeframe("days", -12) == "12 días"
        assert self.locale._format_timeframe("week", -1) == "una semana"
        assert self.locale._format_timeframe("weeks", -2) == "2 semanas"
        assert self.locale._format_timeframe("weeks", -3) == "3 semanas"
        assert self.locale._format_timeframe("month", -1) == "un mes"
        assert self.locale._format_timeframe("months", -3) == "3 meses"
        assert self.locale._format_timeframe("months", -13) == "13 meses"
        assert self.locale._format_timeframe("year", -1) == "un año"
        assert self.locale._format_timeframe("years", -4) == "4 años"
        assert self.locale._format_timeframe("years", -14) == "14 años"


@pytest.mark.usefixtures("lang_locale")
class TestFrenchLocale:
    def test_ordinal_number(self):
        assert self.locale.ordinal_number(1) == "1er"
        assert self.locale.ordinal_number(2) == "2e"

    def test_month_abbreviation(self):
        assert "juil" in self.locale.month_abbreviations


@pytest.mark.usefixtures("lang_locale")
class TestFrenchCanadianLocale:
    def test_month_abbreviation(self):
        assert "juill" in self.locale.month_abbreviations


@pytest.mark.usefixtures("lang_locale")
class TestRussianLocale:
    def test_plurals2(self):
        assert self.locale._format_timeframe("hours", 0) == "0 часов"
        assert self.locale._format_timeframe("hours", 1) == "1 час"
        assert self.locale._format_timeframe("hours", 2) == "2 часа"
        assert self.locale._format_timeframe("hours", 4) == "4 часа"
        assert self.locale._format_timeframe("hours", 5) == "5 часов"
        assert self.locale._format_timeframe("hours", 21) == "21 час"
        assert self.locale._format_timeframe("hours", 22) == "22 часа"
        assert self.locale._format_timeframe("hours", 25) == "25 часов"

        # feminine grammatical gender should be tested separately
        assert self.locale._format_timeframe("minutes", 0) == "0 минут"
        assert self.locale._format_timeframe("minutes", 1) == "1 минуту"
        assert self.locale._format_timeframe("minutes", 2) == "2 минуты"
        assert self.locale._format_timeframe("minutes", 4) == "4 минуты"
        assert self.locale._format_timeframe("minutes", 5) == "5 минут"
        assert self.locale._format_timeframe("minutes", 21) == "21 минуту"
        assert self.locale._format_timeframe("minutes", 22) == "22 минуты"
        assert self.locale._format_timeframe("minutes", 25) == "25 минут"


@pytest.mark.usefixtures("lang_locale")
class TestPolishLocale:
    def test_plurals(self):

        assert self.locale._format_timeframe("seconds", 0) == "0 sekund"
        assert self.locale._format_timeframe("second", 1) == "sekundę"
        assert self.locale._format_timeframe("seconds", 2) == "2 sekundy"
        assert self.locale._format_timeframe("seconds", 5) == "5 sekund"
        assert self.locale._format_timeframe("seconds", 21) == "21 sekund"
        assert self.locale._format_timeframe("seconds", 22) == "22 sekundy"
        assert self.locale._format_timeframe("seconds", 25) == "25 sekund"

        assert self.locale._format_timeframe("minutes", 0) == "0 minut"
        assert self.locale._format_timeframe("minute", 1) == "minutę"
        assert self.locale._format_timeframe("minutes", 2) == "2 minuty"
        assert self.locale._format_timeframe("minutes", 5) == "5 minut"
        assert self.locale._format_timeframe("minutes", 21) == "21 minut"
        assert self.locale._format_timeframe("minutes", 22) == "22 minuty"
        assert self.locale._format_timeframe("minutes", 25) == "25 minut"

        assert self.locale._format_timeframe("hours", 0) == "0 godzin"
        assert self.locale._format_timeframe("hour", 1) == "godzinę"
        assert self.locale._format_timeframe("hours", 2) == "2 godziny"
        assert self.locale._format_timeframe("hours", 5) == "5 godzin"
        assert self.locale._format_timeframe("hours", 21) == "21 godzin"
        assert self.locale._format_timeframe("hours", 22) == "22 godziny"
        assert self.locale._format_timeframe("hours", 25) == "25 godzin"

        assert self.locale._format_timeframe("weeks", 0) == "0 tygodni"
        assert self.locale._format_timeframe("week", 1) == "tydzień"
        assert self.locale._format_timeframe("weeks", 2) == "2 tygodnie"
        assert self.locale._format_timeframe("weeks", 5) == "5 tygodni"
        assert self.locale._format_timeframe("weeks", 21) == "21 tygodni"
        assert self.locale._format_timeframe("weeks", 22) == "22 tygodnie"
        assert self.locale._format_timeframe("weeks", 25) == "25 tygodni"

        assert self.locale._format_timeframe("months", 0) == "0 miesięcy"
        assert self.locale._format_timeframe("month", 1) == "miesiąc"
        assert self.locale._format_timeframe("months", 2) == "2 miesiące"
        assert self.locale._format_timeframe("months", 5) == "5 miesięcy"
        assert self.locale._format_timeframe("months", 21) == "21 miesięcy"
        assert self.locale._format_timeframe("months", 22) == "22 miesiące"
        assert self.locale._format_timeframe("months", 25) == "25 miesięcy"

        assert self.locale._format_timeframe("years", 0) == "0 lat"
        assert self.locale._format_timeframe("year", 1) == "rok"
        assert self.locale._format_timeframe("years", 2) == "2 lata"
        assert self.locale._format_timeframe("years", 5) == "5 lat"
        assert self.locale._format_timeframe("years", 21) == "21 lat"
        assert self.locale._format_timeframe("years", 22) == "22 lata"
        assert self.locale._format_timeframe("years", 25) == "25 lat"


@pytest.mark.usefixtures("lang_locale")
class TestIcelandicLocale:
    def test_format_timeframe(self):

        assert self.locale._format_timeframe("minute", -1) == "einni mínútu"
        assert self.locale._format_timeframe("minute", 1) == "eina mínútu"

        assert self.locale._format_timeframe("hours", -2) == "2 tímum"
        assert self.locale._format_timeframe("hours", 2) == "2 tíma"
        assert self.locale._format_timeframe("now", 0) == "rétt í þessu"


@pytest.mark.usefixtures("lang_locale")
class TestMalayalamLocale:
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


@pytest.mark.usefixtures("lang_locale")
class TestHindiLocale:
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


@pytest.mark.usefixtures("lang_locale")
class TestCzechLocale:
    def test_format_timeframe(self):

        assert self.locale._format_timeframe("hours", 2) == "2 hodiny"
        assert self.locale._format_timeframe("hours", 5) == "5 hodin"
        assert self.locale._format_timeframe("hour", 0) == "0 hodin"
        assert self.locale._format_timeframe("hours", -2) == "2 hodinami"
        assert self.locale._format_timeframe("hours", -5) == "5 hodinami"
        assert self.locale._format_timeframe("now", 0) == "Teď"

        assert self.locale._format_timeframe("weeks", 2) == "2 týdny"
        assert self.locale._format_timeframe("weeks", 5) == "5 týdnů"
        assert self.locale._format_timeframe("week", 0) == "0 týdnů"
        assert self.locale._format_timeframe("weeks", -2) == "2 týdny"
        assert self.locale._format_timeframe("weeks", -5) == "5 týdny"

    def test_format_relative_now(self):

        result = self.locale._format_relative("Teď", "now", 0)
        assert result == "Teď"

    def test_format_relative_future(self):

        result = self.locale._format_relative("hodinu", "hour", 1)
        assert result == "Za hodinu"

    def test_format_relative_past(self):

        result = self.locale._format_relative("hodinou", "hour", -1)
        assert result == "Před hodinou"


@pytest.mark.usefixtures("lang_locale")
class TestSlovakLocale:
    def test_format_timeframe(self):

        assert self.locale._format_timeframe("seconds", -5) == "5 sekundami"
        assert self.locale._format_timeframe("seconds", -2) == "2 sekundami"
        assert self.locale._format_timeframe("second", -1) == "sekundou"
        assert self.locale._format_timeframe("second", 0) == "0 sekúnd"
        assert self.locale._format_timeframe("second", 1) == "sekundu"
        assert self.locale._format_timeframe("seconds", 2) == "2 sekundy"
        assert self.locale._format_timeframe("seconds", 5) == "5 sekúnd"

        assert self.locale._format_timeframe("minutes", -5) == "5 minútami"
        assert self.locale._format_timeframe("minutes", -2) == "2 minútami"
        assert self.locale._format_timeframe("minute", -1) == "minútou"
        assert self.locale._format_timeframe("minute", 0) == "0 minút"
        assert self.locale._format_timeframe("minute", 1) == "minútu"
        assert self.locale._format_timeframe("minutes", 2) == "2 minúty"
        assert self.locale._format_timeframe("minutes", 5) == "5 minút"

        assert self.locale._format_timeframe("hours", -5) == "5 hodinami"
        assert self.locale._format_timeframe("hours", -2) == "2 hodinami"
        assert self.locale._format_timeframe("hour", -1) == "hodinou"
        assert self.locale._format_timeframe("hour", 0) == "0 hodín"
        assert self.locale._format_timeframe("hour", 1) == "hodinu"
        assert self.locale._format_timeframe("hours", 2) == "2 hodiny"
        assert self.locale._format_timeframe("hours", 5) == "5 hodín"

        assert self.locale._format_timeframe("days", -5) == "5 dňami"
        assert self.locale._format_timeframe("days", -2) == "2 dňami"
        assert self.locale._format_timeframe("day", -1) == "dňom"
        assert self.locale._format_timeframe("day", 0) == "0 dní"
        assert self.locale._format_timeframe("day", 1) == "deň"
        assert self.locale._format_timeframe("days", 2) == "2 dni"
        assert self.locale._format_timeframe("days", 5) == "5 dní"

        assert self.locale._format_timeframe("weeks", -5) == "5 týždňami"
        assert self.locale._format_timeframe("weeks", -2) == "2 týždňami"
        assert self.locale._format_timeframe("week", -1) == "týždňom"
        assert self.locale._format_timeframe("week", 0) == "0 týždňov"
        assert self.locale._format_timeframe("week", 1) == "týždeň"
        assert self.locale._format_timeframe("weeks", 2) == "2 týždne"
        assert self.locale._format_timeframe("weeks", 5) == "5 týždňov"

        assert self.locale._format_timeframe("months", -5) == "5 mesiacmi"
        assert self.locale._format_timeframe("months", -2) == "2 mesiacmi"
        assert self.locale._format_timeframe("month", -1) == "mesiacom"
        assert self.locale._format_timeframe("month", 0) == "0 mesiacov"
        assert self.locale._format_timeframe("month", 1) == "mesiac"
        assert self.locale._format_timeframe("months", 2) == "2 mesiace"
        assert self.locale._format_timeframe("months", 5) == "5 mesiacov"

        assert self.locale._format_timeframe("years", -5) == "5 rokmi"
        assert self.locale._format_timeframe("years", -2) == "2 rokmi"
        assert self.locale._format_timeframe("year", -1) == "rokom"
        assert self.locale._format_timeframe("year", 0) == "0 rokov"
        assert self.locale._format_timeframe("year", 1) == "rok"
        assert self.locale._format_timeframe("years", 2) == "2 roky"
        assert self.locale._format_timeframe("years", 5) == "5 rokov"

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


@pytest.mark.usefixtures("lang_locale")
class TestBulgarianLocale:
    def test_plurals2(self):
        assert self.locale._format_timeframe("hours", 0) == "0 часа"
        assert self.locale._format_timeframe("hours", 1) == "1 час"
        assert self.locale._format_timeframe("hours", 2) == "2 часа"
        assert self.locale._format_timeframe("hours", 4) == "4 часа"
        assert self.locale._format_timeframe("hours", 5) == "5 часа"
        assert self.locale._format_timeframe("hours", 21) == "21 час"
        assert self.locale._format_timeframe("hours", 22) == "22 часа"
        assert self.locale._format_timeframe("hours", 25) == "25 часа"

        # feminine grammatical gender should be tested separately
        assert self.locale._format_timeframe("minutes", 0) == "0 минути"
        assert self.locale._format_timeframe("minutes", 1) == "1 минута"
        assert self.locale._format_timeframe("minutes", 2) == "2 минути"
        assert self.locale._format_timeframe("minutes", 4) == "4 минути"
        assert self.locale._format_timeframe("minutes", 5) == "5 минути"
        assert self.locale._format_timeframe("minutes", 21) == "21 минута"
        assert self.locale._format_timeframe("minutes", 22) == "22 минути"
        assert self.locale._format_timeframe("minutes", 25) == "25 минути"


@pytest.mark.usefixtures("lang_locale")
class TestMacedonianLocale:
    def test_singles_mk(self):
        assert self.locale._format_timeframe("second", 1) == "една секунда"
        assert self.locale._format_timeframe("minute", 1) == "една минута"
        assert self.locale._format_timeframe("hour", 1) == "еден саат"
        assert self.locale._format_timeframe("day", 1) == "еден ден"
        assert self.locale._format_timeframe("week", 1) == "една недела"
        assert self.locale._format_timeframe("month", 1) == "еден месец"
        assert self.locale._format_timeframe("year", 1) == "една година"

    def test_meridians_mk(self):
        assert self.locale.meridian(7, "A") == "претпладне"
        assert self.locale.meridian(18, "A") == "попладне"
        assert self.locale.meridian(10, "a") == "дп"
        assert self.locale.meridian(22, "a") == "пп"

    def test_describe_mk(self):
        assert self.locale.describe("second", only_distance=True) == "една секунда"
        assert self.locale.describe("second", only_distance=False) == "за една секунда"
        assert self.locale.describe("minute", only_distance=True) == "една минута"
        assert self.locale.describe("minute", only_distance=False) == "за една минута"
        assert self.locale.describe("hour", only_distance=True) == "еден саат"
        assert self.locale.describe("hour", only_distance=False) == "за еден саат"
        assert self.locale.describe("day", only_distance=True) == "еден ден"
        assert self.locale.describe("day", only_distance=False) == "за еден ден"
        assert self.locale.describe("week", only_distance=True) == "една недела"
        assert self.locale.describe("week", only_distance=False) == "за една недела"
        assert self.locale.describe("month", only_distance=True) == "еден месец"
        assert self.locale.describe("month", only_distance=False) == "за еден месец"
        assert self.locale.describe("year", only_distance=True) == "една година"
        assert self.locale.describe("year", only_distance=False) == "за една година"

    def test_relative_mk(self):
        # time
        assert self.locale._format_relative("сега", "now", 0) == "сега"
        assert self.locale._format_relative("1 секунда", "seconds", 1) == "за 1 секунда"
        assert self.locale._format_relative("1 минута", "minutes", 1) == "за 1 минута"
        assert self.locale._format_relative("1 саат", "hours", 1) == "за 1 саат"
        assert self.locale._format_relative("1 ден", "days", 1) == "за 1 ден"
        assert self.locale._format_relative("1 недела", "weeks", 1) == "за 1 недела"
        assert self.locale._format_relative("1 месец", "months", 1) == "за 1 месец"
        assert self.locale._format_relative("1 година", "years", 1) == "за 1 година"
        assert (
            self.locale._format_relative("1 секунда", "seconds", -1) == "пред 1 секунда"
        )
        assert (
            self.locale._format_relative("1 минута", "minutes", -1) == "пред 1 минута"
        )
        assert self.locale._format_relative("1 саат", "hours", -1) == "пред 1 саат"
        assert self.locale._format_relative("1 ден", "days", -1) == "пред 1 ден"
        assert self.locale._format_relative("1 недела", "weeks", -1) == "пред 1 недела"
        assert self.locale._format_relative("1 месец", "months", -1) == "пред 1 месец"
        assert self.locale._format_relative("1 година", "years", -1) == "пред 1 година"

    def test_plurals_mk(self):
        # Seconds
        assert self.locale._format_timeframe("seconds", 0) == "0 секунди"
        assert self.locale._format_timeframe("seconds", 1) == "1 секунда"
        assert self.locale._format_timeframe("seconds", 2) == "2 секунди"
        assert self.locale._format_timeframe("seconds", 4) == "4 секунди"
        assert self.locale._format_timeframe("seconds", 5) == "5 секунди"
        assert self.locale._format_timeframe("seconds", 21) == "21 секунда"
        assert self.locale._format_timeframe("seconds", 22) == "22 секунди"
        assert self.locale._format_timeframe("seconds", 25) == "25 секунди"

        # Minutes
        assert self.locale._format_timeframe("minutes", 0) == "0 минути"
        assert self.locale._format_timeframe("minutes", 1) == "1 минута"
        assert self.locale._format_timeframe("minutes", 2) == "2 минути"
        assert self.locale._format_timeframe("minutes", 4) == "4 минути"
        assert self.locale._format_timeframe("minutes", 5) == "5 минути"
        assert self.locale._format_timeframe("minutes", 21) == "21 минута"
        assert self.locale._format_timeframe("minutes", 22) == "22 минути"
        assert self.locale._format_timeframe("minutes", 25) == "25 минути"

        # Hours
        assert self.locale._format_timeframe("hours", 0) == "0 саати"
        assert self.locale._format_timeframe("hours", 1) == "1 саат"
        assert self.locale._format_timeframe("hours", 2) == "2 саати"
        assert self.locale._format_timeframe("hours", 4) == "4 саати"
        assert self.locale._format_timeframe("hours", 5) == "5 саати"
        assert self.locale._format_timeframe("hours", 21) == "21 саат"
        assert self.locale._format_timeframe("hours", 22) == "22 саати"
        assert self.locale._format_timeframe("hours", 25) == "25 саати"

        # Days
        assert self.locale._format_timeframe("days", 0) == "0 дена"
        assert self.locale._format_timeframe("days", 1) == "1 ден"
        assert self.locale._format_timeframe("days", 2) == "2 дена"
        assert self.locale._format_timeframe("days", 3) == "3 дена"
        assert self.locale._format_timeframe("days", 21) == "21 ден"

        # Weeks
        assert self.locale._format_timeframe("weeks", 0) == "0 недели"
        assert self.locale._format_timeframe("weeks", 1) == "1 недела"
        assert self.locale._format_timeframe("weeks", 2) == "2 недели"
        assert self.locale._format_timeframe("weeks", 4) == "4 недели"
        assert self.locale._format_timeframe("weeks", 5) == "5 недели"
        assert self.locale._format_timeframe("weeks", 21) == "21 недела"
        assert self.locale._format_timeframe("weeks", 22) == "22 недели"
        assert self.locale._format_timeframe("weeks", 25) == "25 недели"

        # Months
        assert self.locale._format_timeframe("months", 0) == "0 месеци"
        assert self.locale._format_timeframe("months", 1) == "1 месец"
        assert self.locale._format_timeframe("months", 2) == "2 месеци"
        assert self.locale._format_timeframe("months", 4) == "4 месеци"
        assert self.locale._format_timeframe("months", 5) == "5 месеци"
        assert self.locale._format_timeframe("months", 21) == "21 месец"
        assert self.locale._format_timeframe("months", 22) == "22 месеци"
        assert self.locale._format_timeframe("months", 25) == "25 месеци"

        # Years
        assert self.locale._format_timeframe("years", 1) == "1 година"
        assert self.locale._format_timeframe("years", 2) == "2 години"
        assert self.locale._format_timeframe("years", 5) == "5 години"

    def test_multi_describe_mk(self):
        describe = self.locale.describe_multi

        fulltest = [("years", 5), ("weeks", 1), ("hours", 1), ("minutes", 6)]
        assert describe(fulltest) == "за 5 години 1 недела 1 саат 6 минути"
        seconds4000_0days = [("days", 0), ("hours", 1), ("minutes", 6)]
        assert describe(seconds4000_0days) == "за 0 дена 1 саат 6 минути"
        seconds4000 = [("hours", 1), ("minutes", 6)]
        assert describe(seconds4000) == "за 1 саат 6 минути"
        assert describe(seconds4000, only_distance=True) == "1 саат 6 минути"
        seconds3700 = [("hours", 1), ("minutes", 1)]
        assert describe(seconds3700) == "за 1 саат 1 минута"
        seconds300_0hours = [("hours", 0), ("minutes", 5)]
        assert describe(seconds300_0hours) == "за 0 саати 5 минути"
        seconds300 = [("minutes", 5)]
        assert describe(seconds300) == "за 5 минути"
        seconds60 = [("minutes", 1)]
        assert describe(seconds60) == "за 1 минута"
        assert describe(seconds60, only_distance=True) == "1 минута"
        seconds60 = [("seconds", 1)]
        assert describe(seconds60) == "за 1 секунда"
        assert describe(seconds60, only_distance=True) == "1 секунда"


@pytest.mark.usefixtures("time_2013_01_01")
@pytest.mark.usefixtures("lang_locale")
class TestHebrewLocale:
    def test_couple_of_timeframe(self):
        assert self.locale._format_timeframe("days", 1) == "יום"
        assert self.locale._format_timeframe("days", 2) == "יומיים"
        assert self.locale._format_timeframe("days", 3) == "3 ימים"

        assert self.locale._format_timeframe("hours", 1) == "שעה"
        assert self.locale._format_timeframe("hours", 2) == "שעתיים"
        assert self.locale._format_timeframe("hours", 3) == "3 שעות"

        assert self.locale._format_timeframe("week", 1) == "שבוע"
        assert self.locale._format_timeframe("weeks", 2) == "שבועיים"
        assert self.locale._format_timeframe("weeks", 3) == "3 שבועות"

        assert self.locale._format_timeframe("months", 1) == "חודש"
        assert self.locale._format_timeframe("months", 2) == "חודשיים"
        assert self.locale._format_timeframe("months", 4) == "4 חודשים"

        assert self.locale._format_timeframe("years", 1) == "שנה"
        assert self.locale._format_timeframe("years", 2) == "שנתיים"
        assert self.locale._format_timeframe("years", 5) == "5 שנים"

    def test_describe_multi(self):
        describe = self.locale.describe_multi

        fulltest = [("years", 5), ("weeks", 1), ("hours", 1), ("minutes", 6)]
        assert describe(fulltest) == "בעוד 5 שנים, שבוע, שעה ו־6 דקות"
        seconds4000_0days = [("days", 0), ("hours", 1), ("minutes", 6)]
        assert describe(seconds4000_0days) == "בעוד 0 ימים, שעה ו־6 דקות"
        seconds4000 = [("hours", 1), ("minutes", 6)]
        assert describe(seconds4000) == "בעוד שעה ו־6 דקות"
        assert describe(seconds4000, only_distance=True) == "שעה ו־6 דקות"
        seconds3700 = [("hours", 1), ("minutes", 1)]
        assert describe(seconds3700) == "בעוד שעה ודקה"
        seconds300_0hours = [("hours", 0), ("minutes", 5)]
        assert describe(seconds300_0hours) == "בעוד 0 שעות ו־5 דקות"
        seconds300 = [("minutes", 5)]
        assert describe(seconds300) == "בעוד 5 דקות"
        seconds60 = [("minutes", 1)]
        assert describe(seconds60) == "בעוד דקה"
        assert describe(seconds60, only_distance=True) == "דקה"


@pytest.mark.usefixtures("lang_locale")
class TestMarathiLocale:
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


@pytest.mark.usefixtures("lang_locale")
class TestFinnishLocale:
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


@pytest.mark.usefixtures("lang_locale")
class TestGermanLocale:
    def test_ordinal_number(self):
        assert self.locale.ordinal_number(1) == "1."

    def test_define(self):
        assert self.locale.describe("minute", only_distance=True) == "eine Minute"
        assert self.locale.describe("minute", only_distance=False) == "in einer Minute"
        assert self.locale.describe("hour", only_distance=True) == "eine Stunde"
        assert self.locale.describe("hour", only_distance=False) == "in einer Stunde"
        assert self.locale.describe("day", only_distance=True) == "ein Tag"
        assert self.locale.describe("day", only_distance=False) == "in einem Tag"
        assert self.locale.describe("week", only_distance=True) == "eine Woche"
        assert self.locale.describe("week", only_distance=False) == "in einer Woche"
        assert self.locale.describe("month", only_distance=True) == "ein Monat"
        assert self.locale.describe("month", only_distance=False) == "in einem Monat"
        assert self.locale.describe("year", only_distance=True) == "ein Jahr"
        assert self.locale.describe("year", only_distance=False) == "in einem Jahr"

    def test_weekday(self):
        dt = arrow.Arrow(2015, 4, 11, 17, 30, 00)
        assert self.locale.day_name(dt.isoweekday()) == "Samstag"
        assert self.locale.day_abbreviation(dt.isoweekday()) == "Sa"


@pytest.mark.usefixtures("lang_locale")
class TestHungarianLocale:
    def test_format_timeframe(self):
        assert self.locale._format_timeframe("hours", 2) == "2 óra"
        assert self.locale._format_timeframe("hour", 0) == "egy órával"
        assert self.locale._format_timeframe("hours", -2) == "2 órával"
        assert self.locale._format_timeframe("now", 0) == "éppen most"


@pytest.mark.usefixtures("lang_locale")
class TestEsperantoLocale:
    def test_format_timeframe(self):
        assert self.locale._format_timeframe("hours", 2) == "2 horoj"
        assert self.locale._format_timeframe("hour", 0) == "un horo"
        assert self.locale._format_timeframe("hours", -2) == "2 horoj"
        assert self.locale._format_timeframe("now", 0) == "nun"

    def test_ordinal_number(self):
        assert self.locale.ordinal_number(1) == "1a"


@pytest.mark.usefixtures("lang_locale")
class TestThaiLocale:
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


@pytest.mark.usefixtures("lang_locale")
class TestBengaliLocale:
    def test_ordinal_number(self):
        assert self.locale._ordinal_number(0) == "0তম"
        assert self.locale._ordinal_number(1) == "1ম"
        assert self.locale._ordinal_number(3) == "3য়"
        assert self.locale._ordinal_number(4) == "4র্থ"
        assert self.locale._ordinal_number(5) == "5ম"
        assert self.locale._ordinal_number(6) == "6ষ্ঠ"
        assert self.locale._ordinal_number(10) == "10ম"
        assert self.locale._ordinal_number(11) == "11তম"
        assert self.locale._ordinal_number(42) == "42তম"
        assert self.locale._ordinal_number(-1) is None


@pytest.mark.usefixtures("lang_locale")
class TestRomanianLocale:
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


@pytest.mark.usefixtures("lang_locale")
class TestArabicLocale:
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


@pytest.mark.usefixtures("lang_locale")
class TestNepaliLocale:
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


@pytest.mark.usefixtures("lang_locale")
class TestIndonesianLocale:
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


@pytest.mark.usefixtures("lang_locale")
class TestTagalogLocale:
    def test_singles_tl(self):
        assert self.locale._format_timeframe("second", 1) == "isang segundo"
        assert self.locale._format_timeframe("minute", 1) == "isang minuto"
        assert self.locale._format_timeframe("hour", 1) == "isang oras"
        assert self.locale._format_timeframe("day", 1) == "isang araw"
        assert self.locale._format_timeframe("week", 1) == "isang linggo"
        assert self.locale._format_timeframe("month", 1) == "isang buwan"
        assert self.locale._format_timeframe("year", 1) == "isang taon"

    def test_meridians_tl(self):
        assert self.locale.meridian(7, "A") == "ng umaga"
        assert self.locale.meridian(18, "A") == "ng hapon"
        assert self.locale.meridian(10, "a") == "nu"
        assert self.locale.meridian(22, "a") == "nh"

    def test_describe_tl(self):
        assert self.locale.describe("second", only_distance=True) == "isang segundo"
        assert (
            self.locale.describe("second", only_distance=False)
            == "isang segundo mula ngayon"
        )
        assert self.locale.describe("minute", only_distance=True) == "isang minuto"
        assert (
            self.locale.describe("minute", only_distance=False)
            == "isang minuto mula ngayon"
        )
        assert self.locale.describe("hour", only_distance=True) == "isang oras"
        assert (
            self.locale.describe("hour", only_distance=False)
            == "isang oras mula ngayon"
        )
        assert self.locale.describe("day", only_distance=True) == "isang araw"
        assert (
            self.locale.describe("day", only_distance=False) == "isang araw mula ngayon"
        )
        assert self.locale.describe("week", only_distance=True) == "isang linggo"
        assert (
            self.locale.describe("week", only_distance=False)
            == "isang linggo mula ngayon"
        )
        assert self.locale.describe("month", only_distance=True) == "isang buwan"
        assert (
            self.locale.describe("month", only_distance=False)
            == "isang buwan mula ngayon"
        )
        assert self.locale.describe("year", only_distance=True) == "isang taon"
        assert (
            self.locale.describe("year", only_distance=False)
            == "isang taon mula ngayon"
        )

    def test_relative_tl(self):
        # time
        assert self.locale._format_relative("ngayon", "now", 0) == "ngayon"
        assert (
            self.locale._format_relative("1 segundo", "seconds", 1)
            == "1 segundo mula ngayon"
        )
        assert (
            self.locale._format_relative("1 minuto", "minutes", 1)
            == "1 minuto mula ngayon"
        )
        assert (
            self.locale._format_relative("1 oras", "hours", 1) == "1 oras mula ngayon"
        )
        assert self.locale._format_relative("1 araw", "days", 1) == "1 araw mula ngayon"
        assert (
            self.locale._format_relative("1 linggo", "weeks", 1)
            == "1 linggo mula ngayon"
        )
        assert (
            self.locale._format_relative("1 buwan", "months", 1)
            == "1 buwan mula ngayon"
        )
        assert (
            self.locale._format_relative("1 taon", "years", 1) == "1 taon mula ngayon"
        )
        assert (
            self.locale._format_relative("1 segundo", "seconds", -1)
            == "nakaraang 1 segundo"
        )
        assert (
            self.locale._format_relative("1 minuto", "minutes", -1)
            == "nakaraang 1 minuto"
        )
        assert self.locale._format_relative("1 oras", "hours", -1) == "nakaraang 1 oras"
        assert self.locale._format_relative("1 araw", "days", -1) == "nakaraang 1 araw"
        assert (
            self.locale._format_relative("1 linggo", "weeks", -1)
            == "nakaraang 1 linggo"
        )
        assert (
            self.locale._format_relative("1 buwan", "months", -1) == "nakaraang 1 buwan"
        )
        assert self.locale._format_relative("1 taon", "years", -1) == "nakaraang 1 taon"

    def test_plurals_tl(self):
        # Seconds
        assert self.locale._format_timeframe("seconds", 0) == "0 segundo"
        assert self.locale._format_timeframe("seconds", 1) == "1 segundo"
        assert self.locale._format_timeframe("seconds", 2) == "2 segundo"
        assert self.locale._format_timeframe("seconds", 4) == "4 segundo"
        assert self.locale._format_timeframe("seconds", 5) == "5 segundo"
        assert self.locale._format_timeframe("seconds", 21) == "21 segundo"
        assert self.locale._format_timeframe("seconds", 22) == "22 segundo"
        assert self.locale._format_timeframe("seconds", 25) == "25 segundo"

        # Minutes
        assert self.locale._format_timeframe("minutes", 0) == "0 minuto"
        assert self.locale._format_timeframe("minutes", 1) == "1 minuto"
        assert self.locale._format_timeframe("minutes", 2) == "2 minuto"
        assert self.locale._format_timeframe("minutes", 4) == "4 minuto"
        assert self.locale._format_timeframe("minutes", 5) == "5 minuto"
        assert self.locale._format_timeframe("minutes", 21) == "21 minuto"
        assert self.locale._format_timeframe("minutes", 22) == "22 minuto"
        assert self.locale._format_timeframe("minutes", 25) == "25 minuto"

        # Hours
        assert self.locale._format_timeframe("hours", 0) == "0 oras"
        assert self.locale._format_timeframe("hours", 1) == "1 oras"
        assert self.locale._format_timeframe("hours", 2) == "2 oras"
        assert self.locale._format_timeframe("hours", 4) == "4 oras"
        assert self.locale._format_timeframe("hours", 5) == "5 oras"
        assert self.locale._format_timeframe("hours", 21) == "21 oras"
        assert self.locale._format_timeframe("hours", 22) == "22 oras"
        assert self.locale._format_timeframe("hours", 25) == "25 oras"

        # Days
        assert self.locale._format_timeframe("days", 0) == "0 araw"
        assert self.locale._format_timeframe("days", 1) == "1 araw"
        assert self.locale._format_timeframe("days", 2) == "2 araw"
        assert self.locale._format_timeframe("days", 3) == "3 araw"
        assert self.locale._format_timeframe("days", 21) == "21 araw"

        # Weeks
        assert self.locale._format_timeframe("weeks", 0) == "0 linggo"
        assert self.locale._format_timeframe("weeks", 1) == "1 linggo"
        assert self.locale._format_timeframe("weeks", 2) == "2 linggo"
        assert self.locale._format_timeframe("weeks", 4) == "4 linggo"
        assert self.locale._format_timeframe("weeks", 5) == "5 linggo"
        assert self.locale._format_timeframe("weeks", 21) == "21 linggo"
        assert self.locale._format_timeframe("weeks", 22) == "22 linggo"
        assert self.locale._format_timeframe("weeks", 25) == "25 linggo"

        # Months
        assert self.locale._format_timeframe("months", 0) == "0 buwan"
        assert self.locale._format_timeframe("months", 1) == "1 buwan"
        assert self.locale._format_timeframe("months", 2) == "2 buwan"
        assert self.locale._format_timeframe("months", 4) == "4 buwan"
        assert self.locale._format_timeframe("months", 5) == "5 buwan"
        assert self.locale._format_timeframe("months", 21) == "21 buwan"
        assert self.locale._format_timeframe("months", 22) == "22 buwan"
        assert self.locale._format_timeframe("months", 25) == "25 buwan"

        # Years
        assert self.locale._format_timeframe("years", 1) == "1 taon"
        assert self.locale._format_timeframe("years", 2) == "2 taon"
        assert self.locale._format_timeframe("years", 5) == "5 taon"

    def test_multi_describe_tl(self):
        describe = self.locale.describe_multi

        fulltest = [("years", 5), ("weeks", 1), ("hours", 1), ("minutes", 6)]
        assert describe(fulltest) == "5 taon 1 linggo 1 oras 6 minuto mula ngayon"
        seconds4000_0days = [("days", 0), ("hours", 1), ("minutes", 6)]
        assert describe(seconds4000_0days) == "0 araw 1 oras 6 minuto mula ngayon"
        seconds4000 = [("hours", 1), ("minutes", 6)]
        assert describe(seconds4000) == "1 oras 6 minuto mula ngayon"
        assert describe(seconds4000, only_distance=True) == "1 oras 6 minuto"
        seconds3700 = [("hours", 1), ("minutes", 1)]
        assert describe(seconds3700) == "1 oras 1 minuto mula ngayon"
        seconds300_0hours = [("hours", 0), ("minutes", 5)]
        assert describe(seconds300_0hours) == "0 oras 5 minuto mula ngayon"
        seconds300 = [("minutes", 5)]
        assert describe(seconds300) == "5 minuto mula ngayon"
        seconds60 = [("minutes", 1)]
        assert describe(seconds60) == "1 minuto mula ngayon"
        assert describe(seconds60, only_distance=True) == "1 minuto"
        seconds60 = [("seconds", 1)]
        assert describe(seconds60) == "1 segundo mula ngayon"
        assert describe(seconds60, only_distance=True) == "1 segundo"

    def test_ordinal_number_tl(self):
        assert self.locale.ordinal_number(0) == "ika-0"
        assert self.locale.ordinal_number(1) == "ika-1"
        assert self.locale.ordinal_number(2) == "ika-2"
        assert self.locale.ordinal_number(3) == "ika-3"
        assert self.locale.ordinal_number(10) == "ika-10"
        assert self.locale.ordinal_number(23) == "ika-23"
        assert self.locale.ordinal_number(100) == "ika-100"
        assert self.locale.ordinal_number(103) == "ika-103"
        assert self.locale.ordinal_number(114) == "ika-114"


@pytest.mark.usefixtures("lang_locale")
class TestEstonianLocale:
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


@pytest.mark.usefixtures("lang_locale")
class TestPortugueseLocale:
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


@pytest.mark.usefixtures("lang_locale")
class TestBrazilianPortugueseLocale:
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
        assert self.locale._format_relative("uma hora", "hour", -1) == "faz uma hora"


@pytest.mark.usefixtures("lang_locale")
class TestHongKongLocale:
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


@pytest.mark.usefixtures("lang_locale")
class TestChineseTWLocale:
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
        assert self.locale._format_timeframe("week", 1) == "1週"
        assert self.locale._format_timeframe("weeks", 38) == "38週"
        assert self.locale._format_timeframe("month", 1) == "1個月"
        assert self.locale._format_timeframe("months", 11) == "11個月"
        assert self.locale._format_timeframe("year", 1) == "1年"
        assert self.locale._format_timeframe("years", 12) == "12年"


@pytest.mark.usefixtures("lang_locale")
class TestSwahiliLocale:
    def test_format_timeframe(self):
        assert self.locale._format_timeframe("now", 0) == "sasa hivi"
        assert self.locale._format_timeframe("second", 1) == "sekunde"
        assert self.locale._format_timeframe("seconds", 3) == "sekunde 3"
        assert self.locale._format_timeframe("seconds", 30) == "sekunde 30"
        assert self.locale._format_timeframe("minute", 1) == "dakika moja"
        assert self.locale._format_timeframe("minutes", 4) == "dakika 4"
        assert self.locale._format_timeframe("minutes", 40) == "dakika 40"
        assert self.locale._format_timeframe("hour", 1) == "saa moja"
        assert self.locale._format_timeframe("hours", 5) == "saa 5"
        assert self.locale._format_timeframe("hours", 23) == "saa 23"
        assert self.locale._format_timeframe("day", 1) == "siku moja"
        assert self.locale._format_timeframe("days", 6) == "siku 6"
        assert self.locale._format_timeframe("days", 12) == "siku 12"
        assert self.locale._format_timeframe("month", 1) == "mwezi moja"
        assert self.locale._format_timeframe("months", 7) == "miezi 7"
        assert self.locale._format_timeframe("week", 1) == "wiki moja"
        assert self.locale._format_timeframe("weeks", 2) == "wiki 2"
        assert self.locale._format_timeframe("months", 11) == "miezi 11"
        assert self.locale._format_timeframe("year", 1) == "mwaka moja"
        assert self.locale._format_timeframe("years", 8) == "miaka 8"
        assert self.locale._format_timeframe("years", 12) == "miaka 12"

    def test_format_relative_now(self):
        result = self.locale._format_relative("sasa hivi", "now", 0)
        assert result == "sasa hivi"

    def test_format_relative_past(self):
        result = self.locale._format_relative("saa moja", "hour", 1)
        assert result == "muda wa saa moja"

    def test_format_relative_future(self):
        result = self.locale._format_relative("saa moja", "hour", -1)
        assert result == "saa moja iliyopita"


@pytest.mark.usefixtures("lang_locale")
class TestKoreanLocale:
    def test_format_timeframe(self):
        assert self.locale._format_timeframe("now", 0) == "지금"
        assert self.locale._format_timeframe("second", 1) == "1초"
        assert self.locale._format_timeframe("seconds", 2) == "2초"
        assert self.locale._format_timeframe("minute", 1) == "1분"
        assert self.locale._format_timeframe("minutes", 2) == "2분"
        assert self.locale._format_timeframe("hour", 1) == "한시간"
        assert self.locale._format_timeframe("hours", 2) == "2시간"
        assert self.locale._format_timeframe("day", 1) == "하루"
        assert self.locale._format_timeframe("days", 2) == "2일"
        assert self.locale._format_timeframe("week", 1) == "1주"
        assert self.locale._format_timeframe("weeks", 2) == "2주"
        assert self.locale._format_timeframe("month", 1) == "한달"
        assert self.locale._format_timeframe("months", 2) == "2개월"
        assert self.locale._format_timeframe("year", 1) == "1년"
        assert self.locale._format_timeframe("years", 2) == "2년"

    def test_format_relative(self):
        assert self.locale._format_relative("지금", "now", 0) == "지금"

        assert self.locale._format_relative("1초", "second", 1) == "1초 후"
        assert self.locale._format_relative("2초", "seconds", 2) == "2초 후"
        assert self.locale._format_relative("1분", "minute", 1) == "1분 후"
        assert self.locale._format_relative("2분", "minutes", 2) == "2분 후"
        assert self.locale._format_relative("한시간", "hour", 1) == "한시간 후"
        assert self.locale._format_relative("2시간", "hours", 2) == "2시간 후"
        assert self.locale._format_relative("하루", "day", 1) == "내일"
        assert self.locale._format_relative("2일", "days", 2) == "모레"
        assert self.locale._format_relative("3일", "days", 3) == "글피"
        assert self.locale._format_relative("4일", "days", 4) == "그글피"
        assert self.locale._format_relative("5일", "days", 5) == "5일 후"
        assert self.locale._format_relative("1주", "week", 1) == "1주 후"
        assert self.locale._format_relative("2주", "weeks", 2) == "2주 후"
        assert self.locale._format_relative("한달", "month", 1) == "한달 후"
        assert self.locale._format_relative("2개월", "months", 2) == "2개월 후"
        assert self.locale._format_relative("1년", "year", 1) == "내년"
        assert self.locale._format_relative("2년", "years", 2) == "내후년"
        assert self.locale._format_relative("3년", "years", 3) == "3년 후"

        assert self.locale._format_relative("1초", "second", -1) == "1초 전"
        assert self.locale._format_relative("2초", "seconds", -2) == "2초 전"
        assert self.locale._format_relative("1분", "minute", -1) == "1분 전"
        assert self.locale._format_relative("2분", "minutes", -2) == "2분 전"
        assert self.locale._format_relative("한시간", "hour", -1) == "한시간 전"
        assert self.locale._format_relative("2시간", "hours", -2) == "2시간 전"
        assert self.locale._format_relative("하루", "day", -1) == "어제"
        assert self.locale._format_relative("2일", "days", -2) == "그제"
        assert self.locale._format_relative("3일", "days", -3) == "그끄제"
        assert self.locale._format_relative("4일", "days", -4) == "4일 전"
        assert self.locale._format_relative("1주", "week", -1) == "1주 전"
        assert self.locale._format_relative("2주", "weeks", -2) == "2주 전"
        assert self.locale._format_relative("한달", "month", -1) == "한달 전"
        assert self.locale._format_relative("2개월", "months", -2) == "2개월 전"
        assert self.locale._format_relative("1년", "year", -1) == "작년"
        assert self.locale._format_relative("2년", "years", -2) == "제작년"
        assert self.locale._format_relative("3년", "years", -3) == "3년 전"

    def test_ordinal_number(self):
        assert self.locale.ordinal_number(0) == "0번째"
        assert self.locale.ordinal_number(1) == "첫번째"
        assert self.locale.ordinal_number(2) == "두번째"
        assert self.locale.ordinal_number(3) == "세번째"
        assert self.locale.ordinal_number(4) == "네번째"
        assert self.locale.ordinal_number(5) == "다섯번째"
        assert self.locale.ordinal_number(6) == "여섯번째"
        assert self.locale.ordinal_number(7) == "일곱번째"
        assert self.locale.ordinal_number(8) == "여덟번째"
        assert self.locale.ordinal_number(9) == "아홉번째"
        assert self.locale.ordinal_number(10) == "열번째"
        assert self.locale.ordinal_number(11) == "11번째"
        assert self.locale.ordinal_number(12) == "12번째"
        assert self.locale.ordinal_number(100) == "100번째"
