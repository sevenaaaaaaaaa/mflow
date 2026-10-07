---
session_date: 2026-07-15
session_topic: "194 修复页质量审计 + FAQ<3 与禁用词批量修复"
session_slug: "non-tool-quality-audit-faq-banned-fix"
profiles_used: [profile-lovart-quality]
tools_used: [content-quality-gates, sanity-publish, sq/mu-patch]
agents: [opencode]
duration_min: 75
files_changed_count: 97
kb_units_added: 0
schema_bumps: 0
related_sessions: []
related_prs: []
status: ready
---

# Context
- 上一轮完成 194 页非 Tool 落地页产品术语注入 + 1 页重建。
- 用户要求审计这 194 页是否存在质量问题、是否有影响转化率的问题。

# Solution
写审计脚本按 COPY-PREFLIGHT + RULES-30 扫描：确认注入本身无问题，但顺带发现 103 页历史遗留问题。用户批准全部修复。生成页面专属 FAQ（补 29 页至 4-5 条）+ 上下文感知禁用词改写（84 页），合并成 97 个 `patch/set`，dry-run→pilot→分批应用，复审计通过。

# Files Changed
| 路径 | 操作 | 备注 |
|------|------|------|
| Sanity compositePage ×97 (feature/topic/scenario/product/solution) | modify | patch/set bodyJson(+1 title) |

# Decisions Made
- D1: FAQ<3 判为 P0 阻断，29 页全部补到 ≥4 条页面专属真实异议 FAQ（规避跨页复用）。
- D2: 禁用词上下文改写而非一刀切；`seamless carousel/panorama/loop` 等设计术语保护。
- D3: carousel/seamless slug 页整体保护 seamless，避免破坏 SEO 标题关键词。
- D4: 只用 patch/set 改 bodyJson+title，其他字段零改动；先 dry-run→pilot→批量。

# Patterns Observed
- P1: 历史落地页普遍 FAQ 跨页复用（"infographics from data"/"customizable templates"），是转化+SLOP 双重隐患，应纳入常规审计维度。
- P2: 伪造 testimonial 常内嵌禁用词（game-changer），审计需覆盖 testimonial quote 字段。
- P3: 禁用词审计需带合法术语白名单（seamless carousel 等），否则误报率高。
- P4: bodyJson 为字符串字段，patch 需整串 set；改写后必须 json.loads 校验。

# Open Questions
- Q1: 全站（非本次 194）feature/scenario 是否也普遍存在 FAQ<3 与跨页复用？值得跑一次全量审计。
- Q2: "smoothly" 等替换词是否应进 anti-slop 二级观察名单，防止新一轮 AI-tell。

# Cross-References
- decisions: MEMORY-PROJECT.md § 1 (Sanity 铁律), RULES-30 (Anti-Slop 禁用词)
- skills: lovart-content-quality-gates, lovart-sanity-publish
- entities: []

# Tags
- #quality-audit #anti-slop #faq #cro #sanity-patch
