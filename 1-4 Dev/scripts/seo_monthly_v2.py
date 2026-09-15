#!/usr/bin/env python3
"""
Lovart SEO 月报 V2 — 全量 5K 词 GSC + GA4 + 竞品词库 + 完整 10 板块

强制标准（与 AGENTS.md Part A0–A0d / seo_report_standards.py 同步）：
- 环比：报告月 vs 上一自然月（--month 2026-05 → vs 2026-04）
- 关键词：点击+曝光+CTR + 点击/曝光/CTR 环比 + §4.4–4.7 movers
- 结构（固定顺序）：一 核心洞察 → 二 OKR 看板 → 三 SEO Dashboard(A–F)
  → 四 关键词分层 → 五 GA4 用户 → 六 DataWorks 平台拆解 → 七 品牌vs非品牌
  → 八 竞品 → 九 页面目录 → 十 页面查询 → 十一 分地区 → 十二 TODO → 十三 Bing
- 实现：seo_monthly_extras.py；快照 --resume / --render-only
- OKR：跑前 Agent 须问用户是否更新（默认 2026-05 版）
"""
from __future__ import annotations
import argparse, json, re, datetime, sys
from calendar import monthrange
from pathlib import Path
from collections import defaultdict

_SCRIPT_DIR = Path(__file__).resolve().parent
if str(_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_DIR))
from seo_report_standards import (
    OKR_EFFECTIVE_MONTH,
    monthly_post_run_checklist,
    print_pre_run_checklist,
    okr_confirmation_reminder,
)
from lovart_brand_match import is_brand, partition_keywords
from lovart_indexing_metrics import fetch_indexing_bundle
from lovart_seo_geo_metrics import ingest_for_month, load_seo_geo_snapshot
from seo_monthly_extras import (
    annual_note,
    build_region_pages,
    load_metrics_history,
    enrich_core_ctx_with_product,
    enrich_core_ctx_with_bing,
    enrich_core_ctx_with_platforms,
    load_content_inventory,
    render_core_insights,
    render_executive_dashboards,
    render_movers_section,
    render_engine_overview,
    render_bing_keyword_block,
    render_cross_engine_keyword_overlap,
    render_engine_compare_kw,
    render_bing_brand_block,
    render_bing_competitor_detail,
    render_bing_competitor_block,
    render_bing_pages_block,
    render_bing_top_pages,
    render_bing_region_section,
    render_ga4_engine_split,
    okr_traffic_metrics,
    render_okr_section,
    render_seo_geo_section,
    render_region_executive_summary,
    region_mini_block,
    save_metrics_snapshot,
    section_insight_brand,
    section_insight_comp,
    section_insight_ga4_with_product,
    section_insight_keywords,
    section_insight_pages,
    section_insight_region_summary,
    share_pp_chg,
    tiers_table_full,
    pct_str,
)


def report_month_meta(ym: str) -> dict:
    """YYYY-MM report month; compare vs previous calendar month."""
    y, m = map(int, ym.split("-"))
    curr_last = monthrange(y, m)[1]
    if m == 1:
        py, pm = y - 1, 12
    else:
        py, pm = y, m - 1
    prev_last = monthrange(py, pm)[1]
    ps, pe = f"{py}-{pm:02d}-01", f"{py}-{pm:02d}-{prev_last}"
    cs, ce = f"{y}-{m:02d}-01", f"{y}-{m:02d}-{curr_last}"
    return {
        "report_ym": ym,
        "title_year_month": f"{y}年{m}月",
        "period_line": f"{ym} (全月) vs {py}-{pm:02d} (全月)",
        "prev_label": f"{pm}月",
        "curr_label": f"{m}月",
        "prev_start": ps,
        "prev_end": pe,
        "curr_start": cs,
        "curr_end": ce,
        "footer_gsc": (
            f"{pm}月({ps[5:7]}-{ps[8:10]}~{pe[8:10]}) vs "
            f"{m}月({cs[5:7]}-{cs[8:10]}~{ce[8:10]})"
        ),
    }

SKILLS = Path(__file__).resolve().parents[2] / "1-1 Harness/Skills/lovart-trident-data-engine"
_CRED_CANDIDATES = [
    SKILLS / "credentials",
    _SCRIPT_DIR / "sentinel" / "gsc_credentials",
    _SCRIPT_DIR / "sentinel" / "ga4_credentials",
]


def _cred_file(name: str) -> Path:
    for d in _CRED_CANDIDATES:
        p = d / name
        if p.is_file():
            return p
    return _CRED_CANDIDATES[0] / name
TRIDENT = Path(__file__).resolve().parents[2] / "1-2 Insight/Trident Insights"
OUT_DIR = Path(__file__).resolve().parents[2] / "1-4 Dev/Output/Data Ingestion"
OUT_DIR.mkdir(parents=True, exist_ok=True)
SNAPSHOT_DIR = OUT_DIR / "monthly-snapshots"
SNAPSHOT_DIR.mkdir(parents=True, exist_ok=True)


def snapshot_path(kind: str, ym: str) -> Path:
    return SNAPSHOT_DIR / f"{kind}-{ym}.json"


def save_snapshot(kind: str, ym: str, data: dict) -> None:
    snapshot_path(kind, ym).write_text(json.dumps(data, ensure_ascii=False, default=str))


def refresh_keyword_brand_splits(g: dict | None) -> None:
    """快照可能含旧品牌划分；每次跑报前按 lovart_brand_match 重算。"""
    if not g or not g.get("keywords"):
        return
    g["brand_kw"], g["nonbrand_kw"] = partition_keywords(g["keywords"])


def _merge_top_kw_rows(rows: list[dict], extra: list[dict], n: int = 15) -> list[dict]:
    by_q: dict[str, dict] = {}
    for k in rows + extra:
        q = k["q"]
        if q not in by_q or k["clicks"] > by_q[q]["clicks"]:
            by_q[q] = k
    return sorted(by_q.values(), key=lambda x: x["clicks"], reverse=True)[:n]


def rebuild_region_brand_lists(g: dict | None) -> None:
    """从快照 Top 词表纠偏：误落在非品牌表的词条移回品牌表。"""
    if not g:
        return
    rb = g.setdefault("region_brand_top", {})
    rnb = g.setdefault("region_nonbrand_top", {})
    rs = g.setdefault("region_stats", {})
    for grp in set(rb) | set(rnb) | set(rs):
        sc = rs.setdefault(
            grp,
            {"clicks": 0, "impr": 0, "brand": {"clicks": 0, "impr": 0}, "nonbrand": {"clicks": 0, "impr": 0}},
        )
        nb_old = list(rnb.get(grp, []))
        kept_nb, moved = [], []
        for k in nb_old:
            if is_brand(k["q"]):
                moved.append(k)
            else:
                kept_nb.append(k)
        if moved:
            sc["brand"]["clicks"] += sum(x["clicks"] for x in moved)
            sc["brand"]["impr"] += sum(x["impr"] for x in moved)
            sc["nonbrand"]["clicks"] = max(0, sc["nonbrand"]["clicks"] - sum(x["clicks"] for x in moved))
            sc["nonbrand"]["impr"] = max(0, sc["nonbrand"]["impr"] - sum(x["impr"] for x in moved))
        rb[grp] = _merge_top_kw_rows(list(rb.get(grp, [])), moved)
        rnb[grp] = _merge_top_kw_rows(kept_nb, [])


def refresh_gsc_regions_from_api(start: str, end: str, label: str) -> dict:
    """仅重拉 country×query，用最新 is_brand 重算大区品牌/非品牌。"""
    from google.oauth2.credentials import Credentials
    from googleapiclient.discovery import build

    token = json.loads(_cred_file("gsc-token.json").read_text())
    creds = Credentials.from_authorized_user_info(token, ["https://www.googleapis.com/auth/webmasters.readonly"])
    search = build("searchconsole", "v1", credentials=creds).searchanalytics()
    r = search.query(
        siteUrl=SITE,
        body={"startDate": start, "endDate": end, "dimensions": ["country", "query"], "rowLimit": 5000},
    ).execute()
    rq = build_region_from_cq(r.get("rows", []))
    print(f"  🌍 大区重算 {label}: {len(rq['region_stats'])} 区")
    return rq


def load_snapshot(kind: str, ym: str) -> dict | None:
    p = snapshot_path(kind, ym)
    if not p.exists():
        return None
    return json.loads(p.read_text())


def load_ga4_from_legacy_cache(ym: str) -> dict | None:
    """从 ga4-{ym}.json 缓存转换为 fetch_ga4_full 结构。"""
    p = OUT_DIR / f"ga4-{ym}.json"
    if not p.exists():
        return None
    d = json.loads(p.read_text())
    s = d.get("organic_summary", {})
    channels = {}
    for row in d.get("channel_summary", []):
        channels[row["channel"]] = {
            "sessions": row["sessions"],
            "users": row["users"],
            "bounce": row["bounce"],
            "share": row["share"],
        }
    segments = {}
    for row in d.get("user_segments", []):
        t = row["dims"]["newVsReturning"]
        if t in ("new", "returning"):
            segments[t] = {
                "sessions": int(row["metrics"]["sessions"]),
                "dur": round(float(row["metrics"]["averageSessionDuration"])),
                "pages": round(float(row["metrics"]["screenPageViewsPerSession"]), 1),
                "bounce": round(float(row["metrics"]["bounceRate"]) * 100, 1),
            }
    geo = [
        {
            "country": g["country"],
            "sessions": g["sessions"],
            "users": g["users"],
            "new_users": g.get("new_users", 0),
            "dur": g.get("duration", g.get("dur", 0)),
            "pages": g.get("pages", 0),
            "bounce": g.get("bounce", 0),
        }
        for g in d.get("geo_organic", [])
    ]
    m = ym.split("-")[1].lstrip("0") or "0"
    return {
        "_label": f"{m}月",
        "sessions": s.get("sessions", 0),
        "users": s.get("users", 0),
        "new_users": s.get("new_users", 0),
        "return_users": s.get("return_users", s.get("users", 0) - s.get("new_users", 0)),
        "new_user_pct": s.get("new_user_pct", 0),
        "avg_dur": s.get("avg_duration_sec", s.get("avg_dur", 0)),
        "pages_per_session": s.get("pages_per_session", 0),
        "bounce": s.get("bounce_rate", s.get("bounce", 0)),
        "channels": channels,
        "segments": segments,
        "geo": geo,
    }

SITE = "https://www.lovart.ai/"
PROPERTY = "properties/403618427"
STREAM = "10524753059"

# is_brand → lovart_brand_match.py (SSOT)


