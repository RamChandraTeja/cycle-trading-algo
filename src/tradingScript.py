import pandas as pd
import numpy as np

def process_earnings_data(data):
    """
    Process the fetched earnings data into a DataFrame, handling potential missing values and adding calculated fields.

    :param data: Raw JSON data from the API, expected to be a list of dictionaries
    :return: Processed DataFrame
    """
    # Convert list of dictionaries to DataFrame
    df = pd.DataFrame(data)
    
    # Ensure necessary columns exist, if not, create them with NaN
    required_columns = ['actualEPS', 'estimatedEPS', 'revenue', 'surprise', 'fiscalPeriod']
    for col in required_columns:
        if col not in df.columns:
            df[col] = np.nan
    
    # Calculate Surprise_Ratio
    df['Surprise_Ratio'] = (df['actualEPS'] - df['estimatedEPS']) / df['estimatedEPS']
    df['Surprise_Ratio'] = df['Surprise_Ratio'].replace([np.inf, -np.inf], np.nan)  # Handle division by zero
    
    # Convert revenue to numeric, assuming it might come as string with '$' or ','
    df['Revenue'] = df['revenue'].replace('[\$,]', '', regex=True).astype(float)
    
    # Calculate MarketCap if available from another source or API call (this part is commented out as we don't have this data)
    # df['MarketCap'] = ... # You would need to fetch or calculate this
    
    # Calculate PE_Ratio if possible (this assumes we have 'close' price from another source)
    # df['PE_Ratio'] = df['close'] / df['actualEPS']  # Commented out as 'close' is not provided
    
    # Clean up any unwanted columns or add more processing here
    # For example, you might want to convert 'fiscalPeriod' to datetime if needed
    df['Date'] = pd.to_datetime(df['fiscalPeriod'], format='%Y-%m-%d', errors='coerce')
    
    # Drop rows with all NaN values if any
    df = df.dropna(how='all')
    
    # Sort by date if 'Date' column exists
    if 'Date' in df.columns:
        df = df.sort_values('Date')
    
    # Reset index after sorting/dropping
    df = df.reset_index(drop=True)
    
    return df

# Example usage
# Assuming 'data_from_api' is the result from your fetch_earnings_data function
# data_from_api = fetch_earnings_data('AAPL', 'YOUR_API_TOKEN', 'https://cloud.iexapis.com/stable')
# processed_data = process_earnings_data(data_from_api)