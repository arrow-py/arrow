=========================================
Arrow:  better dates and times for Python
=========================================

Arrow is a Python library that provides a sensible, intelligent way of creating, manipulating, formatting and converting dates and times.  Arrow is simple, lightweight and heavily inspired by `moment.js <https://github.com/timrwood/moment>`_ and `requests <https://github.com/kennethreitz/requests>`_.

----
Why?
----

Python's standard library, and some other low-level modules, offer complete functionality but don't work very well from a usability perspective:

- Too many modules:  datetime, time, calendar, dateutil, pytz
- Time zone and timestamp conversions are verbose and error-prone
- Time zones are explicit, naivete is the norm
- Gaps in functionality:  ISO-8601 parsing, timespans, humanization

------------
Key features
------------

- Implements the datetime interface
- TZ-aware & UTC by default
- Concise, intelligent interface for creation
- Easily replace and shift attributes
- Rich parsing & formatting options
- Timezone conversion
- Simple timestamp handling
- Time spans, ranges, floors and ceilings
- Humanization, with support for a growing number of locales

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

    >>> utc = utc.update(hours=-1)
    >>> utc
    <Arrow [2013-05-11T20:23:58.970460+00:00]>

    >>> local = utc.to('US/Pacific')
    >>> local
    <Arrow [2013-05-11T13:23:58.970460-07:00]>

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

Use a datetime, a timezone-aware datetime, a tzinfo or a timezone string:

.. code-block:: python

    >>> arrow.get(datetime.utcnow())
    <Arrow [2013-05-07T04:24:24.152325+00:00]>

    >>> arrow.get(datetime.now(), 'US/Pacific')
    <Arrow [2013-05-06T21:24:32.736373-07:00]>

    >>> arrow.get(datetime.now(), tz.gettz('US/Pacific'))
    <Arrow [2013-05-06T21:24:41.129262-07:00]>

    >>> arrow.get(datetime.now(tz.gettz('US/Pacific')))
    <Arrow [2013-05-06T21:24:49.552236-07:00]>

Or parse from a string:

.. code-block:: python

    >>> arrow.get('2013-05-05 12:30:45', 'YYYY-MM-DD HH:mm:ss')
    <Arrow [2013-05-05T12:30:45+00:00]>

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


Ranges & Spans
==============

Get the timespan of any unit:

.. code-block:: python

    >>> arrow.utcnow().span('hour')
    (<Arrow [2013-05-07T05:00:00+00:00]>, <Arrow [2013-05-07T05:59:59.999999+00:00]>)

Or just get the floor and ceiling:

.. code-block:: python

    >>> arrow.utcnow().floor('hour')
    <Arrow [2013-05-07T05:00:00+00:00]>

    >>> arrow.utcnow().ceil('hour')
    <Arrow [2013-05-07T05:59:59.999999+00:00]>

You can also get a range of timepans:

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


---------
API Guide
---------

.. automodule:: api
    :members:

.. automodule:: arrow
    :members:
