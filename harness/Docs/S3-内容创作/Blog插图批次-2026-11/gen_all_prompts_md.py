#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""生成 ALL-PROMPTS.md：全部 prompt 的单一 md 入口（按 chunk 分节，可整节复制投喂）。"""
import json, os, re
from collections import defaultdict, OrderedDict

BASE = os.path.dirname(os.path.abspath(__file__))
briefs = json.load(open(os.path.join(BASE,'_briefs_flat.json')))
shots  = json.load(open(os.path.join(BASE,'_shots_flat.json')))
w0 = [json.loads(l) for l in open(os.path.join(BASE,'batches/W0-style-sheet.jsonl'))]
man = json.load(open(os.path.join(BASE,'manifest.json')))

# 负面词全文（所有 brief 共用一份，只在顶部出现）
NEG = briefs[0]['negative'] if briefs else ''

CHUNK_ORDER = ['W0'] + sorted({b['chunk'] for b in briefs}, key=lambda c:(c.split('-')[0], int(c.split('-')[1])))
by_chunk = defaultdict(list)
for b in briefs: by_chunk[b['chunk']].append(b)

WAVE_TITLE = {
 'W0':'风格定调（6 航道 × 3 候选，最先跑）',
 'W1':'How-To（3 图/篇）','W2':'Reviews + Best Practice + Branding + Stack',
 'W3':'Insight & Trend + Better Design + 类型未定','W4':'Complete Guide（6 图/篇）','W5':'Pillar / 101（6 图/篇）',
}

out = []
out.append('# Blog 插图批次 · 全部 Prompt 总入口')
out.append('')
out.append(f"> 生成于 2026-11-04 · 风格体系 v3 · 口径：唯一文章 **{man['articles']}** 篇 × 类型规范 → "
           f"AI brief **{man['ai_briefs']}** 条 + 截图任务 **{man['screenshot_tasks']}** 条")
out.append('>')
out.append('> **使用方法**：① 先跑 W0 定调，每航道选定 1 张参考图冻结；② 之后按 chunk 小节顺序投喂——'
           '每个 `###` 小节 = 一个投喂批（24 条），可整节复制；③ 同一篇文章的槽位同会话连跑（seed 已锁）。')
out.append('>')
out.append('> **统一规格**：16:9 · 1600×900 · PNG · 命名用各条 `文件名`。')
out.append('>')
out.append('> **统一负面词（每条 prompt 末尾都要拼接，下文所有 brief 共用此份，不再重复）**：')
out.append('')
out.append('```text')
out.append(NEG)
out.append('```')
out.append('')
out.append('> **风格 SSOT**：`STYLE-SYSTEM.md` · **执行计划**：`BATCH-PLAN.md` · **机器可读源**：`batches/*.jsonl`')
out.append('')

# ---- 目录 ----
out.append('## 目录')
out.append('')
wave_sum = OrderedDict()
for ck in CHUNK_ORDER:
    w = ck.split('-')[0]
    n = len(w0) if w=='W0' else len(by_chunk.get(ck,[]))
    wave_sum.setdefault(w, [0,0])
    wave_sum[w][0]+=1; wave_sum[w][1]+=n
for w,(files,n) in wave_sum.items():
    anchor = w.lower()
    label = WAVE_TITLE.get(w,w)
    out.append(f"- [{w} · {label}](#{anchor}) — {n} 条" + (f" · {files} 个投喂批" if files>1 else ''))
out.append(f"- [截图任务（411，非 AI，另册）](#截图任务)")
out.append('')

def slug_anchor(s):  # md 锚点简化
    return re.sub(r'[^a-z0-9\-]','', s.lower().replace(' ','-'))

# ---- W0 ----
out.append('## W0')
out.append('')
out.append(f"*{WAVE_TITLE['W0']}*")
out.append('')
for b in w0:
    out.append(f"#### {b['id']} · {b['lane']} 候选")
    out.append('')
    out.append(f"- 文件名：`{b.get('filename','style-'+b['id'].lower()+'.png')}` · seed：`{b.get('seed','—')}`")
    out.append('')
    out.append('```text')
    out.append(b['prompt'])
    out.append('```')
    out.append('')

# ---- 各波次 chunk ----
cur_wave=None
for ck in CHUNK_ORDER:
    if ck=='W0': continue
    w = ck.split('-')[0]
    if w != cur_wave:
        cur_wave = w
        out.append(f"## {w}")
        out.append('')
        out.append(f"*{WAVE_TITLE.get(w,w)}*")
        out.append('')
    items = by_chunk[ck]
    out.append(f"### {ck}（{len(items)} 条 · {len({i['article']['slug'] for i in items})} 篇文章）")
    out.append('')
    for b in items:
        a = b['article']
        meta = (f"- `{b['filename']}` · seed `{b['seed']}` · {a['slug']}（{a['lang']}） · "
                f"槽位{b['slot']} {b['image_type']} · {b['lane']}")
        if b.get('archetype'): meta += f" · {b['archetype']}"
        out.append(meta)
        out.append(f"- Alt：{b['alt']}")
        out.append('')
        out.append('```text')
        out.append(b['prompt'])
        out.append('```')
        out.append('')

# ---- 截图任务 ----
out.append('## 截图任务')
out.append('')
out.append('> 411 条真实产品界面截图（非 AI 生成）——走实测截图管线（eeat-system-plan 第 2 层），按 wave 归属与 AI 批次并行。')
out.append('')
out.append('| # | 文件名 | 文章 | 分类 | 波次 |')
out.append('|---|---|---|---|---|')
for i,s in enumerate(shots,1):
    t = s['article']['title'] or s['article']['slug']
    if len(t)>50: t=t[:47]+'…'
    out.append(f"| {i} | `{s['filename']}` | {t}（{s['article']['lang']}） | {s['article']['cat']} | {s['wave']} |")
out.append('')

path=os.path.join(BASE,'ALL-PROMPTS.md')
open(path,'w').write('\n'.join(out)+'\n')
size=os.path.getsize(path)
print(f'ALL-PROMPTS.md 生成完成：{size/1024/1024:.1f} MB，{len(out)} 行')
