#!/usr/bin/env python3
"""section_registry.py — composite-v2 section 注册表与逐型字段校验（纯标准库）。

字段级唯一权威：`1-4 Dev/Sanity Composite Page Section README.md`（本文件是其机器可执行版）。
体系来源：`1-4 Dev/Composite Page 组件开发手册.md`（21 族；README 逐型枚举 34 型 —— 预览夹具
preview-data.json 含 33 型，`feature-grid` 是 bento 系共享底层，README 允许直接使用，故一并注册）。

为什么必须有这一层（2026-09-28 差距分析 P0-1）：
  - 前端按 `type` 字符串分发，**未注册 type 渲染为空**（不报错、不白屏）→ 错误静默丢失
  - 字段错配（faq items=[[q,a]]、proof-block 用 stats 字段、pricing 写 plans）曾直接入库上线
  - icon 不在白名单渲染为空；media.src 非绝对 URL 图片不显示
校验分级：errors=BLOCK（结构/契约破坏，拦发布）；warnings=建议（不拦，进发布结果的 warnings）。
逃逸口：环境变量 MFLOW_SKIP_REGISTRY=1 可整体跳过（应急用，常规禁止）。
"""
import re

# icon 白名单（README「Icon key 字典」；其它值渲染为空，自定义图形走 media.src）
ICON_KEYS = frozenset({
    "chat", "image", "flask", "brand", "globe", "refresh", "search",
    "pointer", "video", "sparkle", "social", "remove-bg",
})
BUTTON_VARIANTS = frozenset({"primary", "secondary", "outline"})
BUTTON_ACTIONS = frozenset({"openLogin"})  # 仅 cta-default 支持登录按钮（README）
VIDEO_SUFFIX_RE = re.compile(r"\.(mp4|webm|mov|m4v)(\?|$)", re.I)

# 旧 8 型（legacy/*.tsx 仅兼容线上历史数据，新文档禁用）
LEGACY_TYPES = frozenset({
    "heroSection", "contentSection", "faqSection", "textImageSection",
    "threeColumnSection", "testimonialSection", "centeredInputSection", "featureGridSection",
})

# 仅图片的族（README：comparison-before-after 拖拽语义、media-marquee 多视频有性能问题）
IMAGE_ONLY_TYPES = frozenset({"media-marquee", "comparison-before-after"})

# 族 = 可互换的变体集合（手册：变体族内可替换，跨族增删必须改故事线）
FAMILIES = {
    "hero": ["hero-split", "hero-cinematic", "hero-journey", "hero-mosaic", "hero-gallery"],
    "bento": ["bento-2", "bento-4", "bento-6", "feature-grid", "cluster-block-dense"],
    "portrait": ["portrait-grid-3", "portrait-grid-4"],
    "showcase": ["showcase-stacked", "showcase-horizontal"],
    "workflow": ["workflow-horizontal", "workflow-vertical"],
    "compare": ["comparison-table", "comparison-before-after"],
    "review": ["review-grid-3col", "review-grid-4col"],
}


def family_of(type_name):
    """type → 所属族（单型族的族名 = 自身）。故事线顺序校验按族比较。"""
    for fam, members in FAMILIES.items():
        if type_name in members:
            return fam
    return type_name


# 逐型 schema：
#   family           所属族
#   required         顶层必填字段（非空）
#   arrays           数组字段 → {item_required, any_of, str_items, nested, optional, legacy}
#   enum_fields      顶层枚举字段 → 合法值（违规 warn）
#   forbid           禁止字段 → 提示语（BLOCK，契约级错配）
#   min_items        (数组名, 下限) 低于下限 warn（视觉完整性建议）
# 数组元素的 media/icon/buttons/src 校验由 _walk 统一做（避免与数组 spec 双报）。
_BTN = {"item_required": ["text"]}
_FEAT = {"item_required": ["title"], "media": True}

