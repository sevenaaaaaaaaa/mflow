---
session_date: 2026-09-20
session_topic: "MCP HTTP/SSE 传输 + automations 硬闸 + 剧本试运行预览"
session_slug: "mcp-http-limits-preview"
profiles_used: [profile-lovart-management]
tools_used: [console.py, console.html, docs/p1-plan.md, deploy/sync.sh]
agents: [opencode]
duration_min: 100
files_changed_count: 3
schema_bumps: 0
status: ready
---

# Context
- 继续自包含项：MCP 远程传输（更开放）、自动化同款硬闸（一致性）、编辑器试运行（更易用/可定制）。

# Solution
1. **MCP HTTP 传输**：`mcp_handle()` 承载 JSON-RPC（initialize / tools/list / tools/call / ping，protocolVersion 2025-06-18）；`POST /api/mcp`（token 或会话）；`GET /api/mcp/sse`（endpoint 事件 + 6×5s 心跳，兼容旧 SSE，且有界不占线程）。stdio 版保留。实测 tools/list=17、initialize=serverInfo/2025-06-18、SSE 收到 endpoint。
2. **automations 硬闸**：与剧本一致的 `limits{max_runs_per_day,max_concurrent,cooldown_min}`，`automation_run` 内统一校验 + `runs_today/day` 计数；列表展示硬闸与今日次数。实测：首跑成功、立即再跑被冷却拦截。
3. **剧本试运行预览**：`playbook_preview()` 逐步 `preset_expand`（无副作用）→ 每步 type/将处理条数/样例/note/错误 + 总条数与硬闸；编辑器加「试运行预览」按钮，结果渲染在抽屉。实测：QA 剧本 total=100（QA扫描 50 + 字段修复 50）。

# Files Changed
| 路径 | 操作 | 备注 |
|------|------|------|
| `1-4 Dev/console/console.py` | modify | mcp_handle + /api/mcp + _send_sse_mcp + automations 硬闸 + playbook_preview/端点 |
| `1-4 Dev/console/console.html` | modify | 编辑器试运行按钮与预览渲染 + 自动化硬闸展示 |
| `docs/p1-plan.md` | modify | 追加三项 |

# Decisions Made
- D1: MCP 同时提供 stdio 与 HTTP 两种传输（本地/远程皆可），HTTP 用同一 JSON-RPC 处理器保证行为一致。
- D2: SSE 采用有界心跳（30s 关闭），避免长连接占满线程；推荐用 POST /api/mcp。
- D3: 预览必须"零副作用"（只展开不建任务），否则预览本身会污染队列。

# Patterns Observed
- P1: 多传输复用同一 JSON-RPC 处理器，可避免 stdio/HTTP 行为漂移。
- P2: 硬闸应在"每个执行入口"统一实现；automations 与 playbook 各有一套，需并行维护。
- P3: 试运行预览是"敢用"的关键——先看要动多少条，再决定跑不跑。

# Open Questions
- Q1: 是否把 automations 与 playbook 合并为同一"定时工作"模型以消除重复？
- Q2: MCP 是否要按 client 维度限速/审计？

# Cross-References
- decisions: docs/mcp.md, docs/p1-plan.md
- related sessions: 2026-09-20-playbook-limits-editor.md

# Tags
- relevant-tags: #mcp #http #sse #automation #limits #preview
