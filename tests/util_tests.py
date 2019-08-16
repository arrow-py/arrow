# -*- coding: utf-8 -*-
import time

from chai import Chai

from arrow import util


class UtilTests(Chai):
    def test_is_timestamp(self):
        timestamp_float = time.time()
        timestamp_int = int(timestamp_float)

        self.assertTrue(util.is_timestamp(timestamp_int))
        self.assertTrue(util.is_timestamp(timestamp_float))

        self.assertFalse(util.is_timestamp(str(timestamp_int)))
        self.assertFalse(util.is_timestamp(str(timestamp_float)))
        self.assertFalse(util.is_timestamp(True))
        self.assertFalse(util.is_timestamp(False))

        full_datetime = "2019-06-23T13:12:42"
        self.assertFalse(util.is_timestamp(full_datetime))

        overflow_timestamp_float = 99999999999999999999999999.99999999999999999999999999
        with self.assertRaises((OverflowError, ValueError)):
            util.is_timestamp(overflow_timestamp_float)

        overflow_timestamp_int = int(overflow_timestamp_float)
        with self.assertRaises((OverflowError, ValueError)):
            util.is_timestamp(overflow_timestamp_int)
