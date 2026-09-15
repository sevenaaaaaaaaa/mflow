#!/usr/bin/env python3
"""
fix-blog-internal-links.py
批量修复 Sanity blog body 中的内链：将绝对 EN URL 转为相对路径。

问题：blog body Portable Text link marks 使用
  https://www.lovart.ai/blog/slug
导致前端根据浏览器语言重定向到 /zh/blog/slug → 若 ZH 版不存在则404。

修复：转换为 /blog/slug（相对路径），前端按当前页面语言解析。

用法：
  python3 fix-blog-internal-links.py            # dry-run
  python3 fix-blog-internal-links.py --apply    # 实际执行
  python3 fix-blog-internal-links.py --limit 50 # 只处理前50篇
"""

import json, urllib.request, urllib.parse, time, sys, os
from pathlib import Path
from collections import defaultdict

# --- Sanity setup ---
_cfg = json.load(open(Path.home() / '.config/sanity/config.json'))
_tok = _cfg.get('authToken', '')
if not _tok:
    print('ERROR: No Sanity auth token', file=sys.stderr)
    sys.exit(1)

PROJECT = 'o11tm2qe'
DATASET = 'production'
API_VERSION = '2024-01-01'
BASE = f'https://{PROJECT}.api.sanity.io/v{API_VERSION}/data'
EN_LINK_PATTERN = 'lovart.ai/blog/'
LANG_PREFIXES = ['zh','ja','de','fr','pt','ko','ru','zh-TW','it','es']

APPLY = '--apply' in sys.argv
LIMIT = None
for i, arg in enumerate(sys.argv):
    if arg == '--limit' and i + 1 < len(sys.argv):
        LIMIT = int(sys.argv[i + 1])

BATCH_SIZE = 50  # mutations per batch
QUERY_DELAY = 0.1  # seconds between individual doc queries
MUTATE_DELAY = 1.0  # seconds between mutation batches

def query_post(q):
    url = f'{BASE}/query/{DATASET}'
    body = json.dumps({'query': q}).encode()
    req = urllib.request.Request(url, data=body, method='POST', headers={
        'Authorization': f'Bearer {_tok}',
        'Content-Type': 'application/json',
        'User-Agent': 'HermesAgent/1.0'
    })
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                return json.loads(r.read()).get('result', [])
        except Exception as e:
            if '400' in str(e) or '401' in str(e):
                raise
            time.sleep(2 ** attempt)
    return []

def mutate_batch(ops):
    url = f'{BASE}/mutate/{DATASET}'
    body = json.dumps({'mutations': ops}).encode()
    req = urllib.request.Request(url, data=body, method='POST', headers={
        'Authorization': f'Bearer {_tok}',
        'Content-Type': 'application/json',
        'User-Agent': 'HermesAgent/1.0'
    })
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                return json.loads(r.read())
        except Exception as e:
            print(f'  MUTATE retry {attempt+1}: {e}', flush=True)
            time.sleep(2 ** attempt)
    raise Exception('All mutation retries exhausted')

def find_en_links(obj):
    """Recursively find link marks with absolute EN-only URLs."""
    found = []
    if isinstance(obj, dict):
        if obj.get('_type') == 'link':
            href = obj.get('href', '')
            if EN_LINK_PATTERN in href:
                has_lang = any(f'lovart.ai/{lg}/blog/' in href for lg in LANG_PREFIXES)
                if not has_lang:
                    found.append(href)
        for v in obj.values():
            found.extend(find_en_links(v))
    elif isinstance(obj, list):
        for item in obj:
            found.extend(find_en_links(item))
    return found

def fix_links_in_body(obj):
    """Recursively fix link marks: absolute EN URL → relative path."""
    count = 0
    if isinstance(obj, dict):
        if obj.get('_type') == 'link':
            href = obj.get('href', '')
            if EN_LINK_PATTERN in href:
                has_lang = any(f'lovart.ai/{lg}/blog/' in href for lg in LANG_PREFIXES)
                if not has_lang:
                    slug = href.split('/blog/')[-1].rstrip('/')
                    obj['href'] = f'/blog/{slug}'
                    count += 1
        for v in obj.values():
            if isinstance(v, (dict, list)):
                count += fix_links_in_body(v)
    elif isinstance(obj, list):
        for item in obj:
            if isinstance(item, (dict, list)):
                count += fix_links_in_body(item)
    return count

