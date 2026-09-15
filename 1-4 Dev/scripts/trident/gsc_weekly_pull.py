#!/usr/bin/env python3
"""GSC 双窗口全维度拉取 — 2026-08-12..08-17 (复盘周, 6d) vs 2026-08-05..08-10 (环比, 6d)

复盘周 2026-08-12(周三)..08-18(周二)，GSC 2 天延迟 → 拉至 08-17；
环比期 2026-08-05(周三)..08-11(周二)，同长截断至 08-10，日均对比公平。
维度: query / country / page / country×query / country×page / device
输出: /tmp/gsc_windows.json (临时), 同时打印关键摘要
"""
import json, sys
from pathlib import Path
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

CRED_DIR = Path(__file__).resolve().parents[3] / "1-1 Harness/Skills/01-strategy/lovart-trident-data-engine/credentials"
TOKEN = json.loads((CRED_DIR / "gsc-token.json").read_text())
SITE = "https://www.lovart.ai/"
SCOPES = ["https://www.googleapis.com/auth/webmasters.readonly"]

WINDOWS = {
    "cur": ("2026-08-12", "2026-08-17"),
    "prev": ("2026-08-05", "2026-08-10"),
}

def fetch_dim(svc, dims, start, end, row_limit=25000):
    body = {"startDate": start, "endDate": end,
            "dimensions": dims, "rowLimit": row_limit}
    resp = svc.searchanalytics().query(siteUrl=SITE, body=body).execute()
    return resp.get("rows", [])

def main():
    creds = Credentials.from_authorized_user_info(TOKEN, SCOPES)
    svc = build("searchconsole", "v1", credentials=creds)
    out = {"_site": SITE, "windows": WINDOWS, "data": {}}
    for wname, (start, end) in WINDOWS.items():
        wdata = {}
        for dims in (["query"], ["country"], ["page"], ["country", "query"], ["country", "page"], ["device"]):
            key = "_".join(dims)
            rows = fetch_dim(svc, dims, start, end)
            wdata[key] = rows
            total_clicks = sum(r["clicks"] for r in rows)
            total_impr = sum(r["impressions"] for r in rows)
            print(f"[{wname}] {key:>16} rows={len(rows):>6} clicks={total_clicks:>9,} impr={total_impr:>10,}")
        out["data"][wname] = wdata
    Path("/tmp/gsc_windows.json").write_text(json.dumps(out, ensure_ascii=False))
    print("\nSaved /tmp/gsc_windows.json")

if __name__ == "__main__":
    main()
