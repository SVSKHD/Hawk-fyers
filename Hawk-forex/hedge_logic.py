class HedgeLogic:
    def __init__(self, symbol, entry_price, current_price, direction, config):
        self.symbol = symbol
        self.entry_price = entry_price
        self.current_price = current_price
        self.direction = direction
        self.config = config[symbol]

    def should_hedge(self):
        pip_size = self.config["pip_size"]
        secure_min = self.config["secure_min"]

        if self.direction == "long":
            pips = (self.current_price - self.entry_price) / pip_size
        else:
            pips = (self.entry_price - self.current_price) / pip_size

        return pips <= -secure_min