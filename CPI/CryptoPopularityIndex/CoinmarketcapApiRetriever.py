import json, requests, operator
from time import sleep
import GoogleTrendsRetriever, CryptoCurrencyModel


def retrieveCurrencies():

    url = 'https://api.coinmarketcap.com/v1/ticker/'

    response = requests.get(url)
    jsonData = response.json()

    currencyList = list()

    for item in jsonData:
        name = item.get("name")
        price = item.get("price_usd")
        currency = CryptoCurrencyModel.CryptoCurrency(name)
        currency.price = ('$' + price)
        currencyList.append(currency)

    currencyList = currencyList[-5:]

    for currency in currencyList:
        currency = GoogleTrendsRetriever.findTrend(currency)
        print (currencyList.index(currency), '% complete')
        #print(currency.name, currency.percentChange)
        sleep(2)  # Time in seconds.

        currencyList.sort(key=operator.attrgetter('percentChange'), reverse=True)

    for currency in currencyList:
        #print(currency.name, currency.percentChange)

        def obj_dict(obj):
            return obj.__dict__

        json_string = json.dumps(currencyList, default=obj_dict)

    print(json_string)

    with open('latestData.json', 'w') as outfile:
        outfile.write(json_string)

    return json_string
