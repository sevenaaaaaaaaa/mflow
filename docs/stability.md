# 稳定性与降噪治理

> 问题：多人多 agent 长期使用后，"越用越噪"——条目堆积、任务文件残留、会话膨胀、规则/技能重复、
> 上下文被无关内容挤占。本文说明 MFlow 用哪些**产品机制**（而非纪律）来对抗。

## 一、噪音从哪来（实测分类）

| 噪音源 | 表现 | 治理机制 |
|--------|------|---------|
| 管线终态堆积 | done/failed/escalated 条目永久留在状态文件 | **每日降噪**：>14 天终态条目归档 `run/_archive/pipeline-YYYYMM.jsonl` |
| 僵尸条目 | S3-creating/draft 卡住 >24h | 自动标记 failed（UI 可重试） |
| 批量任务文件 | `run/batch/*.json` 只增不减 | >14 天归档 |
| Agent 会话 | `run/agent/chat-*.json` 膨胀 | >30 天归档 |
| 引用记录 | citations.jsonl 无限增长 | 只留最近 200 条，其余按月归档 |
| 孤儿草稿 | 无对应管线条目的 md | **只报数不自动删**（避免误删在途稿） |
| 规则/技能重复 | iCloud 冲突副本、重复 references | 归档副本 + `REFERENCE-INDEX.md` 单一入口 + sync `--delete` |
| 显存式上下文 | 规则全量注入挤占 token | **上下文预算**（见 §三） |

## 二、自动体检与治理

**健康检查** `GET /api/health`（总览页可见）
- 依赖：LLM 是否配 Key · Sanity 是否连通（10 分钟缓存）
- 队列：Loop 运行/排队 · 批量待执行项
- 噪音：条目总数/终态数 · 僵尸数 · 任务文件 · 会话 · 草稿 · 磁盘 · 24h 质检 BLOCK 数
- 级别：ok / warn（僵尸>3 或 终态>50 或 批量积压>30 或 磁盘>3GB）/ bad（依赖异常）

**降噪治理** `POST /api/housekeeping/run`（设置页「维护」；**每日 03:20 自动**）
- 默认 dry-run 可预览；真实执行写 `run/logs/housekeeping.log` + `approvals.log`
- 幂等：无旧数据时全 0

## 三、上下文预算（防 Agent 漂移）

| 注入项 | 预算 | 说明 |
|--------|------|------|
| harness 规则 | **≤1200 字符** | 按意图相关性只取 ≤4 个规则文件（必含 RULES-00/70） |
| skills | ≤5 个 | 关键词重合 Top5，回复展示 `skills_used` |
| 内容库命中 | ≤3 条 | 文件名匹配优先 |
| GEO 缺口 | ≤8 条 | 缺口查询 |
| 会话历史 | 最近 6 轮，每轮 ≤1500 字符 | 防历史膨胀 |

→ 规则从"全量 1320 字符"改为"相关 ≤1200"，且随意图变化（实测：质检类意图只带质检相关规则）。

## 四、执行侧稳定性

| 机制 | 说明 |
|------|------|
| 内部重试 | 生成门禁不过 → 带反馈重写 ≤3 轮（实测 2420→2159 字符后通过） |
| 失败重试 | 批量任务单项失败按 `max_attempts` 重试（默认 2） |
| 熔断（人工介入点） | 任务失败项保留 pending/failed，可「重试失败」；僵尸条目由降噪标记后人工决定 |
| 并发保护 | `PS_LOCK` 串行化 pipeline-state 读改写；批量并发 2、全局单任务 |
| 幂等 | 管线条目 upsert 幂等；Sanity 写用 `createIfNotExists` / `ifRevisionID` |
| 审计可溯 | 所有真实写操作 → `run/approvals.log`（含 preset/qa/batch/asset/publish/housekeeping） |

## 五、给运营的日常建议（不是纪律，是产品默认）

1. 每天早上看**总览健康卡**：黄/红再动手，绿就别管
2. 跑预设时**先 dry-run**，确认后再真跑
3. 真实发布前用「发布通道」的 dry-run 复核
4. 每月看一眼「维护 · 最近清理记录」确认自动治理在生效

## 六、熔断（T3，2026-09-17 上线）

| 层级 | 触发 | 行为 |
|------|------|------|
| **任务级** | 单批连续失败 ≥ `fail_threshold`（默认 5） | 任务置 `tripped` 并暂停；日志 + 飞书通知；可「重试失败」 |
| **致命错误** | 连续 2 次命中致命模式（401/403/invalid key/insufficient/balance/quota/unauthorized） | 立即熔断任务 **并触发全局熔断** 30 分钟 |
| **全局** | 熔断期间 | worker **不领取任何任务**；冷却期后自动复位（半开）；可手动解除（设置页） |

API：`GET /api/breaker`（状态）· `POST /api/breaker/reset`（admin）
实测：错误 Key → 任务 `tripped`，全局熔断 reason=`致命错误…HTTP 401`；恢复 Key + 手动解除 → 正常。

## 七、按用户配额与用量（T5，2026-09-17 上线）

**计量**（`run/users-usage.json`，按月）：`tasks / items / tokens / writes`
- 记账点：建任务（tasks）、生成类（items + 真实 tokens）、字段/物料（items + 真实写入数）、QA（items）、批量改稿（items + tokens）
- tokens 取每次 LLM 调用的真实 usage（含内部重试轮）

**配额**（`run/quotas.json`；默认 条目 500 / tokens 500k / 真实写入 200 每月）
- **admin 不限量**；`per_user` 可逐人覆盖，填 `unlimited` 解除限制
- 拦截时机：**建任务前**（配额不足 → HTTP 429 + 明确提示）；涵盖批量任务、预设、Agent 规格、QA 修复编排、复检
- UI：设置页「用户配额与用量」表（本月用量 + 配额 + 一键改配额）
- 实测：admin 设 1 条仍不限 → 正确；`mflow` 建 3 项 QA 任务后用量 `tasks=1, items=3, tokens=0, writes=0`（dry-run 不计写入）→ 正确

**为什么这两条能降低"人人可用"的风险**：配额挡住超支与滥用，熔断挡住"错误配置下的空烧"——两者都是**自动闸门**，不依赖使用者自律。
