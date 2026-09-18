---
session_date: 2026-09-19
session_topic: "Agent v2 主动化 + 全 AI 路径统一上下文 + 导航重组与 next-actions 指挥中心"
session_slug: "agent-v2-unified-context-nav"
profiles_used: [profile-lovart-management]
tools_used: [console.py, console.html, preset_expand, ai_context, next_actions, deploy/sync.sh]
agents: [opencode]
duration_min: 150
files_changed_count: 4
schema_bumps: 0
status: ready
---

# Context
- 用户强反馈三条：① Agent 任务台"太笨"，非要给明确位置/所有细节才开工；② 所有用 AI 的地方都应调用 skills / 上下文 / harness / 知识库，而实际只有 Agent 页部分用了；③ 25+ 导航入口混乱、上手难度极高。
- 目标：把系统做成"所有人都能用起来"的 agent 工作台，而非需要专家配置的工具集。

# Solution
1. **Agent 提示词重写为主动型**（对齐 Claude Code）：先检索上下文自己填细节，只在真正无法决定时才问，且最多 1 条。
2. **LLM 空 spec 时自动匹配预设展开**（`_auto_preset_match`）：宁可产出带假设的 spec，也不空手问一堆。
3. **Agent expand 机制**：范围类任务不让 LLM 猜 doc_id，改为 `spec.expand={preset,opt}`，由后端 `preset_expand` 用真实 Sanity 数据展开。
4. **LLM 降级路径**：402/超时/未配置时，仍用预设+上下文产出可执行 spec，不报错。
5. **统一 AI 上下文** `ai_context(task_type,topic,lang,proj)`：检索 skills + 知识库 + 内容库范例 + harness 规则 + GEO/GSC 事实（≤2400 字符），接入 gen / rewrite / landing_refresh / /api/generate / loop / agent。
6. **导航重组**：25 个平铺 → 5 组（工作台/质量与发布/内容资产/报告与迭代/高级与系统可折叠），ID 与页面不变。
7. **首页 next-actions 指挥中心** + **Agent 空状态能力引导**（6 个一键示例）。
8. **会话标题 + 真实 token 计数 + 每条回复的上下文徽标**（skills/KB/库/规则/tokens）。

# Files Changed
| 路径 | 操作 | 备注 |
|------|------|------|
| `1-4 Dev/console/console.py` | modify | ai_context / kb_search_for_ai / site_of / next_actions / _auto_preset_match / spec_guard expand / agent_reply 主动化+降级 / llm-status 402 记录 / token 计数 |
| `1-4 Dev/console/console.html` | modify | marked.js markdown 渲染 / Ctrl+Enter / 思考动画 / 快捷预设 / 上下文徽标 / 会话标题 token / 空状态引导 / 导航分组 / next-actions 卡片 |
| `1-1 Harness/11-knowledge/sessions/2026-09-19-agent-v2-unified-context-nav.md` | add | 本日志 |

# Decisions Made
- D1: Agent 默认主动产出带假设的 spec，而非保守提问；空 spec 走预设 fallback。
- D2: 范围类任务用 expand+preset 由后端展开真实数据，LLM 不猜 doc_id。
- D3: 所有 LLM 调用点强制注入统一上下文（skills/KB/库/规则/事实）。
- D4: 导航保持 25 个 tab（改分组+折叠），不删功能只降认知负荷。
- D5: LLM 不可用时降级不报错，保证"永远能给下一步"。

# Patterns Observed
- P1: LLM 规划器天然保守 → 仅靠提示词不够，必须有后端 fallback 与 expand 机制兜底。
- P2: "让 LLM 产出字面条目"在数据驱动范围任务上必错；应让 LLM 产出"范围意图"，后端解析。
- P3: `window.alert` 已全局覆盖为 toast，历史 `alert()` 无需逐处改。
- P4: 上下文注入需设预算（≤2400 字符）否则 token 成本与串味风险上升。

# Open Questions
- Q1: 批量任务页的错误提示仍偏技术化，是否要按同一"主动化"标准改造文案？
- Q2: 工作流地图/节点流水线等高级页对新手的暴露是否应默认隐藏？
- Q3: Agent 是否要支持多轮可编辑 spec（在对话内改范围再执行）？

# Cross-References
- entities: ds-console-agent, ds-batch-executor, concept-loop-engineering
- decisions: MEMORY-PROJECT.md § Agent 任务台
- skills: lovart-landing-page, lovart-content-creation-orchestrator, lovart-page-serp-writer

# Tags
- relevant-tags: #agent #ux #context-engineering #harness #navigation
