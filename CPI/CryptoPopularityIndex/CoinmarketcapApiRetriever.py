import json, requests, operator, boto3
from time import sleep
import GoogleTrendsRetriever, CryptoCurrencyModel


# This function calls out to the API of Coinmarketcap.com and gets the top 100 coins as
# determined by their respective market caps
def retrieveCurrencies():

    # The URL of the API
    url = 'https://api.coinmarketcap.com/v1/ticker/'

    # Calling out and getting the returned JSON data
    response = requests.get(url)
    jsonData = response.json()

    # Initializing the list of currencies
    currencyList = list()

    # Parsing the JSON data and adding a currency object for each returned currency
    for item in jsonData:
        name = item.get("name")
        price = item.get("price_usd")
        currency = CryptoCurrencyModel.CryptoCurrency(name)
        currency.price = ('$' + price)
        currencyList.append(currency)

    # This loops over the currency list and makes calls to Google Trends for each.
    # Note that there is a sleep(2) here - this is because I don't want to DOS google by spamming requests
    for currency in currencyList:
        currency = GoogleTrendsRetriever.findTrend(currency)
        print (currencyList.index(currency), '% complete')
        sleep(2)  # Time in seconds.

    # Sort the list by the "percentChange" attribute (the recent change in it's popularity)
    currencyList.sort(key=operator.attrgetter('percentChange'), reverse=True)

    return currencyList
