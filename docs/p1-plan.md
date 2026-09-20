# 统一执行方式（本轮并行交付的能力）

四类能力统一为"同一件工作、可自由切换执行方式"：

| 方式 | 入口 | 后端 |
|---|---|---|
| 创建任务 | 任务看板 / 对话 | `/api/tasks/*` |
| 批量任务 | 批量任务页 / 预设 | `/api/batch/*`、`presets` |
| 任务编排 | 执行画布 / Agent 计划 | `/api/agent/run`、`Run` |
| Agent 模式 | Agent 任务台 / 小 M | `/api/agent/chat`（工具循环） |
| **自动化** | 自动化页 | `/api/automations/*`（定时自动执行） |

**切换**：任意来源 → `⇄ 执行方式` → 转为批量 / Loop / 自动化（定时）/ 交给 Agent。
- 任务卡、批量详情、执行画布、Agent 计划卡均已挂「⇄ 执行方式」。
- API：`/api/work/convert` {from:{kind,id,...}, to:'batch|loop|automation', params}。

---

# P1 安排（可轻量吸收）

> 承接 P0（记忆/会话/角色/自愈）与「开工向导」。以下按"轻量可吸收 + 高杠杆"排序，均为在现有单进程文件态架构内的增量，不引入重框架。
> 状态：待排期（用户确认后按序实施）。

## P1-1 多语言覆盖盘点与补齐 ✅ 已完成（2026-09-19）
- 已交付：内容库「多语言覆盖」卡（每语言 已覆盖/总数 + 一键补 N，dry-run）；API `/api/multilang/coverage`、`/api/multilang/fill`。
- 实测：tools 基准 en 385 篇，de 81 / fr 90 / ja 79 …，一键创建本地化 rewrite 任务。

## P1-1b 记忆审阅 UI ✅ 已完成（2026-09-19）
- 已交付：`记忆审阅` 页（系统组）。事实视图（288 条，按 section 分组，P1/P2/P3 优先级）与实体视图（98 个，按类型）；每条可「更正」（替换文本）或「标为过时」；「已修改」清单可撤销。
- Agent 立即生效：`_memory_index`/`_entities_index` 叠加 `run/memory-overrides.json`；过时=从索引移除，更正=替换文本；缓存按覆盖文件 mtime 失效。
- 实测：标注过时 → 索引消失；更正 → 索引返回新文本（overridden=corrected）；撤销 → 清除覆盖并恢复。

## P1-1c 记忆审阅 UI（原描述）
- **为什么**：`entities.yaml` / `MEMORY-PROJECT.md` 已被 Agent 读取，但用户无法查看/纠正，长期会漂移。
- **做什么**：只读浏览（实体列表 + 事实条目，按 section/优先级筛选）+ 标注"已过时/已更正"；写回复用 `dream/consolidate`。
- **成本**：低（1 个页面 + 2 个只读端点；写回复用现有脚本）。
- **验收**：能看到 288 条事实/98 实体；标注后 Agent 下次不再引用过时条目。

## P1-2 Run 心跳可视化 + 恢复可解释 ✅ 已完成（2026-09-19）
- 已交付：执行器心跳文件 `run/worker-heartbeat.json`（worker 每 5s 写）；`worker_alive()`；`health.worker`；selfcheck 增「执行器不在线」block 项；画布/批量详情显示 心跳时间·停滞秒·自动恢复次数；顶栏常驻执行器状态灯（30s 轮询，离线弹告警）。
- 实测：在线(True,0s)；模拟 600s 无心跳 → selfcheck level=block(id=worker)；恢复后自动 ok。

## P1-2b Run 心跳可视化（原描述）
- **为什么**：已有心跳/孤儿恢复，但用户看不到"是否还活着、恢复过几次"。
- **做什么**：画布与批量详情显示 `heartbeat_ts`（最近心跳）、`recovered`（恢复次数）、停滞时长；停滞时给出"正在自动恢复"提示。
- **成本**：低（前端展示 + 已在后端）。
- **验收**：任务停滞 >6 分钟自动恢复并在 UI 可见。

## P1-3 审阅子代理（planner → reviewer）✅ 已完成（2026-09-19）
- 设计针对历史痛点（无上下文 / 不遵守 skills / 掺水 / 乱改）：
  1) **与规划器共享同一上下文**（skills + harness 规则 + 项目记忆 + 知识库 + 会话目标）；
  2) **硬性要求引用依据**（RULES-xx / skill 名 / 记忆§），无依据不得提；
  3) **只判断、不动笔**（绝对禁止修改/续写内容）→ 天生不可能掺水/乱改；
  4) **只能收紧**（dry-run / 缩小 expand.limit / 补必填参数），绝不改语义、绝不放宽；
  5) 不确定即 pass，最多 3 条；失败 fail-open 不阻塞。
