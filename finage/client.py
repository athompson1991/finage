import os
import requests
from urllib.parse import urlencode
import logging
import re


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

    def get_request(endpoint):
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
                if "symbols" in data.keys():
                    data["symbols"] = ",".join(data["symbols"])
                fargs = re.findall("\\{[a-z_]+\\}", endpoint)
                names = [a.replace("{", "").replace("}", "") for a in fargs]
                if len(names) > 0:
                    kwargs = {n: data[n] for n in names}
                    for n in names:
                        del data[n]
                    url = self._make_query_string(
                        endpoint.format(**kwargs), data=data)
                else:
                    url = self._make_query_string(endpoint, data=data)
                response = self._make_request(url)
                return response
            return wrapper_request
        return decorator

    def _make_query_string(self, endpoint, data={}):
        data_list = list(data.items())
        data_list.insert(0, ("apikey", self.api_key))
        encoded = urlencode(data_list)
        query_string = f"{self.api_root}{endpoint}?{encoded}"
        return query_string

    def _make_request(self, url, headers=None):
        self.session = requests.session()
        if headers is not None:
            self.session.headers.update(headers)
        response = self.session.get(url, timeout=1)
        self.logger.info(f"{response.status_code} GET {url}")
        return response

    @get_request("/last/stock/{symbol}")
    def get_stock_last(self, symbol, ts="ms"):
        pass

    @get_request("/last/stocks")
    def get_stocks_last(self, symbols, ts="ms"):
        pass

    @get_request("/last/trade/stock/{symbol}")
    def get_stock_last_trade(self, symbol, ts="ms"):
        pass

    @get_request("/last/trade/stocks")
    def get_stocks_last_trade(self, symbols, ts="ms"):
        pass

    @get_request("/history/stock/open-close")
    def get_stock_end_of_day(self, stock, date="2021-06-01"):
        pass

    @get_request("/history/stock/all")
    def get_stock_hist_book(self, stock, date="2021-06-01", limit=20):
        pass

    @get_request("/agg/stock/{symbol}/{multiply}/{time}/{from_dt}/{to_dt}")
    def get_stock_aggregates(
        self,
        symbol,
        multiply=1,
        time="day",
        from_dt="2021-06-01",
        to_dt="2021-09-01",
    ):
        pass

    @get_request("/agg/stock/prev-close/{symbol}")
    def get_stock_previous_close(self, symbol, unadjusted=True):
        pass

    @get_request("/last/forex/{symbol}")
    def get_forex_last(self, symbol):
        pass

    @get_request("/last/trade/forex/{symbol}")
    def get_forex_last_trade(self, symbol):
        pass

    @get_request("/history/ticks/forex/{symbol}/{date}")
    def get_forex_hist_tick(self, symbol, date="2021-06-01", limit=10):
        pass

    @get_request("/agg/forex/prev-close/{symbol}")
    def get_forex_previous_close(self, symbol, unadjusted=True):
        pass

    @get_request("/agg/forex/{symbol}/{multiply}/{time}/{from_dt}/{to_dt}")
    def get_forex_aggregates(
        self,
        symbol,
        multiply=1,
        time="day",
        from_dt="2021-06-01",
        to_dt="2021-09-01",
    ):
        pass

    @get_request("/convert/forex/{from_}/{to}/{amount}")
    def get_forex_convert(self, from_, to="USD", amount=1):
        pass

    @get_request("symbol-list/{market_type}")
    def get_symbol_list(self, market_type, page=1):
        pass

    @get_request("/economic-calendar")
    def get_economic_calendar(self, from_="2021-06-01", to="2021-07-01"):
        pass

    @get_request("/cash-flow-statement/{symbol}")
    def get_cash_flow_statements(self, symbol, limit=10, period="annual"):
        pass

    @get_request("/balance-sheet-statements/{symbol}")
    def get_balance_sheet(self, symbol, limit=10, period="annual"):
        pass

    @get_request("/income-statement/{symbol}")
    def get_income_statements(self, symbol, limit=10, period="annual"):
        pass

    @get_request("/detail/{symbol}")
    def get_details(self, symbol):
        pass

    @get_request("/funds/institutional-holder/{symbol}")
    def get_institutional_holders(self, symbol):
        pass

    @get_request("/funds/mutual-fund-holder/{symbol}")
    def get_mutual_fund_holders(self, symbol):
        pass

    @get_request("/funds/etf-holder/{symbol}")
    def get_etf_holders(self, symbol):
        pass

    @get_request("/funds/etf-sector-weightings/{symbol}")
    def get_etf_sector_weightings(self, symbol):
        pass

    @get_request("/funds/rss-feed")
    def get_sec_rss(self, symbol):
        pass

    @get_request("/technical-indicator/{indicator}/{time}/{symbol}")
    def get_indicator(self, symbol, indicator, time="daily", period=10):
        pass

    @get_request("/market-information/us/most-actives")
    def get_most_active(self):
        pass

    @get_request("/market-information/us/most-gainers")
    def get_most_gainers(self):
        pass

    @get_request("/market-information/us/most-losers")
    def get_most_losers(self):
        pass

    @get_request("/market-information/us/sector-performance")
    def get_sector_performance(self):
        pass

    @get_request("/market-information/us/historical-sector-performance")
    def get_sector_performance_hist(self, limit=10):
        pass

    @get_request("/search/market/{market}/{key}")
    def get_market_search(self, market, key, limit=10):
        pass

    @get_request("/search/country/{key}")
    def get_country_search(self, key, limit=10):
        pass

    @get_request("/detail/country/{country}")
    def get_country_details(self, country):
        pass

    @get_request("/search/currency/{key}")
    def get_forex_search(self, key, limit=10):
        pass

    @get_request("/detail/currency/{symbol}")
    def get_forex_details(self, symbol):
        pass

    @get_request("/search/cryptocurrency/{key}")
    def get_crypto_search(self, key, limit=10):
        pass

    @get_request("/detail/cryptocurrency/{key}")
    def get_crypto_details(self, key):
        pass
