import os
import requests
from urllib.parse import urlencode


class Finage(object):
    api_root = "https://api.finage.co.uk"

    def __init__(self, api_key=None):
        env_key = os.environ.get("FINAGE_KEY")
        if api_key is not None:
            self.api_key = api_key
        elif env_key is not None:
            self.api_key = env_key
        else:
            raise ValueError("Needs an API key")

    def _make_query_string(self, endpoint, data):
        data_list = list(data.items())
        data_list.insert(0, ("apikey", self.api_key))
        encoded = urlencode(data_list)
        query_string = f"{self.api_root}{endpoint}?{encoded}"
        return query_string

    def _make_request(self, query, headers=None):
        self.session = requests.session()
        if headers is not None:
            self.session.headers.update(headers)
        response = self.session.get(query, timeout=1)
        if response.ok:
            print(f"Successful GET {query}")
        else:
            print(f"Failed GET {query}")
        return response

    def get_stock_last(self, symbol, ts="ms"):
        endpoint = f"/last/stock/{symbol}"
        url = self._make_query_string(endpoint, {"ts": ts})
        return self._make_request(url)

    def get_stocks_last(self, symbols, ts="ms"):
        endpoint = "/last/stocks"
        symbols = ",".join(symbols)
        url = self._make_query_string(endpoint, {"ts": ts, "symbols": symbols})
        response = requests.get(url)
        if response.ok:
            print(f"GET {url}")
        return response

    def get_stock_last_trade(self, symbol, ts="ms"):
        endpoint = f"/last/trade/stock/{symbol}"
        url = self._make_query_string(endpoint, {"ts": ts})
        return self._make_request(url)

    def get_stocks_last_trade(self, symbols, ts="ms"):
        stocks = ",".join(symbols)
        endpoint = "/last/trade/stocks"
        url = self._make_query_string(endpoint, {"ts": ts, "symbols": stocks})
        return self._make_request(url)

    def get_stock_end_of_day(self, symbol, dt="2021-06-01"):
        endpoint = "/history/stock/open-close"
        url = self._make_query_string(endpoint, {"stock": symbol, "date": dt})
        return self._make_request(url)

    def get_stock_historical_book(
        self, symbol, dt="2021-06-01", limit=50, **kwargs
    ):
        endpoint = "/history/stock/all"
        data = {"stock": symbol, "date": dt, "limit": limit}
        url = self._make_query_string(endpoint, data)
        return self._make_request(url)

    def get_stock_aggregates(
        self,
        symbol,
        multiply=1,
        time="day",
        from_dt="2021-06-01",
        to_dt="2021-09-01",
    ):
        if time not in [
            "minute",
            "hour",
            "day",
            "week",
            "month",
            "quarter",
            "year",
        ]:
            raise ValueError("Invalid time")
        endpoint = f"/agg/stock/{symbol}/{multiply}/{time}/{from_dt}/{to_dt}"
        url = self._make_query_string(endpoint, {})
        return self._make_request(url)

    def get_stock_previous_close(self, symbol, unadj=True):
        endpoint = f"/agg/stock/prev-close/{symbol}"
        url = self._make_query_string(endpoint, {"unadjusted": str(unadj)})
        return self._make_request(url)
