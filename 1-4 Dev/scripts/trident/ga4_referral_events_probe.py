#!/usr/bin/env python3
"""
探测 GA4 property 中 Referral 渠道的注册/付费事件名（双窗口对比用）。

输出: 两窗口内 Referral 渠道下各 eventName 的 eventCount + eventValue，按事件数降序。
用法: python3 ga4_referral_events_probe.py
"""
import json
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

from credential_paths import credential_file

TOKEN_FILE = credential_file("ga4-token.json", "LOVART_GA4_TOKEN_FILE")
PROPERTY = "properties/403618427"
STREAM = "10524753059"
SCOPES = ["https://www.googleapis.com/auth/analytics.readonly"]

CUR_START, CUR_END = "2026-08-04", "2026-08-10"
PRI_START, PRI_END = "2026-07-28", "2026-08-03"


def run(svc, dims, metrics, start, end, limit=1000):
    sf = {"filter": {"fieldName": "streamId", "stringFilter": {"matchType": "EXACT", "value": STREAM}}}
    ref = {"filter": {"fieldName": "sessionDefaultChannelGroup",
                      "stringFilter": {"matchType": "EXACT", "value": "Referral"}}}
    body = {
        "dateRanges": [{"startDate": start, "endDate": end}],
        "dimensions": [{"name": d} for d in dims],
        "metrics": [{"name": m} for m in metrics],
        "limit": limit,
        "dimensionFilter": {"andGroup": {"expressions": [sf, ref]}},
    }
    resp = svc.properties().runReport(property=PROPERTY, body=body).execute()
    rows = []
    for r in resp.get("rows", []):
        rows.append({d: r["dimensionValues"][i]["value"] for i, d in enumerate(dims)} | {
            m: r["metricValues"][i]["value"] for i, m in enumerate(metrics)})
    return rows


def main():
    creds = Credentials.from_authorized_user_info(json.loads(TOKEN_FILE.read_text()), SCOPES)
    svc = build("analyticsdata", "v1beta", credentials=creds)

    for label, start, end in [("CUR", CUR_START, CUR_END), ("PRI", PRI_START, PRI_END)]:
        rows = run(svc, ["eventName"], ["eventCount", "eventValue"], start, end, limit=200)
        rows.sort(key=lambda r: -int(r["eventCount"]))
        print(f"\n===== {label} {start}~{end} — Top 60 events (Referral) =====")
        for r in rows[:60]:
            print(f"  {r['eventName']:<45} count={int(r['eventCount']):>8,}  value={float(r['eventValue']):>12,.0f}")


if __name__ == "__main__":
    main()
