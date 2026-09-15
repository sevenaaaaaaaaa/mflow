#!/usr/bin/env python3
"""JP 全窗口分析 — GSC JP(2025-04~2026-07) + GA4 JP + Bing 全站。

产出:
  /tmp/jp_pull/jp_analysis.json — 全部聚合结果
  stdout — 关键结论速览
"""
import json, re, sys
from pathlib import Path
from collections import defaultdict

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from lovart_brand_match import is_brand

OUT = Path("/tmp/jp_pull")
gsc = json.loads((OUT / "gsc_jp.json").read_text())
ga4 = json.loads((OUT / "ga4_jp.json").read_text())
bing = json.loads((OUT / "bing-full.json").read_text())

A = {"gsc": {}, "ga4": {}, "bing": {}}

# ─────────────────────────────── GSC JP ───────────────────────────────
months = sorted(gsc["months"])
JP = re.compile(r"[\u3040-\u30ff\u4e00-\u9fff]")  # 平假名/片假名/汉字 → 日语文关键词

def agg(rows):
    d = {}
    for r in rows:
        k = r["k"]
        e = d.setdefault(k, {"clicks": 0, "impr": 0, "posw": 0.0, "wsum": 0})
        e["clicks"] += r["clicks"]; e["impr"] += r["impr"]
        if r["pos"] > 0 and r["impr"] > 0:
            e["posw"] += r["pos"] * r["impr"]; e["wsum"] += r["impr"]
    out = []
    for k, e in d.items():
        out.append({"k": k, "clicks": e["clicks"], "impr": e["impr"],
                    "ctr": round(e["clicks"] / e["impr"] * 100, 2) if e["impr"] else 0.0,
                    "pos": round(e["posw"] / e["wsum"], 1) if e["wsum"] else 0.0,
                    "brand": is_brand(k), "jp": bool(JP.search(k))})
    out.sort(key=lambda x: x["clicks"], reverse=True)
    return out

monthly = []
for mo in months:
    q = agg(gsc["months"][mo]["query"])
    p = agg(gsc["months"][mo]["page"])
    d = gsc["months"][mo]["daily"]
    tot_c = sum(r["clicks"] for r in d); tot_i = sum(r["impr"] for r in d)
    posw = sum(r["pos"] * r["impr"] for r in d); wsum = sum(r["impr"] for r in d)
    bq = [r for r in q if r["brand"]]; nbq = [r for r in q if not r["brand"]]
    jpq = [r for r in q if r["jp"]]
    monthly.append({
        "mo": mo, "days": len(d),
        "clicks": tot_c, "impr": tot_i,
        "ctr": round(tot_c / tot_i * 100, 2) if tot_i else 0.0,
        "pos": round(posw / wsum, 1) if wsum else 0.0,
        "n_kw": len(q), "n_page": len(p),
        "brand_clicks": sum(r["clicks"] for r in bq), "brand_n": len(bq),
        "nb_clicks": sum(r["clicks"] for r in nbq), "nb_n": len(nbq),
        "jp_kw_n": len(jpq), "jp_kw_clicks": sum(r["clicks"] for r in jpq),
        "top_q": q[:15], "top_p": p[:15],
    })
A["gsc"]["monthly"] = monthly

# 全窗口聚合关键词（跨月去重求和）
all_q = []
for mo in months:
    all_q.extend(gsc["months"][mo]["query"])
full_kw = agg(all_q)
all_p = []
for mo in months:
    all_p.extend(gsc["months"][mo]["page"])
full_pg = agg(all_p)
A["gsc"]["full_kw"] = full_kw
A["gsc"]["full_pg"] = full_pg

# 品牌 / 非品牌 / 日语文 全窗口汇总
brand_kw = [r for r in full_kw if r["brand"]]
nb_kw = [r for r in full_kw if not r["brand"]]
jp_kw = [r for r in full_kw if r["jp"]]
A["gsc"]["brand_kw"] = brand_kw
A["gsc"]["nb_kw"] = nb_kw
A["gsc"]["jp_kw"] = jp_kw

