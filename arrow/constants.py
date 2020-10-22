# -*- coding: utf-8 -*-

# Output of time.mktime(datetime.max.timetuple()) on macOS
# This value must be hardcoded for compatibility with Windows
# Platform-independent max timestamps are hard to form
# https://stackoverflow.com/q/46133223
MAX_TIMESTAMP = 253402318799.0
MAX_TIMESTAMP_MS = MAX_TIMESTAMP * 1000
MAX_TIMESTAMP_US = MAX_TIMESTAMP * 1000000

humanize_auto_limits = {
    "now": 10,
    "seconds": 60,
    "minute": 120,
    "minutes": 3600,
    "hour": 7200,
    "hours": 86400,
    "day": 172800,
    "days": 604800,
    "week": 1209600,
    "month": 3888000,
    "months": 31536000,
    "year": 63072000,
}
