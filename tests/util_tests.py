# -*- coding: utf-8 -*-
import time
from datetime import datetime

from chai import Chai
from dateutil import tz
from mock import patch

from arrow import util


class UtilTests(Chai):
    def test_is_timestamp(self):
        timestamp_float = time.time()
        timestamp_int = int(timestamp_float)

        self.assertTrue(util.is_timestamp(timestamp_int))
        self.assertTrue(util.is_timestamp(timestamp_float))
        self.assertTrue(util.is_timestamp(str(timestamp_int)))
        self.assertTrue(util.is_timestamp(str(timestamp_float)))

        self.assertFalse(util.is_timestamp(True))
        self.assertFalse(util.is_timestamp(False))

        class InvalidTimestamp:
            pass

        self.assertFalse(util.is_timestamp(InvalidTimestamp()))

        full_datetime = "2019-06-23T13:12:42"
        self.assertFalse(util.is_timestamp(full_datetime))

    def test_iso_gregorian(self):
        with self.assertRaises(ValueError):
            util.iso_to_gregorian(2013, 0, 5)

        with self.assertRaises(ValueError):
            util.iso_to_gregorian(2013, 8, 0)

    def test_windows_datetime_from_timestamp_positive(self):
        # positive timestamps should be tested because
        # datetime.fromtimestamp can be used as
        # the source of truth
        positive_timestamp = 1572204340.6460679

        result = util.windows_datetime_from_timestamp(positive_timestamp)
        expected = datetime.fromtimestamp(positive_timestamp).replace(
            tzinfo=tz.tzlocal()
        )
        self.assertEqual(result, expected)

        result = util.windows_datetime_from_timestamp(
            positive_timestamp, tz.gettz("EST")
        )
        expected = datetime.fromtimestamp(positive_timestamp, tz.gettz("EST")).replace(
            tzinfo=tz.gettz("EST")
        )
        self.assertEqual(result, expected)

    def test_windows_datetime_from_timestamp_negative(self):
        negative_timestamp = -1572204340.6460679
        result = util.windows_datetime_from_timestamp(negative_timestamp)
        # astimezone(tzlocal()) fails on Windows, so we need to
        # fake the local timezone by (1) fetching the local tzname
        # and (2) forming a tzinfo object from that tzname
        local_tz = tz.gettz(datetime.now(tz.tzlocal()).tzname())
        expected_dt = (
            datetime(1920, 3, 7, 4, 34, 19, 353932)
            .replace(tzinfo=tz.tzutc())
            .astimezone(local_tz)
            .replace(tzinfo=tz.tzlocal())
        )
        expected = expected_dt + expected_dt.dst()
        self.assertEqual(result, expected)

    def test_windows_datetime_from_timestamp_utc(self):
        timestamp = -1572204340.6460679
        result = util.windows_datetime_from_timestamp(timestamp, tz.tzutc())
        expected_dt = datetime(1920, 3, 7, 4, 34, 19, 353932).replace(tzinfo=tz.tzutc())
        expected = expected_dt + expected_dt.dst()
        self.assertEqual(result, expected)

    def test_safe_utcfromtimestamp(self):
        timestamp = 1572204340.6460679
        result = util.safe_utcfromtimestamp(timestamp).replace(tzinfo=tz.tzutc())
        expected = datetime.utcfromtimestamp(timestamp).replace(tzinfo=tz.tzutc())
        self.assertEqual(result, expected)

    def test_safe_fromtimestamp_default_tz(self):
        timestamp = 1572204340.6460679
        result = util.safe_fromtimestamp(timestamp).replace(tzinfo=tz.tzlocal())
        expected = datetime.fromtimestamp(timestamp).replace(tzinfo=tz.tzlocal())
        self.assertEqual(result, expected)

    def test_safe_fromtimestamp_paris_tz(self):
        timestamp = 1572204340.6460679
        result = util.safe_fromtimestamp(timestamp, tz.gettz("Europe/Paris"))
        expected = datetime.fromtimestamp(timestamp, tz.gettz("Europe/Paris"))
        self.assertEqual(result, expected)

    def test_safe_utcfromtimestamp_negative(self):
        timestamp = -1572204340.6460679
        result = util.safe_utcfromtimestamp(timestamp).replace(tzinfo=tz.tzutc())
        expected = datetime(1920, 3, 7, 4, 34, 19, 353932, tzinfo=tz.tzutc())
        self.assertEqual(result, expected)

    def test_safe_fromtimestamp_negative(self):
        timestamp = -1572204340.6460679
        result = util.safe_fromtimestamp(timestamp, tz.gettz("Europe/Paris"))
        expected = datetime(
            1920, 3, 7, 5, 34, 19, 353932, tzinfo=tz.gettz("Europe/Paris")
        )
        self.assertEqual(result, expected)

    @patch.object(util, "os_name", "nt")
    def test_safe_utcfromtimestamp_negative_nt(self):
        timestamp = -1572204340.6460679
        result = util.safe_utcfromtimestamp(timestamp).replace(tzinfo=tz.tzutc())
        expected = datetime(1920, 3, 7, 4, 34, 19, 353932, tzinfo=tz.tzutc())
        self.assertEqual(result, expected)

    @patch.object(util, "os_name", "nt")
    def test_safe_fromtimestamp_negative_nt(self):
        timestamp = -1572204340.6460679
        result = util.safe_fromtimestamp(timestamp, tz.gettz("Europe/Paris"))
        expected = datetime(
            1920, 3, 7, 5, 34, 19, 353932, tzinfo=tz.gettz("Europe/Paris")
        )
        self.assertEqual(result, expected)
