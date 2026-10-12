#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""p2-debug.py — 对比 snippet 27 字段，找临时 snippet 不执行的原因。"""
import importlib.util
import json
import urllib.request

spec = importlib.util.spec_from_file_location("dm", "deploy-migrated.py")
dm = importlib.util.module_from_spec(spec)
spec.loader.exec_module(dm)

op = dm.build_opener()
dm.login(op)
nonce = dm.rest_nonce(op)

req = urllib.request.Request(dm.BASE + "/wp-json/code-snippets/v1/snippets/27", headers={"X-WP-Nonce": nonce})
s27 = json.loads(op.open(req, timeout=120).read().decode())
skip = {"code"}
print("snippet 27 字段:")
for k, v in s27.items():
    if k in skip:
        print(f"  {k}: <{len(str(v))} 字符>")
    else:
        print(f"  {k}: {v}")

# 列出全部 snippet 的 id/name/active/scope，看有没有 LR temp 残留
req = urllib.request.Request(dm.BASE + "/wp-json/code-snippets/v1/snippets?per_page=100",
                             headers={"X-WP-Nonce": nonce})
lst = json.loads(op.open(req, timeout=120).read().decode())
print("\n全部 snippets:")
items = lst if isinstance(lst, list) else lst.get("snippets", lst.get("data", []))
for s in items:
    print(f"  id={s.get('id')} active={s.get('active')} scope={s.get('scope')} {s.get('name')}")
