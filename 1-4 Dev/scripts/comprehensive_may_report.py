#!/usr/bin/env python3
"""Lovart May 2026 SEO 月度复盘 — 全维度采集 + 环比 + 报告生成"""
from __future__ import annotations

import json, re, datetime, sqlite3
from pathlib import Path
from collections import defaultdict

import sys
_SCRIPT_DIR = Path(__file__).resolve().parent
if str(_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_DIR))
from lovart_brand_match import is_brand

SKILLS = Path(__file__).resolve().parents[2] / "1-1 Harness/Skills/lovart-trident-data-engine"
CRED = SKILLS / "credentials"
LOVART_DEV = Path(__file__).resolve().parents[2] / "1-4 Dev"
TRIDENT_REPORTS = Path(__file__).resolve().parents[2] / "1-2 Insight/Trident Insights/reports"
WAREHOUSE_DB = LOVART_DEV / "Output/Warehouse/trident_data.db"
OUT_DIR = LOVART_DEV / "Output/Data Ingestion"
OUT_DIR.mkdir(parents=True, exist_ok=True)

SITE = "https://www.lovart.ai/"
SCOPES_GSC = ["https://www.googleapis.com/auth/webmasters.readonly"]
SCOPES_GA4 = ["https://www.googleapis.com/auth/analytics.readonly"]
PROPERTY = "properties/403618427"
STREAM = "10524753059"


COMPETITOR_NONBRAND = [
    'ai design', 'ai image', 'ai video', 'ai logo', 'ai art', 'ai poster',
    'ai branding', 'ai generator', 'text to image', 'text to video', 'image to video',
    'ai upscaler', 'ai background', 'ai banner', 'ai thumbnail', 'ai avatar',
    'ai cartoon', 'ai drawing', 'ai sketch', 'ai photo', 'ai editor',
    'ai design tool', 'free ai', 'best ai', 'online ai', 'ai maker'
]


def is_competitor_nonbrand(q):
    ql = q.lower()
    for p in COMPETITOR_NONBRAND:
        if p in ql and not is_brand(q):
            return True
    return False

def page_directory(url):
    url_lower = url.lower()
    for prefix in ['/blog/', '/blogs/', '/news/', '/docs/', '/features/', '/feature/',
                   '/tools/', '/tool/', '/r/', '/profile/', '/profiles/']:
        if prefix in url_lower:
            return prefix.strip('/')
    for lang in ['/zh/', '/de/', '/ja/', '/ko/', '/fr/', '/ru/', '/pt/', '/it/', '/zh-tw/', '/es/']:
        if lang in url_lower:
            return f"i18n-{lang.strip('/')}"
    return 'other'

def country_group(code):
    na = {'usa', 'can', 'united states', 'canada'}
    anglo = {'gbr', 'aus', 'nzl', 'united kingdom', 'australia', 'new zealand'}
    gc = {'chn', 'hkg', 'twn', 'china', 'hong kong', 'taiwan'}
    jp = {'jpn', 'japan'}
    code_lower = code.lower().strip()
    if code_lower in na: return '北美'
    if code_lower in anglo: return '英联邦'
    if code_lower in gc: return '大中华'
    if code_lower in jp: return '日本'
    return '其他'


# ============================================================
# GSC FETCH
# ============================================================
def fetch_gsc(start_date, end_date):
    from google.oauth2.credentials import Credentials
    from googleapiclient.discovery import build
    token = json.loads((CRED / "gsc-token.json").read_text())
    creds = Credentials.from_authorized_user_info(token, SCOPES_GSC)
    svc = build("searchconsole", "v1", credentials=creds)
    search = svc.searchanalytics()
    results = {"_start": start_date, "_end": end_date, "_site": SITE}

    # Keywords
    kw_body = {"startDate": start_date, "endDate": end_date, "dimensions": ["query"], "rowLimit": 100}
    resp = search.query(siteUrl=SITE, body=kw_body).execute()
    rows = resp.get("rows", [])
    total_clicks = sum(r["clicks"] for r in rows)
    total_impr = sum(r["impressions"] for r in rows)
    brand_rows = [r for r in rows if is_brand(r["keys"][0])]
    nonbrand_rows = [r for r in rows if not is_brand(r["keys"][0])]
    comp_rows = [r for r in nonbrand_rows if is_competitor_nonbrand(r["keys"][0])]

    def kw_stats(lst, label):
        c = sum(r["clicks"] for r in lst)
        i = sum(r["impressions"] for r in lst)
        return {"label": label, "count": len(lst), "clicks": c, "impressions": i,
                "ctr": round(c/i*100,1) if i else 0,
                "share": round(c/total_clicks*100,1) if total_clicks else 0}

    tiers_list = [3, 5, 10, 30, 50]
    all_sorted = sorted(rows, key=lambda r: r["clicks"], reverse=True)
    results["keyword_tiers"] = [kw_stats(all_sorted[:n], f"Top {n}") for n in tiers_list]
    results["keyword_tiers"].append(kw_stats(brand_rows, "品牌词"))
    results["keyword_tiers"].append(kw_stats(nonbrand_rows, "非品牌词"))
    results["keyword_tiers"].append(kw_stats(comp_rows, "竞品非品牌词"))
    results["top100_keywords"] = [
        {"q": r["keys"][0], "clicks": r["clicks"], "impr": r["impressions"],
         "ctr": round(r["ctr"]*100,1), "pos": round(r["position"],1),
         "type": "brand" if is_brand(r["keys"][0]) else "nonbrand"} for r in rows
    ]
    results["total_clicks"] = total_clicks
    results["total_impr"] = total_impr
    results["avg_ctr"] = round(total_clicks/total_impr*100,1) if total_impr else 0
    results["avg_pos"] = round(sum(r["position"] for r in rows)/len(rows),1) if rows else 0

    # Country
    geo_body = {"startDate": start_date, "endDate": end_date, "dimensions": ["country"], "rowLimit": 20}
    resp = search.query(siteUrl=SITE, body=geo_body).execute()
    results["country_summary"] = [
        {"country": r["keys"][0], "clicks": r["clicks"], "impressions": r["impressions"],
         "ctr": round(r["ctr"]*100,1), "pos": round(r["position"],1)} for r in resp.get("rows", [])
    ]

    # Pages
    page_body = {"startDate": start_date, "endDate": end_date, "dimensions": ["page"], "rowLimit": 100}
    resp = search.query(siteUrl=SITE, body=page_body).execute()
    pages = [{"url": r["keys"][0], "clicks": r["clicks"], "impressions": r["impressions"],
              "ctr": round(r["ctr"]*100,1), "pos": round(r["position"],1)} for r in resp.get("rows", [])]
    results["pages"] = pages

    # Page by directory
    dir_data = defaultdict(lambda: {"clicks": 0, "impressions": 0, "pages": 0})
    for p in pages:
        d = page_directory(p["url"])
        dir_data[d]["clicks"] += p["clicks"]
        dir_data[d]["impressions"] += p["impressions"]
        dir_data[d]["pages"] += 1
    results["page_by_directory"] = dict(sorted(dir_data.items(), key=lambda x: x[1]["clicks"], reverse=True))

    print(f"[GSC] {start_date}~{end_date}: {len(rows)} keywords, {total_clicks:,} clicks, {total_impr:,} impr, CTR {results['avg_ctr']}%")
    return results

