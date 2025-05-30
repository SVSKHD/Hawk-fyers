import os
from dotenv import load_dotenv

load_dotenv()

client_id = os.getenv("client_id")
access_token = open("access_token.txt").read().strip()
secret_id = os.getenv("secret_id")
redirect_url = os.getenv("redirect_url")
response_type = "code"
grant_type = "authorization_code"
state = "sample_state"
symbols =[
    "NSE:SBIN-EQ", "NSE:IDEA-EQ", "NSE:RELIANCE-EQ",
    "NSE:INFY-EQ", "NSE:ICICIBANK-EQ", "NSE:HDFCBANK-EQ", "NSE:AXISBANK-EQ"
]