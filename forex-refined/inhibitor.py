class TradeInhibitor:
    def __init__(self):
        self.active_trades = {}

    def is_allowed(self, symbol):
        return not self.active_trades.get(symbol, False)

    def set_active(self, symbol, state=True):
        self.active_trades[symbol] = state

    def reset(self):
        self.active_trades.clear()
