try:
    import zoneinfo
except ImportError:
    from backports import zoneinfo

from dateutil import tz
from dateutil.zoneinfo import get_zonefile_instance


def make_full_tz_list():
    dateutil_zones = set(get_zonefile_instance().zones)
    zoneinfo_zones = set(zoneinfo.available_timezones())
    return dateutil_zones.union(zoneinfo_zones)


def get_timezone(tzinfo_string):
    """
    Get timezone object using the same logic as the parser.

    This function matches the hybrid approach used in arrow.parser.TzinfoParser.parse()
    to ensure test expectations align with parser behavior.
    """
    # Try zoneinfo first for better cross-platform timezone support
    try:
        return zoneinfo.ZoneInfo(tzinfo_string)
    except zoneinfo.ZoneInfoNotFoundError:
        # Fall back to dateutil for backward compatibility and special cases
        return tz.gettz(tzinfo_string)


def assert_datetime_equality(dt1, dt2, within=10):
    assert dt1.tzinfo == dt2.tzinfo
    assert abs((dt1 - dt2).total_seconds()) < within
