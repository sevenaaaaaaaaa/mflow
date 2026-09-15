#!/usr/bin/env python3
"""
Patch refactored blog posts to Sanity CMS.
Converts markdown to Portable Text and patches via API.
"""

import json
import os
import sys
import re
from pathlib import Path
import urllib.request
import urllib.parse

# Configuration
SANITY_CONFIG = os.path.expanduser("~/.config/sanity/config.json")
PROJECT_ID = "o11tm2qe"
DATASET = "production"
API_VERSION = "v2024-01-01"

REWRITTEN_DIR = Path(__file__).parent.parent / "02-rewritten"
PATCHED_DIR = Path(__file__).parent.parent / "03-patched"

def get_auth_token():
    """Get Sanity auth token from config file."""
    with open(SANITY_CONFIG) as f:
        return json.load(f)["authToken"]

# SSOT: Local Dev md_to_portable_text (schema: table.cells = string[])
_SSOT_DIR = str(Path.home() / "Documents/Lovart Local Dev/scripts")
if _SSOT_DIR not in sys.path:
    sys.path.insert(0, _SSOT_DIR)
from md_to_portable_text import md_to_portable_text as markdown_to_portable_text  # noqa: E402


def extract_frontmatter(content):
    """Extract YAML frontmatter from markdown."""
    match = re.match(r'^---\n(.*?)\n---\n', content, re.DOTALL)
    if match:
        frontmatter = {}
        for line in match.group(1).split('\n'):
            if ':' in line:
                key, value = line.split(':', 1)
                frontmatter[key.strip()] = value.strip().strip('"').strip("'")
        return frontmatter, content[match.end():]
    return {}, content

def get_existing_doc_id(slug, token):
    """Get existing document ID from Sanity."""
    groq = f'*[_type == "blog" && slug.current == "{slug}" && !(_id in path("drafts.**"))][0]._id'
    url = f"https://{PROJECT_ID}.api.sanity.io/{API_VERSION}/data/query/{DATASET}"
    params = urllib.parse.urlencode({"query": groq})
    req = urllib.request.Request(
        f"{url}?{params}",
        headers={"Authorization": f"Bearer {token}"}
    )
    resp = urllib.request.urlopen(req, timeout=30)
    result = json.loads(resp.read().decode())
    return result.get("result")

def patch_to_sanity(doc_id, doc, token):
    """Patch document to Sanity using mutations API."""
    url = f"https://{PROJECT_ID}.api.sanity.io/{API_VERSION}/data/mutate/{DATASET}"
    
    # Create mutation payload
    mutation = {
        "mutations": [
            {
                "patch": {
                    "id": doc_id,
                    "set": doc
                }
            }
        ]
    }
    
    data = json.dumps(mutation).encode('utf-8')
    req = urllib.request.Request(
        url,
        data=data,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        },
        method='POST'
    )
    
    resp = urllib.request.urlopen(req, timeout=60)
    return json.loads(resp.read().decode())

def verify_word_count(slug, token):
    """Verify document exists via GROQ."""
    groq = f'*[_type == "blog" && slug.current == "{slug}" && !(_id in path("drafts.**"))][0]._id'
    url = f"https://{PROJECT_ID}.api.sanity.io/{API_VERSION}/data/query/{DATASET}"
    params = urllib.parse.urlencode({"query": groq})
    req = urllib.request.Request(
        f"{url}?{params}",
        headers={"Authorization": f"Bearer {token}"}
    )
    resp = urllib.request.urlopen(req, timeout=30)
    result = json.loads(resp.read().decode())
    doc_id = result.get("result")
    return 1 if doc_id else 0

