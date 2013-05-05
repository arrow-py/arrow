from chai import Chai

from arrow import formatter

from datetime import datetime
from dateutil import tz as dateutil_tz
import time

class DateTimeFormatterFormatTokenTests(Chai):

    def setUp(self):
        super(DateTimeFormatterFormatTokenTests, self).setUp()

        self.format_token = formatter.DateTimeFormatter._format_token

    def test_format(self):

        dt = datetime(2013, 2, 5, 12, 32, 51)

        result = formatter.DateTimeFormatter.format(dt, 'MM-DD-YYYY hh:mm:ss a')

        assertEqual(result, '02-05-2013 12:32:51 pm')

    def test_year(self):

        dt = datetime(2013, 1, 1)
        assertEqual(self.format_token(dt, 'YYYY'), '2013')
        assertEqual(self.format_token(dt, 'YY'), '13')

    def test_month(self):

        dt = datetime(2013, 1, 1)
        assertEqual(self.format_token(dt, 'MMMM'), 'January')
        assertEqual(self.format_token(dt, 'MMM'), 'Jan')
        assertEqual(self.format_token(dt, 'MM'), '01')
        assertEqual(self.format_token(dt, 'M'), '1')

    def test_day(self):

        dt = datetime(2013, 2, 1)
        assertEqual(self.format_token(dt, 'DDDD'), '032')
        assertEqual(self.format_token(dt, 'DDD'), '32')
        assertEqual(self.format_token(dt, 'DD'), '01')
        assertEqual(self.format_token(dt, 'D'), '1')

        assertEqual(self.format_token(dt, 'dddd'), 'Saturday')
        assertEqual(self.format_token(dt, 'ddd'), 'Sat')
        assertEqual(self.format_token(dt, 'd'), '5')

    def test_hour(self):

        dt = datetime(2013, 1, 1, 2)
        assertEqual(self.format_token(dt, 'HH'), '02')
        assertEqual(self.format_token(dt, 'H'), '2')

        dt = datetime(2013, 1, 1, 13)
        assertEqual(self.format_token(dt, 'hh'), '01')
        assertEqual(self.format_token(dt, 'h'), '1')

    def test_minute(self):

        dt = datetime(2013, 1, 1, 0, 1)
        assertEqual(self.format_token(dt, 'mm'), '01')
        assertEqual(self.format_token(dt, 'm'), '1')

    def test_second(self):

        dt = datetime(2013, 1, 1, 0, 0, 1)
        assertEqual(self.format_token(dt, 'ss'), '01')
        assertEqual(self.format_token(dt, 's'), '1')

    def test_sub_second(self):

        dt = datetime(2013, 1, 1, 0, 0, 0, 500000)
        assertEqual(self.format_token(dt, 'SSS'), '500')
        assertEqual(self.format_token(dt, 'SS'), '50')
        assertEqual(self.format_token(dt, 'S'), '5')

    def test_timestamp(self):

        timestamp = time.time()
        dt = datetime.utcfromtimestamp(timestamp)
        assertEqual(self.format_token(dt, 'X'), str(int(timestamp)))

    def test_timezone(self):

        dt = datetime.utcnow().replace(tzinfo=dateutil_tz.gettz('PDT'))
        assertEqual(self.format_token(dt, 'ZZ'), '-07:00')
        assertEqual(self.format_token(dt, 'Z'), '-0700')

    def test_am_pm(self):

        dt = datetime(2012, 1, 1, 11)
        assertEqual(self.format_token(dt, 'a'), 'am')
        assertEqual(self.format_token(dt, 'A'), 'AM')

        dt = datetime(2012, 1, 1, 13)
        assertEqual(self.format_token(dt, 'a'), 'pm')
        assertEqual(self.format_token(dt, 'A'), 'PM')




