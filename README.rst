Arrow - Better dates & times for Python
=======================================

.. image:: https://travis-ci.org/crsmithdev/arrow.png
        :target: https://travis-ci.org/crsmithdev/arrow
        
.. image:: https://pypip.in/d/arrow/badge.png
        :target: https://crate.io/packages/arrow
        
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
- Supports Python 2.6, 2.7 and 3.3
- TZ-aware & UTC by default
- Concise, intelligent interface for creation
- Easily replace and shift attributes
- Rich parsing & formatting options
- Timezone conversion
- Simple timestamp handling
- Time spans, ranges, floors and ceilings
- Humanization, with support for a growing number of locales
- Extensible factory architecture supporting custom Arrow-derived types

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

