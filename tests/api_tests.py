from chai import Chai
from datetime import datetime
from dateutil import tz
import time

from arrow import api

def assertDtEqual(dt1, dt2, within=10):
    assertTrue(abs((dt1 - dt2).total_seconds()) < within)


class GetTests(Chai):

    def test_no_args(self):

        result = api.get()

        assertDtEqual(result, datetime.utcnow().replace(tzinfo=tz.tzutc()))

    def test_one_arg_timestamp(self):

        timestamp = 12345
        timestamp_dt = datetime.utcfromtimestamp(timestamp).replace(tzinfo=tz.tzutc())

        assertEqual(api.get(timestamp), timestamp_dt)
        assertEqual(api.get(str(timestamp)), timestamp_dt)

        timestamp = 123.45
        timestamp_dt = datetime.utcfromtimestamp(timestamp).replace(tzinfo=tz.tzutc())

        assertEqual(api.get(timestamp), timestamp_dt)
        assertEqual(api.get(str(timestamp)), timestamp_dt)

    def test_one_arg_datetime(self):

        dt = datetime.utcnow().replace(tzinfo=tz.tzutc())

        assertEqual(api.get(dt), dt)

    def test_one_arg_tzinfo(self):

        expected = datetime.utcnow().replace(tzinfo=tz.tzutc()).astimezone(tz.gettz('US/Pacific'))

        assertDtEqual(api.get(tz.gettz('US/Pacific')), expected)

    def test_one_arg_tz_str(self):

        expected = datetime.utcnow().replace(tzinfo=tz.tzutc()).astimezone(tz.gettz('US/Pacific'))

        assertDtEqual(api.get('US/Pacific'), expected)

    def test_one_arg_other(self):

        with assertRaises(TypeError):
            api.get(object())

    def test_two_args_datetime_tzinfo(self):

        result = api.get(datetime(2013, 1, 1), tz.gettz('US/Pacific'))

        assertEqual(result._datetime, datetime(2013, 1, 1, tzinfo=tz.gettz('US/Pacific')))

    def test_two_args_datetime_tz_str(self):

        result = api.get(datetime(2013, 1, 1), 'US/Pacific')

        assertEqual(result._datetime, datetime(2013, 1, 1, tzinfo=tz.gettz('US/Pacific')))

    def test_two_args_datetime_other(self):

        with assertRaises(TypeError):
            api.get(datetime.utcnow(), object())

    def test_two_args_str_str(self):

        result = api.get('2013-01-01', 'YYYY-MM-DD')

        assertEqual(result._datetime, datetime(2013, 1, 1, tzinfo=tz.tzutc()))

    def test_two_args_other(self):

        with assertRaises(TypeError):
            api.get(object(), object())

    def test_three_args(self):

        assertEqual(api.get(2013, 1, 1), datetime(2013, 1, 1, tzinfo=tz.tzutc()))


def UtcNowTests(Chai):

    def test_utcnow(self):

        assertDtEqual(api.utcnow()._datetime, datetime.utcnow().replace(tzinfo=tz.tzutc()))


class NowTests(Chai):

    def test_no_tz(self):

        assertDtEqual(api.now(), datetime.now(tz.tzlocal()))

    def test_tzinfo(self):

        assertDtEqual(api.now(tz.gettz('EST')), datetime.now(tz.gettz('EST')))

    def test_tz_str(self):

        assertDtEqual(api.now('EST'), datetime.now(tz.gettz('EST')))


class ArrowTests(Chai):

    def test_none_none(self):

        result = api.arrow()

        assertDtEqual(result._datetime, datetime.utcnow().replace(tzinfo=tz.tzutc()))

    def test_none_tz(self):

        result = api.arrow('local')

        assertDtEqual(result._datetime, datetime.now(tz.tzlocal()))

    def test_dt_str_none(self):

        dt = datetime(2013, 1, 1)

        result = api.arrow(dt)

        assertDtEqual(result._datetime, dt.replace(tzinfo=tz.tzutc()))

    def test_datetime_tzinfo(self):

        result = api.arrow(datetime(2013, 1, 1), 'local')

        assertEqual(result._datetime, datetime(2013, 1, 1, tzinfo=tz.tzlocal()))

    def test_int(self):

        timestamp = int(time.time())

        result = api.arrow(timestamp)
