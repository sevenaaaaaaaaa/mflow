#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Blog 插图批次 · brief 生成器 v3（2026-11）
=========================================
口径：唯一文章（slug 去重，master=en 优先）× 每分类规范张数，多语言零增量。

v3 升级（内容全貌锚定 + 一致性三层）：
  · 内容画像：从 inventory/content.json（正文前 35 块 + 全部 H2/H3）提取——
    交付物形态（content > slug > fallback 三级来源）、目标受众、实际步骤数、提及工具；
    Persona 用真实受众、Diagram token 数用真实步骤数、Output 用正文实证的实体形态。
  · 一致性三层：站点层（调色板/光签名/航道/负面词，冻结）→ 分类层（航道映射 + 三类暖中性
    背景微域：ivory 工作台世界 / greige 评测世界 / cream 编辑部世界）→ 篇内层（seed 锁定 +
    机位/原型互异 + 单一交付物形态贯穿全篇槽位）。
  · 可审计：每条 brief 带 signals 字段（形态来源/受众/步骤数/工具），质量差异可量化。

红线：AI 不画 UI/界面/可读文字；Real UI 槽位一律转截图任务（screenshot-tasks.jsonl）。
用法：python3 gen_blog_illustration_briefs.py
输入：inventory/{articles,h2,content}.json   输出：batches/*.jsonl + _*_flat.json + manifest.json
"""
import json, re, os, hashlib, argparse
from collections import Counter, defaultdict

# ---------------- 分类 → 插图槽位规范（methodology-content-writer v4） ----------------
SPEC = {
    'Lovart 101':     [(1,'PillarHero','L1'),(2,'PillarThumb','L5'),(3,'PillarThumb','L5'),(4,'PillarThumb','L5'),(5,'Diagram','L4'),(6,'CTA','L3')],
    'Complete Guide': [(1,'PillarHero','L1'),(2,'PillarThumb','L5'),(3,'PillarThumb','L5'),(4,'PillarThumb','L5'),(5,'Diagram','L4'),(6,'CTA','L3')],
    'How-To':         [(1,'Output','L5'),(2,'StepCompare','L1'),(3,'CTA','L3')],
    'Best Practice':  [(1,'RealUI','SCREENSHOT'),(2,'CTA','L3')],
    'Reviews':        [(1,'RealUI','SCREENSHOT'),(2,'WorkflowCompare','L4'),(3,'CTA','L3')],
    'Better Design':  [(1,'Principle','L4'),(2,'Output','L5'),(3,'CTA','L3')],
    'Insight & Trend':[(1,'Persona','L1'),(2,'Diagram','L4'),(3,'RealUI','SCREENSHOT'),(4,'CTA','L3')],
    'Branding':       [(1,'Principle','L4'),(2,'Output','L5'),(3,'CTA','L3')],
    'Stack × Stack':  [(1,'RealUI','SCREENSHOT'),(2,'WorkflowCompare','L4'),(3,'CTA','L3')],
    'default':        [(1,'Output','L5'),(2,'Diagram','L4'),(3,'CTA','L3')],
}
CATCODE = {'Lovart 101':'PIL','Complete Guide':'CG','How-To':'HT','Best Practice':'BP','Reviews':'REV',
           'Better Design':'BD','Insight & Trend':'INS','Branding':'BR','Stack × Stack':'STK','default':'GEN'}

# ---------------- 风格航道 v2（工艺词汇，token 冻结） ----------------
LANES = {
 'L1': 'High-end commercial photography, 85-100mm lens, single-source soft key light with one long controlled shadow, true-to-life materials, museum-grade editorial color, seamless paper backdrop',
 'L2': 'Cinematic still, shot on 35mm film, volumetric light, layered depth of field, teal-and-amber cinematic palette, subtle film grain, anamorphic feel',
 'L3': 'Soft-body 3D render, hand-glazed matte ceramic and clay with visible throwing rings and an eggshell finish, single-source studio light, gentle contact shadows',
 'L4': 'Editorial flat-graphic composition on a Swiss grid, heavyweight cotton paper, precise alignment, riso-print misregistration and ink bleed as texture accents',
 'L5': 'Macro still-life on a seamless backdrop, tactile craft materials — handmade cotton-rag paper with deckled edges, blind emboss, matte ceramic, copper foil — raking side light revealing texture, precise cast shadows',
 'L6': 'Layered paper-craft diorama, heavyweight archival cardstock hand-cut with torn-edge reveals, soft real shadows, warm directional daylight, disciplined composition',
}

# ---------------- 一致性·分类层：背景微域（同族暖中性，分类亲缘） ----------------
TINT = {'How-To':'warm ivory', 'Lovart 101':'warm ivory', 'Complete Guide':'warm ivory',
        'Reviews':'soft greige', 'Best Practice':'soft greige', 'Stack × Stack':'soft greige',
        'Insight & Trend':'paper cream', 'Better Design':'paper cream', 'Branding':'paper cream', 'default':'paper cream'}
def palette_for(cat, lane):
    if lane == 'L2': return 'teal-and-amber cinematic palette'
    return f"{TINT.get(cat,'paper cream')} base, deep charcoal ink, one muted coral accent kept to a small part of the frame"

NEGATIVE = ('text, letters, words, numbers, watermark, signature, logo text, gibberish UI labels, distorted faces, visible faces, '
            'extra fingers, low resolution, jpeg artifacts, frame border, oversaturated colors, generic purple-blue gradient, '
            'glassmorphism cliche, floating 3D blobs, isometric startup illustration, fake UI screens, gibberish interface text, '
            'glowing connection lines, floating chips, collage of many elements, cluttered composition, busy layout, '
            'busy background texture, dated stock-photo look, neon cyberpunk, trend-chasing gradient mashup, drop-shadow stacking')

CAMERAS = ['front-on eye-level view','three-quarter angle','macro close crop','top-down flat lay','low angle','side profile view']
W, H = 1600, 900
RATIO = '16:9'
FALLBACK_FORM = 'a framed fine-art print on a small easel'

# ---------------- 构图原型系统（个性来源，确定性轮换） ----------------
ARCHETYPES = {
 'A1-monolith':    'the hero stands alone and centered with monumental calm, symmetric breathing room on all sides',
 'A2-cantilever':  'the hero is anchored on the left third of the frame with a vast open field breathing to the right',
 'A3-arrangement': 'seen from above, two objects sit in a precise quiet diagonal, the rest of the surface bare',
 'A4-suspended':   'the hero floats just above the surface with one soft shadow beneath it as the only counterweight',
 'A5-plinth':      'the hero is presented on a low matte plinth seen slightly from below, quiet gallery presence',
 'A6-dialogue':    'two objects face each other across one deliberate gap, the space between them doing the talking',
 'A7-frame-in-frame': 'the piece is presented within a second frame — archival mat board and a thin brass lip',
 'A8-lightfall':   'the hero rests exactly where a single shaft of soft light falls, the surrounding field in gentle shade',
}
ARCH_POOL = {
 'Output':      list(ARCHETYPES),
 'PillarHero':  ['A1-monolith','A2-cantilever','A5-plinth','A8-lightfall'],
 'PillarThumb': ['A1-monolith','A3-arrangement','A4-suspended','A6-dialogue'],
}
PERSONA_SCENES = [
 'at a worktable beside a tall window in morning light',
 'in a material library aisle with one shelf of blank samples behind',
 'before a gallery-style wall, adjusting one large blank canvas sheet',
]
CTA_MOMENTS = [
 'a single rounded ceramic token with a subtle coral core resting on a shallow matte tray',
 'three matte ceramic pebbles ascending like steps, the topmost accented in coral',
 'a matte ceramic card sliding mid-slot into a rounded console groove, one small coral bead following behind it',
]
PRINCIPLE_MOMENTS = [
 'one large shape counter-balanced by a single small element placed off-axis',
 'a quiet progression of cut-paper bars rising across the field',
 'one large circle held in gentle tension between two thin ink lines',
]

# ---------------- 内容画像（v3：正文锚定） ----------------
OBJECT_NOUNS = [
 (r'mood ?board', 'a pin-up moodboard of blank material swatches on a cork board'),
 (r'menu', 'a tall blank menu card standing on a brass stand'),
 (r'\blogo\b|wordmark|logo mark', 'an embossed abstract mark pressed into a thick cotton-paper card'),
 (r'brand kit|brand identity|brand guide|style guide', 'a linen-bound brand book beside one blank stationery card'),
 (r'business card|name card', 'a small stack of blank letterpress cards with one foil edge'),
 (r'thumbnail', 'a framed video still on a small easel'),
 (r'\bvideo\b|\breel\b|\bclip\b|youtube|storyboard', 'a framed video still on a small easel'),
 (r'poster', 'a large framed poster print leaning on a studio wall ledge'),
 (r'\bflyer\b|leaflet', 'a crisp flyer sheet with clean crop marks on a paper tray'),
 (r'packaging|\bbox\b|label', 'one unbranded matte box with clean creases on a podium'),
 (r'\bbanner\b', 'a wide blank banner sheet draped between two brass stands'),
 (r'pitch deck|\bdeck\b|\bslide\b|presentation|\bppt\b', 'a stack of two blank landscape boards with a thin spine'),
 (r'\bresume\b|\bcv\b|portfolio', 'a crisp document sheet on a paper tray, corner lifted by light'),
 (r'infographic|data viz|chart', 'a matte board with abstract bar shapes cut in layered paper'),
 (r'mockup|website|landing page|web design|\bui\b', 'a printed page mock standing on a small matte stand'),
 (r'interior|room design|floor plan', 'a small architectural paper model on a plinth'),
 (r'fashion|apparel|outfit|clothing', 'a draped fabric swatch pair on a tailoring dummy base'),
 (r'product photo|ecommerce|product listing', 'a matte ceramic bottle on a sand-colored podium'),
 (r'character|avatar|mascot', 'a printed character model sheet standing on a small matte easel'),
 (r'\bicon\b|emoji|sticker', 'one enlarged blank icon tile centered on a low plinth'),
 (r'illustration|artwork|art print', 'a giclée art print with deckled edges held in a thin brass lip frame'),
 (r'brochure|booklet|catalog|\bzine\b', 'an open saddle-stitched booklet with blank spreads'),
 (r'wireframe|prototype|app design', 'a layered blank wireframe sheet pinned above a paper phone mock'),
 (r'headshot|portrait photo', 'a small framed portrait print face-down on a linen cloth'),
 (r'ad creative|social media|instagram|tiktok|social post', 'a vertical photo print with clean crop marks beside a blank square card'),
 (r'watermark|signature', 'a debossed monogram seal on cotton paper'),
 (r'\bfont\b|typeface|typography|lettering', 'a type specimen sheet of blank abstract glyphs, letterpress printed'),
 (r'ebook|book cover|cover design', 'a cloth-bound blank book with a foil-stamped spine'),
 (r'invitation|greeting card|card design', 'an engraved blank invitation card on a matching envelope'),
 (r'copyright|ethic|\blaw\b|policy|report|research|study|salary', 'a linen-bound blank folio opened on a felt-covered stand'),
 (r'workflow|automation|agent|pipeline', 'a sequence of three small blank workcards laid in a gentle arc'),
 (r'gallery|museum|exhibit', 'a spotlit empty gallery shelf holding one small framed piece'),
 (r'voice|audio|speech|podcast|text to speech|sound', 'a matte relief of flowing sound-wave curves carved in layered paper'),
 (r'manifesto|opinion|\bessay\b|editorial', 'a large letterpress poster sheet with blank text-block bars pinned on a gallery wall'),
 (r'double 11|11\.11|shopping festival|sales event', 'one unbranded matte gift box with a coral paper band on a podium'),
]
AUDIENCE = [
 (r'freelanc', 'a freelance designer'),
 (r'small business|small team|solopreneur', 'a small-business owner'),
 (r'marketer|marketing team', 'a marketing lead'),
 (r'student|beginner|newcomer', 'a design student'),
 (r'photograph', 'a photographer'),
 (r'founder|startup|entrepreneur', 'a startup founder'),
 (r'agenc', 'an agency creative director'),
 (r'seller|etsy|shopify|store owner|ecommerce', 'an online-shop owner'),
 (r'creator|influencer|youtuber', 'a content creator'),
 (r'enterprise|corporate|b2b', 'a corporate brand team'),
 (r'real estate|realtor', 'a realtor'),
 (r'coach|consultant', 'an independent consultant'),
 (r'nonprofit|\bngo\b', 'a nonprofit communications lead'),
 (r'recruiter|job seeker|career', 'a job-seeking designer'),
 (r'\bdesigner', 'a designer'),
]
STEP_HINT = re.compile(r'^(step\b|\d{1,2}[\.\)\s])|how to|guide|workflow|process|method|framework|setup|checklist', re.I)

def content_profile(cprof):
    text = ' '.join(cprof['intro'] + cprof['h2'] + cprof['h3']).lower()
    text = text[:20000]
    form = None
    for pat, f in OBJECT_NOUNS:
        if re.search(pat, text): form = f; break
    audience = 'a designer'
    for pat, a in AUDIENCE:
        if re.search(pat, text): audience = a; break
    stepish = [h for h in cprof['h2'] if STEP_HINT.search(h or '')]
    steps = min(5, max(3, len(stepish))) if len(stepish) >= 3 else None
    tools = sorted({b for b in BRANDS if re.search(r'\b'+re.escape(b)+r'\b', text)})[:6]
    return {'form': form, 'audience': audience, 'steps': steps, 'tools': tools}

def slug_form(topic):
    t = topic.lower()
    rules = [
        (r'thumbnail|youtube|video', 'a framed video still on a small easel'),
        (r'logo|brand kit|identity', 'an embossed abstract mark pressed into a thick cotton-paper card'),
        (r'menu|restaurant', 'a tall blank menu card standing on a brass stand'),
        (r'poster|print|flyer', 'a large framed poster print leaning on a studio wall ledge'),
        (r'packaging|box|label', 'one unbranded matte box with clean creases on a podium'),
        (r'banner|cover|social', 'a vertical photo print with clean crop marks beside a blank square card'),
        (r'ppt|presentation|deck|slide', 'a stack of two blank landscape boards with a thin spine'),
        (r'resume|cv\b|portfolio', 'a crisp document sheet on a paper tray, corner lifted by light'),
        (r'infographic|data|chart', 'a matte board with abstract bar shapes cut in layered paper'),
        (r'mockup|website|landing|ui\b', 'a printed page mock standing on a small matte stand'),
        (r'interior|room|floor', 'a small architectural paper model on a plinth'),
        (r'fashion|apparel|outfit', 'a draped fabric swatch pair on a tailoring dummy base'),
        (r'product photo|ecommerce', 'a matte ceramic bottle on a sand-colored podium'),
        (r'character|figure|avatar|mascot', 'a printed character model sheet standing on a small matte easel'),
        (r'icon|emoji|sticker', 'one enlarged blank icon tile centered on a low plinth'),
        (r'copyright|ethic|law|policy|privacy|report|trend|research', 'a linen-bound blank folio opened on a felt-covered stand'),
        (r'workflow|automation|agent|pipeline', 'a sequence of three small blank workcards laid in a gentle arc'),
        (r'portfolio|gallery|museum|exhibit', 'a spotlit empty gallery shelf holding one small framed piece'),
    ]
    for pat, form in rules:
        if re.search(pat, t): return form, 'slug'
    return FALLBACK_FORM, 'fallback'

# ---------------- H2 论点锚定 ----------------
def h2_phrase(h2):
    if not h2: return ''
    t = re.sub(r'\s+',' ', h2).strip(' :：-—')
    words = t.split()
    p = ' '.join(words[:6]).strip(' ,.:;!?，。：')
    if p:
        latin = sum(1 for c in p if c.isascii() and c.isalpha())
        alpha = sum(1 for c in p if c.isalpha())
        if alpha and latin/alpha < 0.7: return ''
    return p

PROC_HINT = re.compile(r'how|why|step|workflow|process|method|framework|guide|pipeline|setup|checklist|mistake|myth|truth|secret|principle|rule|decision|bias|ethic|signal', re.I)
def pick_h2(h2s):
    if not h2s: return ''
    for h in h2s:
        if PROC_HINT.search(h or ''): return h2_phrase(h)
    return h2_phrase(h2s[0])

# ---------------- 主题提取 ----------------
ACRONYMS = {'ai','ui','ux','seo','cv','ppt','b2b','saas','gpt','kpi','crm','roi','cta','qr','3d','api','b2c','erp','nft'}
BRANDS = {'lovart','firefly','midjourney','canva','figma','photoshop','leonardo','openai','chatgpt','sora','heygen','krea',
          'runway','pika','capcut','elevenlabs','flux','dalle','gemini','claude','wordpress','wix','squarespace','webflow',
          'youtube','instagram','tiktok','etsy','amazon','pinterest','dribbble','behance','vimeo','notion','hubspot','shopify',
          'adobe','veo','kling','higgsfield','freepik','fotor','picsart','looka','sketch','blender','illustrator','indesign'}
def smart_case(phrase):
    out=[]
    for i,w in enumerate(phrase.split()):
        if w in ACRONYMS: out.append(w.upper())
        elif w in BRANDS: out.append(w.capitalize())
        elif i==0: out.append(w.capitalize())
        else: out.append(w)
    return ' '.join(out)

def clean_topic(title, slug, master='en'):
    s = slug or ''
    s = re.sub(r'^\d{1,3}[-_]+','', s)
    toks = [t for t in re.split(r'-+', s) if t]
    toks = [t for t in toks if not re.fullmatch(r'[a-z]\d{1,3}', t)]
    LANGS={'en','zh','ja','de','fr','pt','ko','ru','it','es','tw'}
    if len(toks)>=2 and toks[-1].lower() in LANGS and master.lower().replace('-','') == toks[-1].lower():
        toks=toks[:-1]
    topic = smart_case(' '.join(toks))
    words=topic.split()
    while words and len(' '.join(words))>80: words=words[:-1]
    return (' '.join(words) or 'creative design'), ' '.join(toks)

def build_alt(image_type, title, slug):
    t = (title or slug or '').strip()
    return f"{t} — {image_type.lower()} illustration"

# ---------------- Prompt 模板 v3 ----------------
def pick_from(pool, key, salt):
    base = int(hashlib.md5((key+'::'+salt).encode()).hexdigest(),16) % len(pool)
    return pool[base]

def build_prompt(image_type, lane, cat, topic, h2a, cam, arch='', form=None, audience=None, steps=None):
    pal = palette_for(cat, lane)
    tail = f'{RATIO}, uncluttered composition, restrained editorial styling, no text, no letters, no numbers, no watermark, no UI screens'
    if image_type == 'Persona':
        scene = pick_from(PERSONA_SCENES, topic, 'scene')
        who = audience or 'a designer'
        return (f"{LANES['L1']}: {who} seen from behind, {scene}, mid-work on {topic}, "
                f"no visible face, at most two work props, "
                f"{cam}, {pal}, the scene fills about 60% of frame, {tail}")
    if image_type == 'Diagram':
        n = steps or (4 if h2a else 3)
        return (f"{LANES['L4']}: a minimal process diagram about {topic}"
                + (f", centered on the idea of {h2a}" if h2a else '')
                + f", rendered as {n} blank geometric tokens connected by thin hand-inked lines, one token accented in coral, "
                f"nodes are empty shapes with no lettering inside, {pal}, wide margins all around, {tail}")
    if image_type == 'Output':
        placement = ARCHETYPES[arch]
        return (f"{LANES['L5']}: {form} as the single hero for an article about {topic}, {placement}. "
                f"At most two supporting blank props. {cam}, {pal}, hero fills about 60% of frame, {tail}")
    if image_type == 'StepCompare':
        return (f"{LANES['L1']}, split composition with one clean vertical gap: the left half shows the raw early state of {form} "
                f"— loose edges, unfinished material — and the right half shows the same piece finished and crisp, "
                f"identical camera angle and light on both halves, the finished half carries the single coral accent, "
                f"{pal}, both halves share one seamless backdrop, {tail}")
    if image_type == 'WorkflowCompare':
        return (f"{LANES['L4']}: two parallel horizontal tracks about {topic} — the upper track is a fragmented chain of four small disconnected tiles, "
                f"the lower track is one continuous clean line with three calm nodes, thin ink lines only, one coral accent on the lower track, "
                f"{pal}, Swiss-grid alignment, wide margins, {tail}")
    if image_type == 'Principle':
        moment = pick_from(PRINCIPLE_MOMENTS, topic, 'principle')
        return (f"{LANES['L4']}: {moment}, expressing the core idea of {topic}, "
                f"one coral accent kept small, {pal}, wide empty margins on all sides, {tail}")
    if image_type == 'CTA':
        moment = pick_from(CTA_MOMENTS, topic, 'cta')
        return (f"{LANES['L3']}: {moment}, a faint motion arc sweeping toward the open space echoing the theme of {topic}, "
                f"{pal}, the subject fills about 55% of frame, calm and quiet, {tail}")
    if image_type == 'PillarHero':
        placement = ARCHETYPES[arch]
        return (f"{LANES['L1']}: {form}, {placement}, staged for the opening spread of an article about {topic}. "
                f"At most two supporting props. {cam}, {pal}, hero fills about 62% of frame, {tail}")
    if image_type == 'PillarThumb':
        placement = ARCHETYPES[arch]
        return (f"{LANES['L5']}: one small tactile token, a simplified miniature of {form}, {placement}. "
                f"Single subject or a quiet pair only. {cam}, {pal}, the subject fills about 55% of frame, {tail}")
    raise ValueError(image_type)

# ---------------- 主流程 ----------------
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--base', default=os.path.dirname(os.path.abspath(__file__)))
    args = ap.parse_args()
    base = args.base
    inv = os.path.join(base,'inventory')
    arts = json.load(open(os.path.join(inv,'articles.json')))
    def load(name):
        try: return json.load(open(os.path.join(inv,name)))
        except Exception: return {}
    h2map = load('h2.json'); content = load('content.json')
    print(f'载入文章 {len(arts)} 篇 | H2 {len(h2map)} | 内容摘要 {len(content)}')

    cats = Counter(a['cat'] for a in arts)
    WAVES = [('W1',['How-To']), ('W2',['Reviews','Best Practice','Branding','Stack × Stack']),
             ('W3',['Insight & Trend','Better Design','default']), ('W4',['Complete Guide']),
             ('W5',['Lovart 101'])]
    wave_of_cat = {c:w for w,cs in WAVES for c in cs}
    arts.sort(key=lambda a: (-len(a['langs']), a['slug']))

    briefs=[]; shots=[]
    seq_by_cat=defaultdict(int)
    form_src_stat=Counter(); aud_hit=0; steps_hit=0
    for a in arts:
        slug=a['slug']; cat=a['cat']; title=a.get('title') or ''
        topic, slug_topic = clean_topic(title, slug, a['master'])
        cprof = content.get(a['master_id']) or {'intro':[],'h2':[],'h3':[]}
        prof = content_profile(cprof)
        h2s = h2map.get(a.get('master_id'), cprof.get('h2') or [])
        h2a = pick_h2(h2s)
        # 形态三级来源：content > slug > fallback；全篇槽位共用同一形态（篇内一致性）
        if prof['form']:
            form, fsrc = prof['form'], 'content'
        else:
            form, fsrc = slug_form(topic)
        form_src_stat[fsrc]+=1
        if prof['audience']!='a designer': aud_hit+=1
        if prof['steps']: steps_hit+=1
        signals = {'form_source':fsrc,'audience':prof['audience'],'steps':prof['steps'],'tools':prof['tools']}

        wave = wave_of_cat.get(cat,'W3')
        catcode = CATCODE.get(cat,'GEN')
        seq_by_cat[catcode]+=1
        cam_off = int(hashlib.md5(slug.encode()).hexdigest(),16) % len(CAMERAS)
        arch_off = int(hashlib.md5((slug+'::arch').encode()).hexdigest(),16) % 8
        slots = SPEC.get(cat, SPEC['default'])
        cam_i = cam_off; arch_i = arch_off
        for (sn, itype, lane) in slots:
            cam = CAMERAS[cam_i % len(CAMERAS)]; cam_i += 1
            fname = f"blog-{slug}-s{sn}-{itype.lower()}-v1.png"
            h2a_slot = h2a if itype in ('Diagram','WorkflowCompare') else ''
            aid = f"B-ILL-{catcode}-{seq_by_cat[catcode]:04d}-{sn}"
            if lane == 'SCREENSHOT':
                shots.append({'id':aid,'wave':wave,'article':{'slug':slug,'title':title,'lang':a['master'],'cat':cat},
                              'slot':int(sn),'image_type':'RealUI','need':'REAL product UI screenshot per methodology spec (not AI)',
                              'source_hint':'实测截图管线 pick-screenshot（eeat-system-plan 第2层）','filename':fname,
                              'alt':build_alt(itype,title,slug),'topic':topic})
                continue
            arch = ''
            if itype in ARCH_POOL:
                pool = ARCH_POOL[itype]
                arch = pool[arch_i % len(pool)]; arch_i += 1
            prompt = build_prompt(itype, lane, cat, topic, h2a_slot, cam, arch, form, prof['audience'], prof['steps'])
            briefs.append({'id':aid,'wave':wave,'article':{'slug':slug,'title':title,'lang':a['master'],'cat':cat},
                           'slot':int(sn),'image_type':itype,'lane':lane,'camera':cam,'archetype':arch,
                           'w':W,'h':H,'ratio':RATIO,
                           'seed':int(hashlib.md5(slug.encode()).hexdigest()[:8],16)%900000+100000,
                           'prompt':prompt,'negative':NEGATIVE,'alt':build_alt(itype,title,slug),
                           'filename':fname,'topic':topic,'signals':signals})

    CH=24
    order=defaultdict(int)
    for b in briefs:
        k=b['wave']
        b['chunk']=f"{k}-{order[k]//CH+1:03d}"; order[k]+=1

    out_batches=os.path.join(base,'batches'); os.makedirs(out_batches,exist_ok=True)
    # 清掉旧 chunk 文件（避免改规范后残留）
    for f in os.listdir(out_batches):
        if re.match(r'^W[1-5]-\d{3}\.jsonl$', f): os.remove(os.path.join(out_batches,f))
    chunks=defaultdict(list)
    for b in briefs: chunks[b['chunk']].append(b)
    for ck,items in sorted(chunks.items()):
        with open(os.path.join(out_batches,f'{ck}.jsonl'),'w') as f:
            for it in items: f.write(json.dumps(it,ensure_ascii=False)+'\n')
    with open(os.path.join(out_batches,'screenshot-tasks.jsonl'),'w') as f:
        for s in shots: f.write(json.dumps(s,ensure_ascii=False)+'\n')

    n=len(briefs)
    man = {
      'generated_by':'gen_blog_illustration_briefs.py (v3)',
      'style_system':'STYLE-SYSTEM.md v3 — 六航道冻结 + 构图原型轮换 + 光签名 + 点睛纪律 + 内容画像锚定 + 分类视觉亲缘',
      'articles':len(arts),'ai_briefs':n,'screenshot_tasks':len(shots),'slots_total':n+len(shots),
      'by_wave':dict(Counter(b['wave'] for b in briefs)),
      'by_category_articles':dict(cats),
      'by_image_type':dict(Counter(b['image_type'] for b in briefs)),
      'by_archetype':dict(Counter(b['archetype'] for b in briefs if b['archetype'])),
      'form_source_distribution':dict(form_src_stat),
      'persona_audience_from_content':aud_hit,
      'diagram_steps_from_content':steps_hit,
      'chunk_size':CH,'chunks':len(chunks),
    }
    json.dump(man,open(os.path.join(base,'manifest.json'),'w'),ensure_ascii=False,indent=1)
    print(json.dumps(man,ensure_ascii=False,indent=1))
    json.dump(briefs,open(os.path.join(base,'_briefs_flat.json'),'w'),ensure_ascii=False)
    json.dump(shots,open(os.path.join(base,'_shots_flat.json'),'w'),ensure_ascii=False)

if __name__=='__main__':
    main()
