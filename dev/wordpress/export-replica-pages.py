#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""export-replica-pages.py — 把线上复刻页 content.rendered 导出为 lr-assets/pages/{slug}.html。

在 MFlow 服务器上运行。流程：
  1. REST 拉全站页面清单
  2. 复刻页（引用 lr-assets 的）逐页拉 content.rendered，剥 wp:html 注释
  3. 写 /www/wwwroot/nownexts_com/lr-assets/pages/{slug}.html
  4. 逐页设置 template=lovart-replica-template（注册于 Code Snippets Registry）

用法：
  python3 export-replica-pages.py [--apply-template]   # 默认只导出，加参数才改模板
"""
import argparse
import http.cookiejar
import io
import json
import re
import sys
import urllib.parse
import urllib.request
import urllib.error

BASE = "https://blogs.lovart.ai"
ASSET_DIR = "/www/wwwroot/nownexts_com/lr-assets/pages"
ASSET_MARK = "lr-assets/lovart-replica"
TPL = "lovart-replica-template"


def build_opener():
    cj = http.cookiejar.CookieJar()
    return urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))


def login(op):
    lines = io.open("/tmp/.wp-auth.tmp", encoding="utf-8").read().strip().split("\n")
    USER, PASS = lines[0], lines[-1]
    op.open(BASE + "/wp-login.php")
    data = urllib.parse.urlencode({
        "log": USER, "pwd": PASS, "wp-submit": "Log In",
        "redirect_to": BASE + "/wp-admin/", "testcookie": "1",
    }).encode()
    op.open(urllib.request.Request(BASE + "/wp-login.php", data=data))


def get_json(op, url):
    return json.loads(op.open(url, timeout=120).read().decode("utf-8"))


def post_json(op, url, payload, nonce):
    body = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=body, method="POST",
        headers={"Content-Type": "application/json", "X-WP-Nonce": nonce})
    try:
        return op.open(req, timeout=180).status
    except urllib.error.HTTPError as e:
        return e.code


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply-template", action="store_true")
    args = ap.parse_args()

    op = build_opener()
    login(op)
    nonce = op.open(BASE + "/wp-admin/admin-ajax.php?action=rest-nonce", timeout=30).read().decode().strip()

    # 全站清单（轻量）
    pages, pageno = [], 1
    while True:
        batch = get_json(op, "%s/wp-json/wp/v2/pages?per_page=100&page=%d&_fields=id,slug,link,template" % (BASE, pageno))
        pages.extend(batch)
        if len(batch) < 100:
            break
        pageno += 1

    # 复刻页 = search lr-assets
    shared = get_json(op, "%s/wp-json/wp/v2/pages?per_page=100&search=%s&_fields=id,slug" % (
        BASE, urllib.parse.quote(ASSET_MARK)))
    shared_ids = {p["id"] for p in shared}
    replicas = [p for p in pages if p["id"] in shared_ids]

    import os
    os.makedirs(ASSET_DIR, exist_ok=True)
    ok, fail = 0, 0
    for p in replicas:
        full = get_json(op, "%s/wp-json/wp/v2/pages/%d?_fields=slug,template,content" % (BASE, p["id"]))
        html = full["content"]["rendered"]
        html = re.sub(r"<!--\s*/?wp:html\s*-->", "", html).strip()
        out = os.path.join(ASSET_DIR, "%s.html" % p["slug"])
        io.open(out, "w", encoding="utf-8").write(html + "\n")
        os.chmod(out, 0o644)
        code = 200
        if args.apply_template:
            code = post_json(op, "%s/wp-json/wp/v2/pages/%d" % (BASE, p["id"]),
                {"template": TPL}, nonce)
        status = "OK" if code == 200 else "FAIL(%s)" % code
        print("id=%s %s.html (%d bytes) %s" % (p["id"], p["slug"], len(html), status))
        if code == 200:
            ok += 1
        else:
            fail += 1
    print("done: ok=%d fail=%d" % (ok, fail))
    return 1 if fail else 0


if __name__ == "__main__":
    sys.exit(main())