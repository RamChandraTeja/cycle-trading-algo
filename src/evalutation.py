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