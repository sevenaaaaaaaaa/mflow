#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""dump-snippet27.py — 导出 snippet 27 当前代码到本地。"""
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
open("snippet-27-current.php", "w").write(snip["code"])
print("已导出 snippet-27-current.php，", len(snip["code"]), "字符")
print("scope/name:", snip.get("scope"), "|", snip.get("name"))
