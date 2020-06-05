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
