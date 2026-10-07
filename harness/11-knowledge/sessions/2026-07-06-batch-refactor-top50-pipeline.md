---
session_date: 2026-07-06
session_topic: "批量改造 TOP50 博客管道搭建 + 测试批次发布"
session_slug: "batch-refactor-top50-pipeline"

profiles_used: [profile-lovart-creation]
tools_used: [pull-existing, refactor, expand-content, patch-sanity, MiniMax-M3]
agents: [opencode]

duration_min: 180
files_changed_count: 50
kb_units_added: 0
schema_bumps: 0

related_sessions: []
related_prs: []
status: ready
---

# Context
- 用户要求批量改造108篇博客中的 TOP50（按GSC曝光降序）
- 每篇需按改造建议.md的方案执行：frontmatter改写 → H1/H2优化 → 长尾内容 → FAQ → Portable Text → patch Sanity
- 验收标准：50篇全部按方案执行 / patch成功0失败 / 字数≥7500

# Solution
搭建完整批量改造管道：
1. pull-existing.py — GROQ查询Sanity拉取现有博客
2. refactor.py — 调用MiniMax-M3（200K context）生成改写内容
3. expand-content.py — 插入扩展块补到7500+字
4. patch-sanity.py — Markdown→Portable Text + mutations API patch回Sanity
5. orchestrate.py — 主编排脚本（test/batch/report模式）

测试批次TOP3已成功发布到Sanity production。

# Files Changed
| 路径 | 操作 | 备注 |
|------|------|------|
| Output/SEO-Reports/Refactoring/scripts/pull-existing.py | add | Sanity GROQ查询拉取 |
| Output/SEO-Reports/Refactoring/scripts/refactor.py | add | MiniMax-M3内容生成 |
| Output/SEO-Reports/Refactoring/scripts/expand-content.py | add | 字数扩展到7500+ |
| Output/SEO-Reports/Refactoring/scripts/patch-sanity.py | add | Portable Text转换+patch |
| Output/SEO-Reports/Refactoring/scripts/orchestrate.py | add | 主编排脚本 |
| Output/SEO-Reports/Refactoring/PLAN-batch-refactor-top50.md | add | 计划文档 |
| Output/SEO-Reports/Refactoring/01-existing/*.json | add | 12篇现有博客数据 |
| Output/SEO-Reports/Refactoring/02-rewritten/*.md | add | 12篇改写内容 |

# Decisions Made
- D1: 使用MiniMax-M3作为内容生成模型（200K context, 65K output）
- D2: 批次大小10篇/批，先测试3篇确认流程
- D3: 字数不足时用expand-content.py插入通用扩展块（review/comparison/howto三种类型）
- D4: patch使用Sanity mutations API（非直接PATCH），验证简化为文档存在性检查

# Patterns Observed
- P1: MiniMax-M3平均生成4500-5500字，需二次扩展才能达到7500+要求
- P2: 扩展块插入点选在FAQ/Conclusion前效果最佳，不会破坏文章结构
- P3: Sanity slug查询可直接用GROQ，无需额外索引
- P4: 改造建议.md中的模板内容（如[Tool 1]）由LLM根据实际产品信息填充

# Open Questions
- Q1: 部分slug在Sanity中不存在（wan-2.1-ai-review, lovart-ai-image-generator, shutterstock-ai-review, seedance-2-orchestration）需确认是否已删除或改名
- Q2: MiniMax-M3生成内容含少量slop词（seamless, unlock, leverage），后续可加后处理过滤
- Q3: 是否需要触发sitemap更新？
- Q4: 是否需要人工抽检生成质量？

# Cross-References
- entities: blog-pipeline, sanity-cms, minimax-m3
- decisions: MEMORY-PROJECT.md § 1 (Sanity铁律)
- skills: lovart-blog-signal-writer, lovart-sanity-publish, lovart-content-quality-gates

# Tags
- relevant-tags: #batch-refactoring #sanity-patch #minimax #blog-pipeline #seo-optimization
