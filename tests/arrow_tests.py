# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals

from chai import Chai

from datetime import date, datetime, timedelta
from dateutil import tz
import simplejson as json
import warnings
import calendar
import pickle
import time
import sys

from arrow import arrow, util


def assertDtEqual(dt1, dt2, within=10):
    assertEqual(dt1.tzinfo, dt2.tzinfo)
    assertTrue(abs(util.total_seconds(dt1 - dt2)) < within)


class ArrowInitTests(Chai):

    def test_init(self):

        result = arrow.Arrow(2013, 2, 2, 12, 30, 45, 999999)
        expected = datetime(2013, 2, 2, 12, 30, 45, 999999, tzinfo=tz.tzutc())

        assertEqual(result._datetime, expected)


class ArrowFactoryTests(Chai):

    def test_now(self):

        result = arrow.Arrow.now()

        assertDtEqual(result._datetime, datetime.now().replace(tzinfo=tz.tzlocal()))

    def test_utcnow(self):

        result = arrow.Arrow.utcnow()

        assertDtEqual(result._datetime, datetime.utcnow().replace(tzinfo=tz.tzutc()))

    def test_fromtimestamp(self):

        timestamp = time.time()

        result = arrow.Arrow.fromtimestamp(timestamp)

        assertDtEqual(result._datetime, datetime.now().replace(tzinfo=tz.tzlocal()))

    def test_fromdatetime(self):

        dt = datetime(2013, 2, 3, 12, 30, 45, 1)

        result = arrow.Arrow.fromdatetime(dt)

        assertEqual(result._datetime, dt.replace(tzinfo=tz.tzutc()))

    def test_fromdatetime_dt_tzinfo(self):

        dt = datetime(2013, 2, 3, 12, 30, 45, 1, tzinfo=tz.gettz('US/Pacific'))

        result = arrow.Arrow.fromdatetime(dt)

        assertEqual(result._datetime, dt.replace(tzinfo=tz.gettz('US/Pacific')))

    def test_fromdatetime_tzinfo_arg(self):

        dt = datetime(2013, 2, 3, 12, 30, 45, 1)

        result = arrow.Arrow.fromdatetime(dt, tz.gettz('US/Pacific'))

        assertEqual(result._datetime, dt.replace(tzinfo=tz.gettz('US/Pacific')))

    def test_fromdate(self):

        dt = date(2013, 2, 3)

        result = arrow.Arrow.fromdate(dt, tz.gettz('US/Pacific'))

        assertEqual(result._datetime, datetime(2013, 2, 3, tzinfo=tz.gettz('US/Pacific')))

    def test_strptime(self):

        formatted = datetime(2013, 2, 3, 12, 30, 45).strftime('%Y-%m-%d %H:%M:%S')

        result = arrow.Arrow.strptime(formatted, '%Y-%m-%d %H:%M:%S')

        assertEqual(result._datetime, datetime(2013, 2, 3, 12, 30, 45, tzinfo=tz.tzutc()))


class ArrowRepresentationTests(Chai):

    def setUp(self):
        super(ArrowRepresentationTests, self).setUp()

        self.arrow = arrow.Arrow(2013, 2, 3, 12, 30, 45, 1)

    def test_repr(self):

        result = self.arrow.__repr__()

        assertEqual(result, '<Arrow [{0}]>'.format(self.arrow._datetime.isoformat()))

    def test_str(self):

        result = self.arrow.__str__()

        assertEqual(result, self.arrow._datetime.isoformat())

    def test_hash(self):

        result = self.arrow.__hash__()

        assertEqual(result, self.arrow._datetime.__hash__())

    def test_format(self):

        result = '{0:YYYY-MM-DD}'.format(self.arrow)

        assertEqual(result, '2013-02-03')

    def test_bare_format(self):

        result = self.arrow.format()

        assertEqual(result, '2013-02-03 12:30:45+00:00')

    def test_format_no_format_string(self):

        result = '{0}'.format(self.arrow)

        assertEqual(result, str(self.arrow))

    def test_clone(self):

        result = self.arrow.clone()

        assertTrue(result is not self.arrow)
        assertEqual(result._datetime, self.arrow._datetime)


class ArrowAttributeTests(Chai):

    def setUp(self):
        super(ArrowAttributeTests, self).setUp()

        self.arrow = arrow.Arrow(2013, 1, 1)

    def test_getattr_base(self):

        with assertRaises(AttributeError):
            self.arrow.prop

    def test_getattr_week(self):

        assertEqual(self.arrow.week, 1)

    def test_getattr_quarter(self):
        # start dates
        q1 = arrow.Arrow(2013, 1, 1)
        q2 = arrow.Arrow(2013, 4, 1)
        q3 = arrow.Arrow(2013, 8, 1)
        q4 = arrow.Arrow(2013, 10, 1)
        assertEqual(q1.quarter, 1)
        assertEqual(q2.quarter, 2)
        assertEqual(q3.quarter, 3)
        assertEqual(q4.quarter, 4)

        # end dates
        q1 = arrow.Arrow(2013, 3, 31)
        q2 = arrow.Arrow(2013, 6, 30)
        q3 = arrow.Arrow(2013, 9, 30)
        q4 = arrow.Arrow(2013, 12, 31)
        assertEqual(q1.quarter, 1)
        assertEqual(q2.quarter, 2)
        assertEqual(q3.quarter, 3)
        assertEqual(q4.quarter, 4)

    def test_getattr_dt_value(self):

        assertEqual(self.arrow.year, 2013)

    def test_tzinfo(self):

        self.arrow.tzinfo = tz.gettz('PST')
        assertEqual(self.arrow.tzinfo, tz.gettz('PST'))

    def test_naive(self):

        assertEqual(self.arrow.naive, self.arrow._datetime.replace(tzinfo=None))

    def test_timestamp(self):

        assertEqual(self.arrow.timestamp, calendar.timegm(self.arrow._datetime.utctimetuple()))

    def test_float_timestamp(self):

        result = self.arrow.float_timestamp - self.arrow.timestamp

        assertEqual(result, self.arrow.microsecond)


