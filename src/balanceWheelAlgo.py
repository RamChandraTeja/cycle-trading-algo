from financial_metrics import FinancialMetrics

class BalanceWheelAlgo:
    def __init__(self, symbol):
        self.symbol = symbol
        self.metrics = FinancialMetrics(symbol)

    def generate_signal(self):
        # Use financial metrics in your trading logic
        rsi = self.metrics.rsi().iloc[-1]
        ma20 = self.metrics.moving_average(period=20).iloc[-1]
        current_price = self.metrics.df['Close'].iloc[-1]

        if rsi > 70 and current_price > ma20:
            return "Sell"  # Overbought condition
        elif rsi < 30 and current_price < ma20:
            return "Buy"  # Oversold condition
        return "Hold"