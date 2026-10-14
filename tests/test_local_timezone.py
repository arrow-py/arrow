import time
from datetime import datetime, timezone

import pytest

try:
    from zoneinfo import ZoneInfo
except ImportError:
    from backports.zoneinfo import ZoneInfo

from arrow import Arrow

pytestmark = pytest.mark.skipif(
    not hasattr(time, "tzset"), reason="Changing the local timezone requires time.tzset"
)


@pytest.fixture(params=["America/New_York", "Europe/Paris", "Australia/Lord_Howe"])
def local_timezone(request, monkeypatch):
    try:
        with monkeypatch.context() as patch:
            patch.setenv("TZ", request.param)
            time.tzset()
            yield ZoneInfo(request.param)
    finally:
        time.tzset()


@pytest.fixture(
    params=[
        (2000, 1, 1, 12),
        (2000, 7, 1, 12),
        (2030, 1, 1, 12),
        (2030, 7, 1, 12),
        (2024, 3, 10, 6, 59, 59),
        (2024, 3, 10, 7),
        (2024, 11, 3, 5, 30),
        (2024, 11, 3, 6, 30),
        (2024, 4, 6, 14, 45),
        (2024, 4, 6, 15, 15),
    ]
)
def utc_datetime(request):
    return datetime(*request.param, microsecond=123456, tzinfo=timezone.utc)


@pytest.mark.parametrize("tzinfo", [None, "local"])
def test_fromtimestamp_local_offset(local_timezone, utc_datetime, tzinfo):
    """Local conversion uses the timestamp's offset, including repeated hours."""
    expected = utc_datetime.astimezone(local_timezone)
    result = Arrow.fromtimestamp(utc_datetime.timestamp(), tzinfo=tzinfo)

    assert result.naive == expected.replace(tzinfo=None)
    assert result.utcoffset() == expected.utcoffset()
    assert result.timestamp() == utc_datetime.timestamp()


def test_to_local_offset(local_timezone, utc_datetime):
    """Converting to local time uses the destination offset for this instant."""
    expected = utc_datetime.astimezone(local_timezone)
    result = Arrow.fromdatetime(utc_datetime).to("local")

    assert result.naive == expected.replace(tzinfo=None)
    assert result.utcoffset() == expected.utcoffset()
    assert result.timestamp() == utc_datetime.timestamp()


def test_explicit_timezone_offset(local_timezone, utc_datetime):
    """Named zones and tzinfo objects remain independent of the local timezone."""
    explicit_timezone = ZoneInfo("America/Los_Angeles")
    expected = utc_datetime.astimezone(explicit_timezone)
    for tzinfo in [explicit_timezone, "America/Los_Angeles"]:
        constructed = Arrow.fromtimestamp(utc_datetime.timestamp(), tzinfo=tzinfo)
        converted = Arrow.fromdatetime(utc_datetime).to(tzinfo)
        for result in [constructed, converted]:
            assert result.naive == expected.replace(tzinfo=None)
            assert result.utcoffset() == expected.utcoffset()
            assert result.timestamp() == utc_datetime.timestamp()
            assert result.fold == expected.fold