# ============================================================
# GA4 FETCH
# ============================================================
def fetch_ga4(start_date, end_date):
    from google.oauth2.credentials import Credentials
    from googleapiclient.discovery import build
    token = json.loads((CRED / "ga4-token.json").read_text())
    creds = Credentials.from_authorized_user_info(token, SCOPES_GA4)
    svc = build("analyticsdata", "v1beta", credentials=creds)

    sf = {"filter": {"fieldName":"streamId", "stringFilter":{"matchType":"EXACT","value":STREAM}}}
    org_filter = {"filter": {"fieldName":"sessionDefaultChannelGroup", "stringFilter":{"matchType":"EXACT","value":"Organic Search"}}}
    results = {"_start": start_date, "_end": end_date}

    def run(dims, metrics, label, limit=50, extra_filters=None):
        body = {"dateRanges": [{"startDate": start_date, "endDate": end_date}],
                "dimensions": [{"name": d} for d in dims],
                "metrics": [{"name": m} for m in metrics], "limit": limit,
                "dimensionFilter": sf}
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

    # Organic summary
    organic = run(["date"], ["sessions","totalUsers","newUsers","averageSessionDuration","screenPageViewsPerSession","bounceRate"],
                  "organic_daily", limit=62, extra_filters=[org_filter])
    total_sessions = sum(int(r["metrics"]["sessions"]) for r in organic)
    total_users = sum(int(r["metrics"]["totalUsers"]) for r in organic)
    total_new = sum(int(r["metrics"]["newUsers"]) for r in organic)
    avg_dur = sum(float(r["metrics"]["averageSessionDuration"]) for r in organic) / len(organic) if organic else 0
    avg_pages = sum(float(r["metrics"]["screenPageViewsPerSession"]) for r in organic) / len(organic) if organic else 0
    weighted_bounce = sum(float(r["metrics"]["bounceRate"])*int(r["metrics"]["sessions"]) for r in organic) / total_sessions if total_sessions else 0

    results["organic_summary"] = {
        "sessions": total_sessions, "users": total_users, "new_users": total_new,
        "return_users": total_users - total_new,
        "new_user_pct": round(total_new/total_users*100,1) if total_users else 0,
        "avg_duration_sec": round(avg_dur), "pages_per_session": round(avg_pages, 2),
        "bounce_rate": round(weighted_bounce*100, 1)
    }

    # New vs returning
    segments = run(["newVsReturning"], ["sessions","totalUsers","averageSessionDuration","screenPageViewsPerSession","bounceRate"],
                   "user_segments", extra_filters=[org_filter])
    for r in segments:
        d = r["dims"]
        if d["newVsReturning"] == "new":
            results["organic_summary"]["new_sessions"] = int(r["metrics"]["sessions"])
            results["organic_summary"]["new_duration"] = round(float(r["metrics"]["averageSessionDuration"]))
            results["organic_summary"]["new_pages"] = round(float(r["metrics"]["screenPageViewsPerSession"]), 1)
            results["organic_summary"]["new_bounce"] = round(float(r["metrics"]["bounceRate"])*100, 1)
        else:
            results["organic_summary"]["return_sessions"] = int(r["metrics"]["sessions"])
            results["organic_summary"]["return_duration"] = round(float(r["metrics"]["averageSessionDuration"]))
            results["organic_summary"]["return_pages"] = round(float(r["metrics"]["screenPageViewsPerSession"]), 1)
            results["organic_summary"]["return_bounce"] = round(float(r["metrics"]["bounceRate"])*100, 1)

    # Channel overview
    ch = run(["sessionDefaultChannelGroup"], ["sessions","totalUsers","bounceRate","averageSessionDuration"],
             "channel_summary", limit=10)
    total_all_sessions = sum(int(r["metrics"]["sessions"]) for r in ch)
    results["channel_summary"] = []
    for r in ch:
        d, m = r["dims"], r["metrics"]
        sessions = int(m["sessions"])
        results["channel_summary"].append({
            "channel": d["sessionDefaultChannelGroup"],
            "sessions": sessions,
            "users": int(m["totalUsers"]),
            "bounce": round(float(m["bounceRate"])*100, 1),
            "duration": round(float(m["averageSessionDuration"])),
            "share": round(sessions/total_all_sessions*100, 1) if total_all_sessions else 0
        })

    # Geo
    geo = run(["country"], ["sessions","totalUsers","newUsers","averageSessionDuration","screenPageViewsPerSession","bounceRate"],
              "geo_organic", limit=20, extra_filters=[org_filter])
    results["geo_organic"] = []
    for r in geo:
        d, m = r["dims"], r["metrics"]
        results["geo_organic"].append({
            "country": d["country"],
            "sessions": int(m["sessions"]), "users": int(m["totalUsers"]), "new_users": int(m["newUsers"]),
            "duration": round(float(m["averageSessionDuration"])),
            "pages": round(float(m["screenPageViewsPerSession"]), 1),
            "bounce": round(float(m["bounceRate"])*100, 1)
        })

    print(f"[GA4] {start_date}~{end_date}: sessions={total_sessions:,} users={total_users:,} new={total_new:,} duration={round(avg_dur)}s pages={round(avg_pages,2)} bounce={round(weighted_bounce*100,1)}%")
    return results


