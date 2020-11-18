

import calendar
import os
import time
from datetime import datetime

import pytest
from dateutil import tz

import arrow
from arrow import formatter, parser
from arrow.constants import MAX_TIMESTAMP_US
from arrow.parser import DateTimeParser, ParserError, ParserMatchError


def test_english():
    parser_ = parser.DateTimeParser("en_us")

    assert parser_.parse("January 1st, 2013", "MMMM Do, YYYY") == datetime(
        2013, 1, 1
    )
    assert parser_.parse("January 2nd, 2013", "MMMM Do, YYYY") == datetime(
        2013, 1, 2
    )
    assert parser_.parse("January 3rd, 2013", "MMMM Do, YYYY") == datetime(
        2013, 1, 3
    )
    assert parser_.parse("January 4th, 2013", "MMMM Do, YYYY") == datetime(
        2013, 1, 4
    )
    assert parser_.parse("January 11th, 2013", "MMMM Do, YYYY") == datetime(
        2013, 1, 11
    )
    assert parser_.parse("January 12th, 2013", "MMMM Do, YYYY") == datetime(
        2013, 1, 12
    )
    assert parser_.parse("January 13th, 2013", "MMMM Do, YYYY") == datetime(
        2013, 1, 13
    )
    assert parser_.parse("January 21st, 2013", "MMMM Do, YYYY") == datetime(
        2013, 1, 21
    )
    assert parser_.parse("January 31st, 2013", "MMMM Do, YYYY") == datetime(
        2013, 1, 31
    )

    with pytest.raises(ParserError):
        parser_.parse("January 1th, 2013", "MMMM Do, YYYY")

    with pytest.raises(ParserError):
        parser_.parse("January 11st, 2013", "MMMM Do, YYYY")

    print("WORKS")
        
def test():

    parser = DateTimeParser()

    assert parser.parse_iso("2011-W05-4") == datetime(2011, 2, 3)

    assert parser.parse_iso("2011-W05-4T14:17:01") == datetime(
        2011, 2, 3, 14, 17, 1
    )

    assert parser.parse_iso("2011W054") == datetime(2011, 2, 3)

    assert parser.parse_iso("2011W054T141701") == datetime(
        2011, 2, 3, 14, 17, 1
    )

    assert parser.parse("2011-W05-4", "W") == datetime(2011, 2, 3)
    assert parser.parse("2011W054", "W") == datetime(2011, 2, 3)
    assert parser.parse("2011-W05", "W") == datetime(2011, 1, 31)
    assert parser.parse("2011W05", "W") == datetime(2011, 1, 31)
    assert parser.parse("2011-W05-4T14:17:01", "WTHH:mm:ss") == datetime(
        2011, 2, 3, 14, 17, 1
    )
    assert parser.parse("2011W054T14:17:01", "WTHH:mm:ss") == datetime(
        2011, 2, 3, 14, 17, 1
    )
    assert parser.parse("2011-W05T14:17:01", "WTHH:mm:ss") == datetime(
        2011, 1, 31, 14, 17, 1
    )
    assert parser.parse("2011W05T141701", "WTHHmmss") == datetime(
        2011, 1, 31, 14, 17, 1
    )
    assert parser.parse("2011W054T141701", "WTHHmmss") == datetime(
        2011, 2, 3, 14, 17, 1
    )

    print("WORKS!")



if __name__ == "__main__":
    test()
    test_english()