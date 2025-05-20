# logic.py
"""
Contains symbol-specific logic configuration such as pip size, thresholds, and pip targets.
"""
config = {
    "EURUSD": {
        "lot_size": 0.5,
        "pip_size": 0.0001,
        "threshold_pips": 15,
        "min_secure_pips": 10,
        "max_secure_pips": 10,
        "hedge_trigger": 7,
        "enable_trailing": True,
        "usd_per_pip": 10,
        "margin_per_lot": 1000
    },
    "GBPUSD": {
        "lot_size": 0.5,
        "pip_size": 0.0001,
        "threshold_pips": 15,
        "min_secure_pips": 10,
        "max_secure_pips": 10,
        "hedge_trigger": 7,
        "enable_trailing": True,
        "usd_per_pip": 10,
        "margin_per_lot": 1000
    },
    "USDJPY": {
        "lot_size": 0.5,
        "pip_size": 0.01,
        "threshold_pips": 15,
        "min_secure_pips": 10,
        "max_secure_pips": 10,
        "hedge_trigger": 7,
        "enable_trailing": True,
        "usd_per_pip": 9.5,
        "margin_per_lot": 1000
    },
    "XAGUSD": {
        "lot_size": 0.5,
        "pip_size": 0.01,
        "threshold_pips": 15,
        "min_secure_pips": 10,
        "max_secure_pips": 10,
        "hedge_trigger": 7,
        "enable_trailing": True,
        "usd_per_pip": 50,
        "margin_per_lot": 1500
    }
}
