import pandas as pd

def process_earnings_data(data):
    """
    Process the fetched earnings data into a DataFrame.

    :param data: Raw JSON data from the API
    :return: Processed DataFrame
    """
    df = pd.DataFrame(data)
    # Assuming we need 'EPS', 'Revenue', 'MarketCap', 'PE_Ratio', 'Surprise_Ratio'
    # You might need to adjust this based on the actual data structure from the API
    df['Surprise_Ratio'] = (df['actualEPS'] - df['estimatedEPS']) / df['estimatedEPS']
    # Here you would add more data cleaning or feature engineering as needed
    return df

# Example usage
# processed_data = process_earnings_data(data_from_api)