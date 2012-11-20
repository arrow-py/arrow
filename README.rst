===================================================
Arrow - Better date & time manipulation for Python
===================================================

:Version: 0.1.1
:Author: Chris Smith (chris@cir.ca)
:Download: http://pypi.python.org/pypi/arrow
:Source: https://github.com/crsmithdev/arrow
:Keywords: python, dates, datetime, timezone, timestamp, utc

.. contents::
    :local:

.. _arrow-overview:

Overview
========

Inspired by Requests_ and great date / time libraries in other languages (such as moment.js_), Arrow aims to provide a fast, simple way to manipulate dates & times, timezones and timestamps in Python.

Important - UTC
===============

Arrow is UTC by default.  When optional, time zones are assumed to be UTC when none is supplied.

.. _arrow-examples:

Examples
========

Importing
---------

	>>> from arrow import arrow

Instantiation
-------------

Current UTC date & time

	>>> a = arrow()

Current local date & time

	>>> a = arrow('local')

Current date & time in named time zone
	
	>>> a = arrow('US/Pacific') 

Current date & time with offset-based time zone

	>>> a = arrow(timedelta(hours=-1))

Current UTC date & time from timestamp

	>>> a = arrow(time.time())

Another date & time in UTC

	>>> a = arrow(datetime_var)

Another date & time in another time zone

	>>> a = arrow(datetime_var, 'US/Pacific')

Another date & time from timestamp

	>>> a = arrow(time.time(), 'local') 

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
	>>> a1.datetime; a4.datetime
	datetime.datetime(2012, 11, 20, 0, 48, 10, 244547, tzinfo=tzutc())
	datetime.datetime(2012, 11, 20, 0, 48, 13, 948510, tzinfo=tzfile('/usr/share/zoneinfo/UTC'))
	>>> a2.datetime; a3.datetime
	datetime.datetime(2012, 11, 19, 16, 48, 13, 948510, tzinfo=tzfile('/etc/localtime'))
	datetime.datetime(2012, 11, 19, 16, 48, 10, 244547, tzinfo=tzfile('/etc/localtime'))

	>>> a1 = arrow(datetime.now(), tz='local')
	>>> a2 = arrow()
	>>> a3 = a1.utc()
	>>> a2.datetime; a3.datetime
	datetime.datetime(2012, 11, 20, 3, 53, 29, 385932, tzinfo=tzutc())
	datetime.datetime(2012, 11, 20, 3, 53, 25, 985915, tzinfo=tzfile('/usr/share/zoneinfo/UTC'))

.. _arrow-coming-soon:

Coming soon
===========

* Parsing date strings (e.g. arrow('11-19-2012', format='MM-dd-YYYY'))
* Additional time zone formats (e.g. arrow(datetime.now(), tz='+01:00'))
* Humanized relative time (e.g. arrow().since() -> '43 minutes ago')

.. _Requests: http://docs.python-requests.org/
.. _moment.js: http://momentjs.com/