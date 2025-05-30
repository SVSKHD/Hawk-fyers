# strategy_config.py

strategy_config = {
    "EURUSD": {
        "entry_pips": 5,
        "secure_min": 5,
        "secure_max": 7,
        "hedge_trigger": 5,
        "pip_value": 5.0,
        "pip_size": 0.0001,
        "trailing": True,
        "filter": True
    },
    "GBPUSD": {
        "entry_pips": 15,
        "secure_min": 5,
        "secure_max": 10,
        "hedge_trigger": 5,
        "pip_value": 5.0,
        "pip_size": 0.0001,
        "trailing": True,
        "filter": False
    },
    "USDJPY": {
        "entry_pips": 20,
        "secure_min": 10,
        "secure_max": 10,
        "hedge_trigger": 5,
        "pip_value": 5.0,
        "pip_size": 0.01,
        "trailing": True,
        "filter": True
    },
    "XAGUSD": {
        "entry_pips": 10,
        "secure_min": 10,
        "secure_max": 10,
        "hedge_trigger": 5,
        "pip_value": 25.0,
        "pip_size": 0.01,
        "trailing": True,
        "filter": True
    },
    "XAUUSD": {
        "entry_pips": 40,
        "secure_min": 20,
        "secure_max": 20,
        "hedge_trigger": 10,
        "pip_value": 50.0,
        "pip_size": 0.01,
        "trailing": False,
        "filter": False
    }
}
