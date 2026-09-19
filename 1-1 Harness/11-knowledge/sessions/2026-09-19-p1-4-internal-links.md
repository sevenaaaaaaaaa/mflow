---
session_date: 2026-09-19
session_topic: "P1-4 内链建议批量化（只读分析 + 报告 + 性能优化）"
session_slug: "p1-4-internal-link-batch"
profiles_used: [profile-lovart-management]
tools_used: [console.py, console.html, presets.json, docs/p1-plan.md, deploy/sync.sh]
agents: [opencode]
duration_min: 75
files_changed_count: 5
schema_bumps: 0
status: ready
---

# Context
- P1-4：内链建议批量化。既有 link-suggester 插件只能单页用且为朴素关键词重叠；需批量化 + 可靠。

# Solution
1. **执行器 `internal_link`**（只读分析，不写库）：`link_suggest()` 基于 标题/slug/正文前段 token 重叠 + 同栏目加权；输出 {slug,title,section,url,relevance}；URL 按站点 route 构造。
2. **批量体检** `link_audit()`：扫某栏目 N 页 → 汇总 → 落 `11-knowledge/audit/reports/internal-links-<section>-<lang>-<date>.md`（含 markdown 链接）。
3. **预设**「内链建议体检」（type=internal_link，options: section/lang/limit）。
4. **API** `/api/links/suggest`、`/api/links/audit`；**UI**：抽屉展示建议表（目标页/栏目/相关度/打开）。
5. **性能**：`_lib_link_index(site,lang)` 按站点+语言建 token 索引（`base.glob("*/<lang>/*.md")`，缓存 10 分钟）→ 20 项由卡住降到 <8s。
6. 教训落地：延续审阅子代理原则——**只读分析、不擅改正文**；如需应用内链，另设确定性追加块（当前未开启）。

# Files Changed
| 路径 | 操作 | 备注 |
|------|------|------|
| `1-4 Dev/console/console.py` | modify | link_suggest/link_audit/_lib_link_index/_bh_internal_link/preset 分支/端点和 whitelist/spec_guard 类型 |
| `1-4 Dev/console/console.html` | modify | 抽屉内链建议表 |
| `templates/presets.json` | modify | internal-link-audit |
| `docs/p1-plan.md` | modify | P1-4 标记完成 |

# Decisions Made
- D1: 内链任务**只分析不写入**，避免"乱改正文"。
- D2: 相关度可解释（重叠数 ×2 + 同栏目加权），确定性、无 LLM、零 token。
- D3: 用站点+语言索引替代全库扫描（性能是可用性的一部分）。

# Patterns Observed
- P1: 批处理里做全库 rglob = 灾难；必须预建索引。
- P2: 大段替换会用 `def X():` 结尾导致重复签名 → 语法错，需即时验证。
- P3: 同类能力（分析型）应统一"只读"定位，避免越界写入。

# Open Questions
- Q1: 是否提供"确定性追加相关阅读块"（不改正文，仅追加结构化链接）并支持回滚？
- Q2: 是否把内链建议接入 QA 编排（发现孤立页 → 建议内链）？

# Cross-References
- entities: ds-content-link-index
- decisions: docs/p1-plan.md
- related sessions: 2026-09-19-p1-3-review-subagent.md

# Tags
- relevant-tags: #p1-4 #internal-links #batch #read-only #performance
