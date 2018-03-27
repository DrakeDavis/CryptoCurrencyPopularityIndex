from flask import Flask, Response
from flask_cache import Cache
import CoinmarketcapApiRetriever
import threading, datetime, os, logging
app = Flask(__name__)
app.config['CACHE_TYPE'] = 'simple'
app.cache = Cache(app)

#timeout is 10800 seconds, or 3 houea
@app.route('/')
def index_page():

    # asynchronously kick off the retrieval (takes forever or google bans ip)
    t = threading.Thread(target=getLatestTrends)
    t.daemon = True
    t.start()

    # return whatever was populated last
    data = open("latestData.json", "r")
    return Response(response=data, status=200, mimetype='application/json')


def getLatestTrends():

    # Get the last time the json file was modified
    lastModifiedTime = os.path.getmtime("latestData.json")
    currentTime = datetime.datetime.now().timestamp()

    # If its been long enough, call Google Trends again for new data
    # (I did this as to not spam Google with tons of requests)
    timeDifference = currentTime - lastModifiedTime;

    # If its been at least 3600 seconds (one hour) go ahead and refresh data
    if (timeDifference > 3600):
        CoinmarketcapApiRetriever.retrieveCurrencies()
    else:
        # else, just return and use the old data
        logging.info("Not refreshing data, as its only been ", timeDifference, "seconds between calls.")
        print("Not refreshing data, as its only been ", timeDifference, "seconds between calls.")
        return

if __name__ == '__main__':
    app.run()