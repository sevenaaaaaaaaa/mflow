#!/usr/bin/env python3
"""
GA4 全维度拉取 — lovart.ai 专属流 + 有机流量 + 国家分层

报告层要求（seo_report_standards.py）：Sessions/Users 等指标须两期对比 + 环比；
渠道/地区细分须占比 + 环比。
"""
import json
from pathlib import Path
from datetime import date, timedelta
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from credential_paths import credential_file
from trident_paths import DATA_INGESTION_DIR

TOKEN_FILE = credential_file("ga4-token.json", "LOVART_GA4_TOKEN_FILE")
PROPERTY = "properties/403618427"
STREAM = "10524753059"
SCOPES = ["https://www.googleapis.com/auth/analytics.readonly"]

def fetch():
    creds = Credentials.from_authorized_user_info(json.loads(TOKEN_FILE.read_text()), SCOPES)
    svc = build("analyticsdata", "v1beta", credentials=creds)

    end = (date.today() - timedelta(days=2)).strftime("%Y-%m-%d")
    start_7 = (date.today() - timedelta(days=9)).strftime("%Y-%m-%d")
    start_30 = (date.today() - timedelta(days=32)).strftime("%Y-%m-%d")

    sf = {"filter": {"fieldName":"streamId", "stringFilter":{"matchType":"EXACT","value":STREAM}}}
    results = {"_date": end, "_property": PROPERTY, "_stream": STREAM}

    def run(dims, metrics, label, daterange="30d", limit=50, extra_filters=None):
        s = start_30 if daterange == "30d" else start_7
        body = {
            "dateRanges": [{"startDate": s, "endDate": end}],
            "dimensions": [{"name": d} for d in dims],
            "metrics": [{"name": m} for m in metrics],
            "limit": limit, "dimensionFilter": sf,
        }
        if extra_filters:
            body["dimensionFilter"] = {"andGroup": {"expressions": [sf] + extra_filters}}
        resp = svc.properties().runReport(property=PROPERTY, body=body).execute()
        rows = []
        for r in resp.get("rows", []):
            row = {"dims": {d: r["dimensionValues"][i]["value"] for i, d in enumerate(dims)},
                   "metrics": {m: r["metricValues"][i]["value"] for i, m in enumerate(metrics)}}
            rows.append(row)
        results[label] = rows
        return rows

    # =========================================================
    # 1. 基础访问数据 — Organic Search only
    # =========================================================
    org_filter = {"filter": {"fieldName":"sessionDefaultChannelGroup", "stringFilter":{"matchType":"EXACT","value":"Organic Search"}}}
    organic = run(["date"], ["sessions","totalUsers","newUsers","averageSessionDuration","screenPageViewsPerSession","bounceRate"],
                  "organic_daily", limit=31, extra_filters=[org_filter])
    # 30天汇总
    total_sessions = sum(int(r["metrics"]["sessions"]) for r in organic)
    total_users = sum(int(r["metrics"]["totalUsers"]) for r in organic)
    total_new = sum(int(r["metrics"]["newUsers"]) for r in organic)
    avg_dur = sum(float(r["metrics"]["averageSessionDuration"]) for r in organic) / len(organic) if organic else 0
    avg_pages = sum(float(r["metrics"]["screenPageViewsPerSession"]) for r in organic) / len(organic) if organic else 0
    weighted_bounce = sum(float(r["metrics"]["bounceRate"])*int(r["metrics"]["sessions"]) for r in organic) / total_sessions if total_sessions else 0

    results["organic_summary"] = {
        "sessions": total_sessions, "users": total_users, "new_users": total_new,
        "avg_duration_sec": round(avg_dur), "pages_per_session": round(avg_pages, 2),
        "bounce_rate": round(weighted_bounce*100, 1)
    }

    print("📊 自然搜索 — 30天汇总")
    os = results["organic_summary"]
    print(f"  Sessions: {os['sessions']:>10,}  |  Users: {os['users']:>9,}  |  New: {os['new_users']:>9,}")
    print(f"  Avg Duration: {os['avg_duration_sec']:>6}s  |  Pages/Session: {os['pages_per_session']}  |  Bounce: {os['bounce_rate']:.1f}%")

    # 日趋势
    print(f"\n  📈 最近7天:")
    for r in organic[-7:]:
        d, m = r["dims"]["date"], r["metrics"]
        print(f"    {d}  sessions={m['sessions']:>7}  users={m['totalUsers']:>6}  new={m['newUsers']:>6}  duration={float(m['averageSessionDuration']):.0f}s  pages/s={float(m['screenPageViewsPerSession']):.1f}")

    # =========================================================
    # 2. 新老用户 + 回访
    # =========================================================
    segments = run(["newVsReturning"], ["sessions","totalUsers","averageSessionDuration","screenPageViewsPerSession","bounceRate"],
                   "user_segments", extra_filters=[org_filter])
    print(f"\n👤 自然搜索用户分层:")
    for r in segments:
        d, m = r["dims"], r["metrics"]
        dur = float(m['averageSessionDuration'])
        pages = float(m['screenPageViewsPerSession'])
        print(f"  {d['newVsReturning']:<12} sessions={m['sessions']:>7}  users={m['totalUsers']:>7}  duration={dur:.0f}s  pages/s={pages:.1f}  bounce={float(m['bounceRate'])*100:.1f}%")

    # =========================================================
    # 3. 分国家 x 以上所有维度 (Organic only)
    # =========================================================
    geo = run(["country"], ["sessions","totalUsers","newUsers","averageSessionDuration","screenPageViewsPerSession","bounceRate"],
              "geo_organic", limit=20, extra_filters=[org_filter])
    print(f"\n🌍 自然搜索 — 分国家 Top 10:")
    results["geo_top10"] = []
    for r in geo[:10]:
        d, m = r["dims"], r["metrics"]
        dur = float(m['averageSessionDuration'])
        pages = float(m['screenPageViewsPerSession'])
        results["geo_top10"].append({"country": d["country"], **m})
        print(f"  {d['country']:<15} sessions={m['sessions']:>7}  users={m['totalUsers']:>7}  new={m['newUsers']:>6}  duration={dur:.0f}s  pages/s={pages:.1f}  bounce={float(m['bounceRate'])*100:.1f}%")

    # =========================================================
    # 4. 全渠道对比概览
    # =========================================================
    ch = run(["sessionDefaultChannelGroup"], ["sessions","totalUsers","bounceRate","averageSessionDuration"],
             "channel_summary", limit=10)
    print(f"\n📊 全渠道 (30天):")
    for r in ch:
        d, m = r["dims"], r["metrics"]
        print(f"  {d['sessionDefaultChannelGroup']:<20} sessions={m['sessions']:>7}  users={m['totalUsers']:>7}  bounce={float(m['bounceRate'])*100:.1f}%  dur={float(m['averageSessionDuration']):.0f}s")

    # =========================================================
    # 5. 日环比 + 周环比 + 月环比
    # =========================================================
    def period_compare(rows, days, label):
        recent = rows[-days:] if len(rows) >= days else rows
        prior = rows[-2*days:-days] if len(rows) >= 2*days else rows[:days]
        r_sessions = sum(int(r["metrics"]["sessions"]) for r in recent)
        p_sessions = sum(int(r["metrics"]["sessions"]) for r in prior)
        chg = (r_sessions - p_sessions) / p_sessions * 100 if p_sessions else 0
        results[f"trend_{label}"] = {"recent": r_sessions, "prior": p_sessions, "change_pct": round(chg,1)}
        return label, r_sessions, p_sessions, chg

    t_day = period_compare(organic, 1, "daily")
    t_week = period_compare(organic, 7, "weekly")
    t_month = period_compare(organic, 30, "monthly")

    print(f"\n📈 环比:")
    print(f"  日环比: {t_day[1]:,} vs {t_day[2]:,} → {t_day[3]:+.1f}%")
    print(f"  周环比: {t_week[1]:,} vs {t_week[2]:,} → {t_week[3]:+.1f}%")
    print(f"  月环比: {t_month[1]:,} vs {t_month[2]:,} → {t_month[3]:+.1f}%")

    # Output
    out = DATA_INGESTION_DIR
    out.mkdir(parents=True, exist_ok=True)
    (out / "ga4-full.json").write_text(json.dumps(results, indent=2, ensure_ascii=False))
    print(f"\n📁 {out}/ga4-full.json")

if __name__ == "__main__":
    fetch()
