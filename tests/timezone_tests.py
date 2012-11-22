from datetime import datetime, timedelta, tzinfo
from dateutil import tz

import unittest
import arrow.timezone as timezone

class TimeZoneTests(unittest.TestCase):

    def setUp(self):

        self.time_zone = timezone.TimeZone('UTC', datetime.utcnow())
        self.datetime = datetime.utcnow()

    def assert_tzinfo_equal(self, tzinfo_1, tzinfo_2):

        dt = datetime.now()
        self.assertEqual(tzinfo_1.utcoffset(dt), tzinfo_2.utcoffset(dt))

    def test_str(self):
        self.assertEqual(self.time_zone.__str__(), '+00:00 (UTC)')
   
    def test_repr(self):
        self.assertEqual(self.time_zone.__repr__(), 'TimeZone(+00:00 (UTC))')

    def test_name(self):
        self.assertEqual(self.time_zone.name, 'UTC')

    def test_name_delta(self):

        time_zone = timezone.TimeZone(timedelta(hours=-1), datetime.utcnow())

        self.assertIsNone(time_zone.name)

    def test_utcoffset(self):
        self.assertEqual(self.time_zone.utcoffset, timedelta())

    def test_utc(self):
        self.assertTrue(self.time_zone.utc)

    def test_tzinfo(self):
        self.assertIsInstance(self.time_zone.tzinfo, tzinfo)

    def test_parse_str_olson(self):

        result = self.time_zone._parse('UTC')

        self.assert_tzinfo_equal(result, tz.tzutc())

    def test_parse_str_local(self):

        result = self.time_zone._parse('local')

        self.assert_tzinfo_equal(result, tz.tzlocal())

    def test_parse_str_iso(self):

        result = self.time_zone._parse('+01:02')

        self.assert_tzinfo_equal(result, tz.tzoffset(None, 3720))

        result = self.time_zone._parse('-01:02')

        self.assert_tzinfo_equal(result, tz.tzoffset(None, -3720))

    def test_parse_tzinfo_utc(self):

        tz_utc = tz.tzutc()

        result = self.time_zone._parse(tz_utc)

        self.assertEqual(result, tz_utc)

    def test_parse_timedelta(self):

        result = self.time_zone._parse(timedelta(minutes=-60))

        self.assert_tzinfo_equal(result, tz.tzoffset(None, -3600))

    def test_parse_none(self):

        with self.assertRaises(ValueError):
            self.time_zone._parse(None)