#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""list-plugins.py — 线上插件清单与激活状态。"""
import importlib.util
import re

spec = importlib.util.spec_from_file_location("dm", "deploy-migrated.py")
dm = importlib.util.module_from_spec(spec)
spec.loader.exec_module(dm)

op = dm.build_opener()
dm.login(op)
html = op.open(dm.BASE + "/wp-admin/plugins.php", timeout=120).read().decode("utf-8", "ignore")

# 每个插件行：data-plugin=... / active 类 / 名称 / 版本
rows = re.findall(r'<tr[^>]*data-plugin="([^"]+)"[^>]*>(.*?)</tr>', html, re.S)
print(f"共 {len(rows)} 个插件：")
for slug, row in rows:
    active = "inactive" in row[:200] or 'class="active"' not in row
    act = "ACTIVE" if "deactivate" in row else "inactive"
    name = re.search(r"<strong>(.*?)</strong>", row, re.S)
    ver = re.search(r"Version[:\s<]*([0-9.]+)", row)
    name = re.sub(r"<[^>]+>", "", name.group(1)).strip()[:45] if name else "?"
    print(f"  {slug:55s} {act:9s} {ver.group(1) if ver else '?':10s} {name}")
