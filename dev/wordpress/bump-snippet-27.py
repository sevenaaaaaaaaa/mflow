#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""bump-snippet-27.py — snippet 27 缓存参数 ?v=N → ?v=N+1（PUT code-snippets API）。"""
import importlib.util
import json
import urllib.request

spec = importlib.util.spec_from_file_location("dm", "deploy-migrated.py")
dm = importlib.util.module_from_spec(spec)
spec.loader.exec_module(dm)

op = dm.build_opener()
dm.login(op)
nonce = dm.rest_nonce(op)

req = urllib.request.Request(dm.BASE + "/wp-json/code-snippets/v1/snippets/27",
                             headers={"X-WP-Nonce": nonce})
snip = dm._retry(lambda: json.loads(op.open(req, timeout=120).read().decode()))
code = snip["code"]

import re
vers = re.findall(r"\?v=(\d+)", code)
assert vers, "没找到 ?v= 参数"
old = max(int(v) for v in vers)
new = old + 1
n = len(re.findall(r"\?v=%d\b" % old, code))
code2 = code.replace("?v=%d" % old, "?v=%d" % new)
# 只 bump replica.js 相关的（native/mirror 保持不动）——先看上下文
print("当前版本参数分布：")
for m in re.finditer(r"lovart-[a-z-]+\.js\?v=(\d+)", code):
    print("  ", m.group(0))

snip["code"] = code2
put = urllib.request.Request(dm.BASE + "/wp-json/code-snippets/v1/snippets/27",
                             data=json.dumps(snip).encode(), method="PUT",
                             headers={"X-WP-Nonce": nonce, "Content-Type": "application/json"})
res = dm._retry(lambda: json.loads(op.open(put, timeout=120).read().decode()))
check = re.findall(r"lovart-replica\.js\?v=(\d+)", res.get("code", ""))
print(f"PUT 完成：replica.js ?v={check}（原 {old} → 新 {new}，共 {n} 处 bump）")
