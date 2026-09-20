---
session_date: 2026-09-20
session_topic: "剧本分支 if/else（前向 goto）+ 步骤级重试/超时"
session_slug: "playbook-branch-retry"
profiles_used: [profile-lovart-management]
tools_used: [console.py, console.html, templates/playbooks.json, test_console_units.py, deploy/sync.sh, ego-browser]
agents: [cursor]
duration_min: 80
files_changed_count: 5
schema_bumps: 0
status: ready
---

# Context
- 用户说「继续」，按既定顺序落地剧本智能两项：分支（if/else 多路）与步骤级重试/超时。

# Solution
1. **前向分支**：步骤 `id` + `on_true`/`on_false`/`next` 取值 `next|stop|goto:ID`。未走分支标 `skipped`；禁止回跳以防死循环。旧 `continue` 兼容为 `next`。
2. **步骤级重试**：`retry_max`（0–5）+ `retry_delay_sec`。失败先排队重试（重置关联批量任务），用尽才走 run_replan/阻断。
3. **步骤级超时**：`timeout_min`（0=不限）。超时取消关联批量任务，可再进重试。
4. **编辑器**：每步可配 id、跳转、重试/间隔/超时；试运行预览显示将跳过的步骤。
5. 模板「每日 QA 闭环」改为无发现 → 跳过修复、仍验证。已装剧本不自动改（避免覆盖用户配置）。
6. 实测：39 单测绿；线上编辑器可见成立/不成立/完成后跳转；预览 `goto:verify` 只跳过「修复」；回跳保存被拒。

# Files Changed
| 路径 | 操作 | 备注 |
|------|------|------|
| `1-4 Dev/console/console.py` | modify | 分支/重试/超时执行 + 保存校验 + 预览 |
| `1-4 Dev/console/console.html` | modify | 编辑器跳转与重试/超时 + 画布 skipped |
| `1-4 Dev/tests/test_console_units.py` | modify | 11 个分支/重试/超时用例 |
| `templates/playbooks.json` | modify | 每日 QA 闭环演示分支 |
| `docs/p1-plan.md` | modify | 勾掉该后续项 |

# Decisions Made
- D1: 只用前向 goto，不用嵌套步骤树——保持线性编辑、可解释、防死循环。
- D2: 重试发生在 run_replan 之前，避免 LLM 自愈抢在步骤重试前面。
- D3: 已安装剧本不随模板迁移，用户在编辑器里改跳转即可。

# Patterns Observed
- P1: 定时/条件跳转必须禁止回跳，否则与 last_run 事故同类（无限循环）。
- P2: 重试等待期必须跳过 `_run_sync_steps`，否则失败态会立刻把 pending 打回 failed。
- P3: 预览要标「将跳过谁」，用户才敢配分支。

# Open Questions
- Q1: 已装的「每日 QA 闭环」是否一键升级为 goto:verify？
- Q2: 重试是否要指数退避，还是固定间隔足够？

# Cross-References
- decisions: docs/p1-plan.md
- related sessions: 2026-09-20-playbook-automation.md, 2026-09-20-playbook-limits-editor.md

# Tags
- relevant-tags: #playbook #branch #retry #timeout #if-else
