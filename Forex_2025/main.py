import time
import os
from datetime import datetime
from mt5_ops import MT5Ops
from hybrid_strategy_logic import HybridStrategy
from strategy_config import strategy_config
from trade_executor import TradeExecutor

# Setup
symbols = ["EURUSD", "GBPUSD", "USDJPY", "XAGUSD", "XAUUSD"]
mt5ops = MT5Ops()
executor = TradeExecutor()

# Utility functions to handle trade logs
def store_trade_log(symbol, direction, ticket, entry_price, lot):
    today = datetime.now().strftime("%Y-%m-%d")
    os.makedirs("logs", exist_ok=True)
    log_file = f"logs/{today}_trades.txt"
    with open(log_file, "a") as f:
        f.write(f"{symbol}|{direction}|{ticket}|{entry_price}|{lot}|{datetime.now().strftime('%H:%M:%S')}\n")

def find_trade_from_log(symbol):
    today = datetime.now().strftime("%Y-%m-%d")
    log_file = f"logs/{today}_trades.txt"
    if not os.path.exists(log_file):
        return None
    with open(log_file, "r") as f:
        lines = f.readlines()
    for line in reversed(lines):
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

# Initialize strategy per symbol
start_prices = {}
strategies = {}
active_hedge = {symbol: False for symbol in symbols}
for symbol in symbols:
    start_price = mt5ops.get_start_price(symbol)
    start_prices[symbol] = start_price
    strategies[symbol] = HybridStrategy(symbol, start_price, strategy_config[symbol])
    print(f"[START] {symbol} = {start_price}")

print("[RUNNING] Polling live prices every second...")

try:
    while True:
        for symbol in symbols:
            current_price = mt5ops.get_current_price(symbol)
            strategy = strategies[symbol]

            if not strategy.entry_price:
                triggered, direction = strategy.check_entry(current_price)
                if triggered:
                    result = executor.place_trade(symbol, direction)
                    if result.retcode == mt5.TRADE_RETCODE_DONE:
                        store_trade_log(symbol, direction, result.order, current_price, 0.5)
                        active_hedge[symbol] = True  # Enable hedge only after a trade is placed
            else:
                action = strategy.evaluate_trade(current_price)
                if action in ["CLOSE_SECURE", "CLOSE_TRAIL"]:
                    trade = find_trade_from_log(symbol)
                    if trade:
                        executor.close_trade(trade["ticket"], symbol)
                        active_hedge[symbol] = False  # Reset hedge flag after trade close
                elif action == "HEDGE" and active_hedge[symbol]:
                    opposite = "SELL" if strategy.direction == "BUY" else "BUY"
                    result = executor.place_trade(symbol, opposite, lot=1.0)
                    if result.retcode == mt5.TRADE_RETCODE_DONE:
                        store_trade_log(symbol, opposite, result.order, current_price, 1.0)
                        active_hedge[symbol] = False  # Only allow one hedge per trade

        time.sleep(1)

except KeyboardInterrupt:
    print("[STOPPED] Polling interrupted.")
finally:
    mt5ops.shutdown()
    executor.shutdown()
