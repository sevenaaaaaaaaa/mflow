#!/usr/bin/env python3
"""周报最终数字汇总 — GSC/GA4/Bing/DataWorks/竞品词/地区/排名分层 (v2)."""
import json, re, sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from lovart_brand_match import is_brand

GSC = json.load(open("/tmp/gsc_windows.json"))
GA4 = json.load(open("/tmp/ga4_windows.json"))
DW = json.load(open("/tmp/dataworks_windows.json"))
BING = json.load(open(Path.home() / "Documents/Lovart Local Dev/Output/Data Ingestion/bing-full.json"))

def gsc_rows(wname, dim):
    return GSC["data"][wname].get(dim, [])

def qkey(r, i=0):
    return r["keys"][i]

# ============ 竞品核心词 (36 词) ============
CORE_FILE = str(Path(__file__).resolve().parents[3] / "1-2 Insight/Keywords Research/竞品核心非品牌词/lovart_competitors_core_keywords.md")
txt = Path(CORE_FILE).read_text()
core_words = set()
for line in txt.splitlines():
    m = re.match(r"\|\s*([A-Za-z][A-Za-z0-9 \-/]*?)\s*\|", line)
    if m:
        w = m.group(1).strip().lower()
        if len(w) > 2 and not w.startswith(("关键词", "核心", "优先级", "p0", "p1", "p2", "模型", "mid ", "mid|", "sora ", "sora|")):
            core_words.add(w)
for line in txt.splitlines():
    m = re.match(r"\|\s*(sora|kling|veo 3|midjourney|dall-e|flux|seedance|seedream)\s*\|", line.lower())
    if m:
        core_words.add(m.group(1))
core_words = sorted(core_words)
print(f"核心词: {len(core_words)}")
print(core_words)

# 全量词库
FULL_FILE = str(Path(__file__).resolve().parents[3] / "1-2 Insight/Keywords Research/竞品核心非品牌词/lovart_competitors_keywords.md")
txt2 = Path(FULL_FILE).read_text()
full_words = set()
for line in txt2.splitlines():
    m = re.match(r"\|\s*([^|]+?)\s*\|", line)
    if m:
        cell = m.group(1).strip().lower()
        # 取英文部分（" / " 之前）
        if " / " in cell:
            cell = cell.split(" / ")[0].strip()
        if re.fullmatch(r"[a-z0-9 \-]+", cell) and 2 < len(cell) < 40 and cell not in ("关键词", "出现竞品"):
            full_words.add(cell)
full_words = sorted(full_words)
print(f"全量词: {len(full_words)}")
print(full_words[:80])

def word_coverage(rows, words):
    """每个核心词: 是否有 query 命中(非品牌)。返回 covered set + 每词点击/曝光/CTR/pos."""
    per_word = {}
    for r in rows:
        q = qkey(r).lower()
        if is_brand(qkey(r)):
            continue
        for w in words:
            if w in q:
                if w not in per_word:
                    per_word[w] = {"clicks": 0, "impr": 0, "queries": 0, "best_pos": 99}
                per_word[w]["clicks"] += r["clicks"]
                per_word[w]["impr"] += r["impressions"]
                per_word[w]["queries"] += 1
                per_word[w]["best_pos"] = min(per_word[w]["best_pos"], r["position"])
    return per_word

print("\n=== 竞品核心词覆盖 (cur vs prev, 36 词口径) ===")
cov = {}
for wname in ("cur", "prev"):
    pw = word_coverage(gsc_rows(wname, "query"), core_words)
    cov[wname] = pw
    tot_c = sum(v["clicks"] for v in pw.values())
    print(f"[{wname}] 覆盖 {len(pw)}/{len(core_words)} 词, 点击合计={tot_c:,}")
    for w, v in sorted(pw.items(), key=lambda x: -x[1]["clicks"])[:25]:
        print(f"  {w:<24} c={v['clicks']:>4,} i={v['impr']:>8,} ctr={v['clicks']/v['impr']*100:.1f}% best_pos={v['best_pos']:.1f}")
missing = set(core_words) - set(pw.get("cur", {}))
print(f"[cur] 未覆盖核心词 ({len(missing)}): {sorted(missing)}")

print("\n=== 竞品全量词覆盖 (cur vs prev) ===")
for wname in ("cur", "prev"):
    pw = word_coverage(gsc_rows(wname, "query"), full_words)
    tot_c = sum(v["clicks"] for v in pw.values())
    print(f"[{wname}] 覆盖 {len(pw)}/{len(full_words)} 词, 点击合计={tot_c:,}")

# ============ 排名分层 ============
print("\n=== 排名分层 (cur, 6d) ===")
rows = gsc_rows("cur", "query")
tiers = [(1, "≤1"), (3, "≤3"), (5, "≤5"), (10, "≤10"), (20, "≤20"), (50, "≤50")]
tot_c = sum(r["clicks"] for r in rows)
for t, name in tiers:
    c = sum(r["clicks"] for r in rows if r["position"] <= t)
    print(f"  pos{name}: clicks={c:,} ({c/tot_c*100:.1f}%)")

