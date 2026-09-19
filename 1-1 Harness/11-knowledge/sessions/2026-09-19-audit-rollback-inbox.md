---
session_date: 2026-09-19
session_topic: "可用性提升：变更审计+一键回滚、统一收件箱"
session_slug: "audit-rollback-inbox"
profiles_used: [profile-lovart-management]
tools_used: [console.py, console.html, docs/p1-plan.md, ego-browser, deploy/sync.sh]
agents: [opencode]
duration_min: 120
files_changed_count: 4
schema_bumps: 0
status: ready
---

# Context
- 用户：embedding 先挂起（已在 docs/rag-plan.md 留一步开启），继续推其他可用性项。按性价比：审计回滚 → 收件箱 → 失败摘要。

# Solution
1. **变更审计 + 一键回滚**
   - `audit_record()` 写 `run/audit-changes.jsonl`：{id,ts,kind,doc_id,before,after,by,task,rolled_back,extra}；dry-run 不记录；超大 bodyJson 截断标记。
   - 接入 `field_patch`（查询字段原值）、`asset_replace`（cover/coverUrl/bodyJson 原值）、`publish_sanity`（记录但**不自动回滚**，避免对正文造成"假安全感"）。
   - `audit_rollback()`：按记录把字段恢复为 before（`ifRevisionID` 保护），标记 rolled_back + 记录回滚事务；重复回滚拒绝；写 approvals.log。
   - 端点 `/api/audit/changes|rollback`（admin）；「变更审计」页（时间/类型/文档/操作人/状态/回滚）。
   - 实测：真实写入 1 条（把 title 设为原值，等价 no-op）→ 审计记录 before/after 正确 → 回滚成功（tx）→ 再次回滚被拒。
2. **统一收件箱**：`inbox()` 聚合 系统自检 block/warn、分配给我的待办、未指派待办、失败/熔断批量任务、待授权发布、失败执行、待执行 Agent 方案、自动化异常；按优先级排序。「收件箱」页 + 右侧「处理 →」动作（tab/batch/run/api）+ nav 角标。实测 3 项（1 紧急）。

# Files Changed
| 路径 | 操作 | 备注 |
|------|------|------|
| `1-4 Dev/console/console.py` | modify | audit_record/list/rollback/_audit_update + handler 接入 + inbox + 端点 |
| `1-4 Dev/console/console.html` | modify | 变更审计页 + 收件箱页 + nav/角标 + 动作分发 |
| `docs/p1-plan.md` | modify | 追加「可用性提升」清单与 RAG 状态 |

# Decisions Made
- D1: 只对**确定性、字段级**写入提供自动回滚；发布类（改正文）明确标注不可自动回滚。
- D2: dry-run 一律不记录（审计只反映真实变更）。
- D3: 收件箱是"待处理"的聚合，不新增实体；动作直接复用现有入口。
- D4: 回滚写 approvals.log 并记录回滚事务 id，保证可追溯。

# Patterns Observed
- P1: "不敢用"的根因是缺少可逆性；审计+回滚是最直接的信心来源。
- P2: 回滚必须防"假安全感"——不能回滚的场景要显式标注，而非给个按钮了事。
- P3: 收件箱的价值在于"把散落的待处理收敛为一屏"，而非新增能力。

# Open Questions
- Q1: 是否给回滚加"变更前后 diff 可视化"？
- Q2: 审计保留策略（条数/天数）与归档？
- Q3: 失败摘要（下一步）是否直接从收件箱点进批量任务？

# Cross-References
- entities: ds-batch-executor
- decisions: docs/p1-plan.md
- related sessions: 2026-09-19-rag-foundation-kb-ux.md

# Tags
- relevant-tags: #usability #audit #rollback #inbox #reversibility
