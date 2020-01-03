# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import calendar
import pickle
import sys
import time
from datetime import date, datetime, timedelta

import pytz
import simplejson as json
from chai import Chai
from dateutil import tz
from dateutil.relativedelta import FR, MO, SA, SU, TH, TU, WE
from mock import patch

from arrow import arrow, util


def assertDtEqual(dt1, dt2, within=10):
    assertEqual(dt1.tzinfo, dt2.tzinfo)  # noqa: F821
    assertTrue(abs(util.total_seconds(dt1 - dt2)) < within)  # noqa: F821


class ArrowInitTests(Chai):
    def test_init_bad_input(self):

        with self.assertRaises(TypeError):
            arrow.Arrow(2013)

        with self.assertRaises(TypeError):
            arrow.Arrow(2013, 2)

        with self.assertRaises(ValueError):
            arrow.Arrow(2013, 2, 2, 12, 30, 45, 9999999)

    def test_init(self):

        result = arrow.Arrow(2013, 2, 2)
        self.expected = datetime(2013, 2, 2, tzinfo=tz.tzutc())
        self.assertEqual(result._datetime, self.expected)

        result = arrow.Arrow(2013, 2, 2, 12)
        self.expected = datetime(2013, 2, 2, 12, tzinfo=tz.tzutc())
        self.assertEqual(result._datetime, self.expected)

        result = arrow.Arrow(2013, 2, 2, 12, 30)
        self.expected = datetime(2013, 2, 2, 12, 30, tzinfo=tz.tzutc())
        self.assertEqual(result._datetime, self.expected)

        result = arrow.Arrow(2013, 2, 2, 12, 30, 45)
        self.expected = datetime(2013, 2, 2, 12, 30, 45, tzinfo=tz.tzutc())
        self.assertEqual(result._datetime, self.expected)

        result = arrow.Arrow(2013, 2, 2, 12, 30, 45, 999999)
        self.expected = datetime(2013, 2, 2, 12, 30, 45, 999999, tzinfo=tz.tzutc())
        self.assertEqual(result._datetime, self.expected)

        result = arrow.Arrow(
            2013, 2, 2, 12, 30, 45, 999999, tzinfo=tz.gettz("Europe/Paris")
        )
        self.expected = datetime(
            2013, 2, 2, 12, 30, 45, 999999, tzinfo=tz.gettz("Europe/Paris")
        )
        self.assertEqual(result._datetime, self.expected)

    # regression tests for issue #626
    def test_init_pytz_timezone(self):

        result = arrow.Arrow(
            2013, 2, 2, 12, 30, 45, 999999, tzinfo=pytz.timezone("Europe/Paris")
        )
        self.expected = datetime(
            2013, 2, 2, 12, 30, 45, 999999, tzinfo=tz.gettz("Europe/Paris")
        )
        self.assertEqual(result._datetime, self.expected)
        assertDtEqual(result._datetime, self.expected, 1)


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

        result = arrow.Arrow.fromtimestamp(timestamp, tzinfo=tz.gettz("Europe/Paris"))
        assertDtEqual(
            result._datetime,
            datetime.fromtimestamp(timestamp, tz.gettz("Europe/Paris")),
        )

        result = arrow.Arrow.fromtimestamp(timestamp, tzinfo="Europe/Paris")
        assertDtEqual(
            result._datetime,
            datetime.fromtimestamp(timestamp, tz.gettz("Europe/Paris")),
        )

        with self.assertRaises(ValueError):
            arrow.Arrow.fromtimestamp("invalid timestamp")

    def test_utcfromtimestamp(self):

        timestamp = time.time()

        result = arrow.Arrow.utcfromtimestamp(timestamp)
        assertDtEqual(result._datetime, datetime.utcnow().replace(tzinfo=tz.tzutc()))

        with self.assertRaises(ValueError):
            arrow.Arrow.utcfromtimestamp("invalid timestamp")

    def test_fromdatetime(self):

        dt = datetime(2013, 2, 3, 12, 30, 45, 1)

        result = arrow.Arrow.fromdatetime(dt)

        self.assertEqual(result._datetime, dt.replace(tzinfo=tz.tzutc()))

    def test_fromdatetime_dt_tzinfo(self):

        dt = datetime(2013, 2, 3, 12, 30, 45, 1, tzinfo=tz.gettz("US/Pacific"))

        result = arrow.Arrow.fromdatetime(dt)

        self.assertEqual(result._datetime, dt.replace(tzinfo=tz.gettz("US/Pacific")))

    def test_fromdatetime_tzinfo_arg(self):

        dt = datetime(2013, 2, 3, 12, 30, 45, 1)

        result = arrow.Arrow.fromdatetime(dt, tz.gettz("US/Pacific"))

        self.assertEqual(result._datetime, dt.replace(tzinfo=tz.gettz("US/Pacific")))

    def test_fromdate(self):

        dt = date(2013, 2, 3)

        result = arrow.Arrow.fromdate(dt, tz.gettz("US/Pacific"))

        self.assertEqual(
            result._datetime, datetime(2013, 2, 3, tzinfo=tz.gettz("US/Pacific"))
        )

    def test_strptime(self):

        formatted = datetime(2013, 2, 3, 12, 30, 45).strftime("%Y-%m-%d %H:%M:%S")

        result = arrow.Arrow.strptime(formatted, "%Y-%m-%d %H:%M:%S")
        self.assertEqual(
            result._datetime, datetime(2013, 2, 3, 12, 30, 45, tzinfo=tz.tzutc())
        )

        result = arrow.Arrow.strptime(
            formatted, "%Y-%m-%d %H:%M:%S", tzinfo=tz.gettz("Europe/Paris")
        )
        self.assertEqual(
            result._datetime,
            datetime(2013, 2, 3, 12, 30, 45, tzinfo=tz.gettz("Europe/Paris")),
        )


class ArrowRepresentationTests(Chai):
    def setUp(self):
        super(ArrowRepresentationTests, self).setUp()

        self.arrow = arrow.Arrow(2013, 2, 3, 12, 30, 45, 1)

    def test_repr(self):

        result = self.arrow.__repr__()

        self.assertEqual(
            result, "<Arrow [{}]>".format(self.arrow._datetime.isoformat())
        )

    def test_str(self):

        result = self.arrow.__str__()

        self.assertEqual(result, self.arrow._datetime.isoformat())

    def test_hash(self):

        result = self.arrow.__hash__()

        self.assertEqual(result, self.arrow._datetime.__hash__())

    def test_format(self):

        result = "{:YYYY-MM-DD}".format(self.arrow)

        self.assertEqual(result, "2013-02-03")

    def test_bare_format(self):

        result = self.arrow.format()

        self.assertEqual(result, "2013-02-03 12:30:45+00:00")

    def test_format_no_format_string(self):

        result = "{}".format(self.arrow)

        self.assertEqual(result, str(self.arrow))

    def test_clone(self):

        result = self.arrow.clone()

        self.assertTrue(result is not self.arrow)
        self.assertEqual(result._datetime, self.arrow._datetime)


class ArrowAttributeTests(Chai):
    def setUp(self):
        super(ArrowAttributeTests, self).setUp()

        self.arrow = arrow.Arrow(2013, 1, 1)

    def test_getattr_base(self):

        with self.assertRaises(AttributeError):
            self.arrow.prop

    def test_getattr_week(self):

        self.assertEqual(self.arrow.week, 1)

    def test_getattr_quarter(self):
        # start dates
        q1 = arrow.Arrow(2013, 1, 1)
        q2 = arrow.Arrow(2013, 4, 1)
        q3 = arrow.Arrow(2013, 8, 1)
        q4 = arrow.Arrow(2013, 10, 1)
        self.assertEqual(q1.quarter, 1)
        self.assertEqual(q2.quarter, 2)
        self.assertEqual(q3.quarter, 3)
        self.assertEqual(q4.quarter, 4)

        # end dates
        q1 = arrow.Arrow(2013, 3, 31)
        q2 = arrow.Arrow(2013, 6, 30)
        q3 = arrow.Arrow(2013, 9, 30)
        q4 = arrow.Arrow(2013, 12, 31)
        self.assertEqual(q1.quarter, 1)
        self.assertEqual(q2.quarter, 2)
        self.assertEqual(q3.quarter, 3)
        self.assertEqual(q4.quarter, 4)

    def test_getattr_dt_value(self):

        self.assertEqual(self.arrow.year, 2013)

    def test_tzinfo(self):

        self.arrow.tzinfo = tz.gettz("PST")
        self.assertEqual(self.arrow.tzinfo, tz.gettz("PST"))

    def test_naive(self):

        self.assertEqual(self.arrow.naive, self.arrow._datetime.replace(tzinfo=None))

    def test_timestamp(self):

        self.assertEqual(
            self.arrow.timestamp, calendar.timegm(self.arrow._datetime.utctimetuple())
        )

    def test_float_timestamp(self):

        result = self.arrow.float_timestamp - self.arrow.timestamp

        self.assertEqual(result, self.arrow.microsecond)


