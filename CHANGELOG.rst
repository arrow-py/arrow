Changelog
=========

0.17.0 (2020-10-2)
-------------------

- [WARN] Arrow will **drop support** for Python 2.7 and 3.5 in the upcoming 1.0.0 release. This is the last major release to support Python 2.7 and Python 3.5.
- [NEW] Arrow now properly handles imaginary datetimes during DST shifts. For example:

..code-block:: python
    >>> just_before = arrow.get(2013, 3, 31, 1, 55, tzinfo="Europe/Paris")
    >>> just_before.shift(minutes=+10)
    <Arrow [2013-03-31T03:05:00+02:00]>

..code-block:: python
    >>> before = arrow.get("2018-03-10 23:00:00", "YYYY-MM-DD HH:mm:ss", tzinfo="US/Pacific")
    >>> after = arrow.get("2018-03-11 04:00:00", "YYYY-MM-DD HH:mm:ss", tzinfo="US/Pacific")
    >>> result=[(t, t.to("utc")) for t in arrow.Arrow.range("hour", before, after)]
    >>> for r in result:
    ...     print(r)
    ...
    (<Arrow [2018-03-10T23:00:00-08:00]>, <Arrow [2018-03-11T07:00:00+00:00]>)
    (<Arrow [2018-03-11T00:00:00-08:00]>, <Arrow [2018-03-11T08:00:00+00:00]>)
    (<Arrow [2018-03-11T01:00:00-08:00]>, <Arrow [2018-03-11T09:00:00+00:00]>)
    (<Arrow [2018-03-11T03:00:00-07:00]>, <Arrow [2018-03-11T10:00:00+00:00]>)
    (<Arrow [2018-03-11T04:00:00-07:00]>, <Arrow [2018-03-11T11:00:00+00:00]>)

- [NEW] Added ``humanize`` week granularity translation for Tagalog.
- [CHANGE] Calls to the ``timestamp`` property now emit a ``DeprecationWarning``. In a future release, ``timestamp`` will be changed to a method to align with Python's datetime module. If you would like to continue using the property, please change your code to use the ``int_timestamp`` or ``float_timestamp`` properties instead.
- [CHANGE] Expanded and improved Catalan locale.
- [FIX] Fixed a bug that caused ``Arrow.range()`` to incorrectly cut off ranges in certain scenarios when using month, quarter, or year endings.
- [FIX] Fixed a bug that caused day of week token parsing to be case sensitive.
- [INTERNAL] A number of functions were reordered in arrow.py for better organization and grouping of related methods. This change will have no impact on usage.
- [INTERNAL] A minimum tox version is now enforced for compatibility reasons. Contributors must use tox >3.18.0 going forward.

0.16.0 (2020-08-23)
-------------------

- [WARN] Arrow will **drop support** for Python 2.7 and 3.5 in the upcoming 1.0.0 release. The 0.16.x and 0.17.x releases are the last to support Python 2.7 and 3.5.
- [NEW] Implemented `PEP 495 <https://www.python.org/dev/peps/pep-0495/>`_ to handle ambiguous datetimes. This is achieved by the addition of the ``fold`` attribute for Arrow objects. For example:

.. code-block:: python

    >>> before = Arrow(2017, 10, 29, 2, 0, tzinfo='Europe/Stockholm')
    <Arrow [2017-10-29T02:00:00+02:00]>
    >>> before.fold
    0
    >>> before.ambiguous
    True
    >>> after = Arrow(2017, 10, 29, 2, 0, tzinfo='Europe/Stockholm', fold=1)
    <Arrow [2017-10-29T02:00:00+01:00]>
    >>> after = before.replace(fold=1)
    <Arrow [2017-10-29T02:00:00+01:00]>

- [NEW] Added ``normalize_whitespace`` flag to ``arrow.get``. This is useful for parsing log files and/or any files that may contain inconsistent spacing. For example:

.. code-block:: python

    >>> arrow.get("Jun 1 2005     1:33PM", "MMM D YYYY H:mmA", normalize_whitespace=True)
    <Arrow [2005-06-01T13:33:00+00:00]>
    >>> arrow.get("2013-036 \t  04:05:06Z", normalize_whitespace=True)
    <Arrow [2013-02-05T04:05:06+00:00]>

0.15.8 (2020-07-23)
-------------------