TARGET_GROUPS = {
    '北美': ['usa','can','gbr','aus','nzl','united states','canada','united kingdom','australia','new zealand'],
    '大中华': ['chn','hkg','twn','mac','china','hong kong','taiwan','macau'],
    '日本': ['jpn','japan'],
    '拉美': ['bra','mex','arg','col','per','chl','ven','ecu','bol','ury','pry','brazil','mexico','argentina','colombia','peru','chile','venezuela','ecuador','bolivia','uruguay','paraguay'],
    '南亚': ['ind','pak','bgd','lka','npl','india','pakistan','bangladesh','sri lanka','nepal'],
    '中东非洲': ['egy','mar','dza','sau','are','nga','tur','irn','zaf','egypt','morocco','algeria','saudi arabia','united arab emirates','nigeria','turkey','türkiye','iran','south africa'],
}
REGION_ORDER = ['北美', '大中华', '日本', '拉美', '南亚', '中东非洲', '其他']

def country_group(code):
    cl = code.lower().strip()
    for grp, codes in TARGET_GROUPS.items():
        if cl in codes: return grp
    return '其他'


def classify_page(url: str) -> str:
    """与 weekly_review_v3.classify 对齐，避免首页/语言首页落入 other。"""
    base = SITE.lower().rstrip("/")
    u = url.lower().split("?")[0].replace(base, "") or "/"
    if u in ("/", ""):
        return "首页"
    if "/canvas" in u:
        return "canvas"
    if "/login" in u or "/signup" in u or "/auth" in u:
        return "login/auth"
    if "/pricing" in u:
        return "pricing"
    for prefix, name in [
        ("/blog/", "blog"), ("/blogs/", "blog"), ("/news/", "news"), ("/docs/", "docs"),
        ("/features/", "features"), ("/feature/", "features"),
        ("/tools/", "tools"), ("/tool/", "tools"),
        ("/r/", "r"), ("/profile/", "profile"), ("/profiles/", "profile"),
    ]:
        if prefix in u:
            return name
    lang_inner = [
        ("/zh-tw/", "zh-TW"), ("/zh/", "zh"), ("/ja/", "ja"), ("/pt/", "pt"),
        ("/ru/", "ru"), ("/de/", "de"), ("/fr/", "fr"), ("/ko/", "ko"), ("/it/", "it"), ("/es/", "es"),
    ]
    for prefix, code in lang_inner:
        if u.startswith(prefix):
            return f"i18n内页-{code}"
    lang_home = [
        ("/zh-tw", "zh-TW"), ("/zh", "zh"), ("/ja", "ja"), ("/pt", "pt"),
        ("/ru", "ru"), ("/de", "de"), ("/fr", "fr"), ("/ko", "ko"), ("/it", "it"), ("/es", "es"),
    ]
    for path, code in lang_home:
        if u == path or u == path + "/":
            return f"语言首页-{code}"
    return "其他"


def format_page_path(url: str) -> str:
    s = url.replace(SITE, "").replace("https://www.lovart.ai", "").strip()
    return s if s else "/"


def build_region_from_cq(cq_rows):
    """国家×query → 大区汇总、品牌/非品牌 Top5、大区品牌/非品牌汇总。"""
    region_totals = defaultdict(lambda: {"clicks": 0, "impr": 0})
    region_brand_agg = defaultdict(lambda: {"clicks": 0, "impr": 0})
    region_nb_agg = defaultdict(lambda: {"clicks": 0, "impr": 0})
    brand_by_q = defaultdict(lambda: defaultdict(lambda: {"clicks": 0, "impr": 0, "pos": 0.0}))
    nb_by_q = defaultdict(lambda: defaultdict(lambda: {"clicks": 0, "impr": 0, "pos": 0.0}))

    for rw in cq_rows:
        g = country_group(rw["keys"][0])
        q = rw["keys"][1]
        cl, im, pos = rw["clicks"], rw["impressions"], rw["position"]
        region_totals[g]["clicks"] += cl
        region_totals[g]["impr"] += im
        if is_brand(q):
            region_brand_agg[g]["clicks"] += cl
            region_brand_agg[g]["impr"] += im
            brand_by_q[g][q]["clicks"] += cl
            brand_by_q[g][q]["impr"] += im
            brand_by_q[g][q]["pos"] += pos
        else:
            region_nb_agg[g]["clicks"] += cl
            region_nb_agg[g]["impr"] += im
            nb_by_q[g][q]["clicks"] += cl
            nb_by_q[g][q]["impr"] += im
            nb_by_q[g][q]["pos"] += pos

    region_stats = {}
    for g in set(region_totals) | set(region_brand_agg) | set(region_nb_agg):
        region_stats[g] = {
            "clicks": region_totals[g]["clicks"],
            "impr": region_totals[g]["impr"],
            "brand": region_brand_agg.get(g, {"clicks": 0, "impr": 0}),
            "nonbrand": region_nb_agg.get(g, {"clicks": 0, "impr": 0}),
        }

    def top_kw(bucket, g, n=15):
        items = sorted(bucket.get(g, {}).items(), key=lambda x: x[1]["clicks"], reverse=True)[:n]
        return [{"q": q, "clicks": v["clicks"], "impr": v["impr"],
                 "ctr": round(v["clicks"] / v["impr"] * 100, 1) if v["impr"] else 0,
                 "pos": round(v["pos"], 1)} for q, v in items]

    return {
        "region_stats": region_stats,
        "region_brand_top": {g: top_kw(brand_by_q, g) for g in brand_by_q},
        "region_nonbrand_top": {g: top_kw(nb_by_q, g) for g in nb_by_q},
    }

def _chg_delta(a, m):
    if isinstance(a, float):
        a = round(a, 2)
    if isinstance(m, float):
        m = round(m, 2)
    d = m - a
    if isinstance(d, float):
        d = int(d) if d == int(d) else round(d, 2)
    return a, m, d


def chg_str(a, m):
    _, _, d = _chg_delta(a, m)
    p = round(d / a * 100, 1) if a else 0
    arrow = "↑" if d > 0 else ("↓" if d < 0 else "→")
    return f"{arrow}{d:+,} / {p:+.1f}%"


def chg_f(a, m, dec=1):
    _, _, d = _chg_delta(a, m)
    p = round(d / a * 100, 1) if a else 0
    arrow = "↑" if d > 0 else ("↓" if d < 0 else "→")
    return f"{arrow}{d:+{dec + 1 if dec else 0}.{dec}f} / {p:+.1f}%"

# ============================================================
# 1. GSC 5K + Country×Query
# ============================================================
def fetch_gsc_full(start, end, label, report_ym: str | None = None, refresh_indexing: bool = False):
    from google.oauth2.credentials import Credentials
    from googleapiclient.discovery import build
    token = json.loads(_cred_file("gsc-token.json").read_text())
    creds = Credentials.from_authorized_user_info(token, ["https://www.googleapis.com/auth/webmasters.readonly"])
    svc = build("searchconsole", "v1", credentials=creds)
    search = svc.searchanalytics()
    
    # Query dimension
    r = search.query(siteUrl=SITE, body={"startDate":start,"endDate":end,"dimensions":["query"],"rowLimit":5000}).execute()
    kw_rows = r.get("rows", [])
    keywords = [{"q":rw["keys"][0], "clicks":rw["clicks"], "impr":rw["impressions"],
                 "ctr":round(rw["ctr"]*100,1), "pos":round(rw["position"],1)} for rw in kw_rows]
    
    # Country dimension
    r = search.query(siteUrl=SITE, body={"startDate":start,"endDate":end,"dimensions":["country"],"rowLimit":50}).execute()
    countries = [{"country":rw["keys"][0], "clicks":rw["clicks"], "impr":rw["impressions"],
                  "ctr":round(rw["ctr"]*100,1), "pos":round(rw["position"],1)} for rw in r.get("rows",[])]
    
    # Country × Query — 大区品牌/非品牌汇总 + Top5
    r = search.query(siteUrl=SITE, body={"startDate":start,"endDate":end,"dimensions":["country","query"],"rowLimit":5000}).execute()
    cq = r.get("rows", [])
    rq = build_region_from_cq(cq)
    region_kw = defaultdict(list)
    for rw in cq:
        g = country_group(rw["keys"][0])
        region_kw[g].append({
            "q": rw["keys"][1], "clicks": rw["clicks"], "impr": rw["impressions"],
            "ctr": round(rw["ctr"]*100,1), "pos": round(rw["position"],1)
        })
    
    # Country × Page — 大区 Top 页面
    region_pages = {}
    try:
        r = search.query(siteUrl=SITE, body={"startDate":start,"endDate":end,"dimensions":["country","page"],"rowLimit":5000}).execute()
        region_pages = build_region_pages(r.get("rows", []), country_group)
    except Exception as e:
        print(f"  ⚠️ country×page 拉取失败，分区页面将回退全站 Top: {e}")

    ym_key = report_ym or end[:7]
    ix = fetch_indexing_bundle(
        search, SITE, start, end, svc, TRIDENT, OUT_DIR, ym_key,
        use_cache=not refresh_indexing,
    )
    pages = ix["top_pages"]

    total_cl = sum(k["clicks"] for k in keywords)
    total_impr = sum(k["impr"] for k in keywords)
    brand_kw, nb_kw = partition_keywords(keywords)

    res = {
        "_range": f"{start}~{end}", "_label": label,
        "keywords": keywords, "countries": countries, "pages": pages,
        "region_top_keywords": {g: sorted(v, key=lambda x: x["clicks"], reverse=True)[:5] for g, v in region_kw.items()},
        "region_stats": rq["region_stats"],
        "region_brand_top": rq["region_brand_top"],
        "region_nonbrand_top": rq["region_nonbrand_top"],
        "region_pages": region_pages,
        "total_clicks": total_cl, "total_impr": total_impr,
        "avg_ctr": round(total_cl/total_impr*100,1) if total_impr else 0,
        "avg_pos": round(sum(k["pos"] for k in keywords)/len(keywords),1) if keywords else 0,
        "keyword_count": len(keywords),
        "brand_kw": brand_kw, "nonbrand_kw": nb_kw,
        "pages_with_traffic": ix["pages_with_traffic"],
        "indexing_corpus_total": ix["indexing_corpus_total"],
        "index_rate_primary": ix["index_rate_primary"],
        "sitemap_submitted": ix["sitemap_submitted"],
        "sitemap_indexed": ix.get("sitemap_indexed", 0),
        "sitemap_index_rate": ix.get("sitemap_index_rate"),
        "index_pages": ix["pages_with_traffic"],
        "index_rate": ix["index_rate_primary"],
    }
    print(
        f"📊 GSC {label}: {res['keyword_count']:,} keywords, {total_cl:,} clicks, {total_impr:,} impr | "
        f"有曝光URL={ix['pages_with_traffic']:,} 收录率={ix['index_rate_primary']}% (语料库{ix['indexing_corpus_total']:,})"
    )
    return res