SPECS = {
    # ── Hero 族（5）──
    "hero-split": {"family": "hero", "required": ["title"],
                   "arrays": {"buttons": {**_BTN, "optional": True}}},
    "hero-cinematic": {"family": "hero", "required": ["title"],
                       "arrays": {"buttons": {**_BTN, "optional": True}}},
    "hero-journey": {"family": "hero", "required": ["title"],
                     "arrays": {"buttons": {**_BTN, "optional": True},
                                "journeyCards": {"item_required": ["title"]}}},
    "hero-mosaic": {"family": "hero", "required": ["title"],
                    "arrays": {"buttons": {**_BTN, "optional": True},
                               "mosaicTiles": {"item_required": ["title"], "media": True}}},
    "hero-gallery": {"family": "hero", "required": ["title"],
                     "arrays": {"buttons": {**_BTN, "optional": True},
                                "toolTiles": {"item_required": ["label"], "media": True}}},
    # ── Bento / 网格 / 信息簇（5）──
    "bento-2": {"family": "bento", "arrays": {"features": dict(_FEAT)}},
    "bento-4": {"family": "bento", "arrays": {"features": dict(_FEAT)}},
    "bento-6": {"family": "bento", "arrays": {"features": dict(_FEAT)}},
    "feature-grid": {"family": "bento", "enum_fields": {"columns": (2, 3, 4)},
                     "arrays": {"features": dict(_FEAT)}},
    "cluster-block-dense": {"family": "bento",
                            "arrays": {"cards": {"item_required": ["title", "description"]}}},
    # ── Tabs / Tool / Blog / 详情 / 画布 ──
    "capability-tabs": {"family": "capability-tabs", "required": ["tabs"],
                        "arrays": {"tabs": {"item_required": ["label", "content"],
                                            "nested": {"content": {"required": ["title"]}}}}},
    "tool-grid": {"family": "tool-grid", "arrays": {"tools": {"item_required": ["name"]}}},
    "blog-grid": {"family": "blog-grid",
                  "arrays": {"articles": {"item_required": ["title"],
                                          "any_of": [("slug", "href"), ("image", "media")]}}},
    "feature-detail": {"family": "feature-detail",
                       "arrays": {"items": {"item_required": ["title", "description"], "media": True}}},
    "canvas-wall": {"family": "canvas-wall", "min_items": ("items", 10),
                    "arrays": {"items": {"media": True}}},
    # ── 竖卡 / Showcase ──
    "portrait-grid-3": {"family": "portrait", "arrays": {"cards": {"item_required": ["title"], "media": True}}},
    "portrait-grid-4": {"family": "portrait", "arrays": {"cards": {"item_required": ["title"], "media": True}}},
    "showcase-stacked": {"family": "showcase", "arrays": {"items": {"item_required": ["title"], "media": True}}},
    "showcase-horizontal": {"family": "showcase", "arrays": {"items": {"item_required": ["title"], "media": True}}},
    # ── 跑马灯 / 输入 / Logo ──
    "media-marquee": {"family": "media-marquee", "arrays": {"items": {"item_required": ["src"]}}},
    "prompt-launcher": {"family": "prompt-launcher",
                        "arrays": {"prompts": {"item_required": ["prompt"], "optional": True},
                                   "suggestions": {"str_items": True, "optional": True}}},
    "logo-loop": {"family": "logo-loop"},
    # ── CTA / 流程 ──
    "cta-default": {"family": "cta-default", "required": ["title"], "arrays": {"buttons": dict(_BTN)}},
    "workflow-horizontal": {"family": "workflow", "arrays": {"steps": {"item_required": ["title", "description"]}}},
    "workflow-vertical": {"family": "workflow", "arrays": {"steps": {"item_required": ["title", "description"], "media": True}}},
    # ── 对比 ──
    "comparison-table": {"family": "compare", "required": ["headers", "rows"]},
    "comparison-before-after": {"family": "compare", "required": ["before", "after"]},
    # ── 证言 / 评价 ──
    "testimonial": {"family": "testimonial",
                    "arrays": {"testimonials": {"item_required": ["quote", "author"], "optional": True},
                               "quotes": {"item_required": ["content", "name"], "optional": True,
                                          "legacy": "quotes 是旧字段（兼容期），新内容请用 testimonials"}}},
    "review-grid-3col": {"family": "review", "arrays": {"reviews": {"item_required": ["title", "body", "author"]}}},
    "review-grid-4col": {"family": "review", "arrays": {"reviews": {"item_required": ["title", "body", "author"]}}},
    # ── 数据 / 信任 / 定价 / FAQ ──
    "stats": {"family": "stats", "arrays": {"stats": {"item_required": ["value", "label"]}}},
    "proof-block": {"family": "proof-block", "arrays": {"cards": {"item_required": ["title", "description"]}}},
    # 定价走后端 SDK，CMS 只写标题描述（手册 §1.3）；曾实测批量脚本写入 plans 具体价格
    "pricing-block": {"family": "pricing-block",
                      "forbid": {"plans": "价格走后端 SDK，CMS 里只写 title/description，不维护具体价格"}},
    "faq": {"family": "faq", "arrays": {"items": {"item_required": ["question", "answer"],
                                                  "reject_pair_list": True}}},
}