# 页面分类
def classify(url):
    u = url.split("lovart.ai")[-1].lstrip("/")
    if u == "" or u.startswith("?"): return "homepage"
    seg = u.split("/")[0].split("?")[0]
    if seg in ("ja", "jp", "ja-JP"): return "jp_localized"
    if seg == "blog": return "blog"
    if seg == "tools": return "tools"
    if seg == "features": return "features"
    if seg in ("modelinfo", "imageinfo"): return "ai_asset"
    if seg in ("case", "customers"): return "ugc"
    if seg in ("designers", "marketers", "business-owners", "solutions", "explore"): return "solutions"
    return "other"

from collections import Counter
cat_all = Counter(); cat_clicks = Counter()
for r in full_pg:
    c = classify(r["k"])
    cat_all[c] += 1; cat_clicks[c] += r["clicks"]
A["gsc"]["page_cats"] = {c: {"pages": cat_all[c], "clicks": cat_clicks[c]} for c in cat_all}

# 月份 movers（关键词点击环比）
prev = {}
movers = {}
for mo in months:
    cur = {r["k"]: r["clicks"] for r in agg(gsc["months"][mo]["query"])}
    diff = {}
    for k, c in cur.items():
        diff[k] = c - prev.get(k, 0)
    up = sorted(diff.items(), key=lambda x: -x[1])[:12]
    down = sorted(diff.items(), key=lambda x: x[1])[:12]
    movers[mo] = {"up": up, "down": down}
    prev = cur
A["gsc"]["movers"] = movers

# ─────────────────────────────── GA4 JP ───────────────────────────────
sd = ga4["jp_source_daily"]
def engine(src):
    s = src.lower()
    if "google" in s: return "google"
    if "bing" in s: return "bing"
    if "yahoo" in s: return "yahoo"
    if "duckduckgo" in s: return "ddg"
    if "baidu" in s: return "baidu"
    if "docomo" in s or "nttdocomo" in s: return "docomo"
    if s in ("", "(direct)", "(none)"): return "direct"
    return "other:" + src

def mk(datestr):
    s = datestr.replace("-", "")
    return f"{s[:4]}-{s[4:6]}"


eng_mo = defaultdict(lambda: defaultdict(int))
eng_total = Counter()
by_month_sess = Counter()
for r in sd:
    mo = mk(r["date"])
    e = engine(r["source"])
    eng_mo[mo][e] += r["sessions"]
    eng_total[e] += r["sessions"]
    by_month_sess[mo] += r["sessions"]
A["ga4"]["engine_monthly"] = {mo: dict(d) for mo, d in sorted(eng_mo.items())}
A["ga4"]["engine_total"] = dict(eng_total)
A["ga4"]["jp_monthly_sessions"] = dict(sorted(by_month_sess.items()))

# JP organic 月度
org_daily = ga4["jp_organic_daily"]
org_mo = defaultdict(lambda: {"sessions": 0, "users": 0, "new": 0})
for r in org_daily:
    mo = mk(r["date"])
    org_mo[mo]["sessions"] += r["sessions"]
    org_mo[mo]["users"] += r["users"]
    org_mo[mo]["new"] += r["new"]
A["ga4"]["jp_organic_monthly"] = {mo: dict(d) for mo, d in sorted(org_mo.items())}

# JP 占全站 organic 份额
oc = {r["country"]: r["sessions"] for r in ga4["organic_by_country"]}
jp_share = oc.get("Japan", 0)
A["ga4"]["jp_share_of_organic"] = {"jp": jp_share, "world": sum(oc.values()),
                                    "share_pct": round(jp_share / sum(oc.values()) * 100, 2) if oc else 0}
A["ga4"]["organic_top_countries"] = sorted(oc.items(), key=lambda x: -x[1])[:15]

# JP 着陆页 Top（含分类）
lp = [r for r in ga4["jp_landing_pages"]]
lp_sorted = sorted(lp, key=lambda x: -x["sessions"])
A["ga4"]["jp_top_pages"] = [{"page": r["page"], "sessions": r["sessions"],
                             "cat": classify(r["page"])} for r in lp_sorted[:100]]

