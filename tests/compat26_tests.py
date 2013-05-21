# -*- coding: utf-8 -*-

from chai import Chai

from datetime import timedelta

import arrow
from arrow.compat26 import get_total_seconds


class Compat26Tests(Chai):

    def test_not_timedelta(self):
        # creating an arbitrary object
        class Foo(object):
            pass
        o = Foo()
        self.assert_raises(ValueError, get_total_seconds, [o])

    def test_passing_none(self):
        self.assert_raises(ValueError, get_total_seconds, [None])
        self.assert_raises(ValueError, get_total_seconds, [])

    def test_result_is_correct(self):
        dt1 = arrow.get(1369158067)
        dt2 = arrow.get(1369158078)
        td = dt2 - dt1
        self.assert_equals(isinstance(td, timedelta), True)
        self.assert_equals(get_total_seconds(td), 11)