# --- Main ---
print(f"Mode: {'APPLY' if APPLY else 'DRY-RUN'}")
if LIMIT:
    print(f"Limit: {LIMIT} docs")

# Step 1: Get all blog doc IDs
print("\n[1/4] Fetching blog document list...")
all_docs = query_post('*[_type=="blog" && !(_id in path("drafts.**")) && defined(body) && defined(slug)]{_id, slug, language}')
valid_docs = [d for d in all_docs if isinstance(d.get('slug'), dict) and d['slug'].get('current')]
print(f"  Total docs with body: {len(valid_docs)}")

if LIMIT:
    valid_docs = valid_docs[:LIMIT]

# Step 2: Scan each doc for EN-only links
print(f"\n[2/4] Scanning {len(valid_docs)} docs for EN-only absolute links...")
affected = []
scanned = 0

for doc in valid_docs:
    doc_id = doc['_id']
    slug = doc['slug']['current']
    lang = doc.get('language', 'en')
    
    try:
        body = query_post(f'*[_id=="{doc_id}"][0].body')
        if not body:
            continue
        
        en_links = find_en_links(body)
        if en_links:
            affected.append({
                'id': doc_id,
                'slug': slug,
                'lang': lang,
                'links': list(set(en_links)),
                'body': body  # keep for mutation
            })
        scanned += 1
        
        if scanned % 100 == 0:
            print(f"  Scanned {scanned}/{len(valid_docs)}, affected: {len(affected)}")
        
        time.sleep(QUERY_DELAY)
    except Exception as e:
        print(f"  ERROR scanning {doc_id}: {e}")

print(f"\n  Scan complete: {scanned} scanned, {affected_count} affected" if False else "")
print(f"  Scan complete: {scanned} scanned, {len(affected)} affected")

# Step 3: Summary
print(f"\n[3/4] Summary:")
total_links = sum(len(a['links']) for a in affected)
print(f"  Documents to patch: {len(affected)}")
print(f"  Total links to fix: {total_links}")

lang_counts = defaultdict(int)
for a in affected:
    lang_counts[a['lang']] += 1
print(f"\n  By language:")
for lang, count in sorted(lang_counts.items(), key=lambda x: -x[1]):
    print(f"    {lang}: {count} docs")

# Show sample
print(f"\n  Sample fixes (first 10):")
for a in affected[:10]:
    print(f"    [{a['lang']}] {a['slug']}: {len(a['links'])} links")
    for l in a['links'][:3]:
        slug_part = l.split('/blog/')[-1].rstrip('/')
        print(f"      {l} → /blog/{slug_part}")

# Step 4: Apply mutations
if not APPLY:
    print(f"\n[4/4] DRY-RUN complete. Run with --apply to execute mutations.")
    # Save affected list
    save_data = [{'id': a['id'], 'slug': a['slug'], 'lang': a['lang'], 'links': a['links']} for a in affected]
    os.makedirs('Output/QA-Memo', exist_ok=True)
    with open('Output/QA-Memo/blog-internal-links-affected.json', 'w') as f:
        json.dump(save_data, f, indent=2, ensure_ascii=False)
    print(f"  Saved affected list to Output/QA-Memo/blog-internal-links-affected.json")
else:
    print(f"\n[4/4] Applying mutations in batches of {BATCH_SIZE}...")
    
    # Build mutations
    mutations = []
    for a in affected:
        fix_links_in_body(a['body'])
        mutations.append({'patch': {'id': a['id'], 'set': {'body': a['body']}}})
    
    # Apply in batches
    patched = 0
    for i in range(0, len(mutations), BATCH_SIZE):
        batch = mutations[i:i+BATCH_SIZE]
        try:
            result = mutate_batch(batch)
            patched += len(batch)
            print(f"  Patched {patched}/{len(mutations)} docs")
            time.sleep(MUTATE_DELAY)
        except Exception as e:
            print(f"  ERROR patching batch at {i}: {e}")
            break
    
    print(f"\n  Done: {patched}/{len(mutations)} documents patched")
    
    # Verification: spot check
    print("\n  Verification spot checks:")
    for a in affected[:5]:
        body_check = query_post(f'*[_id=="{a["id"]}"][0].body')
        remaining = find_en_links(body_check)
        status = "✓ FIXED" if not remaining else f"✗ STILL HAS {len(remaining)} EN LINKS"
        print(f"    [{a['lang']}] {a['slug']}: {status}")
