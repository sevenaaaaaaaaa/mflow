# Blog 404 Rescue P2 Batch 1 — SIGNAL QUEUE

> Locked 2026-08-06. Lane: **404-rescue-compact** (EN ~1,500 words / ZH ~2,400 字 / 段落体，禁清单体)
> Target: Top 20 P2 from `blog-404-triage-2026-08-04.csv` → 分批生产 + 批内自动发布，**批末一次汇报**（不每 5 篇确认）。

## Batch run mode（2026-08-06 起）

| 环节 | 规则 |
|------|------|
| 批次大小 | **10 篇/批**（先写完本批 ready，再开下一批） |
| 生产 | 按上表 # 顺序；同批内 EN → 多语言 rewrite，不 park |
| 发布 | `ready` + QA 过 → 直接 `createIfNotExists` + patch P1 字段 + HTTP 预热 |
| 汇报 | **仅批末**：CSV、`404-status` 计数、失败清单 |
| 仍会停 | preflight BLOCK>0、Sanity 鉴权失败、slug/_id 冲突 — 整批暂停并说明 |

### 质量铁律（批量 ≠ 滥竽充数）

**宁可少发、整批暂停，也不 slop 上线。**

| 硬 BLOCK | 说明 |
|----------|------|
| 禁用词 | EN/ZH 禁用词库任一击中 → 改完再进队列 |
| 清单体 | 正文靠 bullet 撑结构 → 重写为段落叙述 |
| 占位/编造 | IMAGE PLACEHOLDER、假数据、模板句 → 不得发布 |
| 字数注水 | 禁止重复段、同义句堆砌、无信息 FAQ；未达 lane floor 须**实质扩写**，不许 padding |
| Anti-Slop 10 项 | 首人称/翻车/搭档/金句/H2 密度/AI tell 等 — 缺项 = draft，不进发布 |
| i18n | 中文 **≥ EN 词数 × 1.6**；多语言须重写，禁止机翻缩水 |
| KB | 至少 1 处 Lovart 具体能力（ChatCanvas / Brand Kit / Touch Edit / Design Agent） |
| TDK | title ≤75c、desc ≤160c；与 H1 对齐，禁模板串 |

**批内节奏**：每篇过 QA 才标记 `ready`；本批若有 BLOCK 项，**停止扩批**，先修再写下一篇。

| # | lang | slug | lane | source | status |
|---|------|------|------|--------|--------|
| 1 | de | artlist-ai-review | i18n-rewrite | EN draft artlist-ai-review-en.md | **published** |
| 2 | en | vidu-ai-review-2025-ai-video-generation-platform-features-and-verdict | review | other langs | **published** |
| 3 | pt | animaker-review | i18n-rewrite | EN cluster | **published** |
| 4 | en | how-to-chat-to-generate-mockup | how-to | none | **published** |
| 5 | zh | ultimate-guide-ai-design-agent-canvas-for-creators-business | zh-rewrite | multi-lang | **published** |
| 6 | zh | how-to-speed-up-ai-video-rendering-the-2026-guide-to-escaping-the-progressbar-purgatory | zh-rewrite | multi-lang | **published** |
| 7 | zh | ai-design-freelance-pricing-guide-2026 | zh-rewrite | multi-lang | **published** |
| 8 | en | invideo-ai-review-2025-features-pricing-and-complete-hands-on-test | review | multi-lang | **published** |
| 9 | de | text-to-video | i18n-rewrite | multi-lang | **published** |
| 10 | zh-TW | free-ai-design-tools-2026 | zh-rewrite | multi-lang | **published** |
| 11 | en | ai-video-marketing | how-to | multi-lang | **published** |
| 12 | zh-TW | ai-design-myths-debunked-2026 | zh-rewrite | multi-lang | **published** |
| 13 | ru | lovart-vs-rentahuman-ai-design-comparison | i18n-rewrite | multi-lang | **published** |
| 14 | zh-TW | complete-guide-ai-movie-poster-cinematic-design | zh-rewrite | multi-lang | **published** |
| 15 | de | imagefx-review | i18n-rewrite | multi-lang | **published** |
| 16 | zh-TW | hailuo-2-3-free-guide | zh-rewrite | multi-lang | **published** |
| 17 | ru | complete-guide-brand-kit-every-industry-lovart | i18n-rewrite | multi-lang | **published** |
| 18 | en | sora-2-vs-veo-3 | review | local draft exists | **published** |
| 19 | zh | best-ai-design-agent-for-realtor | segment | multi-lang | **published** |
| 20 | pt | lovart-official-trial-guide-avoid-fake-sites | signal-new | none | **published** |

## Lane spec (404-rescue-compact)

- TDK: seo_title ≤75 chars, seo_description 120–160 chars, description ≤300
- Body: 3–4 H2, paragraph prose (no list-only sections), FAQ 3–5, Lovart KB capability cite ≥1
- QA: banned phrase scan, cover HEAD 200, dates dual-write on publish
- **Not** 7,500-word column lane — upgrade later if GSC signals
