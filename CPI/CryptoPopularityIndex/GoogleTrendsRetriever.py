from pytrends.request import TrendReq
import time

pytrends = TrendReq(hl='en-US', tz=360)

# This function calls out to Google Trends and gets the popularity metrics
# for the currency that is passed as an argument.
def findTrend(argCurrency):

    # If the cryptocurrency's name is a common word (like DASH, Neo, Tether, etc.) it will pull in non-crypto results.
    # Query the naming file and see if we should append 'coin' to the keyword to narrow results.
    with open('CryptoNaming.txt') as f:
        lines = f.read().splitlines()
        if argCurrency.name in lines:
            argCurrency.name = argCurrency.name + " coin"

    # Keyword to search for
    keyword = argCurrency.name

    # New variable that is different from the argument variable (because why not)
    currency = argCurrency

    # Build the payload, the timeframe is one month
    kw_list = [keyword]
    pytrends.build_payload(kw_list, cat=0, timeframe='now 7-d', geo='', gprop='')

    # Make the 'interest over time' call
    dataFrame = pytrends.interest_over_time()

    # Try to get a list of daily popularity over the last week. This list will contain 168 entries (one per hour, or
    # 24*7)
    try:
        weeklyPopularityList = dataFrame.iloc[:, 0].tolist()
    except:
        return currency

    # This is the popularity in the last 3 days, per hour (24*3)
    lastThreeDaysList = weeklyPopularityList[-72:]

    # The current popularity is the last index in the list of weekly popularity scores
    currentPopularity = weeklyPopularityList[-1]
    currency.currentPopularity = currentPopularity

    # Number of 0's in weekly list
    zeroCount = weeklyPopularityList.count(0);

    # If a coin had a popularity of 0 more than five times in the last week, it is exempted due to too much volatility.
    if zeroCount > 5:
        currency.isVolatile = 'true'
        return currency

    # Get Highest in list (excluding current and semi-current)
    highestPopularityInLastThreeDays = max(lastThreeDaysList[:-1])
    currency.highestPopularityInLastThreeDays = highestPopularityInLastThreeDays

    # Getting the averages of the above lists
    weekly_Average = float(sum(weeklyPopularityList)) / len(weeklyPopularityList)
    three_Day_Average = float(sum(lastThreeDaysList)) / len(lastThreeDaysList)

    # Populating that data into the model object. The %.2 should truncate to 2 decimal places
    currency.weeklyAveragePopularity = ("%.2f" % weekly_Average)
    currency.threeDayAveragePopularity = ("%.2f" % three_Day_Average)

    # Sometimes google trends returns 0 if something goes wrong. We definitely don't want to divide by 0
    if highestPopularityInLastThreeDays != 0:
        current_vs_max = currentPopularity / highestPopularityInLastThreeDays
    else:
        current_vs_max = 0

    # Populate the currency object with relevant data
    currency.percentChange = float("%.2f" % (current_vs_max * 100))
    currency.lastUpdated = str(int(time.time()))

    return currency
