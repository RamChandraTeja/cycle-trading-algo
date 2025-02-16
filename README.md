# Balancing Wheel Trading Algo

An automated trading bot that rebalances a portfolio using Python and Azure Functions.

## Features

- ✅ **Fetches real-time stock prices** - Utilizes APIs to get the latest stock price data for decision-making.
- ✅ **Calculates portfolio weight adjustments** - Automatically adjusts the weights of assets in the portfolio based on predefined rules or strategies.
- ✅ **Supports Alpaca, Binance, Interactive Brokers APIs** - Integrates with multiple trading platforms to execute trades and fetch data.
- ✅ **Deployable on Azure Functions / AKS** - Can be deployed on Microsoft Azure cloud services for scalability and reliability.
- ✅ **Earnings Prediction** - Incorporates an earnings prediction model to inform trading decisions based on historical and real-time earnings data.
- ✅ **Data Processing** - Processes raw API data into a format suitable for analysis and trading decisions.

## Installation

To get started with the Balancing Wheel Trading Algo, follow these steps:

```bash
# Clone the repository
git clone https://github.com/your-username/balancing-wheel-trading-bot.git

# Navigate to the project directory
cd balancing-wheel-trading-bot

# Install the required dependencies
pip install -r req.txt

# Run the trading script
python trading_script.py