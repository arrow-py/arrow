# -*- coding: utf-8 -*-

from chai import Chai
from datetime import timedelta
import sys

from arrow import util


class UtilTests(Chai):

    def setUp(self):
        super(UtilTests, self).setUp()

    def test_is_timestamp_True(self):
        timestamp = 1452980706
        assertTrue(util.is_timestamp(timestamp))

    def test_is_timestamp_False(self):
        timestamp = None;
        assertFalse(util.is_timestamp(timestamp))

    def test_total_seconds_26(self):

        td = timedelta(seconds=30)

        assertEqual(util._total_seconds_26(td), 30)

    if util.version >= '2.7':

        def test_total_seconds_27(self):

            td = timedelta(seconds=30)

            assertEqual(util._total_seconds_27(td), 30)
