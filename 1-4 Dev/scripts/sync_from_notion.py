#!/usr/bin/env python3
"""
sync-from-notion.py — pull Notion status changes back to Obsidian.

Direction: Notion → Obsidian (拉)
Trigger: weekly cron / manual
Logic:
  1. Query Notion databases for records with recent Status/Comment changes
  2. Find corresponding Obsidian .md files by File Path
  3. Patch frontmatter with Notion-owned fields (Status, Priority, etc.)
  4. Log to sync-pulled.jsonl

Usage:
  python3 sync-from-notion.py                    # dry-run
  python3 sync-from-notion.py --apply            # actually pull
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import requests

# --- Config ---
NOTION_API_KEY = ""
for p in [Path.home() / ".config" / "notion" / "api_key",
          Path.home() / ".config" / "notion" / "token"]:
    if p.exists():
        NOTION_API_KEY = p.read_text().strip()
        break
if not NOTION_API_KEY:
    NOTION_API_KEY = os.environ.get("NOTION_API_KEY", "")

NOTION_VERSION = "2022-06-28"
NOTION_BASE = "https://api.notion.com/v1"

VAULT = Path(os.environ.get("LOVART_RESOURCE_ROOT",
              Path(__file__).resolve().parents[4]))
MFLOW = VAULT / "1-Project" / "Lovart MFlow"

DATABASES = {
    "content-calendar": {
        "id": "37afc0c7-1bd5-8124-a031-ca4eca128da2",
        "path_field": "Content Path",
        "synced_field": "Last Synced",
        "pull_fields": {
            "Status": "status",
            "Priority": "priority",
            "Score": "score",
            "Notes": "notes",
        },
    },
}

SYNC_LOG = MFLOW / "1-4 Dev" / "scripts" / "sync-pulled.jsonl"


def notion_headers():
    return {
        "Authorization": f"Bearer {NOTION_API_KEY}",
        "Notion-Version": NOTION_VERSION,
        "Content-Type": "application/json",
    }


def query_notion_database(db_id: str, since: str | None = None) -> list[dict]:
    pages = []
    has_more = True
    start_cursor = None
    while has_more:
        body = {"page_size": 100}
        if start_cursor:
            body["start_cursor"] = start_cursor
        if since:
            body["filter"] = {
                "property": "Last Synced",
                "date": {"after": since},
            }
        resp = requests.post(
            f"{NOTION_BASE}/databases/{db_id}/query",
            headers=notion_headers(),
            json=body,
            timeout=30,
        )
        if resp.status_code != 200:
            print(f"  [err] query failed: {resp.status_code}")
            break
        data = resp.json()
        pages.extend(data.get("results", []))
        has_more = data.get("has_more", False)
        start_cursor = data.get("next_cursor")
        time.sleep(0.35)
    return pages


def extract_prop_value(prop: dict) -> str | int | float | None:
    """Extract a plain value from a Notion property."""
    t = prop.get("type", "")
    if t == "title":
        texts = prop.get("title", [])
        return texts[0].get("plain_text", "") if texts else None
    elif t == "rich_text":
        texts = prop.get("rich_text", [])
        return texts[0].get("plain_text", "") if texts else None
    elif t == "select":
        sel = prop.get("select")
        return sel.get("name") if sel else None
    elif t == "number":
        return prop.get("number")
    elif t == "checkbox":
        return prop.get("checkbox")
    elif t == "date":
        d = prop.get("date")
        return d.get("start") if d else None
    return None


def patch_frontmatter(md_path: Path, updates: dict[str, str | int | float | None]) -> bool:
    """Patch specific fields in a .md file's frontmatter."""
    if not md_path.exists():
        return False

    content = md_path.read_text(encoding="utf-8")
    lines = content.split("\n")

    # Find frontmatter boundaries
    if not lines or lines[0].strip() != "---":
        return False

    end_idx = None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            end_idx = i
            break
    if end_idx is None:
        return False

    fm_lines = lines[1:end_idx]
    new_fm = []
    updated_keys = set()

    for line in fm_lines:
        matched = False
        for key, val in updates.items():
            if line.strip().startswith(f"{key}:"):
                if val is None:
                    new_fm.append(f"{key}: null")
                elif isinstance(val, (int, float)):
                    new_fm.append(f"{key}: {val}")
                else:
                    new_fm.append(f'{key}: "{val}"')
                updated_keys.add(key)
                matched = True
                break
        if not matched:
            new_fm.append(line)

    # Add missing keys
    for key, val in updates.items():
        if key not in updated_keys:
            if val is None:
                new_fm.append(f"{key}: null")
            elif isinstance(val, (int, float)):
                new_fm.append(f"{key}: {val}")
            else:
                new_fm.append(f'{key}: "{val}"')

    new_content = "\n".join(lines[:1] + new_fm + lines[end_idx:])
    md_path.write_text(new_content, encoding="utf-8")
    return True


def sync_database(db_name: str, config: dict, apply: bool) -> int:
    db_id = config.get("id")
    if not db_id:
        print(f"  [skip] {db_name}: no Database ID")
        return 0

    print(f"\n--- {db_name} ---")

    # Query Notion for recently updated records
    notion_pages = query_notion_database(db_id)
    print(f"  notion pages: {len(notion_pages)}")

    pulled = 0
    now_iso = datetime.now(timezone.utc).isoformat()

    for page in notion_pages:
        props = page.get("properties", {})

        # Get file path
        path_val = extract_prop_value(props.get(config["path_field"], {}))
        if not path_val:
            continue

        md_path = MFLOW / path_val
        if not md_path.exists():
            continue

        # Extract Notion-owned fields
        updates = {}
        for notion_field, md_key in config["pull_fields"].items():
            val = extract_prop_value(props.get(notion_field, {}))
            if val is not None:
                updates[md_key] = val

        if not updates:
            continue

        if apply:
            ok = patch_frontmatter(md_path, updates)
            if ok:
                pulled += 1
                log_event({"ts": now_iso, "db": db_name, "action": "pull",
                           "path": path_val, "fields": list(updates.keys())})
        else:
            print(f"  would pull: {path_val} ({list(updates.keys())})")
            pulled += 1

    print(f"  pulled: {pulled}")
    return pulled


def log_event(event: dict):
    SYNC_LOG.parent.mkdir(parents=True, exist_ok=True)
    with SYNC_LOG.open("a", encoding="utf-8") as f:
        f.write(json.dumps(event, ensure_ascii=False) + "\n")


def main():
    parser = argparse.ArgumentParser(description="Pull Notion → Obsidian")
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()

    if not NOTION_API_KEY:
        print("[err] No Notion API key found")
        sys.exit(2)

    print(f"=== Notion → Obsidian sync ===")
    print(f"Mode: {'APPLY' if args.apply else 'DRY-RUN'}")

    total = 0
    for name, config in DATABASES.items():
        total += sync_database(name, config, args.apply)

    print(f"\n=== Total: {total} records to pull ===")


if __name__ == "__main__":
    main()
