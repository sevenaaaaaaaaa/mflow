#!/usr/bin/env python3
"""GSC 四周窗口拉取 — W1:7/14-20 W2:7/21-27 W3:7/28-8/3 W4:8/4-10 (周二→周一)

图表需求: 整体曝光/点击/CTR (country 维度全量) + 品牌/非品牌 (query 维度)
输出: /tmp/gsc_4w.json
"""
import json
from pathlib import Path
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

CRED_DIR = Path(__file__).resolve().parents[3] / "1-1 Harness/Skills/01-strategy/lovart-trident-data-engine/credentials"
TOKEN = json.loads((CRED_DIR / "gsc-token.json").read_text())
SITE = "https://www.lovart.ai/"
SCOPES = ["https://www.googleapis.com/auth/webmasters.readonly"]

WINDOWS = {
    "W1": ("2026-07-14", "2026-07-20"),
    "W2": ("2026-07-21", "2026-07-27"),
    "W3": ("2026-07-28", "2026-08-03"),
    "W4": ("2026-08-04", "2026-08-10"),
}

def fetch_dim(svc, dims, start, end, row_limit=25000):
    body = {"startDate": start, "endDate": end, "dimensions": dims, "rowLimit": row_limit}
    return svc.searchanalytics().query(siteUrl=SITE, body=body).execute().get("rows", [])

def main():
    creds = Credentials.from_authorized_user_info(TOKEN, SCOPES)
    svc = build("searchconsole", "v1", credentials=creds)
    out = {"_site": SITE, "windows": WINDOWS, "data": {}}
    for wname, (start, end) in WINDOWS.items():
        wdata = {}
        for dims in (["country"], ["query"]):
            key = "_".join(dims)
            rows = fetch_dim(svc, dims, start, end)
            wdata[key] = rows
            tc = sum(r["clicks"] for r in rows)
            ti = sum(r["impressions"] for r in rows)
            print(f"[{wname}] {key:>8} rows={len(rows):>6} clicks={tc:>9,} impr={ti:>10,} ctr={tc/ti*100 if ti else 0:.1f}%")
        out["data"][wname] = wdata
    Path("/tmp/gsc_4w.json").write_text(json.dumps(out, ensure_ascii=False))
    print("\nSaved /tmp/gsc_4w.json")

if __name__ == "__main__":
    main()
