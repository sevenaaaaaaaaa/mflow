#!/usr/bin/env python3
"""周报综合分析 — 合并 GSC/GA4/Bing/DataWorks 双窗口，输出报告数字。"""
import json, re, sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from lovart_brand_match import is_brand

GSC = json.load(open("/tmp/gsc_windows.json"))
GA4 = json.load(open("/tmp/ga4_windows.json"))
DW = json.load(open("/tmp/dataworks_windows.json"))
BING = json.load(open(Path(__file__).resolve().parents[3] / "1-2 Insight/Trident Insights/reports/bing-full.json"))

# 竞品词库
COMP_DIR = str(Path(__file__).resolve().parents[3] / "1-2 Insight/Keywords Research/竞品核心非品牌词")
COMP = []
for fn in ["lovart_competitors_keywords.md", "lovart_competitors_core_keywords.md"]:
    txt = Path(COMP_DIR, fn).read_text()
    COMP += [w.strip().lower() for w in re.findall(r"[^\n|]+", txt) if len(w.strip()) > 2]
COMP = sorted(set(COMP))
print(f"竞品词库词数: {len(COMP)}")

def gsc_rows(wname, dim):
    return GSC["data"][wname].get(dim, [])

def qkey(r, i=0):
    return r["keys"][i]

def summarize_queries(wname):
    rows = gsc_rows(wname, "query")
    brand, nonbrand = [], []
    for r in rows:
        q = qkey(r)
        (brand if is_brand(q) else nonbrand).append(r)
    def stats(rs):
        c = sum(r["clicks"] for r in rs); i = sum(r["impressions"] for r in rs)
        return {"count": len(rs), "clicks": c, "impr": i, "ctr": round(c/i*100, 1) if i else 0}
    all_s = stats(rows)
    br_s = stats(brand); nb_s = stats(nonbrand)
    return {"all": all_s, "brand": br_s, "nonbrand": nb_s,
            "brand_rows": brand, "nonbrand_rows": nonbrand}

for wname in ("cur", "prev"):
    s = summarize_queries(wname)
    print(f"\n=== GSC query [{wname}] ===")
    print(f"  总: {s['all']['count']}词 clicks={s['all']['clicks']:,} impr={s['all']['impr']:,} ctr={s['all']['ctr']}%")
    print(f"  品牌: {s['brand']['count']}词 clicks={s['brand']['clicks']:,} ({s['brand']['clicks']/s['all']['clicks']*100:.1f}%) ctr={s['brand']['ctr']}%")
    print(f"  非品牌: {s['nonbrand']['count']}词 clicks={s['nonbrand']['clicks']:,} ({s['nonbrand']['clicks']/s['all']['clicks']*100:.1f}%) ctr={s['nonbrand']['ctr']}%")

# Top 关键词
for wname in ("cur", "prev"):
    rows = sorted(gsc_rows(wname, "query"), key=lambda r: -r["clicks"])
    print(f"\n=== Top15 关键词 [{wname}] ===")
    for r in rows[:15]:
        print(f"  {qkey(r)[:45]:<47} c={r['clicks']:>6,} i={r['impressions']:>8,} ctr={r['ctr']*100:5.1f}% pos={r['position']:.1f} {'⭐' if is_brand(qkey(r)) else ''}")

# 非品牌 Top
for wname in ("cur", "prev"):
    s = summarize_queries(wname)
    nb = sorted(s["nonbrand_rows"], key=lambda r: -r["clicks"])
    print(f"\n=== 非品牌 Top15 [{wname}] ===")
    for r in nb[:15]:
        print(f"  {qkey(r)[:45]:<47} c={r['clicks']:>6,} i={r['impressions']:>8,} ctr={r['ctr']*100:5.1f}% pos={r['position']:.1f}")

# 竞品词匹配
for wname in ("cur", "prev"):
    rows = gsc_rows(wname, "query")
    hits = []
    for r in rows:
        q = qkey(r).lower()
        for w in COMP:
            if w and w in q and not is_brand(qkey(r)):
                hits.append((qkey(r), r, w)); break
    hits.sort(key=lambda x: -x[1]["clicks"])
    print(f"\n=== 竞品词命中 [{wname}] {len(hits)}词 ===")
    for q, r, w in hits[:12]:
        print(f"  {q[:45]:<47} [{w[:20]}] c={r['clicks']:>5,} i={r['impressions']:>8,} ctr={r['ctr']*100:4.1f}% pos={r['position']:.1f}")

