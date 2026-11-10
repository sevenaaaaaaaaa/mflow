#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""组装 articles.json：slug 去重 → master 文档（en 优先）+ 语言清单 + 分类（缺失则按 slug 推断）。"""
import json, re, os, sys
from collections import defaultdict

BASE = os.path.dirname(os.path.abspath(__file__))
INV = os.path.join(BASE,'inventory')
os.makedirs(INV, exist_ok=True)

rows = json.load(open('/tmp/blog_full.json'))
h2map = json.load(open('/tmp/blog_h2.json')) if os.path.exists('/tmp/blog_h2.json') else {}

PRIO={'en':0,'zh':1,'ja':2,'de':3,'zh-TW':4,'fr':5,'pt':6,'ko':7,'ru':8,'it':9,'es':10,'':99}
by=defaultdict(list)
for r in rows:
    if not r['slug']: continue
    if r['status'] in ('draft','unpublished'): continue
    by[r['slug']].append(r)

def infer_cat(slug):
    s=slug.lower()
    if 'pillar' in s or re.match(r'^\d{1,3}-',s): return 'Lovart 101'
    if 'complete-guide' in s or s.startswith('guide-'): return 'Complete Guide'
    if 'how-to' in s or s.startswith('how-'): return 'How-To'
    if '-review' in s or s.endswith('-review') or '-vs-' in s or 'compared' in s or 'alternative' in s: return 'Reviews'
    if any(k in s for k in ('mistake','myth','salary','report','trend','portfolio','roi','ethic','bias','future','prediction','statistics')): return 'Insight & Trend'
    return 'default'

arts=[]
for slug, docs in by.items():
    docs.sort(key=lambda r: PRIO.get(r['language'],99))
    m = docs[0]
    cat = m.get('cat') if isinstance(m.get('cat'),str) and m.get('cat') else infer_cat(slug)
    arts.append({
        'slug': slug,
        'master': m['language'] or 'en',
        'master_id': m['_id'],
        'title': m.get('title') or '',
        'desc': (m.get('desc') or '')[:400],
        'cat': cat,
        'langs': sorted({d['language'] or 'en' for d in docs}),
    })
json.dump(arts, open(os.path.join(INV,'articles.json'),'w'), ensure_ascii=False)
json.dump(h2map, open(os.path.join(INV,'h2.json'),'w'), ensure_ascii=False)
from collections import Counter
print('唯一文章:', len(arts))
print('分类:', dict(Counter(a['cat'] for a in arts).most_common()))
print('H2 锚点覆盖:', sum(1 for a in arts if h2map.get(a['master_id'])))
