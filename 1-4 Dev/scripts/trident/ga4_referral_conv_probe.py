#!/usr/bin/env python3
"""
探测 GA4 Referral 渠道的转化/收入指标是否存在。

检查: conversions, totalRevenue, purchaseRevenue, eventCount(所有事件) 在 Referral 渠道双窗口的值。
用法: python3 ga4_referral_conv_probe.py
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

METRIC_CANDIDATES = [
    "conversions", "totalRevenue", "purchaseRevenue", "ecommerceRevenue",
    "engagedSessions", "engagementRate", "totalUsers", "newUsers",
    "activeUsers", "eventCount", "screenPageViews", "userEngagementDuration",
]


def run(svc, metrics, start, end):
    sf = {"filter": {"fieldName": "streamId", "stringFilter": {"matchType": "EXACT", "value": STREAM}}}
    ref = {"filter": {"fieldName": "sessionDefaultChannelGroup",
                      "stringFilter": {"matchType": "EXACT", "value": "Referral"}}}
    body = {
        "dateRanges": [{"startDate": start, "endDate": end}],
        "dimensions": [{"name": "date"}],
        "metrics": [{"name": m} for m in metrics],
        "limit": 100,
        "dimensionFilter": {"andGroup": {"expressions": [sf, ref]}},
    }
    try:
        resp = svc.properties().runReport(property=PROPERTY, body=body).execute()
    except Exception as e:
        return {"error": str(e)}
    out = {}
    for r in resp.get("rows", []):
        d = r["dimensionValues"][0]["value"]
        row = {m: r["metricValues"][i]["value"] for i, m in enumerate(metrics)}
        out[d] = row
    return out


def main():
    creds = Credentials.from_authorized_user_info(json.loads(TOKEN_FILE.read_text()), SCOPES)
    svc = build("analyticsdata", "v1beta", credentials=creds)

    # 先试全量指标
    try:
        data = run(svc, METRIC_CANDIDATES, CUR_START, CUR_END)
        if "error" in data:
            print("批量查询失败:", data["error"])
            # 逐个查
            data = {}
            for m in METRIC_CANDIDATES:
                r = run(svc, [m], CUR_START, CUR_END)
                data[m] = r
        else:
            # 汇总逐日
            print("=== Referral 渠道 本期逐日 (全部候选指标) ===")
            for d in sorted(data):
                row = data[d]
                print(f"{d}: " + "  ".join(f"{k}={v}" for k, v in row.items() if v not in ("0", "0.0")))
    except Exception as e:
        print("FATAL:", e)
        return

    # 两窗口总览
    print("\n=== 两窗口汇总（非零指标） ===")
    for label, s, e in [("CUR", CUR_START, CUR_END), ("PRI", PRI_START, PRI_END)]:
        total = {}
        for m in METRIC_CANDIDATES:
            if isinstance(data, dict) and "error" in data:
                break
            vals = run(svc, [m], s, e)
            total[m] = sum(int(v) for v in vals.values()) if vals and all(
                str(x).lstrip("-").isdigit() for x in vals.values()) else None
        nonzero = {k: v for k, v in total.items() if v not in (None, 0)}
        print(f"{label} {s}~{e}: {nonzero}")


if __name__ == "__main__":
    main()
