from datetime import datetime, timedelta, tzinfo
import time, calendar
import arrow
import unittest

from dateutil import tz

class TimeZoneTests(unittest.TestCase):

    def setUp(self):

        self.time_zone = arrow.TimeZone('UTC')
        self.datetime = datetime.utcnow()

    def assert_tzinfo_equal(self, tzinfo_1, tzinfo_2):

        dt = datetime.now()
        self.assertEqual(tzinfo_1.utcoffset(dt), tzinfo_2.utcoffset(dt))

    def test_str(self):

        self.assertEqual(self.time_zone.__str__(), 'TimeZone(UTC, 0:00:00)')
        self.assertEqual(self.time_zone.__repr__(), 'TimeZone(UTC, 0:00:00)')

    def test_name(self):
        self.assertEqual(self.time_zone.name, 'UTC')

    def test_utcoffset(self):
        self.assertEqual(self.time_zone.utcoffset, timedelta())

    def test_utc(self):
        self.assertTrue(self.time_zone.utc)

    def test_tzinfo(self):
        self.assertIsInstance(self.time_zone.tzinfo, tzinfo)

    def test_get_tz_str(self):

        result = self.time_zone._get_tzinfo('UTC')

        self.assert_tzinfo_equal(result, tz.tzutc())

    def test_get_tz_str_local(self):

        result = self.time_zone._get_tzinfo('local')

        self.assert_tzinfo_equal(result, tz.tzlocal())

    def test_get_tz_tzinfo(self):

        tz_utc = tz.tzutc()

        result = self.time_zone._get_tzinfo(tz_utc)

        self.assertEqual(result, tz_utc)

    def test_get_tz_timedelta(self):

        result = self.time_zone._get_tzinfo(timedelta(minutes=-60))

        self.assert_tzinfo_equal(result, tz.tzoffset(None, -3600))

    def test_get_tz_none(self):

        with self.assertRaises(Exception):
            self.time_zone._get_tzinfo(None)

class BaseArrowTests(unittest.TestCase):

    def assert_ts_equal(self, ts_1, ts_2, delta=5.0):
        eq = abs(ts_1 - ts_2) <= delta

        if not eq:
            raise AssertionError('{0} != {1} within +/- {2}'.format(ts_1, ts_2, delta))

    def assert_dt_equal(self, dt_1, dt_2, delta=5.0):

        ts_1 = time.mktime(dt_1.timetuple())
        ts_2 = time.mktime(dt_2.timetuple())

        eq = abs(ts_1 - ts_2) <= delta

        if not eq:
            raise AssertionError('{0} != {1} within +/- {2}'.format(dt_1, dt_2, delta))

class ArrowTests(BaseArrowTests):

    def setUp(self):

        self.utc = arrow.TimeZone()
        self.local = arrow.TimeZone('local')

        self.arrow = arrow.Arrow()

    def test_datetime(self):

        dt = datetime.utcnow().replace(tzinfo=tz.tzutc())

        self.arrow._datetime = dt
        self.arrow._time_zone = self.utc

        result = self.arrow.datetime

        self.assertEqual(result, dt)

    def test_timestamp_utc(self):

        dt = datetime.utcnow()

        self.arrow._datetime = dt
        self.arrow._time_zone = self.utc

        result = self.arrow.timestamp

        self.assertEqual(result, calendar.timegm(dt.timetuple()))

    def test_timestamp_local(self):

        dt = datetime.now()

        self.arrow._datetime = dt
        self.arrow._time_zone = self.local

        result = self.arrow.timestamp

        self.assertEqual(result, time.mktime(dt.timetuple()))

    def test_get_datetime_none(self):

        result = self.arrow._get_datetime(None, self.utc)

        self.assert_dt_equal(result, datetime.utcnow())
        self.assertEqual(result.tzinfo, self.utc.tzinfo)

    def test_get_datetime_int(self):

        result = self.arrow._get_datetime(int(time.time()), self.utc)

        self.assert_dt_equal(result, datetime.utcnow())

    def test_get_datetime_float_utc(self):

        result = self.arrow._get_datetime(time.time(), self.utc)

        self.assert_dt_equal(result, datetime.utcnow())

    def test_get_datetime_float_local(self):

        result = self.arrow._get_datetime(time.time(), self.local)

        self.assert_dt_equal(result, datetime.now())

    def test_get_datetime_str_float_utc(self):

        result = self.arrow._get_datetime(str(time.time()), self.utc)

        self.assert_dt_equal(result, datetime.utcnow())

    def test_get_datetime_str_int_utc(self):

        result = self.arrow._get_datetime(str(int(time.time())), self.utc)

        self.assert_dt_equal(result, datetime.utcnow())

    def test_get_datetime_str_float_local(self):

        result = self.arrow._get_datetime(str(time.time()), self.local)

        self.assert_dt_equal(result, datetime.now())

    def test_get_datetime_str_int_local(self):

        result = self.arrow._get_datetime(str(int(time.time())), self.local)
        
        self.assert_dt_equal(result, datetime.now())

    def test_get_datetime_datetime(self):

        dt = datetime.utcnow()

        result = self.arrow._get_datetime(dt, self.utc)

        self.assert_dt_equal(result, dt)

    def test_get_datetime_unrecognized(self):

        with self.assertRaises(RuntimeError):
            self.arrow._get_datetime(object, self.utc)

    def test_get_datetime_parse_str(self):

        with self.assertRaises(NotImplementedError):
            self.arrow._get_datetime('1-1-2012', self.utc)



# class ArrowInitTests(BaseArrowTests):

#     def test_none_no_tz(self):

#         arrow = Arrow()

#         self.assert_dt_equal(arrow.datetime, datetime.utcnow())
#         self.assert_ts_equal(arrow.timestamp, time.time())

#     def test_utc_datetime_no_tz(self):

#         arrow = Arrow(datetime.utcnow())

#         self.assert_dt_equal(arrow.datetime, datetime.utcnow())
#         self.assert_ts_equal(arrow.timestamp, time.time())

#     def test_utc_int_timestamp_no_tz(self):

#         arrow = Arrow(int(time.time()))

#         self.assert_dt_equal(arrow.datetime, datetime.utcnow())
#         self.assert_ts_equal(arrow.timestamp, time.time())

#     def test_utc_float_timestamp_no_tz(self):

#         arrow = Arrow(time.time())

#         self.assert_dt_equal(arrow.datetime, datetime.utcnow())
#         self.assert_ts_equal(arrow.timestamp, time.time())

#     def test_utc_int_str_timestamp_no_tz(self):

#         arrow = Arrow(str(int(time.time())))

#         self.assert_dt_equal(arrow.datetime, datetime.utcnow())
#         self.assert_ts_equal(arrow.timestamp, time.time())

#     def test_utc_float_str_timestamp_no_tz(self):

#         arrow = Arrow(str(time.time()))

#         self.assert_dt_equal(arrow.datetime, datetime.utcnow())
#         self.assert_ts_equal(arrow.timestamp, time.time())






