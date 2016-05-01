from chai import Chai

from arrow import formatter, locales

from datetime import datetime
from dateutil import tz as dateutil_tz
import time


def format_en_us(dt, str_format):
    locale = locales.get_locale('en_us')
    return formatter.format_token(dt, str_format, locale)


class DateTimeFormatterFormatTokenTests(Chai):

    def setUp(self):
        super(DateTimeFormatterFormatTokenTests, self).setUp()

    def test_format(self):

        dt = datetime(2013, 2, 5, 12, 32, 51)

        result = formatter.format(dt, 'MM-DD-YYYY hh:mm:ss a')

        assertEqual(result, '02-05-2013 12:32:51 pm')

    def test_year(self):

        dt = datetime(2013, 1, 1)
        assertEqual(format_en_us(dt, 'YYYY'), '2013')
        assertEqual(format_en_us(dt, 'YY'), '13')

    def test_month(self):

        dt = datetime(2013, 1, 1)
        assertEqual(format_en_us(dt, 'MMMM'), 'January')
        assertEqual(format_en_us(dt, 'MMM'), 'Jan')
        assertEqual(format_en_us(dt, 'MM'), '01')
        assertEqual(format_en_us(dt, 'M'), '1')

    def test_day(self):

        dt = datetime(2013, 2, 1)
        assertEqual(format_en_us(dt, 'DDDD'), '032')
        assertEqual(format_en_us(dt, 'DDD'), '32')
        assertEqual(format_en_us(dt, 'DD'), '01')
        assertEqual(format_en_us(dt, 'D'), '1')
        assertEqual(format_en_us(dt, 'Do'), '1st')


        assertEqual(format_en_us(dt, 'dddd'), 'Friday')
        assertEqual(format_en_us(dt, 'ddd'), 'Fri')
        assertEqual(format_en_us(dt, 'd'), '5')

    def test_hour(self):

        dt = datetime(2013, 1, 1, 2)
        assertEqual(format_en_us(dt, 'HH'), '02')
        assertEqual(format_en_us(dt, 'H'), '2')

        dt = datetime(2013, 1, 1, 13)
        assertEqual(format_en_us(dt, 'HH'), '13')
        assertEqual(format_en_us(dt, 'H'), '13')

        dt = datetime(2013, 1, 1, 2)
        assertEqual(format_en_us(dt, 'hh'), '02')
        assertEqual(format_en_us(dt, 'h'), '2')

        dt = datetime(2013, 1, 1, 13)
        assertEqual(format_en_us(dt, 'hh'), '01')
        assertEqual(format_en_us(dt, 'h'), '1')

        # test that 12-hour time converts to '12' at midnight
        dt = datetime(2013, 1, 1, 0)
        assertEqual(format_en_us(dt, 'hh'), '12')
        assertEqual(format_en_us(dt, 'h'), '12')

    def test_minute(self):

        dt = datetime(2013, 1, 1, 0, 1)
        assertEqual(format_en_us(dt, 'mm'), '01')
        assertEqual(format_en_us(dt, 'm'), '1')

    def test_second(self):

        dt = datetime(2013, 1, 1, 0, 0, 1)
        assertEqual(format_en_us(dt, 'ss'), '01')
        assertEqual(format_en_us(dt, 's'), '1')

    def test_sub_second(self):

        dt = datetime(2013, 1, 1, 0, 0, 0, 123456)
        assertEqual(format_en_us(dt, 'SSSSSS'), '123456')
        assertEqual(format_en_us(dt, 'SSSSS'), '12345')
        assertEqual(format_en_us(dt, 'SSSS'), '1234')
        assertEqual(format_en_us(dt, 'SSS'), '123')
        assertEqual(format_en_us(dt, 'SS'), '12')
        assertEqual(format_en_us(dt, 'S'), '1')

        dt = datetime(2013, 1, 1, 0, 0, 0, 2000)
        assertEqual(format_en_us(dt, 'SSSSSS'), '002000')
        assertEqual(format_en_us(dt, 'SSSSS'), '00200')
        assertEqual(format_en_us(dt, 'SSSS'), '0020')
        assertEqual(format_en_us(dt, 'SSS'), '002')
        assertEqual(format_en_us(dt, 'SS'), '00')
        assertEqual(format_en_us(dt, 'S'), '0')

    def test_timestamp(self):

        timestamp = time.time()
        dt = datetime.utcfromtimestamp(timestamp)
        assertEqual(format_en_us(dt, 'X'), str(int(timestamp)))

    def test_timezone(self):

        dt = datetime.utcnow().replace(tzinfo=dateutil_tz.gettz('US/Pacific'))

        result = format_en_us(dt, 'ZZ')
        assertTrue(result == '-07:00' or result == '-08:00')

        result = format_en_us(dt, 'Z')
        assertTrue(result == '-0700' or result == '-0800')

    def test_am_pm(self):

        dt = datetime(2012, 1, 1, 11)
        assertEqual(format_en_us(dt, 'a'), 'am')
        assertEqual(format_en_us(dt, 'A'), 'AM')

        dt = datetime(2012, 1, 1, 13)
        assertEqual(format_en_us(dt, 'a'), 'pm')
        assertEqual(format_en_us(dt, 'A'), 'PM')

    def test_nonsense(self):
        dt = datetime(2012, 1, 1, 11)
        assertEqual(format_en_us(dt, None), None)
        assertEqual(format_en_us(dt, 'NONSENSE'), None)
