#!/usr/bin/env python3
"""JP (Japan) 全窗口 SEO 拉取 — 2025-01-01 ~ 2026-07-31。

GSC (country=JPN 过滤, 逐月, 分页全量):
  - query 维度  -> 关键词全量（品牌/非品牌/竞品分析用）
  - page 维度   -> 页面全量
  - date 维度   -> JP 日度总量（country 维度全量，不被 query 折叠影响）
GA4 (country 含 Japan 过滤):
  - date×sessionSource -> 引擎拆分趋势（Google / Bing / Yahoo / 其他）
  - landingPage        -> JP 着陆页 Top
  - country (organic)  -> JP 占全站 organic 份额
输出: /tmp/jp_pull/gsc_jp.json + /tmp/jp_pull/ga4_jp.json
"""
import json, sys, time
from pathlib import Path
from datetime import date

sys.path.insert(0, str(Path(__file__).resolve().parent))
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from credential_paths import credential_file

SITE = "https://www.lovart.ai/"
OUT = Path("/tmp/jp_pull"); OUT.mkdir(parents=True, exist_ok=True)
SCOPES_GSC = ["https://www.googleapis.com/auth/webmasters.readonly"]
SCOPES_GA4 = ["https://www.googleapis.com/auth/analytics.readonly"]
PROPERTY = "properties/403618427"
MONTHS = [f"{y}-{m:02d}" for y in (2025, 2026) for m in range(1, 13)][:19]  # 2025-01 .. 2026-07


def month_bounds(mo):
    y, m = int(mo[:4]), int(mo[5:7])
    last = [31, 29 if (y % 4 == 0 and (y % 100 != 0 or y % 400 == 0)) else 28,
            31, 30, 31, 30, 31, 31, 30, 31, 30, 31][m - 1]
    return f"{mo}-01", f"{mo}-{last:02d}"


def gsc_query(svc, start, end, dims, page_start=0, row_limit=25000, filters=None):
    body = {
        "startDate": start, "endDate": end,
        "dimensions": dims, "rowLimit": row_limit, "startRow": page_start,
    }
    if filters:
        body["dimensionFilterGroups"] = [{"filters": [{
            "dimension": "country", "operator": "equals", "expression": "JPN"}]}]
    return svc.searchanalytics().query(siteUrl=SITE, body=body).execute()


def gsc_paginate(svc, start, end, dims, filters=None):
    rows, start_row = [], 0
    while True:
        resp = gsc_query(svc, start, end, dims, page_start=start_row, filters=filters)
        batch = resp.get("rows", [])
        rows.extend(batch)
        if len(batch) < 25000:
            break
        start_row += 25000
        time.sleep(1.2)
    return rows


def norm_row(r, key_idx=0):
    k = r["keys"][key_idx]
    return {"k": k, "clicks": r["clicks"], "impr": r["impressions"],
            "ctr": round(r["ctr"] * 100, 2), "pos": round(r["position"], 1)}


def fetch_gsc():
    token = credential_file("gsc-token.json", "LOVART_GSC_TOKEN_FILE")
    creds = Credentials.from_authorized_user_info(json.loads(token.read_text()), SCOPES_GSC)
    svc = build("searchconsole", "v1", credentials=creds)
    out = {"_site": SITE, "months": {}}
    if (OUT / "gsc_jp.json").exists():
        existing = json.loads((OUT / "gsc_jp.json").read_text())
        out = existing
        print(f"  ♻ 续跑：已有 {len(existing.get('months', {}))} 个月，跳过…")
    for mo in MONTHS:
        if mo in out["months"]:
            print(f"  ⏭ {mo}: 已存在，跳过")
            continue
        s, e = month_bounds(mo)
        q = gsc_paginate(svc, s, e, ["query"], filters=True)
        p = gsc_paginate(svc, s, e, ["page"], filters=True)
        d = gsc_paginate(svc, s, e, ["date"], filters=True)
        out["months"][mo] = {
            "query": [norm_row(r) for r in q],
            "page": [norm_row(r) for r in p],
            "daily": [norm_row(r) for r in d],
        }
        tot_c = sum(r["clicks"] for r in q)
        tot_i = sum(r["impressions"] for r in q)
        tot_p = sum(r["clicks"] for r in p)
        print(f"  {mo}: query={len(q)}词({tot_c:,}clk/{tot_i:,}imp) page={len(p)}页({tot_p:,}clk) daily={len(d)}天")
        time.sleep(1.5)
        # 增量保存（断点续跑）
        (OUT / "gsc_jp.json").write_text(json.dumps(out, ensure_ascii=False))
    print("  ✅ GSC JP 全月完成")
    print(f"📁 {OUT}/gsc_jp.json")