class ArrowComparisonTests(Chai):
    def setUp(self):
        super(ArrowComparisonTests, self).setUp()

        self.arrow = arrow.Arrow.utcnow()

    def test_eq(self):

        self.assertTrue(self.arrow == self.arrow)
        self.assertTrue(self.arrow == self.arrow.datetime)
        self.assertFalse(self.arrow == "abc")

    def test_ne(self):

        self.assertFalse(self.arrow != self.arrow)
        self.assertFalse(self.arrow != self.arrow.datetime)
        self.assertTrue(self.arrow != "abc")

    def test_gt(self):

        arrow_cmp = self.arrow.shift(minutes=1)

        self.assertFalse(self.arrow > self.arrow)
        self.assertFalse(self.arrow > self.arrow.datetime)

        with self.assertRaises(TypeError):
            self.arrow > "abc"

        self.assertTrue(self.arrow < arrow_cmp)
        self.assertTrue(self.arrow < arrow_cmp.datetime)

    def test_ge(self):

        with self.assertRaises(TypeError):
            self.arrow >= "abc"

        self.assertTrue(self.arrow >= self.arrow)
        self.assertTrue(self.arrow >= self.arrow.datetime)

    def test_lt(self):

        arrow_cmp = self.arrow.shift(minutes=1)

        self.assertFalse(self.arrow < self.arrow)
        self.assertFalse(self.arrow < self.arrow.datetime)

        with self.assertRaises(TypeError):
            self.arrow < "abc"

        self.assertTrue(self.arrow < arrow_cmp)
        self.assertTrue(self.arrow < arrow_cmp.datetime)

    def test_le(self):

        with self.assertRaises(TypeError):
            self.arrow <= "abc"

        self.assertTrue(self.arrow <= self.arrow)
        self.assertTrue(self.arrow <= self.arrow.datetime)


class ArrowMathTests(Chai):
    def setUp(self):
        super(ArrowMathTests, self).setUp()

        self.arrow = arrow.Arrow(2013, 1, 1)

    def test_add_timedelta(self):

        result = self.arrow.__add__(timedelta(days=1))

        self.assertEqual(result._datetime, datetime(2013, 1, 2, tzinfo=tz.tzutc()))

    def test_add_other(self):

        with self.assertRaises(TypeError):
            self.arrow + 1

    def test_radd(self):

        result = self.arrow.__radd__(timedelta(days=1))

        self.assertEqual(result._datetime, datetime(2013, 1, 2, tzinfo=tz.tzutc()))

    def test_sub_timedelta(self):

        result = self.arrow.__sub__(timedelta(days=1))

        self.assertEqual(result._datetime, datetime(2012, 12, 31, tzinfo=tz.tzutc()))

    def test_sub_datetime(self):

        result = self.arrow.__sub__(datetime(2012, 12, 21, tzinfo=tz.tzutc()))

        self.assertEqual(result, timedelta(days=11))

    def test_sub_arrow(self):

        result = self.arrow.__sub__(arrow.Arrow(2012, 12, 21, tzinfo=tz.tzutc()))

        self.assertEqual(result, timedelta(days=11))

    def test_sub_other(self):

        with self.assertRaises(TypeError):
            self.arrow - object()

    def test_rsub_datetime(self):

        result = self.arrow.__rsub__(datetime(2012, 12, 21, tzinfo=tz.tzutc()))

        self.assertEqual(result, timedelta(days=-11))

    def test_rsub_other(self):

        with self.assertRaises(TypeError):
            timedelta(days=1) - self.arrow


class ArrowDatetimeInterfaceTests(Chai):
    def setUp(self):
        super(ArrowDatetimeInterfaceTests, self).setUp()

        self.arrow = arrow.Arrow.utcnow()

    def test_date(self):

        result = self.arrow.date()

        self.assertEqual(result, self.arrow._datetime.date())

    def test_time(self):

        result = self.arrow.time()

        self.assertEqual(result, self.arrow._datetime.time())

    def test_timetz(self):

        result = self.arrow.timetz()

        self.assertEqual(result, self.arrow._datetime.timetz())

    def test_astimezone(self):

        other_tz = tz.gettz("US/Pacific")

        result = self.arrow.astimezone(other_tz)

        self.assertEqual(result, self.arrow._datetime.astimezone(other_tz))

    def test_utcoffset(self):

        result = self.arrow.utcoffset()

        self.assertEqual(result, self.arrow._datetime.utcoffset())

    def test_dst(self):

        result = self.arrow.dst()

        self.assertEqual(result, self.arrow._datetime.dst())

    def test_timetuple(self):

        result = self.arrow.timetuple()

        self.assertEqual(result, self.arrow._datetime.timetuple())

    def test_utctimetuple(self):

        result = self.arrow.utctimetuple()

        self.assertEqual(result, self.arrow._datetime.utctimetuple())

    def test_toordinal(self):

        result = self.arrow.toordinal()

        self.assertEqual(result, self.arrow._datetime.toordinal())

    def test_weekday(self):

        result = self.arrow.weekday()

        self.assertEqual(result, self.arrow._datetime.weekday())

    def test_isoweekday(self):

        result = self.arrow.isoweekday()

        self.assertEqual(result, self.arrow._datetime.isoweekday())

    def test_isocalendar(self):

        result = self.arrow.isocalendar()

        self.assertEqual(result, self.arrow._datetime.isocalendar())

    def test_isoformat(self):

        result = self.arrow.isoformat()

        self.assertEqual(result, self.arrow._datetime.isoformat())

    def test_simplejson(self):

        result = json.dumps({"v": self.arrow.for_json()}, for_json=True)

        self.assertEqual(json.loads(result)["v"], self.arrow._datetime.isoformat())

    def test_ctime(self):

        result = self.arrow.ctime()

        self.assertEqual(result, self.arrow._datetime.ctime())

    def test_strftime(self):

        result = self.arrow.strftime("%Y")

        self.assertEqual(result, self.arrow._datetime.strftime("%Y"))


class ArrowFalsePositiveDstTests(Chai):
    """These tests relate to issues #376 and #551.
    The key points in both issues are that arrow will assign a UTC timezone if none is provided and
    .to() will change other attributes to be correct whereas .replace() only changes the specified attribute.

    Issue 376
    >>> arrow.get('2016-11-06').to('America/New_York').ceil('day')
    < Arrow [2016-11-05T23:59:59.999999-04:00] >

    Issue 551
    >>> just_before = arrow.get('2018-11-04T01:59:59.999999')
    >>> just_before
    2018-11-04T01:59:59.999999+00:00
    >>> just_after = just_before.shift(microseconds=1)
    >>> just_after
    2018-11-04T02:00:00+00:00
    >>> just_before_eastern = just_before.replace(tzinfo='US/Eastern')
    >>> just_before_eastern
    2018-11-04T01:59:59.999999-04:00
    >>> just_after_eastern = just_after.replace(tzinfo='US/Eastern')
    >>> just_after_eastern
    2018-11-04T02:00:00-05:00
    """

    def setUp(self):

        super(ArrowFalsePositiveDstTests, self).setUp()
        self.before_1 = arrow.Arrow(
            2016, 11, 6, 3, 59, tzinfo=tz.gettz("America/New_York")
        )
        self.before_2 = arrow.Arrow(2016, 11, 6, tzinfo=tz.gettz("America/New_York"))
        self.after_1 = arrow.Arrow(2016, 11, 6, 4, tzinfo=tz.gettz("America/New_York"))
        self.after_2 = arrow.Arrow(
            2016, 11, 6, 23, 59, tzinfo=tz.gettz("America/New_York")
        )
        self.before_3 = arrow.Arrow(
            2018, 11, 4, 3, 59, tzinfo=tz.gettz("America/New_York")
        )
        self.before_4 = arrow.Arrow(2018, 11, 4, tzinfo=tz.gettz("America/New_York"))
        self.after_3 = arrow.Arrow(2018, 11, 4, 4, tzinfo=tz.gettz("America/New_York"))
        self.after_4 = arrow.Arrow(
            2018, 11, 4, 23, 59, tzinfo=tz.gettz("America/New_York")
        )

    def test_dst(self):

        self.assertEqual(self.before_1.day, self.before_2.day)
        self.assertEqual(self.after_1.day, self.after_2.day)
        self.assertEqual(self.before_3.day, self.before_4.day)
        self.assertEqual(self.after_3.day, self.after_4.day)


class ArrowConversionTests(Chai):
    def test_to(self):

        dt_from = datetime.now()
        arrow_from = arrow.Arrow.fromdatetime(dt_from, tz.gettz("US/Pacific"))

        self.expected = dt_from.replace(tzinfo=tz.gettz("US/Pacific")).astimezone(
            tz.tzutc()
        )

        self.assertEqual(arrow_from.to("UTC").datetime, self.expected)
        self.assertEqual(arrow_from.to(tz.tzutc()).datetime, self.expected)


class ArrowPicklingTests(Chai):
    def test_pickle_and_unpickle(self):

        dt = arrow.Arrow.utcnow()

        pickled = pickle.dumps(dt)

        unpickled = pickle.loads(pickled)

        self.assertEqual(unpickled, dt)


