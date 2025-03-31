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
    def get_high_or_low(ticker, period="1d", high=True):
        stock = yf.Ticker(ticker)
        if ticker is None:
            print("Error: Didn't find ticker.")
            return None
        value = stock.history(period=period)
        if high:
            print(f"High: {value['High'].iloc[0]}")
            return value['High'].iloc[0]
        else:
            print(f"Low: {value['Low'].iloc[0]}")
            return value['Low'].iloc[0]


StockDataHandler.search_stock("Apple")
StockDataHandler.search_stock("OIJSDGDOJSDGFNO")
StockDataHandler.get_high_or_low(StockDataHandler.search_stock("Apple"), period="1d", high=True)