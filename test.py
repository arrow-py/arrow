import arrow
from datetime import datetime

original = arrow.get(datetime(2013, 5, 7, 12, 30, 36))
earlier = arrow.get(datetime(2013, 5, 7, 12, 30, 30))
later = arrow.get(datetime(2013, 5, 7, 12, 30, 42))
print(original.is_same_or_after(earlier))
print(original.is_same_or_after(original))
print(original.is_same_or_after(later))