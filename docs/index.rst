=========================================
Arrow:  better dates and times for Python
=========================================

-----
What?
-----

Arrow is a Python library that offers a sensible, human-friendly approach to creating, manipulating, formatting and converting dates, times, and timestamps.  It implements and updates the datetime type, plugging gaps in functionality, and provides an intelligent module API that supports many common creation scenarios.  Simply put, it helps you work with dates and times with fewer imports and a lot less code.

Arrow is heavily inspired by `moment.js <https://github.com/timrwood/moment>`_ and `requests <https://github.com/kennethreitz/requests>`_.

----
Why?
----
Python's standard library and some other low-level modules have near-complete date, time and time zone functionality but don't work very well from a usability perspective:

- Too many modules:  datetime, time, calendar, dateutil, pytz and more
- Too many types:  date, time, datetime, tzinfo, timedelta, relativedelta, etc.
- Time zones and timestamp conversions are verbose and unpleasant
- Time zone naivety is the norm
- Gaps in functionality:  ISO-8601 parsing, time spans, humanization

--------
Features
--------

- Fully implemented, drop-in replacement for datetime
- Supports Python 2.6, 2.7 and 3.3
- Time zone-aware & UTC by default
- Provides super-simple creation options for many common input scenarios
- Updated .replace method with support for relative offsets, including weeks
- Formats and parses strings, including ISO-8601-formatted strings automatically
- Timezone conversion
- Timestamp available as a property
- Generates time spans, ranges, floors and ceilings in time frames from year to microsecond
- Humanizes and supports a growing list of contributed locales
- Extensible for your own Arrow-derived types

----------
Quickstart
----------

.. code-block:: bash

    $ pip install arrow

.. code-block:: python

    >>> import arrow
    >>> utc = arrow.utcnow()
    >>> utc
    <Arrow [2013-05-11T21:23:58.970460+00:00]>

    >>> utc = utc.replace(hours=-1)
    >>> utc
    <Arrow [2013-05-11T20:23:58.970460+00:00]>

    >>> local = utc.to('US/Pacific')
    >>> local
    <Arrow [2013-05-11T13:23:58.970460-07:00]>

    >>> arrow.get('2013-05-11T21:23:58.970460+00:00')
    <Arrow [2013-05-11T21:23:58.970460+00:00]>

    >>> local.timestamp
    1368303838

    >>> local.format('YYYY-MM-DD HH:mm:ss ZZ')
    '2013-05-11 13:23:58 -07:00'

    >>> local.humanize()
    'an hour ago'

    >>> local.humanize(locale='ko_kr')
    '1시간 전'

------------
User's Guide
------------

Creation
========

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

Use a naive or timezone-aware datetime, or flexibly specify a time zone:

.. code-block:: python

    >>> arrow.get(datetime.utcnow())
    <Arrow [2013-05-07T04:24:24.152325+00:00]>

    >>> arrow.get(datetime.now(), 'US/Pacific')
    <Arrow [2013-05-06T21:24:32.736373-07:00]>

    >>> from dateutil import tz
    >>> arrow.get(datetime.now(), tz.gettz('US/Pacific'))
    <Arrow [2013-05-06T21:24:41.129262-07:00]>

    >>> arrow.get(datetime.now(tz.gettz('US/Pacific')))
    <Arrow [2013-05-06T21:24:49.552236-07:00]>

Parse from a string:

.. code-block:: python

    >>> arrow.get('2013-05-05 12:30:45', 'YYYY-MM-DD HH:mm:ss')
    <Arrow [2013-05-05T12:30:45+00:00]>

Many ISO-8601 compliant strings are recognized and parsed without a format string:

    >>> arrow.get('2013-09-30T15:34:00.000-07:00')
    <Arrow [2013-09-30T15:34:00-07:00]>

Arrow objects can be instantiated directly too, with the same arguments as a datetime:

.. code-block:: python

    >>> arrow.get(2013, 5, 5)
    <Arrow [2013-05-05T00:00:00+00:00]>

    >>> arrow.Arrow(2013, 5, 5)
    <Arrow [2013-05-05T00:00:00+00:00]>

Properties
==========

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

Replace & shift
===============

Get a new :class:`Arrow <arrow.Arrow>` object, with altered attributes, just as you would with a datetime:

.. code-block:: python

    >>> arw = arrow.utcnow()
    >>> arw
    <Arrow [2013-05-12T03:29:35.334214+00:00]>

    >>> arw.replace(hour=4, minute=40)
    <Arrow [2013-05-12T04:40:35.334214+00:00]>

Or, get one with attributes shifted forward or backward:

.. code-block:: python

    >>> arw.replace(weeks=+3)
    <Arrow [2013-06-02T03:29:35.334214+00:00]>


Format
======

.. code-block:: python

    >>> arrow.utcnow().format('YYYY-MM-DD HH:mm:ss ZZ')
    '2013-05-07 05:23:16 -00:00'

