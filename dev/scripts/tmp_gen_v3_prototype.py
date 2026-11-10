#!/usr/bin/env python3
"""tmp_gen_v3_prototype.py — v3 原型：选 8 条代表性 brief 重写，对比 v2/v3

选样覆盖：split / cinematic / mosaic / gallery-tiles / module(feature-detail)
"""
import json
from pathlib import Path

D = Path("/Users/seveno/MFlow Dev/mflow/harness/Docs/S3-内容创作/Hero封面批次-2026-11")

ANCHOR = ("material truth with visible surface texture, one focal point only, "
          "muted base palette with at most one accent")
SAFE = "edges safe for rounded-corner crop, no text, no letters, no watermark, no screens, no UI windows"

# ── v3 组件库（与 prompt-v3-premium-agentic.md 对齐）──
MATERIAL = {
    "cold-pressed paper": "cold-pressed watercolor paper with visible fibre",
    "raw linen": "raw unbleached linen with visible weave and thickness",
    "anodized aluminium": "bead-blasted anodized aluminum with a fine matte grain",
    "terracotta": "unglazed terracotta with a chalky, slightly uneven surface",
    "marble plaster": "marble plaster with a faint granular tooth",
    "nubuck leather": "nubuck leather with a soft nap that catches the light",
    "brushed bronze": "brushed bronze with directional micro-scratches",
    "translucent vellum": "translucent vellum that glows at the edges",
    "silkscreen ink": "silkscreen ink with a visible halftone dot",
    "solid oak": "solid oak with an open grain and hand-sanded edges",
}
LIGHT = {
    "north window": "north-facing window light, soft and directional",
    "chiaroscuro": "single-source chiaroscuro with deep falloff from the upper left",
    "softbox rim": "softbox rim light defining the silhouette against a darker ground",
    "raking": "raking sidelight that reveals every surface texture",
    "golden hour": "golden-hour backlight with a faint lens bloom",
    "vitrine": "museum vitrine light, tight and clinical",
    "overcast": "overcast daylight, even and almost shadowless",
    "lamp pool": "one practical task lamp pooling light on the subject",
}
SCENE = {
    "atelier": "a designer's atelier bench with tools pushed to the edges of frame",
    "print shop": "a print workshop bench with ink-stained felt",
    "archive": "an open archive drawer of filed material samples",
    "vitrine": "a museum vitrine with a glass edge catching a sliver of light",
    "material library": "a material library of labelled swatch boards",
    "gallery wall": "a gallery wall with one piece hung and the rest bare",
    "proofing room": "a proofing room with colour charts pinned to the wall",
    "seamless": "a seamless tonal field with no environment",
}

