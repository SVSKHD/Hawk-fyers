from datetime import datetime

class HybridStrategy:
    def __init__(self, symbol, start_price, config):
        self.symbol = symbol
        self.start_price = start_price
        self.config = config
        self.entry_price = None
        self.direction = None
        self.hedge_triggered = False
        self.trail_triggered = False
        self.trail_price = None

    def calculate_pips(self, current_price):
        pip_size = self.config["pip_size"]
        pip_diff = (current_price - self.start_price) / pip_size
        return round(pip_diff, 1)

    def check_entry(self, current_price):
        pips_moved = self.calculate_pips(current_price)
        if not self.entry_price:
            if pips_moved >= self.config["entry_pips"]:
                self.direction = "BUY"
                self.entry_price = current_price
                return True, "BUY"
            elif pips_moved <= -self.config["entry_pips"]:
                self.direction = "SELL"
                self.entry_price = current_price
                return True, "SELL"
        return False, None

    def evaluate_trade(self, current_price):
        if not self.entry_price:
            return None

        pip_size = self.config["pip_size"]
        pip_gain = (current_price - self.entry_price) / pip_size if self.direction == "BUY" else (self.entry_price - current_price) / pip_size
        pip_gain = round(pip_gain, 1)

        # Hedge Trigger
        if not self.hedge_triggered and pip_gain <= -self.config["hedge_trigger_pips"]:
            self.hedge_triggered = True
            return "HEDGE"

        # Trailing Logic
        if pip_gain >= self.config["trailing_step_pips"]:
            if not self.trail_triggered:
                self.trail_price = current_price
                self.trail_triggered = True
            else:
                if self.direction == "BUY":
                    if current_price >= self.trail_price + self.config["trailing_step_pips"] * pip_size:
                        self.trail_price = current_price
                    elif current_price < self.trail_price:
                        return "CLOSE_TRAIL"
                elif self.direction == "SELL":
                    if current_price <= self.trail_price - self.config["trailing_step_pips"] * pip_size:
                        self.trail_price = current_price
                    elif current_price > self.trail_price:
                        return "CLOSE_TRAIL"

        # Secure Exit
        if pip_gain >= self.config["secure_pips"]:
            return "CLOSE_SECURE"

        return None
