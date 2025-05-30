from fyers_apiv3.FyersWebsocket import data_ws
from config import client_id, access_token, symbols
import threading

# Define your access token
obtained_access_token = f"${client_id}:{access_token}"

# Callback functions
def on_message(message):
    print("Live Data:", message)

def on_error(message):
    print("[ERROR]", message)

def on_close(message):
    print("[CLOSED]", message)

def on_open():
    print("[CONNECTED] Subscribing to symbols...")
    # Subscribe to the symbols you want live data for
    fyers_data_socket.subscribe(symbols=symbols, data_type="SymbolUpdate")

# Initialize the WebSocket
fyers_data_socket = data_ws.FyersDataSocket(
    access_token=obtained_access_token,
    log_path="",
    write_to_file=False,
    on_connect=on_open,
    on_close=on_close,
    on_error=on_error,
    on_message=on_message
)

# Start the WebSocket
fyers_data_socket.connect()
threading.Event().wait()
