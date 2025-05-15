import time
from mt5_ops import MT5Ops
from threshold_logic import ThresholdLogic
from config import symbol_config
from datetime import datetime

def main(symbols):
    mt5_instances = {}
    start_prices = {}
    latest_highs = {}
    latest_lows = {}

    # Initialize MT5 instances and get start prices for all symbols
    for symbol in symbols:
        mt5 = MT5Ops(symbol)
        start_price = mt5.get_start_price()
        mt5_instances[symbol] = mt5
        start_prices[symbol] = start_price
        latest_highs[symbol] = start_price
        latest_lows[symbol] = start_price
        print(f"[{datetime.now()}] {symbol} Start Price: {start_price}")

    print("\n--- Bot Started ---\n")

    try:
        while True:
            for symbol in symbols:
                mt5 = mt5_instances[symbol]
                current_price = mt5.get_current_price()

                # Update high/low
                latest_highs[symbol] = max(latest_highs[symbol], current_price)
                latest_lows[symbol] = min(latest_lows[symbol], current_price)

                # Calculate threshold logic
                threshold_data = ThresholdLogic(
                    symbol=symbol,
                    start_price=start_prices[symbol],
                    current_price=current_price,
                    latest_high=latest_highs[symbol],
                    latest_low=latest_lows[symbol],
                    config=symbol_config
                ).calculate()

                print(f"[{datetime.now()}] {symbol}: {threshold_data}")

            time.sleep(0.2)  # 200 milliseconds loop
    except KeyboardInterrupt:
        print("\nBot stopped by user.")
    finally:
        for mt5 in mt5_instances.values():
            mt5.shutdown()

if __name__ == "__main__":
    symbols = ["EURUSD", "GBPUSD"]
    main(symbols)