# Lovart Better Design Skill v0.3

## Description

先加载 `lovart-core`、`lovart-blog`、`lovart-content-quality-gates`，并遵守：
`1-1 Harness/Skills/02-creation/references-blog-subskill-governance.md`

跨 Lovart 全工作流（数据采集 / 内容创作 / 质量审核 / 发布 / 监控 / 编排）的 **方法论 Skill**。它不是 S1–S6 任一阶段的执行 skill，而是治理所有 Lovart 内容生产 / 设计 / marketing deliverable 的质量门禁层。

**核心问题**："deliverable 的 evidence / voice / source 是不是真实可信，能不能 ship？"  
- 不真实 → 反 slop / 假数据 / Authoritative voice 漂移 三个失败模式由本 Skill 拦截。  
- 不完整 → Evidence Gaps section 强制 ship-blocker。  
- 不知何时该用 → "When to Use" 章节强制 load-condition。

**Use Cases**: 任何内容 / 设计 / marketing deliverable 起点；或当 Lovart claim "Lovart 抄袭反 slop" 但 evidence 不明时；或当需要校验 deliverable 是否合 publishing standard。

## Category references

When this skill is used as the `Better Design` blog category subskill, also read:

- [references/benchmark-seed-v1.md](references/benchmark-seed-v1.md)
- [references/benchmark-seed-v2.md](references/benchmark-seed-v2.md)
- [references/benchmark-seed-v3.md](references/benchmark-seed-v3.md)
- [references/lovart-better-design-playbook.md](references/lovart-better-design-playbook.md)
- [references/lovart-better-design-review-checklist.md](references/lovart-better-design-review-checklist.md)

These references define the category-specific benchmark base, critique voice, redesign mechanics, and review standard.

## When to Use

加载本 Skill 当下面任一条件成立：
- 准备输出 Lovart 任何 deliverable（blog post / landing page / comparison / review / SaaS UI pattern / brand recap / ads variant / ethics decision）
- 涉及"best X for Y" 类判断、trend/"next thing" 类断言、tool comparison 类结论
- Lovart positioning claim（Lovart 是 X、Lovart 不 X、Lovart 比 Y）需 evidence
- 校验 v0.3 deliverable 是否 ship-ready

**不要** 加载：
- 寒暄 / hard news / 内部 memo / 不产出 deliverable 的 query
- 已在 Sanity publish script 中固化的 publish steps
- 已经在 `lovart-content-quality-gates` (S4) 走过的 publish gate

## Skill Configuration

**Name**: Lovart Better Design Methodology  
**Version**: 0.3  
**Type**: methodology / cross-cutting / quality-governance  
**Dependencies**: none (self-contained methodology layer)  
**Apply**: any Lovart content / design / market deliverable  
**Skill Cycle**: Brand v2 → SaaS UI v2 → Categories 3-7 summary → v0.3 (anti-slop + ethics)  
**Last Updated**: 2026-07-04

---

## Workflow (mandatory — must run in this order)

```
1. Pre-research    → ask: who reads, what decision does it change?
2. Pain mining     → ≥ 10 user voices (or T2.5 fallback)
3. Source grading  → Tag every claim [T1/T2/T3/T4]
4. Counter-evidence pre-flight  → reverse query before strong claim
5. Voice pick      → Synthesis / Prescription / Authoritative (Authoritative gated)
6. Deliverable     → Header + Body + Evidence Gaps + Refresh + Anti-slop self-audit + Lovart framing
7. Self-audit      → 6 hard gates pass; otherwise → ship-blocker
```

---

## Module 1 — Readme & Hard Breaking Conditions

**硬约束**：**没有 evidence = 没有 claims**。这是 ship-blocker 闸门，不是 slogan。

### 这些动作直接 break 本 Skill：
- 「Pain mining 太慢 / 直接写吧」
- 把 affiliate / 赞助贴当 evidence
- 写 always / never / best / worst 但 source < 3
- 用「工具自家排行榜」证「工具自家强」
- 不写 Evidence Gaps 段直接交稿

---

## Module 2 — Research Protocol: Pain Mining + Quota

