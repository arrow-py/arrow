# -*- coding: utf-8 -*-

from chai import Chai

from datetime import datetime, timedelta
from dateutil import tz
import calendar
import time

import arrow

def assertDtEqual(dt1, dt2, within=10):
    assertTrue(abs((dt1 - dt2).total_seconds()) < within)


class ArrowInitTests(Chai):

    def test_init(self):

        result = arrow.Arrow(2013, 2, 2, 12, 30, 45, 999999)

        assertEqual(result._datetime, datetime(2013, 2, 2, 12, 30, 45, 999999, tzinfo=tz.tzutc()))


class ArrowFactoryTests(Chai):

    def test_now(self):

        result = arrow.Arrow.now()

        assertDtEqual(result._datetime, datetime.now().replace(tzinfo=tz.tzlocal()))

    def test_utcnow(self):

        result = arrow.Arrow.utcnow()

        assertDtEqual(result._datetime, datetime.utcnow().replace(tzinfo=tz.tzutc()))

    #def test_fromtimestamp(self):

    #    timestamp = time.time()
    #    tzinfo = tz.gettz('US/Pacific')

    #    result = arrow.Arrow.fromtimestamp(timestamp, tzinfo)
    #    print result
    #    print datetime.now().replace(tzinfo=tzinfo)

    #    assertDtEqual(result._datetime, datetime.now().replace(tzinfo=tzinfo))

    def test_formtimestamp(self):

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

    def test_plurals(self):

        assertEqual(self.arrow.years, self.arrow.year)
        assertEqual(self.arrow.months, self.arrow.month)
        assertEqual(self.arrow.days, self.arrow.day)
        assertEqual(self.arrow.hours, self.arrow.hour)
        assertEqual(self.arrow.minutes, self.arrow.minute)
        assertEqual(self.arrow.seconds, self.arrow.second)
        assertEqual(self.arrow.microseconds, self.arrow.microsecond)

    def test_year(self):

        self.arrow.year = 2012
        assertEqual(self.arrow.year, 2012)

        self.arrow.year += 1
        assertEqual(self.arrow.year, 2013)

    def test_month(self):

        self.arrow.month = 2
        assertEqual(self.arrow.month, 2)

        self.arrow.month = -1
        assertEqual(self.arrow.month, 11)
        assertEqual(self.arrow.year, 2012)

        self.arrow.month += 2
        assertEqual(self.arrow.month, 1)
        assertEqual(self.arrow.year, 2013)

    def test_day(self):

        self.arrow.day = 2
        assertEqual(self.arrow.day, 2)

        self.arrow.day = -1
        assertEqual(self.arrow.day, 30)
        assertEqual(self.arrow.year, 2012)

        self.arrow.day += 2
        assertEqual(self.arrow.day, 1)
        assertEqual(self.arrow.year, 2013)

    def test_hour(self):

        self.arrow.hour = 1
        assertEqual(self.arrow.hour, 1)

        self.arrow.hour = -1
        assertEqual(self.arrow.hour, 23)
        assertEqual(self.arrow.day, 31)

        self.arrow.hour += 1
        assertEqual(self.arrow.hour, 0)
        assertEqual(self.arrow.day, 1)

    def test_minute(self):

        self.arrow.minute = 1
        assertEqual(self.arrow.minute, 1)

        self.arrow.minute = -1
        assertEqual(self.arrow.minute, 59)
        assertEqual(self.arrow.hour, 23)

        self.arrow.minute += 1
        assertEqual(self.arrow.minute, 0)
        assertEqual(self.arrow.hour, 0)

    def test_second(self):

        self.arrow.second = 1
        assertEqual(self.arrow.second, 1)

        self.arrow.second = -1
        assertEqual(self.arrow.second, 59)
        assertEqual(self.arrow.minute, 59)

        self.arrow.second += 1
        assertEqual(self.arrow.second, 0)
        assertEqual(self.arrow.minute, 0)

    def test_microsecond(self):

        self.arrow.microsecond = 1
        assertEqual(self.arrow.microsecond, 1)

        self.arrow.microsecond = -1
        assertEqual(self.arrow.microsecond, 999999)
        assertEqual(self.arrow.second, 59)

        self.arrow.microsecond += 1
        assertEqual(self.arrow.microsecond, 0)
        assertEqual(self.arrow.second, 0)

    def test_tzinfo(self):

        self.arrow.tzinfo = tz.gettz('PST')
        assertEqual(self.arrow.tzinfo, tz.gettz('PST'))

    def test_naive(self):

        assertEqual(self.arrow.naive, self.arrow._datetime.replace(tzinfo=None))

    def test_timestamp(self):

        assertEqual(self.arrow.timestamp, calendar.timegm(self.arrow._datetime.utctimetuple()))


