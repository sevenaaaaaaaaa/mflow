---
session_date: 2026-09-19
session_topic: "P0：Agent 记忆接线 + 会话压缩/上下文可视化 + 角色 Profile + 失败自愈重规划"
session_slug: "p0-memory-context-profiles-replan"
profiles_used: [profile-lovart-management]
tools_used: [console.py, console.html, ego-browser, memory_digest, recall, run_replan, deploy/sync.sh]
agents: [opencode]
duration_min: 150
files_changed_count: 3
schema_bumps: 0
status: ready
---

# Context
- 对比 DeepSeek Harness / Hermes Agent 后定位 5 维差距，用户批准先做 P0：① 记忆接线；② 会话压缩 + 上下文可视化；③ 失败重规划；④ Profile 角色化。
- 核心判断：项目已有 `entities.yaml`(866行) / `MEMORY-PROJECT.md`(746行) / 6 条 Hermes profile / dream 梦境，但线上 Agent 一个都没接。

# Solution
1. **P0-1 记忆接线**：新增记忆层 `_memory_index()`（解析 MEMORY-PROJECT 为 288 条事实，📌 优先，mtime 缓存）、`_entities_index()`（entities.yaml → 98 实体）、`memory_digest()`、`recall()`（跨源：项目记忆 + 图谱 + 历史会话日志 + 执行记录）。注入 `ai_context` 与 agent 系统提示词；新增 `recall` 工具。实测"Sanity 发布铁律"回答引用真实记忆。
2. **P0-2 会话压缩 + 上下文可视化**：`CTX_LIMIT_CHARS=12000`、`session_ctx_chars()`、`session_maybe_compress()`（超限把最旧消息 LLM 摘要为 `session.summary`，保留最近 8 条，失败回退截断）。实测 16170→6719 字符。前端加"上下文占用"进度条 + 摘要提示；`/api/agent/session` 返回 `ctx`。
3. **P0-3 失败自愈重规划**：`run_replan()` —— run 步骤失败时让 LLM 依据错误+已完成+可用预设给出替代步骤（≤3，一次/run），失败步标记 `replanned`，并追加新步骤继续跑。实测：发布失败 → 自动改规划为「QA 扫描 + 产草稿」。
4. **P0-4 角色 Profile**：`AGENT_PROFILES`（auto/creation/quality/reports/ops/distribution/management = 6 条工作线 + 通用），选择后收窄：只注入该线 RULES 文件 + skill_hint + 对应模型 profile。`context_rules(force_files=…)`；新增 `/api/agent/profiles` + `/api/agent/profile`；前端角色选择器；会话持久化 `profile`。

# Files Changed
| 路径 | 操作 | 备注 |
|------|------|------|
| `1-4 Dev/console/console.py` | modify | 记忆层 / recall 工具 / 会话压缩 / ctx 端点 / AGENT_PROFILES / run_replan / 工具循环 prose 兜底 |
| `1-4 Dev/console/console.html` | modify | 上下文占用条 / 角色选择器 / 画布 replanned·blocked 状态 / ctx 更新 |

# Decisions Made
- D1: 记忆只读接入（entities/MEMORY/历史），写回留到 P1，避免污染 SSOT。
- D2: 会话压缩阈值 12000 字符、保留 8 条；摘要失败回退截断（不让压缩阻塞对话）。
- D3: 重规划每 run 最多一次，且只 dry-run；避免无限自愈循环。
- D4: Profile 用"收窄规则文件 + skill 提示 + 模型档"实现，不复制 Hermes 的 profile 机制。

# Patterns Observed
- P1: 模型会返回散文而非 JSON → 工具循环必须有 prose 兜底，否则误报"最大步数"。
- P2: 自愈重规划要给"参数自包含"的预设约束，否则会选中需要 topic 的预设再次失败。
- P3: 记忆检索与 KB 检索要分开（项目内部约定 vs 外部事实），否则互相稀释。

# Open Questions
- Q1: P1 是否做记忆写回（run/会话 → entities.yaml，复用 dream/consolidate）？
- Q2: 角色是否要与用户权限绑定（不同用户默认不同工作线）？
- Q3: 上下文阈值是否需要按角色/模型动态调整？

# Cross-References
- entities: ds-knowledge-base, ds-console-agent, concept-loop-engineering
- related sessions: 2026-09-19-agent-tool-loop-run-canvas.md

# Tags
- relevant-tags: #agent #memory #context #profile #self-healing #p0