### Tier 1 — 最痛信号 queries
把 `[TOOL]` `[TOPIC]` 换成具体值：
```
"I hate [TOOL/类别]"
"[TOOL] doesn't work"
"[TOOL] broke / blew up"
"spent [hours/days] on [任务] with [TOOL]"
"refund [TOOL]"
"tried [TOOL], here's what..."
```

### Tier 2 — 对比摩擦
```
"[X] vs [Y]" real comparison
"alternative to [TOOL]"
"moving away from [TOOL]"
"anyone else [COMPLAINT]"
```

### Tier 3 — edge / fail
```
"[TOOL] + failure / limitation / honest review"
"[TOOL] at scale"
```

### Site limiters
- `site:reddit.com`（首选）
- `site:news.ycombinator.com`
- `site:indiehackers.com`
- `site:producthunt.com`（评论 ≥ 5 优先）
- 专属 `r/[domain]` subreddit
- Discord 频道 web 不可索引 → 列 Gap 不强引

### 时间窗口
默认 **180 天内**；> 180 天 = stale / 仅作 context。

### v0.3 每个 deliverable quota
| Item | v0.3 Quota | Why |
|---|---|---|
| 真实用户原话（verbatim + URL + date） | **≥ 10** | v0.1 ≥ 5 容易 all-T3 low signal |
| Strong claim 的独立 source | ≥ 3 | — |
| Counter-evidence source **角度** | **≥ 2 different angles** | v0.1 \"≥ 1 counter\" too shallow |
| T1 自家源 | ≥ 1 per deliverable | — |
| Pain voices 涵盖 ≥ 2 个 niche community | **NEW**: ≥ 2 | 单 community 样本偏 |
| **Buyer-side voice quota ≥ 1** | **NEW v0.3** | founder-voice 有 selection bias |
| Authoritative trigger words auto-cut check | **NEW v0.3** | grep 必须 pass |

### Counter-evidence pre-flight (>strong claim)
**写 strong claim 之前**先跑 reverse query：
```
strong_claim_X = "Recraft V4 默认输出 SVG, logo 选 type 时唯一选项"

preflight_reverses:
  "[strong claim 关键字]" + "doesn't"
  "[strong claim 关键字]" + "limitation"
  "[strong claim 关键字]" + "honest review"
```

返回 ≥ 1 反向源 → claim enable，但 **强制引用**反向观点。
返回失败 = 网络失败 → 标 `[counter-evidence search failure]`，写入 Gap #N。

### Quota softening（v0.3 new）
当 pain search 返回 **< 5 user voices** 经 **≥ 3 distinct query attempts**（soft-chit community 如 r/architecture、r/POD 多 429）：

**允许多源 T2.5 industry-analogue fallback**：

| Source | Reaccept as | Caveat tag |
|---|---|---|
| Industry publications (Architectural Digest, Dezeen, PrintMag) | T2 | "industry-context not first-person" |
| G2 / Capterra / Trustpilot reviews | T2 | "buyer-side post-friction, single-cohort" |
| YouTube interviews named practitioners | T2 | "self-reported transcript verbatim" |
| Conference talk / webinar transcript | T2 | "presented for audience" |
| Smashing Magazine / A List Apart class | T2 | "authored, professional editorial" |

Tag: `[T2.5 industry-analogue]`；treat downstream as T2 but explicit caveat in Evidence Gaps。

### Buyer-side voice quota（v0.3 new）
每个 deliverable 必须 ≥ 1 quote **从 buyer / user / consumer 视角**，不是 founder / builder / maker。

Recognized buyer-side signals：
- "I bought X and Y happened"
- "I tried X as a customer / visitor / reader"  
- Reviews G2/Capterra/Trustpilot
- `r/[product consumer]`（customers not builders）
- Twitter / LinkedIn complaint or praise from outside maker community

Why：founder voice 有 severe selection bias（finished building → only survives）。User voice closer to real friction。

If cannot meet：write deliverable as `voice: builder-perspective only (no buyer-side voice)` + add Gap #N9。

### Authoritative-voice auto-detect（v0.3 new）
每 section。Grep **≥ 25-词 句子** 含：
```
must / never / always / every / best / worst / obviously / simply /
everyone knows / the truth is / any expert will tell you
```
combined with action verb (`use` / `do` / `ship` / `deploy` / `must do`)。

