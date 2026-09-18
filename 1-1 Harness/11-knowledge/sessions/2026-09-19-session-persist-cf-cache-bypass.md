---
session_date: 2026-09-19
session_topic: "会话持久化 + Cloudflare 缓存旁路（复用 OpenFlow CF 凭证）"
session_slug: "session-persist-cf-cache-bypass"
profiles_used: [profile-lovart-management, profile-openflow-management]
tools_used: [console.py, deploy/sync.sh, deploy/cf.env, CF rulesets API]
agents: [opencode]
duration_min: 45
files_changed_count: 3
schema_bumps: 0
status: ready
---

# Context
- 上一轮发现两个稳定性/安全问题：① SESSIONS 存内存，每次部署重启都会踢下线所有用户；② CF 有一条 zone 级缓存规则「Cache Dynamic HTML for Anonymous Visitors」按 `PHPSESSID` 判断匿名，而 MFlow 用 `mflow_session`，导致 MFlow 页面被边缘缓存（含已登录控制台页，存在越权/隐私风险，且部署后看到旧页）。
- 用户指示：持久化会话可以；CF 凭证在 OpenFlow 项目里有。

# Solution
1. **会话持久化**：`run/sessions.json`（60 天 TTL），登录/登出/切项目时 `sessions_save()`；模块加载时 `_sessions_load()` 过滤过期。`.gitignore` 排除 sessions.json / sessions.log / llm-status.json / breaker.json / quotas.json / modes.json。
2. **CF 凭证复用**：从 OpenFlow 的 `data/cloudflare.json` 取 token/zone，写入 MFlow `deploy/cf.env`（git-ignore）。
3. **缓存旁路**：定位到 ruleset `e1d4b108...` 的 catch-all 规则，在表达式追加 `and not starts_with(http.request.uri.path, "/mflow")`，经 CF rulesets API PUT 生效。现 `/mflow/` 返回 `cf-cache-status: DYNAMIC`（不再 HIT）。
4. **sync.sh 增强**：CF purge 列表补齐 `index.html` / `console.html`，修正原先 `$SITE_URL/` 产生的 `//` 双斜杠。

# Files Changed
| 路径 | 操作 | 备注 |
|------|------|------|
| `1-4 Dev/console/console.py` | modify | SESSIONS 持久化 + TTL + login/logout/switch 保存 |
| `deploy/sync.sh` | modify | CF purge URL 列表修正（去尾斜杠 + index/console） |
| `deploy/cf.env` | add (ignored) | 复用 OpenFlow 的 CF token/zone（nownexts.com） |
| `.gitignore` | modify | 排除 sessions.json / sessions.log / 运行时状态 |

# Decisions Made
- D1: 会话 TTL 60 天，过期自动清理，避免文件无限增长。
- D2: CF 缓存旁路优先改 catch-all 表达式（最小侵入，不动其他规则与顺序）。
- D3: 凭证不入 git（cf.env/sessions.json 均 ignore）。

# Patterns Observed
- P1: 跨项目复用 CF 凭证可行——OpenFlow `data/cloudflare.json` 的 token 同时具备 Purge 与 Rulesets 读写权限。
- P2: 共享 zone 上按 `PHPSESSID` 判断匿名的缓存规则会误伤用自定义 cookie 名的应用（MFlow/可能的其他子应用）。新增子应用时须同步加旁路。
- P3: CF "Cache Everything" 会忽略 origin 的 `cache-control: no-store`，必须用 Cache Rules 显式 bypass。

# Open Questions
- Q1: zone 里是否还有其他同样按 PHPSESSID 判断的规则会影响未来子应用？（当前仅此一条 catch-all）
- Q2: 是否把 sessions.json 加进 housekeeping 的清理范围？

# Cross-References
- entities: ds-console-auth, ds-cloudflare-cache
- decisions: MEMORY-PROJECT.md § Console Auth
- related sessions: 2026-09-19-agent-v2-unified-context-nav-ux.md

# Tags
- relevant-tags: #auth #session #cloudflare #cache #deploy
