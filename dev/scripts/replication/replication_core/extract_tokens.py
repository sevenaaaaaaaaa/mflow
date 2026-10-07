"""extract_tokens — CSS 变量提取与语义分组（供 theme 映射消费）。"""
import re


def extract_tokens(css):
    """:root 变量全量（键 → 值）。"""
    tokens = {}
    for block in re.findall(r":root[^{]*\{([^}]+)\}", css):
        for k, v in re.findall(r"(--[a-zA-Z0-9-]+)\s*:\s*([^;]+)", block):
            tokens.setdefault(k, v.strip())
    return tokens


def group_tokens(tokens):
    """按首个语义段分组（text/bg/color/font/border/radius…）。"""
    groups = {}
    for k, v in tokens.items():
        g = re.split(r"[-/]", k[2:])[0] if k.startswith("--") else "other"
        groups.setdefault(g, []).append((k, v))
    return {g: sorted(items) for g, items in groups.items()}


def hex_palette(tokens, limit=24):
    """可直接用作色板的十六进制色（按出现序去重）。"""
    out = []
    for k, v in tokens.items():
        if re.match(r"^#[0-9a-fA-F]{3,8}$", v.strip()) and v.strip() not in out:
            out.append(v.strip())
        if len(out) >= limit:
            break
    return out
