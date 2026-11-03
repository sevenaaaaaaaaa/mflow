#!/usr/bin/env python3
"""tmp_refine_v4.py — L4 图形平面航道差异化（解决 G-SOC/G-DOC/G-ADS/G-CMP 瓦片雷同）

思路：L4 四套共用同一 token 导致跨套相似，改为「同一航道 + 不同版式子型」：
  G-DOC → editorial-grid   : 严格网格、细线、大量留白（编辑部/报告感）
  G-SOC → bold-poster      : 大色块、斜切、满版冲击（社媒感）
  G-ADS → badge-stack      : 层叠标签、徽章形、错位（广告感）
  G-CMP → duotone-split    : 双色对撞、中缝硬分割、镜像结构（对比感）
"""
import json, re
from pathlib import Path

D = Path("/Users/seveno/MFlow Dev/mflow/harness/Docs/S3-内容创作/Hero封面批次-2026-11")

SUBSTYLE = {
    "G-DOC": dict(
        head=("Editorial flat-graphic layout on a strict Swiss grid, thin hairline rules and "
              "generous white space, small precise type-free layout blocks, paper grain texture "
              "with riso-print ink edges, flat poster layout with no photographic perspective, "
              "flat even lighting"),
        pal="ivory field with ink-blue and charcoal accents",
        cam=["viewed straight on as a page spread", "framed as a tight crop on the grid modules",
             "seen slightly off-axis as a stacked page", "viewed as a generous margin-led layout",
             "framed as a single module isolated on the grid", "seen as a full-spread cover layout"],
    ),
    "G-SOC": dict(
        head=("Bold flat poster composition with large color blocks and one diagonal slice, "
              "high-impact full-bleed layout, paper grain texture with riso-print ink edges, "
              "flat poster layout with no photographic perspective, flat even lighting"),
        pal="cream field with coral and charcoal in large blocks",
        cam=["cropped tight to the central shape", "framed as a square full-bleed poster",
             "seen with the diagonal slice cutting corner to corner", "framed with the subject pushed low",
             "viewed as a bold off-center composition", "framed as a clean centered emblem"],
    ),
    "G-ADS": dict(
        head=("Flat graphic badge-and-label composition with layered offset cards and one "
              "stamped badge shape, crisp edges and precise registration, paper grain texture "
              "with riso-print ink edges, flat poster layout with no photographic perspective, "
              "flat even lighting"),
        pal="cream field with tangerine and charcoal accents",
        cam=["seen slightly from above as stacked labels", "framed tight on the stamped badge",
             "viewed as an offset card peeking behind the hero card", "framed as a small badge centered in space",
             "seen as a corner-tucked label arrangement", "framed as a clean single-card impression"],
    ),
    "G-CMP": dict(
        head=("Duotone flat composition split by one hard vertical seam, mirrored structure on "
              "both sides, paper grain texture with riso-print ink edges, flat poster layout "
              "with no photographic perspective, flat even lighting"),
        pal="muted warm grey on one side and soft coral on the other",
        cam=["split vertically down the middle", "split with a diagonal seam",
             "split with the seam off-center to the left", "split as stacked halves",
             "split with a narrow center gutter", "split as a wide low-contrast seam"],
    ),
}

def rebuild(rec):
    sid = rec["id"].rsplit("-", 1)[0]
    if sid not in SUBSTYLE:
        return rec
    tile = rec["tile"]
    cfg = SUBSTYLE[sid]
    # 取原主体（去掉原 head 与 tail）
    body = rec["prompt"]
    m = re.search(r"one subject only: (.*?), (?:plain seamless|viewed|seen|framed|cropped|split)", body)
    if m:
        subject = m.group(1)
    else:
        subject = body.split("one subject only: ")[1].split(", ")[0]
    cam = cfg["cam"][tile - 1]
    rec["prompt"] = (
        f"{cfg['head']}, {cfg['pal']}, one subject only: {subject}, {cam}, "
        f"plain seamless backdrop in one flat {sid and ('ivory' if sid in ('G-DOC','G-CMP') else 'cream')} tone, "
        f"hero fills 70% of frame, bottom 25% clean for label scrim, locked seed and style "
        f"reference shared across all six tiles, 1:1, no text, no letters, no watermark")
    return rec

p = D / "p2-batch.jsonl"
recs = [json.loads(l) for l in p.read_text(encoding="utf-8").splitlines() if l.strip()]
n = 0
for r in recs:
    if r["variant"] == "hero-gallery":
        before = r["prompt"]
        rebuild(r)
        if r["prompt"] != before:
            n += 1
p.write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in recs) + "\n", encoding="utf-8")
print(f"p2-batch.jsonl 重建 L4 瓦片 {n} 条")
