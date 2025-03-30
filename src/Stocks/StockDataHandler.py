import yfinance as yf
from datetime import datetime
from tzlocal import *
from yahooquery import *
import dearpygui.dearpygui as dpg
import pytz
from StockData import StockData


class StockDataHandler:
    stock_data_instances = {}

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

    @staticmethod
    def get_ticker_by_name(company_name):
        print(f"Searching for company: {company_name}")
        result = search(company_name)
        print(f"Search result: {result}")

        if result and 'quotes' in result and len(result['quotes']) > 0:
            ticker = result['quotes'][0]['symbol']
            print(f"Found ticker: {ticker}")

            if StockDataHandler.check_stock_instance(ticker):
                print("Stock data instance already exists.")
                return StockDataHandler.stock_data_instances[ticker]
            else:
                stock_data_instance = StockData(ticker)
                StockDataHandler.stock_data_instances[ticker] = stock_data_instance
                print("Stock data instance created.")
                return stock_data_instance
        else:
            print("No quotes found in search result.")
        return None

    @staticmethod
    def suggest_companies(partial_name):
        result = search(partial_name)
        if result and 'quotes' in result:
            return [StockDataHandler.get_stock_data(quote['symbol']) for quote in result['quotes']]
        return []

    @staticmethod
    def check_stock_instance(ticker):
        return ticker in StockDataHandler.stock_data_instances

StockDataHandler.get_ticker_by_name("Apple")
StockDataHandler.get_ticker_by_name("Google")
StockDataHandler.get_ticker_by_name("Apple")