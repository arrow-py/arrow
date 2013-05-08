.. Arrow documentation master file, created by
   sphinx-quickstart on Mon May  6 15:25:39 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

=========================================
Arrow:  better dates and times for Python
=========================================

Arrow is a module for Python that provides a sensible way of creating, manipulating, formatting and converting dates and times.  It is lightweight, Apache-licensed and heavily inspired by `moment.js <https://github.com/timrwood/moment/>`_ and `requests <https://github.com/kennethreitz/requests>`_.

----
Why?
----

Python's standard library, and some other low-level modules, offer complete functionality but don't work very well from a usability perspective:

- Too many modules:  datetime, time, calendar, dateutil, pytz
- Time zone and timestamp conversions are verbose and error-prone
- Time zones are explicit, naievete is the norm
- Gaps in functionality:  ISO-8601 parsing, timespans, humanization

------------
Key features
------------

- Implements the datetime interface
- TZ-aware & UTC by default
- Concise, intelligent interface for creation
- Attribute manipulation, plural names
- Rich parsing & formatting options
- Timezone conversion
- Simple timestamp handling
- Time spans, floors and ceilings
- Humanization

------------
Installation
------------

.. code-block:: bash

    $ pip install arrow

----------
Quickstart
----------

>>> import arrow
>>> utc = arrow.get()
>>> utc
<Arrow [2013-05-07T03:56:38.560988+00:00]>
>>> utc.hours -=1
>>> utc
<Arrow [2013-05-07T02:56:38.560988+00:00]>
>>> local = utc.to('US/Pacific')
>>> local
<Arrow [2013-05-06T19:56:38.560988-07:00]>
>>> local.timestamp
1367895398
>>> local.format('YYYY-MM-DD HH:mm:ss ZZ')
'2013-05-06 19:56:38 -07:00'

------------
User's Guide
------------

Creation
========

Get 'now' easily:

>>> arrow.utcnow()
<Arrow [2013-05-07T04:20:39.369271+00:00]>
>>> arrow.now()
<Arrow [2013-05-06T21:20:40.841085-07:00]>
>>> arrow.now('US/Pacific')
<Arrow [2013-05-06T21:20:44.761511-07:00]>

Create from timestamps (ints or floats, or strings that parse as either):

>>> arrow.get(time.time())
<Arrow [2013-05-07T04:24:04.616438+00:00]>
>>> arrow.get(str(time.time()))
<Arrow [2013-05-07T04:24:12.690000+00:00]>

Use a datetime, a timezone-aware datetime, a tzinfo or a timezone string:

>>> arrow.get(datetime.utcnow())
<Arrow [2013-05-07T04:24:24.152325+00:00]>
>>> arrow.get(datetime.now(), 'US/Pacific')
<Arrow [2013-05-06T21:24:32.736373-07:00]>
>>> arrow.get(datetime.now(), tz.gettz('US/Pacific'))
<Arrow [2013-05-06T21:24:41.129262-07:00]>
>>> arrow.get(datetime.now(tz.gettz('US/Pacific')))
<Arrow [2013-05-06T21:24:49.552236-07:00]>

Or parse from a string:

>>> arrow.get('2013-05-05 12:30:45', 'YYYY-MM-DD HH:mm:ss')
<Arrow [2013-05-05T12:30:45+00:00]>

Arrow objects can be instantiated directly too, with the same arguments as a datetime:

>>> arrow.get(2013, 5, 5)
<Arrow [2013-05-05T00:00:00+00:00]>
>>> arrow.Arrow(2013, 5, 5)
<Arrow [2013-05-05T00:00:00+00:00]>


Properties
==========

Get a datetime or timestamp representation:

>>> a = arrow.utcnow()
>>> a.datetime
datetime.datetime(2013, 5, 7, 4, 38, 15, 447644, tzinfo=tzutc())
>>> a.timestamp
1367901495

Get a naive datetime, and tzinfo:

>>> a.naive
datetime.datetime(2013, 5, 7, 4, 38, 15, 447644)
>>> a.tzinfo
tzutc()

Get values by single or plural name:

>>> a.year
2013
>>> a.years
2013

Set values by the same single or plural names:

>>> a.hours += 1
>>> a.hours
5
>>> a.hour += 1
>>> a.hour
6

Get datetime properties:

>>> a.date()
datetime.date(2013, 5, 7)
>>> a.time()
datetime.time(4, 38, 15, 447644)

Format
======

>>> arrow.utcnow().format('YYYY-MM-DD HH:mm:ss ZZ')
'2013-05-07 05:23:16 -00:00'

Convert
=======

Convert to timezones by name or tzinfo:

>>> utc = arrow.utcnow()
>>> utc
<Arrow [2013-05-07T05:24:11.823627+00:00]>
>>> utc.to('US/Pacific')
<Arrow [2013-05-06T22:24:11.823627-07:00]>
>>> utc.to(tz.gettz('US/Pacific'))
<Arrow [2013-05-06T22:24:11.823627-07:00]>

Or using shorthand:

>>> utc.to('local')
<Arrow [2013-05-06T22:24:11.823627-07:00]>
>>> utc.to('local').to('utc')
<Arrow [2013-05-07T05:24:11.823627+00:00]>


Humanize
========

Humanize relative to now:

>>> a = arrow.utcnow()
>>> a.hours -= 1
>>> a.humanize()
'an hour ago'

Or another Arrow, or datetime:

>>> b = arrow.utcnow()
>>> b.hours += 1
>>> b.humanize(a)
'in 2 hours'

Timespans
=========

Get the timespan of any unit:

>>> arrow.utcnow().span('hour')
(<Arrow [2013-05-07T05:00:00+00:00]>, <Arrow [2013-05-07T05:59:59.999999+00:00]>)

Or just get the floor and ceiling:

>>> arrow.utcnow().floor('hour')
<Arrow [2013-05-07T05:00:00+00:00]>
>>> arrow.utcnow().ceil('hour')
<Arrow [2013-05-07T05:59:59.999999+00:00]>

.. toctree::
   :maxdepth: 2

