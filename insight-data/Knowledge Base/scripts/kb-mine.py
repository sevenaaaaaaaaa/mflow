#!/usr/bin/env python3
"""
kb-mine.py — given a topic (and optional capability), return ranked KB units.

Output JSON shape:
  {
    "topic_query": "...",
    "matched_topic": ["agent", "canvas"],
    "topic_hits": [ {kb_slug, path, origin, authority, snippet, score}, ... ],
    "capability_hits": [ {capability, canonical_url, kb_slug_count, kb_units}, ... ],
    "verbatim_quotes": [ {quote, source_url, source_path, line_hint}, ... ]
  }

Algorithm:
  1. Read all KB .md frontmatter
  2. Topic match: any topic contains the query word → score = topic_match + presence_count + authority * 0.5
  3. Capability match: tokenize query + scan KB capabilities; rank by overlap
  4. Verbatim quotes: regex line search across body for keyword, cap 3 per file

Usage:
  python3 kb-mine.py --root <vault> --topic "电商商品图"
  python3 kb-mine.py --root <vault> --topic "Brand Kit" --capability-mode
  python3 kb-mine.py --root <vault> --topic "Lovart canvas 教程" --json
"""

import argparse
import json
import re
import sys
from collections import defaultdict, Counter
from pathlib import Path


FRONT = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL | re.MULTILINE)
KV = re.compile(r"^([a-zA-Z_][\w-]*):\s*(.+?)\s*$", re.MULTILINE)
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
        if val.strip() == "" and i + 1 < len(lines) and lines[i+1].startswith("  -"):
            items = []
            j = i + 1
            while j < len(lines):
                if lines[j].startswith("  - "):
                    items.append(lines[j][4:].strip().strip('"').strip("'"))
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
    skip_dirs = {".venv", "KB-Index", "scripts"}
    skip_files = {"KB-SCHEMA.md"}
    units = []
    for p in sorted(kb_root.rglob("*.md")):
        rel = str(p.relative_to(root))
        if any(s in rel for s in skip_dirs):
            continue
        if p.name in skip_files:
            continue
        text = p.read_text("utf-8", errors="ignore")
        fm = parse_fm(text)
        if not fm.get("schema_version"):
            continue
        body = FRONT.sub("", text, count=1) if FRONT.match(text) else text
        units.append({"path": rel, "body": body, **fm})
    return units


def normalize(s):
    return s.lower().replace(" ", "").replace("-", "").replace("_", "")


