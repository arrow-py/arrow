# Output of time.mktime(datetime.max.timetuple()) on macOS
# This value must be hardcoded for compatibility with Windows
# Platform-independent max timestamps are hard to form
# https://stackoverflow.com/q/46133223
import os
from datetime import datetime

if os.name == "nt":  # type: ignore
    MAX_TIMESTAMP = datetime(3001, 1, 18, 23, 59, 59, 999999).timestamp()
else:
    MAX_TIMESTAMP = datetime.max.timestamp()
MAX_TIMESTAMP_MS = MAX_TIMESTAMP * 1000
MAX_TIMESTAMP_US = MAX_TIMESTAMP * 1000000
