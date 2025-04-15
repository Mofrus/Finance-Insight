# src/UserGui.py
import dearpygui.dearpygui as dpg
from Stocks.StockDataHandler import StockDataHandler
from Stocks.TechnicalAnalysis import TechnicalAnalysis
import os
import webbrowser
import logging
import subprocess

# Modern color scheme
COLORS = {
    'bg_dark': (15, 15, 15, 255),
    'bg_light': (25, 25, 25, 255),
    'accent': (0, 122, 255, 255),
    'accent_hover': (0, 102, 235, 255),
    'text': (255, 255, 255, 255),
    'text_secondary': (180, 180, 180, 255),
    'border': (40, 40, 40, 255),
    'success': (46, 213, 115, 255),
    'warning': (255, 171, 0, 255),
    'error': (255, 71, 87, 255)
}

def setup_theme():
    with dpg.theme() as global_theme:
        with dpg.theme_component(dpg.mvAll):
            dpg.add_theme_color(dpg.mvThemeCol_WindowBg, COLORS['bg_dark'])
            dpg.add_theme_color(dpg.mvThemeCol_TitleBg, COLORS['bg_light'])
            dpg.add_theme_color(dpg.mvThemeCol_TitleBgActive, COLORS['bg_light'])
            dpg.add_theme_color(dpg.mvThemeCol_Button, COLORS['accent'])
            dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, COLORS['accent_hover'])
            dpg.add_theme_color(dpg.mvThemeCol_Text, COLORS['text'])
            dpg.add_theme_color(dpg.mvThemeCol_Border, COLORS['border'])
            dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 8)
            dpg.add_theme_style(dpg.mvStyleVar_WindowRounding, 8)
            dpg.add_theme_style(dpg.mvStyleVar_FramePadding, 10, 6)
            dpg.add_theme_style(dpg.mvStyleVar_ItemSpacing, 10, 6)
            dpg.add_theme_style(dpg.mvStyleVar_ScrollbarSize, 14)
            dpg.add_theme_style(dpg.mvStyleVar_ScrollbarRounding, 8)
            dpg.add_theme_style(dpg.mvStyleVar_GrabMinSize, 10)
            dpg.add_theme_style(dpg.mvStyleVar_GrabRounding, 8)
    return global_theme

def resize_callback(sender, app_data):
    width, height = dpg.get_viewport_client_width(), dpg.get_viewport_client_height()
    dpg.set_item_width("main_window", width)
    dpg.set_item_height("main_window", height)
    dpg.set_item_width("main_content", width - 220)  # Adjust for sidebar width and padding
    dpg.set_item_height("main_content", height)

def create_card(title, content_callback):
    with dpg.group(horizontal=True):
        with dpg.child_window(width=300, height=200, no_scrollbar=True):
            dpg.add_text(title, color=COLORS['accent'])
            dpg.add_separator()
            content_callback()

def show_basic_info_callback():
    dpg.delete_item("main_content", children_only=True)
    with dpg.group(parent="main_content"):
        dpg.add_text("Company Information", color=COLORS['accent'], tag="section_title")
        with dpg.group(horizontal=True):
            dpg.add_input_text(label="Company or Ticker", tag="info_input", width=300)
            dpg.add_button(label="Get Info", callback=display_basic_info)
        dpg.add_text("", tag="info_output")

def show_day_low_callback():
    dpg.delete_item("main_content", children_only=True)
    with dpg.group(parent="main_content"):
        dpg.add_text("Price Analysis", color=COLORS['accent'], tag="section_title")
        with dpg.group(horizontal=True):
            dpg.add_input_text(label="Stock", tag="stock_input", width=300)
            dpg.add_button(label="Get Data", callback=update_data)
        with dpg.group(horizontal=True):
            dpg.add_radio_button(items=["High", "Low"], horizontal=True, tag="hi_lw_rad_btn_input", default_value="High")
            dpg.add_radio_button(items=["1d", "5d", "1mo", "6mo", "1y", "5y"], horizontal=True, tag="period_rad_btn_input", default_value="1d")
        dpg.add_text("", tag="loading_text")

def find_ticker_callback():
    dpg.delete_item("main_content", children_only=True)
    with dpg.group(parent="main_content"):
        dpg.add_text("Ticker Search", color=COLORS['accent'], tag="section_title")
        with dpg.group(horizontal=True):
            dpg.add_input_text(tag="company_input", width=300)
            dpg.add_button(label="Find Tickers", callback=display_tickers)
        dpg.add_text("", tag="ticker_output")

