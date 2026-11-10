#!/usr/bin/env python3
"""tmp_brief_qc.py — Hero 封面 brief 投喂前自动质检（v5，支持 media/gallery/toolTiles 三形态）

用法: python3 tmp_brief_qc.py <jsonl 文件路径>

BLOCK 级检查：
  1  结构：JSONL 可解析 / ID 唯一 / 必备字段
  2  规格：按 variant+field 校验尺寸比例
  3  no-text 三约束
  4  v2 禁词（"no X" 豁免）
  5  高风险 UI 词（未声明 no screens / abstract bars 则阻断）
  6  航道一致（token 命中 + 无跨航道冲突）
  7  瓦片必须单主体声明
  8  cinematic 三层 + 8% 渐隐
  9  mosaic 四状态 + locked seed + lower 30%
 10  gallery 瓦片机位互异（同套内不得重复机位）
 11  含排版品类必须声明"抽象条块代替文字"
WARN 级：
  alt 长度 / 主题词关联 / 复杂度信号
"""
import json, re, sys
from collections import Counter, defaultdict

BANNED = ["gradient mesh", "glassmorphism", "chrome", "neon", "hologram",
          "floating 3d blob", "isometric", "startup illustration", "fake ui",
          "ui screen", "glowing connection", "floating chip", "collage of",
          "clip-art", "skeuomorph", "glitter", "plastic sheen", "video-game render",
          "theme-park", "hdr over", "stock-photo pose", "snapshot look"]
RISKY_UI = ["screen", "monitor", "dashboard", "interface", "timeline", "chart",
            "infographic", "keyboard", "menu bar", "toolbar", "app window",
            "browser window"]
RISKY_COMPLEX = ["grid of", "rows of", "dozens of", "many ", "various ",
                 "assorted ", "collection of", "array of", "scattered"]

LANE_TOKENS = {
    "L1-photo-editorial": ["commercial photograph", "editorial photograph", "85mm", "100mm", "seamless"],
    "L2-cinematic-still": ["35mm", "cinematic still", "film grain", "volumetric"],
    "L3-soft-3d": ["soft-body 3d", "matte ceramic", "hdri", "contact shadow"],
    "L4-graphic-flat": ["flat-graphic", "swiss grid", "paper grain", "riso"],
    "L5-material-still-life": ["still-life", "macro", "raking", "seamless"],
    "L6-paper-craft": ["paper-craft", "diorama", "hand-cut"],
}
LANE_CONFLICT = {
    "L1-photo-editorial": ["3d render", "flat-graphic", "paper-craft"],
    "L2-cinematic-still": ["3d render", "flat-graphic", "studio hdri"],
    "L3-soft-3d": ["photograph", "35mm film", "flat-graphic"],
    "L4-graphic-flat": ["photograph", "3d render", "depth of field", "bokeh"],
    "L5-material-still-life": ["3d render", "flat-graphic", "paper-craft"],
    "L6-paper-craft": ["photograph", "3d render"],
}
VARIANT_SPEC = {
    ("hero-split", None): (2160, 1620, "4:3"),
    ("hero-cinematic", None): (2400, 1500, "16:10"),
    ("hero-mosaic", None): (1200, 900, "4:3"),
    ("hero-gallery", "gallery"): (1200, 1200, "1:1"),
    ("hero-gallery", "toolTiles"): (1200, 1200, "1:1"),
    ("hero-gallery", "media"): (2160, 1350, "16:10"),
}
# 含排版语义的品类：必须出现"抽象条块代替文字"声明
TYPE_CATS = {"poster", "banner", "menu", "brochure", "packaging", "video-thumbnail",
             "social-media", "product-detail", "ppt", "resume", "infographic"}
TYPE_DECL = "abstract grey bars"


def has_negated(text, word):
    for m in re.finditer(re.escape(word), text):
        head = text[max(0, m.start() - 14):m.start()].lower()
        if not re.search(r"\b(no|without|free of)\s*$", head):
            return False
    return True