class ArrowReplaceTests(Chai):
    def test_not_attr(self):

        with self.assertRaises(AttributeError):
            arrow.Arrow.utcnow().replace(abc=1)

    def test_replace(self):

        arw = arrow.Arrow(2013, 5, 5, 12, 30, 45)

        self.assertEqual(arw.replace(year=2012), arrow.Arrow(2012, 5, 5, 12, 30, 45))
        self.assertEqual(arw.replace(month=1), arrow.Arrow(2013, 1, 5, 12, 30, 45))
        self.assertEqual(arw.replace(day=1), arrow.Arrow(2013, 5, 1, 12, 30, 45))
        self.assertEqual(arw.replace(hour=1), arrow.Arrow(2013, 5, 5, 1, 30, 45))
        self.assertEqual(arw.replace(minute=1), arrow.Arrow(2013, 5, 5, 12, 1, 45))
        self.assertEqual(arw.replace(second=1), arrow.Arrow(2013, 5, 5, 12, 30, 1))

    def test_replace_tzinfo(self):

        arw = arrow.Arrow.utcnow().to("US/Eastern")

        result = arw.replace(tzinfo=tz.gettz("US/Pacific"))

        self.assertEqual(result, arw.datetime.replace(tzinfo=tz.gettz("US/Pacific")))

    def test_replace_week(self):

        with self.assertRaises(AttributeError):
            arrow.Arrow.utcnow().replace(week=1)

    def test_replace_quarter(self):

        with self.assertRaises(AttributeError):
            arrow.Arrow.utcnow().replace(quarter=1)

    def test_replace_other_kwargs(self):

        with self.assertRaises(AttributeError):
            arrow.utcnow().replace(abc="def")


class ArrowShiftTests(Chai):
    def test_not_attr(self):

        now = arrow.Arrow.utcnow()

        with self.assertRaises(AttributeError):
            now.shift(abc=1)

        with self.assertRaises(AttributeError):
            now.shift(week=1)

    def test_shift(self):

        arw = arrow.Arrow(2013, 5, 5, 12, 30, 45)

        self.assertEqual(arw.shift(years=1), arrow.Arrow(2014, 5, 5, 12, 30, 45))
        self.assertEqual(arw.shift(quarters=1), arrow.Arrow(2013, 8, 5, 12, 30, 45))
        self.assertEqual(
            arw.shift(quarters=1, months=1), arrow.Arrow(2013, 9, 5, 12, 30, 45)
        )
        self.assertEqual(arw.shift(months=1), arrow.Arrow(2013, 6, 5, 12, 30, 45))
        self.assertEqual(arw.shift(weeks=1), arrow.Arrow(2013, 5, 12, 12, 30, 45))
        self.assertEqual(arw.shift(days=1), arrow.Arrow(2013, 5, 6, 12, 30, 45))
        self.assertEqual(arw.shift(hours=1), arrow.Arrow(2013, 5, 5, 13, 30, 45))
        self.assertEqual(arw.shift(minutes=1), arrow.Arrow(2013, 5, 5, 12, 31, 45))
        self.assertEqual(arw.shift(seconds=1), arrow.Arrow(2013, 5, 5, 12, 30, 46))
        self.assertEqual(
            arw.shift(microseconds=1), arrow.Arrow(2013, 5, 5, 12, 30, 45, 1)
        )

        # Remember: Python's weekday 0 is Monday
        self.assertEqual(arw.shift(weekday=0), arrow.Arrow(2013, 5, 6, 12, 30, 45))
        self.assertEqual(arw.shift(weekday=1), arrow.Arrow(2013, 5, 7, 12, 30, 45))
        self.assertEqual(arw.shift(weekday=2), arrow.Arrow(2013, 5, 8, 12, 30, 45))
        self.assertEqual(arw.shift(weekday=3), arrow.Arrow(2013, 5, 9, 12, 30, 45))
        self.assertEqual(arw.shift(weekday=4), arrow.Arrow(2013, 5, 10, 12, 30, 45))
        self.assertEqual(arw.shift(weekday=5), arrow.Arrow(2013, 5, 11, 12, 30, 45))
        self.assertEqual(arw.shift(weekday=6), arw)

        with self.assertRaises(IndexError):
            arw.shift(weekday=7)

        # Use dateutil.relativedelta's convenient day instances
        self.assertEqual(arw.shift(weekday=MO), arrow.Arrow(2013, 5, 6, 12, 30, 45))
        self.assertEqual(arw.shift(weekday=MO(0)), arrow.Arrow(2013, 5, 6, 12, 30, 45))
        self.assertEqual(arw.shift(weekday=MO(1)), arrow.Arrow(2013, 5, 6, 12, 30, 45))
        self.assertEqual(arw.shift(weekday=MO(2)), arrow.Arrow(2013, 5, 13, 12, 30, 45))
        self.assertEqual(arw.shift(weekday=TU), arrow.Arrow(2013, 5, 7, 12, 30, 45))
        self.assertEqual(arw.shift(weekday=TU(0)), arrow.Arrow(2013, 5, 7, 12, 30, 45))
        self.assertEqual(arw.shift(weekday=TU(1)), arrow.Arrow(2013, 5, 7, 12, 30, 45))
        self.assertEqual(arw.shift(weekday=TU(2)), arrow.Arrow(2013, 5, 14, 12, 30, 45))
        self.assertEqual(arw.shift(weekday=WE), arrow.Arrow(2013, 5, 8, 12, 30, 45))
        self.assertEqual(arw.shift(weekday=WE(0)), arrow.Arrow(2013, 5, 8, 12, 30, 45))
        self.assertEqual(arw.shift(weekday=WE(1)), arrow.Arrow(2013, 5, 8, 12, 30, 45))
        self.assertEqual(arw.shift(weekday=WE(2)), arrow.Arrow(2013, 5, 15, 12, 30, 45))
        self.assertEqual(arw.shift(weekday=TH), arrow.Arrow(2013, 5, 9, 12, 30, 45))
        self.assertEqual(arw.shift(weekday=TH(0)), arrow.Arrow(2013, 5, 9, 12, 30, 45))
        self.assertEqual(arw.shift(weekday=TH(1)), arrow.Arrow(2013, 5, 9, 12, 30, 45))
        self.assertEqual(arw.shift(weekday=TH(2)), arrow.Arrow(2013, 5, 16, 12, 30, 45))
        self.assertEqual(arw.shift(weekday=FR), arrow.Arrow(2013, 5, 10, 12, 30, 45))
        self.assertEqual(arw.shift(weekday=FR(0)), arrow.Arrow(2013, 5, 10, 12, 30, 45))
        self.assertEqual(arw.shift(weekday=FR(1)), arrow.Arrow(2013, 5, 10, 12, 30, 45))
        self.assertEqual(arw.shift(weekday=FR(2)), arrow.Arrow(2013, 5, 17, 12, 30, 45))
        self.assertEqual(arw.shift(weekday=SA), arrow.Arrow(2013, 5, 11, 12, 30, 45))
        self.assertEqual(arw.shift(weekday=SA(0)), arrow.Arrow(2013, 5, 11, 12, 30, 45))
        self.assertEqual(arw.shift(weekday=SA(1)), arrow.Arrow(2013, 5, 11, 12, 30, 45))
        self.assertEqual(arw.shift(weekday=SA(2)), arrow.Arrow(2013, 5, 18, 12, 30, 45))
        self.assertEqual(arw.shift(weekday=SU), arw)
        self.assertEqual(arw.shift(weekday=SU(0)), arw)
        self.assertEqual(arw.shift(weekday=SU(1)), arw)
        self.assertEqual(arw.shift(weekday=SU(2)), arrow.Arrow(2013, 5, 12, 12, 30, 45))

    def test_shift_negative(self):

        arw = arrow.Arrow(2013, 5, 5, 12, 30, 45)

        self.assertEqual(arw.shift(years=-1), arrow.Arrow(2012, 5, 5, 12, 30, 45))
        self.assertEqual(arw.shift(quarters=-1), arrow.Arrow(2013, 2, 5, 12, 30, 45))
        self.assertEqual(
            arw.shift(quarters=-1, months=-1), arrow.Arrow(2013, 1, 5, 12, 30, 45)
        )
        self.assertEqual(arw.shift(months=-1), arrow.Arrow(2013, 4, 5, 12, 30, 45))
        self.assertEqual(arw.shift(weeks=-1), arrow.Arrow(2013, 4, 28, 12, 30, 45))
        self.assertEqual(arw.shift(days=-1), arrow.Arrow(2013, 5, 4, 12, 30, 45))
        self.assertEqual(arw.shift(hours=-1), arrow.Arrow(2013, 5, 5, 11, 30, 45))
        self.assertEqual(arw.shift(minutes=-1), arrow.Arrow(2013, 5, 5, 12, 29, 45))
        self.assertEqual(arw.shift(seconds=-1), arrow.Arrow(2013, 5, 5, 12, 30, 44))
        self.assertEqual(
            arw.shift(microseconds=-1), arrow.Arrow(2013, 5, 5, 12, 30, 44, 999999)
        )

        # Not sure how practical these negative weekdays are
        self.assertEqual(arw.shift(weekday=-1), arw.shift(weekday=SU))
        self.assertEqual(arw.shift(weekday=-2), arw.shift(weekday=SA))
        self.assertEqual(arw.shift(weekday=-3), arw.shift(weekday=FR))
        self.assertEqual(arw.shift(weekday=-4), arw.shift(weekday=TH))
        self.assertEqual(arw.shift(weekday=-5), arw.shift(weekday=WE))
        self.assertEqual(arw.shift(weekday=-6), arw.shift(weekday=TU))
        self.assertEqual(arw.shift(weekday=-7), arw.shift(weekday=MO))

        with self.assertRaises(IndexError):
            arw.shift(weekday=-8)

        self.assertEqual(
            arw.shift(weekday=MO(-1)), arrow.Arrow(2013, 4, 29, 12, 30, 45)
        )
        self.assertEqual(
            arw.shift(weekday=TU(-1)), arrow.Arrow(2013, 4, 30, 12, 30, 45)
        )
        self.assertEqual(arw.shift(weekday=WE(-1)), arrow.Arrow(2013, 5, 1, 12, 30, 45))
        self.assertEqual(arw.shift(weekday=TH(-1)), arrow.Arrow(2013, 5, 2, 12, 30, 45))
        self.assertEqual(arw.shift(weekday=FR(-1)), arrow.Arrow(2013, 5, 3, 12, 30, 45))
        self.assertEqual(arw.shift(weekday=SA(-1)), arrow.Arrow(2013, 5, 4, 12, 30, 45))
        self.assertEqual(arw.shift(weekday=SU(-1)), arw)
        self.assertEqual(
            arw.shift(weekday=SU(-2)), arrow.Arrow(2013, 4, 28, 12, 30, 45)
        )

    def test_shift_quarters_bug(self):

        arw = arrow.Arrow(2013, 5, 5, 12, 30, 45)

        # The value of the last-read argument was used instead of the ``quarters`` argument.
        # Recall that the keyword argument dict, like all dicts, is unordered, so only certain
        # combinations of arguments would exhibit this.
        self.assertEqual(
            arw.shift(quarters=0, years=1), arrow.Arrow(2014, 5, 5, 12, 30, 45)
        )
        self.assertEqual(
            arw.shift(quarters=0, months=1), arrow.Arrow(2013, 6, 5, 12, 30, 45)
        )
        self.assertEqual(
            arw.shift(quarters=0, weeks=1), arrow.Arrow(2013, 5, 12, 12, 30, 45)
        )
        self.assertEqual(
            arw.shift(quarters=0, days=1), arrow.Arrow(2013, 5, 6, 12, 30, 45)
        )
        self.assertEqual(
            arw.shift(quarters=0, hours=1), arrow.Arrow(2013, 5, 5, 13, 30, 45)
        )
        self.assertEqual(
            arw.shift(quarters=0, minutes=1), arrow.Arrow(2013, 5, 5, 12, 31, 45)
        )
        self.assertEqual(
            arw.shift(quarters=0, seconds=1), arrow.Arrow(2013, 5, 5, 12, 30, 46)
        )
        self.assertEqual(
            arw.shift(quarters=0, microseconds=1),
            arrow.Arrow(2013, 5, 5, 12, 30, 45, 1),
        )


