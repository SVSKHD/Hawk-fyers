# 🧠 Forex Trading Bot - README

## 📂 Project Structure

```
├── strategy_config.py       # Strategy config per symbol (entry, secure, hedge, pip_value, etc.)
├── hybrid_strategy.py       # OOP logic for trade decisions (entry, secure, trailing, hedge)
├── mt5_ops.py               # Handles MT5 price fetching, start price (UTC+3), current price
├── trade_ops.py             # Places & closes MT5 trades using FOK only (no GTC)
├── executor.py              # Core engine to manage live polling, logic, trade state
├── main.py                  # Launch file to run executor
├── logs/                    # Stores daily trade logs with ticket and entry details
└── README.md                # Documentation file (this one)
```

---

## 🔁 How the Flow Works

### 1. `main.py`

* Entry point
* Initializes the `Executor` class and starts the trading loop

### 2. `executor.py`

* Fetches start price (once per symbol at launch using UTC+3 logic)
* Loops every second to get current prices
* Applies strategy per symbol
* Places trades using `TradeExecutor`
* Saves trade details in `logs/YYYY-MM-DD_trades.txt`
* Uses ticket info to close or hedge based on signals

### 3. `strategy_config.py`

* Defines pip thresholds, trailing, hedge trigger, pip size/value for each symbol

### 4. `hybrid_strategy.py`

* Encapsulates trading logic per symbol
* Evaluates when to enter, hedge, or close trade
* Handles trailing logic and secure pip range

### 5. `mt5_ops.py`

* Fetches 12:00 AM price with Monday fallback to Friday's close
* Continuously fetches current price for each symbol

### 6. `trade_ops.py`

* Sends real MT5 orders
* Uses FOK (Fill or Kill) mode only (no GTC)
* Handles both order placement and closing

---

## 📝 Log Format (Daily)

```
symbol|direction|ticket|entry_price|lot|timestamp
```

**Example:**

```
EURUSD|BUY|12345678|1.08500|0.5|12:30:05
```

Used later to close trade by ticket.

---

## ✅ Features

* ✅ Symbol-based pip strategies
* ✅ Trailing stop-loss and hedge support
* ✅ MT5-compatible with OctaFX (FOK only)
* ✅ Volatility filter included
* ✅ Log-based position tracking

---

## 🚀 To Run the Bot

```bash
python main.py
```

> Make sure MT5 terminal is connected and symbols are enabled.

---

## 🔒 Notes

* No compounding — profits are logged, capital preserved
* Only real trades saved with ticket for traceability
* Can be easily extended with Telegram/Discord alerts or DB logging
