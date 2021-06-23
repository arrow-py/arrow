"""Constants used internally in arrow."""

import sys
from datetime import datetime

if sys.version_info < (3, 8):  # pragma: no cover
    from typing_extensions import Final
else:
    from typing import Final  # pragma: no cover

# datetime.max.timestamp() errors on Windows, so we must hardcode
# the highest possible datetime value that can output a timestamp.
# tl;dr platform-independent max timestamps are hard to form
# See: https://stackoverflow.com/q/46133223
try:
    # Get max timestamp. Works on POSIX-based systems like Linux and macOS,
    # but will trigger an OverflowError, ValueError, or OSError on Windows
    _MAX_TIMESTAMP = datetime.max.timestamp()
except (OverflowError, ValueError, OSError):  # pragma: no cover
    # Fallback for Windows and 32-bit systems if initial max timestamp call fails
    # Must get max value of ctime on Windows based on architecture (x32 vs x64)
    # https://docs.microsoft.com/en-us/cpp/c-runtime-library/reference/ctime-ctime32-ctime64-wctime-wctime32-wctime64
    # Note: this may occur on both 32-bit Linux systems (issue #930) along with Windows systems
    is_64bits = sys.maxsize > 2 ** 32
    _MAX_TIMESTAMP = (
        datetime(3000, 1, 1, 23, 59, 59, 999999).timestamp()
        if is_64bits
        else datetime(2038, 1, 1, 23, 59, 59, 999999).timestamp()
    )

MAX_TIMESTAMP: Final[float] = _MAX_TIMESTAMP
MAX_TIMESTAMP_MS: Final[float] = MAX_TIMESTAMP * 1000
MAX_TIMESTAMP_US: Final[float] = MAX_TIMESTAMP * 1_000_000

MAX_ORDINAL: Final[int] = datetime.max.toordinal()
MIN_ORDINAL: Final[int] = 1

DEFAULT_LOCALE: Final[str] = "en-us"

# Supported dehumanize locales
DEHUMANIZE_LOCALES = {
    "en",
    "en-us",
    "en-gb",
    "en-au",
    "en-be",
    "en-jp",
    "en-za",
    "en-ca",
    "en-ph",
    "fr",
    "fr-fr",
    "fr-ca",
    "it",
    "it-it",
    "es",
    "es-es",
    "el",
    "el-gr",
    "ja",
    "ja-jp",
    "se",
    "se-fi",
    "se-no",
    "se-se",
    "sv",
    "sv-se",
    "zh",
    "zh-cn",
    "zh-tw",
    "zh-hk",
    "nl",
    "nl-nl",
    "af",
    "de",
    "de-de",
    "de-ch",
    "de-at",
    "nb",
    "nb-no",
    "nn",
    "nn-no",
    "pt",
    "pt-pt",
    "pt-br",
    "tl",
    "tl-ph",
    "vi",
    "vi-vn",
    "tr",
    "tr-tr",
    "az",
    "az-az",
    "da",
    "da-dk",
    "ml",
    "hi",
    "fa",
    "fa-ir",
    "mr",
    "ca",
    "ca-es",
    "ca-ad",
    "ca-fr",
    "ca-it",
    "eo",
    "eo-xx",
    "bn",
    "bn-bd",
    "bn-in",
    "rm",
    "rm-ch",
    "ro",
    "ro-ro",
    "sl",
    "sl-si",
    "id",
    "id-id",
    "sw",
    "sw-ke",
    "sw-tz",
    "la",
    "la-va",
    "lt",
    "lt-lt",
    "ms",
    "ms-my",
    "ms-bn",
    "or",
    "or-in",
    "lb",
    "lb-lu",
}
