# -*- coding: utf-8 -*-

from arrow import Arrow
import parser

from datetime import datetime, tzinfo
from dateutil import tz as dateutil_tz


def get(*args, **kwargs):
    '''Returns an :class:`Arrow <arrow.Arrow>` object based on flexible inputs.

    Usage::

        >>> import arrow

    **No** inputs to get **current UTC time**::

        >>> arrow.get()
        <Arrow [2013-05-08T05:51:43.316458+00:00]>

    **One str**, **float**, or **int**, convertible to a floating-point timestamp, to get that timestamp in UTC::

        >>> arrow.get(1367992474.293378)
        <Arrow [2013-05-08T05:54:34.293378+00:00]>
        >>>
        >>> arrow.get(1367992474)
        <Arrow [2013-05-08T05:54:34+00:00]>
        >>>
        >>> arrow.get('1367992474.293378')
        <Arrow [2013-05-08T05:54:34.293378+00:00]>
        >>>
        >>> arrow.get('1367992474')
        <Arrow [2013-05-08T05:54:34+00:00]>

    **One str**, convertible to a timezone, or **tzinfo**, to get the current time in that timezone::

        >>> arrow.get('local')
        <Arrow [2013-05-07T22:57:11.793643-07:00]>
        >>>
        >>> arrow.get('US/Pacific')
        <Arrow [2013-05-07T22:57:15.609802-07:00]>
        >>>
        >>> arrow.get('-07:00')
        <Arrow [2013-05-07T22:57:22.777398-07:00]>
        >>>
        >>> arrow.get(tz.tzlocal())
        <Arrow [2013-05-07T22:57:28.484717-07:00]>

    **One** naive **datetime**, to get that datetime in UTC::

        >>> arrow.get(datetime(2013, 5, 5))
        <Arrow [2013-05-05T00:00:00+00:00]>

    **One** aware **datetime**, to get that datetime::

        >>> arrow.get(datetime(2013, 5, 5, tzinfo=tz.tzlocal()))
        <Arrow [2013-05-05T00:00:00-07:00]>

    **Two** arguments, a naive or aware **datetime**, and a timezone expression (as above)::

        >>> arrow.get(datetime(2013, 5, 5), 'US/Pacific')
        <Arrow [2013-05-05T00:00:00-07:00]>

    **Two** arguments, both **str**, to parse the first according to the format of the second::

        >>> arrow.get('2013-05-05 12:30:45', 'YYYY-MM-DD HH:mm:ss')
        <Arrow [2013-05-05T12:30:45+00:00]>

    **Three or more** arguments, as for the constructor of a **datetime**::

        >>> arrow.get(2013, 5, 5, 12, 30, 45)
        <Arrow [2013-05-05T12:30:45+00:00]>
    '''

    arg_count = len(args)

    if arg_count == 0:
        return Arrow.utcnow()

    if arg_count == 1:
        arg = args[0]
        timestamp = None

        try:
            timestamp = float(arg)
        except:
            pass

        # (int), (float), (str(int)) or (str(float)) -> from timestamp.
        if timestamp is not None:
            return Arrow.utcfromtimestamp(timestamp)

        # (datetime) -> from datetime.
        elif isinstance(arg, datetime):
            return Arrow.fromdatetime(arg)

        # (tzinfo) -> now, @ tzinfo.
        elif isinstance(arg, tzinfo):
            return Arrow.now(arg)

        # (str) -> now, @ tzinfo.
        elif isinstance(arg, str):
            _tzinfo = parser.TzinfoParser.parse(arg)
            return Arrow.now(_tzinfo)

        else:
            raise TypeError('Can\'t parse single argument type of \'{0}\''.format(type(arg)))

    elif arg_count == 2:

        arg_1, arg_2 = args[0], args[1]

        if isinstance(arg_1, datetime):

            # (datetime, tzinfo) -> fromdatetime @ tzinfo.
            if isinstance(arg_2, tzinfo):
                return Arrow.fromdatetime(arg_1, arg_2)

            # (datetime, str) -> fromdatetime @ tzinfo.
            elif isinstance(arg_2, str):
                _tzinfo = parser.TzinfoParser.parse(arg_2)
                return Arrow.fromdatetime(arg_1, _tzinfo)

            else:
                raise TypeError('Can\'t parse two arguments of types \'datetime\', \'{0}\''.format(
                    type(arg_2)))

        # (str, format) -> parsed.
        elif isinstance(arg_1, str) and isinstance(arg_2, str):
            dt = parser.DateTimeParser.parse(args[0], args[1])
            return Arrow.fromdatetime(dt)

        else:
            raise TypeError('Can\'t parse two arguments of types \'{0}\', \'{1}\''.format(
                type(arg_1), type(arg_2)))

    # 3+ args.
    else:
        return Arrow(*args, **kwargs)


def utcnow():
    '''Returns an :class:`Arrow <arrow.Arrow>` object, representing "now" in UTC time.

    Usage::

        >>> import arrow
        >>> arrow.utcnow()
        <Arrow [2013-05-08T05:19:07.018993+00:00]>
    '''

    return Arrow.utcnow()


def now(tz=None):
    '''Returns an :class:`Arrow <arrow.Arrow>` object, representing "now".

    :param tz: (optional) An expression representing a timezone.  Defaults to local time.

    Recognized timezone expressions:

        - A **tzinfo** object
        - A **str** describing a timezone, similar to "US/Pacific", or "Europe/Berlin"
        - A **str** in ISO-8601 style, as in "+07:00"
        - A **str**, one of the following:  *local*, *utc*, *UTC*

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

    return Arrow.now(tz)


def arrow(date=None, tz=None):

    if date is None:
        return utcnow() if tz is None else now(tz)

    else:

        if tz is None:
            try:
                tz = parser.TzinfoParser.parse(date)
                return now(tz)
            except:
                return Arrow.fromdatetime(date)

        else:
            tz = parser.TzinfoParser.parse(tz)
            return Arrow.fromdatetime(date, tz)