class ArrowRangeTests(Chai):
    def test_year(self):

        result = list(
            arrow.Arrow.range(
                "year", datetime(2013, 1, 2, 3, 4, 5), datetime(2016, 4, 5, 6, 7, 8)
            )
        )

        self.assertEqual(
            result,
            [
                arrow.Arrow(2013, 1, 2, 3, 4, 5),
                arrow.Arrow(2014, 1, 2, 3, 4, 5),
                arrow.Arrow(2015, 1, 2, 3, 4, 5),
                arrow.Arrow(2016, 1, 2, 3, 4, 5),
            ],
        )

    def test_quarter(self):

        result = list(
            arrow.Arrow.range(
                "quarter", datetime(2013, 2, 3, 4, 5, 6), datetime(2013, 5, 6, 7, 8, 9)
            )
        )

        self.assertEqual(
            result, [arrow.Arrow(2013, 2, 3, 4, 5, 6), arrow.Arrow(2013, 5, 3, 4, 5, 6)]
        )

    def test_month(self):

        result = list(
            arrow.Arrow.range(
                "month", datetime(2013, 2, 3, 4, 5, 6), datetime(2013, 5, 6, 7, 8, 9)
            )
        )

        self.assertEqual(
            result,
            [
                arrow.Arrow(2013, 2, 3, 4, 5, 6),
                arrow.Arrow(2013, 3, 3, 4, 5, 6),
                arrow.Arrow(2013, 4, 3, 4, 5, 6),
                arrow.Arrow(2013, 5, 3, 4, 5, 6),
            ],
        )

    def test_week(self):

        result = list(
            arrow.Arrow.range(
                "week", datetime(2013, 9, 1, 2, 3, 4), datetime(2013, 10, 1, 2, 3, 4)
            )
        )

        self.assertEqual(
            result,
            [
                arrow.Arrow(2013, 9, 1, 2, 3, 4),
                arrow.Arrow(2013, 9, 8, 2, 3, 4),
                arrow.Arrow(2013, 9, 15, 2, 3, 4),
                arrow.Arrow(2013, 9, 22, 2, 3, 4),
                arrow.Arrow(2013, 9, 29, 2, 3, 4),
            ],
        )

    def test_day(self):

        result = list(
            arrow.Arrow.range(
                "day", datetime(2013, 1, 2, 3, 4, 5), datetime(2013, 1, 5, 6, 7, 8)
            )
        )

        self.assertEqual(
            result,
            [
                arrow.Arrow(2013, 1, 2, 3, 4, 5),
                arrow.Arrow(2013, 1, 3, 3, 4, 5),
                arrow.Arrow(2013, 1, 4, 3, 4, 5),
                arrow.Arrow(2013, 1, 5, 3, 4, 5),
            ],
        )

    def test_hour(self):

        result = list(
            arrow.Arrow.range(
                "hour", datetime(2013, 1, 2, 3, 4, 5), datetime(2013, 1, 2, 6, 7, 8)
            )
        )

        self.assertEqual(
            result,
            [
                arrow.Arrow(2013, 1, 2, 3, 4, 5),
                arrow.Arrow(2013, 1, 2, 4, 4, 5),
                arrow.Arrow(2013, 1, 2, 5, 4, 5),
                arrow.Arrow(2013, 1, 2, 6, 4, 5),
            ],
        )

        result = list(
            arrow.Arrow.range(
                "hour", datetime(2013, 1, 2, 3, 4, 5), datetime(2013, 1, 2, 3, 4, 5)
            )
        )

        self.assertEqual(result, [arrow.Arrow(2013, 1, 2, 3, 4, 5)])

    def test_minute(self):

        result = list(
            arrow.Arrow.range(
                "minute", datetime(2013, 1, 2, 3, 4, 5), datetime(2013, 1, 2, 3, 7, 8)
            )
        )

        self.assertEqual(
            result,
            [
                arrow.Arrow(2013, 1, 2, 3, 4, 5),
                arrow.Arrow(2013, 1, 2, 3, 5, 5),
                arrow.Arrow(2013, 1, 2, 3, 6, 5),
                arrow.Arrow(2013, 1, 2, 3, 7, 5),
            ],
        )

    def test_second(self):

        result = list(
            arrow.Arrow.range(
                "second", datetime(2013, 1, 2, 3, 4, 5), datetime(2013, 1, 2, 3, 4, 8)
            )
        )

        self.assertEqual(
            result,
            [
                arrow.Arrow(2013, 1, 2, 3, 4, 5),
                arrow.Arrow(2013, 1, 2, 3, 4, 6),
                arrow.Arrow(2013, 1, 2, 3, 4, 7),
                arrow.Arrow(2013, 1, 2, 3, 4, 8),
            ],
        )

    def test_arrow(self):

        result = list(
            arrow.Arrow.range(
                "day",
                arrow.Arrow(2013, 1, 2, 3, 4, 5),
                arrow.Arrow(2013, 1, 5, 6, 7, 8),
            )
        )

        self.assertEqual(
            result,
            [
                arrow.Arrow(2013, 1, 2, 3, 4, 5),
                arrow.Arrow(2013, 1, 3, 3, 4, 5),
                arrow.Arrow(2013, 1, 4, 3, 4, 5),
                arrow.Arrow(2013, 1, 5, 3, 4, 5),
            ],
        )

    def test_naive_tz(self):

        result = arrow.Arrow.range(
            "year", datetime(2013, 1, 2, 3), datetime(2016, 4, 5, 6), "US/Pacific"
        )

        [self.assertEqual(r.tzinfo, tz.gettz("US/Pacific")) for r in result]

    def test_aware_same_tz(self):

        result = arrow.Arrow.range(
            "day",
            arrow.Arrow(2013, 1, 1, tzinfo=tz.gettz("US/Pacific")),
            arrow.Arrow(2013, 1, 3, tzinfo=tz.gettz("US/Pacific")),
        )

        [self.assertEqual(r.tzinfo, tz.gettz("US/Pacific")) for r in result]

    def test_aware_different_tz(self):

        result = arrow.Arrow.range(
            "day",
            datetime(2013, 1, 1, tzinfo=tz.gettz("US/Eastern")),
            datetime(2013, 1, 3, tzinfo=tz.gettz("US/Pacific")),
        )

        [self.assertEqual(r.tzinfo, tz.gettz("US/Eastern")) for r in result]

    def test_aware_tz(self):

        result = arrow.Arrow.range(
            "day",
            datetime(2013, 1, 1, tzinfo=tz.gettz("US/Eastern")),
            datetime(2013, 1, 3, tzinfo=tz.gettz("US/Pacific")),
            tz=tz.gettz("US/Central"),
        )

        [self.assertEqual(r.tzinfo, tz.gettz("US/Central")) for r in result]

    def test_unsupported(self):

        with self.assertRaises(AttributeError):
            next(arrow.Arrow.range("abc", datetime.utcnow(), datetime.utcnow()))