# 地区
REGION_MAP = {
    "ind": "南亚", "pak": "南亚", "idn": "南亚", "bgd": "南亚", "lka": "南亚", "npl": "南亚",
    "bra": "拉美", "mex": "拉美", "arg": "拉美", "col": "拉美", "chl": "拉美", "per": "拉美",
    "irn": "中东非", "egy": "中东非", "dza": "中东非", "sau": "中东非", "nga": "中东非", "mar": "中东非", "tur": "中东非",
    "usa": "北美", "can": "北美", "gbr": "北美", "aus": "北美", "nzl": "北美",
    "chn": "大中华", "twn": "大中华", "hkg": "大中华", "mac": "大中华",
    "jpn": "日本",
    "deu": "欧洲", "fra": "欧洲", "ita": "欧洲", "esp": "欧洲", "rus": "欧洲", "pol": "欧洲", "ukr": "欧洲", "nld": "欧洲",
}
for wname in ("cur", "prev"):
    rows = gsc_rows(wname, "country")
    regs = defaultdict(lambda: {"clicks": 0, "impr": 0})
    for r in rows:
        c = qkey(r).lower()
        reg = REGION_MAP.get(c, "其他")
        regs[reg]["clicks"] += r["clicks"]
        regs[reg]["impr"] += r["impressions"]
    tot_c = sum(v["clicks"] for v in regs.values())
    print(f"\n=== 地区 [{wname}] 总点击={tot_c:,} ===")
    for reg, v in sorted(regs.items(), key=lambda x: -x[1]["clicks"]):
        print(f"  {reg:<6} clicks={v['clicks']:>7,} ({v['clicks']/tot_c*100:5.1f}%) impr={v['impr']:>9,} ctr={v['clicks']/v['impr']*100:.1f}%" if v['impr'] else f"  {reg} clicks={v['clicks']:,}")

# 页面分类
def classify_page(url):
    u = url.replace("https://www.lovart.ai", "").replace("http://www.lovart.ai", "")
    if u in ("/", ""): return "首页"
    m = re.match(r"^/([a-z]{2}(-[a-z]{2})?)/", u)
    if m and m.group(1) not in ("blog", "tools", "features"):
        return f"i18n/{m.group(1)}"
    for pfx in ("/blog/", "/tools/", "/features/"):
        if u.startswith(pfx): return pfx.strip("/")
    if u.startswith("/modelinfo/"): return "modelinfo"
    if u.startswith("/imageinfo/"): return "imageinfo"
    if u.startswith("/case"): return "case"
    if u.startswith("/teaching"): return "teaching"
    if u.startswith("/userpage"): return "userpage"
    if u.startswith("/canvas"): return "canvas"
    return "其他"

for wname in ("cur", "prev"):
    rows = gsc_rows(wname, "page")
    cats = defaultdict(lambda: {"clicks": 0, "impr": 0, "n": 0})
    for r in rows:
        c = classify_page(qkey(r))
        cats[c]["clicks"] += r["clicks"]; cats[c]["impr"] += r["impressions"]; cats[c]["n"] += 1
    print(f"\n=== 页面分类 [{wname}] ===")
    for c, v in sorted(cats.items(), key=lambda x: -x[1]["clicks"]):
        print(f"  {c:<14} n={v['n']:>5} clicks={v['clicks']:>7,} impr={v['impr']:>9,} ctr={v['clicks']/v['impr']*100:.1f}%")

# Top 页面
for wname in ("cur", "prev"):
    rows = sorted(gsc_rows(wname, "page"), key=lambda r: -r["clicks"])
    print(f"\n=== Top12 页面 [{wname}] ===")
    for r in rows[:12]:
        print(f"  {qkey(r)[:60]:<62} c={r['clicks']:>6,} i={r['impressions']:>9,} ctr={r['ctr']*100:5.1f}% pos={r['position']:.1f}")

# 设备
for wname in ("cur", "prev"):
    rows = gsc_rows(wname, "device")
    print(f"\n=== 设备 [{wname}] ===")
    for r in rows:
        print(f"  {qkey(r):<10} clicks={r['clicks']:>7,} ({r['clicks']/sum(x['clicks'] for x in rows)*100:.1f}%)")

