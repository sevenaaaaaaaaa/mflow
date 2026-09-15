#!/usr/bin/env python3
"""
探测 GA4 property 全站事件名（双窗口）— 查找注册/付费类转化事件。

若全站存在 sign_up/purchase 类事件，则可按 Referral 渠道 + sessionSource 拆分；
若不存在，说明转化漏斗需走 DataWorks（无 Referral 拆分）或 GA4 无埋点。
用法: python3 ga4_events_probe.py
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


def run(svc, dims, metrics, start, end, limit=500):
    sf = {"filter": {"fieldName": "streamId", "stringFilter": {"matchType": "EXACT", "value": STREAM}}}
    body = {
        "dateRanges": [{"startDate": start, "endDate": end}],
        "dimensions": [{"name": d} for d in dims],
        "metrics": [{"name": m} for m in metrics],
        "limit": limit,
        "dimensionFilter": sf,
    }
    resp = svc.properties().runReport(property=PROPERTY, body=body).execute()
    return [({d: r["dimensionValues"][i]["value"] for i, d in enumerate(dims)} | {
        m: r["metricValues"][i]["value"] for i, m in enumerate(metrics)})
        for r in resp.get("rows", [])]


def main():
    creds = Credentials.from_authorized_user_info(json.loads(TOKEN_FILE.read_text()), SCOPES)
    svc = build("analyticsdata", "v1beta", credentials=creds)

    rows = run(svc, ["eventName"], ["eventCount"], CUR_START, CUR_END, limit=500)
    rows.sort(key=lambda r: -int(r["eventCount"]))
    print(f"全站事件 Top 80 ({CUR_START}~{CUR_END}):")
    for r in rows[:80]:
        print(f"  {r['eventName']:<45} count={int(r['eventCount']):>10,}")
    print(f"\n总事件类型数: {len(rows)}")
    # 转化关键字过滤
    conv_keys = ["sign", "purchase", "pay", "order", "checkout", "register", "subscribe", "revenue", "add_to_cart", "begin"]
    hits = [r for r in rows if any(k in r["eventName"].lower() for k in conv_keys)]
    print(f"\n疑似转化事件:")
    for r in hits:
        print(f"  {r['eventName']:<45} count={int(r['eventCount']):>10,}")


if __name__ == "__main__":
    main()
