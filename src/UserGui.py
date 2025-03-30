import dearpygui.dearpygui as dpg
import yfinance as yf
from datetime import datetime
from tzlocal import *
from yahooquery import *
import pytz

def resize_callback(sender, app_data):
    width, height = dpg.get_viewport_client_width(), dpg.get_viewport_client_height()
    dpg.set_item_width("library_window", width - 150)  # Adjust for navbar width
    dpg.set_item_height("library_window", height)
    dpg.set_item_pos("print_info_button", (0, height - 50))  # Adjust position of the button

def compare_stocks_callback():
    dpg.delete_item("library_window", children_only=True)
    with dpg.group(parent="library_window"):
        dpg.add_input_text(label="Stock 1")
        dpg.add_input_text(label="Stock 2")
        dpg.add_button(label="Compare")

def print_info_callback():
    dpg.delete_item("library_window", children_only=True)
    with dpg.group(parent="library_window"):
        dpg.add_text("Print Info button clicked")

def show_day_low_callback():
    dpg.delete_item("library_window", children_only=True)
    with dpg.group(parent="library_window"):
        dpg.add_text("Show Day Low button clicked")

dpg.create_context()

with dpg.window(label="Navbar", tag="navbar", width=150, height=600, no_move=True, no_title_bar=True):
    dpg.add_button(label="Compare Stocks", callback=compare_stocks_callback)
    dpg.add_button(label="Show Day Low", callback=show_day_low_callback)
    dpg.add_button(label="Print Info", callback=print_info_callback, tag="print_info_button", pos=(0, 550))

with dpg.window(label="Library Window", tag="library_window", no_move=True, no_title_bar=True, pos=(150, 0)):
    dpg.add_text("This window will resize with the main window.")

dpg.create_viewport(title='Main Window', width=600, height=600)
dpg.setup_dearpygui()
dpg.show_viewport()

dpg.set_viewport_resize_callback(resize_callback)

dpg.start_dearpygui()
dpg.destroy_context()