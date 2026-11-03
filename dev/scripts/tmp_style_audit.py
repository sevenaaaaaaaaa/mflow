#!/usr/bin/env python3
"""tmp_style_audit.py — Hero brief 风格一致性 & 多样性审计

输出：
  1) 航道 × 模块 分布
  2) n-gram 模板疲劳（8-gram 出现 ≥N 次）
  3) 两两相似度（Jaccard on 内容词）→ 过度同质对
  4) 调色板 / 点睛色 / 镜头焦段 / 背景处理 分布
  5) 结构完整性（主体从句是否唯一）
"""
import json, re, itertools
from collections import Counter, defaultdict
from pathlib import Path

D = Path("/Users/seveno/MFlow Dev/mflow/harness/Docs/S3-内容创作/Hero封面批次-2026-11")

def load(name):
    return [json.loads(l) for l in (D / name).read_text(encoding="utf-8").splitlines() if l.strip()]

recs = []
for f in ["module-A-split.jsonl", "module-B-cinematic.jsonl",
          "module-C-mosaic.jsonl", "module-D-gallery.jsonl"]:
    for r in load(f):
        r["_mod"] = f.split("-")[1]
        recs.append(r)
print(f"总条数: {len(recs)}\n")

STOP = set("""a an the one of on in at with and or for to from by as is are be its it this that
single only each per into across beside behind over under near beside about above below
with without no not very about around along""".split())

def tokens(t):
    w = re.findall(r"[a-z0-9\-']+", t.lower())
    return [x for x in w if x not in STOP and len(x) > 2]

# ── 1. 航道 × 模块 ──
print("=" * 78)
print("1. 航道 × 模块 分布")
lane_mod = defaultdict(Counter)
for r in recs:
    lane_mod[r["lane"]][r["_mod"]] += 1
mods = sorted({r["_mod"] for r in recs})
print(f"{'lane':<26}" + "".join(f"{m:>10}" for m in mods) + f"{'合计':>7}")
for lane in sorted(lane_mod, key=lambda x: -sum(lane_mod[x].values())):
    print(f"{lane:<26}" + "".join(f"{lane_mod[lane][m]:>10}" for m in mods)
          + f"{sum(lane_mod[lane].values()):>7}")

# ── 2. n-gram 模板疲劳 ──
print()
print("=" * 78)
print("2. 模板疲劳：重复出现的 8-gram（≥5 条共享）")
GRAMS = defaultdict(list)
for r in recs:
    w = re.findall(r"[a-z0-9\-\u4e00-\u9fff]+", r["prompt"].lower())
    seen = set()
    for i in range(len(w) - 7):
        g = " ".join(w[i:i + 8])
        if g not in seen:
            GRAMS[g].append(r["id"])
            seen.add(g)
heavy = [(g, ids) for g, ids in GRAMS.items() if len(ids) >= 5]
heavy.sort(key=lambda x: -len(x[1]))
for g, ids in heavy[:25]:
    print(f"  [{len(ids):>2}×] {g}")
print(f"  … 共 {len(heavy)} 个高频短语")

# ── 3. 两两相似度 ──
print()
print("=" * 78)
print("3. 两两相似度（Jaccard ≥0.75 视为过度同质）")
toks = {r["id"]: set(tokens(r["prompt"])) for r in recs}
pairs = []
ids = sorted(toks)
for a, b in itertools.combinations(ids, 2):
    inter = len(toks[a] & toks[b]); uni = len(toks[a] | toks[b])
    j = inter / uni if uni else 0
    if j >= 0.75:
        pairs.append((j, a, b))
pairs.sort(reverse=True)
print(f"  同质对数: {len(pairs)}")
for j, a, b in pairs[:20]:
    print(f"  {j:.2f}  {a} ↔ {b}")
# 同套内高相似是设计意图，仅标注
same_set = [(j, a, b) for j, a, b in pairs if a.rsplit("-", 1)[0] == b.rsplit("-", 1)[0]]
cross_set = [(j, a, b) for j, a, b in pairs if a.rsplit("-", 1)[0] != b.rsplit("-", 1)[0]]
print(f"  其中同套内（预期，同族一致性）: {len(same_set)}  跨套（需关注）: {len(cross_set)}")

# ── 4. 调色板 / 镜头 / 背景 ──
print()
print("=" * 78)
print("4. 视觉参数分布")
def grab(pat, text):
    m = re.search(pat, text, re.I)
    return m.group(1).strip() if m else None

pal, accent, lens, backdrop = Counter(), Counter(), Counter(), Counter()
for r in recs:
    p = r["prompt"]
    m = re.search(r"(warm-grey|warm grey|sand and cream|ivory|cream|charcoal|deep charcoal|"
                  r"warm neutral|warm beige|neutral|teal-and-amber|bone-white|sand)\b[^.]{0,30}?(palette|field|backdrop|tones?)", p, re.I)
    base = None
    for c in ["warm-grey", "warm grey", "sand and cream", "deep charcoal", "teal-and-amber",
              "warm neutral", "warm beige", "charcoal", "ivory", "cream", "sand", "neutral", "bone-white"]:
        if c in p.lower():
            base = c; break
    pal[base or "未标注"] += 1
    for c in ["coral", "copper", "deep-green", "tangerine", "saturated", "electric", "ink", "warm highlight"]:
        if c in p.lower():
            accent[c] += 1
    for l in re.findall(r"\b(50mm|85mm|100mm|35mm)\b", p):
        lens[l] += 1
    if "seamless" in p.lower(): backdrop["seamless"] += 1
    if "one flat" in p.lower(): backdrop["flat single tone (gallery)"] += 1
    if "stone" in p.lower(): backdrop["stone surface"] += 1

print("  底色:", dict(pal.most_common()))
print("  点睛色:", dict(accent.most_common()))
print("  焦段:", dict(lens.most_common()))
print("  背景处理:", dict(backdrop.most_common()))

# ── 5. 结构完整性 ──
print()
print("=" * 78)
print("5. 结构完整性")
FLAT_OK = "flat poster layout with no photographic perspective"
miss_camera = [r["id"] for r in recs if not re.search(r"\d+mm", r["prompt"]) and FLAT_OK not in r["prompt"]]
miss_light = [r["id"] for r in recs if not re.search(r"(key light|daylight|side light|volumetric|light source|raking|spotlight|top light|even lighting|ambient)", r["prompt"], re.I)]
# L2 严格双色（teal-and-amber）是设计意图，无第三色不算缺陷
miss_accent = [r["id"] for r in recs if not re.search(r"(coral|copper|brass|deep-green|tangerine|saturated|electric|ink|accent)", r["prompt"], re.I)
              and not (r["lane"] == "L2-cinematic-still" and "two-color" in r["prompt"])]
print(f"  缺焦段: {miss_camera or '无'}")
print(f"  缺布光: {miss_light or '无'}")
print(f"  缺点睛色: {miss_accent or '无'}")

# ── 导出机读明细 ──
out = []
for r in recs:
    out.append({"id": r["id"], "mod": r["_mod"], "lane": r["lane"], "theme": r["theme"],
                "ratio": r["ratio"], "n_tokens": len(toks[r["id"]])})
(D / "audit-detail.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
print(f"\n明细已写入 audit-detail.json")
