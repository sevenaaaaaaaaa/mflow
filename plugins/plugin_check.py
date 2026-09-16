#!/usr/bin/env python3
"""plugin_check.py — MFlow 插件校验器（六项检查）。用法：python3 plugin_check.py plugins/<dir>"""
import json, re, sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")  # py3.7+; 老 py3.6 静默跳过
except Exception:
    pass

TYPES = {"source", "publisher", "template"}
REQUIRED = ["id", "type", "name", "version", "entry"]

def check(plugin_dir):
    d = Path(plugin_dir)
    errs, oks = [], []
    mf = d / "manifest.json"
    if not mf.exists():
        return [f"缺少 manifest.json"], []
    try:
        m = json.loads(mf.read_text())
    except Exception as e:
        return [f"manifest.json 解析失败: {e}"], []
    for k in REQUIRED:
        (oks if m.get(k) else errs).append(f"manifest.{k} " + ("✓" if m.get(k) else "缺失"))
    if m.get("type") not in TYPES:
        errs.append(f"type '{m.get('type')}' 不在 {TYPES}")
    if d.name != m.get("id"):
        errs.append(f"目录名 '{d.name}' 与 id '{m.get('id')}' 不一致")
    entry = d / str(m.get("entry", ""))
    if not entry.exists():
        errs.append(f"entry 文件不存在: {entry}")
    else:
        code = entry.read_text(errors="ignore")
        for fn in ({"source": ["collect"], "publisher": ["publish"]}.get(m.get("type"), [])):
            (oks if f"def {fn}" in code else errs).append(
                f"entry 暴露 {fn}() " + ("✓" if f"def {fn}" in code else "缺失"))
        for perm in m.get("permissions", []):
            if perm.startswith("credentials:"):
                continue
        # 明文密钥粗查
        if re.search(r"(api[_-]?key|secret|token)\s*[:=]\s*['\"][A-Za-z0-9]{16,}", code, re.I):
            errs.append("疑似明文密钥硬编码（应走 permissions/credentials 或 config）")
        else:
            oks.append("无明文密钥 ✓")
    return errs, oks

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__); sys.exit(2)
    errs, oks = check(sys.argv[1])
    for o in oks: print("  ✓", o)
    for e in errs: print("  ✗", e)
    print("VERDICT:", "PASS" if not errs else f"FAIL ({len(errs)})")
    sys.exit(1 if errs else 0)