Convert
=======

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
========

Humanize relative to now:

.. code-block:: python

    >>> past = arrow.utcnow().replace(hours=-1)
    >>> past.humanize()
    'an hour ago'

Or another Arrow, or datetime:

.. code-block:: python

    >>> present = arrow.utcnow()
    >>> future = present.replace(hours=2)
    >>> future.humanize(present)
    'in 2 hours'

Support for a growing number of locales (see `locales.py` for supported languages):

.. code-block:: python

    >>> future = arrow.utcnow().replace(hours=1)
    >>> future.humanize(a, locale='ru')
    'через 2 час(а,ов)'


Ranges & spans
==============

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
=========

Use factories to harness Arrow's module API for a custom Arrow-derived type.  First, derive your type:

.. code-block:: python

    >>> class CustomArrow(arrow.Arrow):
    ...
    ...     def days_till_xmas(self):
    ...
    ...         xmas = arrow.Arrow(self.year, 12, 25)
    ...
    ...         if self > xmas:
    ...             xmas = xmas.replace(years=1)
    ...
    ...         return (xmas - self).days


Then get and use a factory for it:

.. code-block:: python

    >>> factory = arrow.Factory(CustomArrow)
    >>> custom = factory.utcnow()
    >>> custom
    >>> <CustomArrow [2013-05-27T23:35:35.533160+00:00]>

    >>> custom.days_till_xmas()
    >>> 211

Tokens
======

Use the following tokens in parsing and formatting:

+--------------------------------+--------------+-------------------------------------------+
|                                |Token         |Output                                     |
+================================+==============+===========================================+
|**Year**                        |YYYY          |2000, 2001, 2002 ... 2012, 2013            |
+--------------------------------+--------------+-------------------------------------------+
|                                |YY            |00, 01, 02 ... 12, 13                      |
+--------------------------------+--------------+-------------------------------------------+
|**Month**                       |MMMM          |January, February, March ...               |
+--------------------------------+--------------+-------------------------------------------+
|                                |MMM           |Jan, Feb, Mar ...                          |
+--------------------------------+--------------+-------------------------------------------+
|                                |MM            |01, 02, 03 ... 11, 12                      |
+--------------------------------+--------------+-------------------------------------------+
|                                |M             |1, 2, 3 ... 11, 12                         |
+--------------------------------+--------------+-------------------------------------------+
|**Day of Year**                 |DDDD          |001, 002, 003 ... 364, 365                 |
+--------------------------------+--------------+-------------------------------------------+
|                                |DDD           |1, 2, 3 ... 4, 5                           |
+--------------------------------+--------------+-------------------------------------------+
|**Day of Month**                |DD            |01, 02, 03 ... 30, 31                      |
+--------------------------------+--------------+-------------------------------------------+
|                                |D             |1, 2, 3 ... 30, 31                         |
+--------------------------------+--------------+-------------------------------------------+
|**Day of Week**                 |dddd          |Monday, Tuesday, Wednesday ...             |
+--------------------------------+--------------+-------------------------------------------+
|                                |ddd           |Mon, Tue, Wed ...                          |
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
|**AM / PM**                     |A             |AM, PM                                     |
+--------------------------------+--------------+-------------------------------------------+
|                                |a             |am, pm                                     |
+--------------------------------+--------------+-------------------------------------------+
|**Minute**                      |mm            |00, 01, 02 ... 58, 59                      |
+--------------------------------+--------------+-------------------------------------------+
|                                |m             |0, 1, 2 ... 58, 59                         |
+--------------------------------+--------------+-------------------------------------------+
|**Second**                      |ss            |00, 01, 02 ... 58, 59                      |
+--------------------------------+--------------+-------------------------------------------+
|                                |s             |0, 1, 2 ... 58, 59                         |
+--------------------------------+--------------+-------------------------------------------+
|**Sub-second**                  |SSS           |000, 001, 002 ... 998, 999                 |
+--------------------------------+--------------+-------------------------------------------+
|                                |SS            |00, 01, 02 ... 98, 99                      |
+--------------------------------+--------------+-------------------------------------------+
|                                |S             |0, 1, 2 ... 8, 9                           |
+--------------------------------+--------------+-------------------------------------------+
|**Timezone**                    |ZZ            |-07:00, -06:00 ... +06:00, +07:00          |
+--------------------------------+--------------+-------------------------------------------+
|                                |Z             |-0700, -0600 ... +0600, +0700              |
+--------------------------------+--------------+-------------------------------------------+
|**Timestamp**                   |X             |1381685817                                 |
+--------------------------------+--------------+-------------------------------------------+


---------
API Guide
---------

arrow.arrow
===========

.. automodule:: arrow.arrow
    :members:

arrow.factory
=============

.. automodule:: arrow.factory
    :members:

arrow.api
=========

.. automodule:: arrow.api
    :members:

arrow.locale
============

.. automodule:: arrow.locales
    :members:
