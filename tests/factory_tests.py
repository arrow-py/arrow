from chai import Chai
from datetime import datetime, timedelta
from dateutil import tz
import time

from arrow import factory, util


def assertDtEqual(dt1, dt2, within=10):
    assertEqual(dt1.tzinfo, dt2.tzinfo)
    diff = abs(util.total_seconds(dt1 - dt2)) 
    assertTrue(diff < within, "Diff between {} and {} was {}".format(dt1, dt2, diff))


class GetTests(Chai):

    def setUp(self):
        super(GetTests, self).setUp()

        self.factory = factory.ArrowFactory()

    def test_no_args(self):

        assertDtEqual(self.factory.get(), datetime.utcnow().replace(tzinfo=tz.tzutc()))

    def test_one_arg_non(self):

        assertDtEqual(self.factory.get(None), datetime.utcnow().replace(tzinfo=tz.tzutc()))

    def test_humanized(self):

        assertDtEqual(self.factory.get("5 minutes ago"),
            datetime.utcnow().replace(tzinfo=tz.tzutc()) - timedelta(minutes=5))

    def test_struct_time(self):

        assertDtEqual(self.factory.get(time.gmtime()),
            datetime.utcnow().replace(tzinfo=tz.tzutc()))

    def test_one_arg_timestamp(self):

        timestamp = 12345
        timestamp_dt = datetime.utcfromtimestamp(timestamp).replace(tzinfo=tz.tzutc())

        assertEqual(self.factory.get(timestamp), timestamp_dt)
        assertEqual(self.factory.get(str(timestamp)), timestamp_dt)

        timestamp = 123.45
        timestamp_dt = datetime.utcfromtimestamp(timestamp).replace(tzinfo=tz.tzutc())

        assertEqual(self.factory.get(timestamp), timestamp_dt)
        assertEqual(self.factory.get(str(timestamp)), timestamp_dt)

    def test_one_arg_arrow(self):

        arw = self.factory.utcnow()
        result = self.factory.get(arw)

        assertEqual(arw, result)

    def test_one_arg_datetime(self):

        dt = datetime.utcnow().replace(tzinfo=tz.tzutc())

        assertEqual(self.factory.get(dt), dt)

    def test_one_arg_tzinfo(self):

        expected = datetime.utcnow().replace(tzinfo=tz.tzutc()).astimezone(tz.gettz('US/Pacific'))

        assertDtEqual(self.factory.get(tz.gettz('US/Pacific')), expected)

    def test_one_arg_iso_str(self):
        dt = datetime.utcnow()
        assertDtEqual(self.factory.get(dt.isoformat()), dt.replace(tzinfo=tz.tzutc()))

    def test_one_arg_other(self):

        with assertRaises(TypeError):
            self.factory.get(object())

    def test_two_args_datetime_tzinfo(self):

        result = self.factory.get(datetime(2013, 1, 1), tz.gettz('US/Pacific'))

        assertEqual(result._datetime, datetime(2013, 1, 1, tzinfo=tz.gettz('US/Pacific')))

    def test_two_args_datetime_tz_str(self):

        result = self.factory.get(datetime(2013, 1, 1), 'US/Pacific')

        assertEqual(result._datetime, datetime(2013, 1, 1, tzinfo=tz.gettz('US/Pacific')))

    def test_two_args_datetime_other(self):

        with assertRaises(TypeError):
            self.factory.get(datetime.utcnow(), object())

    def test_two_args_str_str(self):

        result = self.factory.get('2013-01-01', 'YYYY-MM-DD')

        assertEqual(result._datetime, datetime(2013, 1, 1, tzinfo=tz.tzutc()))

    def test_two_args_str_list(self):

        result = self.factory.get('2013-01-01', ['MM/DD/YYYY', 'YYYY-MM-DD'])

        assertEqual(result._datetime, datetime(2013, 1, 1, tzinfo=tz.tzutc()))

    def test_two_args_unicode_unicode(self):

        result = self.factory.get(u'2013-01-01', u'YYYY-MM-DD')

        assertEqual(result._datetime, datetime(2013, 1, 1, tzinfo=tz.tzutc()))

    def test_two_args_other(self):

        with assertRaises(TypeError):
            self.factory.get(object(), object())

    def test_three_args(self):

        assertEqual(self.factory.get(2013, 1, 1), datetime(2013, 1, 1, tzinfo=tz.tzutc()))


def UtcNowTests(Chai):

    def test_utcnow(self):

        assertDtEqual(self.factory.utcnow()._datetime, datetime.utcnow().replace(tzinfo=tz.tzutc()))


class NowTests(Chai):

    def setUp(self):
        super(NowTests, self).setUp()

        self.factory = factory.ArrowFactory()

    def test_no_tz(self):

        assertDtEqual(self.factory.now(), datetime.now(tz.tzlocal()))

    def test_tzinfo(self):

        assertDtEqual(self.factory.now(tz.gettz('EST')), datetime.now(tz.gettz('EST')))

    def test_tz_str(self):

        assertDtEqual(self.factory.now('EST'), datetime.now(tz.gettz('EST')))

