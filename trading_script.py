import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

# Define portfolio mapping with shares and purchase price
portfolio = {
    "AAPL": {"shares": 50, "purchase_price": 150.00},
    "TSLA": {"shares": 30, "purchase_price": 700.00},
    "MSFT": {"shares": 20, "purchase_price": 250.00}
}

def get_prices(symbols, period="1d"):
    """
    Retrieve the latest closing prices for given stock symbols.

    :param symbols: List of stock symbols
    :param period: Time period for historical data, default is '1d'
    :return: Dictionary with stock symbols as keys and their latest prices as values
    """
    prices = {}
    for symbol in symbols:
        try:
            data = yf.Ticker(symbol).history(period=period)
            if not data.empty:
                prices[symbol] = data["Close"].iloc[-1]
            else:
                prices[symbol] = None  # or handle missing data as needed
        except Exception as e:
            print(f"Error fetching data for {symbol}: {e}")
            prices[symbol] = None
    return prices

def calculate_portfolio_value(prices, portfolio):
    """
    Calculate the current value of the portfolio.

    :param prices: Dictionary of current stock prices
    :param portfolio: Dictionary containing shares and purchase price for each stock
    :return: Total portfolio value, gains, and detailed breakdown
    """
    total_value = 0
    gains = 0
    breakdown = []
    
    for symbol, details in portfolio.items():
        if prices[symbol] is not None:
            current_value = details['shares'] * prices[symbol]
            purchase_value = details['shares'] * details['purchase_price']
            gain = current_value - purchase_value
            gains += gain
            total_value += current_value
            breakdown.append({
                'symbol': symbol,
                'current_price': prices[symbol],
                'shares': details['shares'],
                'current_value': current_value,
                'purchase_value': purchase_value,
                'gain': gain
            })
        else:
            breakdown.append({
                'symbol': symbol,
                'current_price': "N/A",
                'shares': details['shares'],
                'current_value': "N/A",
                'purchase_value': details['shares'] * details['purchase_price'],
                'gain': "N/A"
            })
    
    return total_value, gains, breakdown

if __name__ == "__main__":
    symbols = list(portfolio.keys())
    current_prices = get_prices(symbols, period="1d")  # Fetching daily closing prices
    total_value, gains, portfolio_breakdown = calculate_portfolio_value(current_prices, portfolio)

    print("Current Prices:", current_prices)
    print(f"\nTotal Portfolio Value: ${total_value:.2f}")
    print(f"Total Gains: ${gains:.2f}")
    
    # Display detailed breakdown
    for entry in portfolio_breakdown:
        if entry['current_price'] != "N/A":
            print(f"{entry['symbol']}: Shares: {entry['shares']}, Current Price: ${entry['current_price']:.2f}, "
                  f"Current Value: ${entry['current_value']:.2f}, Purchase Value: ${entry['purchase_value']:.2f}, "
                  f"Gain: ${entry['gain']:.2f}")
        else:
            print(f"{entry['symbol']}: Shares: {entry['shares']}, Price Data Unavailable, "
                  f"Purchase Value: ${entry['purchase_value']:.2f}")