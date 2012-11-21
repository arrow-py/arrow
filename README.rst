===================================================
Arrow - Better date & time manipulation for Python
===================================================

:Version: 0.1.4
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

Examples
========

Importing
---------

	>>> from arrow import arrow

Instantiation
-------------

Current UTC date & time

	>>> arrow()
	Arrow(11/20/12 15:40:22.696837 +00:00 (UTC))

Current local date & time

	>>> arrow('local')
	Arrow(11/20/12 07:40:27.473312 -08:00 (PST))

Current date & time in named time zone
	
	>>> arrow('US/Pacific')
	Arrow(11/20/12 07:40:36.707704 -08:00 (PST))

Current date & time with offset-based time zone

	>>> arrow(timedelta(hours=-1))
	Arrow(11/20/12 14:40:54.544660 -01:00 (None))

Current UTC date & time from timestamp

	>>> arrow(time.time())
	Arrow(11/20/12 15:41:13.112031 +00:00 (UTC))

Another date & time in UTC

	>>> d = datetime.utcnow() + timedelta(hours=-1)
	>>> arrow(d)
	Arrow(11/20/12 15:41:22.130000 +00:00 (UTC))

Another date & time in another time zone

	>>> d = datetime.now() + timedelta(hours=-1)
	>>> arrow(d, 'local')
	Arrow(11/20/12 07:18:55.535649 -08:00 (PST))

Another date & time from timestamp

	>>> arrow(time.time())
	Arrow(11/20/12 15:46:49.204422 +00:00 (UTC))

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

Coming soon
===========

* Parsing date strings (e.g. arrow('11-19-2012', format='MM-dd-YYYY'))
* Additional time zone formats (e.g. arrow(datetime.now(), tz='+01:00'))
* Humanized relative time (e.g. arrow().since() -> '43 minutes ago')

.. _Requests: http://docs.python-requests.org/
.. _moment.js: http://momentjs.com/