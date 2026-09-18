---
description: 会话日志 skill。自动写结构化日志。
---
# lovart-session-log — 自我生长循环的 Layer 1

> **核心问题**：每段会话（不限工具 / 限 profile）解决了问题，但 lessons **没沉淀**——下次又从 0 开始。
> **本 skill 解法**：每段会话**结束前**强制写一份结构化 Session Log 到 `1-1 Harness/11-knowledge/sessions/`。
> 后期 dream/reflect.sh（Layer 2）+ PR workflow（Layer 3）会基于这些 logs 做 pattern 提取 → harness 演进。

---

## When this skill loads

加载条件（满足任一即可触发）：

**用户显式触发**（高置信）：
- 用户说"这轮可以收尾"、"写日志"、"归档"、"wrap up"、"log this"、"session 完结"、"本轮收尾"

**Agent 主动判断**（中置信）：
- 触达 ≥ 5 个文件 + ≥ 1 个 schema 改动
- 解决了 ≥ 1 个具体技术问题（不只是查询）
- 触发了 ≥ 1 个新 skill / rule / KB-doc 的新建或修改
- 用户明显在做 harness 演进（不是单篇内容）

**定时触发**（低置信，留 agent 自由裁量）：
- 一轮会话 30 分钟以上 + ≥ 8 个文件改动 → agent 应主动问："这轮值得归档吗？"

不加载：
- 单点查询（无文件改动 / 无决策）
- 简单的 KB-mine / 跑一次 cascade smoke test 这类运维动作
- 用户显式说"先不写日志" / "不必归档"

---

## Process

### Step 1 — 决定 slug

- 取这轮主题的一句话 → kebab-case
- 例：`kb-ranking-tune`, `cascade-v0.2-orchestrator`, `dream-audit-cleanup`
- 避免 slug 重复 → `ls 1-1 Harness/11-knowledge/sessions/` 检查今日已用 slug

### Step 2 — 决定 frontmatter

按 `1-1 Harness/11-knowledge/sessions/SESSION-TEMPLATE.md` schema 填：

```yaml
---
session_date: {YYYY-MM-DD}
session_topic: "{一句话}"
session_slug: "{slug}"
profiles_used: [profile-lovart-management]   # 来自这次会话
tools_used: [kb-mine, ...]                    # 用过的 skill / 脚本
agents: [hermes]                              # 谁参与的
duration_min: {估算}
files_changed_count: {N}
status: draft
---
```

### Step 3 — 写 6 个标准段落

按下面这个 order 写，每段 ≤ 12 行（agent 的轻量约束）：

| 段落 | 内容 | 取自哪里 |
|------|------|---------|
| Context | 触发这次会话的问题；用户的需求是什么 | 会话开头 1-2 段对话 |
| Solution | 实现了什么；一段话说清 | 会话末尾做了什么 |
| Files Changed | 表格：路径 / 操作 (add/modify/del) / 一句话备注 | git diff 记忆 + 修改列表 |
| Decisions Made | D1 / D2 / D3... 编号列决策 | 用户在会话中拍板的点 |
| Patterns Observed | P1 / P2 / P3... 编号列潜在模式 | agent 自己观察到的"可能会成为 future rule" |
| Open Questions | Q1 / Q2... 编号列待 follow-up | 用户说"以后再搞" / agent 自己 flag |

### Step 4 — Cross-References

```yaml
cross_refs:
  entities: [ds-knowledge-base, skill-lovart-quality-cascade]   # 触达的 11-knowledge entities
  decisions: [MEMORY-PROJECT.md § 12]                            # 已写过的 memory section
  skills: [lovart-kb-mine]                                       # 触达的 skill
  related_sessions: []                                            # 之前相关 session（如有）
```

### Step 5 — Frontmatter → 状态 → 写文件

初始状态 `draft`。写完问用户：

```
"这轮会话的 Session Log 写好了。draft → ready？
  接受 = 我会把它写进 1-1 Harness/11-knowledge/sessions/{slug}.md
  修改 = 你说要改哪一段
  取消 = 不写"
```

用户确认 → 状态 `ready` → 写入。

### Step 6 — 通知 dream/audit (Layer 2 预告)

如果这次会话新增了 ≥ 1 个 Pattern P# → 在 audit 报告里附一行：

```
note: 1 new pattern (P5) added — appears 1 time, will be tracked by dream/reflect.sh
```

这是 Layer 2 的钩子，dream/reflect.sh 实现后会扫 sessions/*.md 抽 P# 频率。

---

## Hard rules

1. **不允许自动 commit**：session log 写到 draft → 用户接受才 ready。
2. **不允许自动改 harness**：session log 是 reflections，不是 actions。agent 不要在 log 里同时改文件。
3. **不允许跨工具转录**：不要试图把 hermes 的 transcript 拉到本 skill — 用户输入的"对话上下文"才是信源。
4. **轻量**：单份 log ≤ 80 行（agent cap）。P# / D# 编号不超过 8 条。
5. **不重复 memory**：已写入 MEMORY-PROJECT.md § 0-11 的事，用 `cross_refs.decisions: MEMORY-PROJECT.md § N` 引用，不要复制。
6. **保持诚实**：如果一节 session 没产生什么 lessons，**也写**（标 `decisions: []` + `patterns: []`），而不是跳过 — skipped logs 是 silent loss。

---

## Failure modes (NEVER)

- "这轮没改文件，所以不写" — 即使纯查询的会话也可写（patterns 段填"无新 pattern"）。沉默 = 丢数据。
- "让 agent 自动 commit" — 永远 user-approve。
- "把 1 个 session 拆成 2-3 个" — 一次 session = 1 个 log。如果 user 中间断续，按时间分段。
- "P# 列表里写 12+ 条" — 不行。强制精简。8 条上限。
- "log 里夹带新文件 / 新规则" — log 是 passive reflective record。改文件 / 改规则走独立动作。

---

## Reference

- 模板：`1-1 Harness/11-knowledge/sessions/SESSION-TEMPLATE.md`
- 输出目录：`1-1 Harness/11-knowledge/sessions/`
- Layer 2 (preview, 未实现)：`1-1 Harness/11-knowledge/dream/reflect.sh` — 每周扫 sessions，统计 P# 频率
- Layer 3 (preview, 未实现)：PR Workflow + user approve/decline
- 关联 skill：`lovart-dream-orchestrator` (梦境编排 — Layer 2 实际运行时挂这里)
- 关联 graph entities：`ds-sessions` (planned)