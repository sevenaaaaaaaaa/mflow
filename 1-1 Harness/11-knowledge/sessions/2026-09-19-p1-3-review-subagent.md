---
session_date: 2026-09-19
session_topic: "P1-3 审阅子代理：只判断不动笔，带依据、只收紧（根除历史痛点）"
session_slug: "p1-3-review-subagent"
profiles_used: [profile-lovart-management]
tools_used: [console.py, console.html, docs/p1-plan.md, ego-browser, deploy/sync.sh]
agents: [opencode]
duration_min: 120
files_changed_count: 4
schema_bumps: 0
status: ready
---

# Context
- 用户强调子代理审阅"非常重要"，并陈述历史痛苦：子代理**没有上下文**、**不遵守 skills**、**掺水**、**乱改**。
- 设计结论：审阅子代理不应是"会写内容的 agent"，而应是**只判断、不动笔的闸门**——从机制上杜绝掺水/乱改。

# Solution
**审阅子代理 `review_spec()`（REVIEW_SYS）**，四条硬约束直指痛点：
1. **上下文共享**：与规划器同源注入 —— 会话目标 + 用户原话 + 待审 spec（含 items 示例/expand）+ 相关 skills + 项目记忆 + harness 规则 + 知识库命中。
2. **必须引用依据**：每条意见须引 `RULES-xx` / `skill <名>` / `记忆<§>`，无依据不得提；禁止主观文风建议。
3. **只判断不动笔**：明确禁止修改/续写/重写任何内容。
4. **只能收紧**：`revise` 时只允许 dry_run=true、缩小 expand.limit、补必填参数（`safe_spec`），**绝不改语义、绝不放宽**；`block` 时在 `/api/agent/execute` 拦截，需 `ack_review` 二次确认。不确定即 pass，最多 3 条，失败 fail-open。

**集成**：`/api/agent/chat` 生成 spec → 审阅 → `revise` 自动收紧（`applied_notes`）→ 返回 `review`；会话级开关 `/api/agent/review`（默认开）。
**UI**：spec 卡显示 🛡 结论（通过/已收紧/阻断）+ 逐条理由与依据；block 禁用执行并出现「我已了解风险」。

**附带修复**：规划器 JSON 被 max_tokens 截断导致解析失败（提高至 2600 + 无正则依赖的 `say` 抢救）。

# Files Changed
| 路径 | 操作 | 备注 |
|------|------|------|
| `1-4 Dev/console/console.py` | modify | REVIEW_SYS / review_spec / chat 集成 / execute block 拦截 / review 开关 / JSON 截断兜底 |
| `1-4 Dev/console/console.html` | modify | 审阅徽标与理由 / block 禁用+确认 / 审阅开关 |
| `docs/p1-plan.md` | modify | P1-3 标记完成 |

# Decisions Made
- D1: 审阅器**永不产出内容**——这是根除"掺水/乱改"的根本机制，而非靠提示词劝阻。
- D2: **只能收紧不能放宽**，且收紧动作自动应用（用户不必手改）。
- D3: fail-open（审阅失败不阻塞），避免子代理本身成为新的死路。
- D4: 意见必须可追溯（规则/记忆/技能），使审阅可被人工复核。

# Patterns Observed
- P1: 子代理"乱改"的根因是给了它写权限；**剥夺写权限 + 只给判断权**即可根治。
- P2: 子代理"没上下文"要用同一套 context 构建器（skills/rules/memory/KB），而非另起提示词。
- P3: 长 JSON 输出会被 max_tokens 截断 → 解析失败；需提高额度 + 无损抢救关键字段（正则引号转义在多层脚本里极易被吞，改用字符串扫描更稳）。
- P4: 审阅结论若为 block，执行层必须二次确认（否则前端禁用形同虚设）。

# Open Questions
- Q1: 是否把同一审阅机制用于"生成内容"的事前审阅（当前只审 spec，避免越界写内容）？
- Q2: 是否把审阅结论沉淀到 run/audit，形成质量门报告？
- Q3: 是否支持"自定义审阅规则集"（按站点/项目）？

# Cross-References
- entities: ds-console-agent
- decisions: docs/p1-plan.md
- related sessions: 2026-09-19-p1-1b-memory-review-ui.md

# Tags
- relevant-tags: #p1-3 #subagent #review #guardrail #no-content-write #dry-run