- 集成：`/api/agent/chat` 生成 spec 后自动审阅；`revise` 自动收紧（`applied_notes` 记录）；`block` 在 `/api/agent/execute` 拦截，需 `ack_review` 二次确认。UI：spec 卡显示 🛡 结论 + 逐条理由与依据；block 时禁用执行并出现「我已了解风险」勾选；会话级「审阅」开关。
- 实测：正常任务 verdict=pass；"全站 8000 篇真实写入" → verdict=block，3 条意见分别引用 记忆§1.5、RULES-40-ops#5、RULES-00-iron#5、记忆§6.12。

## P1-3b 子代理：执行前审阅（原描述）
- **为什么**：Agent 会产出带假设的 spec，执行前缺一道独立审查，容易跑偏/浪费额度。
- **做什么**：spec 生成后由 reviewer 子代理（同模型、独立提示词）审"范围是否过大/是否高风险写入/是否与目标一致"，输出 `pass/revise` + 理由；高风险时要求收紧范围或先 dry-run。
- **成本**：中低（一次额外 LLM 调用 + spec 流程加一步）。
- **验收**：大范围/真实写入的 spec 会被要求先 dry-run 或缩范围。

## P1-4 内链建议批量化 ✅ 已完成（2026-09-19）
- 已交付：执行器 `internal_link`（**只读分析、不写库**）+ 预设「内链建议体检」+ `/api/links/audit`、`/api/links/suggest`；产出 markdown 报告到 `11-knowledge/audit/reports/internal-links-*.md`；抽屉展示每页建议（含 URL 与相关度）。
- 性能：新增按「站点+语言」的页面 token 索引（仅扫该语言目录，缓存 10 分钟），避免每项全库 rglob —— 20 项由"卡住"降到 <8s。
- 实测：tools/en 60 页 100% 有建议；报告已生成。

## P1-4b 内链建议批量化（原描述）
- **为什么**：`link-suggester` 插件已存在但只能单页用。
- **做什么**：新增批量执行器类型 `internal_link`（读 CONTENT_LINK_INDEX），为一组页面产出内链建议并 dry-run 应用。
- **成本**：中（复用插件 + 一个 handler）。
- **验收**：能对 50 篇工具页一次性产出内链建议。

## P1-5 多语言覆盖盘点与补齐
- **为什么**：内容库含 10+ 语言，但覆盖不均，用户不知道缺什么。
- **做什么**：按 section 统计每页拥有的语言 → 缺口报表；一键用 `multilang-batch` 补齐 Top N 缺口。
- **成本**：低（读 index.json 的 langs + 报表页）。
- **验收**：能看到"tools/en 有 385 篇，缺 ja 的 N 篇"，并可一键补齐。

## P1-6 Skill / 插件市场一键安装 UI ✅ 已完成（2026-09-19）
- 已交付：市场页「一键安装」（从 marketplace.json 直接装，无需粘贴代码）；`plugin_install` 从仅 source/publisher 扩展到全部 5 类可执行类型（source/publisher/gate/transform/analyzer）；插件「启用/停用」（`plugins/<id>/state.json` + `/api/plugins/toggle`）；新增「Skills 目录」浏览（48 个，按分组 + 检索）。
- 实测：一键安装 rss-source 通过 plugin_check；停用/启用生效；（测试后已卸载还原）。

## P1-6b Skill / 插件市场一键安装（原描述）
- **为什么**：`plugins/marketplace.json` 已有可安装包，但无 UI 入口。
- **做什么**：模板市场页加"插件"分区，展示 marketplace 条目 + 一键安装/卸载（复用 `plugin_install`）。
- **成本**：低（市场页 + 已有端点）。
- **验收**：非工程用户能一键装/卸插件。

## 排序建议
1. P1-5（最轻、直接服务"第一天用起来"）→ 2. P1-2（最轻、稳定性可见）→ 3. P1-6（轻、生态）→ 4. P1-1（记忆治理）→ 5. P1-3（质量门）→ 6. P1-4（内链，成本最高）。

## 明确不做（与项目判断一致）
- 不引入 DeerFlow 的多 Gateway worker / LangGraph checkpointer / 沙箱 / SSE lease 重架构（见 `11-knowledge/dream/OPENHARNESS-BRIDGE.md` 原则）。


---

## 可用性提升（P1 之后，按性价比）

