---
type: session-template
version: 1.0
audience: [hermes, opencode, claude, codex, cursor]
status: active
owner: profile-lovart-management
generator: 1-1 Harness/11-knowledge/sessions/SESSION-TEMPLATE.md
---

# Session Log — Template

> **用法**：每轮会话**结束时**，agent 应该写一份这个文件到 `1-1 Harness/11-knowledge/sessions/{YYYY-MM-DD}-{slug}.md`。
>
> 触发信号（任一即可）：
> - 用户说 "收尾 / 归档 / 这轮可以收尾 / 写日志 / wrap up / log this"
> - Agent 自己判断该会话触及 5+ 个文件 / 重要决策
> - 一轮结束前 agent 主动问 "要不要我写 session log？"

---

## Schema (frontmatter + body)

```yaml
---
session_date: YYYY-MM-DD              # 会话日期
session_topic: "一句话描述主题"          # 例: "Lovart KB ranking 算法调优"
session_slug: "kebab-case"             # 例: "kb-ranking-tune"

# 谁做的 / 用什么做的
profiles_used: [profile-lovart-management]      # 哪条工作线
tools_used: [kb-mine, kb-frontmatter, ...]     # 用了哪些 skill / 脚本
agents: [hermes, claude]                        # 谁参与了

# 元数据
duration_min: 60                                # 估算时长
files_changed_count: 12                         # 改了几个文件
kb_units_added: 0                               # 新增 KB unit
schema_bumps: 0                                 # schema version bumps

# 链接
related_sessions: []                            # 之前相关 sessions
related_prs: []                                 # 关联 PR / 任务

# 状态
status: draft | ready | reviewed | archived
---

# Context
- 用户提出的问题 / 触发 session 的契机
- 一段话讲清楚：这次是为了解决什么

# Solution
- 实现的方案概述（要简短，一段话说清）
- 如果有架构图 / 流程图，描述在这里

# Files Changed
| 路径 | 操作 | 备注 |
|------|------|------|
| `1-1 Harness/.../file.md` | add / modify / delete | 一句话说明 |

# Decisions Made (D-prefixed list)
- D1: [决策内容]
- D2: [决策内容]
- D3: [决策内容]

# Patterns Observed (P-prefixed list, future rule 候选)
- P1: [pattern 内容 + 为什么重要]
- P2: [pattern 内容]

# Open Questions (Q-prefixed list)
- Q1: [未解 / 待 follow-up]
- Q2: [...]

# Cross-References
- entities: [entity-id-1, entity-id-2]    # 关联 11-knowledge graph entities
- decisions: [MEMORY-PROJECT.md § N]      # 关联项目记忆
- skills: [skill-name-1]                   # 关联技能

# Tags
- relevant-tags: #tag1 #tag2
```

---

## 实际填法（举例）

```markdown
---
session_date: 2026-07-05
session_topic: "Lovart KB ranking 算法 + canonical URL boost"
session_slug: "kb-ranking-tune"
profiles_used: [profile-lovart-management]
tools_used: [kb-mine, kb-frontmatter, build-index, dream-audit]
agents: [hermes]
duration_min: 90
files_changed_count: 8
schema_bumps: 0
status: ready
---

# Context
- 上一轮发现 Lovart Docs/ 是真权威、Archive 是已下线 → KB 拆分 clean / legacy
- 但 kb-mine 排名偏 NewHelpCenter 跨提及的"小文件"，Archive canonical 反而不到 top 5
- 这次想验证 canonical-url boost 是否让 Archive 在具体 topic query 时仍可见

# Solution
加 canonical-url boost +4.0 到 kb-mine score 函数；凡是 source_urls 含有 /docs/<section>/<topic> 形式的 KB-doc 享受 boost

# Files Changed
| 路径 | 操作 |
|------|------|
| 1-2 Insight/Knowledge Base/scripts/kb-mine.py | modify |
| 1-2 Insight/Knowledge Base/scripts/kb-frontmatter.py | modify (PATH_RULES + extract_canonical_url) |
| 1-1 Harness/11-knowledge/entities.yaml | modify (concept-loop-engineering + skill-lovart-quality-cascade) |
| 1-2 Insight/Knowledge Base/KB-SCHEMA.md | modify |
| 1-2 Insight/Knowledge Base/Changelog/www-*.md | delete (26 needs-rerender) |

# Decisions Made
- D1: Archive 21 篇降级为 legacy-archive (auth=2, quality=legacy-archive)
- D2: New Help Center 17 篇升为 hand-curated-official (auth=5)
- D3: canonical-url boost = +4.0 (弥补 Archive authority 缺口)

# Patterns Observed
- P1: Lovart 网站 = Next.js + Mantine；curl 抓的 HTML 必有 CSS var + JS escape
- P2: KB-doc 大文件占优排名（auth=3 KB-V8 跨提及 > auth=5 small file）
- P3: parse() 用 regex 不会拿 list 值，KV.findall 只能拿 scalar
- P4: Chinese tokenizer 缺失（kb-mine 不分中文）

# Open Questions
- Q1: Archive 的 Tools/* 内容何时真下线？（Lovart 网站 /docs/tools/ 还能访问吗？）
- Q2: 何时可接 Playwright 重抓剩余 needs-rerender？
- Q3: Lovart 何时可能出 dev-docs API？

# Cross-References
- entities: ds-knowledge-base, skill-lovart-quality-cascade, concept-loop-engineering
- decisions: MEMORY-PROJECT.md § 12 (KB cleanup event)
- skills: lovart-kb-mine, lovart-kb-ingest, lovart-dream-orchestrator
```

---

## 写入规则

1. **路径**：`1-1 Harness/11-knowledge/sessions/{YYYY-MM-DD}-{slug}.md`
2. **slug**：用 kebab-case 简述主题，例如 `kb-ranking-tune`, `cascade-v0.2-orchestrator`, `dream-audit-cleanup`
3. **frontmatter 必填字段**：`session_date`, `session_topic`, `session_slug`, `profiles_used`, `tools_used`, `agents`, `status`
4. **status 生命周期**：`draft` → `ready` → `reviewed` (when user actually reads) → `archived` (when pattern promoted)
5. **不要重复**：cross-references 引用 entity id / memory section / other session，不重复内容
6. **轻量化**：每个 session log ≤ 80 行（agent 的 hard cap）

---

## 与 dream/audit 的关系（Layer 2 准备）

`dream/reflect.sh`（下周实现）会：
- 每周扫 sessions/*.md
- 抽 `Patterns Observed` 段落，每个 P# 计数
- 写入 `audit/recurring-patterns/{YYYY-QW}.md`
- 当某 P# 出现 ≥ 2 次 → 标记"rule candidate"，进入 PR workflow

---

## 修改方式

不要手动改这个模板文件。要改 schema：
1. 改本文件
2. 改 `1-1 Harness/Skills/06-orchestrate/lovart-session-log/SKILL.md` 中引用本文件的段落
3. 写一个 session log 记录 schema 变化