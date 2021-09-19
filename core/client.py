import os
import requests
from urllib.parse import urlencode
import logging


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler()
    ]
)


class Finage(object):
    api_root = "https://api.finage.co.uk"

    def __init__(self, api_key=None):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel("INFO")
        env_key = os.environ.get("FINAGE_KEY")
        if api_key is not None:
            self.api_key = api_key
        elif env_key is not None:
            self.api_key = env_key
        else:
            raise ValueError("Needs an API key")

    def get_request(endpoint, is_symbol=True):
        def decorator(func):
            def wrapper_request(*args, **kwargs):
                data = {}
                self = args[0]
                arg_names = func.__code__.co_varnames
                rev_arg_names = list(reversed(arg_names))
                if func.__defaults__ is not None:
                    defaults = list(reversed(func.__defaults__))
                    for i in range(len(defaults)):
                        data[rev_arg_names[i]] = defaults[i]
                if len(args) > 1:
                    for i in range(1, len(args)):
                        data[arg_names[i]] = args[i]
                for k in kwargs.keys():
                    data[k] = kwargs[k]
                if is_symbol:
                    del data["symbol"]
                    symbol = args[1]
                    url = self._make_query_string(
                        endpoint.format(symbol=symbol), data=data)
                else:
                    url = self._make_query_string(endpoint, data=data)
                response = self._make_request(url)
                self.logger.info(f"{response.status_code} GET {url}")
                return response
            return wrapper_request
        return decorator

    def _make_query_string(self, endpoint, data={}):
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
        return response

    @get_request("/last/stock/{symbol}")
    def get_stock_last(self, symbol, ts="ms"):
        pass

    def get_stocks_last(self, symbols, ts="ms"):
        endpoint = "/last/stocks"
        symbols = ",".join(symbols)
        url = self._make_query_string(endpoint, {"ts": ts, "symbols": symbols})
        response = requests.get(url)
        if response.ok:
            print(f"GET {url}")
        return response

    @get_request("/last/trade/stock/{symbol}")
    def get_stock_last_trade(self, symbol, ts="ms"):
        pass

    def get_stocks_last_trade(self, symbols, ts="ms"):
        stocks = ",".join(symbols)
        endpoint = "/last/trade/stocks"
        url = self._make_query_string(endpoint, {"ts": ts, "symbols": stocks})
        return self._make_request(url)

    @get_request("/history/stock/open-close")
    def get_stock_end_of_day(self, symbol, date="2021-06-01"):
        pass

    @get_request("/history/stock/all", False)
    def get_stock_historical_book(
        self, stock, date="2021-06-01", limit=20
    ):
        pass

    def get_stock_aggregates(
        self,
        symbol,
        multiply=1,
        time="day",
        from_dt="2021-06-01",
        to_dt="2021-09-01",
    ):
        endpoint = f"/agg/stock/{symbol}/{multiply}/{time}/{from_dt}/{to_dt}"
        url = self._make_query_string(endpoint, {})
        return self._make_request(url)

    @get_request("/agg/stock/prev-close/{symbol}")
    def get_stock_previous_close(self, symbol, unadjusted=True):
        pass

    @get_request("/last/forex/{symbol}")
    def get_forex_last(self, symbol):
        pass

    @get_request("/last/trade/forex/{symbol}")
    def get_forex_last_trade(self, symbol):
        pass
