# -*- coding: utf-8 -*-
from __future__ import absolute_import

from arrow.arrow import Arrow
from arrow import parser

from datetime import datetime, tzinfo
from dateutil import tz as dateutil_tz


class ArrowFactory(object):

    def __init__(self, type=Arrow):
        self.type = type

    def get(self, *args, **kwargs):

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

            timestamp = None

            try:
                timestamp = float(arg)
            except:
                pass

            # (int), (float), (str(int)) or (str(float)) -> from timestamp.
            if timestamp is not None:
                return self.type.utcfromtimestamp(timestamp)

            # (datetime) -> from datetime.
            elif isinstance(arg, datetime):
                return self.type.fromdatetime(arg)

            # (tzinfo) -> now, @ tzinfo.
            elif isinstance(arg, tzinfo):
                return self.type.now(arg)

            # (str) -> now, @ tzinfo.
            elif isinstance(arg, str):
                _tzinfo = parser.TzinfoParser.parse(arg)
                return self.type.now(_tzinfo)

            else:
                raise TypeError('Can\'t parse single argument type of \'{0}\''.format(type(arg)))

        elif arg_count == 2:

            arg_1, arg_2 = args[0], args[1]

            if isinstance(arg_1, datetime):

                # (datetime, tzinfo) -> fromdatetime @ tzinfo.
                if isinstance(arg_2, tzinfo):
                    return self.type.fromdatetime(arg_1, arg_2)

                # (datetime, str) -> fromdatetime @ tzinfo.
                elif isinstance(arg_2, str):
                    _tzinfo = parser.TzinfoParser.parse(arg_2)
                    return self.type.fromdatetime(arg_1, _tzinfo)

                else:
                    raise TypeError('Can\'t parse two arguments of types \'datetime\', \'{0}\''.format(
                        type(arg_2)))

            # (str, format) -> parsed.
            elif isinstance(arg_1, str) and isinstance(arg_2, str):
                dt = parser.DateTimeParser(locale).parse(args[0], args[1])
                return self.type.fromdatetime(dt)

            else:
                raise TypeError('Can\'t parse two arguments of types \'{0}\', \'{1}\''.format(
                    type(arg_1), type(arg_2)))

        # 3+ args.
        else:
            return self.type(*args, **kwargs)

    def utcnow(self):

        return self.type.utcnow()

    def now(self, tz=None):

        if tz is None:
            tz = dateutil_tz.tzlocal()
        elif not isinstance(tz, tzinfo):
            tz = parser.TzinfoParser.parse(tz)

        return self.type.now(tz)

    def arrow(self, date=None, tz=None):

        if date is None:
            return self.utcnow() if tz is None else self.now(tz)

        else:

            if tz is None:
                try:
                    tz = parser.TzinfoParser.parse(date)
                    return self.now(tz)
                except:
                    pass

                if isinstance(date, (float, int)):
                    return Arrow.utcfromtimestamp(date)

                return Arrow.fromdatetime(date)

            else:

                tz = parser.TzinfoParser.parse(tz)
                return Arrow.fromdatetime(date, tz)