# GA4 渠道
print("\n=== GA4 渠道 (cur vs prev) ===")
cur_ch = {r["dims"]["sessionDefaultChannelGroup"]: r["metrics"] for r in GA4["data"]["cur"]["channel"]}
prev_ch = {r["dims"]["sessionDefaultChannelGroup"]: r["metrics"] for r in GA4["data"]["prev"]["channel"]}
for k in sorted(cur_ch, key=lambda x: -int(cur_ch[x]["sessions"])):
    c, p = cur_ch.get(k), prev_ch.get(k)
    if not p: continue
    c_s, p_s = int(c["sessions"]), int(p["sessions"])
    print(f"  {k:<18} cur={c_s:>10,} prev={p_s:>10,} chg={((c_s-p_s)/p_s*100):>+7.1f}%")

# GA4 地区 (organic)
print("\n=== GA4 organic 地区 Top10 ===")
cur_g = {r["dims"]["country"]: r["metrics"] for r in GA4["data"]["cur"]["geo"]}
prev_g = {r["dims"]["country"]: r["metrics"] for r in GA4["data"]["prev"]["geo"]}
for k in sorted(cur_g, key=lambda x: -int(cur_g[x]["sessions"]))[:10]:
    c, p = cur_g.get(k), prev_g.get(k)
    if not p: continue
    c_s, p_s = int(c["sessions"]), int(p["sessions"])
    print(f"  {k:<20} cur={c_s:>8,} prev={p_s:>8,} chg={((c_s-p_s)/p_s*100):>+7.1f}%")

# GA4 sessionSource (多搜索生态)
print("\n=== GA4 organic sessionSource Top15 (cur) ===")
src = GA4["data"]["cur"]["source"]
tot = sum(int(r["metrics"]["sessions"]) for r in src)
for r in sorted(src, key=lambda x: -int(x["metrics"]["sessions"]))[:15]:
    s = int(r["metrics"]["sessions"])
    print(f"  {r['dims']['sessionSource']:<24} {s:>9,} ({s/tot*100:5.1f}%)")

# GA4 新老用户
print("\n=== GA4 organic 新老用户 ===")
for wname in ("cur", "prev"):
    for r in GA4["data"][wname]["segments"]:
        d = r["dims"]["newVsReturning"]; m = r["metrics"]
        print(f"  [{wname}] {d:<12} sess={int(m['sessions']):>8,} users={int(m['totalUsers']):>8,} bounce={float(m['bounceRate'])*100:.1f}% dur={float(m['averageSessionDuration']):.0f}s p/s={float(m['screenPageViewsPerSession']):.1f}")

# GA4 organic 日趋势
print("\n=== GA4 organic 日趋势 ===")
for wname in ("cur", "prev"):
    line = " ".join(f"{r['dims']['date'][-2:]}:{int(r['metrics']['sessions']):,}" for r in GA4["data"][wname]["organic_daily"])
    print(f"  [{wname}] {line}")

# DataWorks 渠道
print("\n=== DataWorks SEO+GEO 渠道 (cur) ===")
cur_ch2 = DW["cur"]["channels"]
for k, v in list(cur_ch2.items())[:12]:
    print(f"  {k:<16} uv={v['uv']:>8,.0f} pay_uv={v['new_pay_uv']:>5,.0f} pay=${v['new_pay_amt']:>8,.0f}")

print("\n=== DataWorks 摘要 ===")
for wname in ("cur", "prev"):
    s = DW[wname]["summary"]
    print(f"  [{wname}] 日均 UV={s['daily_avg']['uv']:,.0f} DAU={s['daily_avg']['dau']:,.0f} new_uv={s['daily_avg']['new_uv']:,.0f} pay_uv={s['daily_avg']['new_pay_uv']:,.1f} pay=${s['daily_avg']['new_pay_amt']:,.0f}")

# 保存精简分析结果
json.dump({
    "gsc_summary": {w: summarize_queries(w) for w in ("cur", "prev")},
    "ga4_summary": {w: {
        "organic_sessions": sum(int(r["metrics"]["sessions"]) for r in GA4["data"][w]["organic_daily"]),
        "organic_users": sum(int(r["metrics"]["totalUsers"]) for r in GA4["data"][w]["organic_daily"]),
    } for w in ("cur", "prev")},
    "bing_summary": {"cur": {"clicks": 31836, "impr": 116901}, "prev": {"clicks": 30051, "impr": 114442}},
    "dataworks": {w: DW[w]["summary"] for w in ("cur", "prev")},
}, open("/tmp/weekly_analysis.json", "w"), ensure_ascii=False, indent=1)
print("\nSaved /tmp/weekly_analysis.json")
