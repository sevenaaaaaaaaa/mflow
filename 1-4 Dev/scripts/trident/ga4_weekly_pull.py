#!/usr/bin/env python3
"""GA4 双窗口拉取 — 2026-08-12..08-18 (复盘周, 7d) vs 2026-08-05..08-11 (环比, 7d)

复盘周 2026-08-12(周三)..08-18(周二)；环比期 2026-08-05(周三)..08-11(周二)。
GA4 当日数据基本可用，用完整 7d 窗口；若 08-18 数据缺失按 6d 处理并标注。
维度: organic 日趋势 / 渠道 / 地区 / 新老用户 / sessionSource 多搜索生态 / 页面
输出: /tmp/ga4_windows.json
"""
import json
from pathlib import Path
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

CRED_DIR = Path(__file__).resolve().parents[3] / "1-1 Harness/Skills/01-strategy/lovart-trident-data-engine/credentials"
TOKEN = json.loads((CRED_DIR / "ga4-token.json").read_text())
PROPERTY = "properties/403618427"
STREAM = "10524753059"
SCOPES = ["https://www.googleapis.com/auth/analytics.readonly"]

WINDOWS = {
    "cur": ("2026-08-12", "2026-08-18"),
    "prev": ("2026-08-05", "2026-08-11"),
}

def run(svc, dims, metrics, start, end, filters=None, limit=5000):
    body = {
        "dateRanges": [{"startDate": start, "endDate": end}],
        "dimensions": [{"name": d} for d in dims],
        "metrics": [{"name": m} for m in metrics],
        "limit": limit,
    }
    sf = {"filter": {"fieldName": "streamId", "stringFilter": {"matchType": "EXACT", "value": STREAM}}}
    if filters:
        body["dimensionFilter"] = {"andGroup": {"expressions": [sf] + filters}}
    else:
        body["dimensionFilter"] = sf
    resp = svc.properties().runReport(property=PROPERTY, body=body).execute()
    rows = []
    for r in resp.get("rows", []):
        rows.append({
            "dims": {d: r["dimensionValues"][i]["value"] for i, d in enumerate(dims)},
            "metrics": {m: r["metricValues"][i]["value"] for i, m in enumerate(metrics)},
        })
    return rows

ORG = {"filter": {"fieldName": "sessionDefaultChannelGroup", "stringFilter": {"matchType": "EXACT", "value": "Organic Search"}}}

def main():
    creds = Credentials.from_authorized_user_info(TOKEN, SCOPES)
    svc = build("analyticsdata", "v1beta", credentials=creds)
    out = {"_property": PROPERTY, "windows": WINDOWS, "data": {}}
    for wname, (start, end) in WINDOWS.items():
        w = {}
        w["organic_daily"] = run(svc, ["date"], ["sessions", "totalUsers", "newUsers"], start, end, [ORG])
        w["organic_daily_no_filter"] = run(svc, ["date"], ["sessions", "totalUsers"], start, end)
        w["channel"] = run(svc, ["sessionDefaultChannelGroup"], ["sessions", "totalUsers", "newUsers", "bounceRate", "averageSessionDuration"], start, end)
        w["geo"] = run(svc, ["country"], ["sessions", "totalUsers", "newUsers", "bounceRate", "averageSessionDuration"], start, end, [ORG])
        w["segments"] = run(svc, ["newVsReturning"], ["sessions", "totalUsers", "bounceRate", "averageSessionDuration", "screenPageViewsPerSession"], start, end, [ORG])
        w["source"] = run(svc, ["sessionSource"], ["sessions", "totalUsers"], start, end, [ORG])
        w["pages"] = run(svc, ["pagePath"], ["sessions", "totalUsers", "bounceRate", "averageSessionDuration", "screenPageViewsPerSession"], start, end, [ORG], limit=2000)
        out["data"][wname] = w
        tot_s = sum(int(r["metrics"]["sessions"]) for r in w["organic_daily"])
        print(f"[{wname}] organic_sessions={tot_s:>9,} 渠道={len(w['channel'])} 地区={len(w['geo'])} 来源={len(w['source'])} 页面={len(w['pages'])}")
    Path("/tmp/ga4_windows.json").write_text(json.dumps(out, ensure_ascii=False))
    print("\nSaved /tmp/ga4_windows.json")

if __name__ == "__main__":
    main()
