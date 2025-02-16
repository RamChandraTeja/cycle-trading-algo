import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
from textblob import TextBlob
import requests
import json
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def fetch_stock_data(symbol, api_key, source='NASDAQ'):
    """
    Fetch stock data from NASDAQ or any other open API.
    
    :param symbol: Stock symbol like 'SNOW' for Snowflake
    :param api_key: API key for authentication
    :param source: Data source, default is NASDAQ
    :return: Dictionary containing stock data or None if fetch fails
    """
    if source == 'NASDAQ':
        url = f'https://www.nasdaq.com/api/v1/historical/{symbol}/stocks'
    else:
        # Example for another API, adjust according to the actual API endpoint
        url = f'https://www.tradingview.com/api/v1/symbols/{symbol}/info'
    
    params = {'api_key': api_key}

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        logger.error(f"Failed to fetch data for {symbol}: {e}")
        return None
    
    def analyze_sentiment(text):
    """
    Analyze sentiment of text using TextBlob.
    
    :param text: Text to analyze
    :return: Sentiment polarity (-1 to 1)
    """
    blob = TextBlob(text)
    return blob.sentiment.polarity

def fetch_and_analyze_news(symbol, api_key):
    """
    Fetch news related to the stock and analyze sentiment.
    
    :param symbol: Stock symbol
    :param api_key: API key for news API
    :return: Average sentiment score from news articles
    """
    url = f'https://newsapi.org/v2/everything?q={symbol}&apiKey={api_key}'
    try:
        response = requests.get(url)
        response.raise_for_status()
        news_data = response.json()
        articles = news_data.get('articles', [])
        sentiments = [analyze_sentiment(article['description']) for article in articles if article.get('description')]
        return np.mean(sentiments) if sentiments else 0
    except requests.RequestException as e:
        logger.error(f"Failed to fetch news for {symbol}: {e}")
        return 0
    def prepare_data(stock_data, news_sentiment):
    """
    Prepare data for model training, combining stock metrics with news sentiment.
    
    :param stock_data: Dictionary containing stock data
    :param news_sentiment: Average sentiment from news
    :return: DataFrame with features
    """
    # Example features, adjust based on actual data structure
    features = {
        'Open': stock_data['open'],
        'High': stock_data['high'],
        'Low': stock_data['low'],
        'Close': stock_data['close'],
        'Volume': stock_data['volume'],
        'News_Sentiment': news_sentiment
    }
    return pd.DataFrame([features])

def train_model(X, y):
    """
    Train a Random Forest model for stock prediction.
    
    :param X: Features DataFrame
    :param y: Target variable (e.g., future stock price or movement)
    :return: Trained model
    """
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Evaluate model
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    logger.info(f"Model Performance - MSE: {mse}, R2 Score: {r2}")
    return model

def stock_analysis(symbol, stock_api_key, news_api_key):
    """
    Analyze a given stock, considering financial data, news sentiment, and provide investment advice.
    
    :param symbol: Stock symbol to analyze
    :param stock_api_key: API key for stock data
    :param news_api_key: API key for news data
    :return: Analysis summary
    """
    # Fetch stock data
    stock_data = fetch_stock_data(symbol, stock_api_key)
    if not stock_data:
        return "Failed to fetch stock data."
    # Fetch and analyze news sentiment
    news_sentiment = fetch_and_analyze_news(symbol, news_api_key)
    
    # Prepare data
    features_df = prepare_data(stock_data, news_sentiment)
    
    # Here you would typically have historical data to train the model, 
    # but for this example, we'll simulate with dummy data
    # y = stock_data['future_price'] or some other target metric
    y = np.random.rand(len(features_df))  # Placeholder for actual target
    
    # Train the model (in practice, you'd use historical data)
    model = train_model(features_df, y)
    
    # Predict future movement or price
    prediction = model.predict(features_df)

    # Simplified analysis
    analysis = {
        'Symbol': symbol,
        'Current Price': stock_data['close'],
        'News Sentiment': news_sentiment,
        'Predicted Movement': 'Up' if prediction[0] > stock_data['close'] else 'Down',
        'Investment Recommendation': 'Consider Buying' if prediction[0] > stock_data['close'] and news_sentiment > 0 else 'Hold/Sell'
    }
    
    return analysis