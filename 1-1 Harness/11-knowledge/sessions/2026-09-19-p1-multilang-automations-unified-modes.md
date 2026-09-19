---
session_date: 2026-09-19
session_topic: "P1-1 多语言覆盖 + 自动化注册表 + 统一执行方式（四能力自由切换）"
session_slug: "p1-multilang-automations-unified-modes"
profiles_used: [profile-lovart-management]
tools_used: [console.py, console.html, docs/p1-plan.md, ego-browser, deploy/sync.sh]
agents: [opencode]
duration_min: 150
files_changed_count: 4
schema_bumps: 0
status: ready
---

# Context
- 用户要求：开始做 P1；并在过程中彻底提升「创建任务 / 自动化任务 / 任务编排 / Agent 模式」四项能力，使四者可自由切换执行方式（任务与优化并行）。

# Solution
## A. 统一执行方式（本轮核心）
把四类能力统一为"**同一件工作、可自由切换执行方式**"，并补上缺失的第 5 种：**自动化**。
- **自动化注册表** `run/automations.json`：`{id,name,mode:preset|plan|batch|loop,spec,schedule:{daily|weekly|interval},dry_run,enabled,last_run,task_id}`；CRUD + `run`（立即）+ `toggle`；调度器 `automation_tick()` 挂在 batch_worker 循环（每 5s 检查到期，按 daily/weekly/interval 触发）。
- **模式切换** `/api/work/convert`：任意来源 → `to: batch | loop | automation`（agent 由前端跳转）。来源支持 preset / plan / run / batch / task。
- **前端入口**：任务详情、批量详情、执行画布、Agent 计划卡全部挂「⇄ 执行方式」抽屉（转为批量 / 转为 Loop / 存为自动化 / 交给 Agent）；新增「自动化」页面（列表 + 立即运行 + 启停 + 删除）+ nav。
- 复用重构：抽出 `loop_new()` 供 handler 与自动化共用。

## B. P1-1 多语言覆盖盘点与补齐
- `multilang_coverage()` / `multilang_fill()`：以基准语言为参照，统计各语言覆盖与缺口；一键为缺目标语言的页面创建本地化 rewrite 任务（dry-run）。
- UI：内容库「多语言覆盖」卡（每语言 已覆盖/总数 + 「补 N」）。
- 实测：tools 基准 en 385 篇 → de 81 / fr 90 / it 60 / ja 79 / ko 49 / pt 67 / ru 59 / zh 85 / zh-TW 81。

# Files Changed
| 路径 | 操作 | 备注 |
|------|------|------|
| `1-4 Dev/console/console.py` | modify | multilang_coverage/fill · automations(注册表/CRUD/run/tick) · loop_new 抽取 · /api/work/convert |
| `1-4 Dev/console/console.html` | modify | 自动化页 · ⇄ 执行方式抽屉与各入口 · 多语言覆盖卡 |
| `docs/p1-plan.md` | modify | 顶部新增「统一执行方式」章节；P1-1 标记完成 |
| `11-knowledge/sessions/2026-09-19-p1-multilang-automations-unified-modes.md` | add | 本日志 |

# Decisions Made
- D1: 不新造"工作"实体，而是给现有四类能力加"可切换"与"可自动化"两层，降低回归风险。
- D2: 自动化默认 dry-run，真实执行需显式关闭（延续安全铁律）。
- D3: 自动化调度复用 batch_worker 循环（单进程无额外调度器）。
- D4: 多语言补齐用 rewrite（本地化指令）+ 源文件，而非纯生成，保证事实与结构一致。

# Patterns Observed
- P1: 四类能力各自为政的根因是"缺少统一的执行方式抽象"；用"来源→目标"的转换端点即可低成本打通。
- P2: 前端模板里把结尾反引号误写成单引号，会让整段脚本失败且报错位置偏移（指向无关的 href），需 `node --check` 定位。
- P3: zsh 会吞掉内联 Python 字符串里的反引号，写文档/代码需用 quoted heredoc。

# Open Questions
- Q1: 是否给自动化加"运行历史 + 失败通知"（当前仅 last_run/last_task）？
- Q2: 是否支持事件触发（如"某任务完成即触发另一自动化"）？
- Q3: 继续 P1-5 多语言（已完成）→ P1-2 心跳可视化 的顺序是否合适？

# Cross-References
- entities: ds-batch-executor, ds-console-agent
- decisions: docs/p1-plan.md § 统一执行方式
- related sessions: 2026-09-19-onboarding-wizard-inventory-p1.md

# Tags
- relevant-tags: #p1 #multilang #automation #unified-modes #orchestration
