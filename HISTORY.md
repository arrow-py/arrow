## History

### 0.6.0

- [FIX] Added support for Python 3
- [FIX] Avoid truncating oversized epoch timestamps. Fixes #216.
- [FIX] Fixed month abbreviations for Ukrainian
- [FIX] Fix typo timezone
- [FIX] A couple of dialect fixes and two new languages
- [FIX] Spanish locale: `Miercoles` should have acute accent
- [Fix] Fix Finnish grammar
- [FIX] Fix typo in 'Arrow.floor' docstring
- [FIX] Use read() utility to open README
- [FIX] span_range for week frame
- [NEW] Add minimal support for fractional seconds longer than six digits.
- [NEW] Adding locale support for Marathi (mr)
- [NEW] Add count argument to span method
- [NEW] Improved docs


### 0.5.1 - 0.5.4

- [FIX] test the behavior of simplejson instead of calling for_json directly (tonyseek)
- [FIX] Add Hebrew Locale (doodyparizada)
- [FIX] Update documentation location (andrewelkins)
- [FIX] Update setup.py Development Status level (andrewelkins)
- [FIX] Case insensitive month match (cshowe)

### 0.5.0

- [NEW] struct_time addition. (mhworth)
- [NEW] Version grep (eirnym)
- [NEW] Default to ISO-8601 format (emonty)
- [NEW] Raise TypeError on comparison (sniekamp)
- [NEW] Adding Macedonian(mk) locale (krisfremen)
- [FIX] Fix for ISO seconds and fractional seconds (sdispater) (andrewelkins)
- [FIX] Use correct Dutch wording for "hours" (wbolster)
- [FIX] Complete the list of english locales (indorilftw)
- [FIX] Change README to reStructuredText (nyuszika7h)
- [FIX] Parse lower-cased 'h' (tamentis)
- [FIX] Slight modifications to Dutch locale (nvie)

### 0.4.4

- [NEW] Include the docs in the released tarball
- [NEW] Czech localization Czech localization for Arrow
- [NEW] Add fa_ir to locales
- [FIX] Fixes parsing of time strings with a final Z
- [FIX] Fixes ISO parsing and formatting for fractional seconds
- [FIX] test_fromtimestamp sp
- [FIX] some typos fixed
- [FIX] removed an unused import statement
- [FIX] docs table fix
- [FIX] Issue with specify 'X' template and no template at all to arrow.get
- [FIX] Fix "import" typo in docs/index.rst
- [FIX] Fix unit tests for zero passed
- [FIX] Update layout.html
- [FIX] In Norwegian and new Norwegian months and weekdays should not be capitalized
- [FIX] Fixed discrepancy between specifying 'X' to arrow.get and specifying no template


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

