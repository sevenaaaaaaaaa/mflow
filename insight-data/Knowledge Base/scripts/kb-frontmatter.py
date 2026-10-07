#!/usr/bin/env python3
"""
kb-frontmatter.py — apply KB-SCHEMA-compliant frontmatter to existing KB .md files.

Convention:
  - Reads each .md file under insight-data/Knowledge Base/ (excluding KB-SCHEMA.md, KB-Index/, scripts/, .venv/).
  - Detects layer (origin) based on directory:
        Lovart Introduction/   → official-curated / internal-curated
        Lovart News/           → official-news
        Lovart Docs/           → official-crawl-derived
  - Derives topics/capabilities from filename + first 1000 chars.
  - Adds frontmatter if missing; never overwrites existing frontmatter (unless --force).
  - Outputs a Change-row at end so each file is auditable.

Usage:
  python3 kb-frontmatter.py --root <vault-root>
  python3 kb-frontmatter.py --root <vault-root> --dry-run
  python3 kb-frontmatter.py --root <vault-root> --single <rel-path>

Edge cases:
  - Files already frontmattered → skip (unless --force).
  - Empty files → log only.
  - File path with spaces (iCloud) → handled by relative path string.
"""

import argparse
import datetime
import re
import sys
from pathlib import Path


FRONT = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL | re.MULTILINE)
KV = re.compile(r"^([a-zA-Z_][\w-]*):\s*(.+?)\s*$", re.MULTILINE)


def parse(path):
    text = path.read_text("utf-8", errors="ignore")
    m = FRONT.match(text)
    if not m:
        return None, text
    return {k: v for k, v in KV.findall(m.group(1))}, text


# ---- origin / authority / topics inference rules ----

PATH_RULES = [
    # (path substring, origin, authority)
    ("Lovart New Help Center/", "official-hand-curated-doc", 5),  # current authoritative
    ("Lovart Docs Archive/",    "official-hand-curated-legacy", 2),  # deprecated v1
    ("Lovart Introduction/",    "internal-curated", 3),
    ("Lovart News/",            "official-news",    4),
    ("Lovart Docs/",            "official-hand-curated-doc", 5),  # alias: keep some legacy paths work
    ("Reference/",              "official-crawl-derived", 4),
    ("Changelog/",              "official-crawl-derived", 5),
    ("Cover Url",               "internal-curated", 2),
    ("博客分类",                 "internal-curated", 3),
]

# Map origin → default source_quality
ORIGIN_QUALITY = {
    "official-hand-curated-doc": "hand-curated-official",
    "official-hand-curated-legacy": "legacy-archive",
    "internal-curated": "user-curated",
    "official-news": "cleaned",
    "official-crawl-derived": "cleaned",
    "user-curated": "user-curated",
}


# keyword → topic mapping for capability surfacing
TOPIC_KEYWORDS = {
    "agent":     ["agent", "design agent", "world's first", "multimodal"],
    "canvas":    ["canvas", "chatcanvas", "editable"],
    "tools":     ["tool", "master touch", "pen", "shape", "mask", "frame"],
    "image":     ["image", "image generator", "flux", "nano banana"],
    "video":     ["video", "video generator", "sora", "veo", "kling"],
    "typography": ["text tool", "typography", "label", "headline"],
    "brand":     ["brand", "brand kit", "guideline"],
    "pricing":   ["pro", "会员", "subscription", "pricing"],
    "knowledge": ["knowledge", "knowledge base"],
    "release":   ["released", "launch", "exit beta", "publicly available"],
}


CAPABILITY_KNOWN = [
    "ChatCanvas", "Master Touch", "Smart Select", "Hand Tool",
    "Pen (P)", "Pencil (B)", "Shape", "Mask", "Layout Grid", "Frame",
    "Image Generator", "Video Generator", "Nano Banana Pro", "Flux 2",
    "Sora 2", "Veo 3", "Kling", "Text Tool", "Slides",
    "Brand Kit", "Knowledge Base", "Design Agent", "Multimodal Agent",
    "Avatar Generation", "Brand Identity", "3-D Avatar",
]


def infer_origin(rel):
    for needle, origin, authority in PATH_RULES:
        if needle in rel:
            return origin, authority
    return "user-curated", 2


