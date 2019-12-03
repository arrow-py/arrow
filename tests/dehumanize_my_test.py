# -*- coding: utf-8 -*-
from datetime import date, datetime, timedelta

import arrow
from chai import Chai


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

        result = arw_1.dehumanize('2 days ago')
        result_1 = arw_0.dehumanize('in 1 days')

        self.assertEqual(result, arw_0)
        self.assertEqual(result_1, arw)

    def test_years(self):
        arw = arrow.Arrow(2014, 1, 1, 0, 0, 0)
        arw_1 = arrow.Arrow(2015, 1, 1, 0, 0, 0)
        arw_0 = arrow.Arrow(2013, 1, 1, 0, 0, 0)

        result = arw_1.dehumanize('2 years ago')
        result_1 = arw.dehumanize('in 1 years')

        self.assertEqual(result, arw_0)
        self.assertEqual(result_1, arw_1)

class LocaleTests(Chai):
    def setUp(self):
        super(LocaleTests, self).setUp()

        self.locale = locales.EnglishLocale()
    
    def test_delocale(self):
        self.assertEqual(self.locale.delocale("2 hours ago"), "hours", -2)
        self.assertEqual(self.locale.delocale("in 2 hours"), "hours", 2)
        self.assertEqual(self.locale.delocale("2 years ago"), "years", -2)
        self.assertEqual(self.locale.delocale("in 2 years"), "years", 2)
        self.assertEqual(self.locale.delocale("2 days ago"), "days", -2)
        self.assertEqual(self.locale.delocale("in 2 days"), "days", 2)
        self.assertEqual(self.locale.delocale("11 seconds ago"), "seconds", -11)
        self.assertEqual(self.locale.delocale("in 11 seconds"), "seconds", 11)
        self.assertEqual(self.locale.delocale("now"), "now", 0)

    