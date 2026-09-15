---
session_date: 2026-07-23
session_topic: "post-generation-check.sh — 统一质量门禁(图片404/SEO/质量/批量)"
session_slug: "post-generation-check"
profiles_used: [profile-lovart-management]
tools_used: [post-generation-check, pipeline-state]
agents: [hermes]
duration_min: 15
files_changed_count: 3
schema_bumps: 0
status: ready
---

# Context
- 用户反馈:landing-page 和 signal-writer 仍有 5 个质量问题:
  1. 图片 404
  2. SEO 字段不规范
  3. 运行中忘记约束
  4. 批量脚本无约束
  5. 质量自降
- 现有 hooks 只覆盖词数/H2/日期双写,不覆盖这 5 个

# Solution
**post-generation-check.sh — 统一质量门禁**

5 个 Gate:
- G1: 图片 404 (HEAD 检查所有 URL)
- G2: SEO 字段规范 (9 个必填字段 + Sanity-legal category)
- G3: 结构化质量 (H2 密度 / 词数 / 模板残留)
- G4: 批量脚本约束 (deprecated refs / secrets / safety)
- G5: 质量自降 (fluff / AI 自介 / 低信息密度)

**验证**:
- 真实 blog: PASS with warnings (74 长段落是 warn)
- 脚本检查: 正确拦了命名不合规 (`generate-batch-18-23.py`)
- 20/20 测试 PASS

# Files Changed
| 路径 | 操作 | 备注 |
|------|------|------|
| `1-4 Dev/scripts/hooks/post-generation-check.sh` | add | 5 Gate 统一质量门禁 |
| `1-1 Harness/09-scripts/TOOLS-REGISTRY.md` | modify | 注册新 hook |
| `1-1 Harness/11-knowledge/sessions/2026-07-23-post-generation-check.md` | add | 本文件 |

# Tags
- relevant-tags: #quality-gates #post-generation #image-404 #seo-compliance #2026-07
