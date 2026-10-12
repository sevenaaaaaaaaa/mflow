#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""verify-render.py — 全站 16 页服务端渲染验证：各微件块计数。"""
import importlib.util
import json
import re

spec = importlib.util.spec_from_file_location("dm", "deploy-migrated.py")
dm = importlib.util.module_from_spec(spec)
spec.loader.exec_module(dm)

op = dm.build_opener()
dm.login(op)

PAGES = ["replica-solution-ai-design-solution-for-shopify",
         "replica-solution-ai-design-solution-for-agencies",
         "replica-solution-ai-design-solution-for-creators",
         "replica-solution-ai-design-solution-for-marketing-teams",
         "replica-solution-ai-design-solution-for-nonprofits",
         "replica-solution-ai-design-solution-for-saas",
         "replica-solution-ai-design-for-small-business-hub",
         "replica-solution-ai-design-for-fitness-wellness-hub",
         "replica-solution-good-design-for-business-owners",
         "replica-solution-good-design-for-marketers",
         "replica-comparison-hub", "replica-content-hub", "replica-people-reviews",
         "replica-product-launch", "replica-showcase-gallery", "replica-tool-directory"]
# 备用：真 slug 从 deploy-migrated 的映射拿
try:
    slugs = list(dm.PAGES.keys()) if hasattr(dm, "PAGES") else PAGES
except Exception:
    slugs = PAGES

WIDGETS = {
    "pricing(定价)": ["htmega-2026-pricing|htmega-2026-pricing", "htm25-pricing__card"],
    "testimonial(评价)": ["htmega-2026-testimonials|htmega-2026-testimonials", "htm25-testimonial"],
    "compare(对比表)": ["eael-advanced-data-table|eael-advanced-data-table", "eael-advanced-data-table"],
    "cta": ["eael-cta-box|eael-cta-box", "eael-cta-box"],
    "tabs": ["eael-adv-tabs|eael-adv-tabs", "eael-adv-tabs"],
    "workflow(timeline)": ["htmega-verticletimeline-addons|htmega-verticletimeline-addons", "htmega-verticletimeline"],
    "faq(手风琴)": ["eael-adv-accordion|eael-adv-accordion", "eael-adv-accordion"],
    "footer": ["<footer|<footer", "<footer"],
}

report = {}
for path in PAGES:
    url = dm.BASE + "/" + path
    try:
        html = op.open(url, timeout=60).read().decode("utf-8", "ignore")
    except Exception as e:
        report[path] = {"error": str(e)[:80]}
        continue
    row = {}
    for name, (pat, _) in WIDGETS.items():
        token = pat.split("|")[-1]
        row[name] = html.count(token)
    report[path] = row

keys = list(WIDGETS.keys())
print(f"{'页面':38s} " + " ".join(f"{k[:10]:>12s}" for k in keys))
for path, row in report.items():
    if "error" in row:
        print(f"{path:38s} ERROR {row['error']}")
        continue
    print(f"{path:38s} " + " ".join(f"{row.get(k, 0):>12d}" for k in keys))

json.dump(report, open("verify-render-report.json", "w"), ensure_ascii=False, indent=1)
print("\n已存 verify-render-report.json")