# ============ Bing ============
td = {d["date"]: d for d in BING["traffic_daily"]}
def bing_sum(dates):
    c = sum(td[d]["clicks"] for d in dates if d in td)
    i = sum(td[d]["impressions"] for d in dates if d in td)
    return c, i
cur_dates = ["2026-08-%02d" % d for d in range(12, 19)]
prev_dates = ["2026-08-%02d" % d for d in range(5, 12)]
print("\n=== Bing 周窗口 ===")
for name, ds in (("cur 08/12-08/18", cur_dates), ("prev 08/05-08/11", prev_dates)):
    c, i = bing_sum(ds)
    print(f"  {name}: clicks={c:,} impr={i:,} ctr={c/i*100:.1f}% (Bing 2天延迟, cur 实际 6d 可用)")

print("\n=== Bing 8月 Top12 关键词 ===")
for k in sorted(BING["keywords_monthly"].get("2026-08", []), key=lambda x: -x["clicks"])[:12]:
    print(f"  {k['q'][:40]:<42} c={k['clicks']:>7,} i={k['impr']:>9,} ctr={k['ctr']:.1f}% pos={k['pos']:.1f}")

print("\n=== Bing 8月 Top10 页面 ===")
for p in sorted(BING["pages_monthly"].get("2026-08", []), key=lambda x: -x["clicks"])[:10]:
    print(f"  {p['url'][:55]:<57} c={p['clicks']:>6,} ctr={p['ctr']:.1f}% pos={p['pos']:.1f}")

print("\n=== Bing 7月全月 Top8 关键词 ===")
for k in sorted(BING["keywords_monthly"].get("2026-07", []), key=lambda x: -x["clicks"])[:8]:
    print(f"  {k['q'][:40]:<42} c={k['clicks']:>7,} ctr={k['ctr']:.1f}% pos={k['pos']:.1f}")

# ============ GA4 补充 ============
print("\n=== GA4 全站 sessions (所有渠道) ===")
for wname in ("cur", "prev"):
    rows = GA4["data"][wname]["organic_daily_no_filter"]
    tot = sum(int(r["metrics"]["sessions"]) for r in rows)
    print(f"  [{wname}] 全站 sessions={tot:,}")

# ============ GSC country 明细 Top ============
print("\n=== GSC 国家 Top15 (cur, 6d) ===")
rows_c = gsc_rows("cur", "country")
rows_p = gsc_rows("prev", "country")
pmap = {qkey(r).lower(): r for r in rows_p}
for r in sorted(rows_c, key=lambda x: -x["clicks"])[:15]:
    c = qkey(r).lower()
    p = pmap.get(c)
    pc = p["clicks"] if p else 0
    chg = (r["clicks"] - pc) / pc * 100 if pc else None
    chg_s = f"{chg:+.1f}%" if chg is not None else "new"
    print(f"  {c:<8} clicks={r['clicks']:>6,} (prev {pc:>6,} {chg_s}) ctr={r['ctr']*100:.1f}% pos={r['position']:.1f}")

# ============ GA4 pages Top ============
print("\n=== GA4 organic 着陆页 Top12 (cur vs prev) ===")
cur_p = {r["dims"]["pagePath"]: r["metrics"] for r in GA4["data"]["cur"]["pages"]}
prev_p = {r["dims"]["pagePath"]: r["metrics"] for r in GA4["data"]["prev"]["pages"]}
for k in sorted(cur_p, key=lambda x: -int(cur_p[x]["sessions"]))[:12]:
    c, p = cur_p.get(k), prev_p.get(k)
    c_s = int(c["sessions"])
    p_s = int(p["sessions"]) if p else 0
    chg = (c_s - p_s) / p_s * 100 if p_s else None
    chg_s = f"{chg:+.1f}%" if chg is not None else "new"
    print(f"  {k[:50]:<52} cur={c_s:>7,} prev={p_s:>7,} {chg_s}")

# ============ GA4 source 环比 ============
print("\n=== GA4 organic sessionSource 环比 Top12 ===")
cur_s = {r["dims"]["sessionSource"]: int(r["metrics"]["sessions"]) for r in GA4["data"]["cur"]["source"]}
prev_s = {r["dims"]["sessionSource"]: int(r["metrics"]["sessions"]) for r in GA4["data"]["prev"]["source"]}
for k in sorted(cur_s, key=lambda x: -cur_s[x])[:12]:
    c, p = cur_s[k], prev_s.get(k, 0)
    chg = (c - p) / p * 100 if p else None
    chg_s = f"{chg:+.1f}%" if chg is not None else "new"
    print(f"  {k:<20} cur={c:>8,} prev={p:>8,} {chg_s}")

# 保存核心覆盖
json.dump({w: {k: v for k, v in cov[w].items()} for w in cov},
          open("/tmp/core_coverage.json", "w"), ensure_ascii=False, indent=1, default=str)
print("\nSaved /tmp/core_coverage.json")
