import yfinance as yf
import pandas as pd

# Define portfolio mapping
portfolio = {"AAPL": 50, "TSLA": 30, "MSFT": 20}

def get_prices():
    prices = {s: yf.Ticker(s).history(period="1d")["Close"].iloc[-1] for s in portfolio}
    return prices

if __name__ == "__main__":
    current_prices = get_prices()
    print("Current Prices:", current_prices)
