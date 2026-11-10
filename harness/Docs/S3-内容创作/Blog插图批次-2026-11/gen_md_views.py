#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""从 _briefs_flat.json / _shots_flat.json 生成 md/ 可读版（每分类一份 + 总览）。"""
import json, os, sys
from collections import defaultdict, Counter

BASE = os.path.dirname(os.path.abspath(__file__))
briefs = json.load(open(os.path.join(BASE,'_briefs_flat.json')))
shots  = json.load(open(os.path.join(BASE,'_shots_flat.json')))
man    = json.load(open(os.path.join(BASE,'manifest.json')))

os.makedirs(os.path.join(BASE,'md'), exist_ok=True)

by_art = defaultdict(list)
shot_by_art = defaultdict(list)
for b in briefs: by_art[(b['wave'],b['article']['slug'])].append(b)
for s in shots:  shot_by_art[(s['wave'],s['article']['slug'])].append(s)

CAT_TITLE = {
 'Lovart 101':'Pillar / 101（重视觉 6 张/篇）',
 'Complete Guide':'Complete Guide（重视觉 6 张/篇）',
 'How-To':'How-To 教程（3 张/篇）',
 'Best Practice':'Best Practice（1 AI + 1 截图）',
 'Reviews':'Reviews 对比评测（2 AI + 1 截图）',
 'Better Design':'Better Design（3 张/篇）',
 'Insight & Trend':'Insight & Trend（3 AI + 1 截图）',
 'Branding':'Branding（3 张/篇）',
 'Stack × Stack':'Stack × Stack（2 AI + 1 截图）',
 'default':'类型未定（通用 3 张/篇）',
}
def slugify(c):
    return {'Lovart 101':'pillar-101','Complete Guide':'complete-guide','How-To':'how-to','Best Practice':'best-practice',
            'Reviews':'reviews','Better Design':'better-design','Insight & Trend':'insight-trend','Branding':'branding',
            'Stack × Stack':'stack-stack','default':'generic'}.get(c, 'misc')
SPEC_TXT = {
 'PillarHero':'Pillar 主视觉（L1）','PillarThumb':'分类缩略 token（L5）','Diagram':'概念流程图（L4）',
 'CTA':'品牌收尾（L3）','Output':'成品实体化（L5）','StepCompare':'双联 before/after（L1）',
 'WorkflowCompare':'双轨对比（L4）','Principle':'设计原则形态（L4）','Persona':'人物场景·背影（L1）','RealUI':'真实界面（截图任务）',
}

# 按波次/分类输出
cat_groups = defaultdict(lambda: defaultdict(list))   # wave -> cat -> [slug]
for (wave,slug) in by_art:
    b0 = by_art[(wave,slug)][0]
    cat_groups[wave][b0['article']['cat']].append(slug)

lines_all = []
total_ai = sum(len(v) for v in by_art.values())
lines_all.append(f'# Blog 插图批次 · 全部 brief 可读版\n')
lines_all.append(f'> AI brief 共 **{total_ai} 条**（{len(by_art)} 篇文章）+ 截图任务 **{len(shots)} 条**（另册）。')
lines_all.append('> 风格与纪律见 `../STYLE-SYSTEM.md`；执行顺序见 `../BATCH-PLAN.md`。\n')

for wave in sorted(cat_groups):
    for cat in sorted(cat_groups[wave]):
        slugs = cat_groups[wave][cat]
        fn = f"{wave}-{slugify(cat)}.md"
        out=[]
        out.append(f"# {wave} · {CAT_TITLE.get(cat,cat)}\n")
        out.append(f"- 文章 {len(slugs)} 篇 · AI brief {sum(len(by_art[(wave,s)]) for s in slugs)} 条 · 截图任务 {sum(len(shot_by_art[(wave,s)]) for s in slugs)} 条")
        out.append(f"- 投喂文件：`batches/{wave}-*.jsonl`（每文件 24 条，同一篇文章的槽位在同一会话内连跑，seed 已按 slug 锁定）\n")
        out.append('| # | 文章（master 语言） | 槽位构成 |')
        out.append('|---|---|---|')
        for i,s in enumerate(slugs,1):
            bs = by_art[(wave,s)]
            a = bs[0]['article']
            slots = ' + '.join(SPEC_TXT.get(b['image_type'],b['image_type']) for b in bs)
            if (wave,s) in shot_by_art:
                slots += ' ＋ ' + ' + '.join(SPEC_TXT.get(x['image_type'],'截图') for x in shot_by_art[(wave,s)])
            t = (a['title'] or a['slug'])
            if len(t)>64: t=t[:61]+'…'
            out.append(f"| {i} | `{a['slug']}`（{a['lang']}）{t} | {slots} |")
        # 示例 prompt：该分类第一条 brief
        ex = by_art[(wave,slugs[0])][0]
        out.append(f"\n## 示例 brief（{ex['id']}）\n")
        out.append(f"- 文章：`{ex['article']['slug']}` — {ex['article']['title']}")
        out.append(f"- 槽位 {ex['slot']} · {SPEC_TXT.get(ex['image_type'])} · 航道 {ex['lane']} · seed {ex['seed']}")
        out.append(f"- 文件名：`{ex['filename']}` · Alt：{ex['alt']}\n")
        out.append('```')
        out.append(ex['prompt'])
        out.append('```\n')
        open(os.path.join(BASE,'md',fn),'w').write('\n'.join(out))
        lines_all.append(f"- [`md/{fn}`] {CAT_TITLE.get(cat,cat)} — {len(slugs)} 篇 / {sum(len(by_art[(wave,s)]) for s in slugs)} 条 brief")

open(os.path.join(BASE,'md','00-总览.md'),'w').write('\n'.join(lines_all)+'\n')
print('md 生成完成:', len(cat_groups), '个波次')
