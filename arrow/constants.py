import os
from datetime import datetime

# datetime.max.timestamp() errors on Windows, so we must hardcode
# the highest possible datetime value that can output a timestamp.
# tl;dr platform-independent max timestamps are hard to form
# See: https://stackoverflow.com/q/46133223
MAX_TIMESTAMP: float = (
    datetime(3001, 1, 18, 23, 59, 59, 999999) if os.name == "nt" else datetime.max
).timestamp()
MAX_TIMESTAMP_MS: float = MAX_TIMESTAMP * 1000
MAX_TIMESTAMP_US: float = MAX_TIMESTAMP * 1000000
