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
        try:
            result = search(company_name, first_quote=True)
            if result and 'symbol' in result:
                return result['symbol']
        except Exception as e:
            print(f"Error: {e}")
        print("Error: No result found.")
        return None

    @staticmethod
    def get_high_or_low(ticker, period=None, high=None):
        stock = yf.Ticker(ticker)
        value = stock.history(period=period)
        if high:
            return round(value['High'].max(), 2)
        else:
            return round(value['Low'].min(), 2)