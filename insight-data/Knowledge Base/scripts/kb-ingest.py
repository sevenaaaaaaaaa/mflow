#!/usr/bin/env python3
"""
kb-ingest.py — KB ingest runner (v0.2).

Reads:
  insight-data/Knowledge Base/Changelog/URL-LIST.md
  insight-data/Knowledge Base/Reference/URL-LIST.md

For each URL not yet ingested (cache at Changelog/.ingested.json):
  - download via curl
  - convert HTML → markdown (markdownify/ html2text)
  - save into Changelog/ or Reference/ as a single .md
  - record to .ingested.json
After ingest:
  - run kb-frontmatter.py + build-index.py --write

DOCX ingest is OUT-OF-BAND: build a sibling env outside the vault
(see html_to_md docstring for rebuild instructions).

This is v0.2: actual fetching disabled by default. To enable:
  python3 kb-ingest.py --allow-fetch

Boundary:
  - harvest ratio cap (don't hammer lovart.ai)
  - per-run max N new files (default 10)
  - on failure: log + skip; do not abort

2026-07-05: removed `.venv` documentation; cleaned from KB root.
"""

import argparse
import datetime
import json
import re
import subprocess
import sys
from pathlib import Path


URL_LIST_FILES = [
    "insight-data/Knowledge Base/Changelog/URL-LIST.md",
    "insight-data/Knowledge Base/Reference/URL-LIST.md",
]

EXCLUDE_RE = re.compile(r"^\s*(#|>|\\$|```)")


def harvest_urls(list_path):
    if not list_path.exists():
        return []
    urls = []
    in_code = False
    for line in list_path.read_text("utf-8").splitlines():
        if line.strip().startswith("```"):
            in_code = not in_code
            continue
        if in_code:
            continue
        if EXCLUDE_RE.match(line):
            continue
        m = re.search(r"https?://\S+", line)
        if m:
            urls.append(m.group(0).rstrip("/.,)"))
    return urls


def load_index(p):
    p.parent.mkdir(parents=True, exist_ok=True)
    if not p.exists():
        return {}
    try:
        return json.loads(p.read_text("utf-8"))
    except Exception:
        return {}


def detect_target_dir(url, root):
    if "changelog" in url or "news" in url or "release" in url:
        return root / "insight-data" / "Knowledge Base" / "Changelog"
    return root / "insight-data" / "Knowledge Base" / "Reference"


def http_fetch(url):
    """Wrap curl. Returns (status, body). Caller catches urllib as fallback."""
    try:
        out = subprocess.run(
            ["curl", "-fsSL", "--max-time", "30", "-A", "lovart-kb-ingest/0.1", url],
            capture_output=True, text=True, timeout=35
        )
        if out.returncode == 0:
            return 200, out.stdout
        return out.returncode, out.stderr
    except Exception as e:
        return None, str(e)


def html_to_md(html_text):
    """Convert HTML to markdown.

    Backend priority:
      1. markdownify (Python 9.x+, pure python, dec=100k)
      2. html2text (Python long-lived, dep-light)
      3. raw HTML fallback (last resort)

    DOCX path is NOT in this script. To ingest .docx files, build a
    sibling env OUTSIDE the vault and use mammoth:

        # one-time, outside vault:
        uv venv ~/Documents/Lovart\ Local\ Dev/lovart-kb-venv
        source ~/Documents/Lovart\ Local\ Dev/lovart-kb-venv/bin/activate
        uv pip install mammoth python-docx

        # then call directly from kb-ingest flow:
        mammoth input.docx --output-format=markdown > output.md

    Don't put the venv inside the vault. It bloats vault backups
    (~22 MB of arm64 lxml binaries). 2026-07-05 cleanup removed
    the legacy insight-data/Knowledge Base/.venv that contained
    mammoth/python-docx/lxml/cobble.
    """
    try:
        from markdownify import markdownify as md
        return md(html_text, heading_style="ATX", strip=["script", "style"])
    except ImportError:
        pass
    try:
        import html2text
        return html2text.html2text(html_text)
    except ImportError:
        return html_text


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--root", default=".")
    p.add_argument("--allow-fetch", action="store_true",
                   help="actually HTTP-fetch (default v0.1: dry-run only)")
    p.add_argument("--max-per-run", type=int, default=10)
    args = p.parse_args()

    root = Path(args.root).expanduser().resolve()
    cache_path = root / "insight-data" / "Knowledge Base" / "Changelog" / ".ingested.json"
    state = load_index(cache_path)

    all_urls = []
    for rel in URL_LIST_FILES:
        p = root / rel
        urls = harvest_urls(p)
        print(f"harvested {len(urls)} from {rel}")
        all_urls.extend(urls)

    new_urls = [u for u in all_urls if u not in state]
    print(f"already-ingested: {len(all_urls) - len(new_urls)}")
    print(f"new this run: {len(new_urls)} (cap {args.max_per_run})")

    new_urls = new_urls[:args.max_per_run]

    if not args.allow_fetch:
        print("\nDRY RUN: pass --allow-fetch to enable HTTP. Skipping.")
        return

    today = datetime.date.today().isoformat()
    saved = []
    for url in new_urls:
        target_dir = detect_target_dir(url, root)
        target_dir.mkdir(parents=True, exist_ok=True)
        status, body = http_fetch(url)
        if status != 200:
            print(f"  ⚠ {url}: {status} {body[:120] if isinstance(body, str) else 'n/a'}")
            state[url] = {"status": "failed", "ts": today}
            continue
        md_text = html_to_md(body)
        slug = re.sub(r"[^a-zA-Z0-9]+", "-", url.split("//", 1)[-1].lower())[:60].strip("-")
        fname = f"{slug}.md"
        path = target_dir / fname
        if path.exists():
            print(f"  → already saved at {path}")
            state[url] = {"status": "saved", "path": str(path.relative_to(root)), "ts": today}
            continue
        path.write_text(
            f"<!-- generated by kb-ingest.py from {url} at {today} -->\n\n" + md_text,
            encoding="utf-8"
        )
        state[url] = {"status": "saved", "path": str(path.relative_to(root)), "ts": today}
        saved.append(path)
        print(f"  ✓ {url} → {path.relative_to(root)}")

    cache_path.write_text(json.dumps(state, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\nsaved {len(saved)} new files. run kb-frontmatter.py + build-index.py next.")


if __name__ == "__main__":
    main()
