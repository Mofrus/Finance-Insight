import dearpygui.dearpygui as dpg
from src.Stocks.StockDataHandler import StockDataHandler
import logging
import os

logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s - %(message)s')

def resize_callback(sender, app_data):
    width, height = dpg.get_viewport_client_width(), dpg.get_viewport_client_height()
    dpg.set_item_width("library_window", width - 150)  # Adjust for navbar width
    dpg.set_item_height("library_window", height)

def compare_stocks_callback():
    dpg.delete_item("library_window", children_only=True)
    with dpg.group(parent="library_window"):
        dpg.add_input_text(label="Stock 1")
        dpg.add_input_text(label="Stock 2")
        dpg.add_button(label="Compare")

def print_info_callback():
    os.startfile('app.log')


def show_day_low_callback():
    dpg.delete_item("library_window", children_only=True)
    with dpg.group(parent="library_window"):
        dpg.add_input_text(label="Stock", tag="stock_input")
        dpg.add_radio_button(items=["High", "Low"], horizontal=True, tag="hi_lw_rad_btn_input", default_value="High")
        dpg.add_radio_button(items=["1d", "5d", "1mo", "6mo", "1y", "5y"], horizontal=True, tag="period_rad_btn_input", default_value="1d")
        dpg.add_button(label="Print", callback=update_data)
        dpg.add_text("", tag="loading_text")

def update_loading_text(stock, high_or_low, period, data):
    return f"{stock}'s {'High' if high_or_low == 'High' else 'Low'} for {period}: {data}$"

def update_data():
    dpg.set_value("loading_text", "Loading data...")
    stock = dpg.get_value("stock_input")
    high_or_low = dpg.get_value("hi_lw_rad_btn_input")
    period = dpg.get_value("period_rad_btn_input")

    ticker = StockDataHandler.search_stock(stock)
    if ticker:
        data = StockDataHandler.get_high_or_low(ticker, period=period, high=(high_or_low == "High"))
        result_text = update_loading_text(stock, high_or_low, period, data)
        dpg.set_value("loading_text", result_text)
        logging.info(result_text)
    else:
        error_text = "Error: No result found."
        dpg.set_value("loading_text", error_text)
        logging.error(error_text)

dpg.create_context()
with dpg.window(label="Navbar", tag="navbar", width=150, height=600, no_move=True, no_title_bar=True, no_resize=True):
    dpg.add_button(label="Compare Stocks", callback=compare_stocks_callback)
    dpg.add_button(label="Price high or low", callback=show_day_low_callback)
    dpg.add_button(label="Open log", callback=print_info_callback)

with dpg.window(label="Library Window", tag="library_window", no_move=True, no_title_bar=True, pos=(150, 0), no_resize=True):
    dpg.add_text("This window will resize with the main window.")

dpg.create_viewport(title='Main Window', width=600, height=300, resizable=False)
dpg.setup_dearpygui()
dpg.show_viewport()

dpg.set_viewport_resize_callback(resize_callback)

dpg.start_dearpygui()
dpg.destroy_context()