# executor.py
from trade_ops import TradeOps
from notifier import Notifier
from trailing_stop import calculate_trailing_sl

class Executor:
    def __init__(self, symbol, config, mt5_ops, webhook_url):
        self.symbol = symbol
        self.cfg = config[symbol]
        self.mt5 = mt5_ops
        self.trader = TradeOps()
        self.notifier = Notifier(webhook_url)
        self.start_price = None
        self.trade_state = None
        self.hedge_state = None

    def initialize_day(self):
        self.start_price = self.mt5.get_start_price(self.symbol)
        self.trade_state = None
        self.hedge_state = None
        self.notifier.send(f"{self.symbol} initialized at {self.start_price}", level="DATA")

    def monitor_market(self):
        price_info = self.mt5.get_current_price(self.symbol)
        current_price = price_info['bid']
        pip_size = self.cfg['pip_size']
        pip_diff = round((current_price - self.start_price) / pip_size, 1)

        if not self.trade_state and abs(pip_diff) >= self.cfg['threshold_pips']:
            direction = 'buy' if pip_diff > 0 else 'sell'
            self.place_main_trade(direction, current_price)

        if self.trade_state:
            self.check_main_trade(current_price)

        if self.trade_state and not self.hedge_state:
            if self.should_hedge(current_price):
                self.place_hedge_trade(current_price)

        if self.hedge_state:
            self.check_hedge_exit(current_price)

    def place_main_trade(self, direction, price):
        ticket = self.trader.place_trade(symbol=self.symbol, action=direction, lot=self.cfg['lot_size'])
        self.trade_state = {
            "ticket": ticket.order,
            "entry_price": price,
            "direction": direction,
            "active": True
        }
        self.notifier.send(f"Main trade {direction.upper()} placed for {self.symbol} at {price}", level="NOTIFY")

    def check_main_trade(self, current_price):
        entry_price = self.trade_state["entry_price"]
        direction = self.trade_state["direction"]
        pip_size = self.cfg["pip_size"]
        threshold = self.cfg["min_secure_pips"]

        pip_gain = (current_price - entry_price) / pip_size if direction == "buy" else (entry_price - current_price) / pip_size

        if pip_gain >= threshold:
            self.trader.close_trade(self.trade_state["ticket"])
            self.notifier.send(f"Main trade closed for {self.symbol} at {current_price} | +{round(pip_gain, 1)} pips", level="DATA")
            self.trade_state = None
            return

        if self.cfg.get("enable_trailing", False):
            new_sl = calculate_trailing_sl(entry_price, current_price, direction, pip_size, step_pips=5)
            if new_sl:
                self.trader.modify_trade(self.trade_state["ticket"], new_sl)
                self.notifier.send(f"SL updated to {new_sl} for {self.symbol} main trade", level="INTERVAL")

    def should_hedge(self, current_price):
        entry_price = self.trade_state["entry_price"]
        direction = self.trade_state["direction"]
        pip_size = self.cfg["pip_size"]
        hedge_trigger = self.cfg["hedge_trigger"]

        loss = (entry_price - current_price) / pip_size if direction == "buy" else (current_price - entry_price) / pip_size
        return loss >= hedge_trigger

    def place_hedge_trade(self, current_price):
        direction = "sell" if self.trade_state["direction"] == "buy" else "buy"
        hedge_lot = self.cfg["lot_size"] * 2
        ticket = self.trader.place_trade(symbol=self.symbol, action=direction, lot=hedge_lot)
        self.hedge_state = {
            "ticket": ticket.order,
            "entry_price": current_price,
            "direction": direction,
            "active": True
        }
        self.notifier.send(f"HEDGE trade {direction.upper()} placed for {self.symbol} at {current_price}", level="ALERT")

    def check_hedge_exit(self, current_price):
        entry_price = self.hedge_state["entry_price"]
        direction = self.hedge_state["direction"]
        pip_size = self.cfg["pip_size"]
        threshold = self.cfg["max_secure_pips"]

        gain = (current_price - entry_price) / pip_size if direction == "buy" else (entry_price - current_price) / pip_size

        if gain >= threshold:
            self.trader.close_trade(self.hedge_state["ticket"])
            self.notifier.send(f"HEDGE trade closed for {self.symbol} at {current_price} | +{round(gain, 1)} pips", level="DATA")
            self.hedge_state = None
