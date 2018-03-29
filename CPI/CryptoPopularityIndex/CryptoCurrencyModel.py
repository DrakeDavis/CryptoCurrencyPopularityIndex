class CryptoCurrency(object):

    # Initializing these fields to 0 before they are populated
    # That's a security thing, right? (This is really so I don't forget these attributes)
    def __init__(self, name):
        self.name = name
        self.price = 0;
        self.percentChange = 0
        # This is an ambitious field in case I want to update different currencies at different intervals
        self.lastUpdated = 0;

    def set_trend(self, trend):
        self.trend = trend