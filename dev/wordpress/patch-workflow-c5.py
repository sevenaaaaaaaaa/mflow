#!/usr/bin/env python3
"""patch-workflow-c5.py — C5：给 9 块已迁 timeline 的空步骤 2/3 描述填真内容。

背景
----
源站 hydration 缺失导致 9 页 workflow 块抓取时步骤 2/3 描述为空，
迁移时按「如实迁移不劣化」原则留空（线上现状渲染同样为空）。
本脚本按各页 hero 主题把 18 段描述补进 elem-migrated/*.json 的
htmega-verticletimeline-addons 微件（content_text 字段）。

匹配双保险：页面 slug + content_title 必须同时命中才填充；
只填空行，已有内容一律不碰。幂等，可重跑。

用法：python3 patch-workflow-c5.py            # 预演
      python3 patch-workflow-c5.py --write    # 真写
"""
import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "elem-migrated"

# slug（去 replica- 前缀）→ 步骤标题 → 描述（文风对齐 small-business/agencies 基准块）
C5 = {
    "composite": {
        "Generate the conversion asset set":
            "Product shots, ad sets, and channel banners generated in one pass.",
        "Refine with precise editing":
            "Touch Edit to swap copy, crops, and variants; export in channel-ready sizes.",
    },
    "content-hub": {
        "Generate the conversion asset set":
            "Ad creative, email headers, and PDP refreshes for every step from click to repeat purchase.",
        "Refine with precise editing":
            "Touch Edit to localize copy and layout; ship the winning version everywhere.",
    },
    "solution-ai-design-for-fitness-wellness-hub": {
        "Generate class and member campaigns":
            "Class schedules, seasonal promos, and member challenges in your studio style.",
        "Refine and publish":
            "Touch Edit to update times and offers; export for social, email, and in-studio screens.",
    },
    "solution-ai-design-solution-for-creators": {
        "Get on-brand assets for every channel":
            "Thumbnails, covers, and campaign visuals matched to your channel voice.",
        "Easily change anything with AI editing":
            "Touch Edit to remix hooks and captions; publish the version that pops.",
    },
    "solution-ai-design-solution-for-marketing-teams": {
        "Distribute production to channel owners":
            "Channel owners generate in their own Brand Kit spaces — on brand by default.",
        "Test, approve, and scale winners":
            "Review, approve, and scale the winners; permissions keep brand rules locked.",
    },
    "solution-ai-design-solution-for-saas": {
        "Generate the launch asset set":
            "Launch pages, release graphics, and lifecycle emails rendered from your GTM context.",
        "Iterate and localize":
            "Touch Edit per market and release; export locale-ready sets for every launch.",
    },
    "solution-ai-design-solution-for-shopify": {
        "Generate the conversion asset set":
            "PDP banners, ad sets, and email headers generated from the SKU context.",
        "Refine, test, and export":
            "Touch Edit to match the drop; A/B test variants and export in ad-ready sizes.",
    },
    "solution-good-design-for-business-owners": {
        "On-brand assets for every channel":
            "Store banners, social posts, and promo creatives for every channel you sell on.",
        "Easily change anything with AI editing":
            "Touch Edit when prices or promos change; publish the update everywhere.",
    },
    "solution-good-design-for-marketers": {
        "Get on-brand assets for every channel":
            "Ad variants and channel assets generated against the brief you uploaded.",
        "Easily change anything with AI editing":
            "Touch Edit to tune hook and offer; ship variants for every test cell.",
    },
}


def slugify(fname):
    s = fname[:-5] if fname.endswith(".json") else fname
    for pre in ("replica-", "lr-demo-native-", "lr-demo-faithful-"):
        if s.startswith(pre):
            s = s[len(pre):]
            break
    if s == "composite-replica-all":
        s = "composite"
    return s


def walk(nodes, fn):
    for n in nodes:
        if n.get("widgetType") == "htmega-verticletimeline-addons":
            fn(n)
        walk(n.get("elements") or [], fn)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true")
    args = ap.parse_args()

    total_pages, total_rows = 0, 0
    for f in sorted(OUT.glob("*.json")):
        slug = slugify(f.name)
        table = C5.get(slug)
        if not table:
            continue
        raw = json.loads(f.read_text(encoding="utf-8"))
        data = raw.get("data") if isinstance(raw, dict) else raw
        filled, miss = [], []

        def fn(node):
            rows = (node.get("settings") or {}).get("custom_content_list") or []
            for r in rows:
                if not isinstance(r, dict):
                    continue
                title = (r.get("content_title") or "").strip()
                desc = table.get(title)
                if desc is None:
                    continue
                if (r.get("content_text") or "").strip():
                    continue  # 已有内容，不碰
                r["content_text"] = desc
                filled.append(title)

        walk(data, fn)
        # 命中校验：表里每个标题都要被填（防 slug 错配静默漏填）
        want = set(table)
        miss = want - set(filled)
        if filled:
            total_pages += 1
            total_rows += len(filled)
            print(f"  ✓ {f.name:<58} 填 {len(filled)} 段"
                  + (f"  ⚠ 未命中: {miss}" if miss else ""))
            if args.write:
                f.write_text(json.dumps(raw, ensure_ascii=False, separators=(",", ":")),
                             encoding="utf-8")
        elif miss:
            print(f"  ✗ {f.name:<58} 表里 {len(want)} 个标题一个都没命中——slug 错配，查表！")

    print(f"\n{'写入' if args.write else '预演'}：{total_pages} 页 / {total_rows} 段")
    if total_rows != 18:
        print(f"  ⚠ 预期 18 段（9 页 × 2），实际 {total_rows}——先核对再部署")
    return 0


if __name__ == "__main__":
    sys.exit(main())
