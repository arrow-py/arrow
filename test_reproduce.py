import arrow
from datetime import datetime

try:
    # Passing a string that contains a timezone but isn't a full datetime
    # arrow.get('2023-10-10 10:00:00', tzinfo='+03:00.34')
    a = arrow.get(datetime(2023, 10, 10), tzinfo='+03:00.34')
    print(f"Parsed with tzinfo='+03:00.34' as: {a}")
except Exception as e:
    print(f"Failed with tzinfo='+03:00.34': {e}")
