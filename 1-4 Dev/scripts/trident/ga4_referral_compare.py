#!/usr/bin/env python3
"""
GA4 Referral 渠道双窗口环比对比 — lovart.ai

对比两个 7 天窗口的 Referral 渠道数据：
  - 本期: 2026-08-04 ~ 2026-08-10（上周二~本周一）
  - 上期: 2026-07-28 ~ 2026-08-03（上上周二~上周一）

输出维度：渠道总览 / 来源域名(sessionSource) / 着陆页(landingPage) / 逐日趋势
用法: python3 ga4_referral_compare.py
"""
import json
import sys
from datetime import date, timedelta
from pathlib import Path

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

from credential_paths import credential_file
from trident_paths import DATA_INGESTION_DIR

TOKEN_FILE = credential_file("ga4-token.json", "LOVART_GA4_TOKEN_FILE")
PROPERTY = "properties/403618427"
STREAM = "10524753059"
SCOPES = ["https://www.googleapis.com/auth/analytics.readonly"]

CUR_START, CUR_END = "2026-08-04", "2026-08-10"
PRI_START, PRI_END = "2026-07-28", "2026-08-03"


def run_report(svc, dims, metrics, start, end, limit=50000, extra_filters=None):
    sf = {"filter": {"fieldName": "streamId", "stringFilter": {"matchType": "EXACT", "value": STREAM}}}
    body = {
        "dateRanges": [{"startDate": start, "endDate": end}],
        "dimensions": [{"name": d} for d in dims],
        "metrics": [{"name": m} for m in metrics],
        "limit": limit,
        "dimensionFilter": sf,
    }
    if extra_filters:
        body["dimensionFilter"] = {"andGroup": {"expressions": [sf] + extra_filters}}
    resp = svc.properties().runReport(property=PROPERTY, body=body).execute()
    rows = []
    for r in resp.get("rows", []):
        row = {
            "dims": {d: r["dimensionValues"][i]["value"] for i, d in enumerate(dims)},
            "metrics": {m: r["metricValues"][i]["value"] for i, m in enumerate(metrics)},
        }
        rows.append(row)
    return rows


def aggregate(rows):
    """聚合 sessions/users/newUsers/bounce/duration/pages 到 dict。"""
    s = sum(int(r["metrics"]["sessions"]) for r in rows)
    u = sum(int(r["metrics"]["totalUsers"]) for r in rows)
    n = sum(int(r["metrics"]["newUsers"]) for r in rows)
    d = sum(float(r["metrics"]["averageSessionDuration"]) * int(r["metrics"]["sessions"]) for r in rows)
    p = sum(float(r["metrics"]["screenPageViewsPerSession"]) * int(r["metrics"]["sessions"]) for r in rows)
    b = sum(float(r["metrics"]["bounceRate"]) * int(r["metrics"]["sessions"]) for r in rows)
    return {
        "sessions": s, "users": u, "new_users": n,
        "avg_duration_sec": round(d / s, 1) if s else 0,
        "pages_per_session": round(p / s, 2) if s else 0,
        "bounce_rate": round(b / s * 100, 1) if s else 0,
    }


def compare(a, b):
    chg = (a - b) / b * 100 if b else None
    return chg


