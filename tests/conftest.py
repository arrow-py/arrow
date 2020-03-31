# -*- coding: utf-8 -*-
from datetime import datetime

import pytest

from arrow import arrow, factory, formatter, locales, parser


@pytest.fixture(scope="class")
def utcnow_fixture(request):
    request.cls.arrow = arrow.Arrow.utcnow()


@pytest.fixture(scope="class")
def time2013_01_01_fixture(request):
    request.cls.now = arrow.Arrow.utcnow()
    request.cls.arrow = arrow.Arrow(2013, 1, 1)
    request.cls.datetime = datetime(2013, 1, 1)


@pytest.fixture(scope="class")
def time2013_02_03_fixture(request):
    request.cls.arrow = arrow.Arrow(2013, 2, 3, 12, 30, 45, 1)


@pytest.fixture(scope="class")
def time2013_02_15_fixture(request):
    request.cls.datetime = datetime(2013, 2, 15, 3, 41, 22, 8923)
    request.cls.arrow = arrow.Arrow.fromdatetime(request.cls.datetime)


@pytest.fixture(scope="class")
def formatting_fixture(request):
    request.cls.formatter = formatter.DateTimeFormatter()


@pytest.fixture(scope="class")
def locales_fixture(request):
    request.cls.locales = locales._locales


@pytest.fixture(scope="class")
def lang_locale_fixture(request):
    name = request.cls.__name__[4:]
    if name == "Locale":
        request.cls.locale = locales.get_locale_by_class_name("EnglishLocale")
    else:
        request.cls.locale = locales.get_locale_by_class_name(name)


@pytest.fixture(scope="class")
def factory_fixture(request):
    request.cls.factory = factory.ArrowFactory()


@pytest.fixture(scope="class")
def parser_fixture(request):
    request.cls.parser = parser.DateTimeParser()


@pytest.fixture(scope="class")
def regex_fixture(request):
    request.cls.format_regex = parser.DateTimeParser._FORMAT_RE


@pytest.fixture(scope="class")
def tzinfo_fixture(request):
    request.cls.parser = parser.TzinfoParser()
