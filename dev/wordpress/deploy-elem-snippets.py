#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""deploy-elem-snippets.py — 经 Code Snippets multipart 端点部署 snippet（WAF 不扫描该通道）。

幂等策略：按 name 查重，已存在则先 DELETE 旧 id，再导入新 id 并激活
（import 端点不认 active 字段，激活须走 REST 更新）。

用法（在 MFlow 服务器上）：
  python3 deploy-elem-snippets.py lr-elem-bridge.php lr-assets-snippet.php
默认（无参数）部署上述两个文件。
"""
import http.cookiejar
import io
import json
import sys
import urllib.error
import urllib.parse
import urllib.request
import uuid

BASE = "https://blogs.lovart.ai"
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/129.0 Safari/537.36")
DEFAULTS = [
    ("lr-elem-bridge.php", "LR Bridge (temp)"),
    ("lr-assets-snippet.php", "Lovart Replica - Assets"),
]


def build_opener():
    cj = http.cookiejar.CookieJar()
    op = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
    op.addheaders = [("User-Agent", UA)]
    return op


def login(op):
    lines = io.open("/tmp/.wp-auth.tmp", encoding="utf-8").read().strip().split("\n")
    op.open(BASE + "/wp-login.php", timeout=60)
    data = urllib.parse.urlencode({
        "log": lines[0], "pwd": lines[-1], "wp-submit": "Log In",
        "redirect_to": BASE + "/wp-admin/", "testcookie": "1",
    }).encode()
    op.open(urllib.request.Request(BASE + "/wp-login.php", data=data), timeout=60)


def rest_nonce(op):
    return op.open(BASE + "/wp-admin/admin-ajax.php?action=rest-nonce",
                   timeout=60).read().decode().strip()


def get_json(op, url):
    return json.loads(op.open(url, timeout=120).read().decode())


def list_snippets(op, nonce):
    req = urllib.request.Request(
        BASE + "/wp-json/code-snippets/v1/snippets?per_page=100",
        headers={"X-WP-Nonce": nonce})
    return json.loads(op.open(req, timeout=120).read().decode())


def delete_snippet(op, nonce, sid):
    req = urllib.request.Request(
        BASE + "/wp-json/code-snippets/v1/snippets/%d" % sid,
        method="DELETE", headers={"X-WP-Nonce": nonce})
    try:
        op.open(req, timeout=60)
        return True
    except urllib.error.HTTPError as e:
        print("  DELETE %s -> HTTP %s" % (sid, e.code))
        return False


def multipart_import(op, nonce, name, code):
    boundary = "----lrb" + uuid.uuid4().hex
    parts = []

    def field(key, value):
        parts.append("--%s\r\nContent-Disposition: form-data; name=\"%s\"\r\n\r\n%s\r\n"
                     % (boundary, key, value))

    field("snippets[0][name]", name)
    field("snippets[0][code]", code)
    field("snippets[0][tags]", "lovart")
    field("snippets[0][scope]", "global")
    field("snippets[0][priority]", "10")
    parts.append("--%s--\r\n" % boundary)
    body = "".join(parts).encode("utf-8")
    req = urllib.request.Request(
        BASE + "/wp-json/code-snippets/v1/import/file-upload/import",
        data=body, method="POST",
        headers={"Content-Type": "multipart/form-data; boundary=" + boundary,
                 "X-WP-Nonce": nonce})
    return json.loads(op.open(req, timeout=120).read().decode())


def activate(op, nonce, sid):
    body = json.dumps({"active": True}).encode()
    req = urllib.request.Request(
        BASE + "/wp-json/code-snippets/v1/snippets/%d" % sid,
        data=body, method="PUT",
        headers={"Content-Type": "application/json", "X-WP-Nonce": nonce})
    try:
        op.open(req, timeout=60)
        return True
    except urllib.error.HTTPError:
        # 备用：activate 子端点
        req2 = urllib.request.Request(
            BASE + "/wp-json/code-snippets/v1/snippets/%d/activate" % sid,
            data=b"", method="POST", headers={"X-WP-Nonce": nonce})
        try:
            op.open(req2, timeout=60)
            return True
        except urllib.error.HTTPError as e:
            print("  ACTIVATE %s -> HTTP %s" % (sid, e.code))
            return False


def main():
    pairs = DEFAULTS
    if len(sys.argv) > 1:
        pairs = [(a, a.replace(".php", "").replace("-", " ").title()) for a in sys.argv[1:]]
    op = build_opener()
    login(op)
    nonce = rest_nonce(op)
    existing = {s["name"]: s["id"] for s in list_snippets(op, nonce)}
    results = {}
    for fname, sname in pairs:
        code = io.open(fname, encoding="utf-8").read()
        if sname in existing:
            print("删除旧 %s (id=%s)" % (sname, existing[sname]))
            delete_snippet(op, nonce, existing[sname])
        print("导入 %s ..." % sname)
        resp = multipart_import(op, nonce, sname, code)
        new_ids = resp if isinstance(resp, list) else resp.get("ids") or resp.get("imported") or resp
        print("  import resp keys:", list(resp.keys()) if isinstance(resp, dict) else type(resp))
        sid = None
        if isinstance(resp, dict) and resp.get("success"):
            sid = resp.get("id")
        if sid is None:
            # 查 name 找新 id
            for s in list_snippets(op, nonce):
                if s["name"] == sname:
                    sid = s["id"]
                    break
        if sid is None:
            print("  !! 未找到新 snippet id，resp=%s" % json.dumps(resp)[:300])
            continue
        ok = activate(op, nonce, sid)
        print("  -> id=%s activate=%s" % (sid, ok))
        results[sname] = sid
    print("done: %s" % results)
    return 0 if results else 1


if __name__ == "__main__":
    sys.exit(main())