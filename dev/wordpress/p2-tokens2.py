#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""p2-tokens2.py — token 灌 kit（修正：name 字段 + POST 后显式 PUT active=true）。"""
import importlib.util
import json
import re
import subprocess
import urllib.request

spec = importlib.util.spec_from_file_location("dm", "deploy-migrated.py")
dm = importlib.util.module_from_spec(spec)
spec.loader.exec_module(dm)

op = dm.build_opener()
dm.login(op)
nonce = dm.rest_nonce(op)

SYSTEM_COLORS = [
    {"_id": "primary",   "title": "LR Ink",   "color": "#100f09"},
    {"_id": "secondary", "title": "LR Paper", "color": "#f2f1ee"},
    {"_id": "text",      "title": "LR Text",  "color": "#100f09"},
    {"_id": "accent",    "title": "LR Accent","color": "#171612"},
]
CUSTOM_COLORS = [
    {"_id": "lr_bg_base",      "title": "LR BG Base",         "color": "#f9f8f6"},
    {"_id": "lr_bg_secondary", "title": "LR BG Secondary",    "color": "#f2f1ee"},
    {"_id": "lr_bg_tertiary",  "title": "LR BG Tertiary",     "color": "#eae9e6"},
    {"_id": "lr_bg_dark",      "title": "LR BG Dark",         "color": "#100f09"},
    {"_id": "lr_bg_dark_2",    "title": "LR BG Dark 2",       "color": "#171612"},
    {"_id": "lr_bg_dark_3",    "title": "LR BG Dark 3",       "color": "#1d1b16"},
    {"_id": "lr_text_default", "title": "LR Text Default",    "color": "#100f09"},
    {"_id": "lr_text_invert",  "title": "LR Text Invert",     "color": "#f5f4ef"},
    {"_id": "lr_border",       "title": "LR Border Contrast", "color": "#1a1a19"},
    {"_id": "lr_border_l1",    "title": "LR Border L1",       "color": "#1a1a190f"},
    {"_id": "lr_border_l2",    "title": "LR Border L2",       "color": "#1a1a191f"},
    {"_id": "lr_border_l3",    "title": "LR Border L3",       "color": "#1a1a192e"},
    {"_id": "lr_accent_light", "title": "LR Accent Light",    "color": "#f5f5f5"},
]
SYSTEM_FONTS = [
    {"_id": "primary",   "title": "LR Body",    "font": "Montserrat", "weight": "400"},
    {"_id": "secondary", "title": "LR Display", "font": "Poppins",    "weight": "500"},
    {"_id": "text",      "title": "LR Text",    "font": "Montserrat", "weight": "400"},
    {"_id": "accent",    "title": "LR Accent",  "font": "Poppins",    "weight": "500"},
]


def run_ssh(cmd, input_text=""):
    r = subprocess.run(["bash", "-c", cmd], input=input_text.encode(), capture_output=True, timeout=120)
    return (r.stdout + r.stderr).decode(errors="ignore")


def snippet_create(code, name):
    body = json.dumps({"name": name, "code": code, "scope": "global", "active": True}).encode()
    req = urllib.request.Request(dm.BASE + "/wp-json/code-snippets/v1/snippets", data=body, method="POST",
                                 headers={"X-WP-Nonce": nonce, "Content-Type": "application/json"})
    return json.loads(op.open(req, timeout=120).read().decode())


def snippet_update(sid, patch):
    body = json.dumps(patch).encode()
    req = urllib.request.Request(dm.BASE + f"/wp-json/code-snippets/v1/snippets/{sid}", data=body,
                                 method="PUT", headers={"X-WP-Nonce": nonce, "Content-Type": "application/json"})
    return json.loads(op.open(req, timeout=120).read().decode())


def snippet_delete(sid):
    req = urllib.request.Request(dm.BASE + f"/wp-json/code-snippets/v1/snippets/{sid}", method="DELETE",
                                 headers={"X-WP-Nonce": nonce})
    return op.open(req, timeout=120).read().decode()


