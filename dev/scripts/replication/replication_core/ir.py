"""ir — 中间表示（IR v1.0）构建与校验。IR = 平台无关契约，各产品适配器消费。"""
import json
import re
from . import IR_VERSION
from .extract_css import absolutize


def build_ir(url, sections, design, meta=None, dark_mode="class",
             ir_version=IR_VERSION):
    """组装 IR。sections = split_sections 产物（已 trim）；design = design_assets 产物。"""
    return {
        "irVersion": ir_version,
        "generatedAt": __import__("datetime").datetime.utcnow().isoformat() + "Z",
        "source": {"url": url, "ssr": bool(meta and meta.get("ssr"))},
        "darkMode": dark_mode,
        "design": {
            "css": design.get("css", ""),
            "tokens": design.get("tokens", {}),
            "breakpoints": design.get("breakpoints", {}),
            "fonts": design.get("fonts", {}),
            "cssFiles": design.get("cssFiles", []),
        },
        "sections": [
            {"order": s.get("order", i), "type": s["type"], "html": s["html"],
             "assets": sorted(set(re.findall(
                 r'(?:src|href|poster)="(https?://[^"]+)"', s.get("html", ""))))}
            for i, s in enumerate(sections)
        ],
        "meta": meta or {},
    }


def validate_ir(ir):
    """结构校验（不依赖 jsonschema 包）。返回 (ok, errors)。"""
    errors = []
    if ir.get("irVersion") != IR_VERSION:
        errors.append(f"irVersion 必须为 {IR_VERSION}")
    if not ir.get("source", {}).get("url"):
        errors.append("source.url 缺失")
    if not ir.get("design", {}).get("css"):
        errors.append("design.css 缺失（无 CSS 则视觉无法复刻）")
    sections = ir.get("sections") or []
    if not sections:
        errors.append("sections 为空")
    for i, s in enumerate(sections):
        if not s.get("type"):
            errors.append(f"sections[{i}].type 缺失")
        if not s.get("html"):
            errors.append(f"sections[{i}].html 缺失")
        if "<script" in s.get("html", ""):
            errors.append(f"sections[{i}].html 含 <script>（应剥离）")
    return (len(errors) == 0, errors)


def save_ir(ir, path):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(ir, f, ensure_ascii=False, indent=1)


def load_ir(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def absolutize_ir(ir, base_url):
    """IR 内全部 HTML/CSS 的相对资源 → 绝对 URL（就地）。"""
    base = base_url.rstrip("/")
    ir["design"]["css"] = absolutize(ir["design"].get("css", ""), base)
    for s in ir["sections"]:
        s["html"] = absolutize(s.get("html", ""), base)
    return ir
