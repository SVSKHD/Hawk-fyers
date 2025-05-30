# hybrid_strategy.py
from datetime import datetime

class HybridStrategy:
    def __init__(self, symbol, start_price, config):
        self.symbol = symbol
        self.start_price = start_price
        self.config = config
        self.entry_price = None
        self.direction = None
        self.trail_price = None
        self.hedge_triggered = False
        self.trail_active = False

    def volatility_passed(self, daily_high, daily_low):
        if self.config.get("filter"):
            pip_range = (daily_high - daily_low) / self.config["pip_size"]
            return pip_range >= 20
        return True

    def check_entry(self, current_price):
        pip_diff = round((current_price - self.start_price) / self.config["pip_size"], 1)
        if pip_diff >= self.config["entry_pips"]:
            self.entry_price = current_price
            self.direction = "BUY"
            return True, "BUY"
        elif pip_diff <= -self.config["entry_pips"]:
            self.entry_price = current_price
            self.direction = "SELL"
            return True, "SELL"
        return False, None

    def evaluate_trade(self, current_price):
        if not self.entry_price:
            return None

        pip_gain = (current_price - self.entry_price) / self.config["pip_size"] if self.direction == "BUY" else (self.entry_price - current_price) / self.config["pip_size"]
        pip_gain = round(pip_gain, 1)

        if not self.hedge_triggered and pip_gain <= -self.config["hedge_trigger"]:
            self.hedge_triggered = True
            return "HEDGE"

        if pip_gain >= self.config["secure_max"]:
            return "CLOSE_SECURE"

        if pip_gain >= self.config["secure_min"] and self.config["trailing"]:
            if not self.trail_active:
                self.trail_price = current_price
                self.trail_active = True
                return None
            else:
                trail_diff = (current_price - self.trail_price) / self.config["pip_size"] if self.direction == "BUY" else (self.trail_price - current_price) / self.config["pip_size"]
                trail_diff = round(trail_diff, 1)
                if trail_diff >= 5:
                    self.trail_price = current_price
                elif trail_diff <= -5:
                    return "CLOSE_TRAIL"

        return None

    def reset(self):
        self.entry_price = None
        self.direction = None
        self.trail_price = None
        self.trail_active = False
        self.hedge_triggered = False
