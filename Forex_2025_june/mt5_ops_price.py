import MetaTrader5 as mt5
import pytz
from datetime import datetime, timedelta

class MT5Ops:
    def __init__(self):
        if not mt5.initialize():
            raise RuntimeError(f"MT5 Initialization failed: {mt5.last_error()}")

    def get_start_price(symbol):
        now = datetime.datetime.utcnow() + datetime.timedelta(hours=3)  # UTC+3
        if now.weekday() == 0:  # Monday
            last_trading_day = now - datetime.timedelta(days=3)  # Friday
        else:
            last_trading_day = now

        # Fetch last known candle for that day (e.g. last 5-min candle)
        from_time = last_trading_day.replace(hour=0, minute=0, second=0)
        to_time = last_trading_day.replace(hour=23, minute=58, second=0)

        rates = mt5.copy_rates_range(symbol, mt5.TIMEFRAME_M5, from_time, to_time)
        if rates is not None and len(rates) > 0:
            return rates[-1]["close"]
        else:
            raise Exception(f"Start price not available for {symbol}")

    def get_current_price(self, symbol):
        tick = mt5.symbol_info_tick(symbol)
        if tick is None:
            raise ValueError(f"No tick data for {symbol}")
        return tick.ask

    def shutdown(self):
        mt5.shutdown()

# Example usage:
# mt5ops = MT5Ops()
# start_price = mt5ops.get_start_price("EURUSD")
# current_price = mt5ops.get_current_price("EURUSD")
