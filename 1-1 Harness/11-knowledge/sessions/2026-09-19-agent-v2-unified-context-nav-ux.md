---
session_date: 2026-09-19
session_topic: "Agent v2 主动化 + 全 AI 路径统一上下文 + 导航重组 + 8 项 UX 反馈落地"
session_slug: "agent-v2-unified-context-nav-ux"
profiles_used: [profile-lovart-management]
tools_used: [console.py, console.html, ego-browser, preset_expand, ai_context, batch_view, next_actions, deploy/sync.sh]
agents: [opencode]
duration_min: 300
files_changed_count: 4
schema_bumps: 0
status: ready
---

# Context
- 用户强反馈：① Agent 太笨（非要给全部细节才开工）；② 所有 AI 路径都应调用 skills/上下文/harness/知识库；③ 25+ 导航入口混乱、上手难。
- 随后追加 8 项 UX 反馈：批量详情无法预览/看不懂结果、侧栏按钮无用、导航分组、任务看板无实质、创作/节点/Loop 无预设、要看板娘、登录进总览、每页要 onboarding。

# Solution
1. **Agent 主动化**：重写提示词为先假设后产出；LLM 空 spec → 自动预设 fallback；范围类任务用 `spec.expand={preset,opt}` 由后端用真实 Sanity 数据展开；LLM 不可用时降级不报错。
2. **统一 AI 上下文** `ai_context()`：skills + 知识库 + 内容库范例 + harness 规则 + GEO/GSC 事实（≤2400 字符），接入 gen/rewrite/landing_refresh/api-generate/loop/agent 全部 6 个 LLM 调用点。
3. **导航重组**：25 个 sidebar 项 → 5 组 + 高级折叠；新增顶部 mega-menu 导航（6 组）；侧栏顶部快捷入口（任务看板/Agent/日历）。
4. **批量详情人话化** `batch_view()`：每项输出 ok/status_text/detail + 前台预览 URL（按站点 route 模板构造）+ 草稿阅读；一次性 Sanity 查询批量取 slug。
5. **任务看板**：新增批量任务进度区；手动任务卡加 🤖 交给 Agent。
6. **预设补齐**：创作中心选题灵感、节点流水线预设流程、Loop 快速开始。
7. **看板娘小 M**：右下角浮窗，按当前页面给上下文提示 + 可直接问 Agent。
8. **逐页 onboarding**：`PAGE_GUIDES` + `mountGuide()`，首次进入自动展示、可关闭可重开。

# Files Changed
| 路径 | 操作 | 备注 |
|------|------|------|
| `1-4 Dev/console/console.py` | modify | ai_context / kb_search_for_ai / site_of / next_actions / _auto_preset_match / spec_guard expand / agent_reply 主动化+降级 / batch_view / _site_url / _human_result / llm-status |
| `1-4 Dev/console/console.html` | modify | Agent v2 / mdRender / 顶部导航 / 侧栏快捷 / 任务看板批量进度 / 三页预设 / 看板娘 / 逐页 onboarding / 恢复 16 个被误删函数 |
| `1-1 Harness/11-knowledge/sessions/2026-09-19-agent-v2-unified-context-nav-ux.md` | add | 本日志 |

# Decisions Made
- D1: 范围类任务禁止让 LLM 猜 doc_id，一律 expand+预设由后端展开真实数据。
- D2: 批量结果必须人话化并给出前台预览链接，"原始 JSON"不再作为唯一结果。
- D3: 所有 LLM 调用点强制注入统一上下文（skills/KB/库/规则/事实）。
- D4: 导航改分组+mega menu，不删功能只降认知负荷。
- D5: 每个功能页必须自带 onboarding（可关闭、可重开）。
- D6: 看板娘作为统一下一步入口与问答入口。

# Patterns Observed
- P1: **大段替换易误删相邻函数**——本次 Agent v2 替换删除了 modeLoad/loadPresets/quota*/style*/brk*/hk* 共 16 个函数，导致总览空白。教训：替换后必须做函数集 diff（`funcs(old)-funcs(new)`）。
- P2: LLM 规划器天然保守，必须由后端 fallback + expand 兜底，不能只靠提示词。
- P3: 服务器 SESSIONS 存内存，每次部署重启都会踢下线用户（观感差，建议持久化）。
- P4: CF 缓存会缓存登录页/控制台页；未配 `deploy/cf.env` 时发布不刷新，用户可能看到旧页。
- P5: Rocket Loader 会改写 inline handler，前端依赖 CDN（如 marked）时必须有内置兜底。

# Open Questions
- Q1: 是否持久化 SESSIONS（写 run/sessions.json）以避免部署踢人？
- Q2: 是否配置 deploy/cf.env 以自动清 CF 缓存？
- Q3: 批量任务错误文案仍偏技术化，是否继续人话化？

# Cross-References
- entities: ds-console-agent, ds-batch-executor, concept-loop-engineering
- decisions: MEMORY-PROJECT.md § Agent 任务台
- skills: lovart-landing-page, lovart-content-creation-orchestrator

# Tags
- relevant-tags: #agent #ux #context-engineering #harness #navigation #onboarding
