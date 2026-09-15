#!/usr/bin/env python3
"""
Publish Markdown drafts to blogs.lovart.ai via WordPress REST API (cookie auth).

Auth: set WP_USER / WP_PASS env vars, or copy wp-auth.local.env.example → wp-auth.local.env
      (wp-auth.local.env is gitignored — never commit credentials).

Usage:
  python3 scripts/publish-to-wp.py --dry-run --file comparison-flora-ai-vs-lovart.md
  python3 scripts/publish-to-wp.py --file comparison-flora-ai-vs-lovart.md
  python3 scripts/publish-to-wp.py --limit 5
"""

from __future__ import annotations

import argparse
import http.cookiejar
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

try:
    import yaml
except ImportError:
    print("❌ PyYAML required: pip install pyyaml")
    sys.exit(1)

ROOT = Path(__file__).resolve().parent.parent
DRAFTS_DIR = ROOT / "01-Drafts"
PUBLISHED_DIR = ROOT / "03-Published"
API_BASE = "https://blogs.lovart.ai/wp-json/wp/v2"
AUTH_ENV_FILE = Path(__file__).resolve().parent / "wp-auth.local.env"

COOKIE_JAR = None
OPENER = None
WP_NONCE = None


def load_auth() -> tuple[str, str]:
    user = os.environ.get("WP_USER", "").strip()
    password = os.environ.get("WP_PASS", "").strip()
    if AUTH_ENV_FILE.is_file():
        for line in AUTH_ENV_FILE.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            if key == "WP_USER" and not user:
                user = value
            elif key == "WP_PASS" and not password:
                password = value
    if not user or not password:
        print(
            "❌ Missing WP credentials. Set WP_USER/WP_PASS or create "
            f"{AUTH_ENV_FILE.name} from wp-auth.local.env.example"
        )
        sys.exit(1)
    return user, password


def init_auth() -> None:
    global COOKIE_JAR, OPENER, WP_NONCE
    wp_user, wp_pass = load_auth()
    COOKIE_JAR = http.cookiejar.CookieJar()
    OPENER = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(COOKIE_JAR))

    print("🔑 Logging in...")
    login_data = urllib.parse.urlencode(
        {
            "log": wp_user,
            "pwd": wp_pass,
            "wp-submit": "Log In",
            "redirect_to": "/wp-admin/",
            "testcookie": "1",
        }
    ).encode()
    OPENER.open(
        urllib.request.Request("https://blogs.lovart.ai/wp-login.php", data=login_data)
    )
    if "wordpress_logged_in" not in str(COOKIE_JAR):
        print("❌ Login failed — check WP_USER / WP_PASS")
        sys.exit(1)

    admin_body = OPENER.open(
        urllib.request.Request("https://blogs.lovart.ai/wp-admin/")
    ).read().decode()
    match = re.search(r'var wpApiSettings\s*=\s*\{[^}]*"nonce":"([a-f0-9]+)"', admin_body)
    if not match:
        match = re.search(r'"nonce":"([a-f0-9]+)"', admin_body)
    if not match:
        print("❌ Could not find WP REST nonce")
        sys.exit(1)
    WP_NONCE = match.group(1)
    print(f"✅ Logged in as {wp_user}")


def wp_request(method: str, endpoint: str, data: dict | None = None):
    url = f"{API_BASE}/{endpoint}"
    body = json.dumps(data).encode() if data else None
    req = urllib.request.Request(url, data=body, method=method)
    req.add_header("X-WP-Nonce", WP_NONCE)
    req.add_header("Content-Type", "application/json")
    req.add_header("User-Agent", "Lovart-Blog-Publisher/1.0")
    try:
        resp = OPENER.open(req)
        return json.loads(resp.read())
    except urllib.error.HTTPError as exc:
        err = exc.read().decode()
        print(f"  ❌ HTTP {exc.code}: {err[:300]}")
        return None


CATEGORY_CACHE: dict[str, int] = {}
TAG_CACHE: dict[str, int] = {}


def find_or_create_category(name: str, slug: str) -> int:
    if slug in CATEGORY_CACHE:
        return CATEGORY_CACHE[slug]
    cats = wp_request("GET", f"categories?slug={slug}")
    if cats:
        CATEGORY_CACHE[slug] = cats[0]["id"]
        return cats[0]["id"]
    created = wp_request("POST", "categories", {"name": name, "slug": slug})
    if created:
        CATEGORY_CACHE[slug] = created["id"]
        return created["id"]
    return 144


def find_or_create_tag(name: str) -> int | None:
    slug = name.lower().replace(" ", "-").replace("–", "-").strip("-")
    if slug in TAG_CACHE:
        return TAG_CACHE[slug]
    existing = wp_request("GET", f"tags?slug={slug}")
    if existing:
        TAG_CACHE[slug] = existing[0]["id"]
        return existing[0]["id"]
    created = wp_request("POST", "tags", {"name": name, "slug": slug})
    if created:
        TAG_CACHE[slug] = created["id"]
        return created["id"]
    return None


