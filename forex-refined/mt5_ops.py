import MetaTrader5 as mt5
from datetime import datetime, time, timedelta
import pytz

class MT5Ops:
    def __init__(self, timezone='Etc/GMT-3'):
        self.initialized = False
        self.timezone = pytz.timezone(timezone)
        self.initialize()

    def initialize(self):
        if not self.initialized and not mt5.initialize():
            raise RuntimeError("MT5 Initialization failed")
        self.initialized = True

    def get_start_price(self, symbol):
        now = datetime.now(self.timezone)
        midnight = datetime.combine(now.date(), time(0, 0)).replace(tzinfo=self.timezone)
        midnight_utc = midnight.astimezone(pytz.utc)
        rates = mt5.copy_rates_range(symbol, mt5.TIMEFRAME_M1, midnight_utc, midnight_utc + timedelta(minutes=1))
        if rates is None or len(rates) == 0:
            raise ValueError(f"No data for {symbol} at 12:00 AM")
        return rates[0]['open']

    def get_current_price(self, symbol):
        tick = mt5.symbol_info_tick(symbol)
        if tick is None:
            raise ValueError(f"No price data for {symbol}")
        return {"bid": tick.bid, "ask": tick.ask, "last": tick.last}

    def shutdown(self):
        mt5.shutdown()
