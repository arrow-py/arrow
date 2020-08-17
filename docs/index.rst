Arrow: Better dates & times for Python
======================================

Release v\ |release| (`Installation`_) (`Changelog <releases.html>`_)

.. include:: ../README.rst
  :start-after: start-inclusion-marker-do-not-remove
  :end-before: end-inclusion-marker-do-not-remove

User's Guide
------------

Creation
~~~~~~~~

Get 'now' easily:

.. code-block:: python

    >>> arrow.utcnow()
    <Arrow [2013-05-07T04:20:39.369271+00:00]>

    >>> arrow.now()
    <Arrow [2013-05-06T21:20:40.841085-07:00]>

    >>> arrow.now('US/Pacific')
    <Arrow [2013-05-06T21:20:44.761511-07:00]>

Create from timestamps (:code:`int` or :code:`float`):

.. code-block:: python

    >>> arrow.get(1367900664)
    <Arrow [2013-05-07T04:24:24+00:00]>

    >>> arrow.get(1367900664.152325)
    <Arrow [2013-05-07T04:24:24.152325+00:00]>

Use a naive or timezone-aware datetime, or flexibly specify a timezone:

.. code-block:: python

    >>> arrow.get(datetime.utcnow())
    <Arrow [2013-05-07T04:24:24.152325+00:00]>

    >>> arrow.get(datetime(2013, 5, 5), 'US/Pacific')
    <Arrow [2013-05-05T00:00:00-07:00]>

    >>> from dateutil import tz
    >>> arrow.get(datetime(2013, 5, 5), tz.gettz('US/Pacific'))
    <Arrow [2013-05-05T00:00:00-07:00]>

    >>> arrow.get(datetime.now(tz.gettz('US/Pacific')))
    <Arrow [2013-05-06T21:24:49.552236-07:00]>

Parse from a string:

.. code-block:: python

    >>> arrow.get('2013-05-05 12:30:45', 'YYYY-MM-DD HH:mm:ss')
    <Arrow [2013-05-05T12:30:45+00:00]>

Search a date in a string:

.. code-block:: python

    >>> arrow.get('June was born in May 1980', 'MMMM YYYY')
    <Arrow [1980-05-01T00:00:00+00:00]>

Some ISO 8601 compliant strings are recognized and parsed without a format string:

    >>> arrow.get('2013-09-30T15:34:00.000-07:00')
    <Arrow [2013-09-30T15:34:00-07:00]>

Arrow objects can be instantiated directly too, with the same arguments as a datetime:

.. code-block:: python

    >>> arrow.get(2013, 5, 5)
    <Arrow [2013-05-05T00:00:00+00:00]>

    >>> arrow.Arrow(2013, 5, 5)
    <Arrow [2013-05-05T00:00:00+00:00]>

Properties
~~~~~~~~~~

Get a datetime or timestamp representation:

.. code-block:: python

    >>> a = arrow.utcnow()
    >>> a.datetime
    datetime.datetime(2013, 5, 7, 4, 38, 15, 447644, tzinfo=tzutc())

    >>> a.timestamp
    1367901495

Get a naive datetime, and tzinfo:

.. code-block:: python

    >>> a.naive
    datetime.datetime(2013, 5, 7, 4, 38, 15, 447644)

    >>> a.tzinfo
    tzutc()

Get any datetime value:

.. code-block:: python

    >>> a.year
    2013

Call datetime functions that return properties:

.. code-block:: python

    >>> a.date()
    datetime.date(2013, 5, 7)

    >>> a.time()
    datetime.time(4, 38, 15, 447644)

Replace & Shift
~~~~~~~~~~~~~~~

Get a new :class:`Arrow <arrow.arrow.Arrow>` object, with altered attributes, just as you would with a datetime:

.. code-block:: python

    >>> arw = arrow.utcnow()
    >>> arw
    <Arrow [2013-05-12T03:29:35.334214+00:00]>

    >>> arw.replace(hour=4, minute=40)
    <Arrow [2013-05-12T04:40:35.334214+00:00]>

Or, get one with attributes shifted forward or backward:

.. code-block:: python

    >>> arw.shift(weeks=+3)
    <Arrow [2013-06-02T03:29:35.334214+00:00]>

Even replace the timezone without altering other attributes:

