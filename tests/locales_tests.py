# -*- coding: utf-8 -*-

from chai import Chai

from arrow import locales


class LocaleTests(Chai):

    def test_format_humanize(self):

        with assertRaises(NotImplementedError):
            locales.Locale().format_humanize(1, 'hour', True)


class RussianLocalesTests(Chai):

    def test_plurals(self):

        plurals = ['матрешка', 'матрешки', 'матрешек']
        cases = {
            0: plurals[2],
            1: plurals[0],
            2: plurals[1],
            4: plurals[1],
            5: plurals[2],
            21: plurals[0],
            22: plurals[1],
            25: plurals[2],
        }

        rus = locales.get_locale_by_name('ru')

        for num, exp_pl in cases.items():
            assertEqual(rus._chose_plural(num, plurals), exp_pl)
