# main.py
import time
from datetime import datetime
from mt5_ops import MT5Ops
from trade_ops import TradeOps
from notifier import Notifier
from executor import Executor
from inhibitor import TradeInhibitor
from config import config

symbols = list(config.keys())
mt5 = MT5Ops()
trader = TradeOps()
notifier = Notifier("YOUR_DISCORD_WEBHOOK")
inhibitor = TradeInhibitor()
executors = {}

for symbol in symbols:
    executors[symbol] = Executor(
        symbol=symbol,
        config=config,
        mt5_ops=mt5,
        webhook_url="YOUR_DISCORD_WEBHOOK"
    )

last_refresh_day = None

for executor in executors.values():
    executor.initialize_day()
last_refresh_day = datetime.now().day

print("Bot running...")

while True:
    now = datetime.now()
    if now.hour == 0 and now.minute == 5 and now.day != last_refresh_day:
        for exec_obj in executors.values():
            exec_obj.initialize_day()
        last_refresh_day = now.day
        notifier.send(f"[STATUS] Start price refreshed for all symbols at {now.strftime('%H:%M')} | Logs active.", level="INTERVAL")

    for symbol in symbols:
        if inhibitor.is_allowed(symbol):
            executors[symbol].monitor_market()

    time.sleep(1)
