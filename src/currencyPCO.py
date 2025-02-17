import pandas as pd
from sklearn.linear_model import LinearRegression
from datetime import datetime, timedelta
import currencyapi

# Initialize CurrencyAPI client with your API key
api_key = "YOUR_API_KEY_HERE"
client = currencyapi.Client(api_key)

def fetch_currency_data():
    # Fetch today's INR/USD rate
    response = client.latest(codes=['INR'], base_currency='USD')
    return response['data']['INR']['value']

def get_historical_data(days=30):
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    
    dates = [(start_date + timedelta(days=i)).strftime('%Y-%m-%d') for i in range(days)]
    data = []
    
    for date in dates:
        try:
            response = client.historical(codes=['INR'], date=date, base_currency='USD')
            rate = response['data']['INR']['value']
            data.append({
                'Date': date,
                'INR/USD': rate,
                'GDP_Growth': 6.5,  # Placeholder, replace with actual or forecasted data
                'Inflation_Diff': 2.0,  # Placeholder
                'Interest_Rate_Diff': 2.1,  # Placeholder
                'Oil_Price': 85,  # Placeholder, should be actual Brent Crude price
                'Trade_Balance': -13,  # Placeholder, should be actual trade balance
                'USD_Index': 107  # Placeholder, should be actual DXY
            })
        except Exception as e:
            print(f"Error fetching data for {date}: {e}")
    
    return pd.DataFrame(data)

def train_and_predict():
    df = get_historical_data()
    
    # Features and target
    X = df[['GDP_Growth', 'Inflation_Diff', 'Interest_Rate_Diff', 'Oil_Price', 'Trade_Balance', 'USD_Index']]
    y = df['INR/USD']
    
    # Train model
    model = LinearRegression()
    model.fit(X, y)
    
    # Predict today's rate
    today_data = pd.DataFrame([{
        'GDP_Growth': 6.5,  # Current or forecasted
        'Inflation_Diff': 2.0,
        'Interest_Rate_Diff': 2.1,
        'Oil_Price': 85,  # Current Brent Crude price
        'Trade_Balance': -13,  # Current trade balance
        'USD_Index': 107  # Current DXY
    }])
    
    prediction = model.predict(today_data)
    actual_rate = fetch_currency_data()
    
    print("Predicted INR/USD:", prediction[0])
    print("Actual INR/USD:", actual_rate)
    print("Error:", abs(prediction[0] - actual_rate))

    # Coefficients
    print("Coefficients:", model.coef_)
    print("Intercept:", model.intercept_)

if __name__ == "__main__":
    train_and_predict()