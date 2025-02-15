
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from api_fetcher import fetch_earnings_data
from data_processor import process_earnings_data

def earnings_prediction_model(symbol, token, api_url):
    # Fetch data
    raw_data = fetch_earnings_data(symbol, token, api_url)
    
    if raw_data is None:
        print(f"No data available for {symbol}")
        return None
    
    # Process data
    data = process_earnings_data(raw_data)
    
    # Your existing model code here
    # ...

def earnings_prediction_model(data):
    # Assuming data contains columns like 'EPS', 'Revenue', 'MarketCap', 'PE_Ratio', 'Surprise_Ratio'
    # Where 'Surprise_Ratio' is (Actual EPS - Expected EPS) / Expected EPS from previous periods
    
    # Prepare features and target
    features = ['Revenue', 'MarketCap', 'PE_Ratio', 'Surprise_Ratio']
    X = data[features]
    y = data['EPS']
    
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

# Usage would involve loading data from NASDAQ earnings calendar and then calling this function