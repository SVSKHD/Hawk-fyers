# Forex Trading Bot - Modular Architecture

This bot executes a pip-based scalping strategy with threshold, hedge, and trailing stop logic. It is designed to run on MetaTrader 5 (MT5) and can be simulated using historical data.

## 🧠 Strategy Summary
- **Entry Trigger:** ±15 pip move from start price (at 12:00 AM UTC+3)
- **Trade Execution:** 2 trades on threshold
- **Trailing SL:** Adjusts every 5 pips profit (main trade only)
- **Hedge Logic:** If price moves 7 pips against position, opens 4 opposite trades at double lot size
- **Profit Target:** 10 pips for both main and hedge trades

---

## 📁 File Structure & Purpose

### `mt5_ops.py`
- Initializes and communicates with MetaTrader 5
- Fetches start price (UTC+3 @ 12:00 AM)
- Retrieves live prices (`bid`, `ask`, `last`)

### `trade_ops.py`
- Places, closes, and modifies trades
- All trades use **Fill or Kill (FOK)**

### `trailing_stop.py`
- Contains `calculate_trailing_sl()`
- Returns new SL every 5 pips of gain (main trades only)

### `notifier.py`
- Sends messages to Discord
- Supports levels: `DATA`, `NOTIFY`, `ALERT`, `CRITICAL`, `INTERVAL`
- Formatter for structured output
- Avoids spamming (duplicate and interval-suppressed)

### `inhibitor.py`
- Prevents multiple entries for the same symbol
- Used in `main.py` to check if trade is allowed

### `executor.py`
- **Main logic engine per symbol**
- Monitors market
- Places trades when threshold is crossed
- Applies trailing stop
- Triggers and exits hedges
- Sends notifications and manages trade state

### `main.py`
- Starts the bot
- Refreshes start price once daily (12:05 AM)
- Loops every second to call `executor.monitor_market()`
- Applies `inhibitor` logic
- Sends operational messages

### `logic.py` (a.k.a. `config.py`)
- Contains all configurable per-symbol values:
  - `pip_size`, `threshold_pips`, `lot_size`
  - `hedge_trigger`, `min_secure_pips`, `max_secure_pips`
  - `enable_trailing`, `usd_per_pip`, `margin_per_lot`

---

## ✅ Live Execution Flow
1. `main.py` initializes all modules
2. `executor.py` checks pip distance from `start_price`
3. On breach of ±15 pips, places 2 main trades
4. If price moves +10 pips, trade is closed
5. If price moves -7 pips, hedge is placed (4x lot)
6. Trailing SL is modified every +5 pips on main trade
7. Discord is notified at all key points

---

## 💡 Designed For
- High-speed pip scalping
- Real-time MT5 execution or historical CSV simulation
- Modular deployment across asset classes

---

## 🏁 Next Steps
- Add GUI / dashboard for status monitoring
- Extend to Indian markets with NSE/BSE instruments
- Integrate performance analytics from log files
