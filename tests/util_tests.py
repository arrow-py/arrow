# -*- coding: utf-8 -*-

from chai import Chai
from datetime import timedelta
import sys

from arrow import util


class UtilTests(Chai):

    def setUp(self):
        super(UtilTests, self).setUp()

    def test_total_seconds_26(self):

        td = timedelta(seconds=30)

        assertEqual(util._total_seconds_26(td), 30)

    if util.version >= '2.7': # pragma: no cover

        def test_total_seconds_27(self):

            td = timedelta(seconds=30)

            assertEqual(util._total_seconds_27(td), 30)

