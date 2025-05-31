
from executor import Executor
import time
from datetime import datetime, timedelta

def get_utc3_date():
    return (datetime.utcnow() + timedelta(hours=3)).date()

bot = Executor()
last_refreshed = get_utc3_date()

print("[INFO] Bot started. Initial strategies loaded.")

while True:
    try:
        current_utc3 = datetime.utcnow() + timedelta(hours=3)
        current_date = current_utc3.date()

        # Refresh at 00:05 UTC+3
        if current_date != last_refreshed and current_utc3.hour == 0 and current_utc3.minute >= 5:
            print(f"[INFO] Refreshing strategies at {current_utc3.strftime('%Y-%m-%d %H:%M:%S')} UTC+3")
            bot.initialize_strategies()
            last_refreshed = current_date

        bot.run()
        time.sleep(1)
    except KeyboardInterrupt:
        print("[STOPPED] Bot manually interrupted.")
        break
