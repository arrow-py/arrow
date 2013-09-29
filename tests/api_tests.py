from chai import Chai
from datetime import datetime
from dateutil import tz
import time

from arrow import api, factory, arrow, util


class ModuleTests(Chai):

    def test_get(self):

        expect(api._factory.get).args(1, b=2).returns('result')

        assertEqual(api.get(1, b=2), 'result')

    def test_utcnow(self):

        expect(api._factory.utcnow).returns('utcnow')

        assertEqual(api.utcnow(), 'utcnow')

    def test_now(self):

        expect(api._factory.now).args('tz').returns('now')

        assertEqual(api.now('tz'), 'now')

    def test_factory(self):

        class MockCustomArrowClass(arrow.Arrow):
            pass

        result = api.factory(MockCustomArrowClass)

        assertIsInstance(result, factory.ArrowFactory)
        assertIsInstance(result.utcnow(), MockCustomArrowClass)