def main():
    creds = Credentials.from_authorized_user_info(json.loads(TOKEN_FILE.read_text()), SCOPES)
    svc = build("analyticsdata", "v1beta", credentials=creds)

    ref_filter = {"filter": {"fieldName": "sessionDefaultChannelGroup",
                             "stringFilter": {"matchType": "EXACT", "value": "Referral"}}}

    METRICS = ["sessions", "totalUsers", "newUsers", "averageSessionDuration",
               "screenPageViewsPerSession", "bounceRate"]

    # ---------- 1. 渠道总览 ----------
    cur_tot = run_report(svc, ["date"], METRICS, CUR_START, CUR_END, extra_filters=[ref_filter])
    pri_tot = run_report(svc, ["date"], METRICS, PRI_START, PRI_END, extra_filters=[ref_filter])
    cur_agg, pri_agg = aggregate(cur_tot), aggregate(pri_tot)

    print("=" * 60)
    print("GA4 Referral 渠道 — 双窗口对比")
    print(f"  本期: {CUR_START} ~ {CUR_END}   (上周二~本周一)")
    print(f"  上期: {PRI_START} ~ {PRI_END}   (上上周二~上周一)")
    print("=" * 60)
    print(f"\n{'指标':<18}{'本期':>12}{'上期':>12}{'环比':>10}")
    for k, label in [("sessions", "Sessions"), ("users", "Users"), ("new_users", "New Users"),
                     ("avg_duration_sec", "Avg Duration(s)"), ("pages_per_session", "Pages/Session"),
                     ("bounce_rate", "Bounce %")]:
        a, b = cur_agg[k], pri_agg[k]
        c = compare(a, b)
        cs = f"{c:+.1f}%" if c is not None else "n/a"
        print(f"{label:<18}{a:>12,}{b:>12,}{cs:>10}")

    # ---------- 2. 来源域名 (sessionSource) ----------
    cur_src = run_report(svc, ["sessionSource"], METRICS, CUR_START, CUR_END, extra_filters=[ref_filter])
    pri_src = run_report(svc, ["sessionSource"], METRICS, PRI_START, PRI_END, extra_filters=[ref_filter])
    pri_map = {r["dims"]["sessionSource"]: aggregate([r]) for r in pri_src}

    print("\n" + "=" * 60)
    print("按来源域名 (sessionSource) 对比 — 按本期 sessions 降序")
    print("=" * 60)
    print(f"{'来源域名':<36}{'本期SS':>9}{'上期SS':>9}{'环比':>9}{'本期用户':>9}")
    cur_src_sorted = sorted(cur_src, key=lambda r: -int(r["metrics"]["sessions"]))
    for r in cur_src_sorted:
        dom = r["dims"]["sessionSource"] or "(direct/none)"
        agg = aggregate([r])
        prior = pri_map.get(r["dims"]["sessionSource"])
        p_ss = prior["sessions"] if prior else 0
        c = compare(agg["sessions"], p_ss)
        cs = f"{c:+.1f}%" if c is not None else "new"
        print(f"{dom:<36}{agg['sessions']:>9,}{p_ss:>9,}{cs:>9}{agg['users']:>9,}")
    # 上期有但本期无的（消失来源）
    cur_doms = {r["dims"]["sessionSource"] for r in cur_src}
    lost = []
    for r in pri_src:
        d = r["dims"]["sessionSource"]
        if d not in cur_doms:
            lost.append((d, aggregate([r])))
    if lost:
        print("\n⚠️ 本期消失的来源域名:")
        for d, agg in lost:
            print(f"  {d:<36} 上期 sessions={agg['sessions']:,} users={agg['users']:,}")

    # ---------- 3. 着陆页 (landingPage) ----------
    cur_lp = run_report(svc, ["landingPage"], METRICS, CUR_START, CUR_END, extra_filters=[ref_filter])
    pri_lp = run_report(svc, ["landingPage"], METRICS, PRI_START, PRI_END, extra_filters=[ref_filter])
    pri_lp_map = {r["dims"]["landingPage"]: aggregate([r]) for r in pri_lp}

    print("\n" + "=" * 60)
    print("按着陆页 (landingPage) 对比 — 按本期 sessions 降序 Top 20")
    print("=" * 60)
    print(f"{'着陆页':<52}{'本期SS':>8}{'上期SS':>8}{'环比':>9}")
    cur_lp_sorted = sorted(cur_lp, key=lambda r: -int(r["metrics"]["sessions"]))[:20]
    for r in cur_lp_sorted:
        lp = r["dims"]["landingPage"] or "(none)"
        agg = aggregate([r])
        prior = pri_lp_map.get(r["dims"]["landingPage"])
        p_ss = prior["sessions"] if prior else 0
        c = compare(agg["sessions"], p_ss)
        cs = f"{c:+.1f}%" if c is not None else "new"
        print(f"{lp:<52}{agg['sessions']:>8,}{p_ss:>8,}{cs:>9}")

    # ---------- 4. 逐日趋势 ----------
    print("\n" + "=" * 60)
    print("逐日趋势 (两窗口)")
    print("=" * 60)
    pri_days = {r["dims"]["date"]: int(r["metrics"]["sessions"]) for r in pri_tot}
    print(f"{'日期':<12}{'Sessions':>10}")
    for r in sorted(cur_tot, key=lambda x: x["dims"]["date"]):
        d, ss = r["dims"]["date"], int(r["metrics"]["sessions"])
        print(f"{d:<12}{ss:>10,}")
    print("  --- 上期 ---")
    for d in sorted(pri_days):
        print(f"{d:<12}{pri_days[d]:>10,}")

    # ---------- 5. 保存 JSON ----------
    out = DATA_INGESTION_DIR / "ga4-referral-weekly.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "_generated": date.today().isoformat(),
        "cur_window": {"start": CUR_START, "end": CUR_END},
        "pri_window": {"start": PRI_START, "end": PRI_END},
        "summary": {"cur": cur_agg, "pri": pri_agg},
        "by_source": [
            {"source": r["dims"]["sessionSource"] or "(direct)", **aggregate([r]),
             "prior_sessions": pri_map.get(r["dims"]["sessionSource"], {}).get("sessions", 0)}
            for r in cur_src_sorted
        ],
        "by_landing": [
            {"landing": r["dims"]["landingPage"] or "(none)", **aggregate([r]),
             "prior_sessions": pri_lp_map.get(r["dims"]["landingPage"], {}).get("sessions", 0)}
            for r in cur_lp_sorted
        ],
        "daily_cur": [{"date": r["dims"]["date"], "sessions": int(r["metrics"]["sessions"])}
                      for r in sorted(cur_tot, key=lambda x: x["dims"]["date"])],
        "daily_pri": [{"date": d, "sessions": v} for d, v in sorted(pri_days.items())],
    }
    out.write_text(json.dumps(payload, indent=2, ensure_ascii=False))
    print(f"\n📁 {out}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(130)
