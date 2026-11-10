#!/usr/bin/env python3
"""tmp_qc_v3.py — V3 专项质检：合规 + 高级感信号 + agent 覆盖 + 模板疲劳"""
import json, re, sys
from collections import Counter
from pathlib import Path

V3 = Path("/Users/seveno/MFlow Dev/mflow/harness/Docs/S3-内容创作/Hero封面批次-2026-11/v3")

BAN = ["gradient mesh", "glassmorphism", "chrome", "neon", "hologram", "holographic",
       "isometric", "fake ui", "glowing connection", "floating chip", "clip-art",
       "skeuomorph", "glitter", "snapshot look", "plastic sheen"]
RISK = ["screen", "monitor", "dashboard", "interface", "timeline", "keyboard", "toolbar"]
MATS = ["cold-pressed", "vellum", "newsprint", "cotton stock", "kraft", "coated stock",
        "wood-free", "linen", "nubuck", "bronze", "terracotta", "plaster", "oak",
        "aluminium", "stoneware", "concrete", "soapstone", "paper pulp", "silk"]
LIGHTS = ["north-facing window", "chiaroscuro", "softbox rim", "raking sidelight",
          "golden-hour", "vitrine light", "overcast", "task lamp", "HDRI", "rim light",
          "grazing light", "dome light", "proofing-room light", "practical light"]
SCENES = ["atelier", "print workshop", "archive drawer", "vitrine", "material library",
          "gallery wall", "proofing room", "plinth", "workbench", "pinboard", "bare desk",
          "classroom shelf", "studio volume", "commercial interior"]
AGENT = ["one brief, three deliverables", "raw then resolved", "completing itself",
         "repeated across four material grounds", "earlier drafts"]
ANCHORS = ["material truth", "one focal point only", "at most one accent"]


def main():
    files = sorted(V3.glob("*.jsonl"))
    allrecs = []
    print(f"{'file':<22}{'条数':>6}{'BLOCK':>7}{'WARN':>6}")
    print("-" * 44)
    grand_b = grand_w = 0
    for f in files:
        recs = [json.loads(l) for l in f.read_text(encoding="utf-8").splitlines() if l.strip()]
        b = w = 0
        for r in recs:
            p = r["prompt"].lower()
            errs, warns = [], []
            for t in ("no text", "no letters", "no watermark"):
                if t not in p:
                    errs.append(f"缺 {t}")
            for x in BAN:
                if x in p and not re.search(r"\b(no|without)\s+" + re.escape(x), p):
                    errs.append(f"禁词 {x}")
            for x in RISK:
                if re.search(r"\b" + x + r"\b", p) and "no screens" not in p:
                    errs.append(f"高危 {x}")
            for a in ANCHORS:
                if a not in p:
                    errs.append(f"缺锚定 {a}")
            if not re.search(r"\d+:\d+", p):
                errs.append("缺比例")
            if "material truth" in p and len(p) < 260:
                warns.append("prompt 过短")
            b += len(errs)
            w += len(warns)
            if errs:
                print(f"  ✗ {f.name}/{r['id']}: {errs[:2]}")
        grand_b += b
        grand_w += w
        print(f"{f.name:<22}{len(recs):>6}{b:>7}{w:>6}")
        allrecs += [{**r, "_f": f.name} for r in recs]
    print("-" * 44)
    print(f"{'合计':<22}{len(allrecs):>6}{grand_b:>7}{grand_w:>6}")

    # ── 覆盖度 ──
    txt = " ".join(r["prompt"].lower() for r in allrecs)
    n = len(allrecs)

    def cov(name, words):
        hit = Counter()
        for r in allrecs:
            p = r["prompt"].lower()
            for x in words:
                if x.lower() in p:
                    hit[x] += 1
        used = len(hit)
        print(f"\n{name}：{used}/{len(words)} 种被使用")
        for x, c in hit.most_common(6):
            print(f"    {c:>4}× {x}")
        unused = [x for x in words if x not in hit]
        if unused:
            print(f"    未用: {unused}")

    cov("材质", MATS)
    cov("布光", LIGHTS)
    cov("场景", SCENES)
    cov("Agent 隐喻", AGENT)

    # ── 模板疲劳 ──
    print("\n=== 模板短语（对比 v2）===")
    v2 = {"seamless": 83, "one flat": 77, "bottom 25%": 77, "70% of frame": 77}
    for ph, pct in v2.items():
        c = sum(1 for r in allrecs if ph in r["prompt"].lower())
        print(f"  {ph:<16} v2 {pct:>3}%  →  v3 {c*100//n:>3}%  ({c}/{n})")

    # ── 去重 ──
    prompts = Counter(r["prompt"] for r in allrecs)
    dup = [k[:50] for k, v in prompts.items() if v > 1]
    print(f"\n完全重复 prompt: {len(dup)}")
    for d in dup[:5]:
        print(f"  {d}")

    ids = Counter((r["_f"], r["id"]) for r in allrecs)
    print(f"同文件内 ID 重复: {[k for k,v in ids.items() if v>1] or '无'}")
    print(f"\n结论: {'通过' if grand_b == 0 and not dup else '有问题'}")


if __name__ == "__main__":
    main()
