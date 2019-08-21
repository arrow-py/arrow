Arrow: Better dates & times for Python
======================================

.. start-inclusion-marker-do-not-remove

.. image:: https://travis-ci.org/crsmithdev/arrow.svg?branch=master
   :alt: Build Status
   :target: https://travis-ci.org/crsmithdev/arrow

.. image:: https://codecov.io/github/crsmithdev/arrow/coverage.svg?branch=master
   :alt: Codecov
   :target: https://codecov.io/github/crsmithdev/arrow

.. image:: https://img.shields.io/pypi/v/arrow.svg
   :alt: PyPI Version
   :target: https://pypi.python.org/pypi/arrow

.. image:: https://img.shields.io/pypi/pyversions/arrow.svg
   :alt: Supported Python Versions
   :target: https://pypi.python.org/pypi/arrow

.. image:: https://img.shields.io/pypi/l/arrow.svg
   :alt: License
   :target: https://pypi.python.org/pypi/arrow

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :alt: Code Style: Black
   :target: https://github.com/python/black

What?
-----

Arrow is a Python library that offers a sensible, human-friendly approach to creating, manipulating, formatting and converting dates, times, and timestamps.  It implements and updates the datetime type, plugging gaps in functionality, and provides an intelligent module API that supports many common creation scenarios.  Simply put, it helps you work with dates and times with fewer imports and a lot less code.

Arrow is heavily inspired by `moment.js <https://github.com/moment/moment>`_ and `requests <https://github.com/psf/requests>`_.

Why?
----

Python's standard library and some other low-level modules have near-complete date, time and timezone functionality but don't work very well from a usability perspective:

- Too many modules:  datetime, time, calendar, dateutil, pytz and more
- Too many types:  date, time, datetime, tzinfo, timedelta, relativedelta, etc.
- Timezones and timestamp conversions are verbose and unpleasant
- Timezone naivety is the norm
- Gaps in functionality:  ISO-8601 parsing, timespans, humanization

Features
--------

- Fully implemented, drop-in replacement for datetime
- Supports Python 2.7, 3.5, 3.6, 3.7 and 3.8
- Timezone-aware & UTC by default
- Provides super-simple creation options for many common input scenarios
- :code:`shift` method with support for relative offsets, including weeks
- Formats and parses strings automatically
- Partial support for ISO-8601
- Timezone conversion
- Timestamp available as a property
- Generates time spans, ranges, floors and ceilings in timeframes from year to microsecond
- Humanizes and supports a growing list of contributed locales
- Extensible for your own Arrow-derived types

Quick Start
-----------

Installation
~~~~~~~~~~~~

To install Arrow, use `pip <https://pip.pypa.io/en/stable/quickstart/>`_ or `pipenv <https://docs.pipenv.org/en/latest/>`_:

.. code-block:: console

    $ pip install -U arrow

Example Usage
~~~~~~~~~~~~~

.. code-block:: python

    >>> import arrow
    >>> utc = arrow.utcnow()
    >>> utc
    <Arrow [2013-05-11T21:23:58.970460+00:00]>

    >>> utc = utc.shift(hours=-1)
    >>> utc
    <Arrow [2013-05-11T20:23:58.970460+00:00]>

    >>> local = utc.to('US/Pacific')
    >>> local
    <Arrow [2013-05-11T13:23:58.970460-07:00]>

    >>> arrow.get('2013-05-11T21:23:58.970460+00:00')
    <Arrow [2013-05-11T21:23:58.970460+00:00]>

    >>> local.timestamp
    1368303838

    >>> local.format()
    '2013-05-11 13:23:58 -07:00'

    >>> local.format('YYYY-MM-DD HH:mm:ss ZZ')
    '2013-05-11 13:23:58 -07:00'

    >>> local.humanize()
    'an hour ago'

    >>> local.humanize(locale='ko_kr')
    '1시간 전'

.. end-inclusion-marker-do-not-remove

Documentation
-------------

For full documentation, please visit `arrow.readthedocs.io <https://arrow.readthedocs.io/en/latest/>`_.

Contributing
------------

Contributions are welcome for both code and localizations. To get started, find an issue or feature to tackle on `the issue tracker <https://github.com/crsmithdev/arrow/issues>`_ and then fork `this repository <https://github.com/crsmithdev/arrow>`_ on GitHub to begin making changes. If you would like to help with localizations, please see `locales.py <https://github.com/crsmithdev/arrow/blob/master/arrow/locales.py>`_ to see what locales are currently supported. If you are helping with code, make sure to add a few tests to ensure that the bug was fixed or the feature works as intended.
