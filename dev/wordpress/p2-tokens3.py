#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""p2-tokens3.py — snippet 29 追加 lr_kit_tokens action；token JSON 上资产服务器；调用执行。"""
import importlib.util
import json
import subprocess
import urllib.parse
import urllib.request

spec = importlib.util.spec_from_file_location("dm", "deploy-migrated.py")
dm = importlib.util.module_from_spec(spec)
spec.loader.exec_module(dm)

SYSTEM_COLORS = [
    {"_id": "primary",   "title": "LR Ink",    "color": "#100f09"},
    {"_id": "secondary", "title": "LR Paper",  "color": "#f2f1ee"},
    {"_id": "text",      "title": "LR Text",   "color": "#100f09"},
    {"_id": "accent",    "title": "LR Accent", "color": "#171612"},
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

KIT_TOKENS = {
    "system_colors": SYSTEM_COLORS,
    "custom_colors": CUSTOM_COLORS,
    "system_fonts": SYSTEM_FONTS,
}

ADDON = """
add_action( 'wp_ajax_lr_kit_tokens', function () {
	if ( ! current_user_can( 'edit_pages' ) ) {
		wp_send_json_error( 'perm' );
	}
	if ( ! isset( $_POST['secret'] ) || LR_BRIDGE_SECRET !== $_POST['secret'] ) {
		wp_send_json_error( 'secret' );
	}
	$kit_id = get_option( 'elementor_active_kit' );
	if ( ! $kit_id ) {
		wp_send_json_error( 'no-kit' );
	}
	$r = wp_remote_get( 'https://nownexts.com/lr-assets/elem/kit-tokens.json', array( 'timeout' => 90 ) );
	if ( is_wp_error( $r ) || 200 !== (int) wp_remote_retrieve_response_code( $r ) ) {
		wp_send_json_error( 'fetch' );
	}
	$payload = json_decode( wp_remote_retrieve_body( $r ), true );
	if ( empty( $payload['system_colors'] ) || ! is_array( $payload['system_colors'] ) ) {
		wp_send_json_error( 'payload' );
	}
	$meta = get_post_meta( $kit_id, '_elementor_page_settings', true );
	if ( ! is_array( $meta ) ) {
		$meta = array();
	}
	$meta['system_colors'] = $payload['system_colors'];
	if ( ! empty( $payload['custom_colors'] ) ) {
		$meta['custom_colors'] = $payload['custom_colors'];
	}
	if ( ! empty( $payload['system_fonts'] ) ) {
		$meta['system_fonts'] = $payload['system_fonts'];
	}
	update_post_meta( $kit_id, '_elementor_page_settings', $meta );
	if ( class_exists( '\\Elementor\\Plugin' ) ) {
		\\Elementor\\Plugin::$instance->files_manager->clear_cache();
	}
	wp_send_json_success( array(
		'kit'   => $kit_id,
		'sc'    => count( $meta['system_colors'] ),
		'cc'    => isset( $meta['custom_colors'] ) ? count( $meta['custom_colors'] ) : 0,
		'fonts' => isset( $meta['system_fonts'] ) ? count( $meta['system_fonts'] ) : 0,
	) );
} );
"""

# 1) snippet 29 追加
op = dm.build_opener()
dm.login(op)
nonce = dm.rest_nonce(op)
req = urllib.request.Request(dm.BASE + "/wp-json/code-snippets/v1/snippets/29", headers={"X-WP-Nonce": nonce})
s29 = json.loads(op.open(req, timeout=120).read().decode())
if "lr_kit_tokens" in s29["code"]:
    print("snippet 29 已含 lr_kit_tokens")
else:
    s29["code"] = s29["code"].rstrip() + "\n" + ADDON
    put = urllib.request.Request(dm.BASE + "/wp-json/code-snippets/v1/snippets/29",
                                 data=json.dumps(s29).encode(), method="PUT",
                                 headers={"X-WP-Nonce": nonce, "Content-Type": "application/json"})
    res = json.loads(op.open(put, timeout=120).read().decode())
    print("snippet 29 更新:", "lr_kit_tokens" in res["code"], "| code_error:", res.get("code_error"))

# 2) token JSON 上资产服务器
subprocess.run(["ssh", "-p", "28766", "root@172.96.253.73",
                "cat > /www/wwwroot/nownexts_com/lr-assets/elem/kit-tokens.json"],
               input=json.dumps(KIT_TOKENS).encode(), capture_output=True, timeout=120)
r = subprocess.run(["ssh", "-p", "28766", "root@172.96.253.73",
                    "curl -s -o /dev/null -w '%{http_code}' https://nownexts.com/lr-assets/elem/kit-tokens.json"],
                   capture_output=True, text=True, timeout=120)
print("kit-tokens.json 上传与可达:", r.stdout.strip())

# 3) 调用 lr_kit_tokens
creds = open("/tmp/.wp-auth.tmp").read().splitlines()
log, pwd = creds[0], creds[-1]
data = urllib.parse.urlencode({"action": "lr_kit_tokens", "secret": "lrb-2026-x7k9"}).encode()
try:
    res = op.open(dm.BASE + "/wp-admin/admin-ajax.php", data=data, timeout=300).read().decode()
    print("lr_kit_tokens 响应:", res[:300])
except Exception as e:
    print("调用失败:", e)

# 4) 前台无回归探针
html = op.open(dm.BASE + "/replica-comparison-hub", timeout=90).read().decode("utf-8", "ignore")
ok = all(x in html for x in ["eael-advanced-data-table", "eael-cta-box", "id=\"lr-site-footer\""])
print("前台探针:", "✓" if ok else "✗")