# ============================================================
# 2. GA4
# ============================================================
def fetch_ga4_full(start, end, label):
    from google.oauth2.credentials import Credentials
    from googleapiclient.discovery import build
    token = json.loads(_cred_file("ga4-token.json").read_text())
    creds = Credentials.from_authorized_user_info(token, ["https://www.googleapis.com/auth/analytics.readonly"])
    svc = build("analyticsdata", "v1beta", credentials=creds)
    sf = {"filter": {"fieldName":"streamId", "stringFilter":{"matchType":"EXACT","value":STREAM}}}
    org_f = {"filter": {"fieldName":"sessionDefaultChannelGroup", "stringFilter":{"matchType":"EXACT","value":"Organic Search"}}}
    
    def run(dims, metrics, limit=50, extra=None):
        body = {"dateRanges":[{"startDate":start,"endDate":end}],"dimensions":[{"name":d} for d in dims],
                "metrics":[{"name":m} for m in metrics],"limit":limit,"dimensionFilter":sf}
        if extra: body["dimensionFilter"] = {"andGroup":{"expressions":[sf]+extra}}
        resp = svc.properties().runReport(property=PROPERTY, body=body).execute()
        rows = []
        for rw in resp.get("rows",[]):
            rows.append({"dims":{d:rw["dimensionValues"][i]["value"] for i,d in enumerate(dims)},
                         "metrics":{m:rw["metricValues"][i]["value"] for i,m in enumerate(metrics)}})
        return rows
    
    organic = run(["date"],["sessions","totalUsers","newUsers","averageSessionDuration","screenPageViewsPerSession","bounceRate"],limit=62,extra=[org_f])
    ts = sum(int(r["metrics"]["sessions"]) for r in organic)
    tu = sum(int(r["metrics"]["totalUsers"]) for r in organic)
    tn = sum(int(r["metrics"]["newUsers"]) for r in organic)
    td = sum(float(r["metrics"]["averageSessionDuration"]) for r in organic) / len(organic) if organic else 0
    tp = sum(float(r["metrics"]["screenPageViewsPerSession"]) for r in organic) / len(organic) if organic else 0
    tb = sum(float(r["metrics"]["bounceRate"])*int(r["metrics"]["sessions"]) for r in organic) / ts * 100 if ts else 0
    
    ch = run(["sessionDefaultChannelGroup"],["sessions","totalUsers","bounceRate","averageSessionDuration"],limit=10)
    t_all = sum(int(r["metrics"]["sessions"]) for r in ch)
    ch_data = {r["dims"]["sessionDefaultChannelGroup"]: {"sessions":int(r["metrics"]["sessions"]),"users":int(r["metrics"]["totalUsers"]),"bounce":round(float(r["metrics"]["bounceRate"])*100,1),"share":round(int(r["metrics"]["sessions"])/t_all*100,1)} for r in ch}
    
    segments = run(["newVsReturning"],["sessions","averageSessionDuration","screenPageViewsPerSession","bounceRate"],extra=[org_f])
    seg_data = {}
    for r in segments:
        t = r["dims"]["newVsReturning"]
        seg_data[t] = {"sessions":int(r["metrics"]["sessions"]),"dur":round(float(r["metrics"]["averageSessionDuration"])),"pages":round(float(r["metrics"]["screenPageViewsPerSession"]),1),"bounce":round(float(r["metrics"]["bounceRate"])*100,1)}
    
    geo = run(["country"],["sessions","totalUsers","newUsers","averageSessionDuration","screenPageViewsPerSession","bounceRate"],limit=30,extra=[org_f])
    geo_data = [{"country":r["dims"]["country"],"sessions":int(r["metrics"]["sessions"]),"users":int(r["metrics"]["totalUsers"]),"new_users":int(r["metrics"]["newUsers"]),"dur":round(float(r["metrics"]["averageSessionDuration"])),"pages":round(float(r["metrics"]["screenPageViewsPerSession"]),1),"bounce":round(float(r["metrics"]["bounceRate"])*100,1)} for r in geo]

    # Organic Search 按来源引擎拆分（google / bing / 其他）
    def _eng(s):
        s = (s or "").lower()
        if "google" in s: return "google"
        if "bing" in s: return "bing"
        if "yahoo" in s: return "yahoo"
        if "duckduckgo" in s: return "duckduckgo"
        return "其他"
    src = run(["sessionSource"],["sessions","totalUsers","newUsers","averageSessionDuration","bounceRate"],limit=80,extra=[org_f])
    osrc = {}
    for r in src:
        e = _eng(r["dims"]["sessionSource"])
        se = int(r["metrics"]["sessions"])
        d = osrc.setdefault(e, {"sessions":0,"users":0,"new_users":0,"_bw":0.0,"_dw":0.0})
        d["sessions"] += se; d["users"] += int(r["metrics"]["totalUsers"]); d["new_users"] += int(r["metrics"]["newUsers"])
        d["_bw"] += float(r["metrics"]["bounceRate"])*se; d["_dw"] += float(r["metrics"]["averageSessionDuration"])*se
    for e, d in osrc.items():
        se = d["sessions"] or 1
        d["bounce"] = round(d.pop("_bw")/se*100,1); d["dur"] = round(d.pop("_dw")/se)
        d["share"] = round(d["sessions"]/ts*100,1) if ts else 0

    bing_region = defaultdict(lambda: {"sessions": 0, "users": 0, "new_users": 0, "_bw": 0.0, "_dw": 0.0})
    cs_rows = run(
        ["country", "sessionSource"],
        ["sessions", "totalUsers", "newUsers", "averageSessionDuration", "bounceRate"],
        limit=500, extra=[org_f],
    )
    for r in cs_rows:
        if _eng(r["dims"]["sessionSource"]) != "bing":
            continue
        grp = country_group(r["dims"]["country"])
        se = int(r["metrics"]["sessions"])
        d = bing_region[grp]
        d["sessions"] += se
        d["users"] += int(r["metrics"]["totalUsers"])
        d["new_users"] += int(r["metrics"]["newUsers"])
        d["_bw"] += float(r["metrics"]["bounceRate"]) * se
        d["_dw"] += float(r["metrics"]["averageSessionDuration"]) * se
    for d in bing_region.values():
        se = d["sessions"] or 1
        d["bounce"] = round(d.pop("_bw") / se * 100, 1)
        d["dur"] = round(d.pop("_dw") / se)

    res = {
        "_label": label,
        "sessions": ts, "users": tu, "new_users": tn, "return_users": tu-tn,
        "new_user_pct": round(tn/tu*100,1) if tu else 0,
        "avg_dur": round(td), "pages_per_session": round(tp,2),
        "bounce": round(tb,1),
        "channels": ch_data, "segments": seg_data, "geo": geo_data,
        "organic_sources": osrc,
        "bing_region_ga4": dict(bing_region),
    }
    org_share = ch_data.get("Organic Search",{}).get("share",0)
    print(f"📊 GA4 {label}: sessions={ts:,} users={tu:,} new={tn:,} dur={round(td)}s pages={round(tp,2)} bounce={round(tb,1)}% | organic share={org_share}%")
    return res


# ============================================================
# 3. Keyword tiers from 5K
# ============================================================
def compute_tiers(keywords, brand_kw, nonbrand_kw, tiers=[3,5,10,30,50,100]):
    total_cl = sum(k["clicks"] for k in keywords)
    total_impr = sum(k["impr"] for k in keywords)
    by_clicks = sorted(keywords, key=lambda x: x["clicks"], reverse=True)
    result = {"_total_clicks": total_cl, "_total_impr": total_impr}
    for t in tiers:
        top = by_clicks[:t]
        c = sum(k["clicks"] for k in top)
        i = sum(k["impr"] for k in top)
        result[f"Top{t}"] = {"count": t, "clicks": c, "impr": i, "ctr": round(c/i*100,1) if i else 0, "share": round(c/total_cl*100,1) if total_cl else 0}
    
    def kw_sum(rows):
        c = sum(k["clicks"] for k in rows)
        i = sum(k["impr"] for k in rows)
        return {"count": len(rows), "clicks": c, "impr": i, "ctr": round(c/i*100,1) if i else 0, "share": round(c/total_cl*100,1) if total_cl else 0}
    result["品牌词"] = kw_sum(brand_kw)
    result["非品牌词"] = kw_sum(nonbrand_kw)
    return result


# ============================================================
# 4. Competitor matching
# ============================================================
def match_competitors(nonbrand_kw):
    comp_json = TRIDENT / "reports" / "competitor_keywords.json"
    comp_data = json.loads(comp_json.read_text())
    comp_full = [k for k in comp_data["keywords"] if len(k)>=3]
    comp_core = [k for k in comp_data["core_keywords"] if len(k)>=3]
    
    full_matched, core_matched, matched_comps = [], [], set()
    for gk in nonbrand_kw:
        gql = gk["q"].lower()
        f_c = set(); c_c = set()
        for ck in comp_full:
            if ck in gql: f_c.add(ck)
        for ck in comp_core:
            if ck in gql: c_c.add(ck)
        if f_c:
            full_matched.append({**gk, "comps": sorted(f_c)})
            matched_comps.update(f_c)
        if c_c:
            core_matched.append({**gk, "comps": sorted(c_c)})
    
    # Top 10/50/100
    def tier_matched(lst, n):
        top = lst[:n]
        return {"count": len(top), "clicks": sum(k["clicks"] for k in top), "comps": len(set(c for k in top for c in k["comps"]))}
    
    nb_clicks = sum(k["clicks"] for k in nonbrand_kw)
    fm_clicks = sum(k["clicks"] for k in full_matched)
    return {
        "full_match": len(full_matched),"core_match": len(core_matched),
        "unique_full": len(matched_comps), "unique_core": len(set(c for m in core_matched for c in m["comps"])),
        "full_rate": round(len(matched_comps)/len(comp_full)*100,1), "core_rate": round(len(set(c for m in core_matched for c in m["comps"]))/len(comp_core)*100,1),
        "click_share": round(fm_clicks / nb_clicks * 100, 1) if nb_clicks else 0,
        "tier_full": {"top10": tier_matched(full_matched,10), "top50": tier_matched(full_matched,50), "top100": tier_matched(full_matched,100)},
        "tier_core": {"top10": tier_matched(core_matched,10), "top50": tier_matched(core_matched,50), "top100": tier_matched(core_matched,100)},
        "matched_full_detail": full_matched[:40], "matched_core_detail": core_matched[:30],
        "missing_core": [c for c in comp_core if c not in set(c for m in core_matched for c in m["comps"])],
        "comp_total": len(comp_full), "core_total": len(comp_core),
    }


# ============================================================
# 5. Page directory analysis
# ============================================================
def page_dir_analysis(pages):
    dirs = defaultdict(lambda: {"clicks":0,"impr":0,"count":0})
    for p in pages:
        d = classify_page(p["url"])
        dirs[d]["clicks"] += p["clicks"]
        dirs[d]["impr"] += p["impr"]
        dirs[d]["count"] += 1
    return dict(sorted(dirs.items(), key=lambda x: x[1]["clicks"], reverse=True))


