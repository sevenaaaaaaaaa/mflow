#!/usr/bin/env python3
"""tmp_gen_e4e5.py — E4 hero-journey media 大图 + E5 cinematic 视频版 prompt"""
import json
from pathlib import Path

D = Path("/Users/seveno/MFlow Dev/mflow/harness/Docs/S3-内容创作/Hero封面批次-2026-11")
B = D / "batches"
B.mkdir(exist_ok=True)

L1 = ("High-end editorial photograph, 85mm shallow depth of field, soft key light from "
      "the upper left with a gentle contact shadow")
L2 = ("Cinematic still, shot on 35mm film, strictly a two-color teal-and-amber palette "
      "with soft volumetric light and subtle film grain")

# ── E4: journey media（按页面语义去重，7 张）──
JOURNEY = [
    ("ai-design-solution-for-nonprofits", "journey-nonprofits",
     "a warm community scene: a small notice board with pinned printed posters beside a stack of folded flyers, "
     "people's hands not visible, sense of shared mission",
     "L1", "Nonprofits / 公益组织"),
    ("ai-design-solution-for-shopify", "journey-shopify",
     "a product launch desk: one product box, a fanned set of printed campaign sheets and a small packaging sleeve, "
     "ready-to-ship arrangement",
     "L1", "Shopify / 电商独立站"),
    ("ai-design-for-small-business-hub", "journey-small-business",
     "a small shopfront counter: a printed menu stand, a stack of loyalty cards and one framed promo poster",
     "L1", "Small business / 小微企业"),
    ("zh-designer-expensive", "journey-designer-cost",
     "a designer's desk with a rolled-up plan sheet, a price list card and a single pen, restrained and quiet",
     "L1", "中文：设计师太贵"),
    ("zh-pricing-cn", "journey-pricing-cn",
     "a tidy pricing board: three stacked tier cards of increasing thickness on a warm surface, no numbers visible",
     "L1", "中文：定价"),
    ("zh-pricing-compare", "journey-pricing-compare",
     "two plan cards side by side under even light, the left thinner, the right with more layered inserts",
     "L1", "中文：定价对比"),
    ("zh-solution-ecommerce", "journey-ecommerce",
     "a cross-border commerce desk: a product on a small podium, a printed listing sheet and a shipping label sheet, "
     "clean commerce energy",
     "L1", "中文：电商解决方案（5 页共用）"),
]

# ── E5: cinematic 视频版（5 条，配 B 系列）──
VIDEO = [
    ("C-PLA", "platform",
     "A slow dolly-in across a long warm-grey workbench: a brief card slides into a rounded slot, then three finished "
     "artworks fade in one after another on a shallow tray, matte ceramic materials, one soft coral light source "
     "pulsing gently, warm-grey palette with one coral accent, soft HDRI lighting, 8 seconds, locked-off ending, "
     "no text, no letters, no watermark, no screens"),
    ("C-IMG", "image-gen",
     "A slow lateral truck across a sunlit painter's studio: window light sweeps over one large landscape painting "
     "on an easel as brushes in the foreground drift softly out of focus, warm neutral palette with one saturated "
     "accent inside the painting, 85mm, 8 seconds, no text, no letters, no watermark"),
    ("C-ECO", "ecommerce",
     "A slow orbit around a matte ceramic bottle on a sand podium while a white listing cutout card rotates into "
     "frame behind it, sand and cream palette with one deep-green accent, single key light with gentle falloff, "
     "8 seconds, no text, no letters, no watermark"),
    ("C-LOG", "logo-brand",
     "Raking light travels slowly across a row of upright embossed brand cards, the copper foil catching and releasing "
     "the highlight, ivory and charcoal palette, macro 100mm, shallow depth of field, 8 seconds, "
     "no text, no letters, no watermark"),
    ("C-IND", "industry",
     "A slow push-in toward a matte standing board holding three printed design proofs, the blurred commercial "
     "interior behind it easing into focus at the very end, neutral palette with one warm accent, 85mm, 8 seconds, "
     "no text, no letters, no watermark, no screens"),
]


def main():
    e4 = []
    for slug, jid, scene, lane, zh in JOURNEY:
        head = L1 if lane == "L1" else L2
        e4.append({
            "id": f"JM-{jid}", "priority": "P3", "series": "E4-journey-media",
            "theme": jid, "theme_label": zh, "lane": "L1-photo-editorial",
            "variant": "hero-journey", "field": "media",
            "w": 2160, "h": 1350, "ratio": "16:10",
            "pages": 13,
            "prompt": (f"{head}, wide establishing shot: {scene}, "
                       f"the scene fills about 65% of frame with calm negative space at the top and bottom, "
                       f"16:10, top and bottom 8% fading to a neutral backdrop, "
                       f"no text, no letters, no watermark, no screens"),
            "alt": f"Lovart {zh} — journey hero visual",
        })
    (B / "E4-journey-media.jsonl").write_text(
        "\n".join(json.dumps(r, ensure_ascii=False) for r in e4) + "\n", encoding="utf-8")

    e5 = []
    for cid, theme, motion in VIDEO:
        e5.append({
            "id": f"V-{cid[2:]}", "priority": "P3", "series": "E5-cinematic-video",
            "theme": theme, "lane": "L2-cinematic-still",
            "variant": "hero-cinematic", "field": "video",
            "w": 2400, "h": 1500, "ratio": "16:10", "duration_s": 8,
            "prompt": (f"{L2} — {motion}, composed in three depth layers (foreground, midground, background) "
                       f"with at most one hero element per layer, 16:10, top and bottom 8% fading to a neutral "
                       f"backdrop to match the static poster frame"),
            "alt": f"Lovart {theme} — cinematic hero motion",
            "notes": "8s 静音循环 MP4 ≤8MB；需与对应 C-* 静帧同构图，用静帧作 poster",
        })
    (D / "E5-cinematic-video.jsonl").write_text(
        "\n".join(json.dumps(r, ensure_ascii=False) for r in e5) + "\n", encoding="utf-8")

    print(f"E4 journey media: {len(e4)} 张")
    print(f"E5 cinematic video: {len(e5)} 条")


if __name__ == "__main__":
    main()