class ArrowComparisonTests(Chai):

    def setUp(self):
        super(ArrowComparisonTests, self).setUp()

        self.arrow = arrow.Arrow.utcnow()

    def test_eq(self):

        assertTrue(self.arrow == self.arrow)
        assertTrue(self.arrow == self.arrow.datetime)
        assertFalse(self.arrow == 'abc')

    def test_ne(self):

        assertFalse(self.arrow != self.arrow)
        assertFalse(self.arrow != self.arrow.datetime)
        assertTrue(self.arrow != 'abc')

    def test_deprecated_replace(self):

        with warnings.catch_warnings(record=True) as w:
            # Cause all warnings to always be triggered.
            warnings.simplefilter("always")
            # Trigger a warning.
            self.arrow.replace(weeks=1)
            # Verify some things
            assert len(w) == 1
            assert issubclass(w[-1].category, DeprecationWarning)
            assert "deprecated" in str(w[-1].message)

        with warnings.catch_warnings(record=True) as w:
            # Cause all warnings to always be triggered.
            warnings.simplefilter("always")
            # Trigger a warning.
            self.arrow.replace(hours=1)
            # Verify some things
            assert len(w) == 1
            assert issubclass(w[-1].category, DeprecationWarning)
            assert "deprecated" in str(w[-1].message)

    def test_gt(self):

        arrow_cmp = self.arrow.shift(minutes=1)

        assertFalse(self.arrow > self.arrow)
        assertFalse(self.arrow > self.arrow.datetime)

        with assertRaises(TypeError):
            self.arrow > 'abc'

        assertTrue(self.arrow < arrow_cmp)
        assertTrue(self.arrow < arrow_cmp.datetime)

    def test_ge(self):

        with assertRaises(TypeError):
            self.arrow >= 'abc'

        assertTrue(self.arrow >= self.arrow)
        assertTrue(self.arrow >= self.arrow.datetime)

    def test_lt(self):

        arrow_cmp = self.arrow.shift(minutes=1)

        assertFalse(self.arrow < self.arrow)
        assertFalse(self.arrow < self.arrow.datetime)

        with assertRaises(TypeError):
            self.arrow < 'abc'

        assertTrue(self.arrow < arrow_cmp)
        assertTrue(self.arrow < arrow_cmp.datetime)

    def test_le(self):

        with assertRaises(TypeError):
            self.arrow <= 'abc'

        assertTrue(self.arrow <= self.arrow)
        assertTrue(self.arrow <= self.arrow.datetime)


class ArrowMathTests(Chai):

    def setUp(self):
        super(ArrowMathTests, self).setUp()

        self.arrow = arrow.Arrow(2013, 1, 1)

    def test_add_timedelta(self):

        result = self.arrow.__add__(timedelta(days=1))

        assertEqual(result._datetime, datetime(2013, 1, 2, tzinfo=tz.tzutc()))

    def test_add_other(self):

        with assertRaises(TypeError):
            self.arrow.__add__(1)

    def test_radd(self):

        result = self.arrow.__radd__(timedelta(days=1))

        assertEqual(result._datetime, datetime(2013, 1, 2, tzinfo=tz.tzutc()))

    def test_sub_timedelta(self):

        result = self.arrow.__sub__(timedelta(days=1))

        assertEqual(result._datetime, datetime(2012, 12, 31, tzinfo=tz.tzutc()))

    def test_sub_datetime(self):

        result = self.arrow.__sub__(datetime(2012, 12, 21, tzinfo=tz.tzutc()))

        assertEqual(result, timedelta(days=11))

    def test_sub_arrow(self):

        result = self.arrow.__sub__(arrow.Arrow(2012, 12, 21, tzinfo=tz.tzutc()))

        assertEqual(result, timedelta(days=11))

    def test_sub_other(self):

        with assertRaises(TypeError):
            self.arrow.__sub__(object())

    def test_rsub_datetime(self):

        result = self.arrow.__rsub__(datetime(2012, 12, 21, tzinfo=tz.tzutc()))

        assertEqual(result, timedelta(days=-11))

    def test_rsub_other(self):

        with assertRaises(TypeError):
            self.arrow.__rsub__(timedelta(days=1))


class ArrowDatetimeInterfaceTests(Chai):

    def setUp(self):
        super(ArrowDatetimeInterfaceTests, self).setUp()

        self.arrow = arrow.Arrow.utcnow()

    def test_date(self):

        result = self.arrow.date()

        assertEqual(result, self.arrow._datetime.date())

    def test_time(self):

        result = self.arrow.time()

        assertEqual(result, self.arrow._datetime.time())

    def test_timetz(self):

        result = self.arrow.timetz()

        assertEqual(result, self.arrow._datetime.timetz())

    def test_astimezone(self):

        other_tz = tz.gettz('US/Pacific')

        result = self.arrow.astimezone(other_tz)

        assertEqual(result, self.arrow._datetime.astimezone(other_tz))

    def test_utcoffset(self):

        result = self.arrow.utcoffset()

        assertEqual(result, self.arrow._datetime.utcoffset())

    def test_dst(self):

        result = self.arrow.dst()

        assertEqual(result, self.arrow._datetime.dst())

    def test_timetuple(self):

        result = self.arrow.timetuple()

        assertEqual(result, self.arrow._datetime.timetuple())

    def test_utctimetuple(self):

        result = self.arrow.utctimetuple()

        assertEqual(result, self.arrow._datetime.utctimetuple())

    def test_toordinal(self):

        result = self.arrow.toordinal()

        assertEqual(result, self.arrow._datetime.toordinal())

    def test_weekday(self):

        result = self.arrow.weekday()

        assertEqual(result, self.arrow._datetime.weekday())

    def test_isoweekday(self):

        result = self.arrow.isoweekday()

        assertEqual(result, self.arrow._datetime.isoweekday())

    def test_isocalendar(self):

        result = self.arrow.isocalendar()

        assertEqual(result, self.arrow._datetime.isocalendar())

    def test_isoformat(self):

        result = self.arrow.isoformat()

        assertEqual(result, self.arrow._datetime.isoformat())

    def test_simplejson(self):

        result = json.dumps({'v': self.arrow.for_json()}, for_json=True)

        assertEqual(json.loads(result)['v'], self.arrow._datetime.isoformat())

    def test_ctime(self):

        result = self.arrow.ctime()

        assertEqual(result, self.arrow._datetime.ctime())

    def test_strftime(self):

        result = self.arrow.strftime('%Y')

        assertEqual(result, self.arrow._datetime.strftime('%Y'))


class ArrowConversionTests(Chai):

    def test_to(self):

        dt_from = datetime.now()
        arrow_from = arrow.Arrow.fromdatetime(dt_from, tz.gettz('US/Pacific'))

        expected = dt_from.replace(tzinfo=tz.gettz('US/Pacific')).astimezone(tz.tzutc())

        assertEqual(arrow_from.to('UTC').datetime, expected)
        assertEqual(arrow_from.to(tz.tzutc()).datetime, expected)


class ArrowPicklingTests(Chai):

    def test_pickle_and_unpickle(self):

        dt = arrow.Arrow.utcnow()

        pickled = pickle.dumps(dt)

        unpickled = pickle.loads(pickled)

        assertEqual(unpickled, dt)


