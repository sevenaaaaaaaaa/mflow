#!/usr/bin/env python3
"""GSC OAuth 首次授权 — 获取 Refresh Token"""
import sys, json, os
from pathlib import Path
from credential_paths import credential_file, credential_output_file

OAUTH_FILE = credential_file("oauth-client.json", "LOVART_GSC_OAUTH_FILE")
TOKEN_FILE = credential_output_file("gsc-token.json", "LOVART_GSC_TOKEN_FILE")
SCOPES = ["https://www.googleapis.com/auth/webmasters.readonly"]

def main():
    if not OAUTH_FILE.exists():
        sys.exit(f"Missing: {OAUTH_FILE}")

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

    # verify
    from googleapiclient.discovery import build
    service = build("searchconsole", "v1", credentials=creds)
    sites = service.sites().list().execute()
    print("\n📊 你的 GSC 站点：")
    for s in sites.get("siteEntry", []):
        print(f"  {s['siteUrl']}  ({s['permissionLevel']})")

if __name__ == "__main__":
    main()
