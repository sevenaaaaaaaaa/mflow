---
session_date: 2026-09-20
session_topic: "MCP 开放接入 + 自进化闭环(learnings) + OPC 一键 + 系统配额豁免修复"
session_slug: "mcp-open-selfevolve-opc"
profiles_used: [profile-lovart-management]
tools_used: [console.py, console.html, mcp_server.py, docs/mcp.md, deploy/sync.sh]
agents: [opencode]
duration_min: 140
files_changed_count: 5
schema_bumps: 0
status: ready
---

# Context
- 用户方向：更易用 / 更敏捷 / 更自我进化 / 更 AI Agent / 更 AI Native / 更开放 / 更可定制 / 更兼容 / 面向生态伙伴·开发者·AI 爱好者 / OPC。
- 本轮一次打多维度：**开放（MCP）**、**自进化闭环**、**OPC 开箱即用**。

# Solution
1. **MCP 服务（开放/兼容/面向开发者与 AI 爱好者）**：`mcp_server.py` 纯标准库 stdio JSON-RPC（initialize / tools/list / tools/call）；17 个工具（健康/自检/收件箱/内容检索/知识库/语义检索/回忆/任务/执行/自动化/剧本/URL 检查/报告 + `run_preset`/`run_playbook` **强制 dry-run**）。端点 `GET /api/mcp/tools`、`POST /api/mcp/tool`（token 或 admin；无 token 401）。文档 `docs/mcp.md` + 设置页「开放接入」卡。
2. **自进化闭环**：`learn_from_failures` 已产出学习项；新增 `POST /api/learnings/apply|ignore`；`learning_apply` 复用 `self_evolve_apply`（提示词提示/禁用词），**review 类拒绝自动应用**（不盲自动化）。UI 在「自我迭代」页学习卡。
3. **OPC 开箱即用**：`POST /api/playbooks/enable_recommended` 一键安装并启用 4 个推荐剧本；自动化页按钮。
4. **关键修复（系统自卡死）**：系统执行者（schedule/automation/mcp/playbook/onboard/selfheal/system）此前按普通用户计配额，被默认 500 条上限打满 → health=bad 且自动化被自身配额拒绝。现 `quota_check` 对系统执行者豁免；health 不计入系统侧配额告警。实测 health 由 bad → ok。
5. 实测：MCP initialize/tools/list(17)/tools/call ✓；无 token 401 ✓；OPC 一键启用 → 4 剧本均启用 ✓；learnings apply 对 review 项拒绝 ✓。

# Files Changed
| 路径 | 操作 | 备注 |
|------|------|------|
| `1-4 Dev/console/console.py` | modify | MCP_TOOLS/mcp_tool + /api/mcp/* + /api/open/status + learning_apply/set + playbooks_enable_recommended + SYSTEM_ACTORS 配额豁免 + health 过滤 |
| `1-4 Dev/console/console.html` | modify | 学习卡(应用/忽略) + OPC 按钮 + 开放接入卡 |
| `1-4 Dev/scripts/mcp_server.py` | add | MCP stdio 服务（纯标准库） |
| `docs/mcp.md` | add | MCP 接入文档 |
| `deploy/sync.sh` | modify | 同步 mcp_server.py |

# Decisions Made
- D1: MCP 只开放**只读 + dry-run 动作**；写生产库必须真人会话（安全边界不破）。
- D2: 学习项分"可自动应用"与"需人工复核"，后者拒绝自动执行。
- D3: 系统内部执行者不计入用户配额（否则自动化自我卡死）。
- D4: MCP 用 stdio（本地同机），不额外暴露网络端口。

# Patterns Observed
- P1: 内部自动化必须与"用户配额"解耦，否则规模化后必然自锁。
- P2: 开放接口要把"危险动作"在设计层排除（白名单 + 强制 dry-run），而非靠文档约定。
- P3: MCP 协议用纯标准库即可实现（JSON-RPC over stdio），无需引入依赖。

# Open Questions
- Q1: 是否暴露 HTTP (SSE) 传输的 MCP，供远程客户端？
- Q2: 是否给 MCP 单独的角色/权限（区别于机器 token）？
- Q3: learnings 是否要自动应用到"提示词提示"（低风险）以进一步减人工？

# Cross-References
- decisions: docs/p1-plan.md, docs/mcp.md
- related sessions: 2026-09-20-selfheal-evolve-agile.md

# Tags
- relevant-tags: #mcp #open #developers #self-evolve #opc #quota-fix
