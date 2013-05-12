Arrow - Better dates & times for Python
=======================================

.. image:: https://travis-ci.org/crsmithdev/arrow.png
        :target: https://travis-ci.org/crsmithdev/arrow

**Documentation:** `crsmithdev.com/arrow <http://crsmithdev.com/arrow>`_.

Arrow is a Python library that provides a sensible, intelligent way of creating, manipulating, formatting and converting dates and times.  Arrow is simple, lightweight and heavily inspired by `moment.js <https://github.com/timrwood/moment>`_ and `requests <https://github.com/kennethreitz/requests>`_.

Why?
----

Python's standard library and some other low-level modules offer complete functionality but don't work very well from a usability perspective:

- Too many modules:  datetime, time, calendar, dateutil, pytz
- Time zones and timestamp conversions are verbose and error-prone
- Time zones are explicit, naivete is the norm
- Gaps in functionality:  ISO-8601 parsing, timespans, humanization


Features
--------

- Implements the datetime interface
- TZ-aware & UTC by default
- Concise, intelligent interface for creation
- Easily replace and shift attributes
- Rich parsing & formatting options
- Timezone conversion
- Simple timestamp handling
- Time spans, ranges, floors and ceilings
- Humanization, with support for a growing number of locales

Get started
-----------

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

        >>> local.timestamp
        1368303838

        >>> local.format('YYYY-MM-DD HH:mm:ss ZZ')
        '2013-05-11 13:23:58 -07:00'

        >>> local.humanize()
        'an hour ago'

        >>> local.humanize(locale='ko_kr')
        '1시간 전'

Documentation
-------------

Documentation is available at `crsmithdev.com/arrow <http://crsmithdev.com/arrow>`_.

History
-------

- 0.3.0

  - Arrow objects are no longer mutable
  - Arrow.replace method
  - Plural attribute name semantics altered: single -> absolute, plural -> relative
  - Plural names no longer supported as properties (e.g. arrow.utcnow().years)
  - Limit parameters are respected in range and span_range
  - Accept timestamps, datetimes and Arrows for datetime inputs, where reasonable

- 0.2.1

  - Support for localized humanization
  - English, Russian, Greek, Korean, Chinese locales

- 0.2.0

  - Reimplemented as datetime replacement
  - Added date parsing
  - Added date formatting
  - Added floor, ceil and span methods
  - Added datetime methods for drop-in replacement
  - Added clone method
  - Added get, now and utcnow API methods

- 0.1.6

  - Added humanized time deltas
  - Fixed numerous issues with conversions related to daylight savings time
  - Fixed some inconsistencies in time zone names
  - __str__ uses ISO formatting
  - __eq__ implemented for basic comparison between Arrow objects

- 0.1.5

  - Started tracking changes
  - Added parsing of ISO-formatted time zone offsets (e.g. '+02:30', '-05:00')
  - Fixed some incorrect timestamps with delta / olson time zones
  - Fixed formatting of UTC offsets in TimeStamp's str method