def show_chart_callback():
    dpg.delete_item("main_content", children_only=True)
    with dpg.group(parent="main_content"):
        dpg.add_text("Technical Analysis", color=COLORS['accent'], tag="section_title")
        with dpg.group(horizontal=True):
            dpg.add_input_text(label="Company or Ticker", tag="chart_ticker_input", width=300)
            dpg.add_button(label="Generate Chart", callback=generate_chart)
        with dpg.group(horizontal=True):
            dpg.add_radio_button(items=["1d", "5d", "1mo", "3mo", "6mo", "1y", "5y"], 
                               horizontal=True, tag="chart_period_input", default_value="1mo")
        with dpg.group(horizontal=True):
            dpg.add_checkbox(label="SMA20", tag="sma20_check", default_value=True)
            dpg.add_checkbox(label="SMA50", tag="sma50_check", default_value=True)
            dpg.add_checkbox(label="RSI", tag="rsi_check", default_value=True)
        dpg.add_text("", tag="chart_status")
        dpg.add_button(label="Open Chart Folder", callback=open_charts_folder)

def create_sidebar():
    with dpg.child_window(width=200, height=-1, tag="sidebar"):
        with dpg.group(horizontal=False):
            dpg.add_text("Stock Market Analysis", color=COLORS['accent'])
            dpg.add_separator()
            dpg.add_button(label="Price Analysis", callback=show_day_low_callback, width=180)
            dpg.add_button(label="Ticker Search", callback=find_ticker_callback, width=180)
            dpg.add_button(label="Company Info", callback=show_basic_info_callback, width=180)
            dpg.add_button(label="Technical Chart", callback=show_chart_callback, width=180)
            dpg.add_separator()
            dpg.add_button(label="Open Log", callback=print_info_callback, width=180)
            dpg.add_button(label="Exit", callback=lambda: dpg.stop_dearpygui(), width=180)

def print_info_callback():
    os.startfile('app.log')

def display_basic_info():
    dpg.set_value("info_output", "Loading data...")
    input_value = dpg.get_value("info_input")
    result = StockDataHandler.get_basic_info(input_value)
    dpg.set_value("info_output", result)

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

def generate_chart():
    dpg.set_value("chart_status", "Generating chart...")
    input_value = dpg.get_value("chart_ticker_input")
    
    # Validate input
    if not input_value or input_value.strip() == "":
        dpg.set_value("chart_status", "Error: Please enter a valid company name or ticker symbol")
        return
    
    # Always try to find ticker using search_stock
    dpg.set_value("chart_status", "Looking up ticker symbol...")
    ticker = StockDataHandler.search_stock(input_value)
    if not ticker:
        dpg.set_value("chart_status", f"Error: Could not find ticker for {input_value}")
        return
    
    dpg.set_value("chart_ticker_input", ticker)  # Update the input field with the found ticker
    
    period = dpg.get_value("chart_period_input")
    
    # Get selected indicators
    indicators = []
    if dpg.get_value("sma20_check"):
        indicators.append("SMA20")
    if dpg.get_value("sma50_check"):
        indicators.append("SMA50")
    if dpg.get_value("rsi_check"):
        indicators.append("RSI")
    
    # Generate chart
    chart_path = TechnicalAnalysis.create_chart(ticker, period, indicators)
    
    # Check if chart was created successfully
    if chart_path.startswith("Error"):
        dpg.set_value("chart_status", chart_path)
    else:
        dpg.set_value("chart_status", f"Chart generated successfully at: {chart_path}")
        
        # Open the chart in the default browser
        try:
            # Convert to file URL format
            file_url = f"file:///{chart_path.replace(os.sep, '/')}"
            logging.info(f"Opening chart at: {file_url}")
            webbrowser.open(file_url)
        except Exception as e:
            error_msg = f"Error opening chart: {str(e)}"
            logging.error(error_msg)
            dpg.set_value("chart_status", f"{dpg.get_value('chart_status')} But couldn't open in browser: {error_msg}")

def open_charts_folder():
    """Open the charts folder in file explorer"""
    try:
        charts_path = os.path.abspath("charts")
        if os.path.exists(charts_path):
            if os.name == 'nt':  # Windows
                os.startfile(charts_path)
            else:  # macOS and Linux
                subprocess.call(['open', charts_path])
            logging.info(f"Opened charts folder: {charts_path}")
        else:
            dpg.set_value("chart_status", "Charts folder not found. Creating it now...")
            os.makedirs(charts_path, exist_ok=True)
            if os.name == 'nt':  # Windows
                os.startfile(charts_path)
            else:  # macOS and Linux
                subprocess.call(['open', charts_path])
    except Exception as e:
        error_msg = f"Error opening charts folder: {str(e)}"
        logging.error(error_msg)
        dpg.set_value("chart_status", error_msg)

dpg.create_context()
dpg.create_viewport(title='Stock Market Analysis', width=1200, height=800, resizable=True)
dpg.setup_dearpygui()

# Apply modern theme
theme = setup_theme()
dpg.bind_theme(theme)

# Create main window with full viewport size and proper positioning
with dpg.window(label="Main Window", tag="main_window", no_title_bar=True, no_resize=True, no_move=True, pos=(0,0), autosize=True):
    with dpg.group(horizontal=True):
        create_sidebar()
        with dpg.child_window(width=-1, height=-1, tag="main_content"):
            show_day_low_callback()

# Set initial window size
dpg.set_viewport_resize_callback(resize_callback)
resize_callback(None, None)  # Call once to set initial size

dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()