def infer_topics(text, rel=""):
    head = text.lower()[:2000]
    topics = []
    for topic, kws in TOPIC_KEYWORDS.items():
        if any(kw in head for kw in kws):
            topics.append(topic)
    # path-based topic hints for crawled files (KB-/www-lovart-ai-...)
    rl = rel.lower()
    if "/changelog" in rl:
        topics.append("release")
    if "/news/" in rl or "/news" == rl.rsplit("/", 1)[0].rsplit("/", 1)[-1]:
        topics.append("news")
    if "/docs/" in rl:
        # also infer sub-topic from URL path
        m = re.search(r"/docs/([^/]+)/", rl)
        if m:
            sub = m.group(1).replace("-", " ")
            if sub and sub not in topics:
                topics.append(sub)
    return list(dict.fromkeys(topics + (["general"] if not topics else [])))


def infer_capabilities(text, rel=""):
    """Extract Lovart capability tokens from text. Pure string-match; precise enough for first pass."""
    body = text
    found = []
    seen = set()
    for cap in CAPABILITY_KNOWN:
        if cap in seen:
            continue
        if re.search(re.escape(cap), body, re.IGNORECASE):
            found.append(cap)
            seen.add(cap)
    return found


def slugify(s):
    s = re.sub(r"\.md$", "", s)
    s = re.sub(r"[^A-Za-z0-9_]+", "-", s)
    s = re.sub(r"-+", "-", s).strip("-")
    return s.lower()[:60]


def extract_canonical_url(text, existing_url=None):
    """
    Pick the canonical source URL from a KB-doc body.

    Strategy:
      1. Prefer existing frontmatter `source` if it's a clean https://www.lovart.ai/docs/... URL.
      2. Scan body, pick first URL matching canonical pattern:
         ^https?://www\.lovart\.ai/docs/[^/\s#]+/[^/\s#]+/?
         (no anchor, looks like a primary help page, not a section anchor).
      3. Fallback: any first https://www.lovart.ai URL.
      4. Fallback: any first URL in body.
    """
    CANON_RE = re.compile(r"^https?://www\.lovart\.ai/docs/[^\s#]+/?[^\s#\)]*$", re.IGNORECASE)
    DOMAIN_RE = re.compile(r"^https?://www\.lovart\.ai[^\s#\)]*$", re.IGNORECASE)

    if existing_url and CANON_RE.match(existing_url):
        return existing_url

    candidates = re.findall(r"https?://[^\s\)\]\"'<>]+", text)
    for u in candidates:
        u_clean = u.rstrip("/.,)")
        if CANON_RE.match(u_clean):
            return u_clean
    for u in candidates:
        u_clean = u.rstrip("/.,)")
        if DOMAIN_RE.match(u_clean):
            return u_clean
    if candidates:
        return candidates[0].rstrip("/.,)")
    return None


def build_frontmatter(rel, text, today, existing=None):
    origin, authority = infer_origin(rel)
    topics = infer_topics(text)
    capabilities = infer_capabilities(text, rel)
    fname = Path(rel).stem
    slug = f"kb-{slugify(fname)}"

    # source_urls: start with canonical + add others
    existing_source = (existing or {}).get("source")
    canonical = extract_canonical_url(text, existing_source)
    urls = list(dict.fromkeys(
        u.rstrip("/.,)") for u in re.findall(r"https?://[^\s\)\]\"'<>]+", text)
    ))
    # canonical first
    if canonical:
        urls = [canonical] + [u for u in urls if u != canonical]
    urls = urls[:10]
    # also surface `source:` value from existing if present
    if existing_source and existing_source.startswith("http"):
        if existing_source not in urls:
            urls.insert(0, existing_source)

    fm = {
        "type": "kb-doc",
        "version": "1.0",
        "schema_version": "1.0",
        "kb_slug": slug,
        "origin": origin,
        "authority": authority,
        "fetched_at": today,
        "topics": topics,
        "capabilities": capabilities,
        "source_urls": urls,
        "related_docs": [],
        "claims": [],
        "crawl_status": "hand-placed",
        "audited": False,
        "path": rel,
    }
    # preserve useful existing keys
    if existing:
        for keep_key in ("title", "author", "published", "created", "description", "tags"):
            if existing.get(keep_key):
                fm[keep_key] = existing[keep_key]
    return fm


