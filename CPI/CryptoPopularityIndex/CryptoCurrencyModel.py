class CryptoCurrency(object):

    # Initializing these fields to 0 before they are populated
    # That's a security thing, right? (This is really so I don't forget these attributes)
    def __init__(self, name):
        self.name = name
        self.price = 0;
        self.percentChange = 0
        self.monthlyAverage = 0;
        self.weeklyAverage = 0;
        self.threeDayAverage = 0;

    def set_trend(self, trend):
        self.trend = trend