- [WARN] Arrow will **drop support** for Python 2.7 and 3.5 in the upcoming 1.0.0 release. The 0.15.x, 0.16.x, and 0.17.x releases are the last to support Python 2.7 and 3.5.
- [NEW] Added ``humanize`` week granularity translation for Czech.
- [FIX] ``arrow.get`` will now pick sane defaults when weekdays are passed with particular token combinations, see `#446 <https://github.com/arrow-py/arrow/issues/446>`_.
- [INTERNAL] Moved arrow to an organization. The repo can now be found `here <https://github.com/arrow-py/arrow>`_.
- [INTERNAL] Started issuing deprecation warnings for Python 2.7 and 3.5.
- [INTERNAL] Added Python 3.9 to CI pipeline.

0.15.7 (2020-06-19)
-------------------

- [NEW] Added a number of built-in format strings. See the `docs <https://arrow.readthedocs.io/#built-in-formats>`_ for a complete list of supported formats. For example:

.. code-block:: python

    >>> arw = arrow.utcnow()
    >>> arw.format(arrow.FORMAT_COOKIE)
    'Wednesday, 27-May-2020 10:30:35 UTC'

- [NEW] Arrow is now fully compatible with Python 3.9 and PyPy3.
- [NEW] Added Makefile, tox.ini, and requirements.txt files to the distribution bundle.
- [NEW] Added French Canadian and Swahili locales.
- [NEW] Added ``humanize`` week granularity translation for Hebrew, Greek, Macedonian, Swedish, Slovak.
- [FIX] ms and μs timestamps are now normalized in ``arrow.get()``, ``arrow.fromtimestamp()``, and ``arrow.utcfromtimestamp()``. For example:

.. code-block:: python

    >>> ts = 1591161115194556
    >>> arw = arrow.get(ts)
    <Arrow [2020-06-03T05:11:55.194556+00:00]>
    >>> arw.timestamp
    1591161115

- [FIX] Refactored and updated Macedonian, Hebrew, Korean, and Portuguese locales.

0.15.6 (2020-04-29)
-------------------

- [NEW] Added support for parsing and formatting `ISO 8601 week dates <https://en.wikipedia.org/wiki/ISO_week_date>`_ via a new token ``W``, for example:

.. code-block:: python

    >>> arrow.get("2013-W29-6", "W")
    <Arrow [2013-07-20T00:00:00+00:00]>
    >>> utc=arrow.utcnow()
    >>> utc
    <Arrow [2020-01-23T18:37:55.417624+00:00]>
    >>> utc.format("W")
    '2020-W04-4'

- [NEW] Formatting with ``x`` token (microseconds) is now possible, for example:

.. code-block:: python

    >>> dt = arrow.utcnow()
    >>> dt.format("x")
    '1585669870688329'
    >>> dt.format("X")
    '1585669870'

- [NEW] Added ``humanize`` week granularity translation for German, Italian, Polish & Taiwanese locales.
- [FIX] Consolidated and simplified German locales.
- [INTERNAL] Moved testing suite from nosetest/Chai to pytest/pytest-mock.
- [INTERNAL] Converted xunit-style setup and teardown functions in tests to pytest fixtures.
- [INTERNAL] Setup Github Actions for CI alongside Travis.
- [INTERNAL] Help support Arrow's future development by donating to the project on `Open Collective <https://opencollective.com/arrow>`_.

0.15.5 (2020-01-03)
-------------------

- [WARN] Python 2 reached EOL on 2020-01-01. arrow will **drop support** for Python 2 in a future release to be decided (see `#739 <https://github.com/arrow-py/arrow/issues/739>`_).
- [NEW] Added bounds parameter to ``span_range``, ``interval`` and ``span`` methods. This allows you to include or exclude the start and end values.
- [NEW] ``arrow.get()`` can now create arrow objects from a timestamp with a timezone, for example:

.. code-block:: python

    >>> arrow.get(1367900664, tzinfo=tz.gettz('US/Pacific'))
    <Arrow [2013-05-06T21:24:24-07:00]>

- [NEW] ``humanize`` can now combine multiple levels of granularity, for example:

.. code-block:: python

    >>> later140 = arrow.utcnow().shift(seconds=+8400)
    >>> later140.humanize(granularity="minute")
    'in 139 minutes'
    >>> later140.humanize(granularity=["hour", "minute"])
    'in 2 hours and 19 minutes'