**Auto-cut flag** if found without T2 multi-source backing。Rephrase prescription / synthesis。

Example auto-cut：
- ❌ auto-cut: "The best way to start a brand campaign is to always generate 30 design variants first." (no T2)
- ✅ rewrite: "One approach several teams describe as working: generating 30 variants before listing. We've also seen W fail when…" (prescription with multi-voice)

### 真痛点的判定（≥ 3 命中才用）

- 具体时刻 ("升级 Pro 后我失去 X")
- 具体 artifact ("团队等 3 天")
- 情绪残存 ("this pissed me off")
- mitigation 建议

半 quote 没具体 = marketing copy。**丢**。

### 自吹帖鉴别器（强制）
≥ 1 hit 标 `[filtered]` 或弃：
- 文末 / footer 含 affiliate link ("[affi]" "💰" "yes it's affiliate")
- `[TOOL]` 是 subreddit 名本身
- "Built in N minutes" + N < 60
- 单一 1–10 评分无方法论
- Author 只在该工具 subreddit 活动

---

## Module 3 — Source Grading (T1/T2/T3/T4)

每条事实 一个 tag。Deliverable 末尾贴 tag 分布。

| Tag | 真源 | Allowed in |
|-----|------|------------|
| **T1 强 ≈ first party** | 厂商官方文档 / GitHub / 论文 / 学术 benchmark / 监管 / 法院 | Core assertion；价格（标 valid_through） |
| **T2 中 ≈ second party** | Forbes / TechCrunch / VentureBeat；Apatero / Maginary / MytheAi / Apostle 独立测试；多源共识；Dribbble 评论 / AIGA / 设计师社区 | Prescription（多源支持）；trend claim "as of YYYY-MM" |
| **T3 弱 ≈ single first-hand** | 单 Substack / 单 Reddit 帖 无共鸣 / 个人博客 / 假装中立的 affiliate review | 仅 `[T3]` 标签 + 经独立 query 确认升 T2 / 作 illustrative anecdote |
| **T4 排除** | 工具自家 leaderboard；self-published benchmark 无方法论；付费 award；厂商赞助 "research" | **不引** |

### Selection bias 提醒
- Recraft 在 HuggingFace Text-to-Image 第一 → **T4**（自家参赛）
- Midjourney 自评 "aesthetic ceiling" → **T4**
- Superdesign 自报 "dashboards 第一" → **T4**（=dashboard builder）

### 跨级规则
| Pattern | Tag |
|---------|-----|
| "Tool says X" + 0 独立 confirm | T3 |
| "Tool says X" + ≥ 2 独立 confirm | T2 升 |
| "Industry consensus Y" + ≥ 3 独立 confirm | T2 |
| "1 source Y" + 反向 source + 无法 reconcile | drop |

### Date drift（v0.3 pricing-sensitive）
**易腐烂**：工具价格、模型版本、benchmark。
- 默认 `valid_through` = 90 天
- Pricing-sensitive sections = **30 天**（module 6 + module 8 显式标）
- Benchmark-version-sensitive = 30 天
- 过期未追源 → T1→T2；T2→T3 auto-downgrade。

---

## Module 4 — Content Voice Rules (synthesis / prescription / authoritative)

### Mode 1 — Synthesis（合成）[default allowed]
- 允许 when：合成 ≥ 3 个 T2+ sources
- 禁用：`always / never / best / worst / every / no one / all / studies show / the data shows`
- 健康：`X said this; Y said that; the picture looks roughly like Z` / `Multi-source consensus direction is X; spread between sources is Y`
- For：landscape reports / state-of-X surveys / tool category overview

### Mode 2 — Prescription（处方）
- 允许 when：≥ 5 真实用户原话支持方向（含 caveat）
- 禁用：`the right way is / you must / everyone should / the best practice is / obviously / clearly / simply`
- 健康：`If you're in situation X, one approach we saw several teams use: Y` / `We've also seen W fail when…`
- For：how-to / playbook / framework templates

### Mode 3 — Authoritative Voice（受限）[default 禁止]
**默认禁止**。最易 fabrication。

允许 ONLY when ALL 4 TRUE：
1. Domain expert 具名 attribution（可联系 / 可核验）
2. Review trail 公开 + 可质询
3. Failure cases 与 success 并列
4. SOP 可被 3rd party 复现

