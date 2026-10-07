---
session_date: 2026-07-22
session_topic: "Blog 管线 deprecated 残留清理 + frontmatter 修复"
session_slug: "blog-deprecated-cleanup"
profiles_used: [profile-lovart-management]
tools_used: [signal-writer, article-quality-template, i18n-pipeline, it-blog-translation]
agents: [hermes]
duration_min: 15
files_changed_count: 5
schema_bumps: 0
status: ready
---

# Context
- lovart-article-quality-template 说"frontmatter/管线交给 lovart-blog-automation"——但那个 skill 不存在(deprecated)
- lovart-blog-serp-writer / lovart-blog-automation 幽灵引用残留
- deprecated skill 的 frontmatter name 字段被写成了 lovart-blog-signal-writer(错误)
- i18n-pipeline 和 it-blog-translation 的 description 仍说"翻译管线"

# Solution
**5 个 skill 修复**:

1. **lovart-blog-automation/SKILL.md**: frontmatter name 从错误的 `lovart-blog-signal-writer` 改回 `lovart-blog-automation` + 加 DEPRECATED banner
2. **lovart-blog-serp-writer/SKILL.md**: frontmatter name 从错误的 `lovart-blog-signal-writer` 改回 `lovart-blog-serp-writer` + 加 DEPRECATED banner
3. **lovart-i18n-pipeline/SKILL.md**: description 更新为 v2.0——"骨架派生器 + 本地化规则库"
4. **lovart-it-blog-translation/SKILL.md**: description 加 DEPRECATED for Blog content 说明
5. **lovart-blog-signal-writer/SKILL.md**: 清理所有残留引用(从 7 处减到 0)

**最终验证**: 51 个 skill 全量扫描,0 个非作废引用残留

# Files Changed
| 路径 | 操作 | 备注 |
|------|------|------|
| `lovart-blog-automation/SKILL.md` | modify | frontmatter name 修复 + DEPRECATED banner |
| `lovart-blog-serp-writer/SKILL.md` | modify | frontmatter name 修复 + DEPRECATED banner |
| `lovart-i18n-pipeline/SKILL.md` | modify | description 更新为 v2.0 |
| `lovart-it-blog-translation/SKILL.md` | modify | description 加 DEPRECATED |
| `lovart-blog-signal-writer/SKILL.md` | modify | 清理 7 处残留引用 |

# Decisions Made
- D1: deprecated skill 保留 frontmatter name(正确值) + DEPRECATED banner,不删除
- D2: i18n-pipeline 从"翻译管线"降级为"骨架派生器 + 本地化规则库"
- D3: signal-writer 的所有功能引用不再指向 deprecated skill

# Tags
- relevant-tags: #deprecated-cleanup #blog-pipeline #i18n #frontmatter-fix #2026-07
