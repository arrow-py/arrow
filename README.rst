===================================================
Arrow - Better date & time manipulation for Python
===================================================

:Version: 0.1.6
:Author: Chris Smith (chris@cir.ca)
:Download: http://pypi.python.org/pypi/arrow
:Source: https://github.com/crsmithdev/arrow
:Keywords: python, dates, datetime, timezone, timestamp, utc

.. contents::
    :local:

.. _arrow-overview:

Overview
========

Inspired by the elegant API of Requests_ and JavaScript's moment.js_, Arrow aims to provide a fast, simple way to manipulate dates & times, timezones and timestamps in Python.

Important - UTC
===============

Arrow is UTC by default.  When optional, time zones are assumed to be UTC when none is supplied.

.. _arrow-examples:

Installation
============

You can install arrow from pip::

	$ pip install arrow

Examples
========

Importing
---------

	>>> from arrow import arrow

Instantiation
-------------

Current UTC date & time

	>>> arrow()
	Arrow(2012-11-24T04:12:55.204282+00:00 UTC)

Current local date & time

	>>> arrow('local')
	Arrow(2012-11-23T20:13:21.092619-08:00 PST)

Current date & time in named time zone
	
	>>> arrow('US/Pacific')
	Arrow(2012-11-23T20:13:27.557101-08:00 PST)

Current date & time with offset-based time zone

	>>> arrow(timedelta(hours=-1))
	Arrow(2012-11-24T03:13:38.580132-01:00 None)

Current date & time with ISO-format time zone

	>>> arrow('+01:30')
	Arrow(2012-11-24T05:43:45.076323+01:30 None)

From a timestamp in UTC

	>>> arrow(time.time())
	Arrow(2012-11-24T04:13:48.052395+00:00 UTC)

From a timestamp in another time zone

	>>> arrow(time.time(), 'US/Eastern')
	Arrow(2012-11-23T23:18:34.269432-05:00 EST)

Another date & time in UTC

	>>> arrow(datetime(12, 1, 1))
	Arrow(0012-01-01T00:00:00+00:00 UTC)

Another date & time in another time zone

	>>> arrow(datetime(12, 1, 1), 'US/Central')
	Arrow(0012-01-01T00:00:00-06:00 CST)

Accessing properties
--------------------

	>>> a = arrow()
	>>> a.datetime
	datetime.datetime(2012, 11, 20, 0, 18, 42, 516322, tzinfo=tzutc())
	>>> a.timestamp
	1353370722
	>>> a.tz.name
	'UTC'
	>>> a.tz.utcoffset
	datetime.timedelta(0)
	>>> a.tz.utc
	True

	>>> a = arrow('local')
	>>> a.datetime
	datetime.datetime(2012, 11, 20, 0, 19, 47, 172338, tzinfo=tzfile('/etc/localtime'))
	>>> a.timestamp
	1353399587
	>>> a.tz.name
	'PST'
	>>> a.tz.utcoffset
	datetime.timedelta(-1, 57600)
	>>> a.tz.utc
	False

Converting between time zones
-----------------------------

	>>> a1 = arrow()
	>>> a2 = arrow('local')
	>>> a3 = a1.to('local')
	>>> a4 = a2.to('UTC')
	>>> a1; a4
	Arrow(11/20/12 15:47:27.388437 +00:00 (UTC))
	Arrow(11/20/12 15:47:30.821018 +00:00 (UTC))
	>>> a2; a3
	Arrow(11/20/12 07:47:30.821018 -08:00 (PST))
	Arrow(11/20/12 07:47:27.388437 -08:00 (PST))

	>>> a1 = arrow('local')
	>>> a2 = arrow()
	>>> a3 = a1.utc()
	>>> a2; a3
	Arrow(11/20/12 15:48:32.458546 +00:00 (UTC))
	Arrow(11/20/12 15:48:30.211002 +00:00 (UTC))

.. _arrow-coming-soon:

Humanizing differences in time
------------------------------

Default behavior

	>>> dt_1 = datetime(2012, 1, 1, 3, 3, 3)
	>>> dt_2 = datetime(2012, 1, 2, 4, 4, 4)
	>>> arrow(dt_1).humanize(dt_2)
	'in 1 day'
	>>> arrow(dt_2).humanize(dt_1)
	'1 day ago'

Places & precision

	>>> dt_1 = datetime(2012, 1, 1, 3, 3, 3)
	>>> dt_2 = datetime(2012, 1, 2, 4, 4, 4)
	>>> arrow(dt_1).humanize(dt_2, places=2)
	'in 1 day and 1 hour'
	>>> arrow(dt_1).humanize(dt_2, places=3)
	'in 1 day, 1 hour and 1 minute'
	>>> arrow(dt_2).humanize(dt_1)
	'1 day ago'
	>>> arrow(dt_2).humanize(dt_1, places=2)
	'1 day and 1 hour ago'
	>>> arrow(dt_2).humanize(dt_1, places=3)
	'1 day, 1 hour and 1 minute ago'

Pre- / post-fixing

	>>> dt_1 = datetime(2012, 1, 1, 3, 3, 3)
	>>> dt_2 = datetime(2012, 1, 2, 4, 4, 4)
	>>> arrow(dt_1).humanize(dt_2, fix=False)
	'1 day'
	>>> arrow(dt_2).humanize(dt_1, fix=False)
	'1 day'

Coming soon
===========

* Parsing date strings (e.g. arrow('11-19-2012', format='MM-dd-YYYY'))
* Formatting date strings (e.g. arrow().format('MM-dd-YYYY'))

.. _Requests: http://docs.python-requests.org/
.. _moment.js: http://momentjs.com/

.. _arrow-changelog:

Known issues
============

* Some round trip conversions are inaccurate (see https://github.com/crsmithdev/arrow/issues/4)

Changelog
=========

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
