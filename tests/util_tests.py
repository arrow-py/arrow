# -*- coding: utf-8 -*-
from datetime import datetime

from chai import Chai

from arrow import util


class UtilTests(Chai):
    def test_is_timestamp(self):
        timestamp_float = datetime.now().timestamp()
        timestamp_int = int(timestamp_float)

        self.assertTrue(util.is_timestamp(timestamp_int))
        self.assertTrue(util.is_timestamp(timestamp_float))

        self.assertFalse(util.is_timestamp(str(timestamp_int)))
        self.assertFalse(util.is_timestamp(str(timestamp_float)))
        self.assertFalse(util.is_timestamp(True))
        self.assertFalse(util.is_timestamp(False))

        full_datetime = "2019-06-23T13:12:42"
        self.assertFalse(util.is_timestamp(full_datetime))
