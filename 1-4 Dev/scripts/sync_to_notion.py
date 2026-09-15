#!/usr/bin/env python3
"""
sync-to-notion.py — push Obsidian content to Notion databases.

Direction: Obsidian → Notion (推)
Trigger: weekly cron / manual / after publish
Logic:
  1. Scan Obsidian for changed .md files (by mtime)
  2. Match against Notion records by File Path
  3. New → create in Notion
  4. Existing + Obsidian newer → update (skip Status/Comment fields)
  5. Log to sync-pushed.jsonl

Usage:
  python3 sync-to-notion.py                    # dry-run
  python3 sync-to-notion.py --apply            # actually push
  python3 sync-to-notion.py --database content-calendar  # specific database
"""

from __future__ import annotations

import argparse
import json
import os
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

# Database ID mapping (from lovart-notion-config.md)
DATABASES = {
    "content-calendar": {
        "id": "37afc0c7-1bd5-8124-a031-ca4eca128da2",
        "source_dir": MFLOW / "1-3 GenFlow" / "Content Calendar",
        "file_pattern": "*.md",
        "name_field": "title",
        "path_field": "Content Path",
        "status_field": "Status",
        "synced_field": "Last Synced",
        "source_field": "Sync Source",
    },
    "seo-reports": {
        "id": None,  # TBD: create in Notion first
        "source_dir": MFLOW / "1-2 Insight" / "SEO Reports",
        "file_pattern": "*.md",
        "name_field": "title",
        "path_field": "File Path",
        "status_field": "Status",
        "synced_field": "Last Synced",
        "source_field": "Sync Source",
    },
    "sentinel-orm": {
        "id": None,  # TBD
        "source_dir": MFLOW / "1-2 Insight" / "Lovart ORM",
        "file_pattern": "*.md",
        "name_field": "title",
        "path_field": "File Path",
        "status_field": "Alert Level",
        "synced_field": "Last Synced",
        "source_field": "Sync Source",
    },
    "okr": {
        "id": None,  # TBD
        "source_dir": MFLOW / "1-1 Harness" / "07-okr",
        "file_pattern": "*.md",
        "name_field": "title",
        "path_field": "File Path",
        "status_field": "Status",
        "synced_field": "Last Synced",
        "source_field": "Sync Source",
    },
}

# Fields to NEVER overwrite from Obsidian (Notion is SSOT for these)
NOTION_OWNED_FIELDS = {"Status", "Comment", "Notes", "Conflict Flag"}

SYNC_LOG = MFLOW / "1-4 Dev" / "scripts" / "sync-pushed.jsonl"


def notion_headers():
    return {
        "Authorization": f"Bearer {NOTION_API_KEY}",
        "Notion-Version": NOTION_VERSION,
        "Content-Type": "application/json",
    }


def query_notion_database(db_id: str) -> list[dict]:
    """Query all pages in a Notion database."""
    pages = []
    has_more = True
    start_cursor = None
    while has_more:
        body = {"page_size": 100}
        if start_cursor:
            body["start_cursor"] = start_cursor
        resp = requests.post(
            f"{NOTION_BASE}/databases/{db_id}/query",
            headers=notion_headers(),
            json=body,
            timeout=30,
        )
        if resp.status_code != 200:
            print(f"  [err] query failed: {resp.status_code} {resp.text[:200]}")
            break
        data = resp.json()
        pages.extend(data.get("results", []))
        has_more = data.get("has_more", False)
        start_cursor = data.get("next_cursor")
        time.sleep(0.35)  # rate limit
    return pages


def create_notion_page(db_id: str, properties: dict) -> dict | None:
    """Create a new page in a Notion database."""
    resp = requests.post(
        f"{NOTION_BASE}/pages",
        headers=notion_headers(),
        json={"parent": {"database_id": db_id}, "properties": properties},
        timeout=30,
    )
    if resp.status_code == 200:
        return resp.json()
    print(f"  [err] create failed: {resp.status_code} {resp.text[:200]}")
    return None


def update_notion_page(page_id: str, properties: dict) -> bool:
    """Update an existing Notion page."""
    resp = requests.patch(
        f"{NOTION_BASE}/pages/{page_id}",
        headers=notion_headers(),
        json={"properties": properties},
        timeout=30,
    )
    return resp.status_code == 200


def extract_title_from_md(path: Path) -> str:
    """Extract title from frontmatter or first heading."""
    try:
        content = path.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return path.stem
    # Try frontmatter title
    for line in content.split("\n")[:20]:
        if line.strip().startswith("title:"):
            val = line.split(":", 1)[1].strip().strip('"').strip("'")
            if val:
                return val
    # Try first heading
    for line in content.split("\n")[:30]:
        if line.strip().startswith("# "):
            return line.strip()[2:].strip()
    return path.stem