违反任一 → auto 降 Mode 2 + 重写。

Even when allowed: `This reflects one team's view as of [date]`。

### Voice upgrade gate（防漂移）
写完 Mode 1/2 后问：
> "如果这是错的，谁会打脸？"
无法具名 → 已默认 Authoritative，没满足 4 豁免。**降 Mode 2 + 重写**。

### Mixing in one deliverable
子 section header 标 mode：
```
## Section 1: Landscape
mode: Synthesis [T1, T2]

## Section 2: Workflow playbook
mode: Prescription [T2 multi-source, ≥5 user voices]
```

### Auto-reject trigger phrases
- "Most experts say..." / "Studies show..." / "It is well-known that..." / "Obviously..." / "The best practice is..." / "Everyone knows..." / "Any expert will tell you..."

每命中 → 检查是否降 Mode 2 候选。

---

## Module 5 — Deliverable Template

### Header（强制）
```markdown
# [Title]

mode:           synthesis | prescription | mixed
audience:       谁读、决定改什么
valid_from:     YYYY-MM-DD
valid_through:  YYYY-MM-DD (default +90d; pricing/benchmark/ethics sections +30d)
sources_count:  T1=N, T2=N, T3=N, T4_dropped=N
counter_ev:     [URL, "dissent"]  (or "no dissent found")
pricing_sensitive_sections: [list section titles needing 30d refresh]
```

### Body 规则
- 每个 claim 句末 `[T1]` / `[T2 multi-source]` / `[T3 single]`
- 用户 quote 后立即 `[URL, date, author if available]`
- 表格 source column 必含
- 子 section header 显式 voice mode
- 数字 "as of YYYY-MM-DD"

### Evidence Gaps section（强制 footer）
```markdown
| # | Gap | Why it matters | Action |
|---|---|---|---|
```
无 Gap 段 = 不诚实 prevent ship。

### Refresh triggers（强制 footer）
```markdown
- 90 days elapsed → re-run pain mining
- ≥ 2 T2 sources contradict → drop claim
- Tool new version → re-verify pricing/benchmark
- New counter-evidence → 改 affected section
- 用户原话 < 10 → 重新跑 pain mining
```

### Anti-slop self-audit（强制 footer）
```markdown
| Gate | Pass? |
|---|---|
| Specificity | yes / no / partial |
| Source trail | yes / no / partial |
| Three-source rule | yes / no / partial |
| Counter-evidence | yes / no / partial |
| Time-to-rot | yes / no / partial |
| Role-of-frame | yes / no / partial |
```
任一 no → ship-blocker, 重做对应。

### Pain voices table (recommended)
```markdown
## Voice-of-user (verbatim, with provenance)
| Pain | Source | Date | Tag |
```

### Lovart framing requirement
```markdown
- Tonal fit: [matches Lovart's positioning / neutral / mismatch]
- Confidence: [T2 or T3 with explicit rationale]
- Do NOT claim: "Lovart is the best" / "Lovart is unique" without enterprise-internal evidence
```
**Anchor**: Lovart zero-user-voice state → 限制 claim 到 T1-documented；不可外推。

### Failure mode samples
❌ Bad: "Most designers agree that Recraft produces real SVG vector output — this makes it the best choice for logo work in 2026." (无 source / self-attribution)
✅ Good: "Recraft V4 generates native SVG (no rasterization step). Verified by [T1 Recraft docs] + [T2 Apatero] + [T2 Maginary] + [T2 MytheAi] + [T3 r/generativeAI single]. 'Best' not independently verified — many logo designers still reject AI logos (counter-evidence r/artificial: 'from a logo design perspective they are all bad')."

---

## Module 6 — Tool Keyword Disambiguator

| Search term | Likely collision | Risk | Filter |
|---|---|---|---|
| **Lovart** | Lovable.dev (瑞典 AI app builder) | HIGH | URL 含 `lovable.dev`/`lovable.app` 或 `r/lovab` = **drop**。保留 = `lovart.ai`/`r/LovartAIOfficial` |
| Recraft | — | LOW | Standard |
| Ideogram | — | LOW | Standard |
| Maginary | — | LOW | Standard |
| v0 | v0 Vercel vs "v0" prompt template | MEDIUM | URL = v0.dev = Vercel |
| Claude Design | Claude Design vs general Claude | MEDIUM | 必须字面 "Claude Design" 或 Anthropic Labs 标识 |
| Brand OS | 营销话术多家叫 | MEDIUM | 必须 attributing vendor |
| Generative UI | pattern 不是 product | LOW | 仅概念用 |
| Magic Patterns | magic patterns 设计系统工具 | LOW | unique vendor |

