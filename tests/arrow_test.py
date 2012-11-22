from arrow import arrow, Arrow, TimeZone
from arrow.arrow import FORMAT

from datetime import datetime, timedelta, tzinfo
from dateutil import tz

import time, calendar
import unittest

class BaseArrowTests(unittest.TestCase):

    def setUp(self):
        super(BaseArrowTests, self).setUp()

        self.utc = TimeZone()
        self.local = TimeZone('local')

    def assert_ts_equal(self, ts_1, ts_2, delta=5.0):

        if abs(ts_1 - ts_2) > delta:
            raise AssertionError('{0} != {1} within +/- {2}'.format(ts_1, ts_2, delta))

    def assert_dt_equal(self, dt_1, dt_2, delta=5.0):

        ts_1 = time.mktime(dt_1.timetuple())
        ts_2 = time.mktime(dt_2.timetuple())

        if abs(ts_1 - ts_2) > delta:
            raise AssertionError('{0} != {1} within +/- {2}'.format(dt_1, dt_2, delta))


class ArrowTests(BaseArrowTests):

    def setUp(self):
        super(ArrowTests, self).setUp()

        self.arrow = Arrow(datetime.utcnow(), tz='UTC')

    def test_str(self):

        expected = format(self.arrow.datetime, FORMAT)
        self.assertEqual(str(self.arrow), expected)

    def test_repr(self):

        expected = 'Arrow({0:s})'.format(self.arrow)

        self.assertEqual(repr(self.arrow), expected)

    def test_tz(self):

        self.arrow._timezone = self.utc

        self.assertEqual(self.arrow.tz, self.utc)

    def test_to(self):

        self.arrow._datetime = datetime.utcnow().replace(tzinfo=self.utc.tzinfo)
        self.arrow._timezone = self.utc

        result = self.arrow.to('local')

        self.assert_dt_equal(result.datetime, self.arrow._datetime.astimezone(self.local.tzinfo))

    def test_utc_utc(self):

        self.arrow._datetime = datetime.now().replace(tzinfo=self.local.tzinfo)
        self.arrow._timezone = self.local

        result = self.arrow.utc()

        self.assert_dt_equal(result.datetime, self.arrow._datetime.astimezone(self.utc.tzinfo))

    def test_utc_local(self):

        self.arrow._datetime = datetime.utcnow().replace(tzinfo=self.utc.tzinfo)
        self.arrow._timezone = self.utc

        result = self.arrow.utc()

        self.assert_dt_equal(result.datetime, self.arrow._datetime.astimezone(self.utc.tzinfo))

    def test_datetime(self):

        dt = datetime.utcnow().replace(tzinfo=tz.tzutc())

        self.arrow._datetime = dt
        self.arrow._timezone = self.utc

        result = self.arrow.datetime

        self.assertEqual(result, dt)

    def test_timestamp(self):

        dt = datetime.utcnow()

        self.arrow._datetime = dt
        self.arrow._timezone = self.utc

        result = self.arrow.timestamp

        self.assertEqual(result, calendar.timegm(dt.timetuple()))

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

    def test_get_datetime_parse_str(self):

        with self.assertRaises(RuntimeError):
            self.arrow._get_datetime('abcdefg', self.utc)

    def test_get_datetime_unrecognized(self):

        with self.assertRaises(RuntimeError):
            self.arrow._get_datetime(object, self.utc)