class ArrowSpanRangeTests(Chai):
    def test_year(self):

        result = list(
            arrow.Arrow.span_range("year", datetime(2013, 2, 1), datetime(2016, 3, 31))
        )

        self.assertEqual(
            result,
            [
                (
                    arrow.Arrow(2013, 1, 1),
                    arrow.Arrow(2013, 12, 31, 23, 59, 59, 999999),
                ),
                (
                    arrow.Arrow(2014, 1, 1),
                    arrow.Arrow(2014, 12, 31, 23, 59, 59, 999999),
                ),
                (
                    arrow.Arrow(2015, 1, 1),
                    arrow.Arrow(2015, 12, 31, 23, 59, 59, 999999),
                ),
                (
                    arrow.Arrow(2016, 1, 1),
                    arrow.Arrow(2016, 12, 31, 23, 59, 59, 999999),
                ),
            ],
        )

    def test_quarter(self):

        result = list(
            arrow.Arrow.span_range(
                "quarter", datetime(2013, 2, 2), datetime(2013, 5, 15)
            )
        )

        self.assertEqual(
            result,
            [
                (arrow.Arrow(2013, 1, 1), arrow.Arrow(2013, 3, 31, 23, 59, 59, 999999)),
                (arrow.Arrow(2013, 4, 1), arrow.Arrow(2013, 6, 30, 23, 59, 59, 999999)),
            ],
        )

    def test_month(self):

        result = list(
            arrow.Arrow.span_range("month", datetime(2013, 1, 2), datetime(2013, 4, 15))
        )

        self.assertEqual(
            result,
            [
                (arrow.Arrow(2013, 1, 1), arrow.Arrow(2013, 1, 31, 23, 59, 59, 999999)),
                (arrow.Arrow(2013, 2, 1), arrow.Arrow(2013, 2, 28, 23, 59, 59, 999999)),
                (arrow.Arrow(2013, 3, 1), arrow.Arrow(2013, 3, 31, 23, 59, 59, 999999)),
                (arrow.Arrow(2013, 4, 1), arrow.Arrow(2013, 4, 30, 23, 59, 59, 999999)),
            ],
        )

    def test_week(self):

        result = list(
            arrow.Arrow.span_range("week", datetime(2013, 2, 2), datetime(2013, 2, 28))
        )

        self.assertEqual(
            result,
            [
                (arrow.Arrow(2013, 1, 28), arrow.Arrow(2013, 2, 3, 23, 59, 59, 999999)),
                (arrow.Arrow(2013, 2, 4), arrow.Arrow(2013, 2, 10, 23, 59, 59, 999999)),
                (
                    arrow.Arrow(2013, 2, 11),
                    arrow.Arrow(2013, 2, 17, 23, 59, 59, 999999),
                ),
                (
                    arrow.Arrow(2013, 2, 18),
                    arrow.Arrow(2013, 2, 24, 23, 59, 59, 999999),
                ),
                (arrow.Arrow(2013, 2, 25), arrow.Arrow(2013, 3, 3, 23, 59, 59, 999999)),
            ],
        )

    def test_day(self):

        result = list(
            arrow.Arrow.span_range(
                "day", datetime(2013, 1, 1, 12), datetime(2013, 1, 4, 12)
            )
        )

        self.assertEqual(
            result,
            [
                (
                    arrow.Arrow(2013, 1, 1, 0),
                    arrow.Arrow(2013, 1, 1, 23, 59, 59, 999999),
                ),
                (
                    arrow.Arrow(2013, 1, 2, 0),
                    arrow.Arrow(2013, 1, 2, 23, 59, 59, 999999),
                ),
                (
                    arrow.Arrow(2013, 1, 3, 0),
                    arrow.Arrow(2013, 1, 3, 23, 59, 59, 999999),
                ),
                (
                    arrow.Arrow(2013, 1, 4, 0),
                    arrow.Arrow(2013, 1, 4, 23, 59, 59, 999999),
                ),
            ],
        )

    def test_days(self):

        result = list(
            arrow.Arrow.span_range(
                "days", datetime(2013, 1, 1, 12), datetime(2013, 1, 4, 12)
            )
        )

        self.assertEqual(
            result,
            [
                (
                    arrow.Arrow(2013, 1, 1, 0),
                    arrow.Arrow(2013, 1, 1, 23, 59, 59, 999999),
                ),
                (
                    arrow.Arrow(2013, 1, 2, 0),
                    arrow.Arrow(2013, 1, 2, 23, 59, 59, 999999),
                ),
                (
                    arrow.Arrow(2013, 1, 3, 0),
                    arrow.Arrow(2013, 1, 3, 23, 59, 59, 999999),
                ),
                (
                    arrow.Arrow(2013, 1, 4, 0),
                    arrow.Arrow(2013, 1, 4, 23, 59, 59, 999999),
                ),
            ],
        )

    def test_hour(self):

        result = list(
            arrow.Arrow.span_range(
                "hour", datetime(2013, 1, 1, 0, 30), datetime(2013, 1, 1, 3, 30)
            )
        )

        self.assertEqual(
            result,
            [
                (
                    arrow.Arrow(2013, 1, 1, 0),
                    arrow.Arrow(2013, 1, 1, 0, 59, 59, 999999),
                ),
                (
                    arrow.Arrow(2013, 1, 1, 1),
                    arrow.Arrow(2013, 1, 1, 1, 59, 59, 999999),
                ),
                (
                    arrow.Arrow(2013, 1, 1, 2),
                    arrow.Arrow(2013, 1, 1, 2, 59, 59, 999999),
                ),
                (
                    arrow.Arrow(2013, 1, 1, 3),
                    arrow.Arrow(2013, 1, 1, 3, 59, 59, 999999),
                ),
            ],
        )

        result = list(
            arrow.Arrow.span_range(
                "hour", datetime(2013, 1, 1, 3, 30), datetime(2013, 1, 1, 3, 30)
            )
        )

        self.assertEqual(
            result,
            [(arrow.Arrow(2013, 1, 1, 3), arrow.Arrow(2013, 1, 1, 3, 59, 59, 999999))],
        )

    def test_minute(self):

        result = list(
            arrow.Arrow.span_range(
                "minute", datetime(2013, 1, 1, 0, 0, 30), datetime(2013, 1, 1, 0, 3, 30)
            )
        )

        self.assertEqual(
            result,
            [
                (
                    arrow.Arrow(2013, 1, 1, 0, 0),
                    arrow.Arrow(2013, 1, 1, 0, 0, 59, 999999),
                ),
                (
                    arrow.Arrow(2013, 1, 1, 0, 1),
                    arrow.Arrow(2013, 1, 1, 0, 1, 59, 999999),
                ),
                (
                    arrow.Arrow(2013, 1, 1, 0, 2),
                    arrow.Arrow(2013, 1, 1, 0, 2, 59, 999999),
                ),
                (
                    arrow.Arrow(2013, 1, 1, 0, 3),
                    arrow.Arrow(2013, 1, 1, 0, 3, 59, 999999),
                ),
            ],
        )

    def test_second(self):

        result = list(
            arrow.Arrow.span_range(
                "second", datetime(2013, 1, 1), datetime(2013, 1, 1, 0, 0, 3)
            )
        )

        self.assertEqual(
            result,
            [
                (
                    arrow.Arrow(2013, 1, 1, 0, 0, 0),
                    arrow.Arrow(2013, 1, 1, 0, 0, 0, 999999),
                ),
                (
                    arrow.Arrow(2013, 1, 1, 0, 0, 1),
                    arrow.Arrow(2013, 1, 1, 0, 0, 1, 999999),
                ),
                (
                    arrow.Arrow(2013, 1, 1, 0, 0, 2),
                    arrow.Arrow(2013, 1, 1, 0, 0, 2, 999999),
                ),
                (
                    arrow.Arrow(2013, 1, 1, 0, 0, 3),
                    arrow.Arrow(2013, 1, 1, 0, 0, 3, 999999),
                ),
            ],
        )

    def test_naive_tz(self):

        tzinfo = tz.gettz("US/Pacific")

        result = arrow.Arrow.span_range(
            "hour", datetime(2013, 1, 1, 0), datetime(2013, 1, 1, 3, 59), "US/Pacific"
        )

        for f, c in result:
            self.assertEqual(f.tzinfo, tzinfo)
            self.assertEqual(c.tzinfo, tzinfo)

    def test_aware_same_tz(self):

        tzinfo = tz.gettz("US/Pacific")

        result = arrow.Arrow.span_range(
            "hour",
            datetime(2013, 1, 1, 0, tzinfo=tzinfo),
            datetime(2013, 1, 1, 2, 59, tzinfo=tzinfo),
        )

        for f, c in result:
            self.assertEqual(f.tzinfo, tzinfo)
            self.assertEqual(c.tzinfo, tzinfo)

    def test_aware_different_tz(self):

        tzinfo1 = tz.gettz("US/Pacific")
        tzinfo2 = tz.gettz("US/Eastern")

        result = arrow.Arrow.span_range(
            "hour",
            datetime(2013, 1, 1, 0, tzinfo=tzinfo1),
            datetime(2013, 1, 1, 2, 59, tzinfo=tzinfo2),
        )

        for f, c in result:
            self.assertEqual(f.tzinfo, tzinfo1)
            self.assertEqual(c.tzinfo, tzinfo1)

    def test_aware_tz(self):

        result = arrow.Arrow.span_range(
            "hour",
            datetime(2013, 1, 1, 0, tzinfo=tz.gettz("US/Eastern")),
            datetime(2013, 1, 1, 2, 59, tzinfo=tz.gettz("US/Eastern")),
            tz="US/Central",
        )

        for f, c in result:
            self.assertEqual(f.tzinfo, tz.gettz("US/Central"))
            self.assertEqual(c.tzinfo, tz.gettz("US/Central"))

    def test_bounds_param_is_passed(self):

        result = list(
            arrow.Arrow.span_range(
                "quarter", datetime(2013, 2, 2), datetime(2013, 5, 15), bounds="[]"
            )
        )

        self.assertEqual(
            result,
            [
                (arrow.Arrow(2013, 1, 1), arrow.Arrow(2013, 4, 1)),
                (arrow.Arrow(2013, 4, 1), arrow.Arrow(2013, 7, 1)),
            ],
        )


