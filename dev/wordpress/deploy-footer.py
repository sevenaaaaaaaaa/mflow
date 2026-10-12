#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""deploy-footer.py — snippet 27 追加复刻页页脚注入（wp_footer, 仅 _lr_replica 页）并 PUT。"""
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

if "LRFOOTER" in code:
    print("已注入过，跳过")
    raise SystemExit

raw = open("footer-raw.html").read().strip()
assert "\nLRFOOTER;" not in raw, "结束标记冲突"
assert raw.endswith("</footer>"), "意外结尾: " + raw[-40:]
print("footer-raw:", len(raw), "字符 |", raw.count("href="), "链接")

# PHP 7.1 兼容：nowdoc 结束标记必须顶格（PHP<7.3 无 flexible heredoc）
block = (
    "\n\n/**\n"
    " * 复刻页页脚：服务端直出 17 链接页脚（footer-raw.html，C1 拆页脚批次产物）。\n"
    " * 仅 _lr_replica 整页；主题构建器 footer 已被 CSS 隐藏，此处补真页脚（SEO 友好）。\n"
    " */\n"
    "add_action( 'wp_footer', function () {\n"
    "\tif ( ! is_singular() || ! get_post_meta( get_queried_object_id(), '_lr_replica', true ) ) {\n"
    "\t\treturn;\n"
    "\t}\n"
    "\t$footer_html = <<<'LRFOOTER'\n"
    + raw + "\n"
    + "LRFOOTER;\n"
    "\techo $footer_html;\n"
    "}, 50 );\n"
)
snip["code"] = code + block

put = urllib.request.Request(dm.BASE + "/wp-json/code-snippets/v1/snippets/27",
                             data=json.dumps(snip).encode(), method="PUT",
                             headers={"X-WP-Nonce": nonce, "Content-Type": "application/json"})
res = dm._retry(lambda: json.loads(op.open(put, timeout=120).read().decode()))
print("PUT 完成，LRFOOTER 注入:", "LRFOOTER" in res.get("code", ""))

# 验证：前台页面出现真页脚
html = op.open(dm.BASE + "/replica-comparison-hub", timeout=60).read().decode("utf-8", "ignore")
i = html.find("bg-bg-base-default relative mx-auto w-full max-w-[1400px]")
print("前台 footer 渲染:", "✓" if i > 0 else "✗")
if i > 0:
    seg = html[i:i + 14000]
    print("   链接数:", seg.count("href="))
    print("   含 Products:", "Products" in seg)
