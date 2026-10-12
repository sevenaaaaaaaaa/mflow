#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""probe-lpagery.py — 摸清 LPagery 程序化建页入口与种子模板在线状态。"""
import json
import sys

sys.path.insert(0, ".")
import importlib.util
spec = importlib.util.spec_from_file_location("dm", "deploy-migrated.py")
dm = importlib.util.module_from_spec(spec)
spec.loader.exec_module(dm)

op = dm.build_opener()
dm.login(op)
nonce = dm.rest_nonce(op)
H = {"X-WP-Nonce": nonce, "X-Requested-With": "XMLHttpRequest"}


def get(path, admin=False):
    url = dm.BASE + path
    try:
        r = op.open(urllib_req(url, H), timeout=60)
        return r.getcode(), r.read().decode("utf-8", "replace")
    except Exception as e:
        return getattr(e, "code", 0), str(e)


def urllib_req(url, headers):
    import urllib.request
    return urllib.request.Request(url, headers=headers)


# 1. 种子模板在线状态（page? template? wp_block?）
for q in [
    "/wp-json/wp/v2/pages?slug=lp-lr-native-v1",
    "/wp-json/wp/v2/search?search=lp-lr-native&per_page=20",
    "/wp-json/wp/v2/types",
]:
    code, body = get(q)
    print("== GET", q, "->", code)
    if code == 200:
        try:
            data = json.loads(body)
            if isinstance(data, list):
                for item in data[:10]:
                    if isinstance(item, dict):
                        print("   -", item.get("id"), item.get("slug", ""),
                              item.get("title", {}).get("rendered", "") if "title" in item else item.get("title", ""))
            else:
                print("   keys:", sorted(data.keys())[:40])
        except Exception:
            print("   body head:", body[:300])

# 2. LPagery REST 命名空间探测
for q in [
    "/wp-json/lpagery/v1",
    "/wp-json/",
]:
    code, body = get(q)
    print("== GET", q, "->", code)
    if q == "/wp-json/" and code == 200:
        try:
            data = json.loads(body)
            routes = [r for r in data.get("routes", {}) if "lpagery" in r.lower()]
            print("   lpagery routes:", routes)
        except Exception:
            pass

# 3. LPagery admin 菜单页
for q in [
    "/wp-admin/admin.php?page=lpagery",
    "/wp-admin/admin.php?page=lpagery-create",
    "/wp-admin/edit.php?post_type=lpagery",
]:
    code, body = get(q)
    print("== GET", q, "->", code, "len", len(body))
    if code == 200:
        import re
        m = re.findall(r'page=lpagery[^\s"\'&]*', body)
        print("   lpagery page links:", sorted(set(m))[:20])
        m2 = re.findall(r'lpagery/v1/[a-z\-/]+', body)
        print("   rest mentions:", sorted(set(m2))[:20])
