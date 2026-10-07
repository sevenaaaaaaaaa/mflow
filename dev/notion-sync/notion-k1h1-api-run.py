#!/usr/bin/env python3
"""Push pending K1/H1 batches via Notion REST API (MCP notion-create-pages equivalent)."""
from __future__ import annotations

import json
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

SYNC = Path(__file__).parent
BATCH_DIR = Path("/tmp/notion-push-batches")
RECORD = SYNC / "notion-record-push.py"
RUNNER = SYNC / "notion-push-mcp-runner.py"
TOKEN_PATH = Path.home() / ".config/notion/api_key"
NOTION_VERSION = "2022-06-28"
CHUNK = 1800
SLEEP = 0.35


def token() -> str:
    return TOKEN_PATH.read_text(encoding="utf-8").strip()


def api(method: str, path: str, body: dict | None = None) -> dict:
    data = None if body is None else json.dumps(body).encode("utf-8")
    req = urllib.request.Request(
        f"https://api.notion.com/v1{path}",
        data=data,
        method=method,
        headers={
            "Authorization": f"Bearer {token()}",
            "Notion-Version": NOTION_VERSION,
            "Content-Type": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=180) as resp:
            raw = resp.read().decode()
            return json.loads(raw) if raw else {}
    except urllib.error.HTTPError as e:
        detail = e.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Notion {method} {path} -> {e.code}: {detail[:800]}") from e


def rich_text(content: str) -> list[dict]:
    parts: list[dict] = []
    text = content or ""
    while text:
        piece = text[:CHUNK]
        text = text[CHUNK:]
        parts.append({"type": "text", "text": {"content": piece}})
    return parts or []


def build_properties(flat: dict) -> dict:
    out: dict = {}
    dates: dict[str, dict] = {}
    for k, v in flat.items():
        if k.startswith("date:"):
            parts = k.split(":")
            if len(parts) >= 3:
                dates.setdefault(parts[1], {})[parts[2]] = v
            continue
        if v is None:
            continue
        if k == "Name":
            out[k] = {"title": rich_text(str(v))}
        elif k in ("Type", "Status"):
            out[k] = {"select": {"name": str(v)}}
        else:
            out[k] = {"rich_text": rich_text(str(v))}
    for prop, parts in dates.items():
        start = parts.get("start")
        if start:
            out[prop] = {"date": {"start": start}}
    return out


def md_to_blocks(text: str) -> list[dict]:
    blocks: list[dict] = []
    rest = text or ""
    while rest:
        chunk = rest[:CHUNK]
        rest = rest[CHUNK:]
        blocks.append(
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {"rich_text": rich_text(chunk)},
            }
        )
    return blocks or [
        {"object": "block", "type": "paragraph", "paragraph": {"rich_text": []}}
    ]


def append_blocks(page_id: str, blocks: list[dict]) -> None:
    for i in range(0, len(blocks), 95):
        api("PATCH", f"/blocks/{page_id}/children", {"children": blocks[i : i + 95]})


def create_page(data_source_id: str, page: dict) -> str:
    content = page.get("content", "")
    all_blocks = md_to_blocks(content)
    body = {
        "parent": {"type": "data_source_id", "data_source_id": data_source_id},
        "properties": build_properties(page["properties"]),
        "children": all_blocks[:95],
    }
    res = api("POST", "/pages", body)
    page_id = res["id"]
    if len(all_blocks) > 95:
        append_blocks(page_id, all_blocks[95:])
    return page_id


def pending_files() -> list[Path]:
    out = subprocess.check_output(
        [sys.executable, str(RUNNER), "status"], text=True, encoding="utf-8"
    )
    # use same logic as runner
    done: set[str] = set()
    progress = SYNC / "sync-pushed.jsonl"
    if progress.exists():
        for line in progress.read_text(encoding="utf-8").splitlines():
            if line.strip():
                done.add(json.loads(line)["rel_path"])
    files: list[Path] = []
    for batch in ("K1", "H1"):
        for path in sorted(BATCH_DIR.glob(f"{batch}-*.json")):
            data = json.loads(path.read_text(encoding="utf-8"))
            rel_paths = data.get("rel_paths") or [
                p["properties"]["Source Path"] for p in data["pages"]
            ]
            if any(r not in done for r in rel_paths):
                files.append(path)
    return files


def push_batch(path: Path, done: set[str]) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    ds = data["parent"]["data_source_id"]
    synced: list[str] = []
    errors: list[dict] = []
    for page in data["pages"]:
        rel = page["properties"]["Source Path"]
        if rel in done:
            continue
        try:
            create_page(ds, page)
            subprocess.run([sys.executable, str(RECORD), rel], check=True)
            done.add(rel)
            synced.append(rel)
            print(f"OK: {rel}", flush=True)
            time.sleep(SLEEP)
        except Exception as e:  # noqa: BLE001
            errors.append({"rel_path": rel, "error": str(e)[:500]})
            print(f"FAIL: {rel} -> {e}", flush=True)
    return {"file": path.name, "synced": synced, "errors": errors}


def main() -> None:
    if not TOKEN_PATH.exists():
        raise SystemExit("missing ~/.config/notion/api_key")
    done: set[str] = set()
    progress = SYNC / "sync-pushed.jsonl"
    if progress.exists():
        for line in progress.read_text(encoding="utf-8").splitlines():
            if line.strip():
                done.add(json.loads(line)["rel_path"])
    failures: list[dict] = []
    pushed = 0
    for path in pending_files():
        result = push_batch(path, done)
        pushed += len(result["synced"])
        failures.extend(result["errors"])
    counts = json.loads(
        subprocess.check_output(
            [sys.executable, str(RUNNER), "status"], text=True, encoding="utf-8"
        )
    )
    print(
        json.dumps(
            {"pushed_this_run": pushed, "counts": counts, "failures": failures},
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
