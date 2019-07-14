Arrow: Better dates & times for Python
======================================

Release v\ |release|. (`Installation`_)

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

Create from timestamps (ints or floats, or strings that convert to a float):

.. code-block:: python

    >>> arrow.get(1367900664)
    <Arrow [2013-05-07T04:24:24+00:00]>

    >>> arrow.get('1367900664')
    <Arrow [2013-05-07T04:24:24+00:00]>

    >>> arrow.get(1367900664.152325)
    <Arrow [2013-05-07T04:24:24.152325+00:00]>

    >>> arrow.get('1367900664.152325')
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

Some ISO-8601 compliant strings are recognized and parsed without a format string:

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


Format
~~~~~~

.. code-block:: python

    >>> arrow.utcnow().format('YYYY-MM-DD HH:mm:ss ZZ')
    '2013-05-07 05:23:16 -00:00'

Convert
~~~~~~~

Convert to timezones by name or tzinfo:

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

Use the following tokens in parsing and formatting.  Note that they're not the same as the tokens for `strptime(3) <https://www.gnu.org/software/libc/manual/html_node/Low_002dLevel-Time-String-Parsing.html#index-strptime>`_:

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
|**Day of Year**                 |DDDD [#t5]_   |001, 002, 003 ... 364, 365                 |
+--------------------------------+--------------+-------------------------------------------+
|                                |DDD [#t5]_    |1, 2, 3 ... 4, 5                           |
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
|                                |ZZ            |-07:00, -06:00 ... +06:00, +07:00          |
+--------------------------------+--------------+-------------------------------------------+
|                                |Z             |-0700, -0600 ... +0600, +0700              |
+--------------------------------+--------------+-------------------------------------------+
|**Timestamp**                   |X             |1381685817                                 |
+--------------------------------+--------------+-------------------------------------------+

.. rubric:: Footnotes

.. [#t1] localization support for parsing and formatting
.. [#t2] localization support only for formatting
.. [#t3] the result is truncated to microseconds, with `half-to-even rounding <https://en.wikipedia.org/wiki/IEEE_floating_point#Roundings_to_nearest>`_.
.. [#t4] timezone names from `tz database <https://www.iana.org/time-zones>`_ provided via dateutil package
.. [#t5] support for the DDD and DDDD tokens will be added in a future release

Escaping Formats
~~~~~~~~~~~~~~~~

Tokens, phrases, and regular expressions in a format string can be escaped when parsing by enclosing them within square brackets.

Tokens & Phrases
++++++++++++++++

Any `token <Supported Tokens_>`_ or phrase can be escaped as follows:

.. code-block:: python

    >>> fmt = "YYYY-MM-DD h [h] m"
    >>> arrow.get("2018-03-09 8 h 40", fmt)
    <Arrow [2018-03-09T08:40:00+00:00]>

    >>> fmt = "YYYY-MM-DD h [hello] m"
    >>> arrow.get("2018-03-09 8 hello 40", fmt)
    <Arrow [2018-03-09T08:40:00+00:00]>

    >>> fmt = "YYYY-MM-DD h [hello world] m"
    >>> arrow.get("2018-03-09 8 hello world 40", fmt)
    <Arrow [2018-03-09T08:40:00+00:00]>

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
