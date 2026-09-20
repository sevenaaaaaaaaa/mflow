---
session_date: 2026-09-20
session_topic: "剧本硬闸（防再犯）+ 可视化编辑器 + 僵尸 run 回收"
session_slug: "playbook-limits-editor"
profiles_used: [profile-lovart-management]
tools_used: [console.py, console.html, docs/p1-plan.md, ego-browser, deploy/sync.sh]
agents: [opencode]
duration_min: 120
files_changed_count: 3
schema_bumps: 0
status: ready
---

# Context
- 用户要求优先做：① 剧本可视化编辑；⑭ 单剧本并发/每日次数硬闸（把上轮"重复触发事故"的经验前置为护栏）。

# Solution
1. **单剧本硬闸**：`limits{max_runs_per_day,max_concurrent,cooldown_min,max_steps}`（默认 50/2/5/12，可编辑）；`playbook_limits_check()` 覆盖**手动/定时/事件**全部触发路径；被拦时 `webhook_emit("playbook.blocked")` 并返回明确原因；运行成功累加 `runs_today/day`。
2. **僵尸 run 回收**：`run_gc()` —— >30 分钟 running 且其批量任务都不在 running/queued → 标记 failed 并注明"执行器未跟进，已回收"；执行器每 5 分钟巡检。实测回收 11 个僵尸 run（正是它们占满并发导致硬闸误拦）。
3. **可视化编辑器**（抽屉）：名称/图标/说明/启停/dry-run；**触发器**（手动/定时每天每周/事件+match JSON）；**硬闸三项**；**步骤**支持 **HTML5 拖拽 + ↑↓ 两种排序**、类型下拉（预设/规格 JSON/条件/验证）、预设下拉 + opt JSON、条件表达式 + on_false、verify urls；列表卡片显示硬闸与今日已跑次数。
4. 实测：编辑器渲染 4 步 + 触发器 + 硬闸；重复运行被"并发已达上限"正确拦截；run_gc 后恢复可运行。

# Files Changed
| 路径 | 操作 | 备注 |
|------|------|------|
| `1-4 Dev/console/console.py` | modify | 硬闸 + run_gc + run_list.playbook + 运行计数 |
| `1-4 Dev/console/console.html` | modify | 剧本可视化编辑器（拖拽/排序/类型化字段/触发/硬闸）+ 列表硬闸展示 |
| `docs/p1-plan.md` | modify | 追加硬闸与编辑器 |

# Decisions Made
- D1: 硬闸做在 `playbook_run` 内（单一入口），所有触发器自动受控。
- D2: 被硬闸拦截也要发事件（可观测），而非静默拒绝。
- D3: 僵尸 run 必须回收，否则"并发"类硬闸会被永久占用。
- D4: 编辑器排序同时提供拖拽与 ↑↓（拖拽不可用时仍可操作）。

# Patterns Observed
- P1: 引入"并发上限"类护栏前，必须先保证有**僵尸回收**，否则护栏会变成永久死锁。
- P2: 触发路径统一收敛到单一执行入口，护栏才可靠。
- P3: 可视化编辑器对"可定制化"是决定性的：改 JSON 的门槛 vs 点选/拖拽。

# Open Questions
- Q1: 是否给自动化（automations）也加同样的硬闸？
- Q2: 编辑器是否需要"试运行（dry-run 预览）"按钮？

# Cross-References
- related sessions: 2026-09-20-playbook-runaway-incident.md

# Tags
- relevant-tags: #playbook #guardrail #visual-editor #run-gc #customization