def md_mtime_iso(path: Path) -> str:
    """Get file mtime as ISO string."""
    mt = path.stat().st_mtime
    return datetime.fromtimestamp(mt, tz=timezone.utc).isoformat()


def log_push(event: dict):
    """Append to sync log."""
    SYNC_LOG.parent.mkdir(parents=True, exist_ok=True)
    with SYNC_LOG.open("a", encoding="utf-8") as f:
        f.write(json.dumps(event, ensure_ascii=False) + "\n")


def sync_database(db_name: str, config: dict, apply: bool) -> tuple[int, int]:
    """Sync one database. Returns (created, updated)."""
    db_id = config.get("id")
    if not db_id:
        print(f"  [skip] {db_name}: no Database ID configured")
        return 0, 0

    source_dir = config["source_dir"]
    if not source_dir.exists():
        print(f"  [skip] {db_name}: source dir not found: {source_dir}")
        return 0, 0

    print(f"\n--- {db_name} ---")
    print(f"  source: {source_dir}")

    # 1. Collect local files
    local_files = sorted(source_dir.glob(config["file_pattern"]))
    print(f"  local files: {len(local_files)}")

    # 2. Query Notion
    notion_pages = query_notion_database(db_id)
    print(f"  notion pages: {len(notion_pages)}")

    # 3. Build lookup: file_path → notion_page
    path_to_page = {}
    for page in notion_pages:
        props = page.get("properties", {})
        # Get file path from the configured field
        path_prop = props.get(config["path_field"], {})
        if path_prop.get("type") == "rich_text":
            rt = path_prop.get("rich_text", [])
            if rt:
                file_path = rt[0].get("plain_text", "")
                if file_path:
                    path_to_page[file_path] = page

    # 4. Sync
    created = 0
    updated = 0
    now_iso = datetime.now(timezone.utc).isoformat()

    for f in local_files:
        rel_path = str(f.relative_to(MFLOW))

        if rel_path in path_to_page:
            # Already exists — check if Obsidian is newer
            page = path_to_page[rel_path]
            page_id = page["id"]

            # Check Last Synced
            synced_prop = page.get("properties", {}).get(config["synced_field"], {})
            last_synced = None
            if synced_prop.get("type") == "date" and synced_prop.get("date"):
                last_synced = synced_prop["date"].get("start")

            file_mtime = md_mtime_iso(f)

            if last_synced and file_mtime <= last_synced:
                continue  # Notion is up to date

            # Update: only non-Notion-owned fields
            title = extract_title_from_md(f)
            update_props = {
                config["name_field"]: {"title": [{"text": {"content": title}}]},
                config["path_field"]: {"rich_text": [{"text": {"content": rel_path}}]},
                config["synced_field"]: {"date": {"start": now_iso}},
                config["source_field"]: {"select": {"name": "obsidian"}},
            }

            if apply:
                ok = update_notion_page(page_id, update_props)
                if ok:
                    updated += 1
                    log_push({"ts": now_iso, "db": db_name, "action": "update",
                              "path": rel_path, "page_id": page_id})
                time.sleep(0.35)
            else:
                print(f"  would update: {rel_path}")
                updated += 1
        else:
            # New file — create
            title = extract_title_from_md(f)
            create_props = {
                config["name_field"]: {"title": [{"text": {"content": title}}]},
                config["path_field"]: {"rich_text": [{"text": {"content": rel_path}}]},
                config["synced_field"]: {"date": {"start": now_iso}},
                config["source_field"]: {"select": {"name": "obsidian"}},
            }

            if apply:
                result = create_notion_page(db_id, create_props)
                if result:
                    created += 1
                    log_push({"ts": now_iso, "db": db_name, "action": "create",
                              "path": rel_path, "page_id": result["id"]})
                time.sleep(0.35)
            else:
                print(f"  would create: {rel_path}")
                created += 1

    print(f"  result: +{created} created, ~{updated} updated")
    return created, updated


def main():
    parser = argparse.ArgumentParser(description="Push Obsidian → Notion")
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--database", help="sync only this database")
    args = parser.parse_args()

    if not NOTION_API_KEY:
        print("[err] No Notion API key found. Set NOTION_API_KEY or create ~/.config/notion/api_key")
        sys.exit(2)

    print(f"=== Obsidian → Notion sync ===")
    print(f"Mode: {'APPLY' if args.apply else 'DRY-RUN'}")
    print(f"Vault: {MFLOW}")

    total_created = 0
    total_updated = 0

    for name, config in DATABASES.items():
        if args.database and args.database != name:
            continue
        c, u = sync_database(name, config, args.apply)
        total_created += c
        total_updated += u

    print(f"\n=== Total: +{total_created} created, ~{total_updated} updated ===")


if __name__ == "__main__":
    main()
