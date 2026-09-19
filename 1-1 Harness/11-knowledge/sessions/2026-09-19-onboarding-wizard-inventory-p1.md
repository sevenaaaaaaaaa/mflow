---
session_date: 2026-09-19
session_topic: "开工向导（体检→盘点→规划→填满）+ 能力/内容盘点 + P1 安排"
session_slug: "onboarding-wizard-inventory-p1"
profiles_used: [profile-lovart-management]
tools_used: [console.py, console.html, docs/p1-plan.md, ego-browser, deploy/sync.sh]
agents: [opencode]
duration_min: 150
files_changed_count: 4
schema_bumps: 0
status: ready
---

# Context
- 用户要求：把知识库/Skills/已有内容做一次盘点，找出可做的任务/loop/批量动作，直接放到后台可运行；首次引导要在内容与 KB 建好后跑"体检 → 任务规划 → 填满所有环节"，让用户第一天就能用起来；并安排可轻量吸收的 P1。

# Solution
1. **能力与内容盘点（真实数据）**：内容库 17,535 篇（blog 8864 / features 6400 / tools 1661 / topics 409 / solutions 120 / products 41 / scenarios 23 / news 17）；知识库 74 篇；Skills 48；预设 8；插件 6 可用；物料 17,538 页（10,680 有封面，**1,571 缺 alt**，8,608 有正文图）；GSC 20 条；Sanity compositePage 8,864。
2. **开工向导 `/api/onboard/plan`**：体检（selfcheck）+ 盘点 + 规划（7 类可做任务，带真实计数与 ETA：QA 体检、字段修复、封面 alt、低 CTR 刷新、GEO 缺口、落地页闭环、多语言）+ 推荐启动包。
3. **一键填充 `/api/onboard/seed`**：把启动包前 N 项创建为 **dry-run 批次任务**（不擅自写生产），后台立即开始跑。实测填充 3 个任务：QA 扫描 50/50、字段修复 50/50、封面 alt 50/50 全部完成（0 token，纯规则）。
4. **开工向导页**：四步可视化（① 体检 ② 盘点 ③ 规划 ④ 填满并启动）；首访（admin，每浏览器一次）自动引导进入。
5. **性能**：QA 抽样并行化 + 计划结果缓存 5 分钟（冷 5.0s → 缓存 0.63s）。
6. **口径对齐**：低 CTR 计数改用与 `low-ctr-refresh` 预设一致的 `impact_report` 口径，避免"计划有 N、执行说无"。
7. **P1 安排**：写入 `docs/p1-plan.md`（记忆审阅 UI / Run 心跳可视化 / 子代理审阅 / 内链批量化 / 多语言覆盖盘点 / 插件市场 UI），并给出排序与"明确不做"。

# Files Changed
| 路径 | 操作 | 备注 |
|------|------|------|
| `1-4 Dev/console/console.py` | modify | onboard_plan / onboard_seed / _asset_alt_gap / _qa_sample(并行) / 缓存 / low_ctr 口径 |
| `1-4 Dev/console/console.html` | modify | 开工向导页（四步）+ nav 入口 + 首访引导 |
| `docs/p1-plan.md` | add | P1 轻量吸收清单与排序 |
| `11-knowledge/sessions/2026-09-19-onboarding-wizard-inventory-p1.md` | add | 本日志 |

# Decisions Made
- D1: 首次引导 = 真实数据驱动的"体检→盘点→规划→填满"，而非静态说明页。
- D2: 填充只创建 dry-run 任务（遵守"生产写入需人工授权"铁律），用户确认后再关掉 dry-run。
- D3: 计划结果缓存，避免每次进入都重跑 Sanity 抽样。
- D4: P1 只吸收 DeerFlow 中与本架构契合的轻量部分，不引入重架构。

# Patterns Observed
- P1: "可做任务"必须来自真实数据计数（否则用户第一天就遇到"计划有、执行无"的落差）。
- P2: 引导页的体检+抽样若串行会明显卡顿（15 次 Sanity 查询 ~5s），需并行+缓存。
- P3: 首访自动引导要"每浏览器一次 + admin 优先"，否则打扰老用户。

# Open Questions
- Q1: 启动包默认项是否应按站点类型（blog 站 vs 落地页站）自适应？
- Q2: 是否把"开工向导"完成度计入 setup 的进度？
- Q3: P1 排序是否调整（用户可指定）？

# Cross-References
- entities: ds-batch-executor, ds-knowledge-base
- external: bytedance/deer-flow (DeerFlow 2.0)
- related sessions: 2026-09-19-deadend-audit-deerflow-borrow.md

# Tags
- relevant-tags: #onboarding #inventory #seed #dry-run #p1 #first-day
