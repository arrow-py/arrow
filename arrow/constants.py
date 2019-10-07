# -*- coding: utf-8 -*-

# Output of time.mktime(datetime.max.timetuple()) on macOS
# This value must be hardcoded for compatibility with Windows
# Platform-independent max timestamps are hard to form
# https://stackoverflow.com/q/46133223
MAX_TIMESTAMP = 253402318799.0
MAX_TIMESTAMP_MS = MAX_TIMESTAMP * 1000
MAX_TIMESTAMP_US = MAX_TIMESTAMP * 1000000
