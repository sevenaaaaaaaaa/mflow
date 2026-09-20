---
session_date: 2026-09-20
session_topic: "自动化剧本 Playbook：多步 + 条件 + 触发器（自动化与自我进化核心）"
session_slug: "playbook-automation"
profiles_used: [profile-lovart-management]
tools_used: [console.py, console.html, templates/playbooks.json, ego-browser, deploy/sync.sh]
agents: [opencode]
duration_min: 120
files_changed_count: 4
schema_bumps: 0
status: ready
---

# Context
- 用户方向：让 MFlow 更好用、更智能、更自我进化、更自动化。选定首个落地项：把"定时单步自动化"升级为**剧本（Playbook）**——多步 + 条件 + 失败处理 + 触发器，执行走 Run 画布（可视、可恢复）。

# Solution
1. **剧本模型** `run/playbooks.json`：`{id,name,icon,desc,dry_run,enabled,trigger,steps[]}`；
   - 步骤类型：`preset`（预设展开）/`spec`（直接规格）/`guard`（条件）/`verify`（前台验证）。
   - 触发器：`schedule`（daily/weekly + at）/`event`（如 task.done 匹配 type）/`manual`。
2. **条件步骤 `guard`**：极简安全求值 `VAR op NUM`（`findings>0`、`failed==0` 等）；变量由前序步骤真实产出聚合（findings/suggestions/done/failed/total/skipped）；`on_false: stop|continue`。
3. **执行复用 Run 引擎**：`playbook_run` → `run_new`（kind=playbook），由 `run_tick` 逐步执行，画布可见、可取消/重试；完成后触发 webhook `playbook.run`。
4. **触发器接线**：`playbook_tick()` 挂入执行器循环（定时）；`playbook_event()` 挂在任务终态（事件）。
5. **模板库** `templates/playbooks.json` 6 个：每日 QA 闭环、每周衰减刷新、每周 alt 补齐、每周 GEO 缺口、事件-QA 完成即修复（默认停用）、落地页闭环。
6. **UI**：自动化页新增「自动化剧本」卡（列表 + 步骤链 + 触发器 + 运行/启停/删除 + 看画布；模板库一键添加）。
7. 实测：添加「每日 QA 闭环」→ 运行 → Run 4 步：QA 扫描 50/50 → **条件 findings>0 成立** → 字段修复 50/50 → 验证 → status=done 100%。
8. 修复两处：`run_new` 丢失 `expr/on_false`（guard 失效）；完成判定改了状态未置 `changed`（结果不落盘，run 永远 running）。

# Files Changed
| 路径 | 操作 | 备注 |
|------|------|------|
| `1-4 Dev/console/console.py` | modify | playbooks 存储/CRUD/run/tick/event + guard 执行 + run_new 字段 + 完成落盘 + 端点 |
| `1-4 Dev/console/console.html` | modify | 自动化页「剧本」卡 + 模板库 |
| `templates/playbooks.json` | add | 6 个剧本模板 |

# Decisions Made
- D1: 剧本不新造执行器——复用 Run 引擎，天然获得画布、心跳、重规划、交付物。
- D2: 条件求值只支持 `VAR op NUM`，安全且可解释，不引入表达式引擎。
- D3: 模板默认 dry-run；事件型默认停用，避免误触发。
- D4: 剧本与 webhook 打通（playbook.run 事件），外部系统可监听。

# Patterns Observed
- P1: 新建步骤类型必须同步检查 `run_new` 的字段白名单，否则字段被静默丢弃。
- P2: "改了状态但没置 changed"是后台状态机的经典陷阱——完成态必须强制落盘。
- P3: 条件步骤让自动化从"堆任务"变成"有判断的流程"，这是自进化的基础。

# Open Questions
- Q1: 是否需要分支（if/else 多路）而非仅 stop/continue？
- Q2: 是否支持步骤级重试策略与超时？
- Q3: 剧本编辑是否要可视化（拖拽步骤）而非 JSON？

# Cross-References
- decisions: docs/p1-plan.md
- related sessions: 2026-09-19-empty-cta-mobile-webhook.md

# Tags
- relevant-tags: #automation #playbook #orchestration #condition #event-driven
