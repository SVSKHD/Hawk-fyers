import datetime
import os
from fyers_apiv3 import fyersModel
from config import client_id, access_token

fyers = fyersModel.FyersModel(
    client_id=client_id,
    token=access_token,
    log_path=""
)

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
            # The first candle in the response for resolution '1' should be the market start
            return response['candles'][0][1]  # [timestamp, open, high, low, close, volume]
        else:
            print(f"Could not fetch market start price for {fyers_symbol}. Response: {response}")
            return None
    except Exception as e:
        print(f"An error occurred while fetching market start price for {fyers_symbol}: {e}")
        return None