class ArrowComparisonTests(Chai):

    def setUp(self):
        super(ArrowComparisonTests, self).setUp()

        self.arrow = arrow.Arrow.utcnow()

    def test_cmp_convert(self):

        dt = datetime.utcnow()

        assertEqual(self.arrow._cmp_convert(dt), dt)
        assertEqual(self.arrow._cmp_convert(self.arrow), self.arrow.datetime)

    def test_eq(self):

        assertTrue(self.arrow == self.arrow)
        assertTrue(self.arrow == self.arrow.datetime)
        assertFalse(self.arrow == 'abc')

    def test_ne(self):

        assertFalse(self.arrow != self.arrow)
        assertFalse(self.arrow != self.arrow.datetime)
        assertTrue(self.arrow != 'abc')

    def test_gt(self):

        arrow_cmp = self.arrow.clone()
        self.arrow.minutes += 1

        assertFalse(self.arrow > self.arrow)
        assertFalse(self.arrow > self.arrow.datetime)
        assertFalse(self.arrow > 'abc')
        assertTrue(self.arrow > arrow_cmp)
        assertTrue(self.arrow > arrow_cmp.datetime)

    def test_ge(self):

        assertFalse(self.arrow >= 'abc')
        assertTrue(self.arrow >= self.arrow)
        assertTrue(self.arrow >= self.arrow.datetime)

    def test_lt(self):

        arrow_cmp = self.arrow.clone()
        arrow_cmp.minutes += 1

        assertFalse(self.arrow < self.arrow)
        assertFalse(self.arrow < self.arrow.datetime)
        assertFalse(self.arrow < 'abc')
        assertTrue(self.arrow < arrow_cmp)
        assertTrue(self.arrow < arrow_cmp.datetime)

    def test_le(self):

        assertFalse(self.arrow <= 'abc')
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

        with assertRaises(NotImplementedError):
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

        with assertRaises(NotImplementedError):
            self.arrow.__sub__(object())

    def test_rsub(self):

        result = self.arrow.__rsub__(timedelta(days=1))

        assertEqual(result._datetime, datetime(2012, 12, 31, tzinfo=tz.tzutc()))


class ArrowDatetimeInterfaceTests(Chai):

    def setUp(self):
        super(ArrowDatetimeInterfaceTests, self).setUp()

        self.arrow = arrow.Arrow.utcnow()
        print self.arrow

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

        result = arrow_from.to('UTC')

        expected = dt_from.replace(tzinfo=tz.gettz('US/Pacific')).astimezone(tz.tzutc())

        assertEqual(result.datetime, expected)


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

    def test_span_month(self):

        floor, ceil = self.arrow.span('month')

        assertEqual(floor, datetime(2013, 2, 1, tzinfo=tz.tzutc()))
        assertEqual(ceil, datetime(2013, 2, 28, 23, 59, 59, 999999, tzinfo=tz.tzutc()))

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

    def test_span_hour(self):

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

    def test_seconds(self):

        arw = arrow.Arrow(2013, 1, 1, 0, 0, 44)

        result = arw.humanize(self.datetime)

        assertEqual(result, 'in seconds')

    def test_minute(self):

        arw = arrow.Arrow(2013, 1, 1, 0, 0, 45)

        result = arw.humanize(self.datetime)

        assertEqual(result, 'in a minute')

    def test_minutes(self):

        arw = arrow.Arrow(2013, 1, 1, 0, 1, 30)

        result = arw.humanize(self.datetime)

        assertEqual(result, 'in 2 minutes')

    def test_hour(self):

        arw = arrow.Arrow(2013, 1, 1, 0, 45)

        result = arw.humanize(self.datetime)

        assertEqual(result, 'in an hour')

    def test_hours(self):

        arw = arrow.Arrow(2013, 1, 1, 1, 30)

        result = arw.humanize(self.datetime)

        assertEqual(result, 'in 2 hours')

    def test_day(self):

        arw = arrow.Arrow(2013, 1, 1, 22)

        result = arw.humanize(self.datetime)

        assertEqual(result, 'in a day')

    def test_days(self):

        arw = arrow.Arrow(2013, 1, 2, 12)

        result = arw.humanize(self.datetime)

        assertEqual(result, 'in 2 days')

    def test_month(self):

        arw = arrow.Arrow(2013, 1, 26)

        result = arw.humanize(self.datetime)

        assertEqual(result, 'in a month')

    def test_months(self):

        arw = arrow.Arrow(2013, 2, 15)

        result = arw.humanize(self.datetime)

        assertEqual(result, 'in 2 months')

    def test_year(self):

        arw = arrow.Arrow(2014, 1, 1)

        result = arw.humanize(self.datetime)

        assertEqual(result, 'in a year')

    def test_years(self):

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

    def test_seconds(self):

        arw = arrow.Arrow(2013, 1, 1, 0, 0, 44)

        result = arw.humanize(self.datetime, locale='russian')

        assertEqual(result, 'через несколько секунд')

    def test_years(self):

        arw = arrow.Arrow(2011, 7, 2)

        result = arw.humanize(self.datetime, locale='russian')

        assertEqual(result, '2 года/лет назад')
