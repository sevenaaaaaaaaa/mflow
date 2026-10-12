#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""fix-pricing-slots.py — 修复 pricing repeater 槽错位（端点按模板字段序归位，
我方原序 [plan_name, currency, monthly, annual, period, tagline, features,
is_featured, featured_badge, cta_text, cta_url, cta_variant] 头部多跳 2 槽）。

重映射（存储坏值 → 正确语义槽）：
  plan_name      = plan_name
  currency       = 旧 is_featured      ('$')
  price_monthly  = 旧 featured_badge   (月价)
  price_annual   = 旧 currency         (年价)
  period         = 旧 price_monthly    ('/month')
  tagline        = 旧 price_annual     (省钱钩子/<s>)
  features       = 旧 period           (年付 bill + 权益清单)
  is_featured    = 旧 tagline          ('' / 'yes')
  featured_badge = 旧 features         ('' / 'Most popular')
  cta_*          = 不动
"""
import glob
import json

FIXED = []
for path in sorted(glob.glob("elem-migrated/*.json")):
    if "composite-replica-all" in path:
        continue
    data = json.load(open(path))
    s = json.dumps(data, ensure_ascii=False)
    if '"htmega-2026-pricing"' not in s:
        continue

    def walk(els):
        n = 0
        for el in els:
            if el.get("widgetType") == "htmega-2026-pricing":
                for row in el["settings"]["plan_items"]:
                    if row.get("is_featured") in ("$",) or row.get("currency", "").isdigit():
                        old = {k: row.get(k, "") for k in
                               ("plan_name", "is_featured", "featured_badge", "currency",
                                "price_monthly", "price_annual", "period", "tagline", "features")}
                        row["plan_name"] = old["plan_name"]
                        row["currency"] = old["is_featured"]
                        row["price_monthly"] = old["featured_badge"]
                        row["price_annual"] = old["currency"]
                        row["period"] = old["price_monthly"]
                        row["tagline"] = old["price_annual"]
                        row["features"] = old["period"]
                        row["is_featured"] = old["tagline"] or "no"
                        row["featured_badge"] = old["features"]
                        n += 1
            n += walk(el.get("elements", []))
        return n

    cnt = walk(data["data"] if isinstance(data, dict) else data)
    if cnt:
        json.dump(data, open(path, "w"), ensure_ascii=False)
        FIXED.append((path.split("/")[-1][:-5], cnt))

for slug, cnt in FIXED:
    print(f"  ✓ {slug}: {cnt} 行修复")
print(f"共 {len(FIXED)} 页 / {sum(c for _, c in FIXED)} 行")

# 抽验 shopify 第 1 行 + Pro 行
data = json.load(open("elem-migrated/replica-solution-ai-design-solution-for-shopify.json"))
def find(els):
    for el in els:
        if el.get("widgetType") == "htmega-2026-pricing":
            return el
        r = find(el.get("elements", []))
        if r: return r
w = find(data["data"])
for row in w["settings"]["plan_items"][:1] + w["settings"]["plan_items"][2:3]:
    print("---", row["plan_name"])
    for k in ("currency", "price_monthly", "price_annual", "period", "tagline", "is_featured", "featured_badge"):
        print(f"  {k}: {str(row[k])[:60]!r}")
