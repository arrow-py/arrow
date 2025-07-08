try:
    import zoneinfo
except ImportError:
    from backports import zoneinfo
from dateutil.zoneinfo import get_zonefile_instance


def make_full_tz_list():
    dateutil_zones = set(get_zonefile_instance().zones)
    zoneinfo_zones = set(zoneinfo.available_timezones())
    # Since the tests create ZoneInfo objects, we can only use timezones
    # that are available in zoneinfo. Filter out any dateutil-only timezones
    # that are not available in zoneinfo (like Asia/Hanoi which was renamed to Asia/Ho_Chi_Minh)
    all_zones = dateutil_zones.union(zoneinfo_zones)
    return {tz for tz in all_zones if tz in zoneinfo_zones}


def assert_datetime_equality(dt1, dt2, within=10):
    # Compare timezone behavior instead of object identity for cross-platform compatibility
    assert_timezone_equivalence(dt1.tzinfo, dt2.tzinfo, dt1)
    assert abs((dt1 - dt2).total_seconds()) < within


def assert_timezone_equivalence(tz1, tz2, dt):
    # Timezone objects are equivalent
    if tz1 == tz2:
        return

    # Compare timezone names
    assert tz1.tzname(dt) == tz2.tzname(dt)

    # Compare UTC offset and DST behavior at the given datetime
    assert tz1.utcoffset(dt) == tz2.utcoffset(
        dt
    ), f"UTC offset mismatch: {tz1.utcoffset(dt)} != {tz2.utcoffset(dt)}"
    assert tz1.dst(dt) == tz2.dst(dt), f"DST mismatch: {tz1.dst(dt)} != {tz2.dst(dt)}"