PROBE = dm.BASE + "/replica-comparison-hub"

# ① 清掉残留 31-34（404 = 已不存在，忽略）
for sid in (31, 32, 33, 34):
    try:
        print(f"清理残留 {sid}:", snippet_delete(sid)[:60])
    except Exception:
        print(f"清理残留 {sid}: 已不存在")

# ② token JSON 上传到 WP 机器
for name, data in [("lr-system-colors.json", SYSTEM_COLORS), ("lr-custom-colors.json", CUSTOM_COLORS),
                   ("lr-system-fonts.json", SYSTEM_FONTS)]:
    out = run_ssh(f"ssh -p 28766 root@172.96.253.73 'cat > /tmp/{name} && chmod 644 /tmp/{name}'",
                  json.dumps(data))
    print(f"上传 {name}:", out[:60] or "ok")

# ③ 写入 snippet（无 <?php 开头，纯 PHP 顶层）
php_write = """
$kit_id = get_option( 'elementor_active_kit' );
$meta = get_post_meta( $kit_id, '_elementor_page_settings', true );
if ( ! is_array( $meta ) ) { $meta = []; }
$meta['system_colors'] = json_decode( file_get_contents( '/tmp/lr-system-colors.json' ), true );
$meta['custom_colors'] = json_decode( file_get_contents( '/tmp/lr-custom-colors.json' ), true );
$meta['system_fonts']  = json_decode( file_get_contents( '/tmp/lr-system-fonts.json' ), true );
update_post_meta( $kit_id, '_elementor_page_settings', $meta );
if ( class_exists( 'Elementor\Plugin' ) ) {
    \Elementor\Plugin::$instance->files_manager->clear_cache();
}
echo '<div id="lr-token-write" style="display:none">kit=' . $kit_id . '</div>';
"""
snip = snippet_create(php_write, "LR temp - token write")
sid = snip.get("id")
print("写入 snippet id:", sid, "| active:", snip.get("active"), "| code_error:", snip.get("code_error"))
if not snip.get("active"):
    snip2 = snippet_update(sid, {"active": True})
    print("PUT active 后:", snip2.get("active"), "| code_error:", snip2.get("code_error"))

# ④ 触发执行
html = op.open(PROBE, timeout=180).read().decode("utf-8", "ignore")
m = re.search(r'id="lr-token-write"[^>]*>([^<]*)<', html)
print("执行输出:", m.group(1) if m else "未捕获")

# ⑤ 删写入 snippet
snippet_delete(sid)
print("已删写入 snippet")

# ⑥ 验证 snippet
php_verify = """
$kit_id = get_option( 'elementor_active_kit' );
$meta = get_post_meta( $kit_id, '_elementor_page_settings', true );
$out = [ 'kit' => $kit_id ];
foreach ( (array) ( $meta['system_colors'] ?? [] ) as $c ) { $out['sc'][] = $c['_id'] . '=' . $c['color']; }
$out['cc'] = count( (array) ( $meta['custom_colors'] ?? [] ) );
foreach ( (array) ( $meta['system_fonts'] ?? [] ) as $f ) { $out['fonts'][] = $f['_id'] . '=' . $f['font']; }
echo '<div id="lr-token-verify" style="display:none">' . json_encode( $out ) . '</div>';
"""
snip = snippet_create(php_verify, "LR temp - token verify")
sid = snip.get("id")
if not snip.get("active"):
    snippet_update(sid, {"active": True})
html = op.open(PROBE, timeout=180).read().decode("utf-8", "ignore")
snippet_delete(sid)
print("已删验证 snippet")
m = re.search(r'id="lr-token-verify"[^>]*>(.*?)</div>', html)
if m:
    data = json.loads(m.group(1))
    print("kit:", data.get("kit"))
    print("system_colors:", data.get("sc"))
    print("custom_colors:", data.get("cc"))
    print("fonts:", data.get("fonts"))
else:
    print("✗ 仍未捕获验证输出")