### Lovart.ai vs Lovable.dev 显式判定法

**Lovable.dev 标志**（not Lovart.ai）：
- URL 含 `lovable.dev`/`lovable.app`
- Subreddit `r/Lovable`/`r/lovable`/`r/lovable_dev`
- Pricing: $20/$25/$50 / 100 credits daily/monthly
- 主体: "build an app" / "vibe coding" / "make me a todo app"
- 投诉: "credits ran out" / "AI won't follow commands" / "refund no response"

**Lovart.ai 标志**：
- URL = `lovart.ai` / `insight.lovart.ai`
- Subreddit = `r/LovartAIOfficial`
- Price: Free / Basic $23–$29 / Pro $58–$72 / Ultimate $157–$196（年/月）
- 主体: "design a logo" / "design a brand" / "create a poster" / "social campaign"
- credit consumption: "500+ credits for complete brand identity"

**Rule**: Quote Lovable.dev posts as **Lovable.dev**, NEVER as "Lovart". Fall back to Gap if no Lovart.ai-specific voice found.

### Auto-disambig pre-query

写 tool claim 之前先跑：
```
"[TOOL]" site:reddit.com
"[TOOL]" pricing 2026
"[TOOL] vs [competitor]" 2026
```
读 3 capture 中 ≥ 1 的 URL / 价格 / framing。任一不匹配预期 → 标 `[Filtered — disambiguation]`。

### 双品牌场景
"AI design agent / design canvas" 赛道搜出 Lovable.dev 是常态（热度排序）。如果目标 = Lovart.ai：
1. 先搜 `Lovart AI design agent`（带 "AI design agent" 同现词限缩）
2. 仍无结果 → 标 `[no direct Lovart.ai voice found]`
3. **不要**借 Lovable.dev examples "类比推断"Lovart 痛点。Lovable ≠ Lovart，借用是 fabrication。

---

## Module 7 — Category-Specific Anti-Slop Triggers (v0.3 new)

通用 anti-slop trigger 不够。按 category 各自硬 trigger list。

### SaaS UI
| Trigger | 来源 |
|---|---|
| Top-left = logo / 装饰图（非可操作 KPI） | Mantlr Pattern 1 [T2] |
| 12+ KPI tiles on main view | Mantlr Pattern 7 [T2] |
| Empty state = "Welcome! Click here to add..." | r/SaaS rywswo [T2] |
| Pricing = 5+ tiers | Gogochimp [T2] 30% penalty |
| Setup flow ≥ 15 min before value | r/SaaS qoawys [T2] |
| Email verification = gate (before value) | r/indiehackers pmzg1g 60% drop [T2] |
| 12-step product tour | r/SaaS rywswo [T2] |
| ≥ 1 multi-step flow without "Step 2 of 4" indicator | r/SaaS rywswo 1/3 abandonment [T2] |
| Sample data = blank | cross-cite [T2] |

### Brand / Logo
| Trigger | 来源 |
|---|---|
| Default = purple/blue gradient stack | r/nocode + Eidos [T2 cross] |
| Pillow buttons on every CTA | same [T2] |
| Container-in-container (≥ 3 levels) | r/nocode [T2] |
| Decorative emoji wrapping plain copy | r/nocode [T2] |
| Vertical stacking as default composition | r/nocode [T2] |
| Wordmark default Inter / Geometric Sans 没改 | Brainy paper [T2] |
| Round corners in cascade | r/nocode [T2] |
| "Generic globe / lightning / handshake" 符号 | LogoDesignValley 2026 [T2] |
| AI-generated logo 没 disclose | r/artificial [T3 dissent] |
| Ultra-thin (100/200) wordmark | Lucky Graphics 2026 [T2] |

