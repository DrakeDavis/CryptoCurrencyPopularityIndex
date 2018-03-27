from flask import Flask, Response
from flask_cache import Cache

from CryptoPopularityIndex.DataRetrievers import CoinmarketcapApiRetriever

app = Flask(__name__)
app.config['CACHE_TYPE'] = 'simple'
app.cache = Cache(app)

@app.route('/')
@app.cache.cached(timeout=3000)
def hello_world():
    retrievedCurrencyList = CoinmarketcapApiRetriever.retrieveCurrencies()
    return Response(response=retrievedCurrencyList, status=200, mimetype='application/json')


if __name__ == '__main__':
    app.run()