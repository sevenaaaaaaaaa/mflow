---
session_date: 2026-09-20
session_topic: "事故：剧本定时触发器每 5s 重复触发（last_run 未持久化）——修复与防抖"
session_slug: "playbook-runaway-incident"
profiles_used: [profile-lovart-management]
tools_used: [console.py, deploy/sync.sh]
agents: [opencode]
duration_min: 40
files_changed_count: 2
schema_bumps: 0
status: ready
---

# Context
- OPC「一键启用推荐剧本」后，观察到 13 个重复批量任务、pending 555，health 一度 bad/warn。

# Root cause
- `playbook_run` 结束时调用 `playbook_save({"id":..., "last_run":..., "last_run_id":...})` 记录运行时间；
- 但 `playbook_save` 开头校验 `if not pb.get("name"): return {"error": "缺 name"}` → **纯运行态更新被拒**；
- 于是 `last_run` 从未落盘 → `playbook_tick` 每个周期（5s）都判定"到期未运行" → **重复触发**（每日 QA 剧本每次生成 QA扫描+字段修复各 50 项）。

# Fix
1. 新增 `playbook_patch(pid, fields)`：局部更新不校验 name/steps；`playbook_run` 改用它写 last_run。
2. `playbook_save` 兼容：有 id 无 name 时按 merge 处理（启停/运行态）。
3. `playbook_tick` 增加**最小间隔 10 分钟**防抖。
4. 清理：取消 11 个重复任务（按 type+title 去重）；等待在跑的确定性任务排空。
5. 顺带修复：系统执行者（schedule/automation/mcp/playbook）配额豁免（此前被默认 500 条打满，health=bad 且自动化会被自身配额拒绝）。

# Verification
- last_run 已落盘（12:00）；40s 观察活跃任务数稳定不增长；pending 555 → 0；health ok。
- MCP/OPC/learnings 功能均正常。

# Files Changed
| 路径 | 操作 | 备注 |
|------|------|------|
| `1-4 Dev/console/console.py` | modify | playbook_patch/playbooks_save_all + save 兼容 + tick 防抖 + SYSTEM_ACTORS 配额豁免 |

# Decisions Made
- D1: 任何"定时/事件触发器"必须持久化"上次执行时间"，并在触发前校验最小间隔——双保险。
- D2: 系统内部执行者与用户配额解耦。

# Patterns Observed
- P1: **定时器 + 未持久化的 last_ts = 无限重复触发**；必须有防抖兜底。
- P2: `save` 与 `patch` 语义要分开；用带校验的 save 做局部更新会静默失败。
- P3: 规模化自动化会把"用户配额"变成自锁开关，内部执行者必须豁免。

# Open Questions
- Q1: 是否需要"单剧本并发上限/每日次数上限"的硬闸？

# Cross-References
- related sessions: 2026-09-20-playbook-automation.md, 2026-09-20-mcp-open-selfevolve-opc.md

# Tags
- relevant-tags: #incident #playbook #scheduler #debounce #quota
