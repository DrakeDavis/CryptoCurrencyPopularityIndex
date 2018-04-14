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
    pytrends.build_payload(kw_list, cat=0, timeframe='today 1-m', geo='', gprop='')

    # Make the 'interest over time' call
    dataFrame = pytrends.interest_over_time()

    # Try to get a list of daily popularity over the last month
    try:
        monthlyList = dataFrame.ix[:, 0].tolist()
    except:
        return currency

    # Creating subsets of data for week and 3day
    weeklyList = (monthlyList[-7:])
    threeDatList = (weeklyList[-3:])
    lastDay = (weeklyList[-1:])

    # Getting the averages of the above lists
    monthly_Average = float(sum(monthlyList)) / len(monthlyList)
    weekly_Average = float(sum(weeklyList)) / len(weeklyList)
    threeDay_Average = float(sum(threeDatList)) / len(threeDatList)

    # Populating that data into the model object. The %.2 should truncate to 2 decimal places
    currency.monthlyAveragePopularity = ("%.2f" % monthly_Average)
    currency.weeklyAveragePopularity = ("%.2f" % weekly_Average)
    currency.threeDayAveragePopularity = ("%.2f" % threeDay_Average)
    currency.lastDayPopularity = lastDay[0]

    # Sometimes google trends returns 0 if something goes wrong. We definitely don't want to divide by 0
    if (monthly_Average != 0):
        increaseBetween3dAnd30d = threeDay_Average / monthly_Average
    else:
        increaseBetween3dAnd30d = 0

    # Populate the currency object with relevant data
    currency.percentChange = float("%.2f" % (increaseBetween3dAnd30d *100))
    currency.lastUpdated = str(int(time.time()))
    return currency