class ArrowReplaceTests(Chai):

    def test_not_attr(self):

        with assertRaises(AttributeError):
            arrow.Arrow.utcnow().replace(abc=1)

    def test_replace(self):

        arw = arrow.Arrow(2013, 5, 5, 12, 30, 45)

        assertEqual(arw.replace(year=2012), arrow.Arrow(2012, 5, 5, 12, 30, 45))
        assertEqual(arw.replace(month=1), arrow.Arrow(2013, 1, 5, 12, 30, 45))
        assertEqual(arw.replace(day=1), arrow.Arrow(2013, 5, 1, 12, 30, 45))
        assertEqual(arw.replace(hour=1), arrow.Arrow(2013, 5, 5, 1, 30, 45))
        assertEqual(arw.replace(minute=1), arrow.Arrow(2013, 5, 5, 12, 1, 45))
        assertEqual(arw.replace(second=1), arrow.Arrow(2013, 5, 5, 12, 30, 1))

    def test_replace_shift(self):

        arw = arrow.Arrow(2013, 5, 5, 12, 30, 45)

        # This is all scheduled for deprecation
        assertEqual(arw.replace(years=1), arrow.Arrow(2014, 5, 5, 12, 30, 45))
        assertEqual(arw.replace(quarters=1), arrow.Arrow(2013, 8, 5, 12, 30, 45))
        assertEqual(arw.replace(quarters=1, months=1), arrow.Arrow(2013, 9, 5, 12, 30, 45))
        assertEqual(arw.replace(months=1), arrow.Arrow(2013, 6, 5, 12, 30, 45))
        assertEqual(arw.replace(weeks=1), arrow.Arrow(2013, 5, 12, 12, 30, 45))
        assertEqual(arw.replace(days=1), arrow.Arrow(2013, 5, 6, 12, 30, 45))
        assertEqual(arw.replace(hours=1), arrow.Arrow(2013, 5, 5, 13, 30, 45))
        assertEqual(arw.replace(minutes=1), arrow.Arrow(2013, 5, 5, 12, 31, 45))
        assertEqual(arw.replace(seconds=1), arrow.Arrow(2013, 5, 5, 12, 30, 46))
        assertEqual(arw.replace(microseconds=1), arrow.Arrow(2013, 5, 5, 12, 30, 45, 1))

    def test_replace_shift_negative(self):

        arw = arrow.Arrow(2013, 5, 5, 12, 30, 45)

        # This is all scheduled for deprecation
        assertEqual(arw.replace(years=-1), arrow.Arrow(2012, 5, 5, 12, 30, 45))
        assertEqual(arw.replace(quarters=-1), arrow.Arrow(2013, 2, 5, 12, 30, 45))
        assertEqual(arw.replace(quarters=-1, months=-1), arrow.Arrow(2013, 1, 5, 12, 30, 45))
        assertEqual(arw.replace(months=-1), arrow.Arrow(2013, 4, 5, 12, 30, 45))
        assertEqual(arw.replace(weeks=-1), arrow.Arrow(2013, 4, 28, 12, 30, 45))
        assertEqual(arw.replace(days=-1), arrow.Arrow(2013, 5, 4, 12, 30, 45))
        assertEqual(arw.replace(hours=-1), arrow.Arrow(2013, 5, 5, 11, 30, 45))
        assertEqual(arw.replace(minutes=-1), arrow.Arrow(2013, 5, 5, 12, 29, 45))
        assertEqual(arw.replace(seconds=-1), arrow.Arrow(2013, 5, 5, 12, 30, 44))
        assertEqual(arw.replace(microseconds=-1), arrow.Arrow(2013, 5, 5, 12, 30, 44, 999999))

    def test_replace_quarters_bug(self):

        arw = arrow.Arrow(2013, 5, 5, 12, 30, 45)

        # The value of the last-read argument was used instead of the ``quarters`` argument.
        # Recall that the keyword argument dict, like all dicts, is unordered, so only certain
        # combinations of arguments would exhibit this.
        assertEqual(arw.replace(quarters=0, years=1), arrow.Arrow(2014, 5, 5, 12, 30, 45))
        assertEqual(arw.replace(quarters=0, months=1), arrow.Arrow(2013, 6, 5, 12, 30, 45))
        assertEqual(arw.replace(quarters=0, weeks=1), arrow.Arrow(2013, 5, 12, 12, 30, 45))
        assertEqual(arw.replace(quarters=0, days=1), arrow.Arrow(2013, 5, 6, 12, 30, 45))
        assertEqual(arw.replace(quarters=0, hours=1), arrow.Arrow(2013, 5, 5, 13, 30, 45))
        assertEqual(arw.replace(quarters=0, minutes=1), arrow.Arrow(2013, 5, 5, 12, 31, 45))
        assertEqual(arw.replace(quarters=0, seconds=1), arrow.Arrow(2013, 5, 5, 12, 30, 46))
        assertEqual(arw.replace(quarters=0, microseconds=1), arrow.Arrow(2013, 5, 5, 12, 30, 45, 1))

    def test_replace_tzinfo(self):

        arw = arrow.Arrow.utcnow().to('US/Eastern')

        result = arw.replace(tzinfo=tz.gettz('US/Pacific'))

        assertEqual(result, arw.datetime.replace(tzinfo=tz.gettz('US/Pacific')))

    def test_replace_week(self):

        with assertRaises(AttributeError):
            arrow.Arrow.utcnow().replace(week=1)

    def test_replace_quarter(self):

        with assertRaises(AttributeError):
            arrow.Arrow.utcnow().replace(quarter=1)

    def test_replace_other_kwargs(self):

        with assertRaises(AttributeError):
            arrow.utcnow().replace(abc='def')

