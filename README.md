[![Build Status](https://travis-ci.org/crsmithdev/arrow.png)](https://travis-ci.org/crsmithdev/arrow)
=========================================
Arrow:  better dates and times for Python
=========================================

------------
Introduction
------------

Arrow is a Python module providing a smooth, sensible way of creating, manipulating, formatting and converting dates and times.  Arrow is simple, lightweight and heavily inspired by `moment.js <https://github.com/timrwood/moment/>`_ and `requests <https://github.com/kennethreitz/requests>`_.

Key features
============

- Implements datetime interface
- TZ-aware & UTC by default
- Concise, intelligent interface for creation
- Attribute manipulation, plural names
- Rich parsing & formatting options
- Timezone conversion
- Simple timestamp handling
- Time spans, floors and ceilings
- Humanization

Quickstart
==========

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

# Arrow - Better date & time manipulation for Python

## Documentation:  crsmithdev.com/arrow

## Overview

Inspired by the elegant API of [requests](https://github.com/kennethreitz/requests) and [moment.js](https://github.com/timrwood/moment/), Arrow provides a smooth, sensible approach to creating, manipulating, and formatting dates and times in Python.

Arrow is a Python module providing a smooth, sensible way of creating, maniuplating, formatting and converting dates and times.  Arrow is simple, lightweight and heavily inspired by [moment.js](https://github.com/timrwood/moment/) and [requests](https://github.com/kennethreitz/requests).

### Key features

* Implements the datetime iterface
* TZ-aware & UTC by default
* Concise, intelligent interface for creation
* Attribute manipulation, plural names
* Rich parsing & formatting options
* Timezone conversion
* Simple timestamp handling
* Time spans, floors and ceilings
* Humanization

## Quickstart
```python
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
```

Changelog
=========

* 0.2.0
  * Reimplemented as datetime replacement
  * Added date parsing
  * Added date formatting
  * Added floor, ceil and span methods
  * Added datetime methods for drop-in replacement
  * Added clone method
  * Added get, now and utcnow API methods

* 0.1.6
  * Added humanized time deltas
  * Fixed numerous issues with conversions related to daylight savings time
  * Fixed some inconsistencies in time zone names
  * __str__ uses ISO formatting
  * __eq__ implemented for basic comparison between Arrow objects

* 0.1.5

  * Started tracking changes
  * Added parsing of ISO-formatted time zone offsets (e.g. '+02:30', '-05:00')
  * Fixed some incorrect timestamps with delta / olson time zones
  * Fixed formatting of UTC offsets in TimeStamp's str method

