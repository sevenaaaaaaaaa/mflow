#!/usr/bin/env python3
"""GSC 全维度拉取 — 关键词分层 + 收录分析 + 品牌/竞品分类 + 分国家"""
import json, re
from pathlib import Path
import sys
_scripts = Path(__file__).resolve().parents[2]
if str(_scripts) not in sys.path:
    sys.path.insert(0, str(_scripts))
from lovart_brand_match import is_brand
from datetime import date, timedelta
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

CRED_DIR = Path(__file__).resolve().parent
TOKEN = CRED_DIR / "gsc-token.json"
SITE = "https://www.lovart.ai/"
SCOPES = ["https://www.googleapis.com/auth/webmasters.readonly"]

# === 品牌词规则 ===
# === 竞品非品牌词库 (从知识库加载) ===
COMPETITOR_KEYWORDS = set()
ROOT = CRED_DIR.parent.parent.parent.parent  # → 1-Project/
KW_LIB_PATH = ROOT / "insight-data" / "Trident Insights" / "竞品核心非品牌词" / "lovart_competitors_keywords.md"
try:
    lines = KW_LIB_PATH.read_text().lower().split('\n')
    for line in lines:
        parts = [p.strip() for p in line.split('|')]
        if len(parts) >= 2:
            kw = parts[1].strip().lower()
            kw = re.sub(r'^\d+\.?\s*', '', kw)
            if len(kw) > 3 and not kw.startswith('-') and not kw.startswith('关键词') and not kw.startswith('出现竞品') and not kw.startswith('>'): 
                COMPETITOR_KEYWORDS.add(kw)
except Exception as e:
    print(f"⚠️ 竞品词库加载失败: {e}")

def is_competitor_nonbrand(q):
    ql = q.lower()
    if is_brand(q): return False
    for ck in COMPETITOR_KEYWORDS:
        if ck in ql or ql in ck: return True
    return False

