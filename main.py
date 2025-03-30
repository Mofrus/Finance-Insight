import yfinance as yf
from datetime import datetime
from tzlocal import *
from yahooquery import *
import dearpygui.dearpygui as dpg
import pytz


class StockData:
    def __init__(self, ticker):
        self.ticker = yf.Ticker(ticker)

    # All values are in USD Default
    def get_current_value(self):
        return self.ticker.history(period='1d')['Close'].iloc[0]

    def get_month_value(self):
        history = self.ticker.history(period='1mo')
        month_ago_price = history['Close'].iloc[0]
        return month_ago_price

    def get_year_value(self):
        history = self.ticker.history(period='1y')
        year_ago_price = history['Close'].iloc[0]
        return year_ago_price

    def get_five_year_value(self):
        history = self.ticker.history(period='5y')
        five_years_ago_price = history['Close'].iloc[0]
        return five_years_ago_price

    def get_day_high(self):
        return self.ticker.info['dayHigh']

    def get_day_low(self):
        return self.ticker.info['dayLow']

    def is_market_open(self, market_timezone='US/Eastern', market_open_hour=9, market_open_minute=30, market_close_hour=16, market_close_minute=0):
        market_tz = pytz.timezone(market_timezone)
        market_open_time = datetime.now(market_tz).replace(hour=market_open_hour, minute=market_open_minute, second=0, microsecond=0)
        market_close_time = datetime.now(market_tz).replace(hour=market_close_hour, minute=market_close_minute, second=0, microsecond=0)
        local_time = datetime.now(get_localzone())
        return market_open_time <= local_time <= market_close_time


class StockDataHandler:
    @staticmethod
    def compare_day_high(stock1, stock2):
        return stock1.get_day_high() - stock2.get_current_value()

    @staticmethod
    def compare_day_low(stock1, stock2):
        return stock1.get_day_low() - stock2.get_current_value()

    @staticmethod
    def compare_month_value(stock1, stock2):
        return stock1.get_month_value() - stock2.get_current_value()

    @staticmethod
    def compare_year_value(stock1, stock2):
        return stock1.get_year_value() - stock2.get_current_value()

    @staticmethod
    def get_ticker_by_name(company_name):
        result = search(company_name)
        if result and 'quotes' in result and len(result['quotes']) > 0:
            return result['quotes'][0]['symbol']
        return None
    
    @staticmethod
    def suggest_companies(partial_name):
        result = search(partial_name)
        if result and 'quotes' in result:
            return [quote['shortname'] for quote in result['quotes']]
        return []



# testStock = StockData(StockDataHandler.get_ticker_by_name('Apple'))
# google_stock = StockData('GOOGL')
#
# print(StockDataHandler.compare_day_high(testStock, google_stock))