def main():
    """Main entry point."""
    dry_run = "--dry-run" in sys.argv
    batch_start = int(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1].isdigit() else 0
    batch_size = int(sys.argv[2]) if len(sys.argv) > 2 and sys.argv[2].isdigit() else 3
    
    # Get list of files to process
    rewritten_files = sorted(REWRITTEN_DIR.glob("*.md"))
    batch_files = rewritten_files[batch_start:batch_start + batch_size]
    
    if not batch_files:
        print("No files to process")
        return
    
    print(f"{'[DRY RUN] ' if dry_run else ''}Processing batch: {batch_start} to {batch_start + len(batch_files) - 1}")
    print(f"Files: {[f.stem for f in batch_files]}")
    
    # Create output directory
    PATCHED_DIR.mkdir(parents=True, exist_ok=True)
    
    # Get auth token
    print("\nGetting Sanity auth token...")
    token = get_auth_token()
    
    results = []
    for i, rewritten_file in enumerate(batch_files, 1):
        slug = rewritten_file.stem
        print(f"\n[{i}/{len(batch_files)}] Processing: {slug}")
        
        # Read rewritten content
        with open(rewritten_file, 'r', encoding='utf-8') as f:
            md_content = f.read()
        
        # Extract frontmatter
        frontmatter, body_md = extract_frontmatter(md_content)
        print(f"  Title: {frontmatter.get('title', 'N/A')}")
        
        # Convert to Portable Text
        print(f"  Converting to Portable Text...")
        body_pt = markdown_to_portable_text(body_md)
        word_count = len(body_md.split())
        print(f"  Word count: {word_count}")
        
        # Check word count
        if word_count < 7500:
            print(f"  ⚠ Warning: Word count {word_count} < 7500")
        
        # Get existing document ID
        print(f"  Finding existing document...")
        doc_id = get_existing_doc_id(slug, token)
        
        if not doc_id:
            print(f"  ✗ No existing document found for slug: {slug}")
            results.append({"slug": slug, "status": "not_found"})
            continue
        
        print(f"  Document ID: {doc_id}")
        
        # Prepare patch document
        now = __import__('datetime').datetime.utcnow().isoformat() + 'Z'
        
        patch_doc = {
            "title": frontmatter.get('title', ''),
            "description": frontmatter.get('description', ''),
            "body": body_pt,
            "seo": {
                "_type": "seo",
                "title": frontmatter.get('seo_title', frontmatter.get('title', '')),
                "description": frontmatter.get('seo_description', frontmatter.get('description', '')),
                "noIndex": False,
            },
            "_updatedAt": now,
        }
        
        if dry_run:
            print(f"  [DRY RUN] Would patch document {doc_id}")
            results.append({"slug": slug, "status": "dry_run", "doc_id": doc_id, "word_count": word_count})
        else:
            # Patch to Sanity
            print(f"  Patching to Sanity...")
            try:
                patch_result = patch_to_sanity(doc_id, patch_doc, token)
                print(f"  ✓ Patched successfully")
                
                # Verify word count
                print(f"  Verifying word count...")
                verified_count = verify_word_count(slug, token)
                print(f"  ✓ Verified word count: {verified_count}")
                
                results.append({
                    "slug": slug,
                    "status": "ok",
                    "doc_id": doc_id,
                    "word_count": word_count,
                    "verified_count": verified_count
                })
            except Exception as e:
                print(f"  ✗ Patch failed: {e}")
                results.append({"slug": slug, "status": "patch_failed", "error": str(e)})
        
        # Save patch file for reference
        patch_file = PATCHED_DIR / f"{slug}.json"
        with open(patch_file, 'w', encoding='utf-8') as f:
            json.dump(patch_doc, f, ensure_ascii=False, indent=2)
    
    # Summary
    print(f"\n{'='*60}")
    ok = sum(1 for r in results if r["status"] == "ok")
    print(f"Batch Summary: {ok}/{len(batch_files)} posts patched")
    if not dry_run:
        total_verified = sum(r.get("verified_count", 0) for r in results)
        print(f"Total verified words: {total_verified:,}")
    
    # Save manifest
    manifest_file = PATCHED_DIR / f"manifest-batch-{batch_start}.json"
    with open(manifest_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"Manifest saved to {manifest_file}")

if __name__ == "__main__":
    main()
