import MetaTrader5 as mt5
from datetime import datetime, timedelta
import pytz

class MT5Ops:
    def __init__(self, symbol):
        self.symbol = symbol
        self.utc_plus_3 = pytz.timezone("Etc/GMT-3")

    def ensure_initialized(self):
        if not mt5.initialize():
            raise Exception("MT5 initialization failed.")

    def shutdown(self):
        mt5.shutdown()

    def get_current_price(self):
        self.ensure_initialized()
        tick = mt5.symbol_info_tick(self.symbol)
        if tick is None:
            raise Exception(f"Could not fetch tick for {self.symbol}")
        return tick.ask if tick.ask else tick.last

    def get_start_price(self, date=None):
        self.ensure_initialized()
        if date is None:
            now = datetime.now(self.utc_plus_3)
        else:
            now = self.utc_plus_3.localize(datetime.combine(date, datetime.min.time()))

        start_time = now.replace(hour=0, minute=5, second=0, microsecond=0)
        start_time_utc = start_time.astimezone(pytz.utc)

        rates = mt5.copy_rates_from(self.symbol, mt5.TIMEFRAME_M5, start_time_utc, 1)
        if rates is None or len(rates) == 0:
            raise Exception("Start price not found.")
        return rates[0]["open"]

    def get_price_and_start(self):
        self.ensure_initialized()
        current = self.get_current_price()
        start = self.get_start_price()
        return {"current_price": current, "start_price": start}