### Social Media
| Trigger | 来源 |
|---|---|
| Hero 1 of 5 fixed templates | r/nocode [T2] |
| Same ad running 30+ days | r/FacebookAds 1r67bvt [T2] |
| AI verbiage in hero header | DoWhatWorks [T2] |
| "One perfect creative" workflow | r/FacebookAds 1r67bvt [T2] |
| UGC videos no refresh for 7-10 days | r/FacebookAds 1kr3t72 [T2] |
| Same 3 creatives from 6 months ago | r/FacebookAds 1r67bvt [T2] |
| Catalog ads "no creative refresh schedule" | r/FacebookAds 1r3ezx1 [T2] |
| Container stacking cascade | r/nocode [T2] |
| Emoji-as-design-element in copy | r/nocode [T2] |

### Advertising
| Trigger | 来源 |
|---|---|
| AI in hero header (not subhead) | DoWhatWorks [T2] |
| Frame "AI assistant for X" without unique value | DoWhatWorks [T2] |
| Visual-only variants (no copy framework shift) | Prompt Engines Lab [T2] |
| Single-test decisions (no statistical plan) | aitoolsguidebook [T2] |
| Test < 1000 visitors/variant | Pipeline Monk [T2] |
| Same image copy < 5 variants in batch | DoWhatWorks / Pipeline Monk [T2] |
| Unrealistic numbers in copy（"+500% conversion" no source） | Eidos + Brainy [T2] |
| "Loved by 10M+" without traceability | Brainy paper [T2] |

### E-commerce Listing
| Trigger | 来源 |
|---|---|
| AI-generated 主图 replace 实拍 | r/Etsy 1t5n5os [T2] "85-90% don't match" |
| AI disclosure missing | r/Etsy 1eic8s2 [T1] |
| Hero imagery 在 zoom 下融化 | r/Etsy 1qgktjg [T2] |
| Dropshipping cover-up with AI model | r/GirlGamers 1r40wee [T2] |
| Returns policy 在 footer 反 show | r/micro_saas 1rbwef9 [T2] |
| Lifestyle hero ≠ actual product texture | r/Etsy 1t5n5os [T2] |
| Misleading fabric/cord details | r/Etsy 1qgktjg [T2] |
| AI model generate (no parallel 实拍) | r/Entrepreneur 1r2dfka [T2] |
| Platform 立法时候 hide AI use | r/Etsy 1eic8s2 [T1] |

### Print on Demand
| Trigger | 来源 |
|---|---|
| Same design across mockups inconsistent | implied from Etsy 1qgktjg [T2] |
| Mockup ≠ actual print color/texture | r/Etsy 1t5n5os [T2] reused |
| Bulk design w/o niche specificity | Trendlytic [T1] |
| Generic globe / lightning cliché | brand anti-pattern [T2] |
| 30-design batch but quality drift within | Recraft V4 cross-cite [T2] |
| Uniform style, no token lock | Recraft V4 brand kit [T2] |
| AI disclosure 没 declare | r/Etsy 1eic8s2 [T1] cross |

### Architecture & Interior
| Trigger | 来源 |
|---|---|
| "AI replaces architect" claim | nuit.archi [T1] |
| Midjourney 非-arch context | nuit.archi [T1] |
| Plant / 水 / 大气 lighting claim "solved" | nuit.archi [T1] |
| Geometry flexibility without BIM integration | mnml.ai review [T2] |
| Single AI render vs multi-tool stack | nuit.archi [T1] explicit 2-3 tools |
| Hero claim of <$100/mo 工具 stack | nuit $100-400/user [T1] counter |

### Trigger × category self-check
```
[ ] Walk through applicable triggers for THIS category
[ ] Check each trigger against the deliverable
[ ] Mark [PASS / FAIL / N/A] explicitly
```
Failure → 重做对应 section。

---

## Module 8 — Ethics & Platform AI Disclosure SOP (v0.3 new)

### 原则
```
AI-generated content should be disclosed when it materially affects 
user expectation OR transaction decision.
Default: when in doubt, disclose.
```

### Platform-by-platform rule (as of 2026-07-04, 30d mini-refresh)

