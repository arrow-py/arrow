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
        self.assertTrue(util.is_timestamp(str(timestamp_int)))
        self.assertTrue(util.is_timestamp(str(timestamp_float)))

        self.assertFalse(util.is_timestamp(True))
        self.assertFalse(util.is_timestamp(False))

        class InvalidTimestamp:
            pass

        self.assertFalse(util.is_timestamp(InvalidTimestamp()))

        full_datetime = "2019-06-23T13:12:42"
        self.assertFalse(util.is_timestamp(full_datetime))

    def test_iso_gregorian(self):
        with self.assertRaises(ValueError):
            util.iso_to_gregorian(2013, 0, 5)

        with self.assertRaises(ValueError):
            util.iso_to_gregorian(2013, 8, 0)
