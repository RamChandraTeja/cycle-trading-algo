import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from api_fetcher import fetch_earnings_data
from data_processor import process_earnings_data

def earnings_prediction_model(symbol, token, api_url, period="1y"):
    """
    Fetch, process, and predict earnings for a given stock symbol.

    :param symbol: Stock symbol (e.g., 'AAPL')
    :param token: API token for authentication
    :param api_url: URL of the API endpoint
    :param period: Time period for earnings data, default is '1y' for one year
    :return: Trained model or None if data fetching or processing fails
    """
    # Fetch data
    raw_data = fetch_earnings_data(symbol, token, api_url, period)
    
    if raw_data is None:
        print(f"No data available for {symbol}")
        return None
    
    # Process data
    data = process_earnings_data(raw_data)
    
    # Check if necessary columns exist in the processed data
    features = ['Revenue', 'Surprise_Ratio']  # Adjusted based on available data from process_earnings_data
    if not all(feature in data.columns for feature in features):
        print(f"Required features {features} are not all present in the data for {symbol}")
        return None
    
    # Prepare features and target
    # Here we use 'actualEPS' as our target since 'EPS' might not be in the processed data
    X = data[features]
    y = data['actualEPS']
    
    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Train the model
    model = LinearRegression()
    model.fit(X_train, y_train)
    
    # Make predictions
    y_pred = model.predict(X_test)
    
    # Evaluate the model
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    
    print(f"Mean Squared Error: {mse}")
    print(f"R^2 Score: {r2}")
    
    return model

# Example usage
# model = earnings_prediction_model('AAPL', 'YOUR_API_TOKEN', 'https://cloud.iexapis.com/stable')