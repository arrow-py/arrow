# -*- coding: utf-8 -*-
from datetime import date, datetime, timedelta

from chai import Chai

import arrow
from arrow import locales

utc = arrow.utcnow()


def assertDtEqual(dt1, dt2, within=10):
    assertEqual(dt1.tzinfo, dt2.tzinfo)  # noqa: F821
    assertTrue(abs(util.total_seconds(dt1 - dt2)) < within)  # noqa: F821


class ArrowDehumanizeTestsWithLocale(Chai):
    def setUp(self):
        super(ArrowDehumanizeTestsWithLocale, self).setUp()

        self.datetime = datetime(2013, 1, 1)

    def test_now(self):

        arw = arrow.Arrow(2013, 1, 1, 0, 0, 0)

        result = arw.dehumanize()

        self.assertEqual(result, arw)

    def test_days(self):
        arw = arrow.Arrow(2013, 1, 2, 0, 0, 0)
        arw_1 = arrow.Arrow(2013, 1, 3, 0, 0, 0)
        arw_0 = arrow.Arrow(2013, 1, 1, 0, 0, 0)

        result = arw_1.dehumanize("2 days ago")
        result_1 = arw_0.dehumanize("in 1 days")

        self.assertEqual(result, arw_0)
        self.assertEqual(result_1, arw)

    def test_years(self):
        arw = arrow.Arrow(2014, 1, 1, 0, 0, 0)
        arw_1 = arrow.Arrow(2015, 1, 1, 0, 0, 0)
        arw_0 = arrow.Arrow(2013, 1, 1, 0, 0, 0)

        result = arw_1.dehumanize("2 years ago")
        result_1 = arw.dehumanize("in 1 years")

        self.assertEqual(result, arw_0)
        self.assertEqual(result_1, arw_1)


class LocaleTests(Chai):
    def setUp(self):
        super(LocaleTests, self).setUp()

        self.locale = locales.EnglishLocale()

    def test_delocale(self):
        k_hours, v_n2 = self.locale.delocale("2 hours ago")
        self.assertEqual(self.locale.delocale("2 hours ago"), (u"hours", -2))
        self.assertEqual(k_hours, "hours")
        self.assertEqual(v_n2, -2)

        k_hours, v_2 = self.locale.delocale("in 2 hours")
        self.assertEqual(self.locale.delocale("in 2 hours"), (u"hours", 2))
        self.assertEqual(self.locale.delocale("in an hours"), (u"hours", 1))
        self.assertEqual(k_hours, "hours")
        self.assertEqual(v_2, 2)

        k_years, v_n1 = self.locale.delocale("1 years ago")
        self.assertEqual(self.locale.delocale("1 years ago"), (u"years", -1))
        self.assertEqual(self.locale.delocale("a years ago"), (u"years", -1))
        self.assertEqual(k_years, "years")
        self.assertEqual(v_n1, -1)

        k_years, v_1 = self.locale.delocale("in 1 years")
        self.assertEqual(self.locale.delocale("in 1 years"), (u"years", 1))
        self.assertEqual(k_years, "years")
        self.assertEqual(v_1, 1)

        k_seconds, v_n11 = self.locale.delocale("11 seconds ago")
        self.assertEqual(self.locale.delocale("11 seconds ago"), (u"seconds", -11))
        self.assertEqual(k_seconds, "seconds")
        self.assertEqual(v_n11, -11)

        k_seconds, v_11 = self.locale.delocale("in 11 seconds")
        self.assertEqual(self.locale.delocale("in 11 seconds"), (u"seconds", 11))
        self.assertEqual(k_seconds, "seconds")
        self.assertEqual(v_11, 11)

        k_now, v_0 = self.locale.delocale("now")
        self.assertEqual(self.locale.delocale("now"), (u"now", 0))
        self.assertEqual(k_now, "now")
        self.assertEqual(v_0, 0)