class ArrowIntervalTests(Chai):
    def test_incorrect_input(self):
        correct = True
        try:
            list(
                arrow.Arrow.interval(
                    "month", datetime(2013, 1, 2), datetime(2013, 4, 15), 0
                )
            )
        except:  # noqa: E722
            correct = False

        self.assertEqual(correct, False)

    def test_correct(self):
        result = list(
            arrow.Arrow.interval(
                "hour", datetime(2013, 5, 5, 12, 30), datetime(2013, 5, 5, 17, 15), 2
            )
        )

        self.assertEqual(
            result,
            [
                (
                    arrow.Arrow(2013, 5, 5, 12),
                    arrow.Arrow(2013, 5, 5, 13, 59, 59, 999999),
                ),
                (
                    arrow.Arrow(2013, 5, 5, 14),
                    arrow.Arrow(2013, 5, 5, 15, 59, 59, 999999),
                ),
                (
                    arrow.Arrow(2013, 5, 5, 16),
                    arrow.Arrow(2013, 5, 5, 17, 59, 59, 999999),
                ),
            ],
        )

    def test_bounds_param_is_passed(self):
        result = list(
            arrow.Arrow.interval(
                "hour",
                datetime(2013, 5, 5, 12, 30),
                datetime(2013, 5, 5, 17, 15),
                2,
                bounds="[]",
            )
        )

        self.assertEqual(
            result,
            [
                (arrow.Arrow(2013, 5, 5, 12), arrow.Arrow(2013, 5, 5, 14)),
                (arrow.Arrow(2013, 5, 5, 14), arrow.Arrow(2013, 5, 5, 16)),
                (arrow.Arrow(2013, 5, 5, 16), arrow.Arrow(2013, 5, 5, 18)),
            ],
        )


class ArrowSpanTests(Chai):
    def setUp(self):
        super(ArrowSpanTests, self).setUp()

        self.datetime = datetime(2013, 2, 15, 3, 41, 22, 8923)
        self.arrow = arrow.Arrow.fromdatetime(self.datetime)

    def test_span_attribute(self):

        with self.assertRaises(AttributeError):
            self.arrow.span("span")

    def test_span_year(self):

        floor, ceil = self.arrow.span("year")

        self.assertEqual(floor, datetime(2013, 1, 1, tzinfo=tz.tzutc()))
        self.assertEqual(
            ceil, datetime(2013, 12, 31, 23, 59, 59, 999999, tzinfo=tz.tzutc())
        )

    def test_span_quarter(self):

        floor, ceil = self.arrow.span("quarter")

        self.assertEqual(floor, datetime(2013, 1, 1, tzinfo=tz.tzutc()))
        self.assertEqual(
            ceil, datetime(2013, 3, 31, 23, 59, 59, 999999, tzinfo=tz.tzutc())
        )

    def test_span_quarter_count(self):

        floor, ceil = self.arrow.span("quarter", 2)

        self.assertEqual(floor, datetime(2013, 1, 1, tzinfo=tz.tzutc()))
        self.assertEqual(
            ceil, datetime(2013, 6, 30, 23, 59, 59, 999999, tzinfo=tz.tzutc())
        )

    def test_span_year_count(self):

        floor, ceil = self.arrow.span("year", 2)

        self.assertEqual(floor, datetime(2013, 1, 1, tzinfo=tz.tzutc()))
        self.assertEqual(
            ceil, datetime(2014, 12, 31, 23, 59, 59, 999999, tzinfo=tz.tzutc())
        )

    def test_span_month(self):

        floor, ceil = self.arrow.span("month")

        self.assertEqual(floor, datetime(2013, 2, 1, tzinfo=tz.tzutc()))
        self.assertEqual(
            ceil, datetime(2013, 2, 28, 23, 59, 59, 999999, tzinfo=tz.tzutc())
        )

    def test_span_week(self):

        floor, ceil = self.arrow.span("week")

        self.assertEqual(floor, datetime(2013, 2, 11, tzinfo=tz.tzutc()))
        self.assertEqual(
            ceil, datetime(2013, 2, 17, 23, 59, 59, 999999, tzinfo=tz.tzutc())
        )

    def test_span_day(self):

        floor, ceil = self.arrow.span("day")

        self.assertEqual(floor, datetime(2013, 2, 15, tzinfo=tz.tzutc()))
        self.assertEqual(
            ceil, datetime(2013, 2, 15, 23, 59, 59, 999999, tzinfo=tz.tzutc())
        )

    def test_span_hour(self):

        floor, ceil = self.arrow.span("hour")

        self.assertEqual(floor, datetime(2013, 2, 15, 3, tzinfo=tz.tzutc()))
        self.assertEqual(
            ceil, datetime(2013, 2, 15, 3, 59, 59, 999999, tzinfo=tz.tzutc())
        )

    def test_span_minute(self):

        floor, ceil = self.arrow.span("minute")

        self.assertEqual(floor, datetime(2013, 2, 15, 3, 41, tzinfo=tz.tzutc()))
        self.assertEqual(
            ceil, datetime(2013, 2, 15, 3, 41, 59, 999999, tzinfo=tz.tzutc())
        )

    def test_span_second(self):

        floor, ceil = self.arrow.span("second")

        self.assertEqual(floor, datetime(2013, 2, 15, 3, 41, 22, tzinfo=tz.tzutc()))
        self.assertEqual(
            ceil, datetime(2013, 2, 15, 3, 41, 22, 999999, tzinfo=tz.tzutc())
        )

    def test_span_microsecond(self):

        floor, ceil = self.arrow.span("microsecond")

        self.assertEqual(
            floor, datetime(2013, 2, 15, 3, 41, 22, 8923, tzinfo=tz.tzutc())
        )
        self.assertEqual(
            ceil, datetime(2013, 2, 15, 3, 41, 22, 8923, tzinfo=tz.tzutc())
        )

    def test_floor(self):

        floor, ceil = self.arrow.span("month")

        self.assertEqual(floor, self.arrow.floor("month"))
        self.assertEqual(ceil, self.arrow.ceil("month"))

    def test_span_inclusive_inclusive(self):

        floor, ceil = self.arrow.span("hour", bounds="[]")

        self.assertEqual(floor, datetime(2013, 2, 15, 3, tzinfo=tz.tzutc()))
        self.assertEqual(ceil, datetime(2013, 2, 15, 4, tzinfo=tz.tzutc()))

    def test_span_exclusive_inclusive(self):

        floor, ceil = self.arrow.span("hour", bounds="(]")

        self.assertEqual(floor, datetime(2013, 2, 15, 3, 0, 0, 1, tzinfo=tz.tzutc()))
        self.assertEqual(ceil, datetime(2013, 2, 15, 4, tzinfo=tz.tzutc()))

    def test_span_exclusive_exclusive(self):

        floor, ceil = self.arrow.span("hour", bounds="()")

        self.assertEqual(floor, datetime(2013, 2, 15, 3, 0, 0, 1, tzinfo=tz.tzutc()))
        self.assertEqual(
            ceil, datetime(2013, 2, 15, 3, 59, 59, 999999, tzinfo=tz.tzutc())
        )

    def test_bounds_are_validated(self):

        with self.assertRaises(AttributeError):
            floor, ceil = self.arrow.span("hour", bounds="][")