# ============================================================
# MAIN
# ============================================================
def compute_mom(apr, may, key):
    a = apr.get(key, 0)
    m = may.get(key, 0)
    diff = m - a
    pct = round(diff / a * 100, 1) if a else 0
    return a, m, diff, pct

def fmt_change(a, m, diff, pct):
    arrow = "↑" if diff > 0 else ("↓" if diff < 0 else "→")
    return f"{m:,} ({arrow}{diff:+,} / {pct:+.1f}%)"

def fmt_change_float(a, m, diff, pct, decimals=1):
    arrow = "↑" if diff > 0 else ("↓" if diff < 0 else "→")
    return f"{m:.{decimals}f} ({arrow}{diff:+.{decimals}f} / {pct:+.1f}%)"

def generate_report(gsc_apr, gsc_may, ga4_apr, ga4_may, bing_data):
    report = f"""# Lovart SEO 月度复盘报告 — 2026年5月

> **周期**: 2026-05 (全月) vs 2026-04 (全月) ｜ **生成**: {datetime.date.today().isoformat()}  
> **数据源**: Google Search Console + Google Analytics 4 + Bing Webmaster Tools  
> **采集覆盖**: GSC Top 100 关键词 · GA4 全渠道 · GA4 自然搜索 · Bing 全量历史

---

## 一、整体关键词表现 (GSC 28天窗口)

### 1.1 核心指标

| 指标 | 4月 | 5月 | 环比变化 | 
|------|-----|-----|----------|
| Top 100 总点击 | {gsc_apr['total_clicks']:,} | {gsc_may['total_clicks']:,} | {fmt_change(*compute_mom(gsc_apr, gsc_may, 'total_clicks'))} |
| Top 100 总曝光 | {gsc_apr['total_impr']:,} | {gsc_may['total_impr']:,} | {fmt_change(*compute_mom(gsc_apr, gsc_may, 'total_impr'))} |
| 整体 CTR | {gsc_apr['avg_ctr']}% | {gsc_may['avg_ctr']}% | {fmt_change_float(*compute_mom(gsc_apr, gsc_may, 'avg_ctr'), decimals=1)}% |
| 平均排名 | {gsc_apr['avg_pos']:.1f} | {gsc_may['avg_pos']:.1f} | {fmt_change_float(*compute_mom(gsc_apr, gsc_may, 'avg_pos'), decimals=1)} |

### 1.2 关键词分层 (按点击)

| 分层 | 4月 点击 | 4月 占比 | 4月 CTR | → | 5月 点击 | 5月 占比 | 5月 CTR | 点击环比 |
|------|----------|----------|---------|---|----------|----------|---------|----------|
"""

    tier_names = [3, 5, 10, 30, 50]
    for n in tier_names:
        t_apr = next(t for t in gsc_apr['keyword_tiers'] if t['label'] == f'Top {n}')
        t_may = next(t for t in gsc_may['keyword_tiers'] if t['label'] == f'Top {n}')
        a_cl, m_cl, d_cl, p_cl = compute_mom(t_apr, t_may, 'clicks')
        report += f"| Top {n} | {t_apr['clicks']:,} | {t_apr['share']}% | {t_apr['ctr']}% | → | {t_may['clicks']:,} | {t_may['share']}% | {t_may['ctr']}% | {fmt_change(a_cl, m_cl, d_cl, p_cl)} |\n"

    report += f"""
### 1.3 Top 10 关键词明细

| # | 4月 关键词 | 4月 点击 | 4月 排名 | → | 5月 关键词 | 5月 点击 | 5月 排名 | 点击变化 |
|---|-----------|----------|----------|---|-----------|----------|----------|----------|
"""
    apr_kw = {k['q'].lower(): k for k in gsc_apr['top100_keywords']}
    may_kw = {k['q'].lower(): k for k in gsc_may['top100_keywords']}
    all_kw = list(dict.fromkeys(list(apr_kw.keys())[:10] + list(may_kw.keys())[:10]))[:10]
    for q in all_kw:
        ak = apr_kw.get(q, {'clicks': 0, 'ctr': 0, 'pos': 0})
        mk = may_kw.get(q, {'clicks': 0, 'ctr': 0, 'pos': 0})
        a_cl, m_cl, d_cl, p_cl = ak['clicks'], mk['clicks'], mk['clicks'] - ak['clicks'], round((mk['clicks']-ak['clicks'])/ak['clicks']*100,1) if ak['clicks'] else 0
        report += f"| {all_kw.index(q)+1} | {q[:25]} | {a_cl:,} | {ak['pos']:.1f} | → | {q[:25]} | {m_cl:,} | {mk['pos']:.1f} | {fmt_change(a_cl, m_cl, d_cl, p_cl)} |\n"

    # Section 2: GA4
    report += f"""
---

## 二、自然搜索用户数据 (GA4)

### 2.1 核心用户指标

| 指标 | 4月 | 5月 | 环比变化 |
|------|-----|-----|----------|
| Sessions | {ga4_apr['organic_summary']['sessions']:,} | {ga4_may['organic_summary']['sessions']:,} | {fmt_change(*compute_mom(ga4_apr['organic_summary'], ga4_may['organic_summary'], 'sessions'))} |
| Users | {ga4_apr['organic_summary']['users']:,} | {ga4_may['organic_summary']['users']:,} | {fmt_change(*compute_mom(ga4_apr['organic_summary'], ga4_may['organic_summary'], 'users'))} |
| New Users | {ga4_apr['organic_summary']['new_users']:,} | {ga4_may['organic_summary']['new_users']:,} | {fmt_change(*compute_mom(ga4_apr['organic_summary'], ga4_may['organic_summary'], 'new_users'))} |
| Return Users | {ga4_apr['organic_summary']['return_users']:,} | {ga4_may['organic_summary']['return_users']:,} | {fmt_change(*compute_mom(ga4_apr['organic_summary'], ga4_may['organic_summary'], 'return_users'))} |
| 新用户占比 | {ga4_apr['organic_summary']['new_user_pct']}% | {ga4_may['organic_summary']['new_user_pct']}% | {fmt_change_float(*compute_mom(ga4_apr['organic_summary'], ga4_may['organic_summary'], 'new_user_pct'))}% |
| 平均时长 | {ga4_apr['organic_summary']['avg_duration_sec']}s | {ga4_may['organic_summary']['avg_duration_sec']}s | {fmt_change(*compute_mom(ga4_apr['organic_summary'], ga4_may['organic_summary'], 'avg_duration_sec'))} |
| 页/次 | {ga4_apr['organic_summary']['pages_per_session']} | {ga4_may['organic_summary']['pages_per_session']} | {fmt_change_float(*compute_mom(ga4_apr['organic_summary'], ga4_may['organic_summary'], 'pages_per_session'))} |
| 跳出率 | {ga4_apr['organic_summary']['bounce_rate']}% | {ga4_may['organic_summary']['bounce_rate']}% | {fmt_change_float(*compute_mom(ga4_apr['organic_summary'], ga4_may['organic_summary'], 'bounce_rate'))}% |

### 2.2 新老用户分层

| 类型 | 4月 Sessions | 4月 时长 | 4月 跳出 | → | 5月 Sessions | 5月 时长 | 5月 跳出 |
|------|-------------|----------|----------|---|-------------|----------|----------|
| New | {ga4_apr['organic_summary'].get('new_sessions',0):,} | {ga4_apr['organic_summary'].get('new_duration',0)}s | {ga4_apr['organic_summary'].get('new_bounce',0)}% | → | {ga4_may['organic_summary'].get('new_sessions',0):,} | {ga4_may['organic_summary'].get('new_duration',0)}s | {ga4_may['organic_summary'].get('new_bounce',0)}% |
| Returning | {ga4_apr['organic_summary'].get('return_sessions',0):,} | {ga4_apr['organic_summary'].get('return_duration',0)}s | {ga4_apr['organic_summary'].get('return_bounce',0)}% | → | {ga4_may['organic_summary'].get('return_sessions',0):,} | {ga4_may['organic_summary'].get('return_duration',0)}s | {ga4_may['organic_summary'].get('return_bounce',0)}% |
"""

    # 2.3 Channel share
    report += f"""
### 2.3 全渠道 Sessions 占比

| 渠道 | 4月 Sessions | 4月 占比 | → | 5月 Sessions | 5月 占比 | 占比变化 |
|------|-------------|----------|---|-------------|----------|----------|
"""
    channels_4 = {c['channel']: c for c in ga4_apr.get('channel_summary', [])}
    channels_5 = {c['channel']: c for c in ga4_may.get('channel_summary', [])}
    org_s_4 = channels_4.get('Organic Search', {}).get('share', 0)
    org_s_5 = channels_5.get('Organic Search', {}).get('share', 0)
    for ch_name in channels_5:
        c4 = channels_4.get(ch_name, {})
        c5 = channels_5.get(ch_name, {})
        report += f"| {ch_name} | {c4.get('sessions',0):,} | {c4.get('share',0)}% | → | {c5.get('sessions',0):,} | {c5.get('share',0)}% | {c5.get('share',0)-c4.get('share',0):+.1f}% |\n"

    # Section 3: Brand vs NonBrand
    report += f"""
---

## 三、品牌词 vs 非品牌词

### 3.1 总览

| 维度 | 4月 | 5月 | 环比变化 |
|------|-----|-----|----------|
"""

    b_apr = next(t for t in gsc_apr['keyword_tiers'] if t['label'] == '品牌词')
    b_may = next(t for t in gsc_may['keyword_tiers'] if t['label'] == '品牌词')
    nb_apr = next(t for t in gsc_apr['keyword_tiers'] if t['label'] == '非品牌词')
    nb_may = next(t for t in gsc_may['keyword_tiers'] if t['label'] == '非品牌词')

    for label, apr_t, may_t in [("品牌词 词数", b_apr, b_may), ("品牌词 点击", b_apr, b_may), ("品牌词 曝光", b_apr, b_may),
                                 ("非品牌词 词数", nb_apr, nb_may), ("非品牌词 点击", nb_apr, nb_may), ("非品牌词 曝光", nb_apr, nb_may)]:
        if "词数" in label:
            a, m = apr_t['count'], may_t['count']
        elif "点击" in label:
            a, m = apr_t['clicks'], may_t['clicks']
        else:
            a, m = apr_t['impressions'], may_t['impressions']
        diff, pct = m - a, round((m-a)/a*100,1) if a else 0
        report += f"| {label} | {a:,} | {m:,} | {fmt_change(a,m,diff,pct)} |\n"

    report += f"| 品牌词点击占比 | {b_apr['share']}% | {b_may['share']}% | {b_may['share']-b_apr['share']:+.1f}% |\n"
    report += f"| 非品牌词点击占比 | {nb_apr['share']}% | {nb_may['share']}% | {nb_may['share']-nb_apr['share']:+.1f}% |\n"

    # 3.2 Brand top keywords
    a_brand = sorted([k for k in gsc_apr['top100_keywords'] if k['type']=='brand'], key=lambda x: x['clicks'], reverse=True)
    m_brand = sorted([k for k in gsc_may['top100_keywords'] if k['type']=='brand'], key=lambda x: x['clicks'], reverse=True)
    report += f"""
### 3.2 品牌词 Top 10

| # | 4月 | 4月点击 | 4月排名 | → | 5月 | 5月点击 | 5月排名 | 变化 |
|---|-----|---------|----------|---|-----|---------|----------|------|
"""
    for i in range(10):
        ak = a_brand[i] if i < len(a_brand) else {'q': '', 'clicks': 0, 'pos': 0}
        mk = m_brand[i] if i < len(m_brand) else {'q': '', 'clicks': 0, 'pos': 0}
        a_cl, m_cl, d_cl, p_cl = ak['clicks'], mk['clicks'], mk['clicks']-ak['clicks'], round((mk['clicks']-ak['clicks'])/ak['clicks']*100,1) if ak['clicks'] else 0
        report += f"| {i+1} | {ak['q'][:22]} | {a_cl:,} | {ak['pos']} | → | {mk['q'][:22]} | {m_cl:,} | {mk['pos']} | {fmt_change(a_cl, m_cl, d_cl, p_cl)} |\n"

    # 3.3 Nonbrand top
    a_nb = sorted([k for k in gsc_apr['top100_keywords'] if k['type']=='nonbrand'], key=lambda x: x['clicks'], reverse=True)
    m_nb = sorted([k for k in gsc_may['top100_keywords'] if k['type']=='nonbrand'], key=lambda x: x['clicks'], reverse=True)
    report += f"""
### 3.3 非品牌词 Top 10

| # | 4月 | 4月点击 | 4月CTR | → | 5月 | 5月点击 | 5月CTR | 变化 |
|---|-----|---------|---------|---|-----|---------|---------|------|
"""
    for i in range(10):
        ak = a_nb[i] if i < len(a_nb) else {'q': '', 'clicks': 0, 'ctr': 0}
        mk = m_nb[i] if i < len(m_nb) else {'q': '', 'clicks': 0, 'ctr': 0}
        a_cl, m_cl, d_cl, p_cl = ak['clicks'], mk['clicks'], mk['clicks']-ak['clicks'], round((mk['clicks']-ak['clicks'])/ak['clicks']*100,1) if ak['clicks'] else 0
        report += f"| {i+1} | {ak['q'][:22]} | {a_cl:,} | {ak['ctr']}% | → | {mk['q'][:22]} | {m_cl:,} | {mk['ctr']}% | {fmt_change(a_cl, m_cl, d_cl, p_cl)} |\n"

    # Section 4: Competitor nonbrand
    c_apr = next(t for t in gsc_apr['keyword_tiers'] if t['label'] == '竞品非品牌词')
    c_may = next(t for t in gsc_may['keyword_tiers'] if t['label'] == '竞品非品牌词')
    c_nb_kw_apr = [k for k in gsc_apr['top100_keywords'] if not is_brand(k['q']) and is_competitor_nonbrand(k['q'])]
    c_nb_kw_may = [k for k in gsc_may['top100_keywords'] if not is_brand(k['q']) and is_competitor_nonbrand(k['q'])]
    c_top10_apr = [k for k in c_nb_kw_apr if k['pos'] <= 10]
    c_top10_may = [k for k in c_nb_kw_may if k['pos'] <= 10]

    report += f"""
---

## 四、竞品非品牌词覆盖

| 指标 | 4月 | 5月 | 变化 |
|------|-----|-----|------|
| 竞品词库规模 | 252 词 | 252 词 | → |
| 有排名竞品词数 | {c_apr['count']} | {c_may['count']} | {c_may['count']-c_apr['count']:+d} |
| 竞品词点击 | {c_apr['clicks']:,} | {c_may['clicks']:,} | {fmt_change(c_apr['clicks'], c_may['clicks'], c_may['clicks']-c_apr['clicks'], round((c_may['clicks']-c_apr['clicks'])/c_apr['clicks']*100,1) if c_apr['clicks'] else 0)} |
| 竞品词曝光 | {c_apr['impressions']:,} | {c_may['impressions']:,} | {fmt_change(c_apr['impressions'], c_may['impressions'], c_may['impressions']-c_apr['impressions'], round((c_may['impressions']-c_apr['impressions'])/c_apr['impressions']*100,1) if c_apr['impressions'] else 0)} |
| 竞品词 CTR | {c_apr['ctr']}% | {c_may['ctr']}% | {c_may['ctr']-c_apr['ctr']:+.1f}% |
| 竞品词点击占非品牌比 | {c_apr['share']}% | {c_may['share']}% | {c_may['share']-c_apr['share']:+.1f}% |
| Top 10 排名竞品词数 | {len(c_top10_apr)}/{c_apr['count']} | {len(c_top10_may)}/{c_may['count']} | — |
| Top 10 占比 | {round(len(c_top10_apr)/c_apr['count']*100,1) if c_apr['count'] else 0}% | {round(len(c_top10_may)/c_may['count']*100,1) if c_may['count'] else 0}% | — |

### 4.1 竞品词明细

| # | 5月 竞品词 | 5月点击 | 5月曝光 | CTR | 排名 |
|---|-----------|----------|----------|-----|------|
"""
    for i, k in enumerate(c_nb_kw_may):
        report += f"| {i+1} | {k['q']} | {k['clicks']:,} | {k['impr']:,} | {k['ctr']}% | {k['pos']} |\n"

    # Section 5: Page directory
    report += f"""
---

## 五、页面目录流量 (GSC 自然搜索)

### 5.1 按目录 Top 15

| 目录 | 5月 点击 | 5月 曝光 | 5月 CTR | 页面数 | 占比 |
|------|----------|----------|---------|--------|------|
"""
    p_dirs = gsc_may.get('page_by_directory', {})
    total_page_clicks = sum(v['clicks'] for v in p_dirs.values())
    count = 0
    for d, v in p_dirs.items():
        if count >= 15:
            break
        share = round(v['clicks']/total_page_clicks*100, 1) if total_page_clicks else 0
        ctr = round(v['clicks']/v['impressions']*100, 1) if v['impressions'] else 0
        report += f"| {d} | {v['clicks']:,} | {v['impressions']:,} | {ctr}% | {v['pages']} | {share}% |\n"
        count += 1

    # 5.2 Focus on features/tools/blog/news/docs/r/profile
    target_dirs = ['features', 'tools', 'blog', 'news', 'docs', 'r', 'profile']
    report += f"""
### 5.2 核心内容目录占比 (排除首页/Canvas/Homes)

| 目录 | 5月 点击 | 5月 曝光 | 5月 页面数 | 占非首页流量比例 |
|------|----------|----------|-----------|-----------------|
"""
    non_home_clicks = total_page_clicks - p_dirs.get('other', {}).get('clicks', 0)
    for d in target_dirs:
        v = p_dirs.get(d, {"clicks": 0, "impressions": 0, "pages": 0})
        share = round(v['clicks']/non_home_clicks*100, 1) if non_home_clicks else 0
        ctr = round(v['clicks']/v['impressions']*100, 1) if v['impressions'] else 0
        report += f"| {d} | {v['clicks']:,} | {v['impressions']:,} | {v['pages']} | {share}% |\n"

    # Section 6: Top pages
    report += f"""
---

## 六、页面查询明细 (Top 20)

| # | URL | 5月 点击 | 5月 曝光 | 5月 CTR | 5月 排名 |
|---|-----|----------|----------|---------|----------|
"""
    for i, p in enumerate(gsc_may.get('pages', [])[:20]):
        url_short = p['url'].replace('https://www.lovart.ai', '')[:50]
        report += f"| {i+1} | {url_short} | {p['clicks']:,} | {p['impressions']:,} | {p['ctr']}% | {p['pos']:.1f} |\n"

    # Section 7: Regional breakdown
    report += f"""
---

## 七、分地区表现

### 7.1 GSC 关键词 x 地区 Top 10

| 地区 | 5月 点击 | 5月 曝光 | 5月 CTR | 5月 排名 | 分组 |
|------|----------|----------|---------|----------|------|
"""
    for c in gsc_may.get('country_summary', [])[:10]:
        report += f"| {c['country']} | {c['clicks']:,} | {c['impressions']:,} | {c['ctr']}% | {c['pos']:.1f} | {country_group(c['country'])} |\n"

    # Regional groups
    reg_apr_data = defaultdict(lambda: {"clicks": 0, "impressions": 0, "count": 0})
    reg_may_data = defaultdict(lambda: {"clicks": 0, "impressions": 0, "count": 0})
    for c in gsc_apr.get('country_summary', []):
        g = country_group(c['country'])
        reg_apr_data[g]["clicks"] += c["clicks"]
        reg_apr_data[g]["impressions"] += c["impressions"]
        reg_apr_data[g]["count"] += 1
    for c in gsc_may.get('country_summary', []):
        g = country_group(c['country'])
        reg_may_data[g]["clicks"] += c["clicks"]
        reg_may_data[g]["impressions"] += c["impressions"]
        reg_may_data[g]["count"] += 1

    report += f"""
### 7.2 地区分组 — GSC 关键词

| 地区 | 4月 点击 | 4月 曝光 | 4月 CTR | → | 5月 点击 | 5月 曝光 | 5月 CTR | 点击环比 |
|------|----------|----------|---------|---|----------|----------|---------|----------|
"""
    for grp in ['北美', '英联邦', '大中华', '日本', '其他']:
        a = reg_apr_data.get(grp, {"clicks": 0, "impressions": 0})
        m = reg_may_data.get(grp, {"clicks": 0, "impressions": 0})
        a_ctr = round(a["clicks"]/a["impressions"]*100, 1) if a["impressions"] else 0
        m_ctr = round(m["clicks"]/m["impressions"]*100, 1) if m["impressions"] else 0
        a_cl, m_cl, d_cl, p_cl = a["clicks"], m["clicks"], m["clicks"]-a["clicks"], round((m["clicks"]-a["clicks"])/a["clicks"]*100,1) if a["clicks"] else 0
        report += f"| {grp} | {a['clicks']:,} | {a['impressions']:,} | {a_ctr}% | → | {m['clicks']:,} | {m['impressions']:,} | {m_ctr}% | {fmt_change(a_cl, m_cl, d_cl, p_cl)} |\n"

    # 7.3 GA4 geo groups
    reg_ga4_apr = defaultdict(lambda: {"sessions": 0, "users": 0, "new": 0})
    reg_ga4_may = defaultdict(lambda: {"sessions": 0, "users": 0, "new": 0})
    for g in ga4_apr.get('geo_organic', []):
        reg_ga4_apr[country_group(g['country'])]["sessions"] += g["sessions"]
        reg_ga4_apr[country_group(g['country'])]["users"] += g["users"]
        reg_ga4_apr[country_group(g['country'])]["new"] += g["new_users"]
    for g in ga4_may.get('geo_organic', []):
        reg_ga4_may[country_group(g['country'])]["sessions"] += g["sessions"]
        reg_ga4_may[country_group(g['country'])]["users"] += g["users"]
        reg_ga4_may[country_group(g['country'])]["new"] += g["new_users"]

    report += f"""
### 7.3 地区分组 — GA4 自然搜索

| 地区 | 4月 Sessions | 4月 Users | 4月 New | → | 5月 Sessions | 5月 Users | 5月 New | Sessions环比 |
|------|-------------|-----------|---------|---|-------------|-----------|---------|-------------|
"""
    for grp in ['北美', '英联邦', '大中华', '日本', '其他']:
        a = reg_ga4_apr.get(grp, {"sessions": 0, "users": 0, "new": 0})
        m = reg_ga4_may.get(grp, {"sessions": 0, "users": 0, "new": 0})
        a_s, m_s, d_s, p_s = a["sessions"], m["sessions"], m["sessions"]-a["sessions"], round((m["sessions"]-a["sessions"])/a["sessions"]*100,1) if a["sessions"] else 0
        report += f"| {grp} | {a['sessions']:,} | {a['users']:,} | {a['new']:,} | → | {m['sessions']:,} | {m['users']:,} | {m['new']:,} | {fmt_change(a_s, m_s, d_s, p_s)} |\n"

    # Section 8: Insight + TODO
    report += f"""
---

## 八、核心洞察

1. **关键词集中度极高** — Top 3 品牌词占 {gsc_may['keyword_tiers'][0]['share']}% 点击，Top 50 占 {gsc_may['keyword_tiers'][3]['share']}%。长尾几乎不存在。非品牌词仅 {nb_may['share']}% 份额。

2. **自然搜索流量整体 {('增长' if ga4_may['organic_summary']['sessions'] > ga4_apr['organic_summary']['sessions'] else '下降')}** — 4月 {ga4_apr['organic_summary']['sessions']:,} → 5月 {ga4_may['organic_summary']['sessions']:,} sessions ({round((ga4_may['organic_summary']['sessions']-ga4_apr['organic_summary']['sessions'])/ga4_apr['organic_summary']['sessions']*100,1):+.1f}%)。用户粘性{('改善' if ga4_may['organic_summary']['bounce_rate'] < ga4_apr['organic_summary']['bounce_rate'] else '下降')}（跳出率 {ga4_apr['organic_summary']['bounce_rate']}% → {ga4_may['organic_summary']['bounce_rate']}%）。

3. **竞品非品牌词覆盖几乎为零** — 252 词库仅 {c_may['count']} 词有排名（{round(c_may['count']/252*100,1)}%），Top 10 内仅 {len(c_top10_may)} 词。真正行业词（AI design tool 等）完全缺失。这是 SEO 最核心的结构性问题——不是关键词策略问题，是根本没有对应内容。

4. **页面流量极度集中在首页** — /features/ /tools/ /blog/ 等核心内容目录自然搜索流量占比极低，内容规模与搜索可见性完全不成比例。

5. **地区：大中华区 GA4 流量异常高但 GSC 未覆盖** — 需确认是否为代理/非自然流量。

---

## ✅ TODO

| 优先级 | 行动项 | 数据依据 |
|--------|--------|----------|
| 🔴 P0 | 非品牌内容生产线 — 针对 AI design tool/best AI logo maker 等 252 竞品词产出 landing page | 竞品词覆盖 {c_may['count']}/252，Top 10 内仅 {len(c_top10_may)} 词 |
| 🔴 P0 | /features/ /tools/ /blog/ 目录 SEO 健康检查 — 目前自然搜索流量占比极低 | 页面目录分析 |
| 🟠 P1 | 重点地区优化 — {max(reg_may_data, key=lambda x: reg_may_data[x]['clicks'])} 市场 CTR 仅 {round(reg_may_data.get(max(reg_may_data, key=lambda x: reg_may_data[x]['clicks']), {}).get('clicks',0)/reg_may_data.get(max(reg_may_data, key=lambda x: reg_may_data[x]['clicks']), {}).get('impressions',1)*100,1)}% | 地区 CTR 数据 |
| 🟠 P1 | 内容粘性维护 — 5月页/次 {ga4_may['organic_summary']['pages_per_session']}，保持内容深度 | GA4 页/次 |
| 🟡 P2 | 建立每日/每周/季度数据看板 — 当前仅月度级别 | 需求 #8 |
| 🟡 P2 | 排查大中华区 GA4 流量异常 | {reg_ga4_may.get('大中华', {}).get('sessions', 0):,} sessions |
"""

    # Section 9: Bing supplement
    bing_kw = bing_data.get('keywords', [])
    bing_total_cl = sum(k['clicks'] for k in bing_kw)
    bing_brand = [k for k in bing_kw if is_brand(k.get('query', ''))]
    bing_nb = [k for k in bing_kw if not is_brand(k.get('query', ''))]
    report += f"""
---

## 九、Bing 补充数据 (全量历史)

> ⚠️ Bing API 返回全量历史累计数据，无法按月拆分。以下为全量截至 2026-05-30 的快照。

| 指标 | 值 |
|------|-----|
| 总关键词 | {len(bing_kw):,} |
| 总点击 | {bing_total_cl:,} |
| 品牌词 | {len(bing_brand):,} 词 |
| 非品牌词 | {len(bing_nb):,} 词 |
| 非品牌词占比 | {round(len(bing_nb)/len(bing_kw)*100,1) if bing_kw else 0}% |

### 爬虫状态

| 指标 | 值 |
|------|-----|
| 索引页数 | {bing_data.get('crawl_daily', [{}])[-1].get('InIndex', 'N/A'):,} |
| 日爬取量 | {bing_data.get('crawl_daily', [{}])[-1].get('CrawledPages', 'N/A'):,} |

---

> *本报告由 Lovart Trident Data Engine 自动生成*  
> *GSC 数据窗口: 4月 (2026-04-01~2026-04-30) vs 5月 (2026-05-01~2026-05-30)*  
> *GA4 数据窗口: 同上*  
"""
    return report


