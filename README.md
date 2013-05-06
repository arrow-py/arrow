[![Build Status](https://travis-ci.org/crsmithdev/arrow.png)](https://travis-ci.org/crsmithdev/arrow)
# Arrow - Better date & time manipulation for Python

## Overview

Inspired by the elegant API of [requests](https://github.com/kennethreitz/requests) and [moment.js](https://github.com/timrwood/moment/), Arrow provides a smooth, sensible approach to creating, manipulating, and formatting dates and times in Python.

### Key features

* Drop-in replacement for datetime
* TZ-aware / UTC by default
* Concise syntax for creation from common inputs
* Attribute manipulation, plural names
* Rich parsing / formatting options for dates and timezones
* Timezone conversion
* Time spans, floors and ceilings
* Humanization

### Important - UTC and timezones

Arrow is UTC and timezone aware by default.  When optional, time zones are assumed to be UTC when none is supplied.

## Examples

### Import
```python
>>> import arrow
```

### Current time
```python
>>> arrow.utcnow()
<Arrow [2013-05-05T22:40:24.723023+00:00]>
>>> arrow.now()
<Arrow [2013-05-05T15:40:26.778693-07:00]>
>>> arrow.now('PDT')
<Arrow [2013-05-05T15:40:30.195922-07:00]>
```

### From timestamp

    >>> timestamp = time.time()
    >>> arrow.get(timestamp)
    <Arrow [2013-05-05T22:15:14.864305+00:00]>

    >>> arrow.get(int(timestamp))
    <Arrow [2013-05-05T22:15:14+00:00]>

    >>> arrow.get(str(timestamp))
    <Arrow [2013-05-05T22:15:14.860000+00:00]>

### From datetime / tzinfo

    >>> arrow.get(datetime.utcnow())
    <Arrow [2013-05-05T22:18:40.031238+00:00]>

    >>> arrow.get(datetime.now(gettz('PDT')))
    <Arrow [2013-05-05T15:18:43.063150-07:00]>

    >>> arrow.get(datetime.now(), 'PDT')
    <Arrow [2013-05-05T15:19:33.262255-07:00]>

### From string / format

    >>> arrow.get('2013-05-05 12:30:45', 'YYYY-MM-DD HH:mm:ss')
    <Arrow [2013-05-05T12:30:45+00:00]>

### From year, month, day...

    >>> arrow.get(2013, 5, 5, 12, 30, 45)
    <Arrow [2013-05-05T12:30:45+00:00]>

    >>> arrow.get(2013, 5, 5, 12, 30, 45, tzinfo=tzlocal())
    <Arrow [2013-05-05T12:30:45-07:00]>

### Access properties

    >>> a = arrow.utcnow()
    >>> a
    <Arrow [2013-05-05T22:36:57.832340+00:00]>

    >>> a.datetime
    datetime.datetime(2013, 5, 5, 22, 36, 57, 832340, tzinfo=tzutc())

    >>> a.timestamp
    1367793417

    >>> a.tzinfo
    tzutc()

    >>> a.date()
    datetime.date(2013, 5, 5)

    >>> a.time()
    datetime.time(22, 36, 57, 832340)

    >>> a.dst()
    datetime.timedelta(0)

    >>> a.utcoffset()
    datetime.timedelta(0)

### Update properties

    >>> a = arrow.utcnow()
    >>> a
    <Arrow [2013-05-05T22:27:52.831671+00:00]>

    >>> a.hours += 1
    >>> a
    <Arrow [2013-05-05T23:27:52.831671+00:00]>

    >>> a.hour += 1
    >>> a
    <Arrow [2013-05-06T00:27:52.831671+00:00]>

### Format

    >>> arrow.utcnow().format('YYYY-MM-DD HH:mm:ss Z')
    '2013-05-05 22:31:00 -0000'

### Convert

    >>> arrow.utcnow().to('local')
    <Arrow [2013-05-05T15:33:07.449537-07:00]>

    >>> arrow.utcnow().to('PDT')
    <Arrow [2013-05-05T15:33:14.060642-07:00]>

### Span, floor and ceil

    >>> a = arrow.utcnow()
    >>> a
    <Arrow [2013-05-05T23:08:33.592862+00:00]>

    >>> a.span('hour')
    (<Arrow [2013-05-05T23:00:00+00:00]>, <Arrow [2013-05-05T23:59:59.999999+00:00]>)

    >>> a.floor('hour')
    <Arrow [2013-05-05T23:00:00+00:00]>

    >>> a.ceil('hour')
    <Arrow [2013-05-05T23:59:59.999999+00:00]>

### Clone

    >>> a = arrow.utcnow()
    >>> a
    <Arrow [2013-05-05T23:11:41.173136+00:00]>
    >>> a.clone()
    <Arrow [2013-05-05T23:11:41.173136+00:00]>

### Humanize

    >>> a = arrow.utcnow()
    >>> a.hours -= 1
    >>> a.humanize()
    'an hour ago'

Changelog
=========

* 0.2.0
  * Implemented as datetime replacement
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