class ArrowToTests(BaseArrowTests):

    def test_utc_to_local(self):
        
        arr = Arrow(datetime.utcnow(), tz='UTC')

        result = arr.to('local')

        self.assert_dt_equal(result.datetime, datetime.now())
        self.assert_ts_equal(result.timestamp, time.time())

    def test_local_to_utc(self):

        arr = Arrow(datetime.now(), tz='local')

        result = arr.to('UTC')

        self.assert_dt_equal(result.datetime, datetime.utcnow())
        self.assert_ts_equal(result.timestamp, time.time())

    def test_zone_to_zone(self):

        dt_1 = datetime.utcnow() + timedelta(hours=-2)
        dt_2 = datetime.utcnow() + timedelta(hours=2)

        arr_1 = Arrow(dt_1, timedelta(hours=-2))
        arr_2 = Arrow(dt_2, timedelta(hours=2))

        result_1 = arr_1.to(timedelta(hours=2))
        result_2 = arr_2.to(timedelta(hours=-2))

        self.assert_dt_equal(result_1.datetime, arr_2.datetime)
        self.assert_dt_equal(result_2.datetime, arr_1.datetime)


class ArrowFunctionTest(BaseArrowTests):

    def test_no_args(self):

        result = arrow()

        self.assert_dt_equal(result.datetime, datetime.utcnow())
        self.assert_ts_equal(result.timestamp, time.time())
        self.assertTrue(result.tz.utc)

    def test_one_arg_utc_datetime_now(self):

        result = arrow(datetime.utcnow())

        self.assert_dt_equal(result.datetime, datetime.utcnow())
        self.assert_ts_equal(result.timestamp, time.time())
        self.assertEqual(result.tz.tzinfo, tz.tzutc())

    def test_one_arg_local_datetime_now(self):

        # Wrong, but confirms default handling as UTC.
        result = arrow(datetime.now())

        self.assert_dt_equal(result.datetime, datetime.now())
        self.assertTrue(result.tz.utc)

    def test_one_arg_utc_datetime_prev(self):

        dt = datetime.utcnow() + timedelta(hours=-1)

        result = arrow(dt)

        self.assert_dt_equal(result.datetime, dt)
        self.assert_ts_equal(result.timestamp, time.time() - 3600)

    def test_one_arg_local_timezone(self):

        result = arrow('local')

        self.assert_dt_equal(result.datetime, datetime.now())
        self.assert_ts_equal(result.timestamp, time.time())

    def test_one_arg_named_timezone(self):

        result = arrow('US/Pacific')

        dt_expected = datetime.utcnow().replace(tzinfo=tz.tzutc()).astimezone(
            tz.gettz('US/Pacific'))

        self.assert_dt_equal(result.datetime, dt_expected)
        self.assert_ts_equal(result.timestamp, time.time())

    def test_one_arg_iso_timezone(self):

        result = arrow('-01:30')

        dt_expected = datetime.utcnow().replace(tzinfo=tz.tzutc()).astimezone(
            tz.tzoffset(None, -5400))

        self.assert_dt_equal(result.datetime, dt_expected)
        self.assert_ts_equal(result.timestamp, time.time())

    def test_two_args_utc_datetime_now_utc_str(self):

        result = arrow(datetime.utcnow(), 'UTC')

        self.assert_dt_equal(result.datetime, datetime.utcnow())
        self.assert_ts_equal(result.timestamp, time.time())

    def test_two_args_local_datetime_now_local_str(self):

        result = arrow(datetime.now(), 'local')

        self.assert_dt_equal(result.datetime, datetime.now())
        self.assert_ts_equal(result.timestamp, time.time())
        self.assertEqual(result.tz.utcoffset, self.local.utcoffset)

    def test_two_args_utc_datetime_past_utc_str(self):

        dt = datetime.utcnow() + timedelta(hours=-1)

        result = arrow(dt, 'UTC')

        self.assert_dt_equal(result.datetime, dt)
        self.assert_ts_equal(result.timestamp, time.time() - 3600)

    def test_two_args_olson_datetime_past_iso_str(self):

        dt = datetime.utcnow() + timedelta(hours=-1)

        result = arrow(dt, '+01:00')

        self.assert_dt_equal(result.datetime, dt)
        self.assert_ts_equal(result.timestamp, time.time() - 7200)

    def test_tz_kwarg_local(self):

        result = arrow(tz='local')

        self.assert_dt_equal(result.datetime, datetime.now())
        self.assert_ts_equal(result.timestamp, time.time())