def match(units, query):
    qn = normalize(query)
    qtokens = re.findall(r"[a-zA-Z0-9]+|[\u4e00-\u9fff]+", query)
    qtokens_norm = [normalize(t) for t in qtokens if t]

    topic_hits_scores = Counter()
    cap_hits_scores = defaultdict(int)
    matched_topic_set = set()

    for u in units:
        topics = u.get("topics") or ["general"]
        caps = u.get("capabilities") or []

        # topic-overlap
        for t in topics:
            tn = normalize(t)
            if qn in tn or any(tok == tn or tok in tn or tn in tok for tok in qtokens_norm):
                topic_hits_scores[u["path"]] += 2
                matched_topic_set.add(t)

        # body keyword match
        body_lower = u.get("body", "").lower()
        body_norm = normalize(u.get("body", ""))
        kw_count = sum(1 for t in qtokens_norm if t in body_norm)
        if kw_count:
            topic_hits_scores[u["path"]] += min(kw_count, 5)

        # capability overlap
        for c in caps:
            cn = normalize(c)
            if any(tok == cn or tok in cn or cn in tok for tok in qtokens_norm):
                cap_hits_scores[c] += 2
                topic_hits_scores[u["path"]] += 2

    # convert to ranked list
    # ranking formula:
    #   base = topic_match + kw_count + cap_match
    #   authority_boost = authority * 0.5
    #   quality_boost:
    #     - hand-curated-official      → +3     (extra weight for KB-quality)
    #     - cleaned                     → +0.5
    #     - needs-rerender              → -2     (penalty for noisy crawl files)
    #     - (default / unknown)         → +0
    #   canonical_url_boost:
    #     - source_urls contains /docs/<section>/<topic>  → +1.5
    #     - (helps Archive legacy rise up when query matches the
    #       topic name; NewHelpCenter also has this since it has
    #       clean canonical URLs, but they already rank high via auth.)
    quality_boost = {
        "hand-curated-official": 3.0,
        "cleaned": 0.5,
        "needs-rerender": -2.0,
        "legacy-archive": 0.0,  # quality is by content, not freshness
    }

    CANONICAL_URL_RE = re.compile(r"^https?://(?:www\.)?lovart\.ai/docs/[A-Za-z][\w-]+/[A-Za-z][\w-]+/?$", re.IGNORECASE)

    def has_canonical_url(u):
        for url in (u.get("source_urls") or []):
            url = url.rstrip("/")
            if CANONICAL_URL_RE.match(url):
                return True
        return False

    tier1 = []
    for u in units:
        s = topic_hits_scores.get(u["path"], 0)
        if s == 0:
            continue
        s += int(u.get("authority") or 0) * 0.5
        s += quality_boost.get(u.get("source_quality") or "", 0.0)
        if has_canonical_url(u):
            s += 4.0  # canonical URL = "this IS the page on lovart.ai"
        snippet = first_relevant_snippet(u.get("body", ""), qtokens_norm)
        tier1.append({
            "kb_slug": u.get("kb_slug", "?"),
            "path": u["path"],
            "origin": u.get("origin", "?"),
            "source_quality": u.get("source_quality", "?"),
            "authority": int(u.get("authority") or 0),
            "score": s,
            "snippet": snippet,
            "canonical_url_hit": has_canonical_url(u),
        })
    tier1.sort(key=lambda x: (-x["score"], x["path"]))

    # capability_hits
    cap_hits = []
    by_cap = defaultdict(lambda: {"units": [], "urls": []})
    for u in units:
        for c in (u.get("capabilities") or []):
            by_cap[c]["units"].append(u)
            for url in (u.get("source_urls") or []):
                if url not in by_cap[c]["urls"]:
                    by_cap[c]["urls"].append(url)
    for cap, info in sorted(by_cap.items(), key=lambda kv: -cap_hits_scores.get(kv[0], 0)):
        if cap_hits_scores.get(cap, 0) == 0:
            continue
        urls = info["urls"]
        canon = next((u for u in urls if "/docs/" in u), None) or \
                next((u for u in urls if "/news/" in u), None) or \
                (urls[0] if urls else None)
        cap_hits.append({
            "capability": cap,
            "canonical_url": canon,
            "kb_slug_count": len(info["units"]),
            "top_kb_units": [u.get("kb_slug", "?") for u in info["units"][:5]],
        })

    # verbatim quotes
    quotes = []
    for u in units[:50]:
        body = u.get("body", "")
        for tok in qtokens_norm:
            if not tok:
                continue
            for m in re.finditer(re.escape(tok), body, re.IGNORECASE):
                start = max(0, m.start() - 100)
                end = min(len(body), m.end() + 100)
                snippet = body[start:end].replace("\n", " ").strip()
                # skip noise
                if len(snippet) < 30:
                    continue
                quotes.append({
                    "quote": snippet[:200],
                    "kb_slug": u.get("kb_slug", "?"),
                    "path": u["path"],
                })
                if len(quotes) >= 12:
                    break
            if len(quotes) >= 12:
                break
        if len(quotes) >= 12:
            break

    return {
        "topic_query": query,
        "matched_topics": list(matched_topic_set),
        "topic_hits": tier1[:8],
        "capability_hits": cap_hits[:8],
        "verbatim_quotes": quotes[:5],
    }


def first_relevant_snippet(body, qtokens_norm):
    body_norm = normalize(body)
    for tok in qtokens_norm:
        if not tok or len(tok) < 2:
            continue
        idx = body_norm.find(tok)
        if idx >= 0:
            start = max(0, idx - 60)
            end = min(len(body), idx + 200)
            return body[start:end].replace("\n", " ").strip()[:200]
    # fallback: first 200 chars
    return body[:200].replace("\n", " ").strip()


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--root", default=".")
    p.add_argument("--topic", required=True)
    p.add_argument("--capability-mode", action="store_true",
                   help="rank outputs by capability overlap")
    p.add_argument("--json", action="store_true",
                   help="emit JSON instead of human summary")
    args = p.parse_args()

    root = Path(args.root).expanduser().resolve()
    units = collect_kb(root)
    if not units:
        print(f"kb-mine: no KB units at {root}/insight-data/Knowledge Base", file=sys.stderr)
        sys.exit(2)

    result = match(units, args.topic)

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    # human-friendly formatter
    print(f"topic:  {result['topic_query']}")
    print(f"matched_topics: {', '.join(result['matched_topics']) or '(none)'}")
    print()
    print("--- topic_hits ---")
    for h in result["topic_hits"]:
        print(f"  [{h['authority']}] score={h['score']:.1f}  {h['kb_slug']}")
        print(f"    {h['snippet']}")
    print()
    print("--- capability_hits ---")
    for c in result["capability_hits"]:
        print(f"  {c['capability']}  ({c['kb_slug_count']} units)")
        print(f"    canonical_url: {c['canonical_url']}")
    print()
    print("--- verbatim_quotes (max 5) ---")
    for q in result["verbatim_quotes"]:
        print(f"  [{q['kb_slug']}]  {q['quote'][:120]}...")


if __name__ == "__main__":
    main()
