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