def check(rec):
    errs, warns = [], []
    need = {"id", "variant", "lane", "w", "h", "ratio", "prompt", "alt"}
    if not need <= set(rec):
        return [f"缺字段: {sorted(need - set(rec))}"], warns
    p = rec["prompt"].lower()
    variant, field = rec["variant"], rec.get("field")

    spec = VARIANT_SPEC.get((variant, field)) or VARIANT_SPEC.get((variant, None))
    if spec and (rec["w"], rec["h"], rec["ratio"]) != spec:
        errs.append(f"规格不符: {variant}/{field} 应为 {spec}，实际 ({rec['w']},{rec['h']},{rec['ratio']})")

    for t in ("no text", "no letters", "no watermark"):
        if t not in p:
            errs.append(f"缺约束 '{t}'")

    for w in BANNED:
        if w in p and not has_negated(p, w):
            errs.append(f"禁词 '{w}'")

    risky = [w for w in RISKY_UI if re.search(r"\b" + re.escape(w) + r"\b", p) and not has_negated(p, w)]
    if risky:
        if "no screens" in p or "no ui" in p:
            warns.append(f"高风险词（已声明 no screens）: {risky}")
        else:
            errs.append(f"高风险词未声明 no screens: {risky}")

    lane = rec["lane"]
    toks = LANE_TOKENS.get(lane, [])
    if toks and not any(t in p for t in toks):
        errs.append(f"航道 {lane} token 缺失")
    for w in LANE_CONFLICT.get(lane, []):
        if w in p and not has_negated(p, w):
            errs.append(f"航道冲突词 '{w}'")

    if variant in ("hero-mosaic", "hero-gallery") and field != "media" and "one subject" not in p:
        errs.append("瓦片必须声明 one subject")

    if variant == "hero-cinematic":
        if not re.search(r"(foreground|three layers|three-layer)", p):
            errs.append("cinematic 缺三层深度")
        if "8% fading" not in p and "8% fade" not in p:
            errs.append("cinematic 缺 8% 渐隐")

    if variant == "hero-mosaic":
        if not re.search(r"state \d of a 4-step sequence", p):
            errs.append("mosaic 缺 state N of 4")
        if "locked seed" not in p:
            errs.append("mosaic 缺 locked seed")
        if "lower 30%" not in p:
            errs.append("mosaic 缺 lower 30%")

    # gallery 瓦片：含排版品类必须声明抽象条块
    if field == "gallery":
        if "locked seed" not in p:
            errs.append("gallery 缺 locked seed 声明")
        if rec.get("theme") in TYPE_CATS and TYPE_DECL not in p:
            errs.append(f"含排版品类 {rec.get('theme')} 未声明 '{TYPE_DECL}'")

    for w in RISKY_COMPLEX:
        if w in p:
            warns.append(f"复杂度信号 '{w.strip()}'")

    alt = rec["alt"]
    if not (8 <= len(alt) <= 160):
        warns.append(f"alt 长度 {len(alt)} 异常")
    return errs, warns


def main(path):
    lines = [l for l in open(path, encoding="utf-8").read().splitlines() if l.strip()]
    recs, parse_err = [], []
    for i, l in enumerate(lines, 1):
        try:
            recs.append(json.loads(l))
        except Exception as e:
            parse_err.append((i, str(e)[:60]))

    ids = Counter(r.get("id") for r in recs)
    dup = [k for k, v in ids.items() if v > 1]
    prompts = Counter(r.get("prompt") for r in recs)
    dup_p = [k[:50] for k, v in prompts.items() if v > 1]

    # 同套机位互异检查（gallery 瓦片）
    cam_dupe = []
    by_set = defaultdict(list)
    for r in recs:
        if r.get("field") == "gallery":
            by_set[r.get("theme")].append(r)
    for theme, group in by_set.items():
        if len(group) < 2:
            continue
        cams = []
        for r in group:
            m = re.search(r"(viewed [^,]+|seen [^,]+|cropped [^,]+|shown [^,]+|placed [^,]+|"
                          r"overlapping [^,]+|bled [^,]+|isolated [^,]+|arranged [^,]+|layered [^,]+)", r["prompt"])
            cams.append(m.group(1) if m else "?")
        for cam, n in Counter(cams).items():
            if n > 1 and cam != "?":
                cam_dupe.append(f"{theme}: 机位重复 {n}× '{cam}'")

    total_e = total_w = 0
    print(f"文件: {path}")
    print(f"行数 {len(lines)} | 解析失败 {len(parse_err)} | ID 重复 {dup or '无'} | Prompt 重复 {len(dup_p)}")
    print(f"variant×field: {dict(Counter((r.get('variant'), r.get('field')) for r in recs))}")
    print("-" * 74)
    for r in recs:
        errs, warns = check(r)
        total_e += len(errs); total_w += len(warns)
        if errs or warns:
            tag = "BLOCK" if errs else "WARN"
            print(f"[{tag}] {r.get('id')}")
            for e in errs: print(f"    ✗ {e}")
            for w in warns: print(f"    △ {w}")
    if cam_dupe:
        print(f"\n[机位重复]")
        for c in cam_dupe:
            print(f"    ✗ {c}")
    print("-" * 74)
    extra = len(cam_dupe)
    ok = total_e == 0 and extra == 0 and not dup and not parse_err
    print(f"合计: BLOCK {total_e + extra} / WARN {total_w} → "
          f"{'通过（可投喂）' if ok else '未通过'}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
