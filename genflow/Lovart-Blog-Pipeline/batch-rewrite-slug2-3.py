#!/usr/bin/env python3
"""Batch rewrite thin blogs for luma-dream-machine-review and adobe-firefly-review."""
import json, os, re, urllib.request, urllib.parse, sys, time
sys.path.insert(0, os.path.expanduser('~/Documents/Lovart Local Dev/scripts'))
from md_to_portable_text import md_to_portable_text as md_to_pt

TOKEN = open("/tmp/sanitytoken.txt").read().strip()
PROJECT = "o11tm2qe"
DATASET = "production"
MUTATE_URL = f"https://{PROJECT}.api.sanity.io/v2024-01-01/data/mutate/{DATASET}"
QUERY_URL = f"https://{PROJECT}.api.sanity.io/v2024-01-01/data/query/{DATASET}"


def patch_blog(doc_id, body_pt, title=None):
    patch_set = {"body": body_pt}
    if title: patch_set["title"] = title
    mutation = {"patch": {"id": doc_id, "set": patch_set}}
    payload = json.dumps({"mutations": [mutation]}).encode()
    req = urllib.request.Request(MUTATE_URL, data=payload,
        headers={"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}, method="POST")
    resp = urllib.request.urlopen(req, timeout=30)
    return json.loads(resp.read())

# Define all patches: (lang, doc_id, markdown_file)
PATCHES = [
    # luma-dream-machine-review
    ("ko", "2ot6vlS4UlNmv8lRJ6tF4k", "Output/Lovart-Blog-Pipeline/ko-luma-dream-machine-review.md"),
    ("de", "5D7P1Ms8gETxHN6XPwvaJ6", "Output/Lovart-Blog-Pipeline/de-luma-dream-machine-review.md"),
    ("fr", "7uF0Fir5z7TerKyiSW1Ftb", "Output/Lovart-Blog-Pipeline/fr-luma-dream-machine-review.md"),
    ("es", "7uF0Fir5z7TerKyiSW2aP5", "Output/Lovart-Blog-Pipeline/es-luma-dream-machine-review.md"),
    ("pt", "WHfzzTIzMbtE5NrFEsJyIi", "Output/Lovart-Blog-Pipeline/pt-luma-dream-machine-review.md"),
    ("ru", "WHfzzTIzMbtE5NrFEsOvx4", "Output/Lovart-Blog-Pipeline/ru-luma-dream-machine-review.md"),
    # adobe-firefly-review
    ("es", "7uF0Fir5z7TerKyiSW2ZqF", "Output/Lovart-Blog-Pipeline/es-adobe-firefly-review.md"),
    ("ko", "2uHMXNBF8GsKL6QSzsnwlv", "Output/Lovart-Blog-Pipeline/ko-adobe-firefly-review.md"),
    ("ru", "WHfzzTIzMbtE5NrFEsOuz6", "Output/Lovart-Blog-Pipeline/ru-adobe-firefly-review.md"),
    ("zh", "2uHMXNBF8GsKL6QSzsiYvf", "Output/Lovart-Blog-Pipeline/zh-adobe-firefly-review.md"),
]

for lang, doc_id, md_path in PATCHES:
    if not os.path.exists(md_path):
        print(f"  SKIP {lang} {doc_id}: {md_path} not found")
        continue
    with open(md_path) as f:
        md = f.read()
    if md.startswith('---'):
        end = md.find('---', 3)
        if end > 0: md = md[end+3:].strip()
    body_pt = md_to_pt(md)
    title = None
    for b in body_pt:
        if b.get("style") == "h1":
            title = b["children"][0]["text"]
            break
    result = patch_blog(doc_id, body_pt, title=title)
    tx = result.get("transactionId", "")
    print(f"  [{lang}] {doc_id} -> {len(body_pt)} blocks | tx={tx}")

print("\nDone. Verifying...")
time.sleep(3)

# Verify all
all_ids = [d[1] for d in PATCHES]
ids_str = json.dumps(all_ids)
q = f'*[_id in {ids_str}]{{_id, language, "bodyLen": length(body), title, "slug": slug.current}}'
url = f"{QUERY_URL}?query={urllib.parse.quote(q)}"
req = urllib.request.Request(url, headers={"Authorization": f"Bearer {TOKEN}"})
verified = json.loads(urllib.request.urlopen(req, timeout=30).read())["result"]
print(f"\nVerified {len(verified)} docs:")
for v in sorted(verified, key=lambda x: (x.get("slug",""), x.get("language",""))):
    print(f"  [{v.get('language')}] {v.get('slug','')} body={v['bodyLen']} | {v.get('title','')[:50]}")