def _is_video(src, media):
    return (media or {}).get("type") == "video" or bool(VIDEO_SUFFIX_RE.search(src or ""))


def _walk_media_icon_buttons(i, sec, type_name, errors, warnings):
    """递归校验一段 section 内所有 media / icon / buttons / src（与数组 spec 解耦，只报一次）。"""
    image_only = type_name in IMAGE_ONLY_TYPES

    def walk(node, path):
        if isinstance(node, dict):
            for k, v in node.items():
                p = f"{path}.{k}"
                if k == "media" and isinstance(v, dict):
                    src = v.get("src")
                    if not isinstance(src, str) or not src.strip():
                        # 缺图 = 前端媒体位留白（页面仍成立）；坏引用才是事故 → BLOCK
                        warnings.append(f"{path}.media 缺 src（无图渲染留白，图片位建议必填）")
                    elif not src.startswith(("http://", "https://", "/")):
                        errors.append(f"{p}.src 非绝对 URL（CDN https://… 或 /assets/…），前端不显示")
                    else:
                        if image_only and _is_video(src, v):
                            errors.append(f"{p} 为视频位，但 {type_name} 仅支持图片（README：性能/交互语义）")
                        if _is_video(src, v) and not v.get("poster"):
                            warnings.append(f"{p} 是视频但缺 poster（首屏 LCP 建议必填）")
                    if not (v.get("alt") or "").strip():
                        warnings.append(f"{p}.media 缺 alt（前端用 title 兜底，可访问性建议补）")
                    continue
                if k == "icon":
                    if isinstance(v, str) and v and v not in ICON_KEYS:
                        errors.append(f"{p}={v!r} 不在 icon 白名单 {sorted(ICON_KEYS)}，渲染为空（自定义图形走 media.src）")
                    continue
                if k == "buttons" and isinstance(v, list):
                    for bi, b in enumerate(v):
                        if not isinstance(b, dict) or not (b.get("text") or "").strip():
                            errors.append(f"{p}.buttons[{bi}] 缺 text")
                            continue
                        if b.get("variant") and b["variant"] not in BUTTON_VARIANTS:
                            errors.append(f"{p}.buttons[{bi}].variant={b['variant']!r} 非法（primary/secondary/outline）")
                        if b.get("action") and b["action"] not in BUTTON_ACTIONS:
                            errors.append(f"{p}.buttons[{bi}].action={b['action']!r} 非法（仅 openLogin）")
                        if b.get("action") == "openLogin" and type_name != "cta-default":
                            warnings.append(f"{p}.buttons[{bi}] action=openLogin 仅 cta-default 支持，此处忽略")
                        if not b.get("href") and not b.get("action"):
                            warnings.append(f"{p}.buttons[{bi}] 无 href 且无 action，将渲染为 #（停留当前页）")
                    continue
                if k == "src" and isinstance(v, str) and v.strip():
                    if not v.startswith(("http://", "https://", "/")):
                        errors.append(f"{p}.src 非绝对 URL，前端不显示")
                    elif image_only and VIDEO_SUFFIX_RE.search(v):
                        errors.append(f"{p} 为视频 URL，但 {type_name} 仅支持图片")
                    continue
                walk(v, p)
        elif isinstance(node, list):
            for i, x in enumerate(node):
                walk(x, f"{path}[{i}]")

    walk(sec, f"sections[{i}]({type_name})")


