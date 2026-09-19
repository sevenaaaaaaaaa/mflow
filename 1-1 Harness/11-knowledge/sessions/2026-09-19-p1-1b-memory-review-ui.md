---
session_date: 2026-09-19
session_topic: "P1-1b 记忆审阅 UI（事实/实体浏览 + 更正/标过时，Agent 立即生效）"
session_slug: "p1-1b-memory-review-ui"
profiles_used: [profile-lovart-management]
tools_used: [console.py, console.html, docs/p1-plan.md, ego-browser, deploy/sync.sh]
agents: [opencode]
duration_min: 90
files_changed_count: 4
schema_bumps: 0
status: ready
---

# Context
- P1-1b：记忆审阅 UI。动机：`entities.yaml`（98 实体）/`MEMORY-PROJECT.md`（288 事实）已被 Agent 读取，但用户无法查看/纠正，长期必然漂移并污染生成结果。用户明确"这个非常重要"。

# Solution
1. **覆盖层** `run/memory-overrides.json`：`{facts:{fid:{status,text,note,by,at}}, entities:{eid:{status,note,by,at}}}`；`_fact_id()` 用 section+text 的 sha1 稳定标识。
2. **Agent 立即生效**：`_memory_index()` 跳过 `outdated`、用 `corrected.text` 替换；`_entities_index()` 叠加实体 status/notes；两个缓存 key 均纳入覆盖文件 mtime，改动即失效。
3. **API**：`GET /api/memory`（事实+实体+分组+统计+覆盖）；`POST /api/memory/fact`（status: active|outdated|corrected，可带 text/note；`active` 且无 note/text = 清除覆盖）；`POST /api/memory/entity`（status/note）。
4. **UI**：`记忆审阅` 页（系统组）——三视图切换（事实 / 实体 / 已修改）；事实按 section 分组、P1/P2/P3 优先级徽标，可「更正」（替换文本）或「标为过时」；实体按类型分组、状态徽标 + 「更正」备注；「已修改」清单可撤销。顶部统计（事实/实体/过时/更正/实体修改）。
5. 实测：标注过时 → 索引移除；更正 → 索引返回新文本（overridden=corrected）；撤销 → 清除并恢复；实体视图呈现全部项目档案（person/project/product/tool/profile...）。

# Files Changed
| 路径 | 操作 | 备注 |
|------|------|------|
| `1-4 Dev/console/console.py` | modify | 覆盖层 / _fact_id / 索引叠加 / memory_review / 3 个端点 / hashlib |
| `1-4 Dev/console/console.html` | modify | 记忆审阅页（三视图）+ nav |
| `docs/p1-plan.md` | modify | P1-1b 标记完成 |

# Decisions Made
- D1: 采用"覆盖层"而非直接改写 SSOT（MEMORY-PROJECT/entities），保证可撤销、可审计、不改上游文件。
- D2: 过时=从检索索引移除（Agent 彻底看不到），更正=替换文本（Agent 用新表述）。
- D3: 事实 id 用内容哈希——同 section 同文本稳定，便于覆盖与撤销。

# Patterns Observed
- P1: 记忆治理的关键不是"能看"，而是"改动要立即影响 Agent 检索"；覆盖层 + 缓存失效是低成本高收益做法。
- P2: 返回给前端的索引含 `tok`(set) 无法 JSON 序列化，需剔除派生字段。
- P3: 统计口径要基于"覆盖记录"而非"返回结果"（过时的已被过滤，按结果统计恒为 0）。

# Open Questions
- Q1: 是否提供"批量导入更正确认"与"写回 SSOT（复用 dream/consolidate）"？
- Q2: 是否给实体也支持编辑 name/status 全字段（当前仅 note/status）？
- Q3: 是否需要"记忆变更审计日志"独立文件？

# Cross-References
- entities: ds-knowledge-base
- decisions: docs/p1-plan.md
- related sessions: 2026-09-19-p0-memory-context-profiles-replan.md

# Tags
- relevant-tags: #p1-1b #memory #governance #override #review-ui
