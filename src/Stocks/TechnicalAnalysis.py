import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import logging
import os

class TechnicalAnalysis:
    @staticmethod
    def calculate_sma(data, window):
        """Calculate Simple Moving Average"""
        return data['Close'].rolling(window=window).mean()
    
    @staticmethod
    def calculate_ema(data, window):
        """Calculate Exponential Moving Average"""
        return data['Close'].ewm(span=window, adjust=False).mean()
    
    @staticmethod
    def calculate_rsi(data, periods=14):
        """Calculate Relative Strength Index"""
        delta = data['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=periods).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=periods).mean()
        rs = gain / loss
        return 100 - (100 / (1 + rs))
    
    @staticmethod
    def create_chart(ticker, period='1mo', indicators=None):
        """Create an interactive chart with technical indicators"""
        try:
            # Ensure ticker is not None or empty
            if not ticker or ticker.strip() == "":
                return "Error: Please enter a valid ticker symbol"
                
            # Clean up ticker symbol
            ticker = ticker.strip().upper()
            
            # Create charts directory if it doesn't exist
            os.makedirs('charts', exist_ok=True)
            
            # Get stock data
            stock = yf.Ticker(ticker)
            data = stock.history(period=period)
            
            if data.empty:
                return f"Error: No data available for ticker {ticker}"
            
            # Create figure with secondary y-axis
            fig = make_subplots(rows=2, cols=1, shared_xaxes=True, 
                              vertical_spacing=0.03, 
                              row_heights=[0.7, 0.3])
            
            # Add candlestick
            fig.add_trace(go.Candlestick(x=data.index,
                                        open=data['Open'],
                                        high=data['High'],
                                        low=data['Low'],
                                        close=data['Close'],
                                        name='OHLC'),
                         row=1, col=1)
            
            # Add indicators if specified
            if indicators:
                if 'SMA20' in indicators:
                    sma20 = TechnicalAnalysis.calculate_sma(data, 20)
                    fig.add_trace(go.Scatter(x=data.index, y=sma20,
                                           name='SMA20', line=dict(color='blue')),
                                row=1, col=1)
                
                if 'SMA50' in indicators:
                    sma50 = TechnicalAnalysis.calculate_sma(data, 50)
                    fig.add_trace(go.Scatter(x=data.index, y=sma50,
                                           name='SMA50', line=dict(color='red')),
                                row=1, col=1)
                
                if 'RSI' in indicators:
                    rsi = TechnicalAnalysis.calculate_rsi(data)
                    fig.add_trace(go.Scatter(x=data.index, y=rsi,
                                           name='RSI', line=dict(color='purple')),
                                row=2, col=1)
                    # Add RSI reference lines
                    fig.add_hline(y=70, line_dash="dash", line_color="red", row=2, col=1)
                    fig.add_hline(y=30, line_dash="dash", line_color="green", row=2, col=1)
            
            # Update layout
            fig.update_layout(
                title=f'{ticker} Stock Price',
                yaxis_title='Stock Price',
                yaxis2_title='RSI',
                xaxis_rangeslider_visible=False
            )
            
            # Save the chart as HTML
            chart_path = os.path.abspath(f'charts/{ticker}_chart.html')
            fig.write_html(chart_path)
            logging.info(f"Chart created for {ticker} at {chart_path}")
            return chart_path
            
        except Exception as e:
            error_msg = f"Error creating chart: {str(e)}"
            logging.error(error_msg)
            return error_msg 