# ─────────────────────────────── Bing ───────────────────────────────
bt = bing.get("traffic_monthly", {})
A["bing"]["traffic_monthly"] = bt
bk = bing.get("keywords", [])
bp = bing.get("pages", [])
A["bing"]["keywords_all"] = bk[:200]
A["bing"]["pages_all"] = bp[:200]
bm = bing.get("keywords_monthly", {})
A["bing"]["keywords_monthly"] = {mo: rows[:50] for mo, rows in sorted(bm.items())}
pm = bing.get("pages_monthly", {})
A["bing"]["pages_monthly"] = {mo: rows[:50] for mo, rows in sorted(pm.items())}

(OUT / "jp_analysis.json").write_text(json.dumps(A, ensure_ascii=False, indent=1))

# ─────────────────────── stdout 速览 ───────────────────────
print("== GSC JP 月度总量 ==")
for m in monthly:
    print(f"{m['mo']}  clicks={m['clicks']:>7,} impr={m['impr']:>9,} ctr={m['ctr']:5.2f}% pos={m['pos']:5.1f} 词={m['n_kw']:>4} 页={m['n_page']:>4} 品牌clk={m['brand_clicks']:>6,}({m['brand_n']}词) 日文词={m['jp_kw_n']}({m['jp_kw_clicks']:,}clk)")
print(f"\n全窗口: 关键词 {len(full_kw):,} | 品牌 {len(brand_kw)} 词 {sum(r['clicks'] for r in brand_kw):,}clk | 非品牌 {len(nb_kw)} 词 {sum(r['clicks'] for r in nb_kw):,}clk | 日文 {len(jp_kw)} 词 {sum(r['clicks'] for r in jp_kw):,}clk")
print(f"页面: {len(full_pg):,} | 分类: " + ", ".join(f"{c}={cat_clicks[c]:,}clk/{cat_all[c]}页" for c in sorted(cat_all, key=lambda x: -cat_clicks[x])))
print("\n== GSC 全窗口 Top20 关键词 ==")
for r in full_kw[:20]:
    tag = "BRAND" if r["brand"] else ("日文" if r["jp"] else "英文")
    print(f"  {r['k'][:45]:<45} {r['clicks']:>6,}clk {r['impr']:>8,}imp {r['ctr']:5.2f}% pos={r['pos']:4.1f} [{tag}]")
print("\n== GSC 全窗口 Top15 页面 ==")
for r in full_pg[:15]:
    print(f"  {r['k'][:60]:<60} {r['clicks']:>6,}clk {r['impr']:>8,}imp ctr={r['ctr']:5.2f}% [{classify(r['k'])}]")
print("\n== GA4 JP 引擎月度 ==")
for mo, d in sorted(eng_mo.items()):
    g = d.get("google", 0); b = d.get("bing", 0); y = d.get("yahoo", 0); o = sum(v for k, v in d.items() if k not in ("google", "bing", "yahoo"))
    print(f"  {mo}  total={sum(d.values()):>7,}  google={g:>6,}({g/sum(d.values())*100:4.1f}%) bing={b:>5,}({b/sum(d.values())*100:4.1f}%) yahoo={y:>5,}({y/sum(d.values())*100:4.1f}%) 其他={o:,}")
print(f"\nJP organic 份额: {jp_share:,}/{sum(oc.values()):,} = {jp_share/sum(oc.values())*100:.2f}%")
print("\n== Bing 全站 traffic_monthly ==")
for mo, v in sorted(bt.items()):
    print(f"  {mo}  clicks={v['clicks']:>8,} impr={v['impressions']:>10,} ctr={v['ctr']:5.2f}%")
print(f"\nBing 全窗口 Top15 关键词:")
for r in bk[:15]:
    print(f"  {r['q'][:45]:<45} {r['clicks']:>6,}clk {r['impr']:>8,}imp ctr={r['ctr']:5.2f}% pos={r['pos']:4.1f}")
print(f"Bing 全窗口 Top15 页面:")
for r in bp[:15]:
    print(f"  {r['url'][:60]:<60} {r['clicks']:>6,}clk {r['impr']:>8,}imp ctr={r['ctr']:5.2f}% pos={r['pos']:4.1f}")