1. ✅ **全局命令面板 ⌘K**（2026-09-19）：一处搜并可执行（页面/任务/批量/执行/自动化/内容/Skill/记忆/报告/预设）。
2. ✅ **变更审计 + 一键回滚**（2026-09-19）：真实写入记 before/after（`run/audit-changes.jsonl`），字段级回滚（发布类不自动回滚）；`/api/audit/changes|rollback`；「变更审计」页。
3. ✅ **统一收件箱**（2026-09-19）：系统阻断/待办/失败任务/待授权发布/待执行方案 集中一屏；`/api/inbox`；nav 角标。
4. ✅ **失败摘要 + 一键重试全部失败项**（2026-09-19）：`failure_digest()` 按原因归类（缺主题/文档缺失/LLM余额/查询失败/结构门禁/超时/限流/无对象/系统内部错误）并给人话建议；`/api/batch/failures`、`/api/batch/retry_all`（scope=task|all）；批量详情失败摘要卡 + 批量页「重试所有失败项」+ 收件箱内联重试。实测：5 个卡死任务 9 项一键重试 → 首个任务 2/2 完成（质检通过）。
5. ✅ **空状态 CTA 全覆盖**（2026-09-19）：新增 emptyBox 组件，17+ 处空态从『只有文字』改为『图标+说明+一键动作』（批量/QA/Loop/样式/分发/管线/项目/维护/预设/KB/报告等）。
6. ✅ **窄屏/移动端适配**（2026-09-19）：≤900px 侧栏浮层+遮罩、主区自适应；表格/看板/面板/抽屉单列；≤620px 指标两列、命令面板全宽。
7. ✅ **出站 Webhook**（2026-09-19）：run/webhooks.json + 事件（task/run/automation/rollback），可选 HMAC，后台投递+日志；设置页管理/测试。实测 task.done → HTTP 200。

### 知识库 / RAG（2026-09-19）
- ✅ 知识中台可视化重构（左筛选 + 右宽结果 + 检索底座状态卡）。
- ✅ RAG 底座：可插拔 embedding（配了用远程，未配用本地 TF-IDF）+ 混合检索（RRF）+ `semantic_search` 工具。
- ⏳ 真实 embedding 待配置（见 `docs/rag-plan.md`，一步开启）。


---

## 自动化剧本 Playbook（2026-09-20）
把"定时单步自动化"升级为**多步 + 条件 + 触发器**，执行走 Run 画布：
- 存储 `run/playbooks.json`；模板 `templates/playbooks.json`（6 个）。
- 步骤：preset / spec / guard（条件）/ verify；触发器：schedule / event / manual。
- 端点 `/api/playbooks`、`save|delete|run|install`；UI 在「自动化」页。
- 实测：每日 QA 闭环 → QA扫描 → findings>0 成立 → 字段修复 → 验证（100%）。

### 后续（更智能/自进化）
- 剧本分支（if/else）与步骤级重试/超时。
- 失败与结果 → 自动提炼规则/禁用词；质量趋势 → 自动调参；自检 block 自动修复；记忆写回。
- 子代理分工（planner→workers→reviewer）并发；RAG rerank；命令面板最近/收藏。


---

### 自愈 / 自进化 / 易用敏捷（2026-09-20）

**自愈**：`selfcheck_autofix()` 一键修复自检中带安全动作的项（熔断/卡住任务/维护/RAG 索引/失败重试）；后台 `selfheal_tick()` 每 ~10 分钟静默自愈；自检新增 RAG 索引项。端点 `POST /api/selfcheck/autofix`。

**自我进化**：`learn_from_failures(days)` 聚合近期失败类别 → 生成学习项（含建议动作），落 `run/learnings.json`；`POST /api/learnings/scan`、`GET /api/learnings`；可复用 `self_evolve_apply` 生成提示词提示/禁用词。

**更易用 / 更敏捷**：
- 命令面板 **收藏（★）+ 最近使用**（localStorage，空查询时置顶）。
- **全局快捷键**：`⌘K`/`/` 搜索面板、`?` 帮助、`g h/i/a/r/b/t/m/s/c/q/l/k/d` 快速导航、`Esc` 关闭。
- **帮助浮层**（12 条快捷键）。


---

### MCP 开放 / 自进化闭环 / OPC（2026-09-20）
- **MCP 服务**：`1-4 Dev/scripts/mcp_server.py`（纯标准库 stdio JSON-RPC），17 个工具；端点 `GET /api/mcp/tools`、`POST /api/mcp/tool`（`X-MFlow-Token` 或 admin）。动作类工具**强制 dry-run**。文档 `docs/mcp.md`。
- **开放接入页**：设置页显示 机器 token / MCP 工具数 / 脚本 / 文档 / REST 说明。
- **自进化闭环**：`POST /api/learnings/apply|ignore`；需人工复核的项拒绝自动应用（不盲自动化）。
- **OPC**：`POST /api/playbooks/enable_recommended` 一键安装并启用推荐剧本（每日 QA / 每周衰减 / 每周 alt / 每周 GEO）。
- **关键修复**：系统执行者（`schedule`/`automation`/`mcp`/`playbook`/`onboard`/`selfheal`）**不再计入用户配额**——此前被默认 500 条上限打满导致 health=bad 且自动化被自身配额卡死。
