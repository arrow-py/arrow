# -*- coding: utf-8 -*-
import pytz
from dateutil.zoneinfo import get_zonefile_instance


def make_full_tz_list():
    dateutil_zones = set(get_zonefile_instance().zones)
    pytz_zones = set(pytz.all_timezones)
    return dateutil_zones.union(pytz_zones)
