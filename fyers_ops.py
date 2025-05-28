import datetime
import time
from fyers_apiv3 import fyersModel
from fyers_apiv3.FyersWebsocket import data_ws
from config import client_id, access_token

# Initialize Fyers REST client
fyers = fyersModel.FyersModel(
    client_id=client_id,
    token=access_token,
    log_path=""
)

# Global store for live prices
live_prices = {}

def get_market_start_price(fyers_symbol):
    """
    Fetch the market open price for the day from historical candles.
    """
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
            return response['candles'][0][1]  # open price
        else:
            print(f"Could not fetch market start price for {fyers_symbol}. Response: {response}")
            return None
    except Exception as e:
        print(f"An error occurred while fetching market start price for {fyers_symbol}: {e}")
        return None

# WebSocket Event Handlers
def on_message(message):
    try:
        symbol = message.get("symbol")
        price = message.get("ltp")
        if symbol and price:
            live_prices[symbol] = price
            print(f"[UPDATE] {symbol} = {price}")
    except Exception as e:
        print(f"[ERROR] WebSocket on_message: {e}")

def on_error(msg):
    print("Socket Error:", msg)

def on_close(msg):
    print("Socket Closed:", msg)

def on_connect():
    # List of symbols to subscribe
    symbols = ['NSE:SBIN-EQ', 'NSE:IDEA-EQ', 'NSE:RELIANCE-EQ',
               'NSE:INFY-EQ', 'NSE:ICICIBANK-EQ', 'NSE:HDFCBANK-EQ', 'NSE:AXISBANK-EQ']
    fyers_socket.subscribe(symbols=symbols, data_type="LTP")
    print(f"[SUBSCRIBED] Subscribed to: {symbols}")

# Global socket object
fyers_socket = data_ws.FyersDataSocket(
    access_token=access_token,
    log_path="",
    write_to_file=False,
    reconnect=True,
    on_connect=on_connect,
    on_close=on_close,
    on_error=on_error,
    on_message=on_message
)

def start_fyers_socket():
    """
    Start WebSocket connection and subscribe to LTP updates.
    """
    fyers_socket.connect()
    print("[INFO] Fyers WebSocket started...")
