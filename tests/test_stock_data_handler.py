import pytest
from src.Stocks.StockDataHandler import StockDataHandler

def test_search_tickers():
    companies = ["Apple"]
    tickers = StockDataHandler.search_tickers(companies)
    assert isinstance(tickers, list)
    assert len(tickers) > 0
    assert "AAPL" in tickers

def test_update_data():
    stock = "AAPL"
    high_or_low = "High"
    period = "1d"
    result = StockDataHandler.update_data(stock, high_or_low, period)
    assert isinstance(result, str)
    assert "AAPL" in result

def test_search_stock():
    result = StockDataHandler.search_stock("Apple")
    assert result == "AAPL"