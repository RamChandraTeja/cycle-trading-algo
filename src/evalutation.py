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