.. code-block:: python

    >>> arw.replace(tzinfo='US/Pacific')
    <Arrow [2013-05-12T03:29:35.334214-07:00]>

Move between the earlier and later moments of an ambiguous time:

.. code-block:: python

    >>> paris_transition = arrow.Arrow(2019, 10, 27, 2, tzinfo="Europe/Paris", fold=0)
    >>> paris_transition
    <Arrow [2019-10-27T02:00:00+02:00]>
    >>> paris_transition.ambiguous
    True
    >>> paris_transition.replace(fold=1)
    <Arrow [2019-10-27T02:00:00+01:00]>

Format
~~~~~~

.. code-block:: python

    >>> arrow.utcnow().format('YYYY-MM-DD HH:mm:ss ZZ')
    '2013-05-07 05:23:16 -00:00'

Convert
~~~~~~~

Convert from UTC to other timezones by name or tzinfo:

.. code-block:: python

    >>> utc = arrow.utcnow()
    >>> utc
    <Arrow [2013-05-07T05:24:11.823627+00:00]>

    >>> utc.to('US/Pacific')
    <Arrow [2013-05-06T22:24:11.823627-07:00]>

    >>> utc.to(tz.gettz('US/Pacific'))
    <Arrow [2013-05-06T22:24:11.823627-07:00]>

Or using shorthand:

.. code-block:: python

    >>> utc.to('local')
    <Arrow [2013-05-06T22:24:11.823627-07:00]>

    >>> utc.to('local').to('utc')
    <Arrow [2013-05-07T05:24:11.823627+00:00]>


Humanize
~~~~~~~~

Humanize relative to now:

.. code-block:: python

    >>> past = arrow.utcnow().shift(hours=-1)
    >>> past.humanize()
    'an hour ago'

Or another Arrow, or datetime:

.. code-block:: python

    >>> present = arrow.utcnow()
    >>> future = present.shift(hours=2)
    >>> future.humanize(present)
    'in 2 hours'

Indicate time as relative or include only the distance

.. code-block:: python

    >>> present = arrow.utcnow()
    >>> future = present.shift(hours=2)
    >>> future.humanize(present)
    'in 2 hours'
    >>> future.humanize(present, only_distance=True)
    '2 hours'


Indicate a specific time granularity (or multiple):

.. code-block:: python

    >>> present = arrow.utcnow()
    >>> future = present.shift(minutes=66)
    >>> future.humanize(present, granularity="minute")
    'in 66 minutes'
    >>> future.humanize(present, granularity=["hour", "minute"])
    'in an hour and 6 minutes'
    >>> present.humanize(future, granularity=["hour", "minute"])
    'an hour and 6 minutes ago'
    >>> future.humanize(present, only_distance=True, granularity=["hour", "minute"])
    'an hour and 6 minutes'

Support for a growing number of locales (see ``locales.py`` for supported languages):

.. code-block:: python


    >>> future = arrow.utcnow().shift(hours=1)
    >>> future.humanize(a, locale='ru')
    'через 2 час(а,ов)'


Ranges & Spans
~~~~~~~~~~~~~~

Get the time span of any unit:

.. code-block:: python

    >>> arrow.utcnow().span('hour')
    (<Arrow [2013-05-07T05:00:00+00:00]>, <Arrow [2013-05-07T05:59:59.999999+00:00]>)

Or just get the floor and ceiling:

.. code-block:: python

    >>> arrow.utcnow().floor('hour')
    <Arrow [2013-05-07T05:00:00+00:00]>

    >>> arrow.utcnow().ceil('hour')
    <Arrow [2013-05-07T05:59:59.999999+00:00]>

You can also get a range of time spans:

.. code-block:: python

    >>> start = datetime(2013, 5, 5, 12, 30)
    >>> end = datetime(2013, 5, 5, 17, 15)
    >>> for r in arrow.Arrow.span_range('hour', start, end):
    ...     print r
    ...
    (<Arrow [2013-05-05T12:00:00+00:00]>, <Arrow [2013-05-05T12:59:59.999999+00:00]>)
    (<Arrow [2013-05-05T13:00:00+00:00]>, <Arrow [2013-05-05T13:59:59.999999+00:00]>)
    (<Arrow [2013-05-05T14:00:00+00:00]>, <Arrow [2013-05-05T14:59:59.999999+00:00]>)
    (<Arrow [2013-05-05T15:00:00+00:00]>, <Arrow [2013-05-05T15:59:59.999999+00:00]>)
    (<Arrow [2013-05-05T16:00:00+00:00]>, <Arrow [2013-05-05T16:59:59.999999+00:00]>)