class ArrowHumanizeTests(Chai):
    def setUp(self):
        super(ArrowHumanizeTests, self).setUp()

        self.datetime = datetime(2013, 1, 1)
        self.now = arrow.Arrow.utcnow()

    def test_granularity(self):

        self.assertEqual(self.now.humanize(granularity="second"), "just now")

        later1 = self.now.shift(seconds=1)
        self.assertEqual(self.now.humanize(later1, granularity="second"), "just now")
        self.assertEqual(later1.humanize(self.now, granularity="second"), "just now")
        self.assertEqual(
            self.now.humanize(later1, granularity="minute"), "0 minutes ago"
        )
        self.assertEqual(
            later1.humanize(self.now, granularity="minute"), "in 0 minutes"
        )

        later100 = self.now.shift(seconds=100)
        self.assertEqual(
            self.now.humanize(later100, granularity="second"), "100 seconds ago"
        )
        self.assertEqual(
            later100.humanize(self.now, granularity="second"), "in 100 seconds"
        )
        self.assertEqual(
            self.now.humanize(later100, granularity="minute"), "a minute ago"
        )
        self.assertEqual(
            later100.humanize(self.now, granularity="minute"), "in a minute"
        )
        self.assertEqual(self.now.humanize(later100, granularity="hour"), "0 hours ago")
        self.assertEqual(later100.humanize(self.now, granularity="hour"), "in 0 hours")

        later4000 = self.now.shift(seconds=4000)
        self.assertEqual(
            self.now.humanize(later4000, granularity="minute"), "66 minutes ago"
        )
        self.assertEqual(
            later4000.humanize(self.now, granularity="minute"), "in 66 minutes"
        )
        self.assertEqual(
            self.now.humanize(later4000, granularity="hour"), "an hour ago"
        )
        self.assertEqual(later4000.humanize(self.now, granularity="hour"), "in an hour")
        self.assertEqual(self.now.humanize(later4000, granularity="day"), "0 days ago")
        self.assertEqual(later4000.humanize(self.now, granularity="day"), "in 0 days")

        later105 = self.now.shift(seconds=10 ** 5)
        self.assertEqual(
            self.now.humanize(later105, granularity="hour"), "27 hours ago"
        )
        self.assertEqual(later105.humanize(self.now, granularity="hour"), "in 27 hours")
        self.assertEqual(self.now.humanize(later105, granularity="day"), "a day ago")
        self.assertEqual(later105.humanize(self.now, granularity="day"), "in a day")
        self.assertEqual(self.now.humanize(later105, granularity="week"), "0 weeks ago")
        self.assertEqual(later105.humanize(self.now, granularity="week"), "in 0 weeks")
        self.assertEqual(
            self.now.humanize(later105, granularity="month"), "0 months ago"
        )
        self.assertEqual(
            later105.humanize(self.now, granularity="month"), "in 0 months"
        )
        self.assertEqual(
            self.now.humanize(later105, granularity=["month"]), "0 months ago"
        )
        self.assertEqual(
            later105.humanize(self.now, granularity=["month"]), "in 0 months"
        )

        later106 = self.now.shift(seconds=3 * 10 ** 6)
        self.assertEqual(self.now.humanize(later106, granularity="day"), "34 days ago")
        self.assertEqual(later106.humanize(self.now, granularity="day"), "in 34 days")
        self.assertEqual(self.now.humanize(later106, granularity="week"), "4 weeks ago")
        self.assertEqual(later106.humanize(self.now, granularity="week"), "in 4 weeks")
        self.assertEqual(
            self.now.humanize(later106, granularity="month"), "a month ago"
        )
        self.assertEqual(later106.humanize(self.now, granularity="month"), "in a month")
        self.assertEqual(self.now.humanize(later106, granularity="year"), "0 years ago")
        self.assertEqual(later106.humanize(self.now, granularity="year"), "in 0 years")

        later506 = self.now.shift(seconds=50 * 10 ** 6)
        self.assertEqual(
            self.now.humanize(later506, granularity="week"), "82 weeks ago"
        )
        self.assertEqual(later506.humanize(self.now, granularity="week"), "in 82 weeks")
        self.assertEqual(
            self.now.humanize(later506, granularity="month"), "18 months ago"
        )
        self.assertEqual(
            later506.humanize(self.now, granularity="month"), "in 18 months"
        )
        self.assertEqual(self.now.humanize(later506, granularity="year"), "a year ago")
        self.assertEqual(later506.humanize(self.now, granularity="year"), "in a year")

        later108 = self.now.shift(seconds=10 ** 8)
        self.assertEqual(self.now.humanize(later108, granularity="year"), "3 years ago")
        self.assertEqual(later108.humanize(self.now, granularity="year"), "in 3 years")

        later108onlydistance = self.now.shift(seconds=10 ** 8)
        self.assertEqual(
            self.now.humanize(
                later108onlydistance, only_distance=True, granularity="year"
            ),
            "3 years",
        )
        self.assertEqual(
            later108onlydistance.humanize(
                self.now, only_distance=True, granularity="year"
            ),
            "3 years",
        )

        with self.assertRaises(AttributeError):
            self.now.humanize(later108, granularity="years")

    def test_multiple_granularity(self):
        self.assertEqual(self.now.humanize(granularity="second"), "just now")
        self.assertEqual(self.now.humanize(granularity=["second"]), "just now")
        self.assertEqual(
            self.now.humanize(granularity=["year", "month", "day", "hour", "second"]),
            "in 0 years 0 months 0 days 0 hours and 0 seconds",
        )

        later4000 = self.now.shift(seconds=4000)
        self.assertEqual(
            later4000.humanize(self.now, granularity=["hour", "minute"]),
            "in an hour and 6 minutes",
        )
        self.assertEqual(
            self.now.humanize(later4000, granularity=["hour", "minute"]),
            "an hour and 6 minutes ago",
        )
        self.assertEqual(
            later4000.humanize(
                self.now, granularity=["hour", "minute"], only_distance=True
            ),
            "an hour and 6 minutes",
        )
        self.assertEqual(
            later4000.humanize(self.now, granularity=["day", "hour", "minute"]),
            "in 0 days an hour and 6 minutes",
        )
        self.assertEqual(
            self.now.humanize(later4000, granularity=["day", "hour", "minute"]),
            "0 days an hour and 6 minutes ago",
        )

        later105 = self.now.shift(seconds=10 ** 5)
        self.assertEqual(
            self.now.humanize(later105, granularity=["hour", "day", "minute"]),
            "a day 3 hours and 46 minutes ago",
        )
        with self.assertRaises(AttributeError):
            self.now.humanize(later105, granularity=["error", "second"])

        later108onlydistance = self.now.shift(seconds=10 ** 8)
        self.assertEqual(
            self.now.humanize(
                later108onlydistance, only_distance=True, granularity=["year"]
            ),
            "3 years",
        )
        self.assertEqual(
            self.now.humanize(
                later108onlydistance, only_distance=True, granularity=["month", "week"]
            ),
            "37 months and 4 weeks",
        )
        self.assertEqual(
            self.now.humanize(
                later108onlydistance, only_distance=True, granularity=["year", "second"]
            ),
            "3 years and 5327200 seconds",
        )

        one_min_one_sec_ago = self.now.shift(minutes=-1, seconds=-1)
        self.assertEqual(
            one_min_one_sec_ago.humanize(self.now, granularity=["minute", "second"]),
            "a minute and a second ago",
        )

        one_min_two_secs_ago = self.now.shift(minutes=-1, seconds=-2)
        self.assertEqual(
            one_min_two_secs_ago.humanize(self.now, granularity=["minute", "second"]),
            "a minute and 2 seconds ago",
        )

    def test_seconds(self):

        later = self.now.shift(seconds=10)

        # regression test for issue #727
        self.assertEqual(self.now.humanize(later), "10 seconds ago")
        self.assertEqual(later.humanize(self.now), "in 10 seconds")

        self.assertEqual(self.now.humanize(later, only_distance=True), "10 seconds")
        self.assertEqual(later.humanize(self.now, only_distance=True), "10 seconds")

    def test_minute(self):

        later = self.now.shift(minutes=1)

        self.assertEqual(self.now.humanize(later), "a minute ago")
        self.assertEqual(later.humanize(self.now), "in a minute")

        self.assertEqual(self.now.humanize(later, only_distance=True), "a minute")
        self.assertEqual(later.humanize(self.now, only_distance=True), "a minute")

    def test_minutes(self):

        later = self.now.shift(minutes=2)

        self.assertEqual(self.now.humanize(later), "2 minutes ago")
        self.assertEqual(later.humanize(self.now), "in 2 minutes")

        self.assertEqual(self.now.humanize(later, only_distance=True), "2 minutes")
        self.assertEqual(later.humanize(self.now, only_distance=True), "2 minutes")

    def test_hour(self):

        later = self.now.shift(hours=1)

        self.assertEqual(self.now.humanize(later), "an hour ago")
        self.assertEqual(later.humanize(self.now), "in an hour")

        self.assertEqual(self.now.humanize(later, only_distance=True), "an hour")
        self.assertEqual(later.humanize(self.now, only_distance=True), "an hour")

    def test_hours(self):

        later = self.now.shift(hours=2)

        self.assertEqual(self.now.humanize(later), "2 hours ago")
        self.assertEqual(later.humanize(self.now), "in 2 hours")

        self.assertEqual(self.now.humanize(later, only_distance=True), "2 hours")
        self.assertEqual(later.humanize(self.now, only_distance=True), "2 hours")

    def test_day(self):

        later = self.now.shift(days=1)

        self.assertEqual(self.now.humanize(later), "a day ago")
        self.assertEqual(later.humanize(self.now), "in a day")

        # regression test for issue #697
        less_than_48_hours = self.now.shift(
            days=1, hours=23, seconds=59, microseconds=999999
        )
        self.assertEqual(self.now.humanize(less_than_48_hours), "a day ago")
        self.assertEqual(less_than_48_hours.humanize(self.now), "in a day")

        less_than_48_hours_date = less_than_48_hours._datetime.date()
        with self.assertRaises(TypeError):
            # humanize other argument does not take raw datetime.date objects
            self.now.humanize(less_than_48_hours_date)

        # convert from date to arrow object
        less_than_48_hours_date = arrow.Arrow.fromdate(less_than_48_hours_date)
        self.assertEqual(self.now.humanize(less_than_48_hours_date), "a day ago")
        self.assertEqual(less_than_48_hours_date.humanize(self.now), "in a day")

        self.assertEqual(self.now.humanize(later, only_distance=True), "a day")
        self.assertEqual(later.humanize(self.now, only_distance=True), "a day")

    def test_days(self):

        later = self.now.shift(days=2)

        self.assertEqual(self.now.humanize(later), "2 days ago")
        self.assertEqual(later.humanize(self.now), "in 2 days")

        self.assertEqual(self.now.humanize(later, only_distance=True), "2 days")
        self.assertEqual(later.humanize(self.now, only_distance=True), "2 days")

        # Regression tests for humanize bug referenced in issue 541
        later = self.now.shift(days=3)
        self.assertEqual(later.humanize(), "in 3 days")

        later = self.now.shift(days=3, seconds=1)
        self.assertEqual(later.humanize(), "in 3 days")

        later = self.now.shift(days=4)
        self.assertEqual(later.humanize(), "in 4 days")

    def test_week(self):

        later = self.now.shift(weeks=1)

        self.assertEqual(self.now.humanize(later), "a week ago")
        self.assertEqual(later.humanize(self.now), "in a week")

        self.assertEqual(self.now.humanize(later, only_distance=True), "a week")
        self.assertEqual(later.humanize(self.now, only_distance=True), "a week")

    def test_weeks(self):

        later = self.now.shift(weeks=2)

        self.assertEqual(self.now.humanize(later), "2 weeks ago")
        self.assertEqual(later.humanize(self.now), "in 2 weeks")

        self.assertEqual(self.now.humanize(later, only_distance=True), "2 weeks")
        self.assertEqual(later.humanize(self.now, only_distance=True), "2 weeks")

    def test_month(self):

        later = self.now.shift(months=1)

        self.assertEqual(self.now.humanize(later), "a month ago")
        self.assertEqual(later.humanize(self.now), "in a month")

        self.assertEqual(self.now.humanize(later, only_distance=True), "a month")
        self.assertEqual(later.humanize(self.now, only_distance=True), "a month")

    def test_months(self):

        later = self.now.shift(months=2)
        earlier = self.now.shift(months=-2)

        self.assertEqual(earlier.humanize(self.now), "2 months ago")
        self.assertEqual(later.humanize(self.now), "in 2 months")

        self.assertEqual(self.now.humanize(later, only_distance=True), "2 months")
        self.assertEqual(later.humanize(self.now, only_distance=True), "2 months")

    def test_year(self):

        later = self.now.shift(years=1)

        self.assertEqual(self.now.humanize(later), "a year ago")
        self.assertEqual(later.humanize(self.now), "in a year")

        self.assertEqual(self.now.humanize(later, only_distance=True), "a year")
        self.assertEqual(later.humanize(self.now, only_distance=True), "a year")

    def test_years(self):

        later = self.now.shift(years=2)

        self.assertEqual(self.now.humanize(later), "2 years ago")
        self.assertEqual(later.humanize(self.now), "in 2 years")

        self.assertEqual(self.now.humanize(later, only_distance=True), "2 years")
        self.assertEqual(later.humanize(self.now, only_distance=True), "2 years")

        arw = arrow.Arrow(2014, 7, 2)

        result = arw.humanize(self.datetime)

        self.assertEqual(result, "in 2 years")

    def test_arrow(self):

        arw = arrow.Arrow.fromdatetime(self.datetime)

        result = arw.humanize(arrow.Arrow.fromdatetime(self.datetime))

        self.assertEqual(result, "just now")

    def test_datetime_tzinfo(self):

        arw = arrow.Arrow.fromdatetime(self.datetime)

        result = arw.humanize(self.datetime.replace(tzinfo=tz.tzutc()))

        self.assertEqual(result, "just now")

    def test_other(self):

        arw = arrow.Arrow.fromdatetime(self.datetime)

        with self.assertRaises(TypeError):
            arw.humanize(object())

    def test_invalid_locale(self):

        arw = arrow.Arrow.fromdatetime(self.datetime)

        with self.assertRaises(ValueError):
            arw.humanize(locale="klingon")

    def test_none(self):

        arw = arrow.Arrow.utcnow()

        result = arw.humanize()

        self.assertEqual(result, "just now")

        result = arw.humanize(None)

        self.assertEqual(result, "just now")

    def test_untranslated_granularity(self):

        arw = arrow.Arrow.utcnow()
        later = arw.shift(weeks=1)

        # simulate an untranslated timeframe key
        with patch.dict("arrow.locales.EnglishLocale.timeframes"):
            del arrow.locales.EnglishLocale.timeframes["week"]

            with self.assertRaises(ValueError):
                arw.humanize(later, granularity="week")


