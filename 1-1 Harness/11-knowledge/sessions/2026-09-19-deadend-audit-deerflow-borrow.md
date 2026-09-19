---
session_date: 2026-09-19
session_topic: "防卡死（系统自检/单条重试/恢复指引）+ 借鉴 DeerFlow 2.0（会话目标/手动压缩/交付物/心跳孤儿恢复）"
session_slug: "deadend-audit-deerflow-borrow"
profiles_used: [profile-lovart-management]
tools_used: [console.py, console.html, webfetch(deer-flow), ego-browser, deploy/sync.sh]
agents: [opencode]
duration_min: 120
files_changed_count: 3
schema_bumps: 0
status: ready
---

# Context
- 用户要求：继续推进，并系统检查"因系统不够智能导致用户断掉使用、无法继续"的情况；借鉴开源 DeerFlow 2.0 编排框架。

# Solution
## A. 防卡死（死路审计与修复）
1. **系统自检 `/api/selfcheck`**：检测 10 类阻断项（LLM 配置/402、Sanity 发布器/token、GSC 数据缺失或过旧、知识库为空、内容库未同步、熔断中、任务卡住、配额≥90%、维护超期、质检阻断过多），每条给人话说明 + 一键修复（`tab:`/`url:`/`api:`）。首页卡片 + 一键执行。
2. **卡住任务恢复**：`batch_revive_stale`（手动一键）+ `batch_recover_orphans`（执行器循环内自动：running 且心跳/文件 >360s 无更新 → 自动重置重跑）；任务新增 `heartbeat_ts`。
3. **单条重试**：`/api/batch/retry_item` —— 一个失败条目不必整任务重跑。
4. **门禁失败修复建议**：详情抽屉按失败门禁（post-write/geo/quota/language/落地页结构/QA）给出"怎么修复" + 「🤖 让 Agent 修复这条」预填提示。
5. **错误消息补恢复指引**：发布器未加载/预设展开为空/Sanity 查询失败/需填 topic/草稿不可读/无物料台账/无替换计划等；权限错误明确"当前角色 + 联系管理员"。

## B. 借鉴 DeerFlow 2.0
- **Session Goals** → 会话级 `goal`，注入每次 LLM 调用（始终对齐），Agent 页可设定/清除。
- **Manual Context Compaction** → `/api/agent/compact` + Agent 页「压缩上下文」按钮（已有自动阈值压缩）。
- **Artifacts/Delivery** → `run_view.deliverables`（草稿/前台链接/发布 id），画布「交付物」区一键打开/预览。
- **Run ownership / lease heartbeat / orphan recovery** → 见 A2（execute-or-recover 语义）。
- 印证：DeerFlow 的 `make doctor` 与本轮 `selfcheck` 同思路；本项目先做轻量版即可。

# Files Changed
| 路径 | 操作 | 备注 |
|------|------|------|
| `1-4 Dev/console/console.py` | modify | selfcheck / revive_stale / recover_orphans / retry_item / 错误恢复指引 / goal / compact / deliverables / 心跳 |
| `1-4 Dev/console/console.html` | modify | 自检卡 + 一键修复 / 抽屉修复建议 / 会话目标 / 压缩按钮 / 画布交付物 |

# Decisions Made
- D1: 自检项只在"会阻断或明显影响使用"时提示，避免噪音（info 级不影响状态灯）。
- D2: 孤儿恢复自动执行（360s 心跳超时），比只做手动更防"静默卡死"。
- D3: 只借 DeerFlow 与本场景契合的部分（目标/压缩/交付物/心跳恢复），不引入其多进程/沙箱/checkpointer 重架构。
- D4: 每条错误尽量自带"下一步"，而不是只抛原始异常。

# Patterns Observed
- P1: 死路多来自"错误只说错、不说怎么办"；统一补恢复指引成本低、收益大。
- P2: 前端模板里拼错变量（`idx` vs `i`）会在 Promise 内静默抛错，整块不渲染——必须端到端验证渲染。
- P3: 后台执行需要显式心跳 + 自动恢复，否则进程中断后任务永久 pending。

# Open Questions
- Q1: 是否做 DeerFlow 式"子代理（planner→reviewer→executor）+ 并发上限"？
- Q2: 是否为 Run 引入心跳可视（最近心跳时间）与更细的 lease 语义？
- Q3: 记忆审阅 UI（Settings > Memory，仿 DeerFlow）是否要排入 P1？

# Cross-References
- entities: ds-console-agent, ds-batch-executor
- external: bytedance/deer-flow (DeerFlow 2.0)
- related sessions: 2026-09-19-p0-memory-context-profiles-replan.md

# Tags
- relevant-tags: #selfcheck #recovery #deerflow #session-goal #context #deliverables #resilience
