from threshold_logic import ThresholdLogic
from hedge_logic import HedgeLogic
from config import symbol_config

def simulate_symbol(symbol, df):
    cfg = symbol_config[symbol]
    stats = {"Total Trades": 0, "Secured 5 Pips": 0, "Secured 10 Pips": 0, "Total Pips": 0, "Hedges Triggered": 0}

    start_dates = df['timestamp'].dt.date.unique()

    for day in start_dates:
        day_data = df[df['timestamp'].dt.date == day]
        if len(day_data) < 60:
            continue

        start_price = day_data.iloc[1]['open']
        in_trade, direction, entry_price, hedge_active = False, None, None, False

        for _, row in day_data.iterrows():
            current_price = row['close']
            high, low = row['high'], row['low']

            t = ThresholdLogic(symbol, start_price, current_price, high, low, symbol_config).calculate()

            if not in_trade and t["direction"] in ["up", "down"]:
                in_trade = True
                direction = "long" if t["direction"] == "up" else "short"
                entry_price = current_price
                stats["Total Trades"] += 1

            elif in_trade:
                pip_size = cfg["pip_size"]
                profit_pips = (current_price - entry_price) / pip_size if direction == "long" else (entry_price - current_price) / pip_size

                if profit_pips >= cfg["secure_max"]:
                    stats["Secured 10 Pips"] += 1
                    stats["Total Pips"] += 10
                    in_trade = False
                elif profit_pips >= cfg["secure_min"]:
                    stats["Secured 5 Pips"] += 1
                    stats["Total Pips"] += 5
                    in_trade = False
                elif not hedge_active:
                    h = HedgeLogic(symbol, entry_price, current_price, direction, symbol_config)
                    if h.should_hedge():
                        hedge_active = True
                        stats["Hedges Triggered"] += 1

    return stats