def build_bing_bundle(bing_data: dict, ym: str) -> dict:
    """把 bing-full.json 的某月切片加工成与 GSC 同构的结构（复用品牌/竞品/目录口径）。"""
    km = bing_data.get("keywords_monthly", {}).get(ym, [])
    pm = bing_data.get("pages_monthly", {}).get(ym, [])
    tmo = bing_data.get("traffic_monthly", {}).get(ym, {})
    brand_kw, nb_kw = partition_keywords(km)
    tiers = compute_tiers(km, brand_kw, nb_kw)
    comp = match_competitors(nb_kw) if nb_kw else None
    pdirs = page_dir_analysis(pm) if pm else {}
    return {
        "keywords": km, "pages": pm,
        "brand_kw": brand_kw, "nonbrand_kw": nb_kw,
        "tiers": tiers, "comp": comp, "pdirs": pdirs,
        "total_clicks": sum(k["clicks"] for k in km),
        "total_impr": sum(k["impr"] for k in km),
        "kw_count": len(km),
        "site_clicks": tmo.get("clicks"), "site_impr": tmo.get("impressions"), "site_ctr": tmo.get("ctr"),
    }


def lang_type_rollups(pdirs):
    """聚合：首页 / 语言首页合计 / i18n内页合计 / 各语言首页。"""
    roll = defaultdict(lambda: {"clicks": 0, "impr": 0})
    for d, v in pdirs.items():
        if d == "首页":
            roll["首页"]["clicks"] += v["clicks"]
            roll["首页"]["impr"] += v["impr"]
        elif d.startswith("语言首页-"):
            roll["语言首页合计"]["clicks"] += v["clicks"]
            roll["语言首页合计"]["impr"] += v["impr"]
            roll[d]["clicks"] += v["clicks"]
            roll[d]["impr"] += v["impr"]
        elif d.startswith("i18n内页-"):
            roll["i18n内页合计"]["clicks"] += v["clicks"]
            roll["i18n内页合计"]["impr"] += v["impr"]
    return dict(roll)


BING_FETCH_SCRIPT = _SCRIPT_DIR / "sentinel" / "bing_credentials" / "bing_fetch.py"
BING_FULL_JSON = TRIDENT / "reports" / "bing-full.json"


def ensure_bing_full(report_ym: str, max_age_days: int = 7) -> None:
    """月报前检测 bing-full.json；过期或缺当月数据则自动跑 bing_fetch.py。"""
    need = False
    if not BING_FULL_JSON.exists():
        need = True
    else:
        age_days = (datetime.datetime.now().timestamp() - BING_FULL_JSON.stat().st_mtime) / 86400
        if age_days > max_age_days:
            need = True
        else:
            try:
                data = json.loads(BING_FULL_JSON.read_text())
                if report_ym not in data.get("keywords_monthly", {}):
                    need = True
            except Exception:
                need = True
    if not need:
        return
    print("\n[0/4] Bing 数据过期或缺失，运行 bing_fetch.py...")
    import subprocess
    subprocess.run([sys.executable, str(BING_FETCH_SCRIPT)], check=True, cwd=BING_FETCH_SCRIPT.parent)


def ga4_needs_bing_refresh(ga4: dict | None) -> bool:
    if not ga4:
        return True
    return not ga4.get("organic_sources") or ga4.get("bing_region_ga4") is None