PROTO = [
    # ── 1. S-PLA：split / platform / M1 并行产出 ──
    dict(id="S-PLA", variant="hero-split", ratio="4:3", w=2160, h=1620,
         v3=("Soft-body 3D render in bead-blasted anodized aluminum and unglazed terracotta, "
             "single-source chiaroscuro with deep falloff from the upper left, the scene set on a "
             "designer's atelier bench with tools pushed to the edges of frame, one folded-corner "
             "brief card entering a machined slot while three finished pieces stand beside it in "
             "different media — a cotton-paper print, a linen swatch panel, a bronze-edged plaque — "
             "one brief, three deliverables, rendered at an equivalent 50mm perspective, "
             f"{ANCHOR}, muted warm-grey base with at most one coral accent, "
             f"4:3, {SAFE}"),
         alt="Lovart design agent turning one brief into deliverables across three media"),

    # ── 2. S-VID：split / video / M2 转化序列 ──
    dict(id="S-VID", variant="hero-split", ratio="4:3", w=2160, h=1620,
         v3=("Cinematic still shot on 35mm film with subtle grain, strictly a two-color teal-and-amber "
             "palette, golden-hour backlight with a faint lens bloom, laid on a print workshop bench "
             "with ink-stained felt, a single film strip held by hand-sanded oak pegs showing three "
             "progressive states of the same scene — raw frame, graded frame, finished frame — "
             "shallow depth of field at 50mm, "
             f"{ANCHOR}, 4:3, {SAFE}"),
         alt="Lovart video agent grading one scene from raw frame to finished frame"),

    # ── 3. C-LOG：cinematic / logo-brand / M4 跨媒介并置 ──
    dict(id="C-LOG", variant="hero-cinematic", ratio="16:10", w=2400, h=1500,
         v3=("Cinematic still, strictly a two-color ivory-and-charcoal palette with one brass accent, "
             "museum vitrine light, tight and clinical, a single abstract mark repeated across four "
             "material grounds of the same size — cold-pressed paper, raw linen, brushed bronze, "
             "translucent vellum — each catching the light differently, arranged in a precise row "
             "inside a vitrine, three depth layers with the vellum nearest the glass, "
             f"16:10, top and bottom 8% fading to a neutral ground, {ANCHOR}, {SAFE}"),
         alt="Lovart brand agent applying one mark across four material grounds"),

    # ── 4. M-PLA-2：mosaic / platform / M3 无人值守 ──
    dict(id="M-PLA-2", variant="hero-mosaic", ratio="4:3", w=1200, h=900,
         v3=("Soft-body 3D render in unglazed terracotta and bead-blasted aluminum, raking sidelight "
             "that reveals every surface texture, on a designer's atelier bench, state 2 of a 4-step "
             "sequence on the same machined console: the brief card caught mid-insertion, its leading "
             "edge already inside the slot, the card bending very slightly as it goes in on its own, "
             "single-source chiaroscuro, "
             f"{ANCHOR}, muted warm-grey base with at most one coral accent, "
             f"4:3, lower 30% kept visually simple for caption overlay, {SAFE}"),
         alt="Lovart agent mid-generation — brief card entering the machine"),

    # ── 5. G-logo-01：gallery tile / 国潮 / 材质升级 ──
    dict(id="G-logo-01", variant="hero-gallery", ratio="1:1", w=1200, h=1200,
         v3=("Editorial still life on a Swiss grid with hand-cut paper edges and a visible halftone "
             "dot, vermilion ink on cold-pressed watercolor paper with a carved seal impression, "
             "north-facing window light, soft and directional, set on a material library bench with "
             "labelled swatch boards receding out of focus, one geometric mark rendered as a blind "
             "letterpress impression with one vermilion ink layer registered slightly off — the "
             "traditional misregistration kept as intent, viewed straight on and perfectly centered, "
             f"{ANCHOR}, ivory base with at most one vermilion accent, "
             f"1:1, bottom 25% kept clean for label overlay, {SAFE}"),
         alt="Lovart 国潮 logo 设计 — 盲压凹凸与朱红错版印刷"),

    # ── 6. G-poster-03：gallery tile / 餐饮 / 排版抽象化 ──
    dict(id="G-poster-03", variant="hero-gallery", ratio="1:1", w=1200, h=1200,
         v3=("Editorial still life of a poster layout, silkscreen ink on cold-pressed paper with a "
             "visible halftone dot, raking sidelight that reveals every surface texture, pinned to a "
             "gallery wall with the rest of the wall bare, the poster caught half-way through being "
             "mounted, one corner still lifting, its typographic hierarchy suggested only by abstract "
             "grey bars and shape blocks, never legible characters, warm terracotta base with at most "
             "one cream accent, "
             f"{ANCHOR}, 1:1, bottom 25% kept clean for label overlay, {SAFE}"),
         alt="Lovart 餐饮海报设计 — 丝网印与半贴墙状态"),

    # ── 7. feature-detail-01：module / M5 迭代层叠 ──
    dict(id="feature-detail-01", variant="feature-detail", ratio="4:3", w=1600, h=1200,
         v3=("High-end editorial photograph, north-facing window light, soft and directional, on a "
             "proofing room bench with colour charts pinned to the wall behind, one index card with a "
             "folded corner laid precisely on top of three earlier drafts fanned beneath it at even "
             "intervals — the iteration stack readable as depth, shallow depth of field at 85mm "
             "falling off across the stack, "
             f"{ANCHOR}, warm grey base with at most one coral accent, "
             f"4:3, the subject placed left with calm negative space at right for body copy, {SAFE}"),
         alt="Lovart agent iterating from a brief — drafts stacked under the final card"),

    # ── 8. comparison-before-after-02：module / 高级感对比 ──
    dict(id="comparison-before-after-02", variant="comparison-before-after",
         ratio="16:9", w=1600, h=900,
         v3=("High-end editorial photograph, raking sidelight that reveals every surface texture, "
             "on a print workshop bench, one photographic print split exactly down the centre: the "
             "left half soft and unresolved under a dull overcast wash, the right half resolving into "
             "crisp medium-format detail with true colour, the split line falling on the same object "
             "edge in both halves, "
             f"{ANCHOR}, neutral base with at most one accent on the resolved side, "
             f"16:9, {SAFE}"),
         alt="Lovart before and after — from unresolved capture to medium-format detail"),

    # ── 9. bento-2-01：module / 静物 + 环境记忆 ──
    dict(id="bento-2-01", variant="bento-2", ratio="16:10", w=1600, h=1000,
         v3=("High-end commercial photograph, softbox rim light defining the silhouette against a "
             "darker ground, set on a material library bench with labelled swatch boards receding out "
             "of focus, one product on a nubuck leather pad with a single linen swatch folded beside "
             "it, the product freshly placed rather than arranged, 85mm shallow depth of field, "
             f"{ANCHOR}, muted sand base with at most one deep-green accent, "
             f"16:10, {SAFE}"),
         alt="Lovart ecommerce visual — product on leather with material reference"),

    # ── 10. canvas-wall-01：module / 大卡 / 艺术级 ──
    dict(id="canvas-wall-01", variant="canvas-wall", ratio="16:10", w=1600, h=1000,
         v3=("High-end editorial photograph, museum vitrine light, tight and clinical, one large "
             "framed artwork hung on a gallery wall with the rest of the wall bare, the frame in "
             "hand-sanded oak with a linen liner, the print on cold-pressed paper showing its deckled "
             "edge inside the mount, camera at an equivalent 50mm straight on, "
             f"{ANCHOR}, warm white base with at most one accent inside the artwork, "
             f"16:10, {SAFE}"),
         alt="Lovart canvas example — framed print on a gallery wall"),
]