def ga4_run(svc, start, end, dims, metrics, extra_filter=None, limit=100000):
    body = {
        "dateRanges": [{"startDate": start, "endDate": end}],
        "dimensions": [{"name": d} for d in dims],
        "metrics": [{"name": m} for m in metrics],
        "limit": limit,
    }
    if extra_filter:
        body["dimensionFilter"] = extra_filter
    return svc.properties().runReport(property=PROPERTY, body=body).execute()


def jp_filter():
    return {"filter": {"fieldName": "country", "stringFilter": {
        "matchType": "CONTAINS", "value": "Japan"}}}


def month_key(datestr):
    """GA4 date=YYYYMMDD / GSC date=YYYY-MM-DD → YYYY-MM"""
    s = datestr.replace("-", "")
    return f"{s[:4]}-{s[4:6]}"


def fetch_ga4():
    token = credential_file("ga4-token.json", "LOVART_GA4_TOKEN_FILE")
    creds = Credentials.from_authorized_user_info(json.loads(token.read_text()), SCOPES_GA4)
    svc = build("analyticsdata", "v1beta", credentials=creds)
    out = {}

    org = {"filter": {"fieldName": "sessionDefaultChannelGroup", "stringFilter": {
        "matchType": "EXACT", "value": "Organic Search"}}}

    # 1. JP date×sessionSource 引擎拆分（按月拉，Organic Search only，避免全窗口超时）
    try:
        out["jp_source_daily"] = []
        for mo in MONTHS:
            s, e = month_bounds(mo)
            jp_org = {"andGroup": {"expressions": [jp_filter(), org]}}
            resp = ga4_run(svc, s, e, ["date", "sessionSource"],
                           ["sessions", "totalUsers", "newUsers"], extra_filter=jp_org)
            rows = [
                {"date": r["dimensionValues"][0]["value"], "source": r["dimensionValues"][1]["value"],
                 "sessions": int(r["metricValues"][0]["value"]),
                 "users": int(r["metricValues"][1]["value"]),
                 "new": int(r["metricValues"][2]["value"])} for r in resp.get("rows", [])]
            out["jp_source_daily"].extend(rows)
            if rows:
                print(f"  {mo}: JP organic sessionSource {len(rows)} 行")
            time.sleep(0.5)
        print(f"  JP date×sessionSource 总计: {len(out['jp_source_daily'])} 行")
    except Exception as e:
        print(f"  ⚠ JP date×sessionSource 失败: {e}")

    # 2. JP 着陆页 Top
    try:
        resp = ga4_run(svc, "2025-01-01", "2026-07-31", ["landingPage"],
                       ["sessions", "totalUsers"], extra_filter=jp_filter())
        out["jp_landing_pages"] = [
            {"page": r["dimensionValues"][0]["value"], "sessions": int(r["metricValues"][0]["value"]),
             "users": int(r["metricValues"][1]["value"])} for r in resp.get("rows", [])]
        print(f"  JP landingPage: {len(out['jp_landing_pages'])} 页")
    except Exception as e:
        print(f"  ⚠ JP landingPage 失败: {e}")

    # 3. organic 分国家（JP 份额）
    try:
        resp = ga4_run(svc, "2025-01-01", "2026-07-31", ["country"],
                       ["sessions"], extra_filter=org)
        out["organic_by_country"] = [
            {"country": r["dimensionValues"][0]["value"], "sessions": int(r["metricValues"][0]["value"])}
            for r in resp.get("rows", [])]
        print(f"  organic by country: {len(out['organic_by_country'])} 国家")
    except Exception as e:
        print(f"  ⚠ organic by country 失败: {e}")

    # 4. JP organic 日度趋势（整窗口）
    try:
        jp_org = {"andGroup": {"expressions": [jp_filter(), org]}}
        resp = ga4_run(svc, "2025-01-01", "2026-07-31", ["date"],
                       ["sessions", "totalUsers", "newUsers"], extra_filter=jp_org)
        out["jp_organic_daily"] = [
            {"date": r["dimensionValues"][0]["value"], "sessions": int(r["metricValues"][0]["value"]),
             "users": int(r["metricValues"][1]["value"]), "new": int(r["metricValues"][2]["value"])}
            for r in resp.get("rows", [])]
        print(f"  JP organic daily: {len(out['jp_organic_daily'])} 天")
    except Exception as e:
        print(f"  ⚠ JP organic daily 失败: {e}")

    (OUT / "ga4_jp.json").write_text(json.dumps(out, ensure_ascii=False))
    print(f"📁 {OUT}/ga4_jp.json")


if __name__ == "__main__":
    which = sys.argv[1] if len(sys.argv) > 1 else "all"
    if which in ("all", "gsc"):
        fetch_gsc()
    if which in ("all", "ga4"):
        fetch_ga4()
