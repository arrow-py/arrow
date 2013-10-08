## History


### 0.4.0

- [NEW] Format-free ISO-8601 parsing in factory ``get`` method
- [NEW] Support for 'week' / 'weeks' in ``span``, ``range``, ``span_range``, ``floor`` and ``ceil``
- [NEW] Support for 'weeks' in ``replace``
- [NEW] Norwegian locale (Martinp)
- [NEW] Japanese locale (CortYuming)
- [FIX] Timezones no longer show the wrong sign when formatted (Bean)
- [FIX] Microseconds are parsed correctly from strings (Bsidhom)
- [FIX] Locale day-of-week is no longer off by one (Cynddl)
- [FIX] Corrected plurals of Ukranian and Russina nouns (Catchagain)
- [CHANGE] Old 0.1 ``arrow`` module method removed
- [CHANGE] Timestamp support in ``range`` and ``span_range`` (never worked correctly) 
- [CHANGE] Dropped parsing of single string as tz string in factory ``get`` method (replaced by ISO-8601) 

### 0.3.5

- [NEW] French locale (Cynddl)
- [NEW] Spanish locale (Slapresta)
- [FIX] Ranges handle multiple timezones correctly (Ftobia)
 
### 0.3.4

- [FIX] Humanize no longer sometimes returns the wrong month delta
- [FIX] ``__format__`` works correctly with no format string

### 0.3.3

- [NEW] Python 2.6 support
- [NEW] Initial support for locale-based parsing and formatting
- [NEW] ArrowFactory class, now proxied as the module API
- [NEW] ``factory`` api method to obtain a factory for a custom type
- [FIX] Python 3 support and tests completely ironed out 

### 0.3.2

- [NEW] Python 3+ support

### 0.3.1

- [FIX] The old ``arrow`` module function handles timestamps correctly as it used to

### 0.3.0

- [NEW] ``Arrow.replace`` method
- [NEW] Accept timestamps, datetimes and Arrows for datetime inputs, where reasonable
- [FIX] ``range`` and ``span_range`` respect end and limit paremters correctly
- [CHANGE] Arrow objects are no longer mutable
- [CHANGE] Plural attribute name semantics altered: single -> absolute, plural -> relative
- [CHANGE] Plural names no longer supported as properties (e.g. ``arrow.utcnow().years``)

### 0.2.1

- [NEW] Support for localized humanization
- [NEW] English, Russian, Greek, Korean, Chinese locales

### 0.2.0

- **REWRITE**
- [NEW] Date parsing
- [NEW] Date formatting
- [NEW] ``floor``, ``ceil`` and ``span`` methods
- [NEW] ``datetime`` interface implementation 
- [NEW] ``clone`` method
- [NEW] ``get``, ``now`` and ``utcnow`` API methods

### 0.1.6

- [NEW] Humanized time deltas
- [NEW] ``__eq__`` implemented
- [FIX] Issues with conversions related to daylight savings time resolved
- [CHANGE] ``__str__`` uses ISO formatting

### 0.1.5

- **Started tracking changes**
- [NEW] Parsing of ISO-formatted time zone offsets (e.g. '+02:30', '-05:00')
- [NEW] Resolved some issues with timestamps and delta / Olson time zones

