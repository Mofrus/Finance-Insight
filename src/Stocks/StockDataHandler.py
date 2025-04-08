# src/Stocks/StockDataHandler.py
import yfinance as yf
from yahooquery import *
import logging

logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s - %(message)s')

class StockDataHandler:
    @staticmethod
    def search_stock(company_name):
        try:
            result = search(company_name, first_quote=True)
            if result and 'symbol' in result:
                logging.info(f"Ticker for {company_name}: {result['symbol']}")
                return result['symbol']
        except Exception as e:
            logging.error(f"Error: {e}")
        logging.error("Error: No result found.")
        return None

    @staticmethod
    def get_high_or_low(ticker, period=None, high=None):
        stock = yf.Ticker(ticker)
        value = stock.history(period=period)
        if high:
            return round(value['High'].max(), 2)
        else:
            return round(value['Low'].min(), 2)

    @staticmethod
    def update_loading_text(stock, high_or_low, period, data):
        return f"{stock}'s {'High' if high_or_low == 'High' else 'Low'} for {period}: {data}$"

    @staticmethod
    def update_data(stock, high_or_low, period):
        ticker = StockDataHandler.search_stock(stock)
        if ticker:
            data = StockDataHandler.get_high_or_low(ticker, period=period, high=(high_or_low == "High"))
            result_text = StockDataHandler.update_loading_text(stock, high_or_low, period, data)
            logging.info(result_text)
            return result_text
        else:
            error_text = "Error: No result found."
            logging.error(error_text)
            return error_text

    @staticmethod
    def search_tickers(companies):
        tickers = []
        for company in companies:
            ticker = StockDataHandler.search_stock(company.strip())
            if ticker:
                tickers.append(ticker)
        return tickers
    

    @staticmethod
    def get_basic_info(stock):
        try:
            ticker = StockDataHandler.search_stock(stock)
            stock = yf.Ticker(ticker)
            info = stock.info

            revenue = info.get('totalRevenue', 'N/A')
            debt = info.get('totalDebt', 'N/A')
            profit_margin = info.get('profitMargins', 'N/A')

            result = f"Revenue: {revenue}$\nDebt: {debt}$\nProfit Margin: {profit_margin * 100}%"
            logging.info(result)
            return result
        except Exception as e:
            logging.error(f"Error fetching basic info: {e}")
            return f"Error: {e}"