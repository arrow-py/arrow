# Output of time.mktime(datetime.max.timetuple()) on macOS
# This value must be hardcoded for compatibility with Windows
# Platform-independent max timestamps are hard to form
# https://stackoverflow.com/q/46133223
from datetime import datetime

MAX_TIMESTAMP = datetime.max.timestamp()
MAX_TIMESTAMP_MS = MAX_TIMESTAMP * 1000
MAX_TIMESTAMP_US = MAX_TIMESTAMP * 1000000
