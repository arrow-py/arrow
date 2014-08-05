# -*- coding: utf-8 -*-
'''
Standard timestamp formats.
'''

from __future__ import absolute_import

class Format(object):
    def __init__(self, name=None):
        self.name = name

iso8601 = Format(name="ISO 8601")
"""
ISO-8601 timestamp format

Arrow provides a parser for ISO-8601 timestamps.
"""

rfc2822 = Format(name="RFC 2822")
"""
RFC2822 e-mail timestamp format

Arrow provides a parser and a formatter for RFC 2822 timestamps.

>>> arrow.get('Mon, 30 Sep 2013 15:34:00 -0700', arrow.formats.rfc2822)
<Arrow [2013-09-30T15:34:00-07:00]>
"""
