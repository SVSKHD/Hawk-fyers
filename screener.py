from fyers_ops import get_market_start_price, live_prices
from config import symbols
import time



THRESHOLD_PERCENT = 0.25  # Entry signal trigger



# Allow some time for WebSocket to connect and receive first updates
print("[INFO] Waiting for live prices...")
time.sleep(10)

# Fetch start prices at market open
start_prices = {}
for symbol in symbols:
    sp = get_market_start_price(symbol)
    if sp:
        start_prices[symbol] = sp
        print(f"[START] {symbol} = {sp}")
    else:
        print(f"[ERROR] Could not fetch start price for {symbol}")

# Track already signaled entries
already_signaled = {}

print("\n--- Screener Running (Press Ctrl+C to stop) ---\n")

try:
    while True:
        for symbol in symbols:
            current = live_prices.get(symbol)
            start = start_prices.get(symbol)
            if current is not None and start is not None:
                move = ((current - start) / start) * 100
                direction = "BUY" if move > 0 else "SELL"
                if abs(move) >= THRESHOLD_PERCENT:
                    if symbol not in already_signaled:
                        print(f"[ALERT] {symbol} moved {round(move, 2)}% → {direction} signal")
                        already_signaled[symbol] = direction
            else:
                print(f"[WAITING] {symbol} live/start price not available yet")
        time.sleep(2)

except KeyboardInterrupt:
    print("Screener stopped.")
