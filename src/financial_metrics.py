import pandas as pd
import numpy as np
import yfinance as yf
from datetime import datetime, timedelta

class FinancialMetrics:
    def __init__(self, symbol, start_date=None, end_date=None):
        self.symbol = symbol
        if start_date is None:
            start_date = datetime.now() - timedelta(days=365)  # Default to 1 year
        if end_date is None:
            end_date = datetime.now()
        self.df = self.fetch_data(start_date, end_date)

    def fetch_data(self, start_date, end_date):
        """Fetch historical data using yfinance."""
        ticker = yf.Ticker(self.symbol)
        df = ticker.history(start=start_date, end=end_date)
        return df

    # Technical Indicators
    def moving_average(self, period=20, type_='SMA'):
        """Calculate Simple or Exponential Moving Average."""
        if type_ == 'SMA':
            return self.df['Close'].rolling(window=period).mean()
        elif type_ == 'EMA':
            return self.df['Close'].ewm(span=period, adjust=False).mean()

    def rsi(self, period=14):
        """Calculate Relative Strength Index."""
        delta = self.df['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        return 100 - (100 / (1 + rs))

    def macd(self, fast=12, slow=26, signal=9):
        """Calculate MACD and Signal Line."""
        exp1 = self.df['Close'].ewm(span=fast, adjust=False).mean()
        exp2 = self.df['Close'].ewm(span=slow, adjust=False).mean()
        macd = exp1 - exp2
        signal_line = macd.ewm(span=signal, adjust=False).mean()
        return macd, signal_line

    def bollinger_bands(self, period=20, std_dev=2):
        """Calculate Bollinger Bands."""
        ma = self.df['Close'].rolling(window=period).mean()
        std = self.df['Close'].rolling(window=period).std()
        upper = ma + (std_dev * std)
        lower = ma - (std_dev * std)
        return upper, lower, ma

    # Fundamental Metrics (using yfinance)
    def get_fundamentals(self):
        """Fetch fundamental data like P/E, P/B, Dividend Yield, etc."""
        ticker = yf.Ticker(self.symbol)
        info = ticker.info
        fundamentals = {
            'pe_ratio': info.get('trailingPE', None),
            'pb_ratio': info.get('priceToBook', None),
            'dividend_yield': info.get('dividendYield', None) * 100,  # Convert to percentage
            'eps': info.get('trailingEps', None),
            'debt_to_equity': info.get('debtToEquity', None),
            'roe': info.get('returnOnEquity', None) * 100  # Convert to percentage
        }
        return fundamentals

    # Risk Management Metrics
    def value_at_risk(self, confidence=0.95, period=1):
        """Calculate Value at Risk (VaR) for portfolio or single asset."""
        returns = self.df['Close'].pct_change().dropna()
        var = returns.quantile(1 - confidence)
        return var * self.df['Close'].iloc[-1]

    def sharpe_ratio(self, risk_free_rate=0.01, period=252):
        """Calculate Sharpe Ratio (annualized)."""
        returns = self.df['Close'].pct_change().dropna()
        excess_return = returns.mean() * period - risk_free_rate
        volatility = returns.std() * np.sqrt(period)
        return excess_return / volatility

    def max_drawdown(self):
        """Calculate Maximum Drawdown."""
        roll_max = self.df['Close'].cummax()
        drawdown = self.df['Close'] / roll_max - 1.0
        return drawdown.min()

    # Market Sentiment (Placeholder for Twitter/X or news API)
    def market_sentiment(self):
        """Placeholder for sentiment analysis (e.g., Twitter/X, news)."""
        # This would require an API like Twitter/X or news scraper
        print("Market sentiment analysis requires external API integration (e.g., Twitter/X, news).")
        return None

    # Custom Metrics
    def asset_correlation(self, other_symbol):
        """Calculate correlation between two assets."""
        df1 = self.df['Close']
        df2 = FinancialMetrics(other_symbol).df['Close']
        combined = pd.concat([df1, df2], axis=1, join='inner').dropna()
        return combined.corr().iloc[0, 1]

    def cycle_length(self, period=20):
        """Detect cycle length using autocorrelation or Fourier analysis."""
        # Simple autocorrelation for cycle detection
        autocorr = pd.Series.autocorr(self.df['Close'].pct_change().dropna(), lag=period)
        return autocorr

# Example usage
if __name__ == "__main__":
    metrics = FinancialMetrics("AAPL")
    print("Moving Average (SMA, 20-day):", metrics.moving_average(period=20).tail())
    print("RSI (14-day):", metrics.rsi().tail())
    print("Fundamentals:", metrics.get_fundamentals())
    print("Value at Risk (95% confidence):", metrics.value_at_risk())
    print("Sharpe Ratio:", metrics.sharpe_ratio())