def fetch():
    creds = Credentials.from_authorized_user_info(json.loads(TOKEN.read_text()), SCOPES)
    svc = build("searchconsole", "v1", credentials=creds)
    search = svc.searchanalytics()

    end = (date.today() - timedelta(days=2)).strftime("%Y-%m-%d")
    start_28 = (date.today() - timedelta(days=30)).strftime("%Y-%m-%d")
    results = {"_date": end, "_site": SITE}

    # =========================================================
    # 1. 关键词分层 — Top 3/10/50/100 + 竞品匹配
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
        kw_stats(all_kw[:3], "Top 3"), kw_stats(all_kw[:10], "Top 10"),
        kw_stats(all_kw[:50], "Top 50"), kw_stats(all_kw[:100], "Top 100"),
        kw_stats(brand_kw, "品牌词"), kw_stats(nonbrand_kw, "非品牌词"),
        kw_stats(competitor_hits, "竞品非品牌词"),
    ]
    results["keyword_tiers"] = tiers
    results["top100_keywords"] = [{"q": r["keys"][0], "clicks": r["clicks"], "impr": r["impressions"],
                                   "ctr": round(r["ctr"]*100,1), "pos": round(r["position"],1),
                                   "type": "brand" if is_brand(r["keys"][0]) else ("competitor" if is_competitor_nonbrand(r["keys"][0]) else "nonbrand")}
                                  for r in all_kw]
    # 竞品词 可覆盖 vs 实际排名
    results["competitor_coverage"] = {
        "total_in_library": len(COMPETITOR_KEYWORDS),
        "matched_in_top100": len(competitor_hits),
        "matched_queries": [r["keys"][0] for r in competitor_hits],
        "total_clicks": sum(r["clicks"] for r in competitor_hits)
    }

    print("🔑 关键词分层 (28天)")
    print(f"  总点击: {total_clicks:,}  |  品牌词占比: {kw_stats(brand_kw,'').get('share',0):.1f}%")
    for t in tiers:
        tag = "⭐" if "品牌" in t["label"] else ("🎯" if "竞品" in t["label"] else "  ")
        print(f"  {tag} {t['label']:<14} {t['count']:>4}词  {t['clicks']:>10,}clicks  share={t['share']:>5.1f}%  ctr={t['ctr']:.1f}%")
    
    print(f"\n  🎯 竞品非品牌覆盖: {len(competitor_hits)}/{len(COMPETITOR_KEYWORDS)} 词库关键词出现在Top100 (覆盖 {len(competitor_hits)/max(len(COMPETITOR_KEYWORDS),1)*100:.1f}%)")
    if competitor_hits:
        print(f"  竞品词详情: " + ", ".join(f"{r['keys'][0]}({r['clicks']}cl)" for r in competitor_hits[:10]))

    print(f"\n  Top 10 品牌词:")
    for r in brand_kw[:10]:
        print(f"    {r['keys'][0]:<40} clicks={r['clicks']:>7,}  pos={r['position']:.1f}")

    # =========================================================
    # 2. 分国家
    # =========================================================
    body_geo = {"startDate": start_28, "endDate": end, "dimensions": ["country", "query"], "rowLimit": 100}
    resp = search.query(siteUrl=SITE, body=body_geo).execute()
    geo_kw = {}
    for r in resp.get("rows", []):
        c = r["keys"][0]
        if c not in geo_kw: geo_kw[c] = {"clicks": 0, "impressions": 0, "queries": []}
        geo_kw[c]["clicks"] += r["clicks"]
        geo_kw[c]["impressions"] += r["impressions"]
        geo_kw[c]["queries"].append(r["keys"][1])
    top_countries = sorted(geo_kw.items(), key=lambda x: x[1]["clicks"], reverse=True)
    results["country_keywords"] = {c: d for c, d in top_countries[:10]}

    print(f"\n🌍 Top 10 国家 (关键词)")
    for c, d in top_countries[:10]:
        print(f"  {c:<15} clicks={d['clicks']:>8,}  impr={d['impressions']:>10,}")

    # =========================================================
    # 3. 收录分析 (Sitemaps API)
    # =========================================================
    try:
        sm = svc.sitemaps()
        sitemaps_resp = sm.list(siteUrl=SITE).execute()
        sitemap_entries = sitemaps_resp.get("sitemap", [])
    except Exception:
        sitemap_entries = []

    body_pages = {"startDate": start_28, "endDate": end, "dimensions": ["page"], "rowLimit": 200}
    resp = search.query(siteUrl=SITE, body=body_pages).execute()
    indexed_pages = resp.get("rows", [])
    sitemap_count = sum(int(s.get("contents", [{}])[0].get("submitted", 0)) for s in sitemap_entries if s.get("contents"))
    traffic_pages = len(indexed_pages)
    gap = sitemap_count - traffic_pages if sitemap_count > traffic_pages else 0

    results["indexing"] = {
        "sitemap_submitted": sitemap_count,
        "pages_with_traffic_28d": traffic_pages,
        "gap_submitted_no_traffic": gap,
        "traffic_rate": round(traffic_pages/max(sitemap_count,1)*100, 2),
        "top_pages": [{"url": r["keys"][0], "clicks": r["clicks"], "impr": r["impressions"]}
                      for r in indexed_pages[:20]]
    }

    print(f"\n📄 收录分析: Sitemap提交 {sitemap_count:,} | 28天有流量 {traffic_pages:,} 页 | 缺口 {gap:,} ({traffic_pages/max(sitemap_count,1)*100:.2f}%)")

    # =========================================================
    # 4. 分国家汇总
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
    out = ROOT / "insight-data" / "Trident Insights" / "reports"
    out.mkdir(parents=True, exist_ok=True)
    (out / "gsc-full.json").write_text(json.dumps(results, indent=2, ensure_ascii=False))
    print(f"\n📁 {out}/gsc-full.json")

if __name__ == "__main__":
    fetch()
