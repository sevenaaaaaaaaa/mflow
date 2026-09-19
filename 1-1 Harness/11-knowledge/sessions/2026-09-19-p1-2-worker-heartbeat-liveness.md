---
session_date: 2026-09-19
session_topic: "P1-2 执行器心跳与 Run 恢复可解释（含离线告警）"
session_slug: "p1-2-worker-heartbeat-liveness"
profiles_used: [profile-lovart-management]
tools_used: [console.py, console.html, docs/p1-plan.md, ego-browser, deploy/sync.sh]
agents: [opencode]
duration_min: 60
files_changed_count: 4
schema_bumps: 0
status: ready
---

# Context
- P1-2：Run 心跳可视化 + 恢复可解释。核心动机：若后台执行器（batch_worker）线程死亡，任务会永久 pending，而用户无从得知——这是最隐蔽的死路。

# Solution
1. **执行器心跳**：worker 每循环写 `run/worker-heartbeat.json`（含 ts/at）；`worker_alive(max_idle=30)` 判断在线与空闲秒数。
2. **健康与自检**：`/api/health` 增 `worker:{alive,idle_sec}`；`selfcheck` 增「执行器不在线」**block** 项（附去「调度与日志」的修复入口）。
3. **liveness 下发**：`batch_view` 每任务输出 `liveness{heartbeat_at,idle_sec,stale,recovered}`；`run_view` 输出 `liveness{worker_alive,worker_idle_sec,recovered}`（跨步骤累加）。
4. **UI**：顶栏常驻执行器状态灯（30s 轮询；离线变红并弹告警，恢复自动复位）；执行画布显示「执行器 在线/离线 + 自动恢复 N 次」，离线且运行中提示"恢复服务后自动继续"；批量详情显示心跳时间/停滞秒/恢复次数。

# Files Changed
| 路径 | 操作 | 备注 |
|------|------|------|
| `1-4 Dev/console/console.py` | modify | worker 心跳 / worker_alive / health.worker / selfcheck worker 项 / batch_view·run_view liveness |
| `1-4 Dev/console/console.html` | modify | 顶栏状态灯 + workerPing / 画布 liveness / 批量详情心跳 |
| `docs/p1-plan.md` | modify | P1-2 标记完成 |

# Decisions Made
- D1: 心跳用独立文件而非任务内字段，便于判断"整个执行器"是否活着（区分"任务慢"与"执行器死"）。
- D2: 执行器离线列为 selfcheck **block**（最高级），因为它会让所有任务停摆。
- D3: 离线告警只弹一次（恢复后复位），避免噪音。

# Patterns Observed
- P1: 需要区分两种停滞——"任务在跑但慢"（心跳正常）与"执行器挂了"（无心跳）；否则用户会误判。
- P2: 大段替换锚点可能命中同名前缀的其它函数（本次 `st = read_json(pp["state"], {})` 误入 `mode_report`），必须验证插入位置而非只看语法通过。

# Open Questions
- Q1: 执行器离线时是否尝试自动重启（launchd/systemd 已负责，应用层只告警）？
- Q2: 是否把"资源占用（CPU/内存）"也纳入 health？

# Cross-References
- entities: ds-batch-executor
- decisions: docs/p1-plan.md
- related sessions: 2026-09-19-deadend-audit-deerflow-borrow.md

# Tags
- relevant-tags: #p1-2 #heartbeat #liveness #resilience #observability
