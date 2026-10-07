#!/usr/bin/env python3
"""storylines.py — 故事线 SSOT 加载与 section 顺序校验（纯标准库）。

SSOT：`genflow/Page Gen/Refresh-Page/`（STORYLINES.md + landing/solution/scenarios-storylines.json）。
手册规则：bodyJson 的 type 顺序必须与所选故事线的 sections 数组一致；
**变体族内可替换**（如 bento-2→bento-6、hero-split→hero-cinematic），跨族增删必须改故事线本身。

2026-09-28 差距分析 P0-2：此前顺序正确性只靠提示词与批量脚本内嵌副本，
console/发布链零执行 —— 本模块把顺序校验接进发布链（sanity_publisher.publish_landing）。
T-long / 空序列 = "以 production 为准"，视为无固定序列，跳过校验。
"""
import json
import re
from pathlib import Path

from section_registry import family_of

STORYLINE_DIR = Path(__file__).resolve().parents[3] / "genflow" / "Page Gen" / "Refresh-Page"
JSON_SOURCES = ("landing-storylines.json", "solution-storylines.json", "scenarios-storylines.json")
# 无固定序列的故事线（module 序列"以 production 为准"）
NO_FIXED_SEQUENCE = {"T-long"}
_MD_CACHE = {"mtime": None, "data": None}


def _load_json_storylines(out):
    for name in JSON_SOURCES:
        p = STORYLINE_DIR / name
        try:
            d = json.loads(p.read_text(encoding="utf-8"))
        except Exception:
            continue
        for sid, s in (d.get("storylines") or {}).items():
            if isinstance(s, dict) and isinstance(s.get("sections"), list) and s["sections"]:
                out[sid] = {"sections": [str(x) for x in s["sections"]], "source": name}


def _load_md_storylines(out):
    """STORYLINES.md 表格（F/T/P/C/K/N + T-long）：每行最后一个单元格内是反引号包裹的 type 序列。"""
    p = STORYLINE_DIR / "STORYLINES.md"
    try:
        txt = p.read_text(encoding="utf-8")
        mt = p.stat().st_mtime
    except Exception:
        return
    if _MD_CACHE["mtime"] == mt and _MD_CACHE["data"] is not None:
        out.update(_MD_CACHE["data"])
        return
    parsed = {}
    for line in txt.split("\n"):
        m = re.match(r"^\|\s*\*\*([^*|]+?)\*\*\s*\|", line)
        if not m:
            continue
        sid = m.group(1).strip()
        cells = [c.strip() for c in line.split("|") if c.strip()]
        types = re.findall(r"`([a-z0-9-]+)`", cells[-1]) if cells else []
        # 无反引号序列（如 T-long「以 production 为准」）= 无固定序列，不收录
        if types:
            parsed[sid] = {"sections": types, "source": "STORYLINES.md"}
    _MD_CACHE["mtime"], _MD_CACHE["data"] = mt, parsed
    out.update(parsed)


def load_storylines():
    """返回 {storyline_id: {"sections": [type…], "source": 文件}}。"""
    out = {}
    _load_json_storylines(out)
    _load_md_storylines(out)
    return out


def check_storyline(types, storyline_id):
    """校验页面 type 序列是否符合故事线（族内变体可替换）。

    返回 {"known", "fixed", "ok", "problems", "expected"}：
      known=False  故事线未注册（调用方降级为 warning，不拦发布）
      fixed=False  故事线存在但无固定序列（如 T-long），跳过
      ok=False     problems 里是逐条 BLOCK 级错位描述
    """
    empty = {"known": False, "fixed": False, "ok": True, "problems": [], "expected": []}
    sid = (storyline_id or "").strip()
    if not sid:
        return empty
    if sid in NO_FIXED_SEQUENCE:  # 发布链默认值，明确无固定序列
        return {"known": True, "fixed": False, "ok": True, "problems": [], "expected": []}
    story = load_storylines().get(sid)
    if not story:
        return empty
    exp = story["sections"]
    if not exp:
        return {"known": True, "fixed": False, "ok": True, "problems": [], "expected": []}
    problems = []
    if len(types) != len(exp):
        problems.append(f"段数不符：故事线 {sid} 要求 {len(exp)} 段，实际 {len(types)} 段")
    for pos, want in enumerate(exp):
        got = types[pos] if pos < len(types) else "（缺段）"
        if family_of(str(got)) != family_of(want):
            problems.append(
                f"位置 {pos + 1}：故事线要求 {want}（族 {family_of(want)}），实际 {got}（族 {family_of(str(got))}）；"
                f"族内变体可替换，跨族增删必须改故事线本身")
    return {"known": True, "fixed": True, "ok": not problems,
            "problems": problems, "expected": exp}


if __name__ == "__main__":
    import sys
    types = [t.strip() for t in ",".join(sys.argv[2:]).split(",") if t.strip()]
    r = check_storyline(types, sys.argv[1] if len(sys.argv) > 1 else "")
    print(json.dumps(r, ensure_ascii=False, indent=1))