def main():
    out = []
    for p in PROTO:
        out.append({
            "id": p["id"], "variant": p["variant"],
            "w": p["w"], "h": p["h"], "ratio": p["ratio"],
            "prompt": p["v3"], "alt": p["alt"],
            "note": "v3 原型：材质/布光/场景/agent 隐喻四层变量 + 三层锚定",
        })
    f = D / "v3-prototype.jsonl"
    f.write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in out) + "\n", encoding="utf-8")
    print(f"v3 原型: {len(out)} 条 → {f.name}")

    # 对比统计
    import re
    from collections import Counter
    v3_text = " ".join(r["prompt"] for r in out).lower()
    print("\n=== v3 原型覆盖检查 ===")
    checks = {
        "材质多样性": ["watercolor paper", "linen", "anodized aluminum", "terracotta",
                       "nubuck leather", "brushed bronze", "vellum", "silkscreen", "oak", "plaster"],
        "布光多样性": ["north-facing window", "chiaroscuro", "softbox rim", "raking",
                       "golden-hour", "vitrine", "overcast", "task lamp"],
        "场景记忆": ["atelier", "print workshop", "archive", "vitrine", "material library",
                     "gallery wall", "proofing room"],
        "agent 隐喻": ["one brief, three deliverables", "progressive states",
                       "repeated across four material grounds", "on its own",
                       "caught half-way through being mounted", "iteration stack",
                       "drafts stacked"],
        "锚定声明": ["material truth", "one focal point only", "at most one"],
    }
    for name, words in checks.items():
        hit = [w for w in words if w in v3_text]
        print(f"  {name}: {len(hit)}/{len(words)} → {hit}")

    # 模板疲劳对比
    print("\n=== 模板短语（v2 高频 vs v3 原型）===")
    for ph in ["seamless", "one flat", "bottom 25%", "70% of frame", "swiss grid"]:
        n = v3_text.count(ph)
        print(f"  {ph:<18} v3 出现 {n} 次 / 10 条")


if __name__ == "__main__":
    main()
