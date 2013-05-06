from arrow import Arrow
import parser

from datetime import datetime, tzinfo
from dateutil import tz as dateutil_tz

def get(*args, **kwargs):

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
    return Arrow.utcnow()


def now(tz_expr=None):

    if tz_expr is None:
        tz_expr = dateutil_tz.tzlocal()
    elif not isinstance(tz_expr, tzinfo):
        tz_expr = parser.TzinfoParser.parse(tz_expr)

    return Arrow.now(tz_expr)


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

