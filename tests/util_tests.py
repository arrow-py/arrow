# -*- coding: utf-8 -*-

from chai import Chai
from datetime import timedelta

from arrow import util


class utilTests(Chai):

    def test_total_seconds_27(self):

        td = timedelta(seconds=30)

        assertEqual(util._total_seconds_27(td), 30)

    def test_total_seconds_26(self):

        td = timedelta(seconds=30)

        assertEqual(util._total_seconds_26(td), 30)

