#!/usr/bin/env python3
"""
探测 GA4 全站转化/收入指标（不限定渠道）— 确认 property 是否有任何转化埋点。

用法: python3 ga4_conv_probe_any.py
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

METRICS = [
    "conversions", "totalRevenue", "purchaseRevenue", "ecommercePurchases",
    "engagedSessions", "engagementRate", "totalUsers", "newUsers", "eventCount",
]


def main():
    creds = Credentials.from_authorized_user_info(json.loads(TOKEN_FILE.read_text()), SCOPES)
    svc = build("analyticsdata", "v1beta", credentials=creds)

    sf = {"filter": {"fieldName": "streamId", "stringFilter": {"matchType": "EXACT", "value": STREAM}}}
    body = {
        "dateRanges": [{"startDate": CUR_START, "endDate": CUR_END}],
        "metrics": [{"name": m} for m in METRICS],
        "limit": 10,
        "dimensionFilter": sf,
    }
    try:
        resp = svc.properties().runReport(property=PROPERTY, body=body).execute()
        row = resp.get("rows", [{}])[0]
        for i, m in enumerate(METRICS):
            v = row["metricValues"][i]["value"]
            print(f"  {m:<25} = {v}")
    except Exception as e:
        print("查询失败:", str(e)[:500])


if __name__ == "__main__":
    main()