def md_to_html(md_text: str) -> str:
    try:
        import markdown

        return markdown.markdown(md_text, extensions=["extra", "tables"])
    except ImportError:
        pass
    html: list[str] = []
    in_code = False
    for line in md_text.split("\n"):
        if "[IMAGE" in line and "PLACEHOLDER" in line:
            html.append(f"<!-- {line.strip()} -->")
            continue
        if line.startswith("```"):
            in_code = not in_code
            html.append("</pre>" if in_code else "<pre><code>")
            continue
        if in_code:
            html.append(line)
            continue
        if line.startswith("### "):
            html.append(f"<h3>{line[4:]}</h3>")
        elif line.startswith("## "):
            html.append(f"<h2>{line[3:]}</h2>")
        elif line.startswith("# "):
            html.append(f"<h1>{line[2:]}</h1>")
        elif line.startswith("- "):
            html.append(f"<li>{line[2:]}</li>")
        elif line.startswith("> "):
            html.append(f"<blockquote>{line[2:]}</blockquote>")
        elif line.strip() == "---":
            html.append("<hr>")
        elif line.strip():
            line = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", line)
            html.append(f"<p>{line}</p>")
        else:
            html.append("<br>")
    return "\n".join(html)


def parse_frontmatter(filepath: Path) -> tuple[dict, str]:
    content = filepath.read_text(encoding="utf-8")
    if not content.startswith("---"):
        return {}, content
    parts = content.split("---", 2)
    if len(parts) < 3:
        return {}, content
    try:
        frontmatter = yaml.safe_load(parts[1]) or {}
    except yaml.YAMLError:
        frontmatter = {}
    return frontmatter, parts[2].strip()


def publish_post(filepath: Path):
    frontmatter, body = parse_frontmatter(filepath)
    title = frontmatter.get("title", filepath.stem)
    slug = frontmatter.get("slug", "")
    excerpt = frontmatter.get(
        "description",
        frontmatter.get("meta_description", frontmatter.get("excerpt", "")),
    )
    if isinstance(excerpt, dict):
        excerpt = ""
    category_name = frontmatter.get("category", "Blog")
    tags_list = frontmatter.get("tags", [])
    if isinstance(tags_list, str):
        tags_list = [t.strip() for t in tags_list.split(",")]

    html_content = md_to_html(body)
    cat_slug = category_name.lower().replace(" ", "-").replace("–", "-")
    cat_id = find_or_create_category(category_name, cat_slug)
    tag_ids = []
    for tag in tags_list:
        tag_id = find_or_create_tag(str(tag).strip())
        if tag_id:
            tag_ids.append(tag_id)

    post_data = {
        "title": title,
        "content": html_content,
        "status": "publish",
        "categories": [cat_id],
        "tags": tag_ids,
    }
    if excerpt:
        post_data["excerpt"] = excerpt
    if slug:
        post_data["slug"] = slug
    return wp_request("POST", "posts", post_data)


def move_to_published(filepath: Path, post_id: int) -> None:
    PUBLISHED_DIR.mkdir(parents=True, exist_ok=True)
    dest = PUBLISHED_DIR / filepath.name
    content = filepath.read_text(encoding="utf-8")
    if content.startswith("---"):
        insert = f"\nwp_post_id: {post_id}\npublish_date: '{time.strftime('%Y-%m-%d')}'\n"
        parts = content.split("---", 2)
        if len(parts) >= 3:
            content = f"---{parts[1]}{insert}---{parts[2]}"
    dest.write_text(content, encoding="utf-8")
    filepath.unlink()
    print("  📁 Moved → 03-Published/")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=0)
    parser.add_argument("--file", type=str)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    if args.file:
        files = [DRAFTS_DIR / args.file]
    else:
        files = sorted(
            p for p in DRAFTS_DIR.glob("*.md") if not p.name.startswith("_")
        )

    if args.limit > 0:
        files = files[: args.limit]

    if not files:
        print("No drafts found.")
        return

    if not args.dry_run:
        init_auth()

    print(f"\n📦 Publishing {len(files)} posts...")
    if args.dry_run:
        print("🔍 DRY RUN\n")

    success = fail = 0
    for index, filepath in enumerate(files, 1):
        print(f"[{index}/{len(files)}] {filepath.name}")
        if not filepath.is_file():
            print("  ❌ File not found")
            fail += 1
            continue
        if args.dry_run:
            fm, _ = parse_frontmatter(filepath)
            print(f"  → {(fm.get('title') or filepath.stem)[:80]}")
            print(f"  → Category: {fm.get('category', 'N/A')}")
            continue
        result = publish_post(filepath)
        if result and "id" in result:
            post_id = result["id"]
            post_url = result.get("link", f"https://blogs.lovart.ai/?p={post_id}")
            print(f"  ✅ #{post_id}: {post_url}")
            success += 1
            move_to_published(filepath, post_id)
        else:
            print("  ❌ Failed")
            fail += 1
        time.sleep(0.8)

    print(f"\n🎉 Done! {success} published, {fail} failed")


if __name__ == "__main__":
    main()
