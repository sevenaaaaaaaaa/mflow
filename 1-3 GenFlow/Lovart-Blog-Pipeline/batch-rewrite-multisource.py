#!/usr/bin/env python3
"""
批量重写薄内容博客 — 支持非 EN 源语言。
用法: python3 batch-rewrite-multisource.py [--dry-run]
"""
import json, os, re, urllib.request, urllib.parse, time, sys
sys.path.insert(0, os.path.expanduser('~/Documents/Lovart Local Dev/scripts'))
from md_to_portable_text import md_to_portable_text as md_to_pt

TOKEN = open("/tmp/sanitytoken.txt").read().strip()
PROJECT = "o11tm2qe"
DATASET = "production"
BASE = f"https://{PROJECT}.api.sanity.io/v2024-01-01/data/query/{DATASET}"
MUTATE_URL = f"https://{PROJECT}.api.sanity.io/v2024-01-01/data/mutate/{DATASET}"

DRY_RUN = "--dry-run" in sys.argv


def groq(q):
    url = f"{BASE}?query={urllib.parse.quote(q)}"
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {TOKEN}"})
    return json.loads(urllib.request.urlopen(req, timeout=60).read())["result"]

def patch_doc(doc_id, body_pt, title=None):
    patch_set = {"body": body_pt}
    if title: patch_set["title"] = title
    mutation = {"patch": {"id": doc_id, "set": patch_set}}
    payload = json.dumps({"mutations": [mutation]}).encode()
    req = urllib.request.Request(MUTATE_URL, data=payload,
        headers={"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}, method="POST")
    resp = urllib.request.urlopen(req, timeout=30)
    return json.loads(resp.read())

def extract_body_text(body):
    """Extract text blocks from Portable Text body."""
    blocks = []
    for b in body:
        if b.get("_type") != "block": continue
        style = b.get("style", "")
        text = "".join(c.get("text","") for c in b.get("children",[]))
        if not text.strip(): continue
        blocks.append({"style": style, "text": text})
    return blocks

# ── Multi-source slugs ──────────────────────────────────────────
SLUGS = [
    ("ai-subscription-fatigue-utility-gap", "it"),
    ("capcut-ai-review", "zh"),
    ("medeo-ai-review-or-best-ai-tools-by-lovart", "zh"),
    ("meta-imagine-ai-review", "ko"),
    ("wan-2-1-ai-review", "zh"),
    ("best-ai-character-generators-in-2025-top-tools-for-consistent-character-design", "zh"),
    ("hunyuan-video-review", "de"),
    ("getimg-ai-review", "ja"),
    ("picsart-ai-review", "ja"),
    ("video-ocean-review", "ko"),
    ("create-stunning-ui-layouts", "it"),
    ("artlist-ai-review", "it"),
    ("flora-ai-review", "zh"),
    ("imagefx-review", "ko"),
    ("krea-ai-video-generator-review", "zh"),
    ("pixverse-ai-review", "ja"),
    ("luma-dream-machine-review", "ja"),
]

total_patched = 0
errors = []

for slug, src_lang in SLUGS:
    print(f"\n{'='*50}")
    print(f"{slug} (source: {src_lang})")

    # Get source
    src = groq(f'*[_type=="blog" && slug.current=="{slug}" && language=="{src_lang}" && !(_id in path("drafts.**"))][0]{{title, body}}')
    if not src or not src.get("body"):
        print(f"  SKIP: no source"); continue

    src_blocks = extract_body_text(src["body"])
    src_title = src.get("title", "")

    # Get thin versions
    thin = groq(f'*[_type=="blog" && slug.current=="{slug}" && defined(body) && length(body) < 5 && !(_id in path("drafts.**"))]{{_id, language, title}}')
    if not thin:
        print(f"  No thin versions"); continue

    for doc in sorted(thin, key=lambda x: x["language"]):
        lang = doc["language"]
        doc_id = doc["_id"]
        localized_title = doc.get("title") or src_title

        # Build markdown from source structure
        md_parts = [f"# {localized_title}", ""]
        for block in src_blocks:
            if block["style"] == "h1": continue
            elif block["style"] == "h2":
                md_parts.append(f"## {block['text']}")
                md_parts.append("")
            elif block["style"] == "h3":
                md_parts.append(f"### {block['text']}")
                md_parts.append("")
            elif block["style"] == "blockquote":
                md_parts.append(f"> {block['text']}")
                md_parts.append("")
            else:
                md_parts.append(block["text"])
                md_parts.append("")

        body_pt = md_to_pt("\n".join(md_parts))

        if DRY_RUN:
            print(f"  [{lang}] {doc_id} -> {len(body_pt)} blocks (DRY)")
            total_patched += 1
            continue

        try:
            result = patch_doc(doc_id, body_pt, title=localized_title)
            print(f"  [{lang}] {doc_id} -> {len(body_pt)} blocks")
            total_patched += 1
        except Exception as e:
            print(f"  [{lang}] ERROR: {e}")
            errors.append((slug, lang, str(e)))

    time.sleep(1)

print(f"\n{'='*50}")
print(f"DONE: {total_patched} patched, {len(errors)} errors")
for s, l, e in errors:
    print(f"  {s}/{l}: {e}")
