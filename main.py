import os
from dotenv import load_dotenv
from fyers_apiv3 import fyersModel

load_dotenv()

load_dotenv()

api = os.getenv("api")
secret_id = os.getenv("secret_id")
app_id = os.getenv("app_id")
redirect_url = os.getenv("redirect_url")

# connection = fyersModel.FyersModel(client_id=api, secret_key=secret_id, redirect_uri=redirect_url, response_type="code", grant_type="authorization")