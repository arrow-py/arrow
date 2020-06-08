# -*- coding: utf-8 -*-
import time
from datetime import datetime

import pytest

from arrow import util


class TestUtil:
    def test_total_seconds(self):
        td = datetime(2019, 1, 1) - datetime(2018, 1, 1)
        assert util.total_seconds(td) == td.total_seconds()

    def test_is_timestamp(self):
        timestamp_float = time.time()
        timestamp_int = int(timestamp_float)

        assert util.is_timestamp(timestamp_int)
        assert util.is_timestamp(timestamp_float)
        assert util.is_timestamp(str(timestamp_int))
        assert util.is_timestamp(str(timestamp_float))

        assert not util.is_timestamp(True)
        assert not util.is_timestamp(False)

        class InvalidTimestamp:
            pass

        assert not util.is_timestamp(InvalidTimestamp())

        full_datetime = "2019-06-23T13:12:42"
        assert not util.is_timestamp(full_datetime)

    def test_iso_gregorian(self):
        with pytest.raises(ValueError):
            util.iso_to_gregorian(2013, 0, 5)

        with pytest.raises(ValueError):
            util.iso_to_gregorian(2013, 8, 0)
