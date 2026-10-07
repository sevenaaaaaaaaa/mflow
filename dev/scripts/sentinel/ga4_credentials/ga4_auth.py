#!/usr/bin/env python3
"""GA4 OAuth 首次授权 + 数据验证"""
import sys, json
from pathlib import Path

CRED_DIR = Path(__file__).resolve().parent
OAUTH_FILE = CRED_DIR / "service-account.json"
TOKEN_FILE = CRED_DIR / "ga4-token.json"
SCOPES = ["https://www.googleapis.com/auth/analytics.readonly"]

def main():
    from google_auth_oauthlib.flow import InstalledAppFlow

    flow = InstalledAppFlow.from_client_secrets_file(str(OAUTH_FILE), SCOPES)
    creds = flow.run_local_server(port=0)

    data = {
        "token": creds.token,
        "refresh_token": creds.refresh_token,
        "token_uri": creds.token_uri,
        "client_id": creds.client_id,
        "client_secret": creds.client_secret,
        "scopes": creds.scopes,
    }
    TOKEN_FILE.write_text(json.dumps(data, indent=2))
    print(f"✅ Token saved → {TOKEN_FILE}")

    # Try listing GA4 account summaries
    from googleapiclient.discovery import build
    svc = build("analyticsadmin", "v1beta", credentials=creds)
    resp = svc.accountSummaries().list().execute()
    print("\n📊 你的 GA4 账号和 Property：")
    for a in resp.get("accountSummaries", []):
        print(f"  账号: {a.get('account','?')} — {a.get('displayName','?')}")
        for p in a.get("propertySummaries", []):
            print(f"    Property: {p.get('property','?')} — {p.get('displayName','?')}")

if __name__ == "__main__":
    main()
