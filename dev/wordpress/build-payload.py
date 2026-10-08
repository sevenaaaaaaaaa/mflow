#!/usr/bin/env python3
"""build-payload.py — 把旧的 2.7MB 内联复刻 payload 转成共享资产格式。

旧格式（毛病根源）：
  content = <!-- wp:html --><style>[2.5MB 序列化 CSS]</style>[SSR HTML]<script>[4KB JS]</script><!-- /wp:html -->
  → 每页各带一份 CSS 副本（修一处漂一处）；深色覆盖块无条件挂 :root（配色互踩）；
    solutions 页 JS 缺失（点击 bug）；博客插件样式混入（升级即漂移）。

新格式：
  <link rel=stylesheet href=共享 CSS?v=N>   ← 一处修改全站生效
  <div class="lr dark">[SSR HTML]</div>      ← CSS 全部作用域化到 .lr，明暗由包裹类控制
  <script>CSS 兜底注入</script>
  <script src=共享 JS?v=N defer></script>    ← 所有页都有交互（修点击 bug）

用法：
  python3 build-payload.py old-payload.json -o new-payload.json [--light] [--v 1]
  python3 build-payload.py -d replica-solutions-dir -o out-dir/
"""
import argparse
import http.cookiejar
import io
import json
import os
import re
import sys
import urllib.parse
import urllib.request

ASSET_BASE = "https://nownexts.com/lr-assets"
WP_BASE = "https://blogs.lovart.ai"


def fetch_live(page_id):
    """REST 拉已发布页的 content.rendered（旧 2.7MB 内联格式）。"""
    url = "%s/wp-json/wp/v2/pages/%d?_fields=slug,title,template,status,content" % (WP_BASE, page_id)
    d = json.loads(urllib.request.urlopen(url, timeout=180).read().decode("utf-8"))
    return {
        "slug": d["slug"],
        "title": d["title"]["rendered"],
        "status": d.get("status", "publish"),
        "template": d.get("template") or "elementor_canvas",
        "content": d["content"]["rendered"],
    }


def extract_html(content):
    """剥掉旧 payload 里的内联 <style> 与 <script> 及 wp:html 注释包裹，保留 SSR HTML。"""
    body = re.sub(r"<style[^>]*>.*?</style>", "", content, flags=re.S | re.I)
    body = re.sub(r"<script[^>]*>.*?</script>", "", body, flags=re.S | re.I)
    body = re.sub(r"<!--\s*/?wp:html\s*-->", "", body, flags=re.I)
    # WAF 规避：javascript: URL 触发 Aliyun WAF XSS 评分（405）。
    # 共享 JS 的 initNoJump 对 href="#" 同样 preventDefault，行为不变。
    body = body.replace('href="javascript:void(0)"', 'href="#"')
    body = body.replace("href='javascript:void(0)'", "href='#'")
    body = body.replace('href="javascript:;"', 'href="#"')
    body = re.sub(r'href="javascript:[^"]*"', 'href="#"', body)
    return body.strip()


FALLBACK_JS = """<script>
(function(){var u="%ASSET_BASE%/lovart-replica.css?v=%V%";
if(!document.querySelector('link[href^="%ASSET_BASE%/lovart-replica.css"]')){
var l=document.createElement("link");l.rel="stylesheet";l.href=u;document.head.appendChild(l);}})();
</script>"""


def build(old, mode="dark", version=1):
    html = extract_html(old["content"])
    v = f"?v={version}"
    css_url = f"{ASSET_BASE}/lovart-replica.css{v}"
    js_url = f"{ASSET_BASE}/lovart-replica.js{v}"
    wrapper_cls = "lr dark" if mode == "dark" else "lr"
    parts = [
        "<!-- wp:html -->",
        f'<link rel="stylesheet" href="{css_url}">',
        f'<div class="{wrapper_cls}">',
        html,
        "</div>",
        FALLBACK_JS.replace("%ASSET_BASE%", ASSET_BASE).replace("%V%", str(version)),
        f'<script src="{js_url}" defer></script>',
        "<!-- /wp:html -->",
    ]
    new = {
        "title": old.get("title", ""),
        "slug": old.get("slug", ""),
        "status": old.get("status", "publish"),
        "template": old.get("template", "elementor_canvas"),
        "content": "\n".join(parts),
    }
    return new


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("infile", nargs="?")
    ap.add_argument("-d", "--dir", help="批量处理目录下所有 *.json")
    ap.add_argument("-o", "--out", required=True)
    ap.add_argument("--light", action="store_true", help="明色页（包裹类不含 dark）")
    ap.add_argument("--v", type=int, default=1, help="资产版本号（cache buster）")
    ap.add_argument("--from-live", metavar="ID[,ID...]", help="按 WP 页 ID 现场拉旧页转换")
    args = ap.parse_args()

    mode = "light" if args.light else "dark"

    if args.from_live:
        os.makedirs(args.out, exist_ok=True)
        for pid in [int(x) for x in args.from_live.split(",")]:
            old = fetch_live(pid)
            new = build(old, mode, args.v)
            outp = os.path.join(args.out, "%s.json" % old["slug"])
            with io.open(outp, "w", encoding="utf-8") as f:
                json.dump(new, f, ensure_ascii=False)
            print("id=%d %s: %d → %d bytes" % (pid, old["slug"], len(old["content"]), len(new["content"])))
        return
    if args.dir:
        os.makedirs(args.out, exist_ok=True)
        for f in sorted(os.listdir(args.dir)):
            if not f.endswith(".json"):
                continue
            old = json.load(open(os.path.join(args.dir, f), encoding="utf-8"))
            new = build(old, mode, args.v)
            outp = os.path.join(args.out, f)
            json.dump(new, open(outp, "w", encoding="utf-8"), ensure_ascii=False)
            print(f"{f}: {len(old['content'])} → {len(new['content'])} bytes")
    else:
        if not args.infile:
            ap.error("需要 infile 或 -d")
        old = json.load(open(args.infile, encoding="utf-8"))
        new = build(old, mode, args.v)
        json.dump(new, open(args.out, "w", encoding="utf-8"), ensure_ascii=False)
        print(f"{args.infile}: {len(old['content'])} → {len(new['content'])} bytes")


if __name__ == "__main__":
    main()