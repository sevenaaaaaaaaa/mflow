#!/usr/bin/env python3
"""
build-index.py — generate 3 KB-Index files:
  - KB-Index/by-topic.md
  - KB-Index/citations.md
  - KB-Index/capability-glossary.md

Reads frontmatter from every KB .md under insight-data/Knowledge Base/.
Prints to stdout; writes only with --write.

Run as part of:
  bash kb-frontmatter.py && python3 build-index.py --write
"""

import argparse
import datetime
import re
import sys
from collections import defaultdict, Counter
from pathlib import Path


FRONT = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL | re.MULTILINE)
KV = re.compile(r"^([a-zA-Z_][\w-]*):\s*(.+?)\s*$", re.MULTILINE)

# YAML list value
LIST_RE = re.compile(r"^[a-zA-Z_][\w-]*:\s*$")


def parse_fm(text):
    m = FRONT.match(text)
    if not m:
        return {}
    body = m.group(1)
    out = {}
    i = 0
    lines = body.splitlines()
    while i < len(lines):
        line = lines[i]
        mhead = re.match(r"^([a-zA-Z_][\w-]*):\s*(.*)$", line)
        if not mhead:
            i += 1
            continue
        key, val = mhead.group(1), mhead.group(2)
        if val.strip() == "" and i + 1 < len(lines) and LIST_RE.match(lines[i+1]) is None and lines[i+1].startswith("  -"):
            # list mode
            items = []
            j = i + 1
            while j < len(lines):
                if lines[j].startswith("  - "):
                    items.append(lines[j][4:].strip())
                    j += 1
                elif lines[j].strip() == "":
                    j += 1
                else:
                    break
            out[key] = items
            i = j
        else:
            out[key] = val.strip().strip('"').strip("'")
            i += 1
    return out


def collect_kb(root):
    kb_root = root / "insight-data" / "Knowledge Base"
    if not kb_root.exists():
        sys.stderr.write(f"build-index: KB root not found at {kb_root}\n")
        sys.exit(1)
    skip_dirs = {".venv", "KB-Index", "scripts"}
    skip_files = {"KB-SCHEMA.md"}
    units = []
    for path in sorted(kb_root.rglob("*.md")):
        rel = str(path.relative_to(root))
        if any(s in rel for s in skip_dirs):
            continue
        if path.name in skip_files:
            continue
        text = path.read_text("utf-8", errors="ignore")
        fm = parse_fm(text)
        if not fm or not fm.get("schema_version"):
            continue
        units.append({"path": rel, **fm})
    return units


def build_by_topic(units):
    by_topic = defaultdict(list)
    for u in units:
        for t in (u.get("topics") or ["general"]):
            by_topic[t].append(u)
    return by_topic


def build_capability_glossary(units):
    """For each capability, list units that mention it + canonical URL priority."""
    by_cap = defaultdict(lambda: {"units": [], "all_urls": []})
    for u in units:
        for cap in (u.get("capabilities") or []):
            by_cap[cap]["units"].append(u)
            for url in (u.get("source_urls") or []):
                if "lovart.ai" in url and url not in by_cap[cap]["all_urls"]:
                    by_cap[cap]["all_urls"].append(url)
    # heuristic: pick canonical_url = first lovart.ai/docs/* > first lovart.ai/news/* > first any
    for cap, info in by_cap.items():
        urls = info["all_urls"]
        canon = next((u for u in urls if "/docs/" in u), None)
        if not canon:
            canon = next((u for u in urls if "/news/" in u), None)
        if not canon:
            canon = urls[0] if urls else None
        info["canonical_url"] = canon
    return by_cap


def render_by_topic(by_topic):
    lines = ["---",
             "type: kb-index/by-topic",
             "version: 1.0",
             "generated: 2026-07-05",
             "generator: build-index.py",
             "---",
             "",
             "# KB Index by Topic",
             "",
             "Each topic lists all KB units that touch it, ordered by authority (5 first).",
             ""]
    for topic in sorted(by_topic.keys()):
        units = sorted(by_topic[topic], key=lambda u: (-int(u.get("authority") or 0), u.get("path", "")))
        lines.append(f"## {topic}  ({len(units)} units)")
        for u in units:
            slug = u.get("kb_slug", "?")
            auth = u.get("authority", "?")
            origin = u.get("origin", "?")
            lines.append(f"- **[{auth}] {origin}**  `{slug}` — {u.get('path', '')}")
        lines.append("")
    lines.append("---")
    lines.append("")
    return "\n".join(lines)


