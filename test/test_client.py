import responses
import os
from finage.client import Finage
import logging
import pytest


root = "https://api.finage.co.uk"
symbols = "AAPL,TSLA,GOGL"
good_resp = [
    (f"{root}/last/stock/ALK?apikey=FAKE_KEY&ts=ms", {}),
    (f"{root}/last/stock/ALK?apikey=FAKE_KEY", {}),
    (f"{root}/last/stocks?apikey=FAKE_KEY&ts=ms&symbols={symbols}", {}),
    (f"{root}/last/trade/stock/ALK", {}),
    (
        f"{root}/last/trade/stocks?apikey=FAKE_KEY&ts=ms&symbols={symbols}",
        {},
    ),
    (f"{root}/history/stock/open-close", {}),
    (f"{root}/history/stock/all", {}),
    (f"{root}/agg/stock/ALK/1/day/2021-06-01/2021-09-01", {}),
    (f"{root}/agg/stock/prev-close/ALK?apikey=FAKE_KEY&unadjusted=True", {}),
    (f"{root}/agg/stock/prev-close/ALK?apikey=FAKE_KEY", {}),
]


LOGGER = logging.getLogger(__name__)


class TestClient(object):

    fake = "FAKE_KEY"

    def setup(self):
        self.client = Finage(self.fake)
        for resp in good_resp:
            responses.add(responses.GET, resp[0], json=resp[1], status=200)
        responses.add(
            responses.GET,
            f"{root}/history/stock/all?apikey=FAKE_KEY",
            json={}, status=400
        )

    def test_init(self):
        if "FINAGE_KEY" in os.environ.keys():
            del os.environ["FINAGE_KEY"]
        with pytest.raises(ValueError, match="Needs an API key"):
            Finage()
        os.environ["FINAGE_KEY"] = self.fake
        finage = Finage()
        assert finage.api_key == self.fake
        finage = Finage(self.fake)
        assert finage.api_key == self.fake

    def test_make_query_string(self):
        qs = self.client._make_query_string("/hello", {"foo": "bar"})
        assert qs == "https://api.finage.co.uk/hello?apikey=FAKE_KEY&foo=bar"
        qs = self.client._make_query_string("/hello", {})
        assert qs == "https://api.finage.co.uk/hello?apikey=FAKE_KEY"
        qs = self.client._make_query_string("/hello")

    @responses.activate
    def test_get_stocks(self):
        finage = Finage(self.fake)
        response = finage.get_stocks_last(["AAPL", "TSLA", "GOGL"])
        assert response is not None

    @responses.activate
    def test_get_stock_not_null(self):
        methods = dir(Finage)
        methods = [m for m in methods if m[0:10] == "get_stock_"]
        for method in methods:
            response = self.client.__getattribute__(method)("ALK")
            try:
                assert response is not None
            except AssertionError:
                LOGGER.warning(f"{method} is None")
                raise

    @responses.activate
    def test_get_stocks_not_null(self):
        methods = dir(Finage)
        methods = [m for m in methods if m[0:11] == "get_stocks_"]
        for method in methods:
            stocks = ["AAPL", "TSLA", "GOGL"]
            response = self.client.__getattribute__(method)(stocks)
            try:
                assert response is not None
            except AssertionError:
                LOGGER.warning(f"{method} is None")
                raise
