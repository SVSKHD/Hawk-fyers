from fyers_apiv3 import fyersModel
import os
from dotenv import load_dotenv

# Load saved access token and other variables
load_dotenv()

client_id = os.getenv("client_id")                  # Format: APP_ID-100
access_token = open("access_token.txt").read().strip()  # Load stored token

# Initialize Fyers API
fyers = fyersModel.FyersModel(
    client_id=client_id,
    token=access_token,
    log_path=""
)

# Example symbol for NSE: Reliance Industries (RELIANCE-EQ)
symbol = "NSE:RELIANCE-EQ"  # or MCX:GOLDMIC or NSE:SBIN-EQ etc

# Get the price (LTP)
response = fyers.quotes({"symbols": symbol})
print("📊 Quote Response:\n", response)

# To extract just the price:
try:
    ltp = response['d'][0]['v']['last_price']
    print(f"✅ Last traded price of {symbol}: {ltp}")
except:
    print("⚠️ Failed to extract price from response.")
