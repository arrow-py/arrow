# -*- coding: utf-8 -*-

from chai import Chai
from datetime import timedelta, datetime
import sys
import pytz

from arrow import util


class UtilTests(Chai):

    def setUp(self):
        super(UtilTests, self).setUp()

    def test_total_seconds_26(self):

        td = timedelta(seconds=30)

        assertEqual(util._total_seconds_26(td), 30)

    if util.version >= '2.7':

        def test_total_seconds_27(self):

            td = timedelta(seconds=30)

            assertEqual(util._total_seconds_27(td), 30)

    def test_astimezone(self):
        tz = pytz.timezone("America/Los_Angeles")

        # Test outside of daylight savings time
        dt = datetime(2014, 1, 1, tzinfo=pytz.utc)
        dt = util.astimezone(dt, tz)
        
        assertFalse(dt.dst())
        assertEqual(dt.tzinfo._tzinfos, tz._tzinfos)

        # Test inside of daylight savings time
        dt = datetime(2014, 7, 1, tzinfo=pytz.utc)
        dt = util.astimezone(dt, tz)

        assertTrue(dt.dst())
        assertEqual(dt.tzinfo._tzinfos, tz._tzinfos)