import pytest

import arrow


class TestModule:
    def test_get(self, mocker):
        mocker.patch("arrow.api._factory.get", return_value="result")

        assert arrow.api.get() == "result"

    def test_utcnow(self, mocker):
        mocker.patch("arrow.api._factory.utcnow", return_value="utcnow")

        assert arrow.api.utcnow() == "utcnow"

    def test_now(self, mocker):
        mocker.patch("arrow.api._factory.now", tz="tz", return_value="now")

        assert arrow.api.now("tz") == "now"

    def test_factory(self):
        class MockCustomArrowClass(arrow.Arrow):
            pass

        result = arrow.api.factory(MockCustomArrowClass)

        assert isinstance(result, arrow.factory.ArrowFactory)
        assert isinstance(result.utcnow(), MockCustomArrowClass)

    def test_timezone_utc(self):
        tz = arrow.timezone("UTC")
        assert str(tz) == "UTC"

    def test_timezone_zoneinfo(self):
        tz = arrow.timezone("US/Pacific")
        assert str(tz) == "US/Pacific"

    def test_timezone_local(self):
        tz = arrow.timezone("local")
        assert tz is not None

    def test_timezone_invalid(self):
        with pytest.raises(arrow.parser.ParserError):
            arrow.timezone("not/a/timezone")
