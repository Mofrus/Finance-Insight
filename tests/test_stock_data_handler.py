# tests/test_stock_data_handler.py
import pytest
from src.Stocks.StockDataHandler import StockDataHandler
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

def test_search_tickers():
    # Test with a known company name
    companies = ["Apple"]
    tickers = StockDataHandler.search_tickers(companies)
    assert isinstance(tickers, list)
    assert len(tickers) > 0
    assert "AAPL" in tickers

def test_update_data():
    # Test with a known stock symbol and period
    stock = "AAPL"
    high_or_low = "High"
    period = "1d"
    result = StockDataHandler.update_data(stock, high_or_low, period)
    assert isinstance(result, str)
    assert "AAPL" in result

def test_search_stock():
    # Test with a known company name
    result = StockDataHandler.search_stock("Apple")
    assert result == "AAPL"