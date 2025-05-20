from fyers_ops import get_market_start_price



if __name__ == "__main__":
    symbols_to_check = ["NSE:SBIN-EQ", "NSE:IDEA-EQ", "NSE:RELIANCE-EQ", "NSE:INFY-EQ", "NSE:ICICIBANK-EQ", "NSE:HDFCBANK-EQ", "NSE:AXISBANK-EQ"]

    for symbol in symbols_to_check:
        start_price = get_market_start_price(symbol)
        if start_price is not None:
            print(f"Market start price for {symbol}: {start_price}")
        else:
            print(f"Could not retrieve market start price for {symbol}.")