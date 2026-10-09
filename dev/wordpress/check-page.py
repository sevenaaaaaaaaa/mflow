#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""check-page.py — 单页复刻架构快速检查（公开请求）"""
import re
import sys
import urllib.request

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0 Safari/537.36"

for url in sys.argv[1:]:
    h = urllib.request.urlopen(
        urllib.request.Request(url, headers={"User-Agent": UA}), timeout=60
    ).read().decode("utf-8", "replace")
    print("==", url)
    print("  size:", len(h), " doctype:", len(re.findall(r"<!doctype", h, re.I)))
    print("  elementor wp-page:", 'data-elementor-type="wp-page"' in h)
    print("  html widgets:", len(re.findall(r'class="[^"]*elementor-widget elementor-widget-html"', h)))
    print("  containers:", len(re.findall(r'class="[^"]*\be-con\b', h)))
    print("  lr wrap:", bool(re.search(r'class="lr(?: dark)?"', h)))
    print("  css v2:", "lovart-replica.css?v=2" in h,
          " js cfasync:", bool(re.search(r'<script[^>]*lr-replica[^>]*data-cfasync="false"', h)))
    print("  bodyclass:", "lr-replica-page" in h)
    print("  rocket-loader:", "rocket-loader" in h)
    t = re.search(r"<title>(.*?)</title>", h, re.S)
    print("  title:", t.group(1).strip()[:70] if t else "N/A")