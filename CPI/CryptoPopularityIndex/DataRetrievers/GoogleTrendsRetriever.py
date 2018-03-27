from pytrends.request import TrendReq

pytrends = TrendReq(hl='en-US', tz=360)


def findTrend(argCurrency):

    # Keyword to search for is the coin name + 'crypto' as some names are ambigous
    keyword = argCurrency.name

    # New variable that is different from the argument variable (because why not)
    currency = argCurrency

    # Build the payload, the timeframe is one month
    kw_list = [keyword]
    pytrends.build_payload(kw_list, cat=0, timeframe='today 1-m', geo='', gprop='')

    # Make the 'interest over time' call
    dataFrame = pytrends.interest_over_time()

    try:
        monthlyList = dataFrame.ix[:, 0].tolist()
    except:
        return currency

    # Creating subsets of data for week and 3day
    weeklyList = (monthlyList[-7:])
    threeDatList = (weeklyList[-3:])

    # Getting the averages of the above lists
    monthly_Average = float(sum(monthlyList)) / len(monthlyList)
    weekly_Average = float(sum(weeklyList)) / len(weeklyList)
    threeDay_Average = float(sum(threeDatList)) / len(threeDatList)

    # Populating that data into the model object. The %.2 should truncate to 2 decimal places
    currency.monthlyAverage = ("%.2f" % monthly_Average)
    currency.weeklyAverage = ("%.2f" % weekly_Average)
    currency.threeDayAverage = ("%.2f" % threeDay_Average)

    #print("30d average: ", monthly_Average)
    #print("7d average: ", weekly_Average)
    #print("3d average: ", threeDay_Average)

    # Sometimes google trends returns 0 erroneously. We definitely don't want to divide by 0
    if (weekly_Average != 0):
        increaseBetween3dAnd7d = threeDay_Average / weekly_Average
    else:
        increaseBetween3dAnd7d = 0

    currency.percentChange = float("%.2f" % (increaseBetween3dAnd7d *100))

    #print('Percent change from 3d as compared to 7d:', increaseBetween3dAnd7d * 100, "%")

    return currency
