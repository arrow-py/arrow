"""
Provides the default implementation of :class:`ArrowFactory <arrow.factory.ArrowFactory>`
methods for use as a module API.

"""

from typing import TYPE_CHECKING

from arrow.arrow import Arrow
from arrow.factory import ArrowFactory

if TYPE_CHECKING:
    from datetime import date, datetime
    from datetime import tzinfo as dt_tzinfo
    from time import struct_time
    from typing import Any, List, Optional, SupportsFloat, Tuple, Type, Union, overload

    from arrow.arrow import TZ_EXPR

# internal default factory.
_factory = ArrowFactory()


@overload
def get(
    *,
    locale: str = "en_us",
    tzinfo: Optional[TZ_EXPR] = None,
    normalize_whitespace: bool = False,
    **kwargs: Any,
) -> Arrow:
    ...


@overload
def get(
    __obj: Union[
        Arrow,
        datetime,
        date,
        struct_time,
        dt_tzinfo,
        int,
        SupportsFloat,
        str,
        Tuple[int, int, int],
        None,
    ],
    *,
    locale: str = "en_us",
    tzinfo: Optional[TZ_EXPR] = None,
    normalize_whitespace: bool = False,
    **kwargs: Any,
) -> Arrow:
    ...


@overload
def get(
    __arg1: Union[datetime, date],
    __arg2: TZ_EXPR,
    *,
    locale: str = "en_us",
    tzinfo: Optional[TZ_EXPR] = None,
    normalize_whitespace: bool = False,
    **kwargs: Any,
) -> Arrow:
    ...


@overload
def get(
    __arg1: str,
    __arg2: Union[str, List[str]],
    *,
    locale: str = "en_us",
    tzinfo: Optional[TZ_EXPR] = None,
    normalize_whitespace: bool = False,
    **kwargs: Any,
) -> Arrow:
    ...


def get(*args: Any, **kwargs: Any) -> Arrow:
    """Calls the default :class:`ArrowFactory <arrow.factory.ArrowFactory>` ``get`` method."""

    return _factory.get(*args, **kwargs)


get.__doc__ = _factory.get.__doc__


def utcnow() -> Arrow:
    """Calls the default :class:`ArrowFactory <arrow.factory.ArrowFactory>` ``utcnow`` method."""

    return _factory.utcnow()


utcnow.__doc__ = _factory.utcnow.__doc__


def now(tz: Optional[TZ_EXPR] = None) -> Arrow:
    """Calls the default :class:`ArrowFactory <arrow.factory.ArrowFactory>` ``now`` method."""

    return _factory.now(tz)


now.__doc__ = _factory.now.__doc__


def factory(type: Type[Arrow]) -> ArrowFactory:
    """Returns an :class:`.ArrowFactory` for the specified :class:`Arrow <arrow.arrow.Arrow>`
    or derived type.

    :param type: the type, :class:`Arrow <arrow.arrow.Arrow>` or derived.

    """

    return ArrowFactory(type)


__all__ = ["get", "utcnow", "now", "factory"]