- [NEW] Added Hong Kong locale (``zh_hk``).
- [NEW] Added ``humanize`` week granularity translation for Dutch.
- [NEW] Numbers are now displayed when using the seconds granularity in ``humanize``.
- [CHANGE] ``range`` now supports both the singular and plural forms of the ``frames`` argument (e.g. day and days).
- [FIX] Improved parsing of strings that contain punctuation.
- [FIX] Improved behaviour of ``humanize`` when singular seconds are involved.

0.15.4 (2019-11-02)
-------------------

- [FIX] Fixed an issue that caused package installs to fail on Conda Forge.

0.15.3 (2019-11-02)
-------------------

- [NEW] ``factory.get()`` can now create arrow objects from a ISO calendar tuple, for example:

.. code-block:: python

    >>> arrow.get((2013, 18, 7))
    <Arrow [2013-05-05T00:00:00+00:00]>

- [NEW] Added a new token ``x`` to allow parsing of integer timestamps with milliseconds and microseconds.
- [NEW] Formatting now supports escaping of characters using the same syntax as parsing, for example:

.. code-block:: python

    >>> arw = arrow.now()
    >>> fmt = "YYYY-MM-DD h [h] m"
    >>> arw.format(fmt)
    '2019-11-02 3 h 32'

- [NEW] Added ``humanize`` week granularity translations for Chinese, Spanish and Vietnamese.
- [CHANGE] Added ``ParserError`` to module exports.
- [FIX] Added support for midnight at end of day. See `#703 <https://github.com/arrow-py/arrow/issues/703>`_ for details.
- [INTERNAL] Created Travis build for macOS.
- [INTERNAL] Test parsing and formatting against full timezone database.

0.15.2 (2019-09-14)
-------------------

- [NEW] Added ``humanize`` week granularity translations for Portuguese and Brazilian Portuguese.
- [NEW] Embedded changelog within docs and added release dates to versions.
- [FIX] Fixed a bug that caused test failures on Windows only, see `#668 <https://github.com/arrow-py/arrow/issues/668>`_ for details.

0.15.1 (2019-09-10)
-------------------

- [NEW] Added ``humanize`` week granularity translations for Japanese.
- [FIX] Fixed a bug that caused Arrow to fail when passed a negative timestamp string.
- [FIX] Fixed a bug that caused Arrow to fail when passed a datetime object with ``tzinfo`` of type ``StaticTzInfo``.

0.15.0 (2019-09-08)
-------------------

- [NEW] Added support for DDD and DDDD ordinal date tokens. The following functionality is now possible: ``arrow.get("1998-045")``, ``arrow.get("1998-45", "YYYY-DDD")``, ``arrow.get("1998-045", "YYYY-DDDD")``.
- [NEW] ISO 8601 basic format for dates and times is now supported (e.g. ``YYYYMMDDTHHmmssZ``).
- [NEW] Added ``humanize`` week granularity translations for French, Russian and Swiss German locales.
- [CHANGE] Timestamps of type ``str`` are no longer supported **without a format string** in the ``arrow.get()`` method. This change was made to support the ISO 8601 basic format and to address bugs such as `#447 <https://github.com/arrow-py/arrow/issues/447>`_.

The following will NOT work in v0.15.0:

.. code-block:: python

    >>> arrow.get("1565358758")
    >>> arrow.get("1565358758.123413")

The following will work in v0.15.0:

.. code-block:: python

    >>> arrow.get("1565358758", "X")
    >>> arrow.get("1565358758.123413", "X")
    >>> arrow.get(1565358758)
    >>> arrow.get(1565358758.123413)

- [CHANGE] When a meridian token (a|A) is passed and no meridians are available for the specified locale (e.g. unsupported or untranslated) a ``ParserError`` is raised.
- [CHANGE] The timestamp token (``X``) will now match float timestamps of type ``str``: ``arrow.get(“1565358758.123415”, “X”)``.
- [CHANGE] Strings with leading and/or trailing whitespace will no longer be parsed without a format string. Please see `the docs <https://arrow.readthedocs.io/#regular-expressions>`_ for ways to handle this.
- [FIX] The timestamp token (``X``) will now only match on strings that **strictly contain integers and floats**, preventing incorrect matches.
- [FIX] Most instances of ``arrow.get()`` returning an incorrect ``Arrow`` object from a partial parsing match have been eliminated. The following issue have been addressed: `#91 <https://github.com/arrow-py/arrow/issues/91>`_, `#196 <https://github.com/arrow-py/arrow/issues/196>`_, `#396 <https://github.com/arrow-py/arrow/issues/396>`_, `#434 <https://github.com/arrow-py/arrow/issues/434>`_, `#447 <https://github.com/arrow-py/arrow/issues/447>`_, `#456 <https://github.com/arrow-py/arrow/issues/456>`_, `#519 <https://github.com/arrow-py/arrow/issues/519>`_, `#538 <https://github.com/arrow-py/arrow/issues/538>`_, `#560 <https://github.com/arrow-py/arrow/issues/560>`_.

