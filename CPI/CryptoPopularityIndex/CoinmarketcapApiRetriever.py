import requests, operator, logging, json, os
from requests import Session
from time import sleep
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import GoogleTrendsRetriever


# This function calls out to the API of Coinmarketcap.com and gets the top 100 coins as
# determined by their respective market caps
def retrieveCurrencies():

    # The URL of the API for Coinmarketcap
    url = 'https://api.coinmarketcap.com/v1/ticker/'

    # My API key is stored on the server running this
    API_KEY = os.environ['COINMARKETCAP_API_KEY']

    # Params and headers for calling the coinmarketcap API
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    parameters = {
        'start': '1',
        'limit': '100',
        'convert': 'USD'
    }
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': API_KEY,
    }
    session = Session()
    session.headers.update(headers)

    # Calling out and getting the returned JSON data
    try:
        response = session.get(url, params=parameters)
        jsonData = response.json()
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        logging.error('Error caught during CoinMarketCap API call: ' + e)

    # Initializing the list of currencies
    currencyList = list()

    # Creating a model object for a Cryptocurrency
    class CryptoCurrencyModel():
        def __init__(self, name, price, symbol, id):
            self.name = name
            self.price = price
            self.symbol = symbol
            self.id = id
            # Initializing this guy to 0, he'll be set later
            self.percentChange = 0

    # Parsing the JSON data and adding a currency object for each returned currency
    for item in jsonData['data']:
        name = item.get("name")
        price = item['quote']['USD'].get("price")
        symbol = item.get("symbol")
        id = item.get("slug")
        monetaryDayChange = item['quote']['USD'].get("percent_change_24h")

        currency = CryptoCurrencyModel(name, price, symbol, id)
        currency.price = price
        currency.symbol = symbol
        currency.dailyMonetaryChange = monetaryDayChange
        currencyList.append(currency)

    # This loops over the currency list and makes calls to Google Trends for each.
    # Note that there is a sleep(2) here - this is because I don't want to DOS google by spamming requests
    logging.info("Calling out to Google Trends.")
    for currency in currencyList:
        currency = GoogleTrendsRetriever.findTrend(currency)
        sleep(2)  # Time in seconds.

    # Sort the list by the "percentChange" attribute (the recent change in it's popularity)
    currencyList.sort(key=operator.attrgetter('percentChange'), reverse=True)

    return currencyList
