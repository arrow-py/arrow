# -*- coding: utf-8 -*-
'''
Implements the :class:`ArrowFactory <arrow.factory.ArrowFactory>` class,
providing factory methods for common :class:`Arrow <arrow.arrow.Arrow>`
contruction scenarios.

'''

from __future__ import absolute_import

from arrow.arrow import Arrow
from arrow import parser
from arrow.util import isstr

from datetime import datetime, tzinfo
from dateutil import tz as dateutil_tz
from time import struct_time
import calendar
parsedatetime = None
try:
    import parsedatetime
except ImportError, e:# pragma: no cover
    pass


class ArrowFactory(object):
    ''' A factory for generating :class:`Arrow <arrow.arrow.Arrow>` objects.

    :param type: (optional) the :class:`Arrow <arrow.arrow.Arrow>`-based class to construct from.
        Defaults to :class:`Arrow <arrow.arrow.Arrow>`.

    '''

    def __init__(self, type=Arrow):
        self.type = type

    def get(self, *args, **kwargs):
        ''' Returns an :class:`Arrow <arrow.arrow.Arrow>` object based on flexible inputs.

        Usage::

            >>> import arrow

        **No inputs** to get current UTC time::

            >>> arrow.get()
            <Arrow [2013-05-08T05:51:43.316458+00:00]>

        **None** to also get current UTC time::

            >>> arrow.get(None)
            <Arrow [2013-05-08T05:51:43.316458+00:00]>

        **One** :class:`Arrow <arrow.arrow.Arrow>` object, to get a copy.

            >>> arw = arrow.utcnow()
            >>> arrow.get(arw)
            <Arrow [2013-10-23T15:21:54.354846+00:00]>

        **One** ``str``, ``float``, or ``int``, convertible to a floating-point timestamp, to get that timestamp in UTC::

            >>> arrow.get(1367992474.293378)
            <Arrow [2013-05-08T05:54:34.293378+00:00]>

            >>> arrow.get(1367992474)
            <Arrow [2013-05-08T05:54:34+00:00]>

            >>> arrow.get('1367992474.293378')
            <Arrow [2013-05-08T05:54:34.293378+00:00]>

            >>> arrow.get('1367992474')
            <Arrow [2013-05-08T05:54:34+00:00]>

        **One** ISO-8601-formatted ``str``, to parse it::

            >>> arrow.get('2013-09-29T01:26:43.830580')
            <Arrow [2013-09-29T01:26:43.830580+00:00]>

        **One** ``tzinfo``, to get the current time in that timezone::

            >>> arrow.get(tz.tzlocal())
            <Arrow [2013-05-07T22:57:28.484717-07:00]>

        **One** naive ``datetime``, to get that datetime in UTC::

            >>> arrow.get(datetime(2013, 5, 5))
            <Arrow [2013-05-05T00:00:00+00:00]>

        **One** aware ``datetime``, to get that datetime::

            >>> arrow.get(datetime(2013, 5, 5, tzinfo=tz.tzlocal()))
            <Arrow [2013-05-05T00:00:00-07:00]>

        **Two** arguments, a naive or aware ``datetime``, and a timezone expression (as above)::

            >>> arrow.get(datetime(2013, 5, 5), 'US/Pacific')
            <Arrow [2013-05-05T00:00:00-07:00]>

        **Two** arguments, both ``str``, to parse the first according to the format of the second::

            >>> arrow.get('2013-05-05 12:30:45', 'YYYY-MM-DD HH:mm:ss')
            <Arrow [2013-05-05T12:30:45+00:00]>

        **Two** arguments, first a ``str`` to parse and second a ``list`` of formats to try::

            >>> arrow.get('2013-05-05 12:30:45', ['MM/DD/YYYY', 'YYYY-MM-DD HH:mm:ss'])
            <Arrow [2013-05-05T12:30:45+00:00]>

        **Three or more** arguments, as for the constructor of a ``datetime``::

            >>> arrow.get(2013, 5, 5, 12, 30, 45)
            <Arrow [2013-05-05T12:30:45+00:00]>

        **One** time.struct time::
            >>> arrow.get(gmtime(0))
            <Arrow [1970-01-01T00:00:00+00:00]>

        '''

        arg_count = len(args)
        locale = kwargs.get('locale', 'en_us')

        # () -> now, @ utc.
        if arg_count == 0:
            return self.type.utcnow()

        if arg_count == 1:
            arg = args[0]

            # (None) -> now, @ utc.
            if arg is None:
                return self.type.utcnow()

            # try (int, float, str(int), str(float)) -> utc, from timestamp.
            try:
                return self.type.utcfromtimestamp(arg)
            except:
                pass

            # (Arrow) -> from the object's datetime.
            if isinstance(arg, Arrow):
                return self.type.fromdatetime(arg.datetime)

            # (datetime) -> from datetime.
            if isinstance(arg, datetime):
                return self.type.fromdatetime(arg)

            # (tzinfo) -> now, @ tzinfo.
            elif isinstance(arg, tzinfo):
                return self.type.now(arg)

            # (str) -> now, @ tzinfo.
            if isstr(arg):
                try:
                    # Try to parse as ISO
                    dt = parser.DateTimeParser(locale).parse_iso(arg)
                    return self.type.fromdatetime(dt)
                except parser.ParserError: 
                    pass

            # (str) -> from humanized string
            if isstr(arg) and parsedatetime:
                cal = parsedatetime.Calendar()
                time_struct, _ = cal.parse(arg, sourceTime=datetime.utcnow())
                return self.type.utcfromtimestamp(calendar.timegm(time_struct))

            # (struct_time) -> from struct_time
            elif isinstance(arg, struct_time):
                return self.type.utcfromtimestamp(calendar.timegm(arg))

            else:
                raise TypeError('Can\'t parse single argument type of \'{0}\''.format(type(arg)))

        elif arg_count == 2:

            arg_1, arg_2 = args[0], args[1]

            if isinstance(arg_1, datetime):

                # (datetime, tzinfo) -> fromdatetime @ tzinfo/string.
                if isinstance(arg_2, tzinfo) or isstr(arg_2):
                    return self.type.fromdatetime(arg_1, arg_2)
                else:
                    raise TypeError('Can\'t parse two arguments of types \'datetime\', \'{0}\''.format(
                        type(arg_2)))

            # (str, format) -> parse.
            elif isstr(arg_1) and (isstr(arg_2) or isinstance(arg_2, list)):
                dt = parser.DateTimeParser(locale).parse(args[0], args[1])
                return self.type.fromdatetime(dt)

            else:
                raise TypeError('Can\'t parse two arguments of types \'{0}\', \'{1}\''.format(
                    type(arg_1), type(arg_2)))

        # 3+ args -> datetime-like via constructor.
        else:
            return self.type(*args, **kwargs)

    def utcnow(self):
        '''Returns an :class:`Arrow <arrow.arrow.Arrow>` object, representing "now" in UTC time.

        Usage::

            >>> import arrow
            >>> arrow.utcnow()
            <Arrow [2013-05-08T05:19:07.018993+00:00]>
        '''

        return self.type.utcnow()

    def now(self, tz=None):
        '''Returns an :class:`Arrow <arrow.arrow.Arrow>` object, representing "now".

        :param tz: (optional) An expression representing a timezone.  Defaults to local time.

        Recognized timezone expressions:

            - A ``tzinfo`` object.
            - A ``str`` describing a timezone, similar to 'US/Pacific', or 'Europe/Berlin'.
            - A ``str`` in ISO-8601 style, as in '+07:00'.
            - A ``str``, one of the following:  'local', 'utc', 'UTC'.

        Usage::

            >>> import arrow
            >>> arrow.now()
            <Arrow [2013-05-07T22:19:11.363410-07:00]>

            >>> arrow.now('US/Pacific')
            <Arrow [2013-05-07T22:19:15.251821-07:00]>

            >>> arrow.now('+02:00')
            <Arrow [2013-05-08T07:19:25.618646+02:00]>

            >>> arrow.now('local')
            <Arrow [2013-05-07T22:19:39.130059-07:00]>
        '''

        if tz is None:
            tz = dateutil_tz.tzlocal()
        elif not isinstance(tz, tzinfo):
            tz = parser.TzinfoParser.parse(tz)

        return self.type.now(tz)
