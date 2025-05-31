# inhibitor.py
import os
from datetime import datetime


def should_allow_trade(symbol):
    """
    Checks if a trade has already been placed for the symbol today.
    Prevents multiple trades per symbol per day.
    """
    today = datetime.now().strftime("%Y-%m-%d")
    log_path = f"logs/{today}_trades.txt"

    if not os.path.exists(log_path):
        return True  # No trades today yet

    with open(log_path, "r") as file:
        for line in file:
            if line.startswith(symbol):
                return False  # Trade already placed for this symbol today

    return True
