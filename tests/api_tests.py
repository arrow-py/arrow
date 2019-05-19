# -*- coding: utf-8 -*-
from chai import Chai

from arrow import api, arrow, factory


class ModuleTests(Chai):
    def test_get(self):

        self.expect(api._factory.get).args(1, b=2).returns("result")

        self.assertEqual(api.get(1, b=2), "result")

    def test_utcnow(self):

        self.expect(api._factory.utcnow).returns("utcnow")

        self.assertEqual(api.utcnow(), "utcnow")

    def test_now(self):

        self.expect(api._factory.now).args("tz").returns("now")

        self.assertEqual(api.now("tz"), "now")

    def test_factory(self):
        class MockCustomArrowClass(arrow.Arrow):
            pass

        result = api.factory(MockCustomArrowClass)

        self.assertIsInstance(result, factory.ArrowFactory)
        self.assertIsInstance(result.utcnow(), MockCustomArrowClass)
