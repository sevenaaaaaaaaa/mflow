#!/usr/bin/env python3
"""link-suggest.py — 从内容库自动找相关页做内链建议。
Usage: python3 link-suggest.py --file draft.md --site lovart-global --top 5
从 draft 中提取关键词 → 在 run/library/{site} 的 17.5k 篇中找最相关的页面 → 输出建议内链列表"""
import json, math, re, sys, argparse, collections
from pathlib import Path

def tokens(text):
    t = (text or "").lower()
    words = set(re.findall(r"[a-z0-9]{3,}", t))
    cjk = re.findall(r"[\u4e00-\u9fff]", t)
    bigrams = {"".join(cjk[i:i+2]) for i in range(len(cjk)-1)}
    return words | bigrams

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--file", required=True)
    ap.add_argument("--site", default="lovart-global")
    ap.add_argument("--top", type=int, default=5)
    a = ap.parse_args()

    draft = Path(a.file).read_text(encoding="utf-8")[:3000]
    dt = tokens(draft)
    if not dt:
        print(json.dumps({"suggestions": [], "note": "无法从草稿提取关键词"}))
        return

    base = Path("/www/wwwroot/mflow/run/library") / a.site
    if not base.exists():
        print(json.dumps({"suggestions": [], "note": "内容库不存在（先同步）"}))
        return

    hits = []
    for f in base.rglob("*.md"):
        if f.name.startswith("_"): continue
        name_t = tokens(f.stem.replace("-", " "))
        overlap = len(dt & name_t)
        if overlap < 2: continue
        # 计算 TF-IDF 简化分数
        score = overlap * math.log(1 + overlap)
        # 偏好同 section
        if f.parent.name in draft.lower():
            score *= 1.5
        # 排除同名（自身）
        if f.stem == Path(a.file).stem: continue
        hits.append((score, f, overlap))

    hits.sort(key=lambda x: -x[0])
    suggestions = []
    for score, f, in hits[:a.top]:
        rel = str(f)
        slug = f.stem
        section = f.parent.parent.name if f.parent.name.isalpha() else f.parent.parent.parent.name
        suggestions.append({"path": rel, "slug": slug, "section": section,
                            "relevance": round(score, 1),
                            "suggest_anchor": slug.replace("-", " ").title()[:60]})
    print(json.dumps({"suggestions": suggestions[:a.top], "total_scanned": len(hits)}, ensure_ascii=False, indent=1))

if __name__ == "__main__":
    main()