# ============================================================
# 6. Report generation
# ============================================================
def generate_report(
    g_prev, g_curr, ga4_prev, ga4_curr, comp_prev, comp_curr,
    pdirs_prev, pdirs_curr, meta: dict, hist: dict | None = None,
    sgeo_prev: dict | None = None, sgeo_curr: dict | None = None,
    bing_prev_override: dict | None = None,
    bing_curr_override: dict | None = None,
):
    pl, cl = meta["prev_label"], meta["curr_label"]
    ty, period = meta["title_year_month"], meta["period_line"]
    footer_gsc = meta["footer_gsc"]
    hist = hist or {}

    try:
        bing_data = json.loads((TRIDENT / "reports" / "bing-full.json").read_text())
    except Exception:
        bing_data = {}
    bing_curr = bing_curr_override if bing_curr_override is not None else build_bing_bundle(bing_data, meta["report_ym"])
    bing_prev = bing_prev_override if bing_prev_override is not None else build_bing_bundle(bing_data, meta["prev_start"][:7])
    bing_in_index = None
    try:
        crawl = bing_data.get("crawl_daily") or []
        if crawl:
            ix = crawl[-1].get("InIndex")
            bing_in_index = int(ix) if ix not in (None, "N/A", "") else None
    except (TypeError, ValueError):
        bing_in_index = None

    def trend_word(prev_val, curr_val):
        return "下滑" if curr_val < prev_val else ("增长" if curr_val > prev_val else "持平")

    def tiers_table(t_prev, t_curr, tier_names):
        lines = []
        for n in tier_names:
            ta = t_prev[f"Top{n}"]; tm = t_curr[f"Top{n}"]
            a_c, m_c = ta["clicks"], tm["clicks"]
            lines.append(f"| Top {n} | {ta['count']} | {ta['clicks']:,} | {ta['share']}% | {ta['ctr']}% | → | {tm['count']} | {tm['clicks']:,} | {tm['share']}% | {tm['ctr']}% | {chg_str(a_c, m_c)} |")
        return "\n".join(lines)
    
    # Brand/NonBrand
    b_prev = g_prev["tiers"]["品牌词"]; b_curr = g_curr["tiers"]["品牌词"]
    nb_prev = g_prev["tiers"]["非品牌词"]; nb_curr = g_curr["tiers"]["非品牌词"]

    org_share_prev = ga4_prev["channels"].get("Organic Search", {}).get("share", 0)
    org_share_curr = ga4_curr["channels"].get("Organic Search", {}).get("share", 0)
    gsc_trend = trend_word(g_prev["total_clicks"], g_curr["total_clicks"])
    org_share_trend = (
        "升至" if org_share_curr > org_share_prev
        else ("降至" if org_share_curr < org_share_prev else "持平")
    )
    
    # Region grouping
    def group_regions(countries):
        grps = defaultdict(lambda: {"clicks":0,"impr":0,"count":0})
        for c in countries:
            g = country_group(c["country"])
            grps[g]["clicks"] += c["clicks"]
            grps[g]["impr"] += c["impr"]
            grps[g]["count"] += 1
        return grps
    
    def group_ga4_regions(geo):
        grps = defaultdict(lambda: {"sessions":0,"users":0,"new":0})
        for g in geo:
            grp = country_group(g["country"])
            grps[grp]["sessions"] += g["sessions"]
            grps[grp]["users"] += g["users"]
            grps[grp]["new"] += g["new_users"]
        return grps
    
    reg_prev = {g: {"clicks": v["clicks"], "impr": v["impr"]} for g, v in g_prev.get("region_stats", {}).items()}
    reg_curr = {g: {"clicks": v["clicks"], "impr": v["impr"]} for g, v in g_curr.get("region_stats", {}).items()}
    if not reg_prev:
        reg_prev = group_regions(g_prev["countries"])
    if not reg_curr:
        reg_curr = group_regions(g_curr["countries"])
    reg_ga4_prev = group_ga4_regions(ga4_prev["geo"])
    reg_ga4_curr = group_ga4_regions(ga4_curr["geo"])
    reg_bing_prev = ga4_prev.get("bing_region_ga4") or {}
    reg_bing_curr = ga4_curr.get("bing_region_ga4") or {}
    rs_prev = g_prev.get("region_stats", {})
    rs_curr = g_curr.get("region_stats", {})
    total_reg_cl_prev = sum(v["clicks"] for v in reg_prev.values()) or g_prev["total_clicks"]
    total_reg_im_prev = sum(v["impr"] for v in reg_prev.values()) or g_prev["total_impr"]
    total_reg_cl_curr = sum(v["clicks"] for v in reg_curr.values()) or g_curr["total_clicks"]
    total_reg_im_curr = sum(v["impr"] for v in reg_curr.values()) or g_curr["total_impr"]
    total_pc_prev = sum(v["clicks"] for v in pdirs_prev.values()) or 1
    total_pc_curr = sum(v["clicks"] for v in pdirs_curr.values()) or 1
    total_pi_prev = sum(v["impr"] for v in pdirs_prev.values()) or 1
    total_pi_curr = sum(v["impr"] for v in pdirs_curr.values()) or 1
    lang_prev = lang_type_rollups(pdirs_prev)
    lang_curr = lang_type_rollups(pdirs_curr)

    def an(metric, val, digits=0):
        return annual_note(hist, metric, val, digits=digits)

    home_curr = pdirs_curr.get("首页", {"clicks": 0})
    content_cl = sum(pdirs_curr.get(d, {}).get("clicks", 0) for d in ["tools", "features", "blog"])
    top_region = max(reg_curr, key=lambda x: reg_curr.get(x, {}).get("clicks", 0), default="其他")
    m_br = sorted(g_curr["brand_kw"], key=lambda x: x["clicks"], reverse=True)[:3]
    brand_top3 = " / ".join(k["q"] for k in m_br)
    nb_pages = sorted(
        [(d, v["clicks"]) for d, v in pdirs_curr.items() if d not in ("首页", "other") and v["clicks"] > 0],
        key=lambda x: x[1], reverse=True,
    )
    _tm = okr_traffic_metrics(ga4_prev, ga4_curr, sgeo_prev, sgeo_curr)
    o1 = pct_str(_tm["uv_c"], 960_000)
    o3 = pct_str(_tm["ref_uv_c"], 360_000)
    region_summary_md = render_region_executive_summary(
        REGION_ORDER, reg_prev, reg_curr, rs_prev, rs_curr,
        reg_ga4_prev, reg_ga4_curr, pl, cl, chg_str, brief=True,
    ).strip()
    corpus = g_curr.get("indexing_corpus_total", 20_000)
    pwt = g_curr.get("pages_with_traffic", g_curr.get("index_pages", 0))
    pwt_prev = g_prev.get("pages_with_traffic", g_prev.get("index_pages", 0))
    index_rate_prev = g_prev.get("index_rate", g_prev.get("index_rate_primary", 0))
    index_rate_curr = g_curr.get("index_rate", g_curr.get("index_rate_primary", 0))
    index_gap = max(0, corpus - pwt)
    core_ctx = {
        "b_share": b_curr["share"],
        "b_share_chg": share_pp_chg(b_prev["share"], b_curr["share"]),
        "nb_share": nb_curr["share"],
        "top3_share": g_curr["tiers"]["Top3"]["share"],
        "top10_share": g_curr["tiers"]["Top10"]["share"],
        "top10_clicks_chg": chg_str(g_prev["tiers"]["Top10"]["clicks"], g_curr["tiers"]["Top10"]["clicks"]),
        "top3_clicks_chg": chg_str(g_prev["tiers"]["Top3"]["clicks"], g_curr["tiers"]["Top3"]["clicks"]),
        "gsc_clicks_chg": chg_str(g_prev["total_clicks"], g_curr["total_clicks"]),
        "gsc_impr_chg": chg_str(g_prev["total_impr"], g_curr["total_impr"]),
        "gsc_ctr_chg": chg_f(g_prev["avg_ctr"], g_curr["avg_ctr"]),
        "nb_impr_chg": chg_str(nb_prev["impr"], nb_curr["impr"]),
        "home_clicks": home_curr["clicks"],
        "home_share": round(home_curr["clicks"] / total_pc_curr * 100, 1),
        "content_clicks": content_cl,
        "content_clicks_chg": chg_str(
            sum(pdirs_prev.get(d, {}).get("clicks", 0) for d in ["tools", "features", "blog"]),
            content_cl,
        ),
        "top_nb_pages": [d for d, _ in nb_pages[:5]],
        "brand_top3": brand_top3,
        "missing_core": comp_curr["missing_core"],
        "ga4_sess_chg": chg_str(ga4_prev["sessions"], ga4_curr["sessions"]),
        "org_share_prev": org_share_prev,
        "org_share_curr": org_share_curr,
        "bounce": ga4_curr["bounce"],
        "pages": ga4_curr["pages_per_session"],
        "core_rate": comp_curr["core_rate"],
        "unique_core": comp_curr["unique_core"],
        "core_total": comp_curr["core_total"],
        "comp_click_share": comp_curr["click_share"],
        "index_rate": index_rate_curr,
        "index_rate_prev": index_rate_prev,
        "index_rate_pp": share_pp_chg(index_rate_prev, index_rate_curr),
        "pwt_prev": pwt_prev,
        "index_pwt_chg": chg_str(pwt_prev, pwt),
        "pages_with_traffic": pwt,
        "content_inventory": load_content_inventory(),
        "corpus": corpus,
        "index_gap": index_gap,
        "index_pages": pwt,
        "sitemap": g_curr.get("sitemap_submitted", 0),
        "top_region": top_region,
        "top_region_clicks": reg_curr.get(top_region, {}).get("clicks", 0),
        "okr_o1_pct": o1,
        "okr_o3_pct": o3,
        "region_summary": region_summary_md or "见 §8.0 大区总览。",
    }
    enrich_core_ctx_with_product(core_ctx, sgeo_prev, sgeo_curr, chg_str)
    enrich_core_ctx_with_platforms(core_ctx, sgeo_curr)
    enrich_core_ctx_with_bing(core_ctx, bing_prev, bing_curr, ga4_curr, chg_str)
    core_ctx["gsc_clicks_curr"] = g_curr["total_clicks"]
    if bing_curr.get("keywords") and g_curr.get("keywords"):
        gm = {k["q"].lower() for k in g_curr["keywords"]}
        bm = {k["q"].lower() for k in bing_curr["keywords"]}
        core_ctx["cross_engine_count"] = len(gm & bm)

    # ========== BUILD REPORT ==========
    heading = meta.get("report_heading") or f"Lovart SEO 月度复盘报告 — {ty}"
    perspective = meta.get("perspective_line")
    perspective_line = f"> **视角**: {perspective}  \n" if perspective else ""
    rep = f"""# {heading}

> **周期**: {period} ｜ **生成**: {datetime.date.today().isoformat()}  
{perspective_line}> **数据源**: Google Search Console (5,000 词) + Google Analytics 4 + Bing Webmaster Tools  
> **竞品词库**: 265 全量 / 36 核心 (来自 `竞品核心非品牌词/`)

---

{render_core_insights(core_ctx)}
---

{render_okr_section(ga4_curr, ga4_prev, pl, cl, chg_str, sgeo_prev, sgeo_curr)}
---

{render_executive_dashboards(g_prev, g_curr, ga4_prev, ga4_curr, comp_prev, comp_curr, pl, cl, chg_str, chg_f, b_prev, b_curr, nb_prev, nb_curr, sgeo_prev, sgeo_curr, bing_prev, bing_curr, bing_in_index)}

---

## 四、关键词分层明细

{render_engine_overview(g_prev, g_curr, bing_prev, bing_curr, pl, cl, chg_str)}### 4.1 Top N 分层 (点击 / 曝光 / CTR 全维) — Google (GSC)

| 分层 | {pl} 词数 | {pl} 点击 | {pl} 曝光 | {pl} 占比 | {pl} CTR | → | {cl} 词数 | {cl} 点击 | {cl} 曝光 | {cl} 占比 | {cl} CTR | 点击环比 | 曝光环比 | CTR环比 |
|------|----------|----------|----------|----------|---------|---|----------|----------|----------|----------|---------|----------|----------|---------|
{tiers_table_full(g_prev['tiers'], g_curr['tiers'], [3,5,10,30,50,100], pl, cl, chg_str, chg_f)}

### 4.2 品牌词 Top 10（Google）

| # | {pl} | {pl} 点击 | → | {cl} | {cl} 点击 | 环比变化 |
|---|-----|----------|---|-----|----------|----------|
"""
    a_br_sorted = sorted(g_prev["brand_kw"], key=lambda x: x["clicks"], reverse=True)
    m_br_sorted = sorted(g_curr["brand_kw"], key=lambda x: x["clicks"], reverse=True)
    for i in range(10):
        ak = a_br_sorted[i] if i<len(a_br_sorted) else {'q':'','clicks':0}
        mk = m_br_sorted[i] if i<len(m_br_sorted) else {'q':'','clicks':0}
        rep += f"| {i+1} | {ak['q'][:22]} | {ak['clicks']:,} | → | {mk['q'][:22]} | {mk['clicks']:,} | {chg_str(ak['clicks'], mk['clicks'])} |\n"
    
    rep += f"""
### 4.3 非品牌词 Top 10（Google）

| # | {pl} | {pl} 点击 | → | {cl} | {cl} 点击 | 环比变化 |
|---|-----|----------|---|-----|----------|----------|
"""
    a_nb_sorted = sorted(g_prev["nonbrand_kw"], key=lambda x: x["clicks"], reverse=True)
    m_nb_sorted = sorted(g_curr["nonbrand_kw"], key=lambda x: x["clicks"], reverse=True)
    for i in range(10):
        ak = a_nb_sorted[i] if i<len(a_nb_sorted) else {'q':'','clicks':0}
        mk = m_nb_sorted[i] if i<len(m_nb_sorted) else {'q':'','clicks':0}
        rep += f"| {i+1} | {ak['q'][:22]} | {ak['clicks']:,} | → | {mk['q'][:22]} | {mk['clicks']:,} | {chg_str(ak['clicks'], mk['clicks'])} |\n"

    rep += render_movers_section(g_prev, g_curr, pl, cl, chg_str, 15)
    rep += render_bing_keyword_block(bing_prev, bing_curr, pl, cl, chg_str, chg_f)
    rep += render_cross_engine_keyword_overlap(g_curr, bing_curr, pl, cl)
    rep += render_engine_compare_kw(g_curr, b_curr, bing_curr)
    rep += section_insight_keywords(g_prev, g_curr, chg_str, bing_curr).replace(
        "<!--ANNUAL:keywords-->", an("gsc_clicks", g_curr["total_clicks"])
    )

    # Section 3: GA4 detail
    rep += f"""
---

## 五、自然搜索用户数据（GA4）

### 5.1 核心用户指标

| 指标 | {pl} | {cl} | 环比变化 |
|------|-----|-----|----------|
| Sessions | {ga4_prev['sessions']:,} | {ga4_curr['sessions']:,} | {chg_str(ga4_prev['sessions'], ga4_curr['sessions'])} |
| Users | {ga4_prev['users']:,} | {ga4_curr['users']:,} | {chg_str(ga4_prev['users'], ga4_curr['users'])} |
| New Users | {ga4_prev['new_users']:,} | {ga4_curr['new_users']:,} | {chg_str(ga4_prev['new_users'], ga4_curr['new_users'])} |
| Return Users | {ga4_prev['return_users']:,} | {ga4_curr['return_users']:,} | {chg_str(ga4_prev['return_users'], ga4_curr['return_users'])} |
| 新用户占比 | {ga4_prev['new_user_pct']}% | {ga4_curr['new_user_pct']}% | {chg_f(ga4_prev['new_user_pct'], ga4_curr['new_user_pct'])}% |
| 平均停留时长 | {ga4_prev['avg_dur']}s | {ga4_curr['avg_dur']}s | {chg_str(ga4_prev['avg_dur'], ga4_curr['avg_dur'])} |
| 页/次 | {ga4_prev['pages_per_session']} | {ga4_curr['pages_per_session']} | {chg_f(ga4_prev['pages_per_session'], ga4_curr['pages_per_session'])} |
| 跳出率 | {ga4_prev['bounce']}% | {ga4_curr['bounce']}% | {chg_f(ga4_prev['bounce'], ga4_curr['bounce'])}% |

### 5.2 新老用户分层 (Organic Search)

| 类型 | {pl} Sessions | {pl} 时长 | {pl} 跳出 | → | {cl} Sessions | {cl} 时长 | {cl} 跳出 |
|------|-------------|----------|----------|---|-------------|----------|----------|
| New | {ga4_prev['segments'].get('new',{}).get('sessions',0):,} | {ga4_prev['segments'].get('new',{}).get('dur',0)}s | {ga4_prev['segments'].get('new',{}).get('bounce',0)}% | → | {ga4_curr['segments'].get('new',{}).get('sessions',0):,} | {ga4_curr['segments'].get('new',{}).get('dur',0)}s | {ga4_curr['segments'].get('new',{}).get('bounce',0)}% |
| Returning | {ga4_prev['segments'].get('returning',{}).get('sessions',0):,} | {ga4_prev['segments'].get('returning',{}).get('dur',0)}s | {ga4_prev['segments'].get('returning',{}).get('bounce',0)}% | → | {ga4_curr['segments'].get('returning',{}).get('sessions',0):,} | {ga4_curr['segments'].get('returning',{}).get('dur',0)}s | {ga4_curr['segments'].get('returning',{}).get('bounce',0)}% |

### 5.3 全渠道 Sessions 占比

| 渠道 | {pl} Sessions | {pl} 占比 | → | {cl} Sessions | {cl} 占比 | 占比变化 |
|------|-------------|----------|---|-------------|----------|----------|
"""
    for ch in ga4_curr["channels"]:
        c4 = ga4_prev["channels"].get(ch, {})
        c5 = ga4_curr["channels"][ch]
        rep += f"| {ch} | {c4.get('sessions',0):,} | {c4.get('share',0)}% | → | {c5['sessions']:,} | {c5['share']}% | {c5['share']-c4.get('share',0):+.1f}% |\n"

    rep += render_ga4_engine_split(ga4_prev, ga4_curr, pl, cl, chg_str)
    rep += section_insight_ga4_with_product(ga4_curr, ga4_prev, chg_str, sgeo_curr).replace(
        "<!--ANNUAL:ga4_sessions-->", an("ga4_sessions", ga4_curr["sessions"])
    )
    rep += render_seo_geo_section(sgeo_prev, sgeo_curr, pl, cl, chg_str)

    # Section 4: Brand vs NonBrand
    rep += f"""
---

## 七、品牌词 vs 非品牌词

### 7A 品牌词 vs 非品牌词（Google · GSC）

| 维度 | {pl} | {cl} | 环比变化 |
|------|-----|-----|----------|
| 品牌词数量 | {b_prev['count']} | {b_curr['count']} | {chg_str(b_prev['count'], b_curr['count'])} |
| 品牌词点击 | {b_prev['clicks']:,} | {b_curr['clicks']:,} | {chg_str(b_prev['clicks'], b_curr['clicks'])} |
| 品牌词曝光 | {b_prev['impr']:,} | {b_curr['impr']:,} | {chg_str(b_prev['impr'], b_curr['impr'])} |
| 非品牌词数量 | {nb_prev['count']} | {nb_curr['count']} | {chg_str(nb_prev['count'], nb_curr['count'])} |
| 非品牌词点击 | {nb_prev['clicks']:,} | {nb_curr['clicks']:,} | {chg_str(nb_prev['clicks'], nb_curr['clicks'])} |
| 非品牌词曝光 | {nb_prev['impr']:,} | {nb_curr['impr']:,} | {chg_str(nb_prev['impr'], nb_curr['impr'])} |
| 品牌词点击占比 | {b_prev['share']}% | {b_curr['share']}% | {b_curr['share']-b_prev['share']:+.1f}% |
| 非品牌词点击占比 | {nb_prev['share']}% | {nb_curr['share']}% | {nb_curr['share']-nb_prev['share']:+.1f}% |

{section_insight_brand(b_prev, b_curr, nb_prev, nb_curr, bing_curr).replace('<!--ANNUAL:brand_share-->', an('brand_share', b_curr['share'], digits=1))}
"""
    rep += render_bing_brand_block(bing_prev, bing_curr, b_curr, nb_curr, pl, cl, chg_str, chg_f)

    # Section 5: Competitor
    rep += f"""---

## 八、竞品非品牌词覆盖

> 竞品词库: {comp_curr['comp_total']} 全量词 / {comp_curr['core_total']} 核心词 (来自 `竞品核心非品牌词/`)

### 8.1 总览

| 指标 | {pl} | {cl} | 变化 |
|------|-----|-----|------|
| Full 匹配 GSC 关键词 | {comp_prev["full_match"]} | {comp_curr["full_match"]} | {chg_str(comp_prev["full_match"], comp_curr["full_match"])} |
| Full 唯一竞品词 | {comp_prev["unique_full"]} | {comp_curr["unique_full"]} | {chg_str(comp_prev["unique_full"], comp_curr["unique_full"])} |
| Full 覆盖率 | {comp_prev["full_rate"]}% | {comp_curr["full_rate"]}% | {comp_curr["full_rate"]-comp_prev["full_rate"]:+.1f}% |
| Core 匹配 GSC 关键词 | {comp_prev["core_match"]} | {comp_curr["core_match"]} | {chg_str(comp_prev["core_match"], comp_curr["core_match"])} |
| Core 唯一竞品词 | {comp_prev["unique_core"]} | {comp_curr["unique_core"]} | {chg_str(comp_prev["unique_core"], comp_curr["unique_core"])} |
| Core 覆盖率 | {comp_prev["core_rate"]}% | {comp_curr["core_rate"]}% | {comp_curr["core_rate"]-comp_prev["core_rate"]:+.1f}% |
| 竞品词点击占非品牌比 | {comp_prev["click_share"]}% | {comp_curr["click_share"]}% | {comp_curr["click_share"]-comp_prev["click_share"]:+.1f}% |

### 8.2 分层表现 ({cl})

| 分层 | Full 命中词数 | Full Clicks | Core 命中词数 | Core Clicks | 竞品词去重数 |
|------|:-----------:|------------:|:-----------:|------------:|:----------:|
| Top 10 | {comp_curr['tier_full']['top10']['count']} | {comp_curr['tier_full']['top10']['clicks']:,} | {comp_curr['tier_core']['top10']['count']} | {comp_curr['tier_core']['top10']['clicks']:,} | {comp_curr['tier_full']['top10']['comps']} |
| Top 50 | {comp_curr['tier_full']['top50']['count']} | {comp_curr['tier_full']['top50']['clicks']:,} | {comp_curr['tier_core']['top50']['count']} | {comp_curr['tier_core']['top50']['clicks']:,} | {comp_curr['tier_full']['top50']['comps']} |
| Top 100 | {comp_curr['tier_full']['top100']['count']} | {comp_curr['tier_full']['top100']['clicks']:,} | {comp_curr['tier_core']['top100']['count']} | {comp_curr['tier_core']['top100']['clicks']:,} | {comp_curr['tier_full']['top100']['comps']} |

### 8.3 命中的核心竞品词明细 (Top 20)

| # | 竞品词 | 匹配的 GSC 关键词 | 点击 | 曝光 | CTR |
|---|--------|-----------------|------|------|-----|
"""
    core_seen = {}
    for m in comp_curr["matched_core_detail"]:
        for c in m["comps"]:
            if c not in core_seen or m["clicks"] > core_seen[c]["clicks"]:
                core_seen[c] = {"q":m["q"], "clicks":m["clicks"], "impr":m["impr"], "ctr":m["ctr"]}
    for i, (comp, d) in enumerate(sorted(core_seen.items(), key=lambda x: x[1]["clicks"], reverse=True)[:20]):
        rep += f"| {i+1} | {comp} | {d['q'][:35]} | {d['clicks']:,} | {d['impr']:,} | {d['ctr']}% |\n"

    rep += f"""
### 8.4 Full 匹配 Top 20

| # | GSC 关键词 | 命中竞品词 | 点击 | 曝光 | CTR | 排名 |
|---|-----------|-----------|------|------|-----|------|
"""
    for i, m in enumerate(comp_curr["matched_full_detail"][:20]):
        cs = ", ".join(m["comps"][:4])
        rep += f"| {i+1} | {m['q'][:30]} | {cs[:40]} | {m['clicks']:,} | {m['impr']:,} | {m['ctr']}% | {m['pos']} |\n"

    rep += f"""
### 8.5 未覆盖的核心竞品词 ({len(comp_curr['missing_core'])} 个)

以下高优先级词在 GSC 5,000 词中完全无排名:
"""
    for kw in comp_curr["missing_core"][:20]:
        rep += f"- {kw}\n"

    rep += section_insight_comp(comp_curr, bing_curr).replace(
        "<!--ANNUAL:comp_core_rate-->", an("comp_core_rate", comp_curr["core_rate"], digits=1)
    )
    rep += render_bing_competitor_detail(bing_prev, bing_curr, pl, cl, chg_str)
    rep += render_bing_competitor_block(bing_curr, comp_curr, chg_str)

    # Section 6: Page directory
    rep += f"""
---

## 九、页面目录流量

### 9.1 按目录（{pl} vs {cl} 环比）

| 目录 | {pl} 点击 | {pl} 曝光 | {pl} 点击占比 | {pl} 曝光占比 | → | {cl} 点击 | {cl} 曝光 | {cl} 点击占比 | {cl} 曝光占比 | 点击环比 | 曝光环比 |
|------|----------|----------|--------------|--------------|---|----------|----------|--------------|--------------|----------|----------|
"""
    all_dirs = sorted(set(pdirs_prev) | set(pdirs_curr), key=lambda d: pdirs_curr.get(d, pdirs_prev.get(d, {"clicks": 0}))["clicks"], reverse=True)
    for d in all_dirs[:20]:
        pv = pdirs_prev.get(d, {"clicks": 0, "impr": 0, "count": 0})
        cv = pdirs_curr.get(d, {"clicks": 0, "impr": 0, "count": 0})
        rep += (
            f"| {d} | {pv['clicks']:,} | {pv['impr']:,} | "
            f"{round(pv['clicks']/total_pc_prev*100,1)}% | {round(pv['impr']/total_pi_prev*100,1)}% | → | "
            f"{cv['clicks']:,} | {cv['impr']:,} | "
            f"{round(cv['clicks']/total_pc_curr*100,1)}% | {round(cv['impr']/total_pi_curr*100,1)}% | "
            f"{chg_str(pv['clicks'], cv['clicks'])} | {chg_str(pv['impr'], cv['impr'])} |\n"
        )

    target = ['features', 'tools', 'blog', 'news', 'docs', 'r', 'profile']
    rep += f"""
### 9.2 核心内容目录

| 目录 | {pl} 点击 | {pl} 曝光 | {cl} 点击 | {cl} 曝光 | 点击环比 | 曝光占比({cl}) |
|------|----------|----------|----------|----------|----------|----------------|
"""
    for d in target:
        pv = pdirs_prev.get(d, {"clicks": 0, "impr": 0})
        cv = pdirs_curr.get(d, {"clicks": 0, "impr": 0})
        rep += (
            f"| {d} | {pv['clicks']:,} | {pv['impr']:,} | {cv['clicks']:,} | {cv['impr']:,} | "
            f"{chg_str(pv['clicks'], cv['clicks'])} | {round(cv['impr']/total_pi_curr*100,1)}% |\n"
        )

    rep += f"""
### 9.3 多语言页面类型占比

| 类型 | {pl} 点击 | {pl} 曝光 | {pl} 点击占比 | → | {cl} 点击 | {cl} 曝光 | {cl} 点击占比 | 点击环比 |
|------|----------|----------|--------------|---|----------|----------|--------------|----------|
"""
    lang_types = ["首页", "语言首页合计", "i18n内页合计"]
    lang_types += sorted(k for k in lang_curr if k.startswith("语言首页-"))
    seen = set()
    for t in lang_types:
        if t in seen:
            continue
        seen.add(t)
        pv = lang_prev.get(t, {"clicks": 0, "impr": 0})
        cv = lang_curr.get(t, {"clicks": 0, "impr": 0})
        rep += (
            f"| {t} | {pv['clicks']:,} | {pv['impr']:,} | {round(pv['clicks']/total_pc_prev*100,1)}% | → | "
            f"{cv['clicks']:,} | {cv['impr']:,} | {round(cv['clicks']/total_pc_curr*100,1)}% | "
            f"{chg_str(pv['clicks'], cv['clicks'])} |\n"
        )

    rep += section_insight_pages(pdirs_curr, total_pc_curr, bing_curr).replace(
        "<!--ANNUAL:homepage_clicks-->", an("homepage_clicks", home_curr["clicks"])
    )
    rep += render_bing_pages_block(bing_prev, bing_curr, pl, cl, chg_str)

    # Section 7: Top pages
    rep += f"""
---

## 十、页面查询明细 (Top 20)

### 10A Google 页面查询明细 (Top 20 · GSC)

| # | URL | 点击 | 曝光 | CTR | 排名 |
|---|-----|------|------|-----|------|
"""
    for i, p in enumerate(g_curr["pages"][:20]):
        url_s = format_page_path(p["url"])[:55]
        rep += f"| {i+1} | {url_s} | {p['clicks']:,} | {p['impr']:,} | {p['ctr']}% | {p['pos']:.1f} |\n"
    rep += render_bing_top_pages(bing_prev, bing_curr, pl, cl, chg_str, 20)

    # Section 8: Region
    bing_sess_total = sum(v.get("sessions", 0) for v in reg_bing_curr.values())
    bing_sess_note = (
        f"Bing Sessions（GA4 近似）合计 **{bing_sess_total:,}**，详见 **§11.10**。"
        if bing_sess_total else "Bing 分地区见 **§11.10**（需 GA4 `country×sessionSource` 快照）。"
    )
    rep += f"""
---

## 十一、分地区表现（Google GSC + Bing GA4 近似）

> ⚠️ **Google**：GSC country×query/page 搜索词地区。**Bing**：Webmaster 无 geo → **§11.10** 用 GA4 `country × sessionSource(bing)` Sessions 行为近似（非搜索词地区）。{bing_sess_note}  
> 北美 = 美国 + 加拿大 + 英国 + 澳大利亚 + 新西兰  
> 大中华 = 中国大陆 + 香港 + 台湾 + **澳门**  
> 日本 = 日本  
> 拉美 / 南亚 / 中东非洲 = 见 AGENTS.md A2

{render_region_executive_summary(REGION_ORDER, reg_prev, reg_curr, rs_prev, rs_curr, reg_ga4_prev, reg_ga4_curr, pl, cl, chg_str)}
### 11.1 地区 GSC 汇总（{pl} vs {cl}）

| 地区 | {pl} 点击 | {pl} 曝光 | {pl} CTR | 点击占比 | 曝光占比 | → | {cl} 点击 | {cl} 曝光 | {cl} CTR | 点击占比 | 曝光占比 | 点击环比 | 曝光环比 |
|------|----------|----------|----------|----------|----------|---|----------|----------|----------|----------|----------|----------|----------|
"""
    for grp in REGION_ORDER:
        a = reg_prev.get(grp, {"clicks": 0, "impr": 1})
        m = reg_curr.get(grp, {"clicks": 0, "impr": 1})
        a_ctr = round(a["clicks"] / a["impr"] * 100, 1) if a["impr"] else 0
        m_ctr = round(m["clicks"] / m["impr"] * 100, 1) if m["impr"] else 0
        rep += (
            f"| {grp} | {a['clicks']:,} | {a['impr']:,} | {a_ctr}% | "
            f"{round(a['clicks']/total_reg_cl_prev*100,1)}% | {round(a['impr']/total_reg_im_prev*100,1)}% | → | "
            f"{m['clicks']:,} | {m['impr']:,} | {m_ctr}% | "
            f"{round(m['clicks']/total_reg_cl_curr*100,1)}% | {round(m['impr']/total_reg_im_curr*100,1)}% | "
            f"{chg_str(a['clicks'], m['clicks'])} | {chg_str(a['impr'], m['impr'])} |\n"
        )

    rep += f"""
### 11.1b 各地区品牌词 vs 非品牌词（GSC 点击/曝光）

| 地区 | {pl} 品牌点击 | {pl} 品牌曝光 | {pl} 非品牌点击 | {pl} 非品牌曝光 | → | {cl} 品牌点击 | {cl} 品牌曝光 | {cl} 非品牌点击 | {cl} 非品牌曝光 | 品牌点击环比 |
|------|-------------|-------------|---------------|---------------|---|-------------|-------------|---------------|---------------|-------------|
"""
    for grp in REGION_ORDER:
        sp = rs_prev.get(grp, {"brand": {"clicks": 0, "impr": 0}, "nonbrand": {"clicks": 0, "impr": 0}})
        sc = rs_curr.get(grp, {"brand": {"clicks": 0, "impr": 0}, "nonbrand": {"clicks": 0, "impr": 0}})
        pb, pnb = sp["brand"], sp["nonbrand"]
        cb, cnb = sc["brand"], sc["nonbrand"]
        rep += (
            f"| {grp} | {pb['clicks']:,} | {pb['impr']:,} | {pnb['clicks']:,} | {pnb['impr']:,} | → | "
            f"{cb['clicks']:,} | {cb['impr']:,} | {cnb['clicks']:,} | {cnb['impr']:,} | "
            f"{chg_str(pb['clicks'], cb['clicks'])} |\n"
        )

    rep += section_insight_region_summary()

    sec_idx = 2
    for grp in REGION_ORDER:
        bq = list(g_curr.get("region_brand_top", {}).get(grp, []))
        nq = [k for k in g_curr.get("region_nonbrand_top", {}).get(grp, []) if not is_brand(k["q"])]
        pages = g_curr.get("region_pages", {}).get(grp, [])
        if not pages:
            pages = g_curr.get("pages", [])[:10]
        if not bq and not nq and not pages:
            continue
        bq_prev = list(g_prev.get("region_brand_top", {}).get(grp, []))
        nq_prev = [k for k in g_prev.get("region_nonbrand_top", {}).get(grp, []) if not is_brand(k["q"])]
        pages_prev = g_prev.get("region_pages", {}).get(grp, [])
        rep += region_mini_block(
            grp, pl, cl,
            reg_prev, reg_curr, rs_prev, rs_curr,
            reg_ga4_prev, reg_ga4_curr,
            bq, nq, bq_prev, nq_prev,
            pages, pages_prev,
            total_reg_cl_prev, total_reg_cl_curr,
            total_reg_im_prev, total_reg_im_curr,
            chg_str, chg_f, format_page_path,
        ).replace("11.x", f"11.{sec_idx}")
        sec_idx += 1

    # GA4 region summary
    rep += f"""
### 11.9 地区 GA4 自然搜索（{pl} vs {cl}）

| 地区 | {pl} Sessions | {pl} Users | → | {cl} Sessions | {cl} Users | Sessions环比 |
|------|-------------|-----------|------|-------------|-----------|-------------|
"""
    for grp in REGION_ORDER:
        a = reg_ga4_prev.get(grp, {"sessions": 0, "users": 0})
        m = reg_ga4_curr.get(grp, {"sessions": 0, "users": 0})
        rep += f"| {grp} | {a['sessions']:,} | {a['users']:,} | → | {m['sessions']:,} | {m['users']:,} | {chg_str(a['sessions'], m['sessions'])} |\n"

    rep += render_bing_region_section(REGION_ORDER, reg_bing_prev, reg_bing_curr, pl, cl, chg_str)

    # Section 9: TODO
    rep += f"""
---

## 十二、TODO

| 优先级 | 行动项 | 数据依据 |
|--------|--------|----------|
| 🔴 P0 | 针对 {len(comp_curr['missing_core'])} 个缺失核心词建 landing page (ai logo generator, image to video, graphic design 等) | Core 覆盖率 {comp_curr['core_rate']}% |
| 🔴 P0 | 收录率（主口径）{g_curr.get('index_rate', g_curr.get('index_rate_primary', 0))}% — {g_curr.get('pages_with_traffic', g_curr.get('index_pages', 0)):,}/{g_curr.get('indexing_corpus_total', 20000):,} 有曝光 URL | 收录分析（非 rowLimit=1000÷sitemap） |
| 🔴 P0 | 品牌依赖 {b_curr['share']}%，非品牌内容生产线启动 | 品牌/非品牌拆分 |
| 🟠 P1 | /tools/ /features/ /blog/ 目录 SEO 优化 — 内容量大但搜索流量占比极低 | 页面目录分析 |
| 🟠 P1 | 北美市场 CTR {round(reg_curr.get('北美',{}).get('clicks',0)/reg_curr.get('北美',{}).get('impr',1)*100,1)}%，需提升排名质量 | 地区 CTR |
| 🟠 P1 | 新用户获取 — {cl} new {chg_str(ga4_prev['new_users'], ga4_curr['new_users'])} | GA4 新用户 |
| 🟠 P1 | 大中华区流量来源排查 — GA4 ({reg_ga4_curr.get('大中华',{}).get('sessions',0):,} sessions) vs GSC ({reg_curr.get('大中华',{}).get('clicks',0):,} clicks) 严重不对称 | 地区对比 |
| 🟡 P2 | 建立日/周/季/年多粒度看板 | 需求 #8 |

---

## 十三、Bing 补充数据（站点级 + 收录）

> 13.1 站点级月度流量来自 `GetRankAndTrafficStats` 日序列按月聚合；Bing **关键词/页面明细已并入 §四 / §九 / §十**（每周 top~100 词聚合为月度，含词位与环比）。13.2 为收录/爬取与全期结构参考。

"""
    bing = json.loads((TRIDENT / "reports" / "bing-full.json").read_text())
    bing_kw = bing.get("keywords", [])
    tm = bing.get("traffic_monthly", {})
    cur_m = meta["report_ym"]  # YYYY-MM
    prev_m = meta["prev_start"][:7]
    cur = tm.get(cur_m)
    prv = tm.get(prev_m)
    if cur:
        def _chg(p, c):
            if not p:
                return "—"
            d = c - p
            return f"{'↑+' if d >= 0 else '↓'}{d:,} / {d / p * 100:+.1f}%"
        rep += f"""### 13.1 Bing 月度流量（按月聚合 · 可比）

| 指标 | {prev_m} | {cur_m} | 环比 |
|------|----------|----------|------|
| 点击 | {(prv or {}).get('clicks', 0):,} | {cur['clicks']:,} | {_chg((prv or {}).get('clicks', 0), cur['clicks'])} |
| 曝光 | {(prv or {}).get('impressions', 0):,} | {cur['impressions']:,} | {_chg((prv or {}).get('impressions', 0), cur['impressions'])} |
| CTR | {(prv or {}).get('ctr', 0)}% | {cur['ctr']}% | {round(cur['ctr'] - (prv or {}).get('ctr', 0), 2):+}pp |

"""
    else:
        rep += f"> ⚠️ `traffic_monthly` 缺 {cur_m}，请重跑 `bing_fetch.py`（或该月尚无 Bing 数据）。\n\n"
    rep += f"""### 13.2 Bing 收录与全期结构参考

| 指标 | 值 |
|------|-----|
| 全期关键词（去重） | {len(bing_kw):,} |
| 全期总点击 | {sum(k['clicks'] for k in bing_kw):,} |
| 品牌词 | {sum(1 for k in bing_kw if is_brand(k.get('q',''))):,} 词 |
| 非品牌词 | {sum(1 for k in bing_kw if not is_brand(k.get('q',''))):,} 词 |
| 索引页数 | {bing.get('crawl_daily',[{}])[-1].get('InIndex','N/A'):,} |
| 日爬取量 | {bing.get('crawl_daily',[{}])[-1].get('CrawledPages','N/A'):,} |

---

> *本报告由 Lovart Trident Data Engine V2 生成*  
> *GSC: 5,000 关键词全量, {footer_gsc}*  
> *GA4: 同期全月*  
> *竞品词库: 265 全量 / 36 核心 (来自 1-2 Insight/Trident Insights/竞品核心非品牌词/)*
"""
    return rep


