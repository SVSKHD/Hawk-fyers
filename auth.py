import os
import webbrowser
from fyers_apiv3 import fyersModel
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

client_id = os.getenv("client_id")  # Format: APP_ID-100
secret_id = os.getenv("secret_id")
redirect_uri = os.getenv("redirect_url")

# Initialize the session
session = fyersModel.SessionModel(
    client_id=client_id,
    secret_key=secret_id,
    redirect_uri=redirect_uri,
    response_type="code",
    grant_type="authorization_code"
)

# Generate the auth code URL
auth_url = session.generate_authcode()
print(f"Please open the following URL in your browser to authorize the application:\n{auth_url}")

# Prompt user to enter the auth code from the redirected URL
auth_code = input("Enter the auth code from the URL after authorization: ").strip()

# Set the auth code and generate the access token
session.set_token(auth_code)
response = session.generate_token()

access_token = response.get("access_token")
if access_token:
    print("Access Token:", access_token)
    # Save the access token for future use
    with open("access_token.txt", "w") as f:
        f.write(access_token)
    print("Access Token saved to access_token.txt")
else:
    print("Failed to retrieve access token. Response:", response)
