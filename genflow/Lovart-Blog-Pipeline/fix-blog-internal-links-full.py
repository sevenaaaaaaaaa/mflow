#!/usr/bin/env python3
"""
fix-blog-internal-links-full.py
全量扫描 + 修复 Sanity blog body 中的内链。

扫描 8333 篇 blog，将绝对 EN URL 转为相对路径。
支持断点续扫（结果实时写入 JSON）。

用法：
  python3 fix-blog-internal-links-full.py              # 扫描 + 修复
  python3 fix-blog-internal-links-full.py --scan-only  # 只扫描不修复
"""

import json, urllib.request, urllib.parse, time, sys, os
from pathlib import Path
from collections import defaultdict

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
BATCH_SIZE = 50
SCAN_ONLY = '--scan-only' in sys.argv
PROGRESS_FILE = 'Output/QA-Memo/blog-links-scan-progress.json'
REPORT_FILE = 'Output/QA-Memo/blog-internal-links-fix-report.json'

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
            time.sleep(2 ** attempt)
    raise Exception('Mutate failed')

def find_en_links(obj):
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
print(f"Mode: {'SCAN-ONLY' if SCAN_ONLY else 'SCAN + FIX'}")
print(f"Start: {time.strftime('%Y-%m-%d %H:%M:%S')}")

# Load progress if exists
scanned_ids = set()
affected = []
if os.path.exists(PROGRESS_FILE):
    with open(PROGRESS_FILE) as f:
        progress = json.load(f)
    scanned_ids = set(progress.get('scanned_ids', []))
    affected = progress.get('affected', [])
    print(f"Resuming: {len(scanned_ids)} already scanned, {len(affected)} affected")

# Get all doc IDs
print("\nFetching blog document list...")
all_docs = query_post('*[_type=="blog" && !(_id in path("drafts.**")) && defined(body) && defined(slug)]{_id}')
doc_ids = [d['_id'] for d in all_docs if d.get('_id')]
print(f"Total docs: {len(doc_ids)}")

# Filter out already scanned
remaining = [d for d in doc_ids if d not in scanned_ids]
print(f"Remaining to scan: {len(remaining)}")

# Scan
print("\nScanning...")
errors = 0
for i, doc_id in enumerate(remaining):
    try:
        result = query_post(f'*[_id=="{doc_id}"][0]{{_id, slug, language, body}}')
        if not result or not isinstance(result, dict):
            scanned_ids.add(doc_id)
            continue
        body = result.get('body')
        if not body:
            scanned_ids.add(doc_id)
            continue
        en_links = find_en_links(body)
        if en_links:
            affected.append({
                'id': result['_id'],
                'slug': result.get('slug', {}).get('current', ''),
                'lang': result.get('language', 'en'),
                'links': list(set(en_links)),
                'body': body
            })
        scanned_ids.add(doc_id)
        time.sleep(0.05)
    except Exception as e:
        errors += 1
        scanned_ids.add(doc_id)
    
    if (i + 1) % 100 == 0:
        print(f"  Scanned {len(scanned_ids)}/{len(doc_ids)}, affected: {len(affected)}, errors: {errors}")
        # Save progress
        with open(PROGRESS_FILE, 'w') as f:
            json.dump({
                'scanned_ids': list(scanned_ids),
                'affected': [{'id': a['id'], 'slug': a['slug'], 'lang': a['lang'], 'links': a['links']} for a in affected],
                'last_update': time.strftime('%Y-%m-%d %H:%M:%S')
            }, f, ensure_ascii=False)

print(f"\nScan complete: {len(scanned_ids)} scanned, {len(affected)} affected, {errors} errors")

# Summary
lang_counts = defaultdict(int)
for a in affected:
    lang_counts[a['lang']] += 1
total_links = sum(len(a['links']) for a in affected)

print(f"\nSummary:")
print(f"  Documents with EN-only links: {len(affected)}")
print(f"  Total links to fix: {total_links}")
print(f"  By language:")
for lang, count in sorted(lang_counts.items(), key=lambda x: -x[1]):
    print(f"    {lang}: {count}")

# Save final report
report = {
    'total_scanned': len(scanned_ids),
    'total_affected': len(affected),
    'total_links': total_links,
    'by_language': dict(lang_counts),
    'docs': [{'id': a['id'], 'slug': a['slug'], 'lang': a['lang'], 'links': a['links']} for a in affected],
    'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
}
os.makedirs('Output/QA-Memo', exist_ok=True)
with open(REPORT_FILE, 'w') as f:
    json.dump(report, f, indent=2, ensure_ascii=False)
print(f"\nReport: {REPORT_FILE}")

if SCAN_ONLY:
    print("\nScan-only mode. Run without --scan-only to apply fixes.")
    sys.exit(0)

# Apply mutations
print(f"\nApplying mutations to {len(affected)} documents...")
patched = 0
for i in range(0, len(affected), BATCH_SIZE):
    batch = affected[i:i+BATCH_SIZE]
    mutations = []
    for a in batch:
        fix_links_in_body(a['body'])
        mutations.append({'patch': {'id': a['id'], 'set': {'body': a['body']}}})
    try:
        mutate_batch(mutations)
        patched += len(batch)
        print(f"  Patched {patched}/{len(affected)}")
        time.sleep(0.5)
    except Exception as e:
        print(f"  ERROR at batch {i}: {e}")
        break

print(f"\nDone: {patched}/{len(affected)} documents patched")
print(f"End: {time.strftime('%Y-%m-%d %H:%M:%S')}")
