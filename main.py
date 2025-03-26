import yfinance as yf
from datetime import datetime
from tzlocal import *
import pytz


class StockData:
    def __init__(self, ticker):
        self.ticker = yf.Ticker(ticker)

    # All values are in USD Default
    def getCurrentValue(self):
        return self.ticker.history(period='1d')['Close'].iloc[0]

    def getMonthValue(self):
        history = self.ticker.history(period='1mo')
        month_ago_price = history['Close'].iloc[0]
        return month_ago_price

    def getYearValue(self):
        history = self.ticker.history(period='1y')
        year_ago_price = history['Close'].iloc[0]
        return year_ago_price

    def getFiveYearValue(self):
        history = self.ticker.history(period='5y')
        fiveYears_ago_price = history['Close'].iloc[0]
        return fiveYears_ago_price

    def getDayHigh(self):
        return self.ticker.info['dayHigh']

    def getDayLow(self):
        return self.ticker.info['dayLow']

    def isMarketOpen(self, market_timezone='US/Eastern', market_open_hour=9, market_open_minute=30,market_close_hour=16, market_close_minute=0):
        market_tz = pytz.timezone(market_timezone)
        market_open_time = datetime.now(market_tz).replace(hour=market_open_hour, minute=market_open_minute, second=0,microsecond=0)
        market_close_time = datetime.now(market_tz).replace(hour=market_close_hour, minute=market_close_minute,second=0, microsecond=0)
        local_time = datetime.now(get_localzone())
        return market_open_time <= local_time <= market_close_time

Stock = StockData('AAPL')
print(Stock.isMarketOpen())