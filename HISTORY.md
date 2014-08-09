## History

### 0.4.3

- [NEW] Turkish locale (Emre)
- [NEW] Arabic locale (Mosab Ahmad)
- [NEW] Danish locale (Holmars)
- [NEW] Icelandic locale (Holmars)
- [NEW] Hindi locale (Atmb4u)
- [NEW] Malayalam locale (Atmb4u)
- [NEW] Finnish locale (Stormpat)
- [NEW] Portuguese locale (Danielcorreia)
- [NEW] ``h`` and ``hh`` strings are now supported (Averyonghub)
- [FIX] An incorrect inflection in the Polish locale has been fixed (Avalanchy)
- [FIX] ``arrow.get`` now properly handles ``Date``s (Jaapz)
- [FIX] Tests are now declared in ``setup.py`` and the manifest (Pypingou)
- [FIX] ``__version__`` has been added to ``__init__.py`` (Sametmax)
- [FIX] ISO 8601 strings can be parsed without a separator (Ivandiguisto / Root)
- [FIX] Documentation is now more clear regarding some inputs on ``arrow.get`` (Eriktaubeneck)
- [FIX] Some documentation links have been fixed (Vrutsky)
- [FIX] Error messages for parse errors are now more descriptive (Maciej Albin)
- [FIX] The parser now correctly checks for separators in strings (Mschwager)


### 0.4.2

- [NEW] Factory ``get`` method now accepts a single ``Arrow`` argument.
- [NEW] Tokens SSSS, SSSSS and SSSSSS are supported in parsing.
- [NEW] ``Arrow`` objects have a ``float_timestamp`` property.
- [NEW] Vietnamese locale (Iu1nguoi)
- [NEW] Factory ``get`` method now accepts a list of format strings (Dgilland)
- [NEW] A MANIFEST.in file has been added (Pypingou)
- [NEW] Tests can be run directly from ``setup.py`` (Pypingou)
- [FIX] Arrow docs now list 'day of week' format tokens correctly (Rudolphfroger)
- [FIX] Several issues with the Korean locale have been resolved (Yoloseem)
- [FIX] ``humanize`` now correctly returns unicode (Shvechikov)
- [FIX] ``Arrow`` objects now pickle / unpickle correctly (Yoloseem)

### 0.4.1

- [NEW] Table / explanation of formatting & parsing tokens in docs
- [NEW] Brazilian locale (Augusto2112)
- [NEW] Dutch locale (OrangeTux)
- [NEW] Italian locale (Pertux)
- [NEW] Austrain locale (LeChewbacca)
- [NEW] Tagalog locale (Marksteve)
- [FIX] Corrected spelling and day numbers in German locale (LeChewbacca)
- [FIX] Factory ``get`` method should now handle unicode strings correctly (Bwells)
- [FIX] Midnight and noon should now parse and format correctly (Bwells)

### 0.4.0

- [NEW] Format-free ISO-8601 parsing in factory ``get`` method
- [NEW] Support for 'week' / 'weeks' in ``span``, ``range``, ``span_range``, ``floor`` and ``ceil``
- [NEW] Support for 'weeks' in ``replace``
- [NEW] Norwegian locale (Martinp)
- [NEW] Japanese locale (CortYuming)
- [FIX] Timezones no longer show the wrong sign when formatted (Bean)
- [FIX] Microseconds are parsed correctly from strings (Bsidhom)
- [FIX] Locale day-of-week is no longer off by one (Cynddl)
- [FIX] Corrected plurals of Ukrainian and Russian nouns (Catchagain)
- [CHANGE] Old 0.1 ``arrow`` module method removed
- [CHANGE] Dropped timestamp support in ``range`` and ``span_range`` (never worked correctly) 
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
- [FIX] ``range`` and ``span_range`` respect end and limit parameters correctly
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

