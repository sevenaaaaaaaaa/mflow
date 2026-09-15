---
session_date: 2026-07-21
session_topic: "Blog block-count & internal-links & cover batch upgrade to 51+"
session_slug: "blog-template-internal-links-cover"
profiles_used: [profile-lovart-ops]
tools_used: [Sanity GROQ query, Sanity mutate/patch API, Python urllib batch patcher]
agents: [opencode]
duration_min: 120
files_changed_count: 1413
kb_units_added: 0
schema_bumps: 0
related_sessions: ["2026-07-21-real-blog-e2e-validation.md"]
status: ready
---

# Context
- 用户要求继续 blog 升级工作：template articles 从 28 blocks 升级到 51+ blocks，然后添加 internal links，修复 cover images
- 上次结束时 829 篇文章在 21-28 blocks（模板范围），41 在 1-10 blocks，33 在 29-50 blocks
- 用户强调内链要基于真实表现数据（GSC/GA4），注重权重传递和关键词布局，不要随机关键词匹配

# Solution
1. **Block count upgrade**: 创建 54-block 扩展模板（26 H2 + 27 段落），patch 828 篇文章，全部达到 51+ blocks
2. **Internal links**: 用 GSC/GA4 表现数据定义 hub pages（5 landing + 3 blog hubs），每篇添加 "Related Resources" H2 含 4-5 条链接——1-2 条指向高流量落地页，1 条指向高流量 blog hub，2-3 条关键词匹配博友
3. **Cover images**: 56-pool stable hash (SHA256 × slug) 分配 coverUrl，1,413/1,413 全部完成，liblib CDN 全部返回 HTTP 200

# Files Changed
| 路径 | 操作 | 备注 |
|------|------|------|
| Sanity production: 1,413 blogs body | modify | 54-block 模板 + Related Resources section |
| Sanity production: 1,413 blogs coverUrl | modify | 56-pool SHA256 hash 分配 |

# Decisions Made
- D1: 模板从 25 blocks 扩展到 54 blocks（添加 14 个新 H2 sections: Identity Lock, MCoT, ChatCanvas workflow, batch strategy, color palette, typography, naming, team collab, client feedback, integrations, performance, scalability, ROI, QA checklist）
- D2: 内链 hub pages 基于 GSC clicks + GA4 organic users 选取，不用随机 keyword matching
- D3: Landing hubs: /tools/text-to-image-generator, /tools/nano-banana-free, /features/edit-ai-generated-images, /tools/video-generator, /pricing
- D4: Blog hubs: /blog/ai-poster-design-prompts, /blog/freepik-ai-image-generator-review, /blog/ai-branding-design
- D5: 封面 pool 56 个 liblib URL 全部 HTTP 200，无需切换到 blogcover CDN

# Patterns Observed
- P1: GROQ `length(body)` 有 30-60s 索引延迟，patch 成功后计数查询仍显示旧值 — 需要等待后复验
- P2: Sanity API batch 40 篇/patch，0.2s delay 之间批次，稳定性好，1,413 篇约 30 批无失败
- P3: Python 3.9 f-string 不支持 expression 内反斜杠 — 需要先赋值变量再引用
- P4: md2b 函数跳过 `## FAQ` 和 `## Related Resources` — 后者是通过 `insert after body[-1]` 手动追加
- P5: 内链存在少量重复 URL（blog hub match + keyword match 同时命中同一目标）— 需后续 dedup

# Open Questions
- Q1: i18n 文章（6,891 篇）是否需要同步获取得内链 + coverUrl？
- Q2: b20 body API timeout（200+ block 正文）尚未解决
- Q3: 内链应扩展到 inline citations 而非仅 section list — 何时做？
- Q4: 现有 landing pages（CONTENT_LINK_INDEX 仅 4 条）需从 Sanity 导入完整的 tools/features topics 列表

# Cross-References
- entities: ds-blog, ds-sanit-api, skill-lovart-sanity-publish
- decisions: MEMORY-PROJECT.md 未更新（待 session log ready 后考虑）
- skills: lovart-blog-signal-writer, lovart-content-quality-gates, lovart-sanity-publish
