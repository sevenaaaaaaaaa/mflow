---
session_date: 2026-09-19
session_topic: "失败摘要（按原因归类+建议）+ 一键重试全部失败项"
session_slug: "failure-digest-retry-all"
profiles_used: [profile-lovart-management]
tools_used: [console.py, console.html, docs/p1-plan.md, deploy/sync.sh]
agents: [opencode]
duration_min: 75
files_changed_count: 4
schema_bumps: 0
status: ready
---

# Context
- 可用性第 4 项：失败要给人话摘要与处理建议，并能一键重试全部失败项，而不是让用户翻日志。

# Solution
1. **失败摘要 `failure_digest(task)`**：把失败项按原因归类——缺主题 / 目标文档缺失 / LLM 余额配额 / 数据查询失败 / 结构门禁 / 超时 / 限流 / 范围内无对象 / **系统内部错误（代码异常）** / 其他；每类给 count、样例与人话处理建议；覆盖"任务级异常终止（无逐条错误）"。`batch_view` 附带 `failures`。
2. **一键重试** `batch_retry_all(scope=task|all)`：把 failed 或 pending-with-error 的条目重置为 pending、任务回到 queued；`/api/batch/retry_all`；批量页「重试所有失败项」、批量详情失败摘要卡内按钮、收件箱内联按钮。
3. **修复**：`batch_list()` 不含 `items`，`retry_all` 必须逐个 `batch_load` 全量（否则永远重试 0 项）。
4. 实测：5 个历史卡死任务 → 一键重试 9 项 → 首个 rewrite 任务 2/2 完成（质检通过），验证"卡死→重跑→产出"闭环。

# Files Changed
| 路径 | 操作 | 备注 |
|------|------|------|
| `1-4 Dev/console/console.py` | modify | _categorize_error / failure_digest / batch_retry_all / batch_view.failures / 端点 |
| `1-4 Dev/console/console.html` | modify | 失败摘要卡 + 批量页重试按钮 + 收件箱内联重试 |
| `docs/p1-plan.md` | modify | 标记第 4 项完成 |

# Decisions Made
- D1: 摘要必须给"怎么办"，不能只给错误原文。
- D2: 区分"可重试"（超时/限流/查询/内部错误）与"需先修条件"（缺主题/结构/无对象）。
- D3: 内部代码异常单列一类，明确"多为版本缺陷、重试通常可过，复发请反馈"。

# Patterns Observed
- P1: 任务级失败 ≠ 条目级失败；摘要口径必须同时覆盖两者，否则"有失败却无摘要"。
- P2: 列表接口通常裁剪大字段（items），任何需要明细的批处理都必须重新 load，否则静默 0 操作。

# Open Questions
- Q1: 是否把失败摘要写入收件箱的详情（而非仅一行）？
- Q2: 是否对"可重试"类做自动重试（带次数上限）？

# Cross-References
- decisions: docs/p1-plan.md
- related sessions: 2026-09-19-audit-rollback-inbox.md

# Tags
- relevant-tags: #usability #failure-digest #retry #observability