# ============================================================
# EXECUTION
# ============================================================
if __name__ == "__main__":
    print("=" * 60)
    print("  Lovart May 2026 SEO 月度复盘 — 全自动采集+分析")
    print("=" * 60)

    # 1. Fetch GSC
    print("\n[1/4] 采集 GSC 数据...")
    gsc_may_data = fetch_gsc("2026-05-01", "2026-05-30")
    gsc_apr_data = fetch_gsc("2026-04-01", "2026-04-30")

    # 2. Fetch GA4
    print("\n[2/4] 采集 GA4 数据...")
    ga4_may_data = fetch_ga4("2026-05-01", "2026-05-30")
    ga4_apr_data = fetch_ga4("2026-04-01", "2026-04-30")

    # 3. Load Bing
    print("\n[3/4] 加载 Bing 数据...")
    bing_data = json.loads(TRIDENT_REPORTS.joinpath("bing-full.json").read_text())

    # 4. Save raw data
    for name, data in [("gsc-2026-04", gsc_apr_data), ("gsc-2026-05", gsc_may_data),
                       ("ga4-2026-04", ga4_apr_data), ("ga4-2026-05", ga4_may_data)]:
        (OUT_DIR / f"{name}.json").write_text(json.dumps(data, indent=2, ensure_ascii=False))
        print(f"  📁 {OUT_DIR}/{name}.json")

    # 5. Generate report
    print("\n[4/4] 生成月度报告...")
    report = generate_report(gsc_apr_data, gsc_may_data, ga4_apr_data, ga4_may_data, bing_data)
    out_path = TRIDENT_REPORTS / "monthly" / "Lovart-SEO-2026-05.md"
    out_path.write_text(report)
    print(f"\n  📄 {out_path}")
    print(f"  📊 Report: {len(report):,} chars, ~{len(report.splitlines())} lines")
    print("\n✅ Done!")
