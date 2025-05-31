import MetaTrader5 as mt5
from datetime import datetime, timedelta

class MT5Ops:
    def __init__(self):
        if not mt5.initialize():
            raise RuntimeError(f"MT5 Initialization failed: {mt5.last_error()}")

    def get_start_price(self, symbol):
        now = datetime.utcnow() + timedelta(hours=3)  # UTC+3

        if now.weekday() == 0:  # Monday
            last_trading_day = now - timedelta(days=3)  # Use Friday
        else:
            last_trading_day = now - timedelta(days=1)  # Use previous day

        from_time = datetime(last_trading_day.year, last_trading_day.month, last_trading_day.day, 0, 0)
        to_time = from_time + timedelta(hours=23, minutes=59)

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
