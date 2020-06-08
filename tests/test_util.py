# -*- coding: utf-8 -*-
import sys
import time
from datetime import datetime

import pytest
from dateutil import tz as dateutil_tz

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

    @pytest.mark.skipif(
        sys.version_info >= (3, 6),
        reason="enfold has different behaviour pre python 3.6",
    )
    def test_determine_fold_27_35(self):
        dt_non_ambiguous = datetime(2018, 1, 1, tzinfo=dateutil_tz.tzutc())
        result = util.determine_fold(dt_non_ambiguous)
        with pytest.raises(AttributeError):
            # enfold will return a datetime with no fold attribute here on python 2.7/3.5
            assert result.fold == 0

        dt_ambiguous = datetime(
            2018, 11, 4, 1, 30, tzinfo=dateutil_tz.gettz("America/New_York")
        )
        result = util.determine_fold(dt_ambiguous)

        # enfold will return a DatetimeWithFold object here
        assert result.fold == 1

    @pytest.mark.skipif(
        sys.version_info < (3, 6),
        reason="enfold has different behaviour in python 3.6+",
    )
    def test_determine_fold_36_plus(self):
        dt_non_ambiguous = datetime(2018, 1, 1, tzinfo=dateutil_tz.tzutc())
        result = util.determine_fold(dt_non_ambiguous)
        assert result.fold == 0

        dt_ambiguous = datetime(
            2018, 11, 4, 1, 30, tzinfo=dateutil_tz.gettz("America/New_York")
        )
        result = util.determine_fold(dt_ambiguous)
        assert result.fold == 1
