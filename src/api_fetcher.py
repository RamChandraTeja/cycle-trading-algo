import requests
import logging

# Set up logging for better error tracking
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def fetch_earnings_data(symbol, token, api_url, period="1y"):
    """
    Fetch earnings data for a given stock symbol from the specified API.

    :param symbol: Stock symbol (e.g., 'AAPL')
    :param token: API token for authentication
    :param api_url: URL of the API endpoint
    :param period: Time period for earnings data, default is '1y' for one year
    :return: JSON response or None if request fails
    """
    # Construct the URL with the period parameter
    url = f"{api_url}/stock/{symbol}/earnings/{period}?token={token}"
    
    try:
        # Make the API request
        response = requests.get(url, timeout=10)  # Added timeout for request
        
        # Check if the request was successful
        if response.status_code == 200:
            # Log success and return data
            logging.info(f"Successfully fetched earnings data for {symbol}")
            return response.json()
        else:
            # Log the error with status code
            logging.error(f"Failed to fetch data for {symbol}. Status code: {response.status_code}")
            return None
    
    except requests.RequestException as e:
        # Handle network errors or timeouts
        logging.error(f"Request failed for {symbol}: {str(e)}")
        return None

# Example usage
# data = fetch_earnings_data('AAPL', 'YOUR_API_TOKEN', 'https://cloud.iexapis.com/stable')