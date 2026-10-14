"""wp_blocks — MFlow 适配器：IR → WordPress（Gutenberg {prefix}/{type} 区块）。

Block namespace / asset prefix: MFLOW_BLOCK_PREFIX env, else the active site profile
(ops/site.json "block_prefix"), else "mflow".
"""
import json
import os
import re
import sys
IR_VERSION = "1.0"  # 与 replication_core.IR_VERSION 同步


def block_prefix():
    if os.environ.get("MFLOW_BLOCK_PREFIX"):
        return sanitize_type(os.environ["MFLOW_BLOCK_PREFIX"]) or "mflow"
    lib = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "library")
    try:
        sys.path.insert(0, os.path.abspath(lib))
        import site_profile
        return sanitize_type(site_profile.block_prefix()) or "mflow"
    except Exception:
        return "mflow"


def sanitize_type(t):
    return re.sub(r"[^a-z0-9-]", "", t.lower())


def ir_to_theme_blocks(ir, theme_dir):
    """IR → 主题区块产物。

    每个 section 生成 blocks/{type}/：block.json + render.php（section.html 直出）。
    同时写 assets/{prefix}-site.css（IR design.css）与 assets/{prefix}-tokens.json。
    返回 {blocks: [type], cssBytes, themeDir}。
    """
    px = block_prefix()
    blocks_dir = os.path.join(theme_dir, "blocks")
    assets_dir = os.path.join(theme_dir, "assets")
    os.makedirs(assets_dir, exist_ok=True)
    types = []
    for s in ir["sections"]:
        typ = sanitize_type(s["type"])
        d = os.path.join(blocks_dir, typ)
        os.makedirs(d, exist_ok=True)
        # 真实 SSR HTML 直出（render.php 从文件读，主题激活后即时生效）
        open(os.path.join(d, "section.html"), "w",
             encoding="utf-8").write(s["html"])
        meta = {
            "$schema": "https://schemas.wp.org/trunk/block.json",
            "apiVersion": 3, "name": f"{px}/{typ}", "version": IR_VERSION,
            "title": f"{px} {typ}", "category": px, "icon": "layout",
            "description": f"1:1 replica of source {typ} section.",
            "supports": {"align": ["full", "wide"], "html": False},
        }
        json.dump(meta, open(os.path.join(d, "block.json"), "w"),
                  ensure_ascii=False, indent=1)
        open(os.path.join(d, "render.php"), "w", encoding="utf-8").write(
            "<?php\n/** %s — 1:1 SSR replica (replication-core %s). */\n"
            "$h = file_get_contents(get_theme_file_path('blocks/%s/section.html'));\n"
            "echo $h;\n" % (px + "/" + typ, IR_VERSION, typ))
        types.append(typ)
    open(os.path.join(assets_dir, f"{px}-site.css"), "w",
         encoding="utf-8").write(ir["design"]["css"])
    json.dump(ir["design"].get("tokens", {}),
              open(os.path.join(assets_dir, f"{px}-tokens.json"), "w"),
              ensure_ascii=False, indent=1)
    return {"blocks": types, "cssBytes": len(ir["design"]["css"]), "themeDir": theme_dir}


def ir_to_page_content(ir):
    """IR → 页面内容（Gutenberg 注释 × sections 顺序）。"""
    px = block_prefix()
    return "\n".join(f"<!-- wp:{px}/{sanitize_type(s['type'])} /-->"
                     for s in ir["sections"]) + "\n"


def dark_class_filter_snippet(page_slugs):
    """复刻页深色模式 body_class 片段（class-based dark 源站适用）。"""
    slugs = ", ".join(f"'{s}'" for s in page_slugs)
    return ("add_filter('body_class', function ($classes) {\n"
            "    if (is_page([%s])) { $classes[] = 'dark'; }\n"
            "    return $classes;\n});\n" % slugs)