class ArrowShiftTests(Chai):

    def test_not_attr(self):

        with assertRaises(AttributeError):
            arrow.Arrow.utcnow().shift(abc=1)

    def test_shift(self):

        arw = arrow.Arrow(2013, 5, 5, 12, 30, 45)

        assertEqual(arw.shift(years=1), arrow.Arrow(2014, 5, 5, 12, 30, 45))
        assertEqual(arw.shift(quarters=1), arrow.Arrow(2013, 8, 5, 12, 30, 45))
        assertEqual(arw.shift(quarters=1, months=1), arrow.Arrow(2013, 9, 5, 12, 30, 45))
        assertEqual(arw.shift(months=1), arrow.Arrow(2013, 6, 5, 12, 30, 45))
        assertEqual(arw.shift(weeks=1), arrow.Arrow(2013, 5, 12, 12, 30, 45))
        assertEqual(arw.shift(days=1), arrow.Arrow(2013, 5, 6, 12, 30, 45))
        assertEqual(arw.shift(hours=1), arrow.Arrow(2013, 5, 5, 13, 30, 45))
        assertEqual(arw.shift(minutes=1), arrow.Arrow(2013, 5, 5, 12, 31, 45))
        assertEqual(arw.shift(seconds=1), arrow.Arrow(2013, 5, 5, 12, 30, 46))
        assertEqual(arw.shift(microseconds=1), arrow.Arrow(2013, 5, 5, 12, 30, 45, 1))

    def test_shift_negative(self):

        arw = arrow.Arrow(2013, 5, 5, 12, 30, 45)

        assertEqual(arw.shift(years=-1), arrow.Arrow(2012, 5, 5, 12, 30, 45))
        assertEqual(arw.shift(quarters=-1), arrow.Arrow(2013, 2, 5, 12, 30, 45))
        assertEqual(arw.shift(quarters=-1, months=-1), arrow.Arrow(2013, 1, 5, 12, 30, 45))
        assertEqual(arw.shift(months=-1), arrow.Arrow(2013, 4, 5, 12, 30, 45))
        assertEqual(arw.shift(weeks=-1), arrow.Arrow(2013, 4, 28, 12, 30, 45))
        assertEqual(arw.shift(days=-1), arrow.Arrow(2013, 5, 4, 12, 30, 45))
        assertEqual(arw.shift(hours=-1), arrow.Arrow(2013, 5, 5, 11, 30, 45))
        assertEqual(arw.shift(minutes=-1), arrow.Arrow(2013, 5, 5, 12, 29, 45))
        assertEqual(arw.shift(seconds=-1), arrow.Arrow(2013, 5, 5, 12, 30, 44))
        assertEqual(arw.shift(microseconds=-1), arrow.Arrow(2013, 5, 5, 12, 30, 44, 999999))

    def test_shift_quarters_bug(self):

        arw = arrow.Arrow(2013, 5, 5, 12, 30, 45)

        # The value of the last-read argument was used instead of the ``quarters`` argument.
        # Recall that the keyword argument dict, like all dicts, is unordered, so only certain
        # combinations of arguments would exhibit this.
        assertEqual(arw.replace(quarters=0, years=1), arrow.Arrow(2014, 5, 5, 12, 30, 45))
        assertEqual(arw.replace(quarters=0, months=1), arrow.Arrow(2013, 6, 5, 12, 30, 45))
        assertEqual(arw.replace(quarters=0, weeks=1), arrow.Arrow(2013, 5, 12, 12, 30, 45))
        assertEqual(arw.replace(quarters=0, days=1), arrow.Arrow(2013, 5, 6, 12, 30, 45))
        assertEqual(arw.replace(quarters=0, hours=1), arrow.Arrow(2013, 5, 5, 13, 30, 45))
        assertEqual(arw.replace(quarters=0, minutes=1), arrow.Arrow(2013, 5, 5, 12, 31, 45))
        assertEqual(arw.replace(quarters=0, seconds=1), arrow.Arrow(2013, 5, 5, 12, 30, 46))
        assertEqual(arw.replace(quarters=0, microseconds=1), arrow.Arrow(2013, 5, 5, 12, 30, 45, 1))

class ArrowRangeTests(Chai):

    def test_year(self):

        result = arrow.Arrow.range('year', datetime(2013, 1, 2, 3, 4, 5),
            datetime(2016, 4, 5, 6, 7, 8))

        assertEqual(result, [
            arrow.Arrow(2013, 1, 2, 3, 4, 5),
            arrow.Arrow(2014, 1, 2, 3, 4, 5),
            arrow.Arrow(2015, 1, 2, 3, 4, 5),
            arrow.Arrow(2016, 1, 2, 3, 4, 5),
        ])

    def test_quarter(self):

        result = arrow.Arrow.range('quarter', datetime(2013, 2, 3, 4, 5, 6),
            datetime(2013, 5, 6, 7, 8, 9))

        assertEqual(result, [
            arrow.Arrow(2013, 2, 3, 4, 5, 6),
            arrow.Arrow(2013, 5, 3, 4, 5, 6),
        ])

    def test_month(self):

        result = arrow.Arrow.range('month', datetime(2013, 2, 3, 4, 5, 6),
            datetime(2013, 5, 6, 7, 8, 9))

        assertEqual(result, [
            arrow.Arrow(2013, 2, 3, 4, 5, 6),
            arrow.Arrow(2013, 3, 3, 4, 5, 6),
            arrow.Arrow(2013, 4, 3, 4, 5, 6),
            arrow.Arrow(2013, 5, 3, 4, 5, 6),
        ])

    def test_week(self):

        result = arrow.Arrow.range('week', datetime(2013, 9, 1, 2, 3, 4),
            datetime(2013, 10, 1, 2, 3, 4))

        assertEqual(result, [
            arrow.Arrow(2013, 9, 1, 2, 3, 4),
            arrow.Arrow(2013, 9, 8, 2, 3, 4),
            arrow.Arrow(2013, 9, 15, 2, 3, 4),
            arrow.Arrow(2013, 9, 22, 2, 3, 4),
            arrow.Arrow(2013, 9, 29, 2, 3, 4)
        ])

    def test_day(self):

        result = arrow.Arrow.range('day', datetime(2013, 1, 2, 3, 4, 5),
            datetime(2013, 1, 5, 6, 7, 8))

        assertEqual(result, [
            arrow.Arrow(2013, 1, 2, 3, 4, 5),
            arrow.Arrow(2013, 1, 3, 3, 4, 5),
            arrow.Arrow(2013, 1, 4, 3, 4, 5),
            arrow.Arrow(2013, 1, 5, 3, 4, 5),
        ])

    def test_hour(self):

        result = arrow.Arrow.range('hour', datetime(2013, 1, 2, 3, 4, 5),
            datetime(2013, 1, 2, 6, 7, 8))

        assertEqual(result, [
            arrow.Arrow(2013, 1, 2, 3, 4, 5),
            arrow.Arrow(2013, 1, 2, 4, 4, 5),
            arrow.Arrow(2013, 1, 2, 5, 4, 5),
            arrow.Arrow(2013, 1, 2, 6, 4, 5),
        ])

        result = arrow.Arrow.range('hour', datetime(2013, 1, 2, 3, 4, 5),
            datetime(2013, 1, 2, 3, 4, 5))

        assertEqual(result, [
            arrow.Arrow(2013, 1, 2, 3, 4, 5),
        ])

    def test_minute(self):

        result = arrow.Arrow.range('minute', datetime(2013, 1, 2, 3, 4, 5),
            datetime(2013, 1, 2, 3, 7, 8))

        assertEqual(result, [
            arrow.Arrow(2013, 1, 2, 3, 4, 5),
            arrow.Arrow(2013, 1, 2, 3, 5, 5),
            arrow.Arrow(2013, 1, 2, 3, 6, 5),
            arrow.Arrow(2013, 1, 2, 3, 7, 5),
        ])

    def test_second(self):

        result = arrow.Arrow.range('second', datetime(2013, 1, 2, 3, 4, 5),
            datetime(2013, 1, 2, 3, 4, 8))

        assertEqual(result, [
            arrow.Arrow(2013, 1, 2, 3, 4, 5),
            arrow.Arrow(2013, 1, 2, 3, 4, 6),
            arrow.Arrow(2013, 1, 2, 3, 4, 7),
            arrow.Arrow(2013, 1, 2, 3, 4, 8),
        ])

    def test_arrow(self):

        result = arrow.Arrow.range('day', arrow.Arrow(2013, 1, 2, 3, 4, 5),
            arrow.Arrow(2013, 1, 5, 6, 7, 8))

        assertEqual(result, [
            arrow.Arrow(2013, 1, 2, 3, 4, 5),
            arrow.Arrow(2013, 1, 3, 3, 4, 5),
            arrow.Arrow(2013, 1, 4, 3, 4, 5),
            arrow.Arrow(2013, 1, 5, 3, 4, 5),
        ])

    def test_naive_tz(self):

        result = arrow.Arrow.range('year', datetime(2013, 1, 2, 3), datetime(2016, 4, 5, 6),
            'US/Pacific')

        [assertEqual(r.tzinfo, tz.gettz('US/Pacific')) for r in result]

    def test_aware_same_tz(self):

        result = arrow.Arrow.range('day',
            arrow.Arrow(2013, 1, 1, tzinfo=tz.gettz('US/Pacific')),
            arrow.Arrow(2013, 1, 3, tzinfo=tz.gettz('US/Pacific')))

        [assertEqual(r.tzinfo, tz.gettz('US/Pacific')) for r in result]

    def test_aware_different_tz(self):

        result = arrow.Arrow.range('day',
            datetime(2013, 1, 1, tzinfo=tz.gettz('US/Eastern')),
            datetime(2013, 1, 3, tzinfo=tz.gettz('US/Pacific')))

        [assertEqual(r.tzinfo, tz.gettz('US/Eastern')) for r in result]

    def test_aware_tz(self):

        result = arrow.Arrow.range('day',
            datetime(2013, 1, 1, tzinfo=tz.gettz('US/Eastern')),
            datetime(2013, 1, 3, tzinfo=tz.gettz('US/Pacific')),
            tz=tz.gettz('US/Central'))

        [assertEqual(r.tzinfo, tz.gettz('US/Central')) for r in result]

    def test_unsupported(self):

        with assertRaises(AttributeError):
            arrow.Arrow.range('abc', datetime.utcnow(), datetime.utcnow())


