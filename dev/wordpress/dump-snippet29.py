#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""dump-snippet29.py — 看 lr_elem_bridge 的完整接口。"""
import importlib.util
import json
import urllib.request

spec = importlib.util.spec_from_file_location("dm", "deploy-migrated.py")
dm = importlib.util.module_from_spec(spec)
spec.loader.exec_module(dm)

op = dm.build_opener()
dm.login(op)
nonce = dm.rest_nonce(op)
req = urllib.request.Request(dm.BASE + "/wp-json/code-snippets/v1/snippets/29", headers={"X-WP-Nonce": nonce})
s = json.loads(op.open(req, timeout=120).read().decode())
open("snippet-29-current.php", "w").write(s["code"])
print("已导出", len(s["code"]), "字符")
