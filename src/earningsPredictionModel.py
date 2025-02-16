import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.exceptions import NotFittedError
from typing import Optional, Dict, Any
import logging

from api_fetcher import fetch_earnings_data
from data_processor import process_earnings_data

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def validate_params(symbol: str, token: str, api_url: str, period: str = "1y") -> None:
    """
    Validate input parameters for the earnings prediction model.

    :param symbol: Stock symbol (e.g., 'AAPL')
    :param token: API token for authentication
    :param api_url: URL of the API endpoint
    :param period: Time period for earnings data, default is '1y' for one year
    :raises ValueError: If any parameter is invalid
    """
    if not isinstance(symbol, str) or not symbol:
        raise ValueError("Symbol must be a non-empty string.")
    if not isinstance(token, str) or not token:
        raise ValueError("Token must be a non-empty string.")
    if not isinstance(api_url, str) or not api_url:
        raise ValueError("API URL must be a non-empty string.")
    if period not in ["1d", "1m", "3m", "6m", "1y", "2y", "5y", "10y", "ytd", "max"]:
        raise ValueError("Invalid period. Choose from '1d', '1m', '3m', '6m', '1y', '2y', '5y', '10y', 'ytd', 'max'.")

def earnings_prediction_model(symbol: str, token: str, api_url: str, period: str = "1y") -> Optional[LinearRegression]:
    """
    Fetch, process, and predict earnings for a given stock symbol.

    :param symbol: Stock symbol (e.g., 'AAPL')
    :param token: API token for authentication
    :param api_url: URL of the API endpoint
    :param period: Time period for earnings data, default is '1y' for one year
    :return: Trained LinearRegression model or None if data fetching or processing fails
    """
    try:
        # Validate parameters
        validate_params(symbol, token, api_url, period)
        
        # Fetch data
        logger.info(f"Fetching earnings data for {symbol}")
        raw_data = fetch_earnings_data(symbol, token, api_url, period)
        
        if raw_data is None:
            logger.warning(f"No data available for {symbol}")
            return None
        
        # Process data
        logger.info(f"Processing data for {symbol}")
        data = process_earnings_data(raw_data)
        
        # Check if necessary columns exist in the processed data
        features = ['Revenue', 'Surprise_Ratio']
        if not all(feature in data.columns for feature in features):
            logger.error(f"Required features {features} are not all present in the data for {symbol}")
            return None
        
        # Prepare features and target
        X = data[features]
        y = data['actualEPS']
        
        # Check for sufficient data
        if len(X) < 10:  # Example threshold, adjust based on your needs
            logger.warning(f"Insufficient data for {symbol} to train the model. Only {len(X)} samples available.")
            return None
        
        # Split the data into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Train the model
        logger.info(f"Training model for {symbol}")
        model = LinearRegression()
        model.fit(X_train, y_train)
        
        # Make predictions
        y_pred = model.predict(X_test)
        
        # Evaluate the model
        mse = mean_squared_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        
        logger.info(f"Model evaluation for {symbol}:")
        logger.info(f"Mean Squared Error: {mse}")
        logger.info(f"R^2 Score: {r2}")
        
        # Check if the model is properly fitted
        try:
            model.predict(X_test)
        except NotFittedError:
            logger.error("Model was not fitted properly.")
            return None
        
        return model
    
    except Exception as e:
        logger.error(f"An error occurred while processing {symbol}: {str(e)}")
        return None

# Example usage
if __name__ == "__main__":
    symbol = 'AAPL'
    token = 'YOUR_API_TOKEN'
    api_url = 'https://cloud.iexapis.com/stable'
    model = earnings_prediction_model(symbol, token, api_url)
    
    if model:
        logger.info(f"Model successfully created for {symbol}")
    else:
        logger.info(f"Failed to create model for {symbol}")