class ArrowSpanRangeTests(Chai):

    def test_year(self):

        result = arrow.Arrow.span_range('year', datetime(2013, 2, 1), datetime(2016, 3, 31))

        assertEqual(result, [
            (arrow.Arrow(2013, 1, 1), arrow.Arrow(2013, 12, 31, 23, 59, 59, 999999)),
            (arrow.Arrow(2014, 1, 1), arrow.Arrow(2014, 12, 31, 23, 59, 59, 999999)),
            (arrow.Arrow(2015, 1, 1), arrow.Arrow(2015, 12, 31, 23, 59, 59, 999999)),
            (arrow.Arrow(2016, 1, 1), arrow.Arrow(2016, 12, 31, 23, 59, 59, 999999)),
        ])

    def test_quarter(self):

        result = arrow.Arrow.span_range('quarter', datetime(2013, 2, 2), datetime(2013, 5, 15))

        assertEqual(result, [
            (arrow.Arrow(2013, 1, 1), arrow.Arrow(2013, 3, 31, 23, 59, 59, 999999)),
            (arrow.Arrow(2013, 4, 1), arrow.Arrow(2013, 6, 30, 23, 59, 59, 999999)),
        ])

    def test_month(self):

        result = arrow.Arrow.span_range('month', datetime(2013, 1, 2), datetime(2013, 4, 15))

        assertEqual(result, [
            (arrow.Arrow(2013, 1, 1), arrow.Arrow(2013, 1, 31, 23, 59, 59, 999999)),
            (arrow.Arrow(2013, 2, 1), arrow.Arrow(2013, 2, 28, 23, 59, 59, 999999)),
            (arrow.Arrow(2013, 3, 1), arrow.Arrow(2013, 3, 31, 23, 59, 59, 999999)),
            (arrow.Arrow(2013, 4, 1), arrow.Arrow(2013, 4, 30, 23, 59, 59, 999999)),
        ])

    def test_week(self):

        result = arrow.Arrow.span_range('week', datetime(2013, 2, 2), datetime(2013, 2, 28))

        assertEqual(result, [
            (arrow.Arrow(2013, 1, 28), arrow.Arrow(2013, 2, 3, 23, 59, 59, 999999)),
            (arrow.Arrow(2013, 2, 4), arrow.Arrow(2013, 2, 10, 23, 59, 59, 999999)),
            (arrow.Arrow(2013, 2, 11), arrow.Arrow(2013, 2, 17, 23, 59, 59, 999999)),
            (arrow.Arrow(2013, 2, 18), arrow.Arrow(2013, 2, 24, 23, 59, 59, 999999)),
            (arrow.Arrow(2013, 2, 25), arrow.Arrow(2013, 3, 3, 23, 59, 59, 999999)),
        ])


    def test_day(self):

        result = arrow.Arrow.span_range('day', datetime(2013, 1, 1, 12),
            datetime(2013, 1, 4, 12))

        assertEqual(result, [
            (arrow.Arrow(2013, 1, 1, 0), arrow.Arrow(2013, 1, 1, 23, 59, 59, 999999)),
            (arrow.Arrow(2013, 1, 2, 0), arrow.Arrow(2013, 1, 2, 23, 59, 59, 999999)),
            (arrow.Arrow(2013, 1, 3, 0), arrow.Arrow(2013, 1, 3, 23, 59, 59, 999999)),
            (arrow.Arrow(2013, 1, 4, 0), arrow.Arrow(2013, 1, 4, 23, 59, 59, 999999)),
        ])

    def test_hour(self):

        result = arrow.Arrow.span_range('hour', datetime(2013, 1, 1, 0, 30),
            datetime(2013, 1, 1, 3, 30))

        assertEqual(result, [
            (arrow.Arrow(2013, 1, 1, 0), arrow.Arrow(2013, 1, 1, 0, 59, 59, 999999)),
            (arrow.Arrow(2013, 1, 1, 1), arrow.Arrow(2013, 1, 1, 1, 59, 59, 999999)),
            (arrow.Arrow(2013, 1, 1, 2), arrow.Arrow(2013, 1, 1, 2, 59, 59, 999999)),
            (arrow.Arrow(2013, 1, 1, 3), arrow.Arrow(2013, 1, 1, 3, 59, 59, 999999)),
        ])

        result = arrow.Arrow.span_range('hour', datetime(2013, 1, 1, 3, 30),
            datetime(2013, 1, 1, 3, 30))

        assertEqual(result, [
            (arrow.Arrow(2013, 1, 1, 3), arrow.Arrow(2013, 1, 1, 3, 59, 59, 999999)),
        ])

    def test_minute(self):

        result = arrow.Arrow.span_range('minute', datetime(2013, 1, 1, 0, 0, 30),
            datetime(2013, 1, 1, 0, 3, 30))

        assertEqual(result, [
            (arrow.Arrow(2013, 1, 1, 0, 0), arrow.Arrow(2013, 1, 1, 0, 0, 59, 999999)),
            (arrow.Arrow(2013, 1, 1, 0, 1), arrow.Arrow(2013, 1, 1, 0, 1, 59, 999999)),
            (arrow.Arrow(2013, 1, 1, 0, 2), arrow.Arrow(2013, 1, 1, 0, 2, 59, 999999)),
            (arrow.Arrow(2013, 1, 1, 0, 3), arrow.Arrow(2013, 1, 1, 0, 3, 59, 999999)),
        ])

    def test_second(self):

        result = arrow.Arrow.span_range('second', datetime(2013, 1, 1),
            datetime(2013, 1, 1, 0, 0, 3))

        assertEqual(result, [
            (arrow.Arrow(2013, 1, 1, 0, 0, 0), arrow.Arrow(2013, 1, 1, 0, 0, 0, 999999)),
            (arrow.Arrow(2013, 1, 1, 0, 0, 1), arrow.Arrow(2013, 1, 1, 0, 0, 1, 999999)),
            (arrow.Arrow(2013, 1, 1, 0, 0, 2), arrow.Arrow(2013, 1, 1, 0, 0, 2, 999999)),
            (arrow.Arrow(2013, 1, 1, 0, 0, 3), arrow.Arrow(2013, 1, 1, 0, 0, 3, 999999)),
        ])

    def test_naive_tz(self):

        tzinfo = tz.gettz('US/Pacific')

        result = arrow.Arrow.span_range('hour', datetime(2013, 1, 1, 0),
            datetime(2013, 1, 1, 3, 59), 'US/Pacific')

        for f, c in result:
            assertEqual(f.tzinfo, tzinfo)
            assertEqual(c.tzinfo, tzinfo)

    def test_aware_same_tz(self):

        tzinfo = tz.gettz('US/Pacific')

        result = arrow.Arrow.span_range('hour', datetime(2013, 1, 1, 0, tzinfo=tzinfo),
            datetime(2013, 1, 1, 2, 59, tzinfo=tzinfo))

        for f, c in result:
            assertEqual(f.tzinfo, tzinfo)
            assertEqual(c.tzinfo, tzinfo)

    def test_aware_different_tz(self):

        tzinfo1 = tz.gettz('US/Pacific')
        tzinfo2 = tz.gettz('US/Eastern')

        result = arrow.Arrow.span_range('hour', datetime(2013, 1, 1, 0, tzinfo=tzinfo1),
            datetime(2013, 1, 1, 2, 59, tzinfo=tzinfo2))

        for f, c in result:
            assertEqual(f.tzinfo, tzinfo1)
            assertEqual(c.tzinfo, tzinfo1)

    def test_aware_tz(self):

        result = arrow.Arrow.span_range('hour',
            datetime(2013, 1, 1, 0, tzinfo=tz.gettz('US/Eastern')),
            datetime(2013, 1, 1, 2, 59, tzinfo=tz.gettz('US/Eastern')),
            tz='US/Central')

        for f, c in result:
            assertEqual(f.tzinfo, tz.gettz('US/Central'))
            assertEqual(c.tzinfo, tz.gettz('US/Central'))


