import arrow
try:
    a = arrow.get("+03:00.34")
    print(f"Parsed '+03:00.34' as: {a}")
except Exception as e:
    print(f"Failed to parse '+03:00.34': {e}")

try:
    a = arrow.get("2023-10-10T10:00:00+03:00.34")
    print(f"Parsed '2023-10-10T10:00:00+03:00.34' as: {a}")
except Exception as e:
    print(f"Failed to parse '2023-10-10T10:00:00+03:00.34': {e}")
