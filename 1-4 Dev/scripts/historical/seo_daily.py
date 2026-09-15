#!/usr/bin/env python3
"""SEO 日报：GSC 200 词 + GA4 Organic（轻量）。"""
from __future__ import annotations

import json
import sys
from datetime import date, timedelta
from pathlib import Path

_SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(_SCRIPT_DIR.parent))

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

from credential_paths import credential_file
from lovart_brand_match import is_brand
from seo_monthly_v2 import country_group

from path_constants import DAILY_DIR
SITE = "https://www.lovart.ai/"
PROPERTY = "properties/403618427"
STREAM = "10524753059"


def _clients():
    gsc_t = json.loads(credential_file("gsc-token.json").read_text())
    gc = Credentials.from_authorized_user_info(gsc_t, ["https://www.googleapis.com/auth/webmasters.readonly"])
    gsc = build("searchconsole", "v1", credentials=gc, cache_discovery=False).searchanalytics()
    ga4_t = json.loads(credential_file("ga4-token.json").read_text())
    ga = Credentials.from_authorized_user_info(ga4_t, ["https://www.googleapis.com/auth/analytics.readonly"])
    ga4 = build("analyticsdata", "v1beta", credentials=ga, cache_discovery=False)
    sf = {"filter": {"fieldName": "streamId", "stringFilter": {"matchType": "EXACT", "value": STREAM}}}
    org_f = {"filter": {"fieldName": "sessionDefaultChannelGroup", "stringFilter": {"matchType": "EXACT", "value": "Organic Search"}}}
    return gsc, ga4, sf, org_f


def render_day(day: str) -> Path:
    prev = (date.fromisoformat(day) - timedelta(days=1)).isoformat()
    gsc, ga4, sf, org_f = _clients()

    def gsc_q(start, end):
        return gsc.query(
            siteUrl=SITE,
            body={"startDate": start, "endDate": end, "dimensions": ["query"], "rowLimit": 200},
        ).execute().get("rows", [])

    ck = [{"q": r["keys"][0], "clicks": r["clicks"], "impr": r["impressions"],
           "ctr": round(r["ctr"] * 100, 1)} for r in gsc_q(day, day)]
    pk = [{"q": r["keys"][0], "clicks": r["clicks"], "impr": r["impressions"],
           "ctr": round(r["ctr"] * 100, 1)} for r in gsc_q(prev, prev)]
    c_cl, p_cl = sum(k["clicks"] for k in ck), sum(k["clicks"] for k in pk)
    c_br = [k for k in ck if is_brand(k["q"])]
    c_nb = [k for k in ck if not is_brand(k["q"])]

    body_ga4 = {
        "dateRanges": [{"startDate": day, "endDate": day}],
        "dimensions": [],
        "metrics": [{"name": "sessions"}, {"name": "totalUsers"}],
        "dimensionFilter": {"andGroup": {"expressions": [sf, org_f]}},
    }
    ga4_r = ga4.properties().runReport(property=PROPERTY, body=body_ga4).execute().get("rows", [])
    sess = int(ga4_r[0]["metricValues"][0]["value"]) if ga4_r else 0
    users = int(ga4_r[0]["metricValues"][1]["value"]) if ga4_r else 0

    def chg(a, b):
        if not a:
            return f"↑{b:,}"
        d = b - a
        return f"{'↑' if d>0 else '↓'}{d:+,} / {d/a*100:.1f}%"

    top = sorted(ck, key=lambda x: x["clicks"], reverse=True)[:10]
    top_lines = "\n".join(f"- {k['q']}: {k['clicks']} clicks" for k in top)

    report = f"""# Lovart SEO 日报 — {day}

> **环比**: vs {prev}  
> **生成**: {date.today().isoformat()}  
> **数据完整度**: Draft（日报不含 DataWorks）

---

## 核心指标

| 指标 | 前日 | 当日 | 环比 |
|------|-----:|-----:|------|
| GSC 点击 | {p_cl:,} | {c_cl:,} | {chg(p_cl, c_cl)} |
| GA4 Organic Sessions | — | {sess:,} | — |
| GA4 Organic Users | — | {users:,} | — |
| 品牌词数 | — | {len(c_br)} | — |
| 非品牌词数 | — | {len(c_nb)} | — |

## Top 10 关键词

{top_lines}

## i18n 内容生产雷达

> 占位：按 locale 拆 query 需 country×query 维；日报轻量版见月报 §十一。

"""
    DAILY_DIR.mkdir(parents=True, exist_ok=True)
    out = DAILY_DIR / f"Lovart-SEO-{day}.md"
    out.write_text(report)
    print(f"✅ {out.name}")
    return out


def render_daily_range(start: date, end: date, skip_existing: bool = True) -> None:
    d = start
    while d <= end:
        out = DAILY_DIR / f"Lovart-SEO-{d.isoformat()}.md"
        if out.is_file() and skip_existing:
            print(f"  skip {d}")
        else:
            try:
                render_day(d.isoformat())
            except Exception as e:
                print(f"  ⚠️ {d}: {e}")
        d += timedelta(days=1)