class ArrowSpanTests(Chai):

    def setUp(self):
        super(ArrowSpanTests, self).setUp()

        self.datetime = datetime(2013, 2, 15, 3, 41, 22, 8923)
        self.arrow = arrow.Arrow.fromdatetime(self.datetime)

    def test_span_attribute(self):

        with assertRaises(AttributeError):
            self.arrow.span('span')

    def test_span_year(self):

        floor, ceil = self.arrow.span('year')

        assertEqual(floor, datetime(2013, 1, 1, tzinfo=tz.tzutc()))
        assertEqual(ceil, datetime(2013, 12, 31, 23, 59, 59, 999999, tzinfo=tz.tzutc()))


    def test_span_quarter(self):

        floor, ceil = self.arrow.span('quarter')

        assertEqual(floor, datetime(2013, 1, 1, tzinfo=tz.tzutc()))
        assertEqual(ceil, datetime(2013, 3, 31, 23, 59, 59, 999999, tzinfo=tz.tzutc()))


    def test_span_quarter_count(self):

        floor, ceil = self.arrow.span('quarter', 2)

        assertEqual(floor, datetime(2013, 1, 1, tzinfo=tz.tzutc()))
        assertEqual(ceil, datetime(2013, 6, 30, 23, 59, 59, 999999, tzinfo=tz.tzutc()))


    def test_span_year_count(self):

        floor, ceil = self.arrow.span('year', 2)

        assertEqual(floor, datetime(2013, 1, 1, tzinfo=tz.tzutc()))
        assertEqual(ceil, datetime(2014, 12, 31, 23, 59, 59, 999999, tzinfo=tz.tzutc()))


    def test_span_month(self):

        floor, ceil = self.arrow.span('month')

        assertEqual(floor, datetime(2013, 2, 1, tzinfo=tz.tzutc()))
        assertEqual(ceil, datetime(2013, 2, 28, 23, 59, 59, 999999, tzinfo=tz.tzutc()))

    def test_span_week(self):

        floor, ceil = self.arrow.span('week')

        assertEqual(floor, datetime(2013, 2, 11, tzinfo=tz.tzutc()))
        assertEqual(ceil, datetime(2013, 2, 17, 23, 59, 59, 999999, tzinfo=tz.tzutc()))

    def test_span_day(self):

        floor, ceil = self.arrow.span('day')

        assertEqual(floor, datetime(2013, 2, 15, tzinfo=tz.tzutc()))
        assertEqual(ceil, datetime(2013, 2, 15, 23, 59, 59, 999999, tzinfo=tz.tzutc()))

    def test_span_hour(self):

        floor, ceil = self.arrow.span('hour')

        assertEqual(floor, datetime(2013, 2, 15, 3, tzinfo=tz.tzutc()))
        assertEqual(ceil, datetime(2013, 2, 15, 3, 59, 59, 999999, tzinfo=tz.tzutc()))

    def test_span_minute(self):

        floor, ceil = self.arrow.span('minute')

        assertEqual(floor, datetime(2013, 2, 15, 3, 41, tzinfo=tz.tzutc()))
        assertEqual(ceil, datetime(2013, 2, 15, 3, 41, 59, 999999, tzinfo=tz.tzutc()))

    def test_span_second(self):

        floor, ceil = self.arrow.span('second')

        assertEqual(floor, datetime(2013, 2, 15, 3, 41, 22, tzinfo=tz.tzutc()))
        assertEqual(ceil, datetime(2013, 2, 15, 3, 41, 22, 999999, tzinfo=tz.tzutc()))

    def test_span_microsecond(self):

        floor, ceil = self.arrow.span('microsecond')

        assertEqual(floor, datetime(2013, 2, 15, 3, 41, 22, 8923, tzinfo=tz.tzutc()))
        assertEqual(ceil, datetime(2013, 2, 15, 3, 41, 22, 8923, tzinfo=tz.tzutc()))

    def test_floor(self):

        floor, ceil = self.arrow.span('month')

        assertEqual(floor, self.arrow.floor('month'))
        assertEqual(ceil, self.arrow.ceil('month'))