# ============================================================
# MAIN
# ============================================================
def run_monthly_report(
    report_ym: str,
    *,
    resume: bool = False,
    render_only: bool = False,
    snapshots_only: bool = False,
    refresh_indexing: bool = False,
    refresh_brand: bool = False,
) -> Path:
    meta = report_month_meta(report_ym)
    print_pre_run_checklist(
        "monthly",
        meta["period_line"].split(" vs ")[0].strip(),
        meta["period_line"].split(" vs ")[1].strip(),
        okr_effective=OKR_EFFECTIVE_MONTH,
    )
    print(f"  ℹ️  {okr_confirmation_reminder()}\n")
    ym_prev = meta["prev_start"][:7]

    g_curr = load_snapshot("gsc", report_ym) if resume or render_only else None
    g_prev = load_snapshot("gsc", ym_prev) if resume or render_only else None
    ga4_curr = load_snapshot("ga4", report_ym) if resume or render_only else None
    ga4_prev = load_snapshot("ga4", ym_prev) if resume or render_only else None

    if render_only and (not g_curr or not g_prev):
        raise SystemExit(f"缺少 GSC 快照：请先完整跑月报或去掉 --render-only（需要 {SNAPSHOT_DIR}/gsc-*.json）")

    if not render_only:
        ensure_bing_full(report_ym)
        if g_curr is None:
            print("\n[1/4] GSC 5K 拉取（当月）...")
            g_curr = fetch_gsc_full(
                meta["curr_start"], meta["curr_end"], meta["curr_label"],
                report_ym=report_ym, refresh_indexing=refresh_indexing,
            )
            save_snapshot("gsc", report_ym, g_curr)
        elif refresh_indexing:
            print("\n[1/4] GSC 当月 — 刷新收录指标...")
            g_curr = fetch_gsc_full(
                meta["curr_start"], meta["curr_end"], meta["curr_label"],
                report_ym=report_ym, refresh_indexing=True,
            )
            save_snapshot("gsc", report_ym, g_curr)
        else:
            print(f"\n[1/4] GSC 当月 — 使用快照 {report_ym}")

        if g_prev is None:
            print("[1/4] GSC 5K 拉取（对比月）...")
            g_prev = fetch_gsc_full(
                meta["prev_start"], meta["prev_end"], meta["prev_label"],
                report_ym=ym_prev, refresh_indexing=refresh_indexing,
            )
            save_snapshot("gsc", ym_prev, g_prev)
        elif refresh_indexing:
            print("[1/4] GSC 对比月 — 刷新收录指标...")
            g_prev = fetch_gsc_full(
                meta["prev_start"], meta["prev_end"], meta["prev_label"],
                report_ym=ym_prev, refresh_indexing=True,
            )
            save_snapshot("gsc", ym_prev, g_prev)
        else:
            print(f"[1/4] GSC 对比月 — 使用快照 {ym_prev}")

        if ga4_curr is None or (resume and ga4_needs_bing_refresh(ga4_curr)):
            if ga4_curr is not None:
                print("\n[2/4] GA4 当月 — 快照缺 bing_region_ga4（或 organic_sources），重拉...")
            else:
                print("\n[2/4] GA4 拉取（当月）...")
            ga4_curr = fetch_ga4_full(meta["curr_start"], meta["curr_end"], meta["curr_label"])
            save_snapshot("ga4", report_ym, ga4_curr)
        else:
            print(f"\n[2/4] GA4 当月 — 使用快照 {report_ym}")

        if ga4_prev is None or (resume and ga4_needs_bing_refresh(ga4_prev)):
            if ga4_prev is not None:
                print("[2/4] GA4 对比月 — 快照缺 bing_region_ga4（或 organic_sources），重拉...")
            else:
                print("[2/4] GA4 拉取（对比月）...")
            ga4_prev = fetch_ga4_full(meta["prev_start"], meta["prev_end"], meta["prev_label"])
            save_snapshot("ga4", ym_prev, ga4_prev)
        else:
            print(f"[2/4] GA4 对比月 — 使用快照 {ym_prev}")
    else:
        if ga4_curr is None:
            ga4_curr = load_ga4_from_legacy_cache(report_ym)
        if ga4_prev is None:
            ga4_prev = load_ga4_from_legacy_cache(ym_prev)
        if not ga4_curr or not ga4_prev:
            raise SystemExit("缺少 GA4 快照或 ga4-{ym}.json 缓存")

    if snapshots_only:
        print(f"\n✅ 快照已写入 {SNAPSHOT_DIR}（--snapshots-only，跳过报告生成）")
        return SNAPSHOT_DIR / f"gsc-{report_ym}.json"

    refresh_keyword_brand_splits(g_curr)
    refresh_keyword_brand_splits(g_prev)

    if refresh_brand and not render_only:
        print("\n[2b/4] 重拉 country×query 并重算大区品牌/非品牌...")
        rq = refresh_gsc_regions_from_api(meta["curr_start"], meta["curr_end"], meta["curr_label"])
        g_curr["region_stats"] = rq["region_stats"]
        g_curr["region_brand_top"] = rq["region_brand_top"]
        g_curr["region_nonbrand_top"] = rq["region_nonbrand_top"]
        save_snapshot("gsc", report_ym, g_curr)
        rq_prev = refresh_gsc_regions_from_api(meta["prev_start"], meta["prev_end"], meta["prev_label"])
        g_prev["region_stats"] = rq_prev["region_stats"]
        g_prev["region_brand_top"] = rq_prev["region_brand_top"]
        g_prev["region_nonbrand_top"] = rq_prev["region_nonbrand_top"]
        save_snapshot("gsc", ym_prev, g_prev)
    else:
        rebuild_region_brand_lists(g_curr)
        rebuild_region_brand_lists(g_prev)

    print("\n[3/4] 计算分层 + 匹配竞品词...")
    g_curr["tiers"] = compute_tiers(g_curr["keywords"], g_curr["brand_kw"], g_curr["nonbrand_kw"])
    g_prev["tiers"] = compute_tiers(g_prev["keywords"], g_prev["brand_kw"], g_prev["nonbrand_kw"])
    comp_curr = match_competitors(g_curr["nonbrand_kw"])
    comp_prev = match_competitors(g_prev["nonbrand_kw"])
    pdirs_prev = page_dir_analysis(g_prev["pages"])
    pdirs_curr = page_dir_analysis(g_curr["pages"])

    print(f"  品牌词: {g_prev['tiers']['品牌词']['count']} → {g_curr['tiers']['品牌词']['count']}")
    print(f"  非品牌词: {g_prev['tiers']['非品牌词']['count']} → {g_curr['tiers']['非品牌词']['count']}")
    print(f"  竞品 Core: {comp_curr['unique_core']}/{comp_curr['core_total']} ({comp_curr['core_rate']}%)")
    print(f"  页面目录: {len(pdirs_curr)} groups")

    metrics_dir = TRIDENT / "reports" / "monthly" / ".metrics"
    hist = load_metrics_history(metrics_dir, OUT_DIR, report_ym)
    save_metrics_snapshot(metrics_dir, report_ym, g_curr, ga4_curr, comp_curr, pdirs_curr)

    print("\n[3b/4] DataWorks SEO/GEO 产品数据...")
    sgeo_curr = load_seo_geo_snapshot(report_ym)
    sgeo_prev = load_seo_geo_snapshot(ym_prev)
    if sgeo_curr is None or not render_only:
        sgeo_curr = ingest_for_month(report_ym)
    if sgeo_prev is None or not render_only:
        sgeo_prev = ingest_for_month(ym_prev)
    print(f"  当月: {sgeo_curr.get('source_file', '—')} | 月去重: {sgeo_curr.get('has_monthly_dedup')}")
    print(f"  对比月: {sgeo_prev.get('source_file', '—')} | 月去重: {sgeo_prev.get('has_monthly_dedup')}")

    print("\n[4/4] 生成完整报告...")
    report = generate_report(
        g_prev, g_curr, ga4_prev, ga4_curr, comp_prev, comp_curr,
        pdirs_prev, pdirs_curr, meta, hist,
        sgeo_prev=sgeo_prev, sgeo_curr=sgeo_curr,
    )

    out_path = TRIDENT / "reports" / "monthly" / f"Lovart-SEO-{report_ym}.md"
    out_path.write_text(report)
    print(f"\n  📄 {out_path}")
    print(f"  📊 {len(report):,} chars, {len(report.splitlines())} lines")
    print("\n  月报 V2 自检（AGENTS.md A0d / seo_report_standards）：")
    for item in monthly_post_run_checklist():
        print(f"    [ ] {item}")

    ym_prev = meta["prev_start"][:7]
    for name, data in [
        (f"gsc-5k-{ym_prev}", {"tiers": g_prev["tiers"], "countries": g_prev["countries"], "pages": g_prev["pages"], "region_top_kw": g_prev["region_top_keywords"]}),
        (f"gsc-5k-{report_ym}", {"tiers": g_curr["tiers"], "countries": g_curr["countries"], "pages": g_curr["pages"], "region_top_kw": g_curr["region_top_keywords"]}),
    ]:
        (OUT_DIR / f"{name}.json").write_text(json.dumps(data, indent=2, ensure_ascii=False))

    print("\n✅ Done!")
    return out_path


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Lovart SEO monthly report (GSC 5K + GA4 + competitor)")
    parser.add_argument("--month", default="2026-05", help="Report month YYYY-MM (default: 2026-05)")
    parser.add_argument("--resume", action="store_true", help="Use cached snapshots for completed fetch steps")
    parser.add_argument("--render-only", action="store_true", help="Skip API; render from GSC snapshots + GA4 cache")
    parser.add_argument(
        "--snapshots-only",
        action="store_true",
        help="Fetch GSC/GA4 and write monthly-snapshots only; skip report render",
    )
    parser.add_argument(
        "--refresh-indexing",
        action="store_true",
        help="Re-fetch page pagination + sitemap indexing (even with --resume)",
    )
    parser.add_argument(
        "--refresh-brand",
        action="store_true",
        help="Re-fetch country×query and rebuild region brand/nonbrand splits",
    )
    args = parser.parse_args()
    run_monthly_report(
        args.month,
        resume=args.resume,
        render_only=args.render_only,
        snapshots_only=args.snapshots_only,
        refresh_indexing=args.refresh_indexing,
        refresh_brand=args.refresh_brand,
    )