0.14.7 (2019-09-04)
-------------------

- [CHANGE] ``ArrowParseWarning`` will no longer be printed on every call to ``arrow.get()`` with a datetime string. The purpose of the warning was to start a conversation about the upcoming 0.15.0 changes and we appreciate all the feedback that the community has given us!

0.14.6 (2019-08-28)
-------------------

- [NEW] Added support for ``week`` granularity in ``Arrow.humanize()``. For example, ``arrow.utcnow().shift(weeks=-1).humanize(granularity="week")`` outputs "a week ago". This change introduced two new untranslated words, ``week`` and ``weeks``, to all locale dictionaries, so locale contributions are welcome!
- [NEW] Fully translated the Brazilian Portugese locale.
- [CHANGE] Updated the Macedonian locale to inherit from a Slavic base.
- [FIX] Fixed a bug that caused ``arrow.get()`` to ignore tzinfo arguments of type string (e.g. ``arrow.get(tzinfo="Europe/Paris")``).
- [FIX] Fixed a bug that occurred when ``arrow.Arrow()`` was instantiated with a ``pytz`` tzinfo object.
- [FIX] Fixed a bug that caused Arrow to fail when passed a sub-second token, that when rounded, had a value greater than 999999 (e.g. ``arrow.get("2015-01-12T01:13:15.9999995")``). Arrow should now accurately propagate the rounding for large sub-second tokens.

0.14.5 (2019-08-09)
-------------------

- [NEW] Added Afrikaans locale.
- [CHANGE] Removed deprecated ``replace`` shift functionality. Users looking to pass plural properties to the ``replace`` function to shift values should use ``shift`` instead.
- [FIX] Fixed bug that occurred when ``factory.get()`` was passed a locale kwarg.

0.14.4 (2019-07-30)
-------------------

- [FIX] Fixed a regression in 0.14.3 that prevented a tzinfo argument of type string to be passed to the ``get()`` function. Functionality such as ``arrow.get("2019072807", "YYYYMMDDHH", tzinfo="UTC")`` should work as normal again.
- [CHANGE] Moved ``backports.functools_lru_cache`` dependency from ``extra_requires`` to ``install_requires`` for ``Python 2.7`` installs to fix `#495 <https://github.com/arrow-py/arrow/issues/495>`_.

0.14.3 (2019-07-28)
-------------------

- [NEW] Added full support for Python 3.8.
- [CHANGE] Added warnings for upcoming factory.get() parsing changes in 0.15.0. Please see `#612 <https://github.com/arrow-py/arrow/issues/612>`_ for full details.
- [FIX] Extensive refactor and update of documentation.
- [FIX] factory.get() can now construct from kwargs.
- [FIX] Added meridians to Spanish Locale.

0.14.2 (2019-06-06)
-------------------

