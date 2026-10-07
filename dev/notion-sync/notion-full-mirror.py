#!/usr/bin/env python3
"""Enumerate scoped files for Notion full-mirror sync. Outputs sync-queue.jsonl."""
from __future__ import annotations

import fnmatch
import hashlib
import json
import re
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]  # 1-Project
SCOPE = json.loads((Path(__file__).parent / "sync-scope.json").read_text())
TARGETS = json.loads((Path(__file__).parent / "notion-targets.json").read_text())
OUT = Path(__file__).parent / "sync-queue.jsonl"
MANIFEST = Path(__file__).parent / "sync-progress.json"

DB_IDS = {k: v["data_source_id"] for k, v in TARGETS["databases"].items()}


def load_scope() -> dict:
    return SCOPE


def sha256_text(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()[:16]


def excluded(rel: str, name: str, scope: dict) -> bool:
    ex = scope["exclude"]
    for p in ex["path_prefixes"]:
        if rel.startswith(p) or rel.startswith(p.rstrip("/") + "/"):
            return True
    for pat in ex["filename_patterns"]:
        if fnmatch.fnmatch(name, pat):
            return True
    rel_posix = rel.replace("\\", "/")
    if rel_posix in ex.get("superseded_docs", []):
        return True
    for glob_pat in ex["path_globs"]:
        g = glob_pat.replace("**/", "")
        if g in rel_posix:
            return True
    return False


def walk_md_under(base: Path, rel_base: str, extra_exclude: list[str] | None = None) -> list[Path]:
    if not base.exists():
        return []
    out = []
    for p in sorted(base.rglob("*")):
        if not p.is_file():
            continue
        rel = str(p.relative_to(ROOT)).replace("\\", "/")
        if extra_exclude and rel in extra_exclude:
            continue
        if excluded(rel, p.name, SCOPE):
            continue
        if p.suffix.lower() not in (".md", ".mdc"):
            continue
        if "notion-sync/templates" in rel or rel.endswith("sync-queue.jsonl"):
            continue
        out.append(p)
    return out


def walk_skill_docs(skill_root: str, scope: dict) -> list[Path]:
    base = ROOT / skill_root
    if not base.exists():
        return []
    skip_parts = ("scripts", "credentials", "samples", "_fixtures", "feedback", "node_modules")
    out = []
    for p in sorted(base.rglob("*")):
        if not p.is_file():
            continue
        if any(part in p.parts for part in skip_parts):
            continue
        if p.suffix.lower() != ".md":
            continue
        rel = str(p.relative_to(ROOT)).replace("\\", "/")
        if excluded(rel, p.name, scope):
            continue
        out.append(p)
    return out


def walk_glob_md(pattern: str) -> list[Path]:
    # pattern like insight-data/Trident Insights/reports/**/*.md
    base_part = pattern.split("**")[0].rstrip("/")
    base = ROOT / base_part
    if not base.exists():
        return []
    out = []
    for p in sorted(base.rglob("*.md")):
        rel = str(p.relative_to(ROOT)).replace("\\", "/")
        if excluded(rel, p.name, SCOPE):
            continue
        if "/raw/" in rel:
            continue
        out.append(p)
    return out


def walk_files(paths: list[str], extensions: tuple[str, ...], exclude_dirs: list[str] | None = None) -> list[Path]:
    out = []
    for item in paths:
        p = ROOT / item
        if p.is_file() and p.suffix.lower() in extensions:
            rel = str(p.relative_to(ROOT)).replace("\\", "/")
            if not excluded(rel, p.name, SCOPE):
                out.append(p)
        elif p.is_dir():
            for f in sorted(p.rglob("*")):
                if not f.is_file() or f.suffix.lower() not in extensions:
                    continue
                rel = str(f.relative_to(ROOT)).replace("\\", "/")
                if exclude_dirs and any(rel.startswith(d) for d in exclude_dirs):
                    continue
                if excluded(rel, f.name, SCOPE):
                    continue
                out.append(f)
    return out


def report_type(rel: str) -> str:
    r = rel.lower()
    if "sentinel" in r or "lovart orm" in r:
        return "Sentinel"
    if "monthly" in r:
        return "SEO Monthly"
    if "weekly" in r or "周报" in r:
        return "SEO Weekly"
    if "daily" in r or "automation-reports" in r:
        return "SEO Daily"
    if "audit" in r or "quality" in r:
        return "Audit"
    if "quarterly" in r:
        return "Research"
    return "Research"


def resource_type(rel: str) -> str:
    if "SKILL" in rel or "Skills/" in rel:
        return "Rule"
    if "SOP" in rel:
        return "SOP"
    if "定期任务" in rel or "AGENTS" in rel:
        return "Rule"
    return "Reference"


def make_entry(batch: str, rel: str, db: str, p: Path) -> dict:
    try:
        body = p.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return {}
    title = p.stem
    if title in ("README", "SKILL"):
        title = f"{p.parent.name}/{p.name}"
    props = {
        "Name": title[:200],
        "Source Path": rel,
        "Local ID": f"lifeos:mirror:{sha256_text(rel)}",
        "date:Last Synced At:start": date.today().isoformat(),
        "date:Last Synced At:is_datetime": 0,
    }
    if db == "Resources":
        props["Type"] = resource_type(rel)
        props["Status"] = "Current"
        props["Summary"] = body[:500].replace("\n", " ")
    elif db == "Reports/Insights":
        props["Report Type"] = report_type(rel)
        props["Status"] = "Published"
        props["Period"] = rel.split("/")[-2] if "/" in rel else ""
        props["Key Insight"] = body[:300].replace("\n", " ")
    elif db == "Automations":
        props["Status"] = "Active"
        props["Cadence"] = "see doc"
        props["Entry Command"] = rel
    return {
        "batch": batch,
        "database": db,
        "data_source_id": DB_IDS[db],
        "rel_path": rel,
        "content_hash": sha256_text(body),
        "properties": props,
        "content": body[:95000],  # Notion safe chunk; very long split later
        "content_truncated": len(body) > 95000,
    }


def collect_all() -> list[dict]:
    scope = load_scope()
    entries: list[dict] = []

    kb = scope["include"]["knowledge_base"]
    for p in walk_md_under(ROOT, ""):
        rel = str(p.relative_to(ROOT)).replace("\\", "/")
        if not any(rel == x.rstrip("/") or rel.startswith(x.rstrip("/") + "/") or rel == Path(x).name for x in kb["paths"] if not x.endswith("/")):
            # match explicit files and dirs
            ok = False
            for x in kb["paths"]:
                x = x.replace("\\", "/")
                if x.endswith("/"):
                    if rel.startswith(x):
                        ok = True
                        break
                elif rel == x:
                    ok = True
                    break
            if not ok:
                continue
        if rel in kb.get("exclude_under_paths", []):
            continue
        e = make_entry("K1", rel, kb["target_database"], p)
        if e:
            entries.append(e)

    for root in scope["include"]["confirmed_agent_skills"]["skill_roots"]:
        for p in walk_skill_docs(root, scope):
            rel = str(p.relative_to(ROOT)).replace("\\", "/")
            e = make_entry("S1", rel, "Resources", p)
            if e:
                entries.append(e)

    hh = scope["include"]["harness_hub"]
    for p in walk_files(hh["paths"], (".md",)):
        rel = str(p.relative_to(ROOT)).replace("\\", "/")
        for pat in hh.get("exclude_patterns", []):
            if fnmatch.fnmatch(p.name, pat):
                continue
        else:
            e = make_entry("H1", rel, hh["target_database"], p)
            if e:
                entries.append(e)

    for pat in scope["include"]["reports"]["paths"]:
        if "**" in pat:
            for p in walk_glob_md(pat):
                rel = str(p.relative_to(ROOT)).replace("\\", "/")
                batch = "R1" if "Trident" in rel or "Lovart ORM" in rel else (
                    "R2" if "Keywords" in rel or "Page Analytic" in rel else "R3"
                )
                e = make_entry(batch, rel, "Reports/Insights", p)
                if e:
                    entries.append(e)

    ao = scope["include"]["automation_ops"]
    ex = ao.get("exclude_paths", [])
    for item in ao["paths"]:
        item = item.replace("\\", "/")
        if "**" in item:
            base_part = item.split("**")[0].rstrip("/")
            base = ROOT / base_part
            if not base.exists():
                continue
            for f in sorted(base.rglob("*")):
                if not f.is_file():
                    continue
                if f.suffix.lower() not in (".md", ".sh", ".json"):
                    continue
                rel = str(f.relative_to(ROOT)).replace("\\", "/")
                if any(rel.startswith(d.rstrip("/") + "/") or rel == d for d in ex):
                    continue
                if excluded(rel, f.name, SCOPE):
                    continue
                e = make_entry("A1", rel, "Automations", f)
                if e:
                    entries.append(e)
        else:
            for ext in (".md", ".sh", ".json"):
                p = ROOT / item
                if p.is_file() and p.suffix.lower() == ext:
                    rel = str(p.relative_to(ROOT)).replace("\\", "/")
                    if not excluded(rel, p.name, SCOPE):
                        e = make_entry("A1", rel, "Automations", p)
                        if e:
                            entries.append(e)

    # dedupe by rel_path
    seen = set()
    uniq = []
    for e in entries:
        if e["rel_path"] in seen:
            continue
        seen.add(e["rel_path"])
        uniq.append(e)
    return uniq


def main() -> None:
    entries = collect_all()
    OUT.write_text("\n".join(json.dumps(e, ensure_ascii=False) for e in entries) + "\n", encoding="utf-8")
    by_batch: dict[str, int] = {}
    for e in entries:
        by_batch[e["batch"]] = by_batch.get(e["batch"], 0) + 1
    MANIFEST.write_text(
        json.dumps(
            {
                "generated": date.today().isoformat(),
                "total": len(entries),
                "by_batch": by_batch,
                "status": "queued",
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    print(json.dumps({"total": len(entries), "by_batch": by_batch}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
