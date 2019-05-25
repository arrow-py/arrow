# -*- coding: utf-8 -*-
import time
from datetime import datetime

import pytz
from chai import Chai
from dateutil import tz as dateutil_tz

from arrow import formatter


class DateTimeFormatterFormatTokenTests(Chai):
    def setUp(self):
        super(DateTimeFormatterFormatTokenTests, self).setUp()

        self.formatter = formatter.DateTimeFormatter()

    def test_format(self):

        dt = datetime(2013, 2, 5, 12, 32, 51)

        result = self.formatter.format(dt, "MM-DD-YYYY hh:mm:ss a")

        self.assertEqual(result, "02-05-2013 12:32:51 pm")

    def test_year(self):

        dt = datetime(2013, 1, 1)
        self.assertEqual(self.formatter._format_token(dt, "YYYY"), "2013")
        self.assertEqual(self.formatter._format_token(dt, "YY"), "13")

    def test_month(self):

        dt = datetime(2013, 1, 1)
        self.assertEqual(self.formatter._format_token(dt, "MMMM"), "January")
        self.assertEqual(self.formatter._format_token(dt, "MMM"), "Jan")
        self.assertEqual(self.formatter._format_token(dt, "MM"), "01")
        self.assertEqual(self.formatter._format_token(dt, "M"), "1")

    def test_day(self):

        dt = datetime(2013, 2, 1)
        self.assertEqual(self.formatter._format_token(dt, "DDDD"), "032")
        self.assertEqual(self.formatter._format_token(dt, "DDD"), "32")
        self.assertEqual(self.formatter._format_token(dt, "DD"), "01")
        self.assertEqual(self.formatter._format_token(dt, "D"), "1")
        self.assertEqual(self.formatter._format_token(dt, "Do"), "1st")

        self.assertEqual(self.formatter._format_token(dt, "dddd"), "Friday")
        self.assertEqual(self.formatter._format_token(dt, "ddd"), "Fri")
        self.assertEqual(self.formatter._format_token(dt, "d"), "5")

    def test_hour(self):

        dt = datetime(2013, 1, 1, 2)
        self.assertEqual(self.formatter._format_token(dt, "HH"), "02")
        self.assertEqual(self.formatter._format_token(dt, "H"), "2")

        dt = datetime(2013, 1, 1, 13)
        self.assertEqual(self.formatter._format_token(dt, "HH"), "13")
        self.assertEqual(self.formatter._format_token(dt, "H"), "13")

        dt = datetime(2013, 1, 1, 2)
        self.assertEqual(self.formatter._format_token(dt, "hh"), "02")
        self.assertEqual(self.formatter._format_token(dt, "h"), "2")

        dt = datetime(2013, 1, 1, 13)
        self.assertEqual(self.formatter._format_token(dt, "hh"), "01")
        self.assertEqual(self.formatter._format_token(dt, "h"), "1")

        # test that 12-hour time converts to '12' at midnight
        dt = datetime(2013, 1, 1, 0)
        self.assertEqual(self.formatter._format_token(dt, "hh"), "12")
        self.assertEqual(self.formatter._format_token(dt, "h"), "12")

    def test_minute(self):

        dt = datetime(2013, 1, 1, 0, 1)
        self.assertEqual(self.formatter._format_token(dt, "mm"), "01")
        self.assertEqual(self.formatter._format_token(dt, "m"), "1")

    def test_second(self):

        dt = datetime(2013, 1, 1, 0, 0, 1)
        self.assertEqual(self.formatter._format_token(dt, "ss"), "01")
        self.assertEqual(self.formatter._format_token(dt, "s"), "1")

    def test_sub_second(self):

        dt = datetime(2013, 1, 1, 0, 0, 0, 123456)
        self.assertEqual(self.formatter._format_token(dt, "SSSSSS"), "123456")
        self.assertEqual(self.formatter._format_token(dt, "SSSSS"), "12345")
        self.assertEqual(self.formatter._format_token(dt, "SSSS"), "1234")
        self.assertEqual(self.formatter._format_token(dt, "SSS"), "123")
        self.assertEqual(self.formatter._format_token(dt, "SS"), "12")
        self.assertEqual(self.formatter._format_token(dt, "S"), "1")

        dt = datetime(2013, 1, 1, 0, 0, 0, 2000)
        self.assertEqual(self.formatter._format_token(dt, "SSSSSS"), "002000")
        self.assertEqual(self.formatter._format_token(dt, "SSSSS"), "00200")
        self.assertEqual(self.formatter._format_token(dt, "SSSS"), "0020")
        self.assertEqual(self.formatter._format_token(dt, "SSS"), "002")
        self.assertEqual(self.formatter._format_token(dt, "SS"), "00")
        self.assertEqual(self.formatter._format_token(dt, "S"), "0")

    def test_timestamp(self):

        timestamp = time.time()
        dt = datetime.utcfromtimestamp(timestamp)
        self.assertEqual(self.formatter._format_token(dt, "X"), str(int(timestamp)))

    def test_timezone(self):

        dt = datetime.utcnow().replace(tzinfo=dateutil_tz.gettz("US/Pacific"))

        result = self.formatter._format_token(dt, "ZZ")
        self.assertTrue(result == "-07:00" or result == "-08:00")

        result = self.formatter._format_token(dt, "Z")
        self.assertTrue(result == "-0700" or result == "-0800")

    def test_timezone_formatter(self):

        tz_map = {
            # 'BRST': 'America/Sao_Paulo', TODO investigate why this fails
            "CET": "Europe/Berlin",
            "JST": "Asia/Tokyo",
            "PST": "US/Pacific",
        }

        for abbreviation, full_name in tz_map.items():
            # This test will fail if we use "now" as date as soon as we change from/to DST
            dt = datetime(1986, 2, 14, tzinfo=pytz.timezone("UTC")).replace(
                tzinfo=dateutil_tz.gettz(full_name)
            )
            result = self.formatter._format_token(dt, "ZZZ")
            self.assertEqual(result, abbreviation)

    def test_am_pm(self):

        dt = datetime(2012, 1, 1, 11)
        self.assertEqual(self.formatter._format_token(dt, "a"), "am")
        self.assertEqual(self.formatter._format_token(dt, "A"), "AM")

        dt = datetime(2012, 1, 1, 13)
        self.assertEqual(self.formatter._format_token(dt, "a"), "pm")
        self.assertEqual(self.formatter._format_token(dt, "A"), "PM")

    def test_nonsense(self):
        dt = datetime(2012, 1, 1, 11)
        self.assertEqual(self.formatter._format_token(dt, None), None)
        self.assertEqual(self.formatter._format_token(dt, "NONSENSE"), None)
