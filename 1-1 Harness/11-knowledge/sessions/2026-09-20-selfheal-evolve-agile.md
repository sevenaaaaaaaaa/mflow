---
session_date: 2026-09-20
session_topic: "自愈、失败→学习、命令面板收藏/最近、全局快捷键"
session_slug: "selfheal-evolve-agile"
profiles_used: [profile-lovart-management]
tools_used: [console.py, console.html, docs/p1-plan.md, ego-browser, deploy/sync.sh]
agents: [opencode]
duration_min: 120
files_changed_count: 3
schema_bumps: 0
status: ready
---

# Context
- 用户方向：自愈 + 自进化 + 更易用 + 更敏捷。

# Solution
1. **自愈**：`selfcheck_autofix()` 对自检中带 `api:` 安全动作的项自动执行（熔断解除/卡住任务恢复/维护/RAG 重建/失败重试）；`selfheal_tick()` 挂入执行器循环（每 120 轮 ≈ 10 分钟静默自愈，仅白名单安全动作）；自检新增「RAG 索引未构建」项。端点 `POST /api/selfcheck/autofix`（写操作走 POST）。
2. **失败→学习（自进化）**：`learn_from_failures(days)` 扫描近期批量任务失败，按类别聚合并给出建议动作（internal→提示词提示、structure→强化结构、timeout/rate→降低并发、no_data→调范围），落 `run/learnings.json`；`POST /api/learnings/scan`、`GET /api/learnings`。
3. **更易用/敏捷**：命令面板 **★收藏 + 最近使用**（localStorage，空查询置顶）；**全局快捷键**（⌘K 或 `/` 开面板、`?` 帮助、`g+字母` 11 条导航、Esc 关闭）；**帮助浮层**；顶栏加 `?` 入口。
4. 实测：`?` 弹帮助（12 条）✓；`g i` → 收件箱 ✓；面板空查询显示收藏/最近 ✓；自愈端点返回 skipped(需人工) ✓；失败学习扫描产出 1 条 ✓。

# Files Changed
| 路径 | 操作 | 备注 |
|------|------|------|
| `1-4 Dev/console/console.py` | modify | selfcheck_autofix/_selfcheck_apply_fix/selfheal_tick + learn_from_failures/learnings + RAG 自检项 + 端点 |
| `1-4 Dev/console/console.html` | modify | 快捷键/帮助浮层/面板收藏最近 |
| `docs/p1-plan.md` | modify | 追加三类进展 |

# Decisions Made
- D1: 自动自愈只做**白名单安全动作**（熔断/卡住/维护/索引），其余仅提示人工。
- D2: 失败学习只产出**建议**，应用仍走既有 `self_evolve_apply`（可追溯）。
- D3: 快捷键 `g+字母` 两段式，避开输入框（typing 时不触发）。

# Patterns Observed
- P1: 状态变更端点必须走 POST（GET 会被权限/白名单逻辑挡成 not found）。
- P2: "自愈"必须限定白名单，否则自动动作可能放大问题。
- P3: 快捷键要判断输入焦点，否则打字即误触。

# Open Questions
- Q1: learnings 是否要在 UI 提供"一键应用"与"忽略"？
- Q2: 自愈是否记录到独立的 heal 日志便于审计？

# Cross-References
- decisions: docs/p1-plan.md
- related sessions: 2026-09-20-playbook-automation.md

# Tags
- relevant-tags: #self-heal #self-evolve #shortcuts #agility #palette
