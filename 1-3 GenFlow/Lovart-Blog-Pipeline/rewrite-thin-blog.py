#!/usr/bin/env python3
"""Rewrite thin blog: convert markdown to Portable Text and patch to Sanity."""
import json, os, re, sys, urllib.request, urllib.parse
sys.path.insert(0, os.path.expanduser('~/Documents/Lovart Local Dev/scripts'))
from md_to_portable_text import md_to_portable_text

TOKEN = open("/tmp/sanitytoken.txt").read().strip()
PROJECT = "o11tm2qe"
DATASET = "production"
MUTATE_URL = f"https://{PROJECT}.api.sanity.io/v2024-01-01/data/mutate/{DATASET}"
QUERY_URL = f"https://{PROJECT}.api.sanity.io/v2024-01-01/data/query/{DATASET}"

COVER_POOL = [
    "/images/blog/white-space-hero.jpg",
    "/images/blog/grid-systems-hero.jpg",
    "/images/blog/bento-grid-hero.jpg",
    "/images/blog/color-theory-hero.jpg",
    "/images/blog/typography-hero.jpg",
    "/images/blog/motion-graphics-hero.jpg",
]

def patch_blog(doc_id, body_pt, title=None, description=None, seo_title=None, seo_desc=None):
    """Patch blog body (and optional metadata) to Sanity."""
    patch = {"body": body_pt}
    if title:
        patch["title"] = title
    if description:
        patch["description"] = description
    if seo_title:
        patch["seoTitle"] = seo_title
    if seo_desc:
        patch["seoDescription"] = seo_desc

    mutation = {"patch": {"id": doc_id, "set": patch}}
    payload = json.dumps({"mutations": [mutation], "returnDocuments": False}).encode()
    req = urllib.request.Request(MUTATE_URL, data=payload,
        headers={"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}, method="POST")
    resp = urllib.request.urlopen(req, timeout=30)
    return json.loads(resp.read())


def verify_blog(doc_id):
    """Verify the patch by querying body length."""
    q = f'*[_id=="{doc_id}"][0]{{_id, title, "bodyLen": length(body)}}'
    url = f"{QUERY_URL}?query={urllib.parse.quote(q)}"
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {TOKEN}"})
    return json.loads(urllib.request.urlopen(req, timeout=30).read())["result"]


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: rewrite-thin-blog.py <markdown_file> <doc_id> [title]")
        sys.exit(1)

    md_file = sys.argv[1]
    doc_id = sys.argv[2]
    title = sys.argv[3] if len(sys.argv) > 3 else None

    with open(md_file, 'r') as f:
        md = f.read()

    # Strip frontmatter if present
    if md.startswith('---'):
        end = md.find('---', 3)
        if end > 0:
            md = md[end+3:].strip()

    body_pt = markdown_to_portable_text(md)
    print(f"Converted {len(body_pt)} blocks from {md_file}")

    result = patch_blog(doc_id, body_pt, title=title)
    print(f"Patch result: {json.dumps(result, indent=2)}")

    import time; time.sleep(2)
    verify = verify_blog(doc_id)
    print(f"Verify: {verify}")
