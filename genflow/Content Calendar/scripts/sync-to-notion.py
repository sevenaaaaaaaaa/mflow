#!/usr/bin/env python3
"""
Sync Content Calendar to Notion.

Reads the priority queue JSON (from build-content-calendar-priority.js)
and pushes each item as a Notion database row.

Usage:
  python3 sync-to-notion.py                          # sync from default JSON
  python3 sync-to-notion.py --json path/to/file.json  # custom JSON
  python3 sync-to-notion.py --dry-run                 # preview only
  python3 sync-to-notion.py --limit 10                # first 10 items only
"""
import json, urllib.request, os, sys, time, argparse

# ── Config ──────────────────────────────────────────────────────
NOTION_KEY = os.environ.get(
    "NOTION_API_KEY",
    "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"
)
DB_ID = "37afc0c7-1bd5-8124-a031-ca4eca128da2"
API_VERSION = "2022-06-28"
DEFAULT_JSON = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "content-calendar-priority-queue-2026-06.json"
)

# ── Notion API helpers ──────────────────────────────────────────
def notion_request(method, endpoint, body=None):
    """Make a Notion API request and return parsed JSON."""
    url = f"https://api.notion.com{endpoint}"
    headers = {
        "Authorization": f"Bearer {NOTION_KEY}",
        "Notion-Version": API_VERSION,
        "Content-Type": "application/json",
    }
    data = json.dumps(body).encode() if body else None
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        body_text = e.read().decode()
        return {"error": True, "status": e.code, "message": body_text[:300]}


def query_database(start_cursor=None):
    """Query all pages in the database (paginated)."""
    body = {"page_size": 100}
    if start_cursor:
        body["start_cursor"] = start_cursor
    return notion_request("POST", f"/v1/databases/{DB_ID}/query", body)


def get_existing_pages():
    """Fetch all existing pages and index by slug for dedup."""
    pages = {}
    cursor = None
    while True:
        result = query_database(cursor)
        if "error" in result:
            print(f"  ❌ Query error: {result.get('message', '')}")
            break
        for page in result.get("results", []):
            props = page.get("properties", {})
            slug_prop = props.get("Slug", {}).get("rich_text", [])
            if slug_prop:
                slug = slug_prop[0].get("plain_text", "")
                pages[slug] = page["id"]
        if result.get("has_more") and result.get("next_cursor"):
            cursor = result["next_cursor"]
        else:
            break
    return pages


def create_page(properties):
    """Create a new page in the database."""
    return notion_request("POST", "/v1/pages", {
        "parent": {"database_id": DB_ID},
        "properties": properties,
    })


def update_page(page_id, properties):
    """Update an existing page."""
    return notion_request("PATCH", f"/v1/pages/{page_id}", {
        "properties": properties,
    })


# ── Property builders ──────────────────────────────────────────
def title(text):
    return {"title": [{"text": {"content": str(text)[:2000]}}]}

def rich_text(text):
    if not text:
        return {"rich_text": []}
    return {"rich_text": [{"text": {"content": str(text)[:2000]}}]}

def select(name):
    if not name or name == "(blank)":
        return {"select": None}
    return {"select": {"name": str(name)}}

def number(val):
    if val is None:
        return {"number": None}
    return {"number": int(val)}

def url(val):
    if not val:
        return {"url": None}
    return {"url": str(val)}

def date_val(val):
    if not val:
        return {"date": None}
    return {"date": {"start": str(val)}}


def row_to_properties(row):
    """Convert a priority queue row to Notion properties."""
    status_map = {
        "": "Backlog",
        "(blank)": "Backlog",
        "draft": "Draft",
        "ready": "Ready",
        "published": "Published",
        "internal": "Internal",
    }
    status = status_map.get(row.get("status", "").lower(), "Backlog")

    # Infer content type from bucket
    bucket = row.get("bucket", "")
    if bucket in ("01-How-To", "02-Comparison", "03-Industry-Segment",
                   "05-Insight-Trend", "08-Best-Practice", "09-Better-Design"):
        content_type = "Blog"
    elif bucket in ("11-Programmatic-SEO",):
        content_type = "Page"
    elif bucket in ("14-Product-Update", "13-Onboarding"):
        content_type = "Page"
    else:
        content_type = "Blog"

    return {
        "Name": title(row.get("slug", "untitled")),
        "Slug": rich_text(row.get("slug", "")),
        "Status": select(status),
        "Priority": select(row.get("priority", "")),
        "Score": number(row.get("score", 0)),
        "Bucket": select(bucket),
        "Language": select(row.get("language", "en")),
        "Canonical Slug": rich_text(row.get("canonical_slug", "")),
        "Cluster Type": select(row.get("cluster_type", "")),
        "Cluster Size": number(row.get("cluster_size", 0)),
        "Target Keywords": rich_text(row.get("target_keywords", "")),
        "Content Path": rich_text(row.get("path", "")),
        "Content Type": select(content_type),
    }


# ── Main ───────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="Sync Content Calendar to Notion")
    parser.add_argument("--json", default=DEFAULT_JSON, help="Path to priority queue JSON")
    parser.add_argument("--dry-run", action="store_true", help="Preview only, no writes")
    parser.add_argument("--limit", type=int, default=0, help="Max items to sync (0=all)")
    args = parser.parse_args()

    # Load data
    if not os.path.exists(args.json):
        print(f"❌ JSON not found: {args.json}")
        print("   Run build-content-calendar-priority.js first.")
        sys.exit(1)

    with open(args.json) as f:
        rows = json.load(f)

    if args.limit > 0:
        rows = rows[:args.limit]

    print(f"📋 Loaded {len(rows)} items from {os.path.basename(args.json)}")

    if args.dry_run:
        print("\n🏃 DRY RUN — preview first 5 items:")
        for row in rows[:5]:
            props = row_to_properties(row)
            print(f"  → {row['slug']} | {row['priority']} | {row['bucket']} | {row['language']}")
        print(f"  ... ({len(rows)} total)")
        return

    # Get existing pages for dedup
    print("🔍 Fetching existing Notion pages for dedup...")
    existing = get_existing_pages()
    print(f"   Found {len(existing)} existing pages")

    # Sync
    created, updated, skipped, errors = 0, 0, 0, 0
    for i, row in enumerate(rows):
        slug = row.get("slug", "")
        props = row_to_properties(row)

        if slug in existing:
            # Update existing
            result = update_page(existing[slug], props)
            if "error" in result:
                print(f"  ❌ [{i+1}] Update failed: {slug} — {result.get('message', '')[:80]}")
                errors += 1
            else:
                updated += 1
        else:
            # Create new
            result = create_page(props)
            if "error" in result:
                print(f"  ❌ [{i+1}] Create failed: {slug} — {result.get('message', '')[:80]}")
                errors += 1
            else:
                created += 1

        # Progress
        if (i + 1) % 50 == 0:
            print(f"  ... {i+1}/{len(rows)} done (created={created} updated={updated} errors={errors})")

        # Rate limit: ~3 req/sec
        time.sleep(0.35)

    print(f"\n✅ Sync complete!")
    print(f"   Created: {created}")
    print(f"   Updated: {updated}")
    print(f"   Skipped: {skipped}")
    print(f"   Errors:  {errors}")
    print(f"   Total:   {len(rows)}")


if __name__ == "__main__":
    main()
