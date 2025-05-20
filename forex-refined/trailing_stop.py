def calculate_trailing_sl(entry_price, current_price, direction, pip_size, step_pips=5):
    pip_gain = (current_price - entry_price) / pip_size if direction == "buy" else (entry_price - current_price) / pip_size
    steps = int(pip_gain // step_pips)
    if steps <= 0:
        return None
    return round(entry_price + ((steps - 1) * step_pips * pip_size), 5) if direction == "buy" else round(entry_price - ((steps - 1) * step_pips * pip_size), 5)
