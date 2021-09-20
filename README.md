# Finage Python Client

The unofficial Python library for accessing the [Finage](https://finage.co.uk/docs/api/getting-started)
REST API. Though a work in progress, this package can already fetch data on stocks, forex, and fundamentals.

## Installation

The package can be installed directly from PyPI with `pip`:

```
pip install finage
```

## Usage

You need an [API](https://moon.finage.co.uk/login) key to use this product.
Once you have that key, there are a couple options. You can either 
save it as and environment variable (`export FINAGE_KEY=<api_key>`), or you can pass it directly to the
client class `Finage` as is done in the below example:

```python
from finage import Finage

api_key = "FAKE_KEY"
client = Finage(api_key)
resp = client.get_stock_last("AMZN")
resp.json()
```

## License
[MIT](https://choosealicense.com/licenses/mit/)
