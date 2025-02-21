# Financial Metrics Documentation

This document outlines the financial metrics implemented in the `financial_metrics.py` file for the cycle trading algorithm. These metrics enhance the trading strategy by providing technical, fundamental, risk, and sentiment analysis.

## 1. Technical Indicators
- **Moving Average (SMA/EMA)**: Measures the average price over a specific period to smooth out price data. Used for trend identification.
  - Source: Historical price data (e.g., `yfinance`).
- **Relative Strength Index (RSI)**: Measures the speed and change of price movements to identify overbought (>70) or oversold (<30) conditions.
  - Source: Historical price data.
- **MACD**: Identifies changes in the strength, direction, momentum, and duration of a trend using moving averages.
  - Source: Historical price data.
- **Bollinger Bands**: Measures volatility and identifies potential reversal points using a moving average and standard deviation bands.
  - Source: Historical price data.
- **Stochastic Oscillator**: Compares a closing price to its price range over a period to identify potential reversals.
  - Source: Historical price data (can be added to `financial_metrics.py`).
- **On-Balance Volume (OBV)**: Uses volume flow to predict price movements.
  - Source: Historical price and volume data.
- **Average True Range (ATR)**: Measures market volatility.
  - Source: Historical price data.

## 2. Fundamental Metrics
- **Price-to-Earnings (P/E) Ratio**: Indicates how much investors are willing to pay per dollar of earnings. Higher values may suggest overvaluation.
  - Source: `yfinance.Ticker.info`.
- **Price-to-Book (P/B) Ratio**: Compares market value to book value, useful for value investing.
  - Source: `yfinance.Ticker.info`.
- **Dividend Yield**: Percentage of a company's stock price paid out as dividends annually.
  - Source: `yfinance.Ticker.info`.
- **Earnings Per Share (EPS)**: Profit allocated to each share, indicating profitability.
  - Source: `yfinance.Ticker.info`.
- **Debt-to-Equity Ratio**: Measures financial leverage and risk.
  - Source: `yfinance.Ticker.info`.
- **Return on Equity (ROE)**: Measures profitability relative to shareholders' equity.
  - Source: `yfinance.Ticker.info`.

## 3. Risk Management Metrics
- **Value at Risk (VaR)**: Estimates the potential loss in value of a portfolio over a defined period with a given confidence level.
  - Source: Historical returns data.
- **Sharpe Ratio**: Measures risk-adjusted return, comparing excess return to volatility.
  - Source: Historical returns data.
- **Sortino Ratio**: Similar to Sharpe but only considers downside risk.
  - Source: Historical returns data (can be added to `financial_metrics.py`).
- **Maximum Drawdown**: Measures the largest peak-to-trough decline in portfolio value.
  - Source: Historical price data.
- **Beta**: Measures an asset's volatility relative to the market.
  - Source: `yfinance.Ticker.info` or historical data correlation.

## 4. Market Sentiment Metrics
- **Put/Call Ratio**: Indicates market sentiment using options data (bullish or bearish).
  - Source: Options data APIs (e.g., Alpha Vantage, Quandl).
- **VIX (Volatility Index)**: Measures market fear and expected volatility.
  - Source: CBOE data or financial APIs.
- **Social Media Sentiment**: Analyzes sentiment from platforms like Twitter/X to gauge public perception.
  - Source: Twitter/X API (e.g., `tweepy`, `snscrape`).

## 5. Custom Metrics
- **Asset Correlation**: Measures the relationship between two assets' price movements.
  - Source: Historical price data.
- **Cycle Length Detection**: Identifies periodic patterns in price data using autocorrelation or Fourier analysis.
  - Source: Historical price data.

## Data Sources
- **Yahoo Finance (`yfinance`)**: Provides stock prices, fundamentals, and technical data.
- **Alpha Vantage**: Offers real-time and historical data, including technical indicators and fundamentals.
- **Quandl**: Provides macroeconomic and financial data.
- **Twitter/X API**: For sentiment analysis (requires authentication and rate limits).
- **Custom Scraping**: For news or alternative data sources (e.g., web scraping libraries).

## Implementation Notes
- All metrics are implemented in `financial_metrics.py` and can be integrated into `balanceWheelAlgo.py`, `data_processor.py`, or `tradingScript.py`.
- Some metrics (e.g., sentiment analysis) require external API keys and additional libraries (e.g., `tweepy`, `requests`).
- Ensure you handle missing data and errors appropriately in production.