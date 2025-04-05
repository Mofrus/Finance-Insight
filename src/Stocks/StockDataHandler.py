import yfinance as yf
from datetime import datetime
from tzlocal import *
from yahooquery import *
import dearpygui.dearpygui as dpg
import pytz

class StockDataHandler:
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