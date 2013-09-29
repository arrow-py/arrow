History
-------

0.4.0
+++++

- [ADDED] Format-free ISO-8601 parsing in factory .get method
- [ADDED] Support for 'week' / 'weeks' in .span, .range, .span_range, .floor and .ceil
- [ADDED] Suppott for 'weeks' in .replace
- [ADDED] Norwegian locale (Martinp)
- [ADDED] Japanese locale (CortYuming)
- [BUGFIX] Fixed wrong sign on formatted timezones (Bean)
- [BUGFIX] Fixed issues w/ microsecond parsing (Bsidhom)
- [BUGFIX] Fixed day of week number in locales (Cynddl)
- [REMOVED] Old 0.1 .arrow module method

0.3.5
+++++

- Fix for losing source timezones in range calculation (Ftobia)
- French locale added (Cynddl)
- Spanish locale added (Slapresta)
 

0.3.4
+++++

- Fix for incorrect month delta in .humanize
- Fix for empty result when using str.format and no format string

0.3.3
+++++

- Python 2.6 and 3.3 fully supported, including tests
- Initial support for locale-based parsing and formatting
- ArrowFactory class, now proxied as the module API
- arrow.factory() method to obtain a factory for a custom type

0.3.2
+++++

- Python 3.0 support / fixes

0.3.1
+++++

- Fix for incorrect timestamp handling in old arrow function (for old API compatibility)

0.3.0
+++++

- Arrow objects are no longer mutable
- Arrow.replace method
- Plural attribute name semantics altered: single -> absolute, plural -> relative
- Plural names no longer supported as properties (e.g. arrow.utcnow().years)
- Limit parameters are respected in range and span_range
- Accept timestamps, datetimes and Arrows for datetime inputs, where reasonable

0.2.1
+++++

- Support for localized humanization
- English, Russian, Greek, Korean, Chinese locales

0.2.0
+++++

- Rewrite, re-implemented as datetime replacement
- Added date parsing
- Added date formatting
- Added floor, ceil and span methods
- Added datetime methods for drop-in replacement
- Added clone method
- Added get, now and utcnow API methods

0.1.6
+++++

- Added humanized time deltas
- Fixed numerous issues with conversions related to daylight savings time
- Fixed some inconsistencies in time zone names
- __str__ uses ISO formatting
- __eq__ implemented for basic comparison between Arrow objects

0.1.5
+++++

- Started tracking changes
- Added parsing of ISO-formatted time zone offsets (e.g. '+02:30', '-05:00')
- Fixed some incorrect timestamps with delta / olson time zones
- Fixed formatting of UTC offsets in TimeStamp's str method

