---
session_date: 2026-09-19
session_topic: "Agent 工具循环 + 执行画布（Run）+ 编排闭环：让系统能力不输本地 agent 且更可视化"
session_slug: "agent-tool-loop-run-canvas"
profiles_used: [profile-lovart-management]
tools_used: [console.py, console.html, ego-browser, agent_tool, run_tick, ego-browser]
agents: [opencode]
duration_min: 180
files_changed_count: 3
schema_bumps: 0
status: ready
---

# Context
- 用户明确目标：把这个系统做到"不输本地 agent"，且要"比本地 agent 更可视化"——对话后要有画布，显示完成了几步、正在做什么、进度到哪；任务能后台跑，画布/看板让人"真实感受到任务在被执行"。
- 关键差距：原 Agent 只做"一次性规划"，不能查真实数据、不能观察执行结果、不能自我纠错、不能多步编排。

# Solution
1. **Agent 工具循环**：`agent_tool()` 提供 9 个工具（search_content/search_kb/get_task/list_tasks/list_drafts/geo_facts/gsc_facts/check_url/run_preset）。`agent_reply` 改为最多 5 步的推理循环：LLM 输出 `{tool:{name,args}}` → 执行 → 结果回灌 → 继续，直到给出 `spec` 或 `plan`。全程只读或 dry-run。
2. **执行画布（Run）**：`run_new/run_save/run_load/run_list/run_view` + `run_tick()`（batch_worker 每 5s 推进）。Run = 有序步骤（理解与规划/展开范围/批量执行/发布/校验），批量步与 batch 任务联动取实时进度；发布步自动承接前序改稿草稿（含 frontmatter 补 slug/lang/page_type）；校验步用真实 doc URL 检查前台可访问；dry-run 自动跳过前台校验。
3. **编排闭环 + 依赖门控**：plan 执行走 `/api/agent/run`；前序步骤失败 → 后续 `blocked`，不再连锁执行。
4. **前端**：新增「执行画布」页（工作台组），步骤时间线 + 状态点 + 进度条 + 自动刷新 + 取消/重试；Agent 线程渲染推理轨迹（工具调用）与多步计划卡片（一键"执行计划（后台运行）"）。
5. **修复 3 个真实 bug**：① `_auto_preset_match` 类型错误（fallback 崩溃）；② `run_generation` 引用未定义的 `style_id`（导致所有 rewrite/gen 批次失败）；③ `run_tick` 误放在 worker 循环外（只执行一次）。

# Files Changed
| 路径 | 操作 | 备注 |
|------|------|------|
| `1-4 Dev/console/console.py` | modify | agent_tool + 工具循环 / Run 系统 / run_tick / 依赖门控 / style_id 修复 / _auto_preset_match 修复 / publish 步增强 / landing 配对引导 |
| `1-4 Dev/console/console.html` | modify | 执行画布页 + run 渲染轮询 / Agent 轨迹与计划卡片 / nav 入口 / 引导 |

# Decisions Made
- D1: Agent 从"单次规划"升级为"工具循环 + 观察 + 多步"，对齐本地 agent 能力。
- D2: Run 作为一等执行记录持久化，画布/看板/线程共享同一状态。
- D3: 工具一律只读或 dry-run，真实写入仍需 spec + force（安全边界不变）。
- D4: 前序失败阻断后续（依赖门控），避免无效连锁。
- D5: dry-run 不验证前台（避免误判），真实发布才验证。
- D6: compositePage 的改稿发布统一走 `landing-refresh-publish` 闭环，避免结构校验失败。

# Patterns Observed
- P1: Agent 只有"能查数据 + 能观察结果"才算 agent；纯注入上下文无法替代工具循环。
- P2: 步骤编排必须显式门控依赖，否则失败会连锁产生垃圾任务。
- P3: 大段代码编辑后必须跑"函数集合 diff + 真实批次端到端"，本轮才暴露 style_id 与 run_tick 位置两个隐藏 bug。
- P4: 后台线程的任务要放在 `while` 循环内；放在循环外只在启动时执行一次。

# Open Questions
- Q1: 是否让 Agent 在 run 结束后自动读结果并给"下一步建议"（闭环自治）？
- Q2: 画布是否需要支持并行分支（而非纯线性步骤）？
- Q3: 是否把 Run 与 Loop 模式打通（Run 作为 Loop 的一次迭代的可视化）？

# Cross-References
- entities: ds-console-agent, ds-batch-executor, concept-loop-engineering
- related sessions: 2026-09-19-interaction-feedback-kb-retrieval-board.md

# Tags
- relevant-tags: #agent #tool-use #orchestration #canvas #run #loop #visualization
