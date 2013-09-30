# Arrow - Better dates & times for Python

[![build status](https://travis-ci.org/crsmithdev/arrow.png)](https://travis-ci.org/crsmithdev/arrow)
[![downloads](https://pypip.in/d/arrow/badge.png)](https://crate.io/packages/arrow)
        
## Documentation: [crsmithdev.com/arrow](http://crsmithdev.com/arrow)

## What?

Arrow is a Python library with a sensible, intelligent approach to creating, manipulating, formatting and converting dates, times, and timestamps.  It implements and updates the ``datetime`` type, compatibly enhancing existing methods and adding new ones, and has an intelligent module API that supports many common creation scenarios.  Chances are, you'll find that it provides the functionality you commonly need with fewer imports and a lot less code.  Arrow is simple, lightweight and heavily inspired by [moment.js](https://github.com/timrwood/moment>) and [requests](https://github.com/kennethreitz/requests).

## Why?

Python's standard library and some other low-level modules have near-complete date, time and time zone functionality but don't work very well from a usability perspective:

- Too many modules:  datetime, time, calendar, dateutil, pytz and more
- Too many types:  date, time, datetime, tzinfo, timedelta, relativedelta, etc.
- Time zones and timestamp conversions are verbose and unpleasant 
- Time zone naievety is the norm
- Gaps in functionality:  ISO-8601 parsing, timespans, humanization

## Features

- Fully implemented, drop-in replacement for ``datetime`` 
- Supports Python 2.6, 2.7 and 3.3
- Time zone-aware & UTC by default
- Provides a super-simple creation options for many common input scenarios
- Updated .replace method with support for relative offsets, including weeks
- Formats and parses strings, including ISO-8601-formatted strings automatically
- Timezone conversion
- Timestamp available as a property
- Generates time spans, ranges, floors and ceilings in timeframes from year to microsecond
- Humanizes and supports a growing list of contributed locales
- Extensible for your own Arrow-derived types

## Get started

First:

```shell
$ pip install arrow
```

And then:

```python
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
```

## Documentation: [crsmithdev.com/arrow](http://crsmithdev.com/arrow)

