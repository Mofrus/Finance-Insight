# src/Stocks/StockDataHandler.py
import yfinance as yf
from yahooquery import Ticker, search
import logging

logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s - %(message)s')

class StockDataHandler:
    """Class for handling stock data operations."""

    @staticmethod
    def search_stock(company_name):
        """Search for a stock ticker by company name."""
        try:
            results = search(company_name)
            if results and len(results['quotes']) > 0:
                return results['quotes'][0]['symbol']
            return None
        except Exception as e:
            logging.error(f"Error searching for stock: {str(e)}")
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
        """Update stock data for the specified period."""
        try:
            ticker = Ticker(stock)
            history = ticker.history(period=period)
            if history.empty:
                return f"No data available for {stock}"

            if high_or_low == "High":
                max_price = history['high'].max()
                return (
                    f"{stock} highest price in {period}: "
                    f"${max_price:.2f}"
                )
            else:
                min_price = history['low'].min()
                return (
                    f"{stock} lowest price in {period}: "
                    f"${min_price:.2f}"
                )
        except Exception as e:
            logging.error(f"Error updating data: {str(e)}")
            return f"Error getting data for {stock}"

    @staticmethod
    def search_tickers(companies):
        """Search for multiple stock tickers."""
        try:
            tickers = []
            for company in companies:
                ticker = StockDataHandler.search_stock(company)
                if ticker:
                    tickers.append(ticker)
            return tickers
        except Exception as e:
            logging.error(f"Error searching tickers: {str(e)}")
            return []
    

    @staticmethod
    def get_basic_info(ticker):
        """Get basic information about a stock."""
        try:
            stock = Ticker(ticker)
            info = stock.price[ticker]
            return (
                f"Symbol: {ticker}\n"
                f"Name: {info.get('longName', 'N/A')}\n"
                f"Current Price: ${info.get('regularMarketPrice', 'N/A')}\n"
                f"Market Change: {info.get('regularMarketChangePercent', 'N/A')}%"
            )
        except Exception as e:
            logging.error(f"Error getting basic info: {str(e)}")
            return f"Error getting information for {ticker}"