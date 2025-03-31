import yfinance as yf
from datetime import datetime
from tzlocal import *
from yahooquery import *
import dearpygui.dearpygui as dpg
import pytz

class StockDataHandler:
    """
        @staticmethod
    def get_stock_data(ticker):
        if ticker not in StockDataHandler.stock_data_instances:
            StockDataHandler.stock_data_instances[ticker] = StockData(ticker)
        return StockDataHandler.stock_data_instances[ticker]

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
    """

    @staticmethod
    def search_stock(company_name):
        result = search(company_name, first_quote=True)
        if result and 'symbol' in result:
            print(f"Found ticker: {result['symbol']}")
            return result['symbol']
        print("Error: No result found.")
        return None

    @staticmethod
    def get_high_or_low(ticker, period=None, high=None):
        if ticker is None:
            print("Error: Didn't find ticker.")
            return None
        stock = yf.Ticker(ticker)
        value = stock.history(period=period)
        if high:
            high_value = value['High'].iloc[-1]
            print(f"High: {round(high_value, 2)}")
            return round(high_value, 2)
        else:
            low_value = value['Low'].iloc[-1]
            print(f"Low: {round(low_value, 2)}")
            return round(low_value, 2)
