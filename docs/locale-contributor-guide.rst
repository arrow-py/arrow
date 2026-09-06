Locale implementation guide
===========================

Locales provide the words and formatting rules used by Arrow's formatting,
parsing and humanization APIs. To add or update one, start with ``Locale`` and
``EnglishLocale`` in ``arrow/locales.py`` and the corresponding tests in
``tests/test_locales.py``. Use language references or a fluent speaker to check
translations; passing tests alone cannot establish linguistic accuracy.

Implementation checklist
------------------------

* Add a ``Locale`` subclass in ``arrow/locales.py``, or update an existing one.
  Reuse inherited behaviour where it fits the language.
* Set ``names`` to the supported aliases in lower case, using hyphens, for
  example ``["en", "en-us"]``. Subclasses register automatically; do not edit
  ``_locale_map``. Each alias must be unique. ``get_locale()`` accepts case and
  underscore variants, so ``EN_US`` resolves to ``en-us``.
* Define ``past`` and ``future`` around a ``{0}`` placeholder for the complete
  distance phrase, such as ``"{0} ago"`` and ``"in {0}"``. Negative deltas use
  ``past``; non-negative deltas use ``future``. The base implementation leaves
  ``now`` unwrapped, and ``only_distance=True`` omits the relative wrapper.
* Set ``and_word`` if the language needs a conjunction between the final two
  parts of a multi-unit distance. The default ``None`` joins parts with spaces.
* Fill ``timeframes`` using the keys in ``TimeFrameLiteral``: ``now`` and the
  singular/plural pairs from ``second``/``seconds`` through ``year``/``years``,
  including weeks and quarters. A singular entry must be a complete phrase
  (English ``"a week"``, not ``"week"``); a plural template uses ``{0}`` for the
  count. Keep relative wording in the wrapper unless the language requires
  different forms. Check distance-only output as well as past and future.
* Supply ``month_names`` and ``month_abbreviations`` with 13 entries: an empty
  string at index 0, then January through December at indices 1 through 12.
  Supply ``day_names`` and ``day_abbreviations`` with 8 entries: an empty string
  followed by Monday through Sunday at indices 1 through 7. Keep abbreviations
  in the same order as the full names.
* Check ``meridians`` for the ``am``, ``pm``, ``AM`` and ``PM`` tokens. If the
  language needs ordinal suffixes, follow the existing ``_ordinal_number()``
  and ``ordinal_day_re`` implementations and their formatting/parsing tests.

Timeframe and relative formatting
---------------------------------

``humanize()`` selects a timeframe key before calling ``describe()`` or
``describe_multi()``. Calling ``describe("hours", 1)`` directly does not select
the singular ``hour`` key. The base ``_format_timeframe()`` formats string
templates with an absolute integer count; it does not implement additional
plural rules. If the language needs count- or direction-dependent forms, use
an existing locale with similar rules as a reference and override the relevant
formatting method. A dictionary or list in ``timeframes`` alone does not teach
the base formatter how to select a form.

Prefer inheriting ``describe()`` and ``describe_multi()``. If overriding them,
preserve their handling of ``only_distance`` and truncate each delta with
``math.trunc()`` before passing it to ``_format_timeframe()``. Keep the original
delta for relative direction in ``describe()``. For multiple units, format
each part, join them, then wrap the whole phrase once; the base implementation
uses the first non-zero truncated delta to determine direction. Test fractional
deltas and leading zero units when changing this behaviour.

These examples exercise the existing English locale, without defining or
registering another locale::

    >>> from arrow.locales import get_locale
    >>> locale = get_locale("EN_US")
    >>> locale.describe("week", -1)
    'a week ago'
    >>> locale.describe("weeks", 2)
    'in 2 weeks'
    >>> locale.describe("hours", -2.9, only_distance=True)
    '2 hours'
    >>> locale.describe("now")
    'just now'
    >>> locale.describe_multi([("hours", 0), ("minutes", -2)])
    '0 hours and 2 minutes ago'
    >>> locale.month_name(1), locale.month_abbreviation(12)
    ('January', 'Dec')
    >>> locale.day_name(1), locale.day_abbreviation(7)
    ('Monday', 'Sun')

Dehumanize support
------------------

Registration for formatting and humanization does not enable ``dehumanize()``.
That method reads ``timeframes``, ``past`` and ``future`` directly; it does not
reverse custom formatting methods. It builds regular expressions from those
strings, replacing ``{0}`` in a timeframe with a digit pattern and in a wrapper
with ``.*``. Check that the actual phrases are recognised and that past and
future wrappers distinguish direction, especially if a language omits a
preposition. Do not change valid translations merely to satisfy a round trip.

When the locale supports dehumanization:

* Add its supported aliases to ``DEHUMANIZE_LOCALES`` in ``arrow/constants.py``.
* Add them to ``locale_list_no_weeks`` in ``tests/test_arrow.py`` for the general
  ``TestArrowDehumanize`` tests. Despite its name, this fixture also includes
  locales that support weeks; it is the tests that omit week granularity.
* Also add them to ``locale_list_with_weeks`` when week forms are supported.
  Use the existing ``slavic_locales`` fixture only when its plural-form tests
  apply. Add explicit cases for grammar not exercised by these shared tests.

For example, check both directions with a fixed reference time::

    >>> import arrow
    >>> base = arrow.get(2024, 1, 1)
    >>> past = base.shift(hours=-2)
    >>> future = base.shift(hours=2, minutes=3)
    >>> past.humanize(base, locale="en")
    '2 hours ago'
    >>> base.dehumanize(past.humanize(base, locale="en"), locale="en") == past
    True
    >>> phrase = future.humanize(base, locale="en", granularity=["hour", "minute"])
    >>> phrase
    'in 2 hours and 3 minutes'
    >>> base.dehumanize(phrase, locale="en") == future
    True

Tests and checks
----------------

Add a class named ``Test<LocaleClassName>`` in ``tests/test_locales.py`` with
``@pytest.mark.usefixtures("lang_locale")``. The fixture derives the locale
class name from the test class and sets ``self.locale``. ``TestEnglishLocale``
shows this pattern. The existing ``TestLocaleValidation`` checks registered
aliases and the shape of month/day lists automatically; add assertions for the
actual names, abbreviations and grammar you are contributing.

Cover singular and plural forms, past and future, ``now``, distance-only and
multi-unit output, and every additional plural rule or method override. Use
``tests/test_arrow.py`` for public ``humanize()``/``dehumanize()`` behaviour and
``tests/test_formatter.py`` or ``tests/test_parser.py`` for changes affecting
formatting or parsing.

From the repository root, set up a virtual environment and run the checks::

    python -m venv venv
    . venv/bin/activate
    python -m pip install -r requirements/requirements-tests.txt
    python -m pip install tox
    python -m doctest docs/locale-contributor-guide.rst
    python -m pytest
    tox -e lint,docs

On Windows, activate with ``venv\Scripts\activate`` instead. The full test run
keeps Arrow's configured coverage requirement. For a quick focused check while
editing, run ``python -m pytest --no-cov tests/test_locales.py``; also run
``python -m pytest --no-cov tests/test_arrow.py::TestArrowDehumanize`` when adding
dehumanize support. Run the full checks before submitting a pull request.
