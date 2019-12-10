# -*- coding: utf-8 -*-

from typing import TYPE_CHECKING

from ._version import __version__
from .api import get, now, utcnow
from .arrow import Arrow
from .factory import ArrowFactory
from .parser import ParserError

if TYPE_CHECKING:
    import sys
    from datetime import tzinfo

    from typing import Union

    if sys.version_info < (3, 0):
        _basestring = basestring
    else:
        _basestring = str

    _tzinfo_exp = Union[_basestring, tzinfo]
