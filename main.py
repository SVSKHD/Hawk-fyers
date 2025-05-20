import os
import webbrowser
from dotenv import load_dotenv
from fyers_apiv3 import fyersModel
from config import client_id, secret_id, redirect_url, response_type, grant_type, state

# Load .env variables
load_dotenv()

session = fyersModel.SessionModel(
    client_id=client_id,
    secret_key=secret_id,
    redirect_uri=redirect_url,
    response_type=response_type,
    grant_type=grant_type,
    state=state
)

auth_url = session.generate_authcode()
print(f"\n🔗 Opening this URL in default browser: {auth_url}\n")
webbrowser.open(auth_url)  # Automatically opens in the default browser

auth_code = input("📥 Paste the 'auth_code' from the redirected URL here:\n> ").strip()

session.set_token(auth_code)
response = session.generate_token()

access_token = response.get("access_token")
if access_token:
    print("✅ Access Token:", access_token)
    with open("access_token.txt", "w") as f:
        f.write(access_token)
    print("💾 Access Token saved.")
else:
    print("❌ Failed to retrieve access token:")
    print(response)
