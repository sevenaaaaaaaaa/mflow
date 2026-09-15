#!/usr/bin/env python3
"""
GSC 全维度拉取 — 关键词分层 + 收录状态 + 品牌分类 + 分国家

输出字段要求（seo_report_standards.py / AGENTS.md A0c）：
- 每条 query：clicks, impressions, ctr（及 position）
- 报告层须对两期数据算：点击/曝光/CTR 环比
- 细分聚合须含：点击占比、曝光占比
"""
import json, re
from pathlib import Path
from datetime import date, timedelta
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from credential_paths import credential_file
from trident_paths import DATA_INGESTION_DIR

TOKEN = credential_file("gsc-token.json", "LOVART_GSC_TOKEN_FILE")
SITE = "https://www.lovart.ai/"
SCOPES = ["https://www.googleapis.com/auth/webmasters.readonly"]

# 品牌词分类规则 — SSOT: lovart_brand_match.py
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from lovart_brand_match import is_brand, partition_keywords
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

def fetch():
    creds = Credentials.from_authorized_user_info(
        json.loads(TOKEN.read_text()), SCOPES
    )
    svc = build("searchconsole", "v1", credentials=creds)
    search = svc.searchanalytics()

    end = (date.today() - timedelta(days=2)).strftime("%Y-%m-%d")
    start_28 = (date.today() - timedelta(days=30)).strftime("%Y-%m-%d")
    results = {"_date": end, "_site": SITE}

    # =========================================================
    # 1. 关键词分层 — Top 3/10/50/100
    # =========================================================
    body_kw = {"startDate": start_28, "endDate": end, "dimensions": ["query"], "rowLimit": 100}
    resp = search.query(siteUrl=SITE, body=body_kw).execute()
    all_kw = resp.get("rows", [])
    total_clicks = sum(r["clicks"] for r in all_kw)

    brand_kw = [r for r in all_kw if is_brand(r["keys"][0])]
    nonbrand_kw = [r for r in all_kw if not is_brand(r["keys"][0])]
    competitor_hits = [r for r in nonbrand_kw if is_competitor_nonbrand(r["keys"][0])]

    def kw_stats(rows, label):
        clicks = sum(r["clicks"] for r in rows)
        impr = sum(r["impressions"] for r in rows)
        ctr = clicks / impr * 100 if impr else 0
        return {"label": label, "count": len(rows), "clicks": clicks, "impressions": impr,
                "ctr": round(ctr,1), "share": round(clicks/total_clicks*100,1) if total_clicks else 0}

    tiers = [
        kw_stats(all_kw[:3], "Top 3"),
        kw_stats(all_kw[:10], "Top 10"),
        kw_stats(all_kw[:50], "Top 50"),
        kw_stats(all_kw[:100], "Top 100"),
        kw_stats(brand_kw, "品牌词"),
        kw_stats(nonbrand_kw, "非品牌词"),
        kw_stats(competitor_hits, "竞品非品牌词"),
    ]
    results["keyword_tiers"] = tiers
    results["top100_keywords"] = [{"q": r["keys"][0], "clicks": r["clicks"], "impr": r["impressions"],
                                   "ctr": round(r["ctr"]*100,1), "pos": round(r["position"],1),
                                   "type": "brand" if is_brand(r["keys"][0]) else "nonbrand"}
                                  for r in all_kw]

    print("🔑 关键词分层 (28天)")
    print(f"  总点击: {total_clicks:,}  |  品牌词占比: {kw_stats(brand_kw,'').get('share',0):.1f}%  |  竞品词: {len(competitor_hits)}个/{kw_stats(competitor_hits,'').get('clicks',0):,}clicks")
    for t in tiers:
        tag = "⭐" if "品牌" in t["label"] else ("🎯" if "竞品" in t["label"] else "  ")
        print(f"  {tag} {t['label']:<14} {t['count']:>4}词  {t['clicks']:>10,}clicks  share={t['share']:>5.1f}%  ctr={t['ctr']:.1f}%")

    print(f"\n  Top 10 品牌词:")
    for r in brand_kw[:10]:
        print(f"    {r['keys'][0]:<40} clicks={r['clicks']:>7,}  pos={r['position']:.1f}")
    print(f"\n  Top 10 竞品非品牌词:")
    for r in competitor_hits[:10]:
        print(f"    {r['keys'][0]:<40} clicks={r['clicks']:>7,}  pos={r['position']:.1f}")

    # =========================================================
    # 2. 分国家关键词
    # =========================================================
    body_geo = {"startDate": start_28, "endDate": end, "dimensions": ["country", "query"], "rowLimit": 100}
    resp = search.query(siteUrl=SITE, body=body_geo).execute()
    geo_kw = {}
    for r in resp.get("rows", []):
        c = r["keys"][0]
        if c not in geo_kw:
            geo_kw[c] = {"clicks": 0, "impressions": 0, "queries": []}
        geo_kw[c]["clicks"] += r["clicks"]
        geo_kw[c]["impressions"] += r["impressions"]
        geo_kw[c]["queries"].append(r["keys"][1])
    top_countries = sorted(geo_kw.items(), key=lambda x: x[1]["clicks"], reverse=True)
    results["country_keywords"] = {c: d for c, d in top_countries[:10]}

    print(f"\n🌍 Top 10 国家 (关键词)")
    for c, d in top_countries[:10]:
        top_qs = sorted(d["queries"], key=lambda q: sum(r["clicks"] for r in all_kw if r["keys"][0]==q), reverse=True)[:3]
        print(f"  {c:<15} clicks={d['clicks']:>8,}  impr={d['impressions']:>10,}  关键词: {', '.join(top_qs[:3])}")

    # =========================================================
    # 3. 页面收录状态 (Sitemaps API + URL Inspection)
    # =========================================================
    try:
        sm = svc.sitemaps()
        sitemaps_resp = sm.list(siteUrl=SITE).execute()
        sitemap_entries = sitemaps_resp.get("sitemap", [])
    except Exception:
        sitemap_entries = []

    # GSC 页面维度获取已收录页面列表
    body_pages = {"startDate": start_28, "endDate": end, "dimensions": ["page"], "rowLimit": 200}
    resp = search.query(siteUrl=SITE, body=body_pages).execute()
    indexed_pages = resp.get("rows", [])
    results["pages"] = {
        "indexed_count": len(indexed_pages),
        "top20_pages": [{"url": r["keys"][0], "clicks": r["clicks"], "impr": r["impressions"]}
                        for r in indexed_pages[:20]]
    }
    sitemap_count = sum(int(s.get("contents", [{}])[0].get("submitted", 0)) for s in sitemap_entries if s.get("contents"))
    print(f"\n📄 页面收录: GSC可见 {len(indexed_pages)}+ 页  |  Sitemap提交 {sitemap_count}+ URL")

    # =========================================================
    # 4. 分国家全维度 (页面 + 关键词)
    # =========================================================
    body_geo_page = {"startDate": start_28, "endDate": end, "dimensions": ["country"], "rowLimit": 20}
    resp = search.query(siteUrl=SITE, body=body_geo_page).execute()
    results["country_summary"] = []
    print(f"\n🌍 分国家汇总:")
    for r in resp.get("rows", []):
        c, clicks, impr, ctr, pos = r["keys"][0], r["clicks"], r["impressions"], r["ctr"]*100, r["position"]
        results["country_summary"].append({"country": c, "clicks": clicks, "impressions": impr, "ctr": round(ctr,1), "pos": round(pos,1)})
        print(f"  {c:<15} clicks={clicks:>8,}  impr={impr:>10,}  ctr={ctr:5.1f}%  pos={pos:.1f}")

    # Output
    out = DATA_INGESTION_DIR
    out.mkdir(parents=True, exist_ok=True)
    (out / "gsc-full.json").write_text(json.dumps(results, indent=2, ensure_ascii=False))
    print(f"\n📁 {out}/gsc-full.json")

if __name__ == "__main__":
    fetch()
