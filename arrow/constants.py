# Output of time.mktime(datetime.max.timetuple()) on macOS
# This value must be hardcoded for compatibility with Windows
# Platform-independent max timestamps are hard to form
# https://stackoverflow.com/q/46133223
import os
from datetime import datetime

if os.name == "nt":  # pragma: no cover
    MAX_TIMESTAMP: float = datetime(3001, 1, 18, 23, 59, 59, 999999).timestamp()
else:  # pragma: no cover
    MAX_TIMESTAMP: float = datetime.max.timestamp()
MAX_TIMESTAMP_MS: float = MAX_TIMESTAMP * 1000
MAX_TIMESTAMP_US: float = MAX_TIMESTAMP * 1000000
