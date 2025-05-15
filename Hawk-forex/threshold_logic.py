class ThresholdLogic:
    def __init__(self, symbol, start_price, current_price, latest_high, latest_low, config):
        self.symbol = symbol
        self.start_price = start_price
        self.current_price = current_price
        self.latest_high = latest_high
        self.latest_low = latest_low
        self.config = config[symbol]

    def calculate(self):
        pip_size = self.config["pip_size"]
        threshold = self.config["threshold"]

        pip_diff = self.current_price - self.start_price
        formatted_pips = round(pip_diff / pip_size, 4)
        thresholds_moved = round(formatted_pips / threshold, 2)

        if thresholds_moved >= 1:
            direction = "up"
        elif thresholds_moved <= -1:
            direction = "down"
        else:
            direction = "neutral"

        return {
            "thresholds_moved": thresholds_moved,
            "formatted_pips": formatted_pips,
            "direction": direction
        }