def render_capability_glossary(by_cap):
    lines = ["---",
             "type: kb-index/capability-glossary",
             "version: 1.0",
             "generated: 2026-07-05",
             "generator: build-index.py",
             "---",
             "",
             "# Capability Glossary — Lovart 产品能力词表",
             "",
             "> writer profile 写 brand/product 表达时**只**使用本 glossary 内的 capability 名 + URL。",
             "> SEO 拓词时把关键词 → glossary 内 capability，匹配不到 = 不可用 / 需先入库。",
             ">",
             "> **canonical_url** = KB 里 authority 最高的 lovart.ai/docs/* 直链（writer 引用 URL 必取这个）。",
             ""]
    # group by category
    placeholders = []
    no_url = []
    for cap in sorted(by_cap.keys()):
        info = by_cap[cap]
        n = len(info["units"])
        if not info['canonical_url']:
            no_url.append(cap)
            placeholders.append((cap, info))
            continue
        first_unit = info["units"][0]
        lines.append(f"## `{cap}`  ({n} KB units)")
        lines.append(f"- canonical_url: `{info['canonical_url']}`")
        lines.append(f"- KB units:")
        for u in sorted(info["units"], key=lambda u: (-int(u.get("authority") or 0), u.get("path", "")))[:5]:
            lines.append(f"  - `{u.get('kb_slug', '?')}` (auth {u.get('authority')})")
        lines.append("")

    if placeholders:
        lines.append("---")
        lines.append("")
        lines.append("## ⚠️ Capabilities without canonical URL (need ingest)")
        for cap, _ in placeholders:
            lines.append(f"- `{cap}`")
        lines.append("")
    return "\n".join(lines)


def render_citations(units):
    """Citations = URL → which KB units reference it. Plus claim-level placeholder."""
    by_url = defaultdict(list)
    for u in units:
        for url in (u.get("source_urls") or []):
            by_url[url].append(u)

    lines = ["---",
             "type: kb-index/citations",
             "version: 1.0",
             "generated: 2026-07-05",
             "generator: build-index.py",
             "---",
             "",
             "# KB Citations — URL Authority Map",
             "",
             "> writer 写外链时**只**用本表中的 URL。URL 不在表里 = 拒绝。",
             ">",
             "> 反向：每条 claim 在哪个 unit；这条 claim 在哪个下游 blog/landing 引用（write-only 段）。",
             ""]

    lines.append("## URL → KB units (forward)")
    for url in sorted(by_url.keys()):
        units_here = sorted(by_url[url], key=lambda u: (-int(u.get("authority") or 0), u.get("path", "")))
        hosts = "lovart-official" if "lovart.ai" in url else "third-party"
        lines.append(f"\n### `{url}`  ({hosts}, {len(units_here)} units)")
        for u in units_here[:5]:
            lines.append(f"- `{u.get('kb_slug', '?')}` (auth {u.get('authority')}, {u.get('origin', '?')})")

    lines.append("\n---\n")
    lines.append("## Claim → KB unit (placeholder)")
    lines.append("")
    lines.append("> 每个 claim ID 形如 `[kb-{slug}-{n}]`，由 ingest 阶段扩展。此表反映**已被 KB 注册**的 claim。")
    lines.append("> 当下为占位 — 还未合并 inline claim markers，期待 Phase 2 ingest.")
    lines.append("")
    lines.append("_(empty until ingest populates claim blocks)_")
    return "\n".join(lines)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--root", default=".")
    p.add_argument("--write", action="store_true")
    args = p.parse_args()
    root = Path(args.root).expanduser().resolve()
    units = collect_kb(root)

    by_topic = build_by_topic(units)
    by_cap = build_capability_glossary(units)

    print(f"kb units: {len(units)}")
    print(f"topics:   {len(by_topic)}")
    print(f"capabilities: {len(by_cap)}")
    if not args.write:
        # preview only
        return

    out_dir = root / "insight-data" / "Knowledge Base" / "KB-Index"
    out_dir.mkdir(parents=True, exist_ok=True)

    (out_dir / "by-topic.md").write_text(render_by_topic(by_topic), encoding="utf-8")
    (out_dir / "citations.md").write_text(render_citations(units), encoding="utf-8")
    (out_dir / "capability-glossary.md").write_text(render_capability_glossary(by_cap), encoding="utf-8")
    print(f"wrote {out_dir}/by-topic.md")
    print(f"wrote {out_dir}/citations.md")
    print(f"wrote {out_dir}/capability-glossary.md")


if __name__ == "__main__":
    main()
