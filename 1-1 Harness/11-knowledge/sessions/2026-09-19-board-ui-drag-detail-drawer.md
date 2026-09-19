---
session_date: 2026-09-19
session_topic: "看板/列表 UI 强化 + 拖拽性能 + 详情抽屉（含质检门禁与 QA findings）"
session_slug: "board-ui-drag-detail-drawer"
profiles_used: [profile-lovart-management]
tools_used: [console.py, console.html, ego-browser, deploy/sync.sh]
agents: [opencode]
duration_min: 120
files_changed_count: 3
schema_bumps: 0
status: ready
---

# Context
- 用户要求：强化看板与列表的排版/UI；提升拖拽性能；尤其要能单独查看细节，呈现更多信息以及质检结果。

# Solution
1. **看板 UI**：卡片重排（标题 / 2 行截断描述 / meta chips：负责人·截止·关联）；hover 才显示操作（🤖 交给 Agent / ⤢ 详情 / × 删除）；列头带计数、列内滚动（62vh）、拖拽高亮整列；列内按进行中优先排序。
2. **拖拽性能**：`DRAGGING` 标志 → 拖拽期间 `loadTasks`/`loadTaskBatches` 与 5s 轮询全部跳过重渲染；`dragstart` 标记 dragging 样式；`drop` 走**乐观移动**（直接搬 DOM + 更新计数 + `taskSetSilent` 静默 API），不再整页重载；失败才兜底 reload。
3. **详情抽屉**：新增右侧抽屉（`openDrawer/closeDrawer`，ESC 关闭，遮罩）。批量任务条目行可点击 → `GET /api/batch/item` 打开抽屉，呈现：
   - **质检门禁**（post-write/geo/quota/language/落地页结构/QA 阻断告警，pass·warn·fail 三态 + 被拦截门禁名 + 结构问题）
   - **预览/操作**（前台预览、打开草稿）
   - **基本信息**（条目/主题/语言/页面类型/状态+重试/说明/token/事务等 8+ 字段）
   - **QA findings 明细表**（级别/规则/问题/可修复）
   - 原始结果 JSON（可展开）
4. **门禁提取扩展**：`batch_view` 除 gen/rewrite 的 `*_rc` 外，新增 landing_refresh 的 `ready_to_publish`/`struct_errors`/`gates_blocked` 与 QA 的 `block/warn`；`_human_result` 对 landing_refresh 给出结构校验结论。

# Files Changed
| 路径 | 操作 | 备注 |
|------|------|------|
| `1-4 Dev/console/console.py` | modify | batch_item_detail 端点 / gates 提取扩展 / landing_refresh 人话结果 |
| `1-4 Dev/console/console.html` | modify | 看板卡片与列 UI / 拖拽优化 / 详情抽屉 / 列计数 |

# Decisions Made
- D1: 拖拽用"乐观移动"，不做整页重渲染；拖拽期间冻结轮询。
- D2: 详情用右侧抽屉而非新页面，保持上下文。
- D3: 门禁三态（pass/warn/fail）+ 被拦截清单，直接回答"这条到底成不成"。
- D4: 原始 JSON 折叠保留，默认给人话信息。

# Patterns Observed
- P1: 局部变量命名与闭包内函数同名会因 TDZ 报错（`const card` 遮蔽 `card()`），且因在 Promise 里静默失败，必须端到端验证渲染结果而非只看语法。
- P2: 轮询刷新会打断拖拽；必须显式冻结。
- P3: 不同执行器的结果字段不一致（gen/rewrite vs landing_refresh vs qa），门禁提取需按类型分别映射。

# Open Questions
- Q1: 是否把该抽屉复用到内容库/报告列表（统一详情体验）？
- Q2: 拖拽是否要支持列内排序（当前按状态+固定优先级）？
- Q3: 门禁结果是否要回写 Sanity 便于前台侧展示？

# Cross-References
- entities: ds-batch-executor, ds-console-agent
- related sessions: 2026-09-19-daily-start-etarisk-email-notify.md

# Tags
- relevant-tags: #kanban #drag-drop #detail-drawer #quality-gates #ui
