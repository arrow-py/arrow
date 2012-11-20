==============================================
Arrow - Simple dates and timezones for Python
==============================================

:Version: 0.1.1
:Author: Chris Smith (chris@cir.ca)
:Download: http://pypi.python.org/pypi/arrow
:Source: https://github.com/crsmithdev/arrow
:Keywords: python, dates, datetime, timezone, timestamp, utc

.. _arrow-overview:

Overview
========

Inspired by Requests (http://docs.python-requests.org/en/latest/) and great date / time libraries in other languages (moment.js, etc.), Arrow aims to provide a fast, simple way to manipulate dates & times, timezones and timestamps in Python.

Arrow is UTC by default.  When not supplied, the time zone is assumed to be UTC, and when not supplied, the internal date of an Arrow object is set to datetime.utcnow().

.. _arrow-examples:

Examples
========

Importing:
----------

	>>> from arrow import arrow

Instantiation:
--------------

Current UTC date & time

	>>> a = arrow()

Current local date & time

	>>> a = arrow(datetime.now(), tz='local')

Current date & time in named time zone
	
	>>> a = arrow(datetime.now(), tz='US/PST') 

Current date & time with offset-based time zone

	>>> a = arrow(datetime.now(), tz=timedelta(hours=-1))

Current UTC date & time from timestamp

	>>> a = arrow(time.time())

Current local date & time from timestamp

	>>> a = arrow(time.time(), tz='local')

Accessing properties:
---------------------

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

	>>> a = arrow(tz='local')
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

Converting between time zones:
------------------------------

	>>> a1 = arrow()
	>>> a2 = arrow(datetime.now(), tz='local')
	>>> a3 = a1.as('local')
	>>> a4 = a2.as('UTC')
	>>> a1.datetime; a4.datetime
	datetime.datetime(2012, 11, 20, 0, 48, 10, 244547, tzinfo=tzutc())
	datetime.datetime(2012, 11, 20, 0, 48, 13, 948510, tzinfo=tzfile('/usr/share/zoneinfo/UTC'))
	>>> a2.datetime; a3.datetime
	datetime.datetime(2012, 11, 19, 16, 48, 13, 948510, tzinfo=tzfile('/etc/localtime'))
	datetime.datetime(2012, 11, 19, 16, 48, 10, 244547, tzinfo=tzfile('/etc/localtime'))

Running tests
=============::

	virtualenv local
	. local/bin/activate
	pip install python-dateutil nose nose-dov
	./scripts/tests

.. _arrow-coming-soon:

Coming soon
===========

* Parsing date strings (e.g. arrow('11-19-2012', format='MM-dd-YYYY'))
* Additional time zone formats (e.g. arrow(datetime.now(), tz='+01:00'))
* Humanized relative time (e.g. arrow().since() -> '43 minutes ago')