Or just iterate over a range of time:

.. code-block:: python

    >>> start = datetime(2013, 5, 5, 12, 30)
    >>> end = datetime(2013, 5, 5, 17, 15)
    >>> for r in arrow.Arrow.range('hour', start, end):
    ...     print repr(r)
    ...
    <Arrow [2013-05-05T12:30:00+00:00]>
    <Arrow [2013-05-05T13:30:00+00:00]>
    <Arrow [2013-05-05T14:30:00+00:00]>
    <Arrow [2013-05-05T15:30:00+00:00]>
    <Arrow [2013-05-05T16:30:00+00:00]>

.. toctree::
   :maxdepth: 2

Factories
~~~~~~~~~

Use factories to harness Arrow's module API for a custom Arrow-derived type.  First, derive your type:

.. code-block:: python

    >>> class CustomArrow(arrow.Arrow):
    ...
    ...     def days_till_xmas(self):
    ...
    ...         xmas = arrow.Arrow(self.year, 12, 25)
    ...
    ...         if self > xmas:
    ...             xmas = xmas.shift(years=1)
    ...
    ...         return (xmas - self).days


Then get and use a factory for it:

.. code-block:: python

    >>> factory = arrow.ArrowFactory(CustomArrow)
    >>> custom = factory.utcnow()
    >>> custom
    >>> <CustomArrow [2013-05-27T23:35:35.533160+00:00]>

    >>> custom.days_till_xmas()
    >>> 211

Supported Tokens
~~~~~~~~~~~~~~~~

Use the following tokens for parsing and formatting. Note that they are **not** the same as the tokens for `strptime <https://linux.die.net/man/3/strptime>`_:

