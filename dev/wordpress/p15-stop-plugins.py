#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P1.5 停 7 个零使用 Elementor 插件包（保留 EA + HT Mega）。
逐个停用，每停一个跑渲染探针（shopify 页关键微件计数），异常立即回滚激活。
"""
import importlib.util
import re
import urllib.parse

spec = importlib.util.spec_from_file_location("dm", "deploy-migrated.py")
dm = importlib.util.module_from_spec(spec)
spec.loader.exec_module(dm)

op = dm.build_opener()
dm.login(op)

TARGETS = [
    "advanced-animation/advanced-animation.php",
    "elementskit-lite/elementskit-lite.php",
    "powerpack-lite-for-elementor/powerpack-lite-elementor.php",
    "royal-elementor-addons/wpr-addons.php",
    "header-footer-elementor/header-footer-elementor.php",
    "unlimited-elements-for-elementor/unlimited_elements.php",
    "ht-menu-lite/ht-mega-menu.php",
]

PROBE_URL = dm.BASE + "/replica-solution-ai-design-solution-for-shopify"
MUST = ["eael-advanced-data-table", "eael-cta-box", "eael-adv-tabs", "eael-adv-accordion",
        "htmega-verticletimeline-addons", "htm25-pricing__card", "id=\"lr-site-footer\""]


def probe(tag):
    html = op.open(PROBE_URL, timeout=90).read().decode("utf-8", "ignore")
    missing = [m for m in MUST if m not in html]
    print(f"    探针[{tag}]: " + ("全部命中 ✓" if not missing else f"缺失 {missing}"))
    return not missing


def deactivate(plugin, nonce):
    url = (dm.BASE + "/wp-admin/plugins.php?action=deactivate&plugin="
           + urllib.parse.quote(plugin, safe="") + "&_wpnonce=" + nonce)
    res = op.open(url, timeout=300).read().decode("utf-8", "ignore")
    return "插件已停用" in res or "deactivated" in res.lower()


def activate(plugin, nonce):
    url = (dm.BASE + "/wp-admin/plugins.php?action=activate&plugin="
           + urllib.parse.quote(plugin, safe="") + "&_wpnonce=" + nonce)
    op.open(url, timeout=300).read()
    print(f"    ↩ 已回滚激活 {plugin.split('/')[0]}")


def get_nonce(plugin):
    html = op.open(dm.BASE + "/wp-admin/plugins.php", timeout=120).read().decode("utf-8", "ignore")
    m = re.search(r'action=deactivate&amp;plugin=' + re.escape(urllib.parse.quote(plugin, safe=""))
                  + r'&amp;_wpnonce=([a-f0-9]+)', html)
    if not m:
        m = re.search(r'deactivate[^"]*?' + re.escape(plugin.split("/")[0])
                      + r'[^"]*?_wpnonce=([a-f0-9]+)', html)
    return m.group(1) if m else None


assert probe("停用前基线"), "基线探针已异常，中止"

stopped = []
for plugin in TARGETS:
    name = plugin.split("/")[0]
    nonce = get_nonce(plugin)
    if not nonce:
        print(f"  ✗ {name}: 找不到停用 nonce，跳过")
        continue
    ok = deactivate(plugin, nonce)
    if not ok:
        print(f"  ⚠ {name}: 停用响应未确认，探针复核")
    if probe(name):
        stopped.append(plugin)
        print(f"  ✓ {name} 已停用")
    else:
        activate(plugin, get_nonce(plugin) or nonce)
        print(f"  ✗ {name} 探针异常，已回滚。中止后续。")
        break

# 终态复核：停用的确实 inactive
pl = op.open(dm.BASE + "/wp-admin/plugins.php", timeout=120).read().decode("utf-8", "ignore")
for plugin in TARGETS:
    state = "ACTIVE" if f'data-plugin="{plugin}"' in pl and "deactivate" in pl.split(f'data-plugin="{plugin}"')[1][:600] else "inactive"
    print(f"终态 {plugin.split('/')[0]:35s} {state}")
print(f"\n完成：停用 {len(stopped)}/{len(TARGETS)}")
