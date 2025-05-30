# executor.py
import time
import os
from datetime import datetime
from mt5_ops_price import MT5Ops
from hybrid_strategy import HybridStrategy
from config import strategy_config


class Executor:
    def __init__(self):
        self.mt5ops = MT5Ops()
        self.symbols = list(strategy_config.keys())
        self.strategies = {}
        self.start_prices = {}
        self.active_hedge = {symbol: False for symbol in self.symbols}
        self.initialize_strategies()

    def initialize_strategies(self):
        for symbol in self.symbols:
            start_price = self.mt5ops.get_start_price(symbol)
            self.start_prices[symbol] = start_price
            self.strategies[symbol] = HybridStrategy(symbol, start_price, strategy_config[symbol])
            print(f"[START] {symbol} = {start_price}")

    def store_trade_log(self, symbol, direction, ticket, entry_price, lot):
        today = datetime.now().strftime("%Y-%m-%d")
        os.makedirs("logs", exist_ok=True)
        with open(f"logs/{today}_trades.txt", "a") as f:
            f.write(f"{symbol}|{direction}|{ticket}|{entry_price}|{lot}|{datetime.now().strftime('%H:%M:%S')}\n")

    def find_trade(self, symbol):
        today = datetime.now().strftime("%Y-%m-%d")
        file_path = f"logs/{today}_trades.txt"
        if not os.path.exists(file_path):
            return None
        with open(file_path, "r") as f:
            for line in reversed(f.readlines()):
                parts = line.strip().split("|")
                if parts[0] == symbol:
                    return {
                        "symbol": parts[0],
                        "direction": parts[1],
                        "ticket": int(parts[2]),
                        "entry_price": float(parts[3]),
                        "lot": float(parts[4])
                    }
        return None

    def run(self):
        print("[RUNNING] Executor live polling...")
        try:
            while True:
                for symbol in self.symbols:
                    price = self.mt5ops.get_current_price(symbol)
                    strategy = self.strategies[symbol]

                    if not strategy.entry_price:
                        triggered, direction = strategy.check_entry(price)
                        if triggered:
                            print(f"[ENTRY] {symbol} - {direction} @ {price}")
                            # Placeholder for placing trade
                            ticket = 100000  # dummy ticket for testing
                            self.store_trade_log(symbol, direction, ticket, price, 0.5)
                            self.active_hedge[symbol] = True
                    else:
                        action = strategy.evaluate_trade(price)
                        if action in ["CLOSE_SECURE", "CLOSE_TRAIL"]:
                            trade = self.find_trade(symbol)
                            if trade:
                                print(f"[EXIT] {symbol} - {action} @ {price}")
                                self.active_hedge[symbol] = False
                                strategy.reset()
                        elif action == "HEDGE" and self.active_hedge[symbol]:
                            print(f"[HEDGE] {symbol} - reverse entry @ {price}")
                            self.active_hedge[symbol] = False

                time.sleep(1)
        except KeyboardInterrupt:
            print("[STOPPED] Manually interrupted")
        finally:
            self.mt5ops.shutdown()