+--------------------------------+--------------+-------------------------------------------+
|                                |Token         |Output                                     |
+================================+==============+===========================================+
|**Year**                        |YYYY          |2000, 2001, 2002 ... 2012, 2013            |
+--------------------------------+--------------+-------------------------------------------+
|                                |YY            |00, 01, 02 ... 12, 13                      |
+--------------------------------+--------------+-------------------------------------------+
|**Month**                       |MMMM          |January, February, March ... [#t1]_        |
+--------------------------------+--------------+-------------------------------------------+
|                                |MMM           |Jan, Feb, Mar ... [#t1]_                   |
+--------------------------------+--------------+-------------------------------------------+
|                                |MM            |01, 02, 03 ... 11, 12                      |
+--------------------------------+--------------+-------------------------------------------+
|                                |M             |1, 2, 3 ... 11, 12                         |
+--------------------------------+--------------+-------------------------------------------+
|**Day of Year**                 |DDDD          |001, 002, 003 ... 364, 365                 |
+--------------------------------+--------------+-------------------------------------------+
|                                |DDD           |1, 2, 3 ... 364, 365                       |
+--------------------------------+--------------+-------------------------------------------+
|**Day of Month**                |DD            |01, 02, 03 ... 30, 31                      |
+--------------------------------+--------------+-------------------------------------------+
|                                |D             |1, 2, 3 ... 30, 31                         |
+--------------------------------+--------------+-------------------------------------------+
|                                |Do            |1st, 2nd, 3rd ... 30th, 31st               |
+--------------------------------+--------------+-------------------------------------------+
|**Day of Week**                 |dddd          |Monday, Tuesday, Wednesday ... [#t2]_      |
+--------------------------------+--------------+-------------------------------------------+
|                                |ddd           |Mon, Tue, Wed ... [#t2]_                   |
+--------------------------------+--------------+-------------------------------------------+
|                                |d             |1, 2, 3 ... 6, 7                           |
+--------------------------------+--------------+-------------------------------------------+
|**ISO week date**               |W             |2011-W05-4, 2019-W17                       |
+--------------------------------+--------------+-------------------------------------------+
|**Hour**                        |HH            |00, 01, 02 ... 23, 24                      |
+--------------------------------+--------------+-------------------------------------------+
|                                |H             |0, 1, 2 ... 23, 24                         |
+--------------------------------+--------------+-------------------------------------------+
|                                |hh            |01, 02, 03 ... 11, 12                      |
+--------------------------------+--------------+-------------------------------------------+
|                                |h             |1, 2, 3 ... 11, 12                         |
+--------------------------------+--------------+-------------------------------------------+
|**AM / PM**                     |A             |AM, PM, am, pm [#t1]_                      |
+--------------------------------+--------------+-------------------------------------------+
|                                |a             |am, pm [#t1]_                              |
+--------------------------------+--------------+-------------------------------------------+
|**Minute**                      |mm            |00, 01, 02 ... 58, 59                      |
+--------------------------------+--------------+-------------------------------------------+
|                                |m             |0, 1, 2 ... 58, 59                         |
+--------------------------------+--------------+-------------------------------------------+
|**Second**                      |ss            |00, 01, 02 ... 58, 59                      |
+--------------------------------+--------------+-------------------------------------------+
|                                |s             |0, 1, 2 ... 58, 59                         |
+--------------------------------+--------------+-------------------------------------------+
|**Sub-second**                  |S...          |0, 02, 003, 000006, 123123123123... [#t3]_ |
+--------------------------------+--------------+-------------------------------------------+
|**Timezone**                    |ZZZ           |Asia/Baku, Europe/Warsaw, GMT ... [#t4]_   |
+--------------------------------+--------------+-------------------------------------------+
|                                |ZZ            |-07:00, -06:00 ... +06:00, +07:00, +08, Z  |
+--------------------------------+--------------+-------------------------------------------+
|                                |Z             |-0700, -0600 ... +0600, +0700, +08, Z      |
+--------------------------------+--------------+-------------------------------------------+
|**Seconds Timestamp**           |X             |1381685817, 1381685817.915482 ... [#t5]_   |
+--------------------------------+--------------+-------------------------------------------+
|**ms or µs Timestamp**          |x             |1569980330813, 1569980330813221            |
+--------------------------------+--------------+-------------------------------------------+

.. rubric:: Footnotes

.. [#t1] localization support for parsing and formatting
.. [#t2] localization support only for formatting
.. [#t3] the result is truncated to microseconds, with `half-to-even rounding <https://en.wikipedia.org/wiki/IEEE_floating_point#Roundings_to_nearest>`_.
.. [#t4] timezone names from `tz database <https://www.iana.org/time-zones>`_ provided via dateutil package, note that abbreviations such as MST, PDT, BRST are unlikely to parse due to ambiguity. Use the full IANA zone name instead (Asia/Shanghai, Europe/London, America/Chicago etc).
.. [#t5] this token cannot be used for parsing timestamps out of natural language strings due to compatibility reasons

Built-in Formats
++++++++++++++++

There are several formatting standards that are provided as built-in tokens.

.. code-block:: python

    >>> arw = arrow.utcnow()
    >>> arw.format(arrow.FORMAT_ATOM)
    '2020-05-27 10:30:35+00:00'
    >>> arw.format(arrow.FORMAT_COOKIE)
    'Wednesday, 27-May-2020 10:30:35 UTC'
    >>> arw.format(arrow.FORMAT_RSS)
    'Wed, 27 May 2020 10:30:35 +0000'
    >>> arw.format(arrow.FORMAT_RFC822)
    'Wed, 27 May 20 10:30:35 +0000'
    >>> arw.format(arrow.FORMAT_RFC850)
    'Wednesday, 27-May-20 10:30:35 UTC'
    >>> arw.format(arrow.FORMAT_RFC1036)
    'Wed, 27 May 20 10:30:35 +0000'
    >>> arw.format(arrow.FORMAT_RFC1123)
    'Wed, 27 May 2020 10:30:35 +0000'
    >>> arw.format(arrow.FORMAT_RFC2822)
    'Wed, 27 May 2020 10:30:35 +0000'
     >>> arw.format(arrow.FORMAT_RFC3339)
    '2020-05-27 10:30:35+00:00'
     >>> arw.format(arrow.FORMAT_W3C)
    '2020-05-27 10:30:35+00:00'

Escaping Formats
~~~~~~~~~~~~~~~~

Tokens, phrases, and regular expressions in a format string can be escaped when parsing and formatting by enclosing them within square brackets.

Tokens & Phrases
++++++++++++++++

Any `token <Supported Tokens_>`_ or phrase can be escaped as follows:

.. code-block:: python

    >>> fmt = "YYYY-MM-DD h [h] m"
    >>> arw = arrow.get("2018-03-09 8 h 40", fmt)
    <Arrow [2018-03-09T08:40:00+00:00]>
    >>> arw.format(fmt)
    '2018-03-09 8 h 40'

    >>> fmt = "YYYY-MM-DD h [hello] m"
    >>> arw = arrow.get("2018-03-09 8 hello 40", fmt)
    <Arrow [2018-03-09T08:40:00+00:00]>
    >>> arw.format(fmt)
    '2018-03-09 8 hello 40'

    >>> fmt = "YYYY-MM-DD h [hello world] m"
    >>> arw = arrow.get("2018-03-09 8 hello world 40", fmt)
    <Arrow [2018-03-09T08:40:00+00:00]>
    >>> arw.format(fmt)
    '2018-03-09 8 hello world 40'

This can be useful for parsing dates in different locales such as French, in which it is common to format time strings as "8 h 40" rather than "8:40".

Regular Expressions
+++++++++++++++++++

You can also escape regular expressions by enclosing them within square brackets. In the following example, we are using the regular expression :code:`\s+` to match any number of whitespace characters that separate the tokens. This is useful if you do not know the number of spaces between tokens ahead of time (e.g. in log files).

.. code-block:: python

    >>> fmt = r"ddd[\s+]MMM[\s+]DD[\s+]HH:mm:ss[\s+]YYYY"
    >>> arrow.get("Mon Sep 08 16:41:45 2014", fmt)
    <Arrow [2014-09-08T16:41:45+00:00]>

    >>> arrow.get("Mon \tSep 08   16:41:45     2014", fmt)
    <Arrow [2014-09-08T16:41:45+00:00]>

    >>> arrow.get("Mon Sep 08   16:41:45   2014", fmt)
    <Arrow [2014-09-08T16:41:45+00:00]>

Punctuation
~~~~~~~~~~~

Date and time formats may be fenced on either side by one punctuation character from the following list: ``, . ; : ? ! " \` ' [ ] { } ( ) < >``

.. code-block:: python

    >>> arrow.get("Cool date: 2019-10-31T09:12:45.123456+04:30.", "YYYY-MM-DDTHH:mm:ss.SZZ")
    <Arrow [2019-10-31T09:12:45.123456+04:30]>

    >>> arrow.get("Tomorrow (2019-10-31) is Halloween!", "YYYY-MM-DD")
    <Arrow [2019-10-31T00:00:00+00:00]>

    >>> arrow.get("Halloween is on 2019.10.31.", "YYYY.MM.DD")
    <Arrow [2019-10-31T00:00:00+00:00]>

    >>> arrow.get("It's Halloween tomorrow (2019-10-31)!", "YYYY-MM-DD")
    # Raises exception because there are multiple punctuation marks following the date

Redundant Whitespace
~~~~~~~~~~~~~~~~~~~~

Redundant whitespace characters (spaces, tabs, and newlines) can be normalized automatically by passing in the ``normalize_whitespace`` flag to ``arrow.get``:

.. code-block:: python

    >>> arrow.get('\t \n  2013-05-05T12:30:45.123456 \t \n', normalize_whitespace=True)
    <Arrow [2013-05-05T12:30:45.123456+00:00]>

    >>> arrow.get('2013-05-05  T \n   12:30:45\t123456', 'YYYY-MM-DD T HH:mm:ss S', normalize_whitespace=True)
    <Arrow [2013-05-05T12:30:45.123456+00:00]>

API Guide
---------

arrow.arrow
~~~~~~~~~~~

.. automodule:: arrow.arrow
    :members:

arrow.factory
~~~~~~~~~~~~~

.. automodule:: arrow.factory
    :members:

arrow.api
~~~~~~~~~

.. automodule:: arrow.api
    :members:

arrow.locale
~~~~~~~~~~~~

.. automodule:: arrow.locales
    :members:
    :undoc-members:

Release History
---------------

.. toctree::
   :maxdepth: 2

   releases