class ArrowHumanizeTests(Chai):

    def setUp(self):
        super(ArrowHumanizeTests, self).setUp()

        self.datetime = datetime(2013, 1, 1)
        self.now = arrow.Arrow.utcnow()

    def test_seconds(self):

        later = self.now.shift(seconds=10)

        assertEqual(self.now.humanize(later), 'seconds ago')
        assertEqual(later.humanize(self.now), 'in seconds')

        assertEqual(self.now.humanize(later, only_distance=True), 'seconds')
        assertEqual(later.humanize(self.now, only_distance=True), 'seconds')

    def test_minute(self):

        later = self.now.shift(minutes=1)

        assertEqual(self.now.humanize(later), 'a minute ago')
        assertEqual(later.humanize(self.now), 'in a minute')

        assertEqual(self.now.humanize(later, only_distance=True), 'a minute')
        assertEqual(later.humanize(self.now, only_distance=True), 'a minute')


    def test_minutes(self):

        later = self.now.shift(minutes=2)

        assertEqual(self.now.humanize(later), '2 minutes ago')
        assertEqual(later.humanize(self.now), 'in 2 minutes')

        assertEqual(self.now.humanize(later, only_distance=True), '2 minutes')
        assertEqual(later.humanize(self.now, only_distance=True), '2 minutes')

    def test_hour(self):

        later = self.now.shift(hours=1)

        assertEqual(self.now.humanize(later), 'an hour ago')
        assertEqual(later.humanize(self.now), 'in an hour')

        assertEqual(self.now.humanize(later, only_distance=True), 'an hour')
        assertEqual(later.humanize(self.now, only_distance=True), 'an hour')

    def test_hours(self):

        later = self.now.shift(hours=2)

        assertEqual(self.now.humanize(later), '2 hours ago')
        assertEqual(later.humanize(self.now), 'in 2 hours')

        assertEqual(self.now.humanize(later, only_distance=True), '2 hours')
        assertEqual(later.humanize(self.now, only_distance=True), '2 hours')

    def test_day(self):

        later = self.now.shift(days=1)

        assertEqual(self.now.humanize(later), 'a day ago')
        assertEqual(later.humanize(self.now), 'in a day')

        assertEqual(self.now.humanize(later, only_distance=True), 'a day')
        assertEqual(later.humanize(self.now, only_distance=True), 'a day')

    def test_days(self):

        later = self.now.shift(days=2)

        assertEqual(self.now.humanize(later), '2 days ago')
        assertEqual(later.humanize(self.now), 'in 2 days')

        assertEqual(self.now.humanize(later, only_distance=True), '2 days')
        assertEqual(later.humanize(self.now, only_distance=True), '2 days')

    def test_month(self):

        later = self.now.shift(months=1)

        assertEqual(self.now.humanize(later), 'a month ago')
        assertEqual(later.humanize(self.now), 'in a month')

        assertEqual(self.now.humanize(later, only_distance=True), 'a month')
        assertEqual(later.humanize(self.now, only_distance=True), 'a month')

    def test_months(self):

        later = self.now.shift(months=2)
        earlier = self.now.shift(months=-2)

        assertEqual(earlier.humanize(self.now), '2 months ago')
        assertEqual(later.humanize(self.now), 'in 2 months')

        assertEqual(self.now.humanize(later, only_distance=True), '2 months')
        assertEqual(later.humanize(self.now, only_distance=True), '2 months')

    def test_year(self):

        later = self.now.shift(years=1)

        assertEqual(self.now.humanize(later), 'a year ago')
        assertEqual(later.humanize(self.now), 'in a year')

        assertEqual(self.now.humanize(later, only_distance=True), 'a year')
        assertEqual(later.humanize(self.now, only_distance=True), 'a year')

    def test_years(self):

        later = self.now.shift(years=2)

        assertEqual(self.now.humanize(later), '2 years ago')
        assertEqual(later.humanize(self.now), 'in 2 years')

        assertEqual(self.now.humanize(later, only_distance=True), '2 years')
        assertEqual(later.humanize(self.now, only_distance=True), '2 years')

        arw = arrow.Arrow(2014, 7, 2)

        result = arw.humanize(self.datetime)

        assertEqual(result, 'in 2 years')

    def test_arrow(self):

        arw = arrow.Arrow.fromdatetime(self.datetime)

        result = arw.humanize(arrow.Arrow.fromdatetime(self.datetime))

        assertEqual(result, 'just now')

    def test_datetime_tzinfo(self):

        arw = arrow.Arrow.fromdatetime(self.datetime)

        result = arw.humanize(self.datetime.replace(tzinfo=tz.tzutc()))

        assertEqual(result, 'just now')

    def test_other(self):

        arw = arrow.Arrow.fromdatetime(self.datetime)

        with assertRaises(TypeError):
            arw.humanize(object())

    def test_invalid_locale(self):

        arw = arrow.Arrow.fromdatetime(self.datetime)

        with assertRaises(ValueError):
            arw.humanize(locale='klingon')

    def test_none(self):

        arw = arrow.Arrow.utcnow()

        result = arw.humanize()

        assertEqual(result, 'just now')