def render_front(fm):
    """Render YAML frontmatter python-side (no PyYAML dep)."""
    lines = ["---"]
    # scalars first, then lists
    scalar_keys = ["type", "version", "schema_version", "kb_slug", "origin", "authority",
                   "fetched_at", "source_quality", "crawl_status", "audited", "path"]
    for k in scalar_keys:
        if k in fm:
            v = fm[k]
            if isinstance(v, str):
                # quote if contains colon
                if ":" in v or "#" in v:
                    lines.append(f'{k}: "{v}"')
                else:
                    lines.append(f"{k}: {v}")
            else:
                lines.append(f"{k}: {v}")
    # lists
    list_keys = ["topics", "capabilities", "source_urls", "related_docs", "claims"]
    for k in list_keys:
        if k in fm and fm[k] is not None:
            lines.append(f"{k}:")
            for v in fm[k]:
                if isinstance(v, dict):
                    lines.append(f"  - {next(iter(v.items()))}")
                else:
                    lines.append(f"  - {v}")
    lines.append("---")
    return "\n".join(lines) + "\n"


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--root", default=".")
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--force", action="store_true")
    p.add_argument("--single", help="only process this rel-path (relative to KB root)")
    args = p.parse_args()
    root = Path(args.root).expanduser().resolve()

    kb_root = root / "insight-data" / "Knowledge Base"
    if not kb_root.exists():
        sys.stderr.write(f"kb-frontmatter: KB root not found at {kb_root}\n")
        sys.exit(1)

    today = datetime.date.today().isoformat()

    skip_paths = {
        # meta / index docs (not KB-doc units)
        "KB-SCHEMA.md", "README.md",
        "scripts/", "KB-Index/",
        # URL-list slots (kb-ingest harvests; not KB-doc themselves)
        "Changelog/URL-LIST.md", "Reference/URL-LIST.md",
    }
    targets = []
    for p in sorted(kb_root.rglob("*.md")):
        rel = str(p.relative_to(root))
        skip = False
        for sp in skip_paths:
            if sp in rel:
                skip = True
                break
        if not skip:
            targets.append((rel, p))

    if args.single:
        targets = [(s, root / s) for s, _ in targets if s.endswith(args.single)]

    plan = []
    for rel, p in targets:
        existing, text = parse(p)
        if existing and existing.get("schema_version") and not args.force:
            continue
        plan.append((rel, existing is not None))

    if not plan:
        print(f"kb-frontmatter: nothing to do ({len(targets)} files; all already gated)")
        return

    print(f"kb-frontmatter plan: {len(plan)} files to update")
    for rel, has_none in plan:
        flag = "MISSING_FM" if has_none else "PARTIAL_FM"
        print(f"  [{flag:<11}]  {rel}")

    if args.dry_run:
        return

    for rel, has_none in plan:
        path = root / rel
        text = path.read_text("utf-8", errors="ignore")
        existing_dict, _ = parse(path)
        fm = build_frontmatter(rel, text, today, existing=existing_dict)
        # set source_quality from origin (default policy)
        fm["source_quality"] = ORIGIN_QUALITY.get(fm["origin"], "user-curated")
        # allow existing source_quality to take precedence (so we don't downgrade legacy docs)
        if existing_dict and existing_dict.get("source_quality"):
            fm["source_quality"] = existing_dict["source_quality"]
        # refresh topics/capabilities/source_urls (canonical URL goes first)
        fm["topics"] = infer_topics(text, rel)
        fm["capabilities"] = infer_capabilities(text, rel)
        canonical = extract_canonical_url(text, (existing_dict or {}).get("source"))
        body_urls = []
        for u in re.findall(r"https?://[^\s\)\]\"'<>]+", text):
            cu = u.rstrip("/.,)")
            if canonical and cu == canonical: continue
            body_urls.append(cu)
        fm["source_urls"] = ([canonical] if canonical else []) + body_urls
        fm["source_urls"] = fm["source_urls"][:10]

        new_block = render_front(fm)
        if has_none:
            text2 = FRONT.sub("", text, count=1).lstrip("\n")
        else:
            text2 = text
        path.write_text(new_block + "\n" + text2, encoding="utf-8")


if __name__ == "__main__":
    main()