class ArrowHumanizeTestsWithLocale(Chai):
    def setUp(self):
        super(ArrowHumanizeTestsWithLocale, self).setUp()

        self.datetime = datetime(2013, 1, 1)

    def test_now(self):

        arw = arrow.Arrow(2013, 1, 1, 0, 0, 0)

        result = arw.humanize(self.datetime, locale="ru")

        self.assertEqual(result, "сейчас")

    def test_seconds(self):
        arw = arrow.Arrow(2013, 1, 1, 0, 0, 44)

        result = arw.humanize(self.datetime, locale="ru")

        self.assertEqual(result, "через 44 несколько секунд")

    def test_years(self):

        arw = arrow.Arrow(2011, 7, 2)

        result = arw.humanize(self.datetime, locale="ru")

        self.assertEqual(result, "2 года назад")


class ArrowIsBetweenTests(Chai):
    def test_start_before_end(self):
        target = arrow.Arrow.fromdatetime(datetime(2013, 5, 7))
        start = arrow.Arrow.fromdatetime(datetime(2013, 5, 8))
        end = arrow.Arrow.fromdatetime(datetime(2013, 5, 5))
        result = target.is_between(start, end)
        self.assertFalse(result)

    def test_exclusive_exclusive_bounds(self):
        target = arrow.Arrow.fromdatetime(datetime(2013, 5, 5, 12, 30, 27))
        start = arrow.Arrow.fromdatetime(datetime(2013, 5, 5, 12, 30, 10))
        end = arrow.Arrow.fromdatetime(datetime(2013, 5, 5, 12, 30, 36))
        result = target.is_between(start, end, "()")
        self.assertTrue(result)
        result = target.is_between(start, end)
        self.assertTrue(result)

    def test_exclusive_exclusive_bounds_same_date(self):
        target = arrow.Arrow.fromdatetime(datetime(2013, 5, 7))
        start = arrow.Arrow.fromdatetime(datetime(2013, 5, 7))
        end = arrow.Arrow.fromdatetime(datetime(2013, 5, 7))
        result = target.is_between(start, end, "()")
        self.assertFalse(result)

    def test_inclusive_exclusive_bounds(self):
        target = arrow.Arrow.fromdatetime(datetime(2013, 5, 6))
        start = arrow.Arrow.fromdatetime(datetime(2013, 5, 4))
        end = arrow.Arrow.fromdatetime(datetime(2013, 5, 6))
        result = target.is_between(start, end, "[)")
        self.assertFalse(result)

    def test_exclusive_inclusive_bounds(self):
        target = arrow.Arrow.fromdatetime(datetime(2013, 5, 7))
        start = arrow.Arrow.fromdatetime(datetime(2013, 5, 5))
        end = arrow.Arrow.fromdatetime(datetime(2013, 5, 7))
        result = target.is_between(start, end, "(]")
        self.assertTrue(result)

    def test_inclusive_inclusive_bounds_same_date(self):
        target = arrow.Arrow.fromdatetime(datetime(2013, 5, 7))
        start = arrow.Arrow.fromdatetime(datetime(2013, 5, 7))
        end = arrow.Arrow.fromdatetime(datetime(2013, 5, 7))
        result = target.is_between(start, end, "[]")
        self.assertTrue(result)

    def test_type_error_exception(self):
        with self.assertRaises(TypeError):
            target = arrow.Arrow.fromdatetime(datetime(2013, 5, 7))
            start = datetime(2013, 5, 5)
            end = arrow.Arrow.fromdatetime(datetime(2013, 5, 8))
            target.is_between(start, end)

        with self.assertRaises(TypeError):
            target = arrow.Arrow.fromdatetime(datetime(2013, 5, 7))
            start = arrow.Arrow.fromdatetime(datetime(2013, 5, 5))
            end = datetime(2013, 5, 8)
            target.is_between(start, end)

        with self.assertRaises(TypeError):
            target.is_between(None, None)

    def test_attribute_error_exception(self):
        target = arrow.Arrow.fromdatetime(datetime(2013, 5, 7))
        start = arrow.Arrow.fromdatetime(datetime(2013, 5, 5))
        end = arrow.Arrow.fromdatetime(datetime(2013, 5, 8))
        with self.assertRaises(AttributeError):
            target.is_between(start, end, "][")
        with self.assertRaises(AttributeError):
            target.is_between(start, end, "")
        with self.assertRaises(AttributeError):
            target.is_between(start, end, "]")
        with self.assertRaises(AttributeError):
            target.is_between(start, end, "[")
        with self.assertRaises(AttributeError):
            target.is_between(start, end, "hello")


class ArrowUtilTests(Chai):
    def test_get_datetime(self):

        get_datetime = arrow.Arrow._get_datetime

        arw = arrow.Arrow.utcnow()
        dt = datetime.utcnow()
        timestamp = time.time()

        self.assertEqual(get_datetime(arw), arw.datetime)
        self.assertEqual(get_datetime(dt), dt)
        self.assertEqual(
            get_datetime(timestamp), arrow.Arrow.utcfromtimestamp(timestamp).datetime
        )

        with self.assertRaises(ValueError) as raise_ctx:
            get_datetime("abc")
        self.assertFalse("{}" in str(raise_ctx.exception))

    def test_get_tzinfo(self):

        get_tzinfo = arrow.Arrow._get_tzinfo

        with self.assertRaises(ValueError) as raise_ctx:
            get_tzinfo("abc")
        self.assertFalse("{}" in str(raise_ctx.exception))

    def test_get_iteration_params(self):

        self.assertEqual(
            arrow.Arrow._get_iteration_params("end", None), ("end", sys.maxsize)
        )
        self.assertEqual(
            arrow.Arrow._get_iteration_params(None, 100), (arrow.Arrow.max, 100)
        )
        self.assertEqual(arrow.Arrow._get_iteration_params(100, 120), (100, 120))

        with self.assertRaises(ValueError):
            arrow.Arrow._get_iteration_params(None, None)
