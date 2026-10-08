#!/usr/bin/env python3
"""merge-live-css.py — 把 ego-browser 从 lovart.ai 现场抓的 CSS chunks 合并进 canonical base。

用途：补齐 base 快照缺失的组件样式（如 prompt-to-images 系列）。
- 去重：按序列化后的规则文本哈希，base 优先。
- 字体路径：url(../media/x) → 绝对 https://web-static3.lovart.ai/...（与 Round 32 序列化处理一致）。
- 输出合并后的 canonical CSS 供 scope-css.py 作用域化。

用法：
  python3 merge-live-css.py --base /tmp/replica-base.css \
      --live /tmp/live-css-chunks.json --out /tmp/replica-base-merged.css
"""
import argparse
import hashlib
import re

import tinycss2

MEDIA_BASE = "https://web-static3.lovart.ai/lovart_prd/static/_next/static/media/"


def absolutize_fonts(css):
    # chunk 位于 _next/static/chunks/，相对 ../media/xxx → 绝对
    css = re.sub(r"url\(\s*['\"]?\.\./media/", f"url({MEDIA_BASE}", css)
    css = re.sub(r"url\(\s*['\"]?/lovart_prd/static/_next/static/media/", f"url({MEDIA_BASE}", css)
    return css


def iter_rules(css):
    for node in tinycss2.parse_stylesheet(css, skip_comments=True, skip_whitespace=True):
        if node.type == "qualified-rule":
            yield tinycss2.serialize([node])
        elif node.type == "at-rule":
            # @media/@supports/@layer 等整块按文本哈希；顶层重复的整块也去重
            yield tinycss2.serialize([node])
        # parse error 等忽略


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", required=True)
    ap.add_argument("--live", required=True, help="live-css-chunks.json（数组的 CSS 文本）")
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    import json
    base = open(args.base, encoding="utf-8").read()
    live_chunks = json.load(open(args.live, encoding="utf-8"))

    seen, out = set(), []
    stats = {"base": 0, "live_new": 0, "live_dup": 0}
    for src, text in [("base", base)] + [("live", absolutize_fonts(c)) for c in live_chunks]:
        for rule in iter_rules(text):
            h = hashlib.sha1(rule.encode()).hexdigest()
            if h in seen:
                if src == "live":
                    stats["live_dup"] += 1
                continue
            seen.add(h)
            out.append(rule)
            stats["base" if src == "base" else "live_new"] += 1

    merged = absolutize_fonts("\n".join(out))
    open(args.out, "w", encoding="utf-8").write(merged + "\n")
    print(f"merged: base={stats['base']} live_new={stats['live_new']} live_dup={stats['live_dup']} → {args.out}")


if __name__ == "__main__":
    main()