class ArrowHumanizeTestsWithLocale(Chai):

    def setUp(self):
        super(ArrowHumanizeTestsWithLocale, self).setUp()

        self.datetime = datetime(2013, 1, 1)

    def test_now(self):

        arw = arrow.Arrow(2013, 1, 1, 0, 0, 0)

        result = arw.humanize(self.datetime, locale='ru')

        assertEqual(result, 'сейчас')

    def test_seconds(self):
        arw = arrow.Arrow(2013, 1, 1, 0, 0, 44)

        result = arw.humanize(self.datetime, locale='ru')

        assertEqual(result, 'через несколько секунд')

    def test_years(self):

        arw = arrow.Arrow(2011, 7, 2)

        result = arw.humanize(self.datetime, locale='ru')

        assertEqual(result, '2 года назад')

class ArrowDehumanizeTests(Chai):

    def setUp(self):
        super(ArrowDehumanizeTests, self).setup()
        self.datetime = datetime(2013,1,1)
        self.datetime2012 = datetime(2012,1,1)

    def test_seconds(self):
        arw = arrow.Arrow.fromdatetime(self.datetime)

        result = arw.dehumanize('1 second later')
        assertEqual(result, arrow.Arrow(2013,1,1,0,0,1))

        result = arw.dehumanize('1 second ago')
        assertEqual(result, arrow.Arrow(2012,12,31,23,59,59))

        result = arw.dehumanize('2 seconds later')
        assertEqual(result, arrow.Arrow(2013,1,1,0,0,2))

        result = arw.dehumanize('2 seconds ago')
        assertEqual(result, arrow.Arrow(2012,12,31,23,59,58))

    def test_minutes(self):
        arw = arrow.Arrow.fromdatetime(self.datetime)

        result = arw.dehumanize('1 minute later')
        assertEqual(result, arrow.Arrow(2013,1,1,0,1,0))

        result = arw.dehumanize('1 minute ago')
        assertEqual(result, arrow.Arrow(2012,12,31,23,59,0))

    def test_hours(self):
        arw = arrow.Arrow.fromdatetime(self.datetime)

        result = arw.dehumanize('1 hour later')
        assertEqual(result, arrow.Arrow(2013,1,1,1,0,0))

        result = arw.dehumanize('1 hour ago')
        assertEqual(result, arrow.Arrow(2012,12,31,23,0,0))

    def test_days(self):
        arw = arrow.Arrow.fromdatetime(self.datetime)

        result = arw.dehumanize('1 day later')
        assertEqual(result, arrow.Arrow(2013,1,2,0,0,0))

        result = arw.dehumanize('1 day ago')
        assertEqual(result, arrow.Arrow(2012,12,31,0,0,0))

    def test_weeks(self):
        arw = arrow.Arrow.fromdatetime(self.datetime)

        result = arw.dehumanize('1 week later')
        assertEqual(result, arrow.Arrow(2013,1,8,0,0,0))

        result = arw.dehumanize('1 week ago')
        assertEqual(result, arrow.Arrow(2012,12,25,0,0,0))

    def test_months(self):
        arw = arrow.Arrow.fromdatetime(self.datetime)

        result = arw.dehumanize('1 month later')
        assertEqual(result, arrow.Arrow(2013,2,1,0,0,0))

        result = arw.dehumanize('1 month ago')
        assertEqual(result, arrow.Arrow(2012,12,1,0,0,0))

    def test_years(self):
        arw = arrow.Arrow.fromdatetime(self.datetime)

        result = arw.dehumanize('1 year later')
        assertEqual(result, arrow.Arrow(2014,1,1,0,0,0))

        result = arw.dehumanize('1 year ago')
        assertEqual(result, arrow.Arrow(2012,1,1,0,0,0))

    def test_additional(self):
        arw = arrow.Arrow.fromdatetime(self.datetime)
        arw2012 = arrow.Arrow.fromdatetime(self.datetime2012)

        result = arw.dehumanize('3 year 12 months 365 days later')
        assertEqual(result, arrow.Arrow(2018,1,1,0,0,0))

        result = arw2012.dehumanize('3 year 12 months 365 days later')
        assertEqual(result, arrow.Arrow(2016,12,31,0,0,0))

        result = arw.dehumanize('3 year 12 months 365 days ago')
        assertEqual(result, arrow.Arrow(2008,1,2,0,0,0))

        result = arw2012.dehumanize('3 year 12 months 365 days ago')
        assertEqual(result, arrow.Arrow(2007,1,1,0,0,0))

    def test_errors(self):
        arw = arrow.Arrow.fromdatetime(self.datetime)

        test = True
        try:
            result = arw.dehumanize('nothing')
        except:
            test = False

        assertEqual(test, False)

        test = True
        try:
            result = arw.dehumanize('3 weeks 1 day blahblah')
        except:
            test = False
        assertEqual(test, False)

        test = True
        try:
            result = arw.dehumanize('3 ago')
        except:
            test = False
        assertEqual(test, False)

        test = True
        try:
            result = arw.dehumanize('3 blahblah ago')
        except:
            test = False
        assertEqual(test, False)

class ArrowUtilTests(Chai):

    def test_get_datetime(self):

        get_datetime = arrow.Arrow._get_datetime

        arw = arrow.Arrow.utcnow()
        dt = datetime.utcnow()
        timestamp = time.time()

        assertEqual(get_datetime(arw), arw.datetime)
        assertEqual(get_datetime(dt), dt)
        assertEqual(get_datetime(timestamp), arrow.Arrow.utcfromtimestamp(timestamp).datetime)

        with assertRaises(ValueError) as raise_ctx:
            get_datetime('abc')
        assertFalse('{0}' in str(raise_ctx.exception))

    def test_get_tzinfo(self):

        get_tzinfo = arrow.Arrow._get_tzinfo

        with assertRaises(ValueError) as raise_ctx:
            get_tzinfo('abc')
        assertFalse('{0}' in str(raise_ctx.exception))

    def test_get_timestamp_from_input(self):

        assertEqual(arrow.Arrow._get_timestamp_from_input(123), 123)
        assertEqual(arrow.Arrow._get_timestamp_from_input(123.4), 123.4)
        assertEqual(arrow.Arrow._get_timestamp_from_input('123'), 123.0)
        assertEqual(arrow.Arrow._get_timestamp_from_input('123.4'), 123.4)

        with assertRaises(ValueError):
            arrow.Arrow._get_timestamp_from_input('abc')

    def test_get_iteration_params(self):

        assertEqual(arrow.Arrow._get_iteration_params('end', None), ('end', sys.maxsize))
        assertEqual(arrow.Arrow._get_iteration_params(None, 100), (arrow.Arrow.max, 100))
        assertEqual(arrow.Arrow._get_iteration_params(100, 120), (100, 120))

        with assertRaises(Exception):
            arrow.Arrow._get_iteration_params(None, None)
