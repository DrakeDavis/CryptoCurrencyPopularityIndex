from pytrends.request import TrendReq
import time

pytrends = TrendReq(hl='en-US', tz=360)


# This function calls out to Google Trends and gets the popularity metrics
# for the currency that is passed as an argument.
def findTrend(argCurrency):
    # Keyword to search for
    keyword = argCurrency.name

    # New variable that is different from the argument variable (because why not)
    currency = argCurrency

    # Build the payload, the timeframe is one month
    kw_list = [keyword]
    pytrends.build_payload(kw_list, cat=0, timeframe='now 7-d', geo='', gprop='')

    # Make the 'interest over time' call
    dataFrame = pytrends.interest_over_time()

    # Try to get a list of daily popularity over the last month
    try:
        weeklyPopularityList = dataFrame.iloc[:, 0].tolist()
    except:
        return currency

    # The current popularity is the last index in the list of weekly popularity scores
    currentPopularity = weeklyPopularityList[-1]
    currency.currentPopularity = currentPopularity

    weeklyPopularityList = [i for i in weeklyPopularityList if i != 0]

    # Getting the averages of the above lists
    weekly_Average = float(sum(weeklyPopularityList)) / len(weeklyPopularityList)

    # Populating that data into the model object. The %.2 should truncate to 2 decimal places
    currency.weeklyAveragePopularity = ("%.2f" % weekly_Average)

    # Sometimes google trends returns 0 if something goes wrong. We definitely don't want to divide by 0
    if weeklyPopularityList != 0:
        changeBetween7dAndCurrentAverage = currentPopularity / weekly_Average
    else:
        changeBetween7dAndCurrentAverage = 0

    # Populate the currency object with relevant data
    currency.percentChange = float("%.2f" % (changeBetween7dAndCurrentAverage * 100))
    currency.lastUpdated = str(int(time.time()))

    return currency
