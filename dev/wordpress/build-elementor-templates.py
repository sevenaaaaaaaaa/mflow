#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""build-elementor-templates.py — 把 18 个复刻页的 Elementor 数据转成模板库产物。

产出（outdir，默认 elem-templates/）：
  - lr-{short}-full.json            整页模板（template_type=page，全部容器）
  - lr-{short}-{nn}.json            单区块模板（template_type=container，一个容器）
  - manifest.json                   [{name, slug, type, file}] 供浏览器端逐个调
                                    admin-ajax lr_elem_template 导入

命名对齐站点现有模板库惯例（短 slug、英文标题）。区块短名从 HTML 微件内容的
首个 h1/h2/h3 提取，无标题时用结构标签（header/footer/nav/form）兜底。

用法：python3 build-elementor-templates.py [--src elem-src] [--out elem-templates]
"""
import argparse
import glob
import io
import json
import os
import re

SHORT = {
    "replica-homepage": "homepage",
    "replica-comparison-hub": "comparison",
    "replica-content-hub": "content",
    "replica-people-reviews": "people-reviews",
    "replica-product-launch": "product-launch",
    "replica-showcase-gallery": "showcase",
    "replica-tool-directory": "tool-directory",
    "composite-replica-all": "composite",
    "replica-solution-ai-design-solution-for-shopify": "shopify",
    "replica-solution-ai-design-solution-for-saas": "saas",
    "replica-solution-ai-design-solution-for-nonprofits": "nonprofits",
    "replica-solution-ai-design-solution-for-marketing-teams": "marketing-teams",
    "replica-solution-ai-design-solution-for-creators": "creators",
    "replica-solution-ai-design-solution-for-agencies": "agencies",
    "replica-solution-ai-design-for-small-business-hub": "small-biz",
    "replica-solution-ai-design-for-fitness-wellness-hub": "fitness",
    "replica-solution-good-design-for-marketers": "design-marketers",
    "replica-solution-good-design-for-business-owners": "design-owners",
}

TITLE = {
    "homepage": "Homepage", "comparison": "Comparison Hub", "content": "Content Hub",
    "people-reviews": "People Reviews", "product-launch": "Product Launch",
    "showcase": "Showcase Gallery", "tool-directory": "Tool Directory",
    "composite": "Composite All", "shopify": "Shopify Solution", "saas": "SaaS Solution",
    "nonprofits": "Nonprofits Solution", "marketing-teams": "Marketing Teams Solution",
    "creators": "Creators Solution", "agencies": "Agencies Solution",
    "small-biz": "Small Business Hub", "fitness": "Fitness & Wellness Hub",
    "design-marketers": "Design for Marketers", "design-owners": "Design for Business Owners",
}


def section_tag(container):
    """从容器 HTML 微件内容提取短名：首个标题文本，否则结构标签。"""
    html = ""
    for w in container.get("elements", []):
        s = w.get("settings", {}) or {}
        if w.get("widgetType") == "html" and s.get("html"):
            html = s["html"]
            break
    if not html:
        return "section"
    m = re.search(r"<h[1-3][^>]*>(.*?)</h[1-3]>", html, re.S)
    if m:
        text = re.sub(r"<[^>]+>", " ", m.group(1))
        text = re.sub(r"[^A-Za-z0-9 ]+", " ", text).strip().lower()
        words = text.split()[:4]
        if words:
            return "-".join(words)
    m = re.search(r"<(header|footer|nav|form|blockquote)\b", html)
    if m:
        return m.group(1)
    return "section"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", default="elem-src")
    ap.add_argument("--out", default="elem-templates")
    args = ap.parse_args()
    os.makedirs(args.out, exist_ok=True)

    manifest = []
    for f in sorted(glob.glob(os.path.join(args.src, "*.json"))):
        slug = os.path.basename(f)[:-5]
        short = SHORT.get(slug)
        if not short:
            print("skip unknown:", slug)
            continue
        d = json.load(io.open(f, encoding="utf-8"))
        version = d.get("version", "3.35.7")

        # 整页模板
        full_slug = "lr-%s-full" % short
        io.open(os.path.join(args.out, full_slug + ".json"), "w", encoding="utf-8").write(
            json.dumps({"version": version, "data": d["data"]}, ensure_ascii=False))
        manifest.append({
            "name": "LR %s \u2014 Full Page" % TITLE[short],
            "slug": full_slug, "type": "page", "file": full_slug + ".json",
        })

        # 单区块模板
        for i, c in enumerate(d["data"]):
            nn = "%02d" % (i + 1)
            ts = section_tag(c)
            cslug = "lr-%s-%s" % (short, nn)
            io.open(os.path.join(args.out, cslug + ".json"), "w", encoding="utf-8").write(
                json.dumps({"version": version, "data": [c]}, ensure_ascii=False))
            manifest.append({
                "name": "LR %s %s \u2014 %s" % (TITLE[short], nn, ts.replace("-", " ").title()),
                "slug": cslug, "type": "container", "file": cslug + ".json",
            })

    io.open(os.path.join(args.out, "manifest.json"), "w", encoding="utf-8").write(
        json.dumps(manifest, ensure_ascii=False, indent=1))
    print("manifest entries:", len(manifest),
          "(pages:", sum(1 for m in manifest if m["type"] == "page"),
          "sections:", sum(1 for m in manifest if m["type"] == "container"), ")")


if __name__ == "__main__":
    main()