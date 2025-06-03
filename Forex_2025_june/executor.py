
import time
import os
from datetime import datetime
from mt5_ops_price import MT5Ops
from hybrid_strategy import HybridStrategy
from config import strategy_config
from trade_ops import TradeExecutor


class Executor:
    def __init__(self):
        self.mt5ops = MT5Ops()
        self.symbols = list(strategy_config.keys())
        self.strategies = {}
        self.start_prices = {}
        self.symbol_state = {symbol: "IDLE" for symbol in self.symbols}
        self.initialize_strategies()
        self.trade_executor = TradeExecutor()

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
                    state = self.symbol_state[symbol]

                    if state == "IDLE":
                        triggered, direction = strategy.check_entry(price)
                        if triggered:
                            print(f"[ENTRY] {symbol} - {direction} @ {price}")
                            result = self.trade_executor.place_trade(symbol, direction, lot=0.5)
                            if result.retcode == 10009:
                                ticket = result.order
                                self.store_trade_log(symbol, direction, ticket, price, 0.5)
                                self.symbol_state[symbol] = "OPEN"
                            else:
                                print(f"[ERROR] Trade failed for {symbol}: {result.comment}")

                    elif state in ["OPEN", "HEDGED"]:
                        action = strategy.evaluate_trade(price)
                        if action in ["CLOSE_SECURE", "CLOSE_TRAIL"]:
                            trade = self.find_trade(symbol)
                            if trade:
                                print(f"[EXIT] {symbol} - {action} @ {price}")
                                result = self.trade_executor.close_trade(trade["ticket"], symbol)
                                if result.retcode == 10009:
                                    print(f"[CLOSED] {symbol} ticket {trade['ticket']} successfully.")
                                else:
                                    print(f"[ERROR] Failed to close {symbol} ticket {trade['ticket']}: {result.comment}")
                                self.symbol_state[symbol] = "IDLE"
                                strategy.reset()

                        elif action == "HEDGE" and state == "OPEN":
                            print(f"[HEDGE] {symbol} - reverse entry @ {price}")
                            result = self.trade_executor.place_trade(symbol, "SELL" if strategy.direction == "BUY" else "BUY", lot=1.0)
                            if result.retcode == 10009:
                                print(f"[HEDGED] {symbol} - hedge placed ticket {result.order}")
                                self.symbol_state[symbol] = "HEDGED"
                            else:
                                print(f"[ERROR] Failed to hedge {symbol}: {result.comment}")

                time.sleep(1)
        except KeyboardInterrupt:
            print("[STOPPED] Manually interrupted")
        finally:
            self.mt5ops.shutdown()