| Platform | Rule | Source | Toggle |
|---|---|---|---|
| **Etsy** | Mandatory AI disclosure since 2024-08 (modified/generated photos/videos) | [T1] r/Etsy 1eic8s2 + Etsy seller handbook | "Made with AI" toggle |
| **Amazon** | No formal AI rule, A9 Trust + FTC misrepresentation law | [T2] inferred FTC | Align to actual product — never AI replace hero photo |
| **Shopify merchants** | Self-regulatory + FTC §5 | [T2] FTC | Disclose in product page or terms |
| **Meta Ads** | Must label AI-generated subjects | [T1] Meta transparency | "AI-generated" toggle |
| **Vinted / Depop** | Anti-misrepresentation clause; AI model 图 未明确立法 | [T2] platform ToS | Disclose in listing description |
| **YouTube** | "Altered or synthetic content" label mandatory for realistic AI | [T1] YouTube 2024 | Upload-level toggle |
| **TikTok** | "AI-generated" label mandatory 2024- | [T1] TikTok | Upload-level toggle |
| **LinkedIn** | "AI-generated content" 标签 | [T1] LinkedIn | Optional for B2B posts |
| **Google Ads** | Auto-disclosed via structured metadata | [T1] Google Ads 2025 | Auto "AI" risk signal |

### Global baseline
- **FTC Act §5 (US)**: AI material deception is actionable. 2024-02 enforcement ≥ 5 companies cited. 2025 structured metadata `AI.Generative.Content` schema recommended.
- **EU AI Act**: 2026 transparency obligations effective Aug 2026 — generative content labeling.
- **China 网信办**: 2023 生成式 AI 管理办法 + 2025 实施细则 — 短视频/直播强制 metadata "AI生成" 标识。

### Business decision tree
```
1. Will user perceive this as "real"?
   → Yes: standard disclosure rules
   → No: heightened disclosure (badge / lead with "AI" wording)

2. Does it materially affect transaction decision?
   → Yes: explicit disclosure + opt-out
   → No: standard disclosure OK

3. Platform has explicit rule?
   → Yes: follow verbatim
   → No: default to FTC §5 / EU AI Act / China CAC

4. Industry / domain has norm?
   → Yes: follow norm
   → No: above baseline
```

### Failure cost matrix
| Failure | Reputation | Legal risk |
|---|---|---|
| Etsy product mismatch (AI hero ≠ actual) | refund + 1-star chain + platform audit | platform de-listing |
| Amazon misleading AI photo | listing removal | FTC §5 consumer protection |
| Meta ad AI subject undisclosed | ad reject + audience penalty | FTC + brand safety |
| TikTok undeclared AI content | reduced reach | platform enforcement |
| YouTube AI realistic content unlabeled | channel strike | platform enforcement |
| Architecture render ≠ built | client lawsuit + professional liability | AIA / RIBA + malpractice |
| Brand system "made by AI" claim false | brand credibility collapse | consumer protection |

### Deliverable Ethics footer (mandatory)
```markdown
## Ethics & disclosure self-check
- [ ] Platform-specific rule confirmed (T1)
- [ ] Disclosure language / toggle planned
- [ ] Cross-claim made between content type 和 platform rule
- [ ] FTC § 5 / EU AI Act baseline acknowledged if no platform rule
- [ ] Failure cost estimated ($ / risk band)
```

任一 no → 不 ship。

### Lovart role in ethics (inferred from product strategy, T1 inferred)
Lovart 是 generation layer — **不替用户做 disclosure**。但：
1. 默认 EXIF `XAI.Content: true` 嵌入
2. Templates 内嵌 disclosure-best-practice prompt hint
3. Brand book outputs contain disclosure reminder
4. Publish 前 checklist 包含 disclosure toggle

[T1 inferred — confirm with Marketing/CS]。

### Quick reference (deliverable footer inclusion)
```
| Platform | AI Disclosure Required? | Source |
|---|---|---|
| Etsy | Yes (since 2024-08) | [T1] |
| Amazon | Implicit (FTC) | [T2] |
| Shopify merchants | Self (FTC) | [T2] |
| Meta Ads | Yes (transparency) | [T1] |
| TikTok | Yes (since 2024) | [T1] |
| YouTube | Yes (realistic content) | [T1] |
```

任一 deliverable 涉及 surface miss → ethics fail。

---

## Open Gaps (per deliverable 必须显式处理)