def _check_section(i, s, errors, warnings):
    tag = f"sections[{i}]"
    if not isinstance(s, dict):
        errors.append(f"{tag} 不是对象（每条 section 必须是 {{type, …}}）")
        return
    t = s.get("type")
    if not t or not isinstance(t, str):
        errors.append(f"{tag} 缺 type 字符串")
        return
    tag = f"{tag}({t})"
    if t in LEGACY_TYPES:
        errors.append(f"{tag} 是 legacy 旧 8 型（仅兼容线上历史数据），新文档禁用")
        return
    spec = SPECS.get(t)
    if spec is None:
        hint = ""
        flat = re.sub(r"([a-z])([A-Z])", r"\1-\2", t).lower()  # camelCase → 短横线
        if flat in SPECS:
            hint = f"；疑似驼峰/大小写错写，应为 {flat!r}"
        errors.append(f"{tag} 未注册（前端按 type 分发，未注册渲染为空 = 该段静默丢失）{hint}")
        return
    for f in spec.get("required", ()):
        v = s.get(f)
        if v is None or (isinstance(v, str) and not v.strip()) or \
           (isinstance(v, (list, dict)) and not v):
            errors.append(f"{tag} 缺必填字段 {f}")
    for f, msg in spec.get("forbid", {}).items():
        if f in s:
            errors.append(f"{tag} 含禁止字段 {f}：{msg}")
    for f, allowed in spec.get("enum_fields", {}).items():
        if f in s and s[f] not in allowed:
            warnings.append(f"{tag}.{f}={s[f]!r} 不在预设值 {list(allowed)}（渲染按默认处理）")
    name, low = spec.get("min_items", (None, 0))
    # 数组字段校验
    for fname, asp in spec.get("arrays", {}).items():
        arr = s.get(fname)
        if arr in (None, []):
            if not asp.get("optional"):
                errors.append(f"{tag} 缺 {fname} 数组（渲染为空段）")
            continue
        if not isinstance(arr, list):
            errors.append(f"{tag}.{fname} 必须是数组")
            continue
        if name == fname and len(arr) < low:
            warnings.append(f"{tag}.{fname} 仅 {len(arr)} 条（< {low}，视觉不完整，建议补足）")
        if asp.get("str_items"):
            bad = [j for j, x in enumerate(arr) if not isinstance(x, str) or not x.strip()]
            if bad:
                errors.append(f"{tag}.{fname}[{bad[0]}] 应为非空字符串")
            continue
        if asp.get("reject_pair_list") and arr and isinstance(arr[0], list):
            errors.append(f"{tag}.{fname} 是 [[q,a]] 数对嵌套（实测错配形态）：手册要求 [{{question, answer}}]，"
                          f"现形态前端渲染为空")
            continue
        req = asp.get("item_required") or []
        any_of = asp.get("any_of") or []
        nested = asp.get("nested") or {}
        for j, item in enumerate(arr):
            itag = f"{tag}.{fname}[{j}]"
            if not isinstance(item, dict):
                errors.append(f"{itag} 不是对象")
                continue
            for f in req:
                v = item.get(f)
                if v is None or (isinstance(v, str) and not v.strip()):
                    errors.append(f"{itag} 缺 {f}")
            for group in any_of:
                if not any(item.get(g) for g in group):
                    errors.append(f"{itag} 缺 {' / '.join(group)}（任一即可）")
            for nf, nsp in nested.items():
                sub = item.get(nf)
                if isinstance(sub, dict):
                    for f in nsp.get("required", ()):
                        if not sub.get(f):
                            errors.append(f"{itag}.{nf} 缺 {f}")
                elif sub is not None:
                    errors.append(f"{itag}.{nf} 应为对象")
        if asp.get("legacy") and arr:
            warnings.append(f"{tag}.{fname}：{asp['legacy']}")
    # 全量走查 media/icon/buttons/src（与数组 spec 互补，只按一条路径报）
    _walk_media_icon_buttons(i, s, t, errors, warnings)


def validate_sections_full(sections):
    """注册表校验。返回 {"errors": [BLOCK…], "warnings": [建议…]}。"""
    errors, warnings = [], []
    if not isinstance(sections, list) or not sections:
        return {"errors": ["sections 必须是非空数组"], "warnings": []}
    for i, s in enumerate(sections):
        _check_section(i, s, errors, warnings)
    return {"errors": errors, "warnings": warnings}


def validate_sections(sections):
    """仅返回 BLOCK 级错误字符串列表（兼容旧调用方签名）。"""
    return validate_sections_full(sections)["errors"]


if __name__ == "__main__":
    import json
    import sys
    data = json.loads(sys.stdin.read()) if not sys.argv[1:] else json.loads(open(sys.argv[1]).read())
    secs = data.get("sections", data) if isinstance(data, dict) else data
    r = validate_sections_full(secs)
    print(json.dumps(r, ensure_ascii=False, indent=1))
    sys.exit(1 if r["errors"] else 0)
