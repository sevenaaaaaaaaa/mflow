#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""deploy-footer2.py — 修页脚：.lr dark 作用域包裹 + 隐藏主题空页脚。"""
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

# 1) 页脚输出包 .lr dark 作用域（tailwind 类生效）
old_echo = "\techo $footer_html;"
new_echo = "\techo '<div class=\"lr dark\" id=\"lr-site-footer\">';\n\techo $footer_html;\n\techo '</div>';"
assert old_echo in code, "未找到 echo $footer_html;"
code = code.replace(old_echo, new_echo)

# 2) 隐藏主题空页脚（site-footer 无 data-elementor-type 属性，补选择器）
old_hide = ".lr-replica-page [data-elementor-type=\"footer\"]{display:none !important}"
assert old_hide in code, "未找到隐藏规则"
code = code.replace(old_hide, old_hide[:-len("{display:none !important}")]
                    + ",.lr-replica-page #site-footer{display:none !important}")

snip["code"] = code
put = urllib.request.Request(dm.BASE + "/wp-json/code-snippets/v1/snippets/27",
                             data=json.dumps(snip).encode(), method="PUT",
                             headers={"X-WP-Nonce": nonce, "Content-Type": "application/json"})
res = dm._retry(lambda: json.loads(op.open(put, timeout=120).read().decode()))
print("PUT 完成 | lr 作用域包裹:", 'id=\\"lr-site-footer\\"' in res["code"] or "lr-site-footer" in res["code"],
      "| 隐藏 site-footer:", "#site-footer" in res["code"])

# 前台验证
html = op.open(dm.BASE + "/replica-comparison-hub", timeout=60).read().decode("utf-8", "ignore")
i = html.find('id="lr-site-footer"')
print("前台包裹 footer:", "✓" if i > 0 else "✗")
if i > 0:
    back = html[max(0, i - 60):i]
    print("   包裹类确认:", '<div class="lr dark"' in back)