| # | Gap | 处理 |
|---|-----|-------|
| 1 | Lovart.ai 专属 user voice | Pull 内部 NPS / CS / Discord verbatim |
| 2 | Buyer-side voice ≥ 1 / deliverable | 否则标 builder-perspective only |
| 3 | Pricing drift | 30d mini-refresh |
| 4 | Designer community reactions | 多类轮次 refresh 补 |
| 5 | DTCG token / .brand/ runtime cross-cite | 类 2 已 OK，其他类 ref 缺 |
| 6 | 中文圈痛点 baseline | 类 1-7 全英文 Reddit；下次 refresh 加 CSDN/Zhihu |

---

## 工作流示例（brand v2 实战 applied — condensed）

```
Topic: "Best AI logo tools 2026"

Pre-research: audience = Lovart content team; decision = Lovart positioning in brand vertical

Pain mining:
- r/artificial: "From a logo design perspective they are all bad"
- r/growmybusiness: "AI tools ... completely lose the plot" (multi-image brand)
- r/SaaS: "Recraft credit-based too much, I just want prep tools"
- r/Freepik_AI: "Just tested Recraft V4 - image generation fails at all attempts" (regression)
- r/KLINGAIVideo: "3-4 subscriptions split flow"
... (10+ voices)

Source grading:
- Recraft SVG: [T1 Recraft docs] + [T1 Cloudflare mirror] + [T2 Apatero] + [T2 Maginary] + [T2 MytheAi + Ropewalk T2]
- Recraft HuggingFace #1: [T1 self-claim] → **T4 dropped** (self-attribution)
- Lovart pricing: [T1 Lovart official]
- Lovart user voice: **0** → Gap #1

Counter-evidence:
- r/artificial 设计师 rejection (slop 不接受)
- Recraft V4 reliability regression (single failure post but flagged)

Voice mode:
- Section 1 Landscape → Synthesis [T1, T2]
- Section 2 Workflow → Prescription [T2 multi-source, 10 user voices]
- Section 3 Anti-slop → Mixed

Module 5 deliverable:
- Header with valid_through = +90d default, +30d pricing-sensitive
- All claims tagged
- Evidence Gaps section: 7 gaps including Lovart.ai voice Gap #1
- Refresh triggers listed
- Anti-slop self-audit table: all "yes"

Module 7 anti-slop gate:
- Walk triggers: Purple gradient stack ✓ — Lovart outputs often have this
- Container nesting ✓
- Decorative emoji ✓
... each PASS/FAIL marked

Module 8 ethics gate:
- Etsy disclosure mention ✓
- Brand kit / logo use case primarily not subject to AI legislation (consumer trust self-regulatory)
- Failure cost evaluated ✓

Ship? → All gates pass → ship-ready。
```

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| v0.1 | 2026-07-04 (test) | Initial: pain mining / source grading / voice rules / template |
| v0.2 | 2026-07-04 | + tool-disambig, quota 5→10, counter-evidence pre-flight, pricing 30d tier |
| **v0.3** | 2026-07-04 | + category-anti-slop(**07**) + ethics-disclosure(**08**) + quota softening + buyer-side voice + authoritative auto-detect + Lovart zero-voice handling rule |

---

## Anti-fabrication inviolables

1. **Lovable ≠ Lovart**. No quote cross-attribution. (Module 6)
2. **No unverified "best / always / never" sentence.** (Module 4 auto-cut)
3. **No 1-source strong claim.** (Module 3 three-source rule)
4. **No T4 self-attribution as evidence.** (Module 3 selection bias call-out)
5. **No "Lovart 优于 X" without user evidence.** (Module 5 Lovart framing: T1-only)
6. **No AI-generated product-photo replace 实拍 on Etsy.** (Module 7/8 dual)
7. **No missing Evidence Gaps section.** (Module 5 ship-blocker)
8. **No Platform ethics bypass.** (Module 8 ship-blocker)
9. **No founder-only voice deliverable.** (Module 2 buyer-side hard quota)
10. **No cross-tool finding without Lovart zero-voice handling.** (Module 5)

任一违 → deliverable 不 ship。

---

**Skill Status**: v0.3 published, ready for production use. Refresh trigger = 90 days / new Lovart voice / new platform law / new tool collision.