- [CHANGE] Travis CI builds now use tox to lint and run tests.
- [FIX] Fixed UnicodeDecodeError on certain locales (#600).

0.14.1 (2019-06-06)
-------------------

- [FIX] Fixed ``ImportError: No module named 'dateutil'`` (#598).

0.14.0 (2019-06-06)
-------------------

- [NEW] Added provisional support for Python 3.8.
- [CHANGE] Removed support for EOL Python 3.4.
- [FIX] Updated setup.py with modern Python standards.
- [FIX] Upgraded dependencies to latest versions.
- [FIX] Enabled flake8 and black on travis builds.
- [FIX] Formatted code using black and isort.

0.13.2 (2019-05-30)
-------------------

- [NEW] Add is_between method.
- [FIX] Improved humanize behaviour for near zero durations (#416).
- [FIX] Correct humanize behaviour with future days (#541).
- [FIX] Documentation updates.
- [FIX] Improvements to German Locale.

0.13.1 (2019-02-17)
-------------------

- [NEW] Add support for Python 3.7.
- [CHANGE] Remove deprecation decorators for Arrow.range(), Arrow.span_range() and Arrow.interval(), all now return generators, wrap with list() to get old behavior.
- [FIX] Documentation and docstring updates.

0.13.0 (2019-01-09)
-------------------

- [NEW] Added support for Python 3.6.
- [CHANGE] Drop support for Python 2.6/3.3.
- [CHANGE] Return generator instead of list for Arrow.range(), Arrow.span_range() and Arrow.interval().
- [FIX] Make arrow.get() work with str & tzinfo combo.
- [FIX] Make sure special RegEx characters are escaped in format string.
- [NEW] Added support for ZZZ when formatting.
- [FIX] Stop using datetime.utcnow() in internals, use datetime.now(UTC) instead.
- [FIX] Return NotImplemented instead of TypeError in arrow math internals.
- [NEW] Added Estonian Locale.
- [FIX] Small fixes to Greek locale.
- [FIX] TagalogLocale improvements.
- [FIX] Added test requirements to setup.
- [FIX] Improve docs for get, now and utcnow methods.
- [FIX] Correct typo in depreciation warning.

0.12.1
------

- [FIX] Allow universal wheels to be generated and reliably installed.
- [FIX] Make humanize respect only_distance when granularity argument is also given.

0.12.0
------

- [FIX] Compatibility fix for Python 2.x

0.11.0
------

- [FIX] Fix grammar of ArabicLocale
- [NEW] Add Nepali Locale
- [FIX] Fix month name + rename AustriaLocale -> AustrianLocale
- [FIX] Fix typo in Basque Locale
- [FIX] Fix grammar in PortugueseBrazilian locale
- [FIX] Remove pip --user-mirrors flag
- [NEW] Add Indonesian Locale

0.10.0
------

- [FIX] Fix getattr off by one for quarter
- [FIX] Fix negative offset for UTC
- [FIX] Update arrow.py

0.9.0
-----

- [NEW] Remove duplicate code
- [NEW] Support gnu date iso 8601
- [NEW] Add support for universal wheels
- [NEW] Slovenian locale
- [NEW] Slovak locale
- [NEW] Romanian locale
- [FIX] respect limit even if end is defined range
- [FIX] Separate replace & shift functions
- [NEW] Added tox
- [FIX] Fix supported Python versions in documentation
- [NEW] Azerbaijani locale added, locale issue fixed in Turkish.
- [FIX] Format ParserError's raise message

0.8.0
-----

- []

0.7.1
-----

- [NEW] Esperanto locale (batisteo)

0.7.0
-----

- [FIX] Parse localized strings #228 (swistakm)
- [FIX] Modify tzinfo parameter in ``get`` api #221 (bottleimp)
- [FIX] Fix Czech locale (PrehistoricTeam)
- [FIX] Raise TypeError when adding/subtracting non-dates (itsmeolivia)
- [FIX] Fix pytz conversion error (Kudo)
- [FIX] Fix overzealous time truncation in span_range (kdeldycke)
- [NEW] Humanize for time duration #232 (ybrs)
- [NEW] Add Thai locale (sipp11)
- [NEW] Adding Belarusian (be) locale (oire)
- [NEW] Search date in strings (beenje)
- [NEW] Note that arrow's tokens differ from strptime's. (offby1)

0.6.0
-----

- [FIX] Added support for Python 3
- [FIX] Avoid truncating oversized epoch timestamps. Fixes #216.
- [FIX] Fixed month abbreviations for Ukrainian
- [FIX] Fix typo timezone
- [FIX] A couple of dialect fixes and two new languages
- [FIX] Spanish locale: ``Miercoles`` should have acute accent
- [Fix] Fix Finnish grammar
- [FIX] Fix typo in 'Arrow.floor' docstring
- [FIX] Use read() utility to open README
- [FIX] span_range for week frame
- [NEW] Add minimal support for fractional seconds longer than six digits.
- [NEW] Adding locale support for Marathi (mr)
- [NEW] Add count argument to span method
- [NEW] Improved docs

0.5.1 - 0.5.4
-------------

- [FIX] test the behavior of simplejson instead of calling for_json directly (tonyseek)
- [FIX] Add Hebrew Locale (doodyparizada)
- [FIX] Update documentation location (andrewelkins)
- [FIX] Update setup.py Development Status level (andrewelkins)
- [FIX] Case insensitive month match (cshowe)

0.5.0
-----

- [NEW] struct_time addition. (mhworth)
- [NEW] Version grep (eirnym)
- [NEW] Default to ISO 8601 format (emonty)
- [NEW] Raise TypeError on comparison (sniekamp)
- [NEW] Adding Macedonian(mk) locale (krisfremen)
- [FIX] Fix for ISO seconds and fractional seconds (sdispater) (andrewelkins)
- [FIX] Use correct Dutch wording for "hours" (wbolster)
- [FIX] Complete the list of english locales (indorilftw)
- [FIX] Change README to reStructuredText (nyuszika7h)
- [FIX] Parse lower-cased 'h' (tamentis)
- [FIX] Slight modifications to Dutch locale (nvie)

0.4.4
-----

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

0.4.3
-----

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
- [FIX] ``arrow.get`` now properly handles ``Date`` (Jaapz)
- [FIX] Tests are now declared in ``setup.py`` and the manifest (Pypingou)
- [FIX] ``__version__`` has been added to ``__init__.py`` (Sametmax)
- [FIX] ISO 8601 strings can be parsed without a separator (Ivandiguisto / Root)
- [FIX] Documentation is now more clear regarding some inputs on ``arrow.get`` (Eriktaubeneck)
- [FIX] Some documentation links have been fixed (Vrutsky)
- [FIX] Error messages for parse errors are now more descriptive (Maciej Albin)
- [FIX] The parser now correctly checks for separators in strings (Mschwager)

0.4.2
-----

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

0.4.1
-----

- [NEW] Table / explanation of formatting & parsing tokens in docs
- [NEW] Brazilian locale (Augusto2112)
- [NEW] Dutch locale (OrangeTux)
- [NEW] Italian locale (Pertux)
- [NEW] Austrain locale (LeChewbacca)
- [NEW] Tagalog locale (Marksteve)
- [FIX] Corrected spelling and day numbers in German locale (LeChewbacca)
- [FIX] Factory ``get`` method should now handle unicode strings correctly (Bwells)
- [FIX] Midnight and noon should now parse and format correctly (Bwells)

0.4.0
-----

- [NEW] Format-free ISO 8601 parsing in factory ``get`` method
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
- [CHANGE] Dropped parsing of single string as tz string in factory ``get`` method (replaced by ISO 8601)

0.3.5
-----

- [NEW] French locale (Cynddl)
- [NEW] Spanish locale (Slapresta)
- [FIX] Ranges handle multiple timezones correctly (Ftobia)

0.3.4
-----

- [FIX] Humanize no longer sometimes returns the wrong month delta
- [FIX] ``__format__`` works correctly with no format string

0.3.3
-----

- [NEW] Python 2.6 support
- [NEW] Initial support for locale-based parsing and formatting
- [NEW] ArrowFactory class, now proxied as the module API
- [NEW] ``factory`` api method to obtain a factory for a custom type
- [FIX] Python 3 support and tests completely ironed out

0.3.2
-----

- [NEW] Python 3+ support

0.3.1
-----

- [FIX] The old ``arrow`` module function handles timestamps correctly as it used to

0.3.0
-----

- [NEW] ``Arrow.replace`` method
- [NEW] Accept timestamps, datetimes and Arrows for datetime inputs, where reasonable
- [FIX] ``range`` and ``span_range`` respect end and limit parameters correctly
- [CHANGE] Arrow objects are no longer mutable
- [CHANGE] Plural attribute name semantics altered: single -> absolute, plural -> relative
- [CHANGE] Plural names no longer supported as properties (e.g. ``arrow.utcnow().years``)

0.2.1
-----

- [NEW] Support for localized humanization
- [NEW] English, Russian, Greek, Korean, Chinese locales

0.2.0
-----

- **REWRITE**
- [NEW] Date parsing
- [NEW] Date formatting
- [NEW] ``floor``, ``ceil`` and ``span`` methods
- [NEW] ``datetime`` interface implementation
- [NEW] ``clone`` method
- [NEW] ``get``, ``now`` and ``utcnow`` API methods

0.1.6
-----

- [NEW] Humanized time deltas
- [NEW] ``__eq__`` implemented
- [FIX] Issues with conversions related to daylight savings time resolved
- [CHANGE] ``__str__`` uses ISO formatting

0.1.5
-----

- **Started tracking changes**
- [NEW] Parsing of ISO-formatted time zone offsets (e.g. '+02:30', '-05:00')
- [NEW] Resolved some issues with timestamps and delta / Olson time zones
