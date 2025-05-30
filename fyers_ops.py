import datetime
from fyers_apiv3 import fyersModel
from fyers_apiv3.FyersWebsocket import data_ws
from config import client_id, access_token, symbols

# REST client (for historical data)
fyers = fyersModel.FyersModel(
    client_id=client_id,
    token=access_token,
    log_path=""
)

# Global live price storage
live_prices = {}

def get_market_start_price(fyers_symbol):
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    payload = {
        "symbol": fyers_symbol,
        "resolution": "1",
        "date_format": "1",
        "range_from": today,
        "range_to": today,
        "cont_flag": "1"
    }
    try:
        response = fyers.history(payload)
        if response.get('code') == 200 and 'candles' in response and len(response['candles']) > 0:
            return response['candles'][0][1]  # Open price
        else:
            print(f"[ERROR] Could not fetch open price for {fyers_symbol}. Response: {response}")
            return None
    except Exception as e:
        print(f"[EXCEPTION] {e}")
        return None

def on_message(msg):
    print("Response:", msg)
    try:
        if msg.get("type") == "symbolUpdate":
            symbol = msg["symbol"]
            ltp = msg["ltp"]
            live_prices[symbol] = ltp
            print(f"[LIVE] {symbol} = {ltp}")
    except Exception as e:
        print("[PARSE ERROR]", e)

def on_error(msg):
    print("[ERROR]", msg)

def on_close(msg):
    print("[CLOSE]", msg)

def on_open(ws):
    print("[CONNECTED] Subscribing to symbols...")
    symbols = ['NSE:SBIN-EQ', 'NSE:ADANIENT-EQ']
    ws.subscribe(symbols=symbols, data_type="SymbolUpdate")

# Create and connect the FyersDataSocket
fyers_live = data_ws.FyersDataSocket(
    access_token=access_token,
    log_path="",
    litemode=False,
    write_to_file=False,
    reconnect=True,
    on_connect=on_open,
    on_close=on_close,
    on_error=on_error,
    on_message=on_message
)

# Connect to the socket (this must be last)
fyers_live.connect()
