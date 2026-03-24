"""
Step 1 — Run this ONCE to authenticate with Microsoft Teams.
It will open a browser login page. Sign in with ayesha.khan@taleemabad.com.
Token saved to teams_token.json for future use.
"""

import msal
import json
import os

CLIENT_ID = "e48c927b-a021-43d0-ac47-e1c2060805a1"
TENANT_ID = "629ab41b-cec2-46db-8bb5-7596d8a9243a"
AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
SCOPES = ["https://graph.microsoft.com/OnlineMeetings.ReadWrite"]
TOKEN_FILE = "teams_token.json"

app = msal.PublicClientApplication(CLIENT_ID, authority=AUTHORITY)

# Try cached token first
accounts = app.get_accounts()
result = None
if accounts:
    result = app.acquire_token_silent(SCOPES, account=accounts[0])

if not result:
    # Interactive login — opens browser
    result = app.acquire_token_interactive(scopes=SCOPES)

if "access_token" in result:
    with open(TOKEN_FILE, "w") as f:
        json.dump(result, f)
    print("✅ Authentication successful! Token saved to teams_token.json")
    print(f"   Signed in as: {result.get('id_token_claims', {}).get('preferred_username', 'unknown')}")
else:
    print("❌ Authentication failed:")
    print(result.get("error_description", result))
