---
session_date: 2026-09-19
session_topic: "每日开工体感（开工简报/继续上次）+ 对话画布细节（进度/token/ETA/累积风险）+ 负责人离线邮件通知"
session_slug: "daily-start-etarisk-email-notify"
profiles_used: [profile-lovart-management]
tools_used: [console.py, console.html, smtplib, ego-browser, deploy/sync.sh]
agents: [opencode]
duration_min: 150
files_changed_count: 3
schema_bumps: 0
status: ready
---

# Context
- 用户三点：① 优化每日开启任务体感 + 继续上一轮任务的入口；② 优化对话/画布交互细节（多轮对话要能看到进度、token 消耗、剩余时间、是否有累积风险）；③ 当前任务负责人不在登录态时邮件通知。

# Solution
1. **开工简报 `/api/start`**：返回 greeting / away_hours / last_session（继续上次）/ running_runs / active_batches / overnight（done·failed·reports·maintenance）/ my_tasks / next。按用户记录 `run/start-state.json` 的 last_ts，计算"离开后变化"。首页新增「🌅 欢迎回来（离开 N 小时）」卡片 + 一键「继续上次」回到 Agent 会话；housekeeping 日志人话化（归档 N 项/批）。
2. **画布/对话细节**：
   - 批量任务统计新增 `tokens`（累加各 item 的 `result.tokens`）与 `retries`。
   - `run_view` 新增 `metrics`（items_done/total、tokens、retries、elapsed_sec、**eta_sec**、rate_per_min）与 `risk`（失败/重试/告警/熔断/配额≥80%/长时间无产出 → low/medium/high）。
   - 画布渲染指标行（进度·条目·token·已用·剩余 ETA·重试·速率）+ 风险横幅。
   - Agent 实时任务卡新增 ETA 与 token（已用 Ns · 剩余约 Ns · ⚠ 失败 · 重试）。
3. **离线邮件通知**：`run/email.json`（SMTP：host/port/user/pass/sender/tls + recipients + default_to）。`email_send`（SSL/STARTTLS/none）、`user_email`、`user_online`（查活跃会话 12h 内）。`notify_task_end`：批量任务终态 → 若负责人离线则发邮件（并顺带飞书），写任务日志。`notify_offline` 如实报告 email/feishu 结果。设置页新增「邮件通知」卡片（SMTP + 成员邮箱 + 测试）。
4. **修复**：`write_json` 此前从未定义（llm-status 写入一直静默失败），补上原子写实现；`/api/account/list` 返回 email。

# Files Changed
| 路径 | 操作 | 备注 |
|------|------|------|
| `1-4 Dev/console/console.py` | modify | start_report / run metrics+risk / token&retries 统计 / 邮件层 / notify_task_end / write_json / account email |
| `1-4 Dev/console/console.html` | modify | 开工简报卡片 + 继续上次 / 画布指标+风险 / Agent 任务卡 ETA+token / 邮件设置 UI |

# Decisions Made
- D1: 开工简报以"离开时长 + 变化"为核心，不做成静态欢迎语。
- D2: ETA 用条目吞吐率估算（done/elapsed × remaining），无产出时给"计算中"。
- D3: 风险分级 low/medium/high，聚合失败/重试/熔断/配额/停滞五类。
- D4: 邮件与飞书并存，互相兜底；未配置邮件时仅日志+飞书。
- D5: 只在负责人离线时通知，在线不打扰（避免噪音）。

# Patterns Observed
- P1: 通知类功能必须"如实报告通道结果"，否则用户以为发了其实没发。
- P2: 已定义的配置端点若函数未实现（write_json）会静默失败，需端到端验证而非只看语法。
- P3: 进度/ETA/风险要落在"任务/执行"层（batch/run），而非会话层，才能跨页面共享。

# Open Questions
- Q1: SMTP 凭证需用户提供（设置 → 邮件通知）才能真正发信。
- Q2: 是否要给手动待办也加"到期/指派"邮件提醒？
- Q3: ETA 是否要按批次历史平均（当前用即时速率，早期波动大）？

# Cross-References
- entities: ds-console-agent, ds-batch-executor
- related sessions: 2026-09-19-p0-memory-context-profiles-replan.md

# Tags
- relevant-tags: #daily-start #eta #risk #email #notify #ux
