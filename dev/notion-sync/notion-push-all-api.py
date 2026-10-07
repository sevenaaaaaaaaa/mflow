#!/usr/bin/env python3
"""Push prepared .batch-out/*.json files via Notion MCP-compatible create flow.

Uses notion-create-pages semantics by calling Notion API with converted properties.
"""
from __future__ import annotations

import json
import sys
import urllib.error
import urllib.request
from pathlib import Path

SYNC = Path(__file__).parent
BATCH_DIR = SYNC / ".batch-out"
PROGRESS = SYNC / "sync-pushed.jsonl"
TOKEN_PATH = Path.home() / ".config/notion/api_key"
NOTION_VERSION = "2022-06-28"


def token() -> str:
    return TOKEN_PATH.read_text(encoding="utf-8").strip()


def sqlite_prop(name: str, value) -> dict:
    if name.startswith("date:"):
        return {}
    if value is None:
        return {}
    if name == "Name":
        return {"title": [{"type": "text", "text": {"content": str(value)}}]}
    if isinstance(value, (int, float)):
        return {"number": value}
    if value in ("__YES__", "__NO__"):
        return {"checkbox": value == "__YES__"}
    return {"rich_text": [{"type": "text", "text": {"content": str(value)}}]}


def build_properties(flat: dict) -> dict:
    out: dict = {}
    dates: dict[str, dict] = {}
    for k, v in flat.items():
        if k.startswith("date:"):
            parts = k.split(":")
            if len(parts) >= 3:
                prop = parts[1]
                field = parts[2]
                dates.setdefault(prop, {})[field] = v
            continue
        converted = sqlite_prop(k, v)
        if converted:
            out[k] = converted
    for prop, parts in dates.items():
        start = parts.get("start")
        if not start:
            continue
        is_dt = int(parts.get("is_datetime", 0)) == 1
        out[prop] = {"date": {"start": start, "time_zone": None if not is_dt else "Asia/Shanghai"}}
    return out


def md_to_blocks(text: str) -> list[dict]:
    # Notion API: chunk markdown as paragraph blocks (MCP handles rich md server-side)
    blocks = []
    chunk = text[:1800]
    while chunk:
        blocks.append(
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {"rich_text": [{"type": "text", "text": {"content": chunk}}]},
            }
        )
        text = text[1800:]
        chunk = text[:1800]
    return blocks or [
        {
            "object": "block",
            "type": "paragraph",
            "paragraph": {"rich_text": [{"type": "text", "text": {"content": ""}}]},
        }
    ]


def create_page(data_source_id: str, page: dict) -> dict:
    body = {
        "parent": {"type": "data_source_id", "data_source_id": data_source_id},
        "properties": build_properties(page["properties"]),
        "children": md_to_blocks(page.get("content", "")),
    }
    req = urllib.request.Request(
        "https://api.notion.com/v1/pages",
        data=json.dumps(body).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {token()}",
            "Notion-Version": NOTION_VERSION,
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        err = e.read().decode()
        raise RuntimeError(f"Notion API {e.code}: {err}") from e


def record(rel_paths: list[str]) -> None:
    with PROGRESS.open("a", encoding="utf-8") as f:
        for rel in rel_paths:
            f.write(json.dumps({"rel_path": rel, "status": "synced"}, ensure_ascii=False) + "\n")


def push_file(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    ds = data["mcp"]["parent"]["data_source_id"]
    for page in data["mcp"]["pages"]:
        create_page(ds, page)
    record(data["rel_paths"])
    return {"batch": data["batch"], "index": data["index"], "count": data["count"], "rel_paths": data["rel_paths"]}


def main() -> None:
    if not TOKEN_PATH.exists():
        print("missing Notion token", file=sys.stderr)
        sys.exit(1)
    files = sorted(p for p in BATCH_DIR.glob("*.json") if p.name != "manifest.json")
    results = []
    for path in files:
        try:
            results.append(push_file(path))
            print(json.dumps(results[-1], ensure_ascii=False))
        except Exception as e:
            print(json.dumps({"file": path.name, "error": str(e)}, ensure_ascii=False), file=sys.stderr)
            sys.exit(1)
    summary = {}
    for r in results:
        b = r["batch"]
        summary[b] = summary.get(b, 0) + r["count"]
    print(json.dumps({"summary": summary, "total": sum(summary.values())}, ensure_ascii=False))


if __name__ == "__main__":
    main()
