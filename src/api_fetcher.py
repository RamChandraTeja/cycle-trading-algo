import requests

def fetch_earnings_data(symbol, token, api_url):
    """
    Fetch earnings data for a given stock symbol from the specified API.

    :param symbol: Stock symbol (e.g., 'AAPL')
    :param token: API token for authentication
    :param api_url: URL of the API endpoint
    :return: JSON response or None if request fails
    """
    url = f"{api_url}/stock/{symbol}/earnings/1y?token={token}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch data for {symbol}. Status code: {response.status_code}")
        return None

# Example usage
# data = fetch_earnings_data('AAPL', 'YOUR_API_TOKEN', 'https://cloud.iexapis.com/stable')