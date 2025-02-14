# src/predict.py
import pandas as pd
from sklearn.externals import joblib

# Load the trained model
model = joblib.load('../models/saved_model.pkl')

# Load new data for prediction
new_data = pd.read_csv('../data/processed/new_data.csv')

# Make predictions
predictions = model.predict(new_data)

# Output predictions
print(predictions)
