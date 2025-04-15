# src/UserGui.py
import dearpygui.dearpygui as dpg
from src.Stocks.StockDataHandler import StockDataHandler
from src.Stocks.TechnicalAnalysis import TechnicalAnalysis
import os
import webbrowser

def resize_callback(sender, app_data):
    width, height = dpg.get_viewport_client_width(), dpg.get_viewport_client_height()
    dpg.set_item_width("library_window", width - 150)  # Adjust for navbar width
    dpg.set_item_height("library_window", height)

def print_info_callback():
    os.startfile('app.log')

def show_basic_info_callback():
    dpg.delete_item("library_window", children_only=True)
    with dpg.group(parent="library_window"):
        dpg.add_input_text(label="Company or Ticker", tag="info_input")
        dpg.add_text("Enter a company name or ticker symbol (e.g., AAPL or Apple).")
        dpg.add_button(label="Get Info", callback=display_basic_info)
        dpg.add_text("", tag="info_output")

def display_basic_info():
    dpg.set_value("info_output", "Loading data...")
    input_value = dpg.get_value("info_input")
    result = StockDataHandler.get_basic_info(input_value)
    dpg.set_value("info_output", result)

def show_day_low_callback():
    dpg.delete_item("library_window", children_only=True)
    with dpg.group(parent="library_window"):
        dpg.add_input_text(label="Stock", tag="stock_input")
        dpg.add_text("Enter the stock symbol (e.g., AAPL for Apple).")
        dpg.add_radio_button(items=["High", "Low"], horizontal=True, tag="hi_lw_rad_btn_input", default_value="High")
        dpg.add_radio_button(items=["1d", "5d", "1mo", "6mo", "1y", "5y"], horizontal=True, tag="period_rad_btn_input", default_value="1d")
        dpg.add_button(label="Print", callback=update_data)
        dpg.add_text("", tag="loading_text")

def find_ticker_callback():
    dpg.delete_item("library_window", children_only=True)
    with dpg.group(parent="library_window"):
        dpg.add_input_text(tag="company_input")
        dpg.add_text("Enter company names separated by commas (Google, Apple...).")
        dpg.add_button(label="Find Tickers", callback=display_tickers)
        dpg.add_text("", tag="ticker_output")

def display_tickers():
    dpg.set_value("ticker_output", "Loading data...")
    companies = dpg.get_value("company_input").split(',')
    tickers = StockDataHandler.search_tickers(companies)
    dpg.set_value("ticker_output", "Tickers: " + ", ".join(tickers))

def update_data():
    dpg.set_value("loading_text", "Loading data...")
    stock = dpg.get_value("stock_input")
    high_or_low = dpg.get_value("hi_lw_rad_btn_input")
    period = dpg.get_value("period_rad_btn_input")
    result_text = StockDataHandler.update_data(stock, high_or_low, period)
    dpg.set_value("loading_text", result_text)

def show_chart_callback():
    dpg.delete_item("library_window", children_only=True)
    with dpg.group(parent="library_window"):
        dpg.add_input_text(label="Stock Ticker", tag="chart_ticker_input")
        dpg.add_text("Enter the stock symbol (e.g., AAPL for Apple).")
        dpg.add_radio_button(items=["1d", "5d", "1mo", "3mo", "6mo", "1y", "5y"], 
                           horizontal=True, tag="chart_period_input", default_value="1mo")
        with dpg.group(horizontal=True):
            dpg.add_checkbox(label="SMA20", tag="sma20_check", default_value=True)
            dpg.add_checkbox(label="SMA50", tag="sma50_check", default_value=True)
            dpg.add_checkbox(label="RSI", tag="rsi_check", default_value=True)
        dpg.add_button(label="Generate Chart", callback=generate_chart)
        dpg.add_text("", tag="chart_status")

def generate_chart():
    dpg.set_value("chart_status", "Generating chart...")
    ticker = dpg.get_value("chart_ticker_input")
    period = dpg.get_value("chart_period_input")
    
    # Get selected indicators
    indicators = []
    if dpg.get_value("sma20_check"):
        indicators.append("SMA20")
    if dpg.get_value("sma50_check"):
        indicators.append("SMA50")
    if dpg.get_value("rsi_check"):
        indicators.append("RSI")
    
    chart_path = TechnicalAnalysis.create_chart(ticker, period, indicators)
    if chart_path.startswith("Error"):
        dpg.set_value("chart_status", chart_path)
    else:
        dpg.set_value("chart_status", "Chart generated successfully!")
        webbrowser.open('file://' + os.path.realpath(chart_path))

dpg.create_context()
with dpg.window(label="Navbar", tag="navbar", width=150, height=600, no_move=True, no_title_bar=True, no_resize=True):
    dpg.add_button(label="Price high or low", callback=show_day_low_callback)
    dpg.add_button(label="Find Ticker", callback=find_ticker_callback)
    dpg.add_button(label="Basic Info", callback=show_basic_info_callback)
    dpg.add_button(label="Technical Chart", callback=show_chart_callback)
    dpg.add_button(label="Open log", callback=print_info_callback)
    dpg.add_button(label="Exit", callback=lambda: dpg.stop_dearpygui())
    
with dpg.window(label="Library Window", tag="library_window", no_move=True, no_title_bar=True, pos=(150, 0), no_resize=True):
    pass

dpg.create_viewport(title='Main Window', width=650, height=300, resizable=False)
dpg.setup_dearpygui()
dpg.show_viewport()

dpg.set_viewport_resize_callback(resize_callback)

show_day_low_callback()
dpg.start_dearpygui()
dpg.destroy_context()