import sys
from datetime import datetime

# datetime.max.timestamp() errors on Windows, so we must hardcode
# the highest possible datetime value that can output a timestamp.
# tl;dr platform-independent max timestamps are hard to form
# See: https://stackoverflow.com/q/46133223
try:
    # Get max timestamp. Works on POSIX-based systems like Linux and macOS,
    # but will trigger an OverflowError, ValueError, or OSError on Windows
    MAX_TIMESTAMP = datetime.max.timestamp()
except (OverflowError, ValueError, OSError):  # pragma: no cover
    # Fallback for Windows if initial max timestamp call fails
    # Must get max value of ctime on Windows based on architecture (x32 vs x64)
    # https://docs.microsoft.com/en-us/cpp/c-runtime-library/reference/ctime-ctime32-ctime64-wctime-wctime32-wctime64
    is_64bits = sys.maxsize > 2 ** 32
    MAX_TIMESTAMP = (
        datetime(3000, 12, 31, 23, 59, 59, 999999).timestamp()
        if is_64bits
        else datetime(2038, 1, 18, 23, 59, 59, 999999).timestamp()
    )

MAX_TIMESTAMP_MS = MAX_TIMESTAMP * 1e3
MAX_TIMESTAMP_US = MAX_TIMESTAMP * 1e6
