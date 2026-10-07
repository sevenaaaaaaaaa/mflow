---
type: session-log
session_date: 2026-09-17
session_slug: onboarding-stability-p14
status: ready
---

# Session Log — 0 门槛与稳定性（Phase 14）

## 用户问题
① 让更多人 0 门槛使用（对话加内容、做 QA、搭新工作流）——提前配置好什么？
② 稳定性差、agent 越用噪音越多——产品机制上怎么防？

## 诊断（实测）
噪音源与现状：管线终态/僵尸条目/批量任务文件/agent 会话/citations 只增不减；规则全量注入占上下文；
iCloud 重复文件；无健康视图。（当时 run/ 241MB，其中 library 224MB）

## 交付
**P14.1 预设工作流（0 门槛核心）**
- `templates/presets.json` 7 个：GEO 缺口改稿 / 高曝光低 CTR 刷新 / 衰减页刷新 / QA 字段修复 / 封面 alt 补齐 / 例行 QA 扫描 / 多语言批量产出
- 服务端 `preset_expand()` 用**真实数据**展开（geo gaps / impact rows / decay / assets 台账 / Sanity 过滤 / 主题×语言）
- `POST /api/presets/run`（admin，默认 dry-run，审计 PRESET-RUN）；UI chips + 参数弹层
- 实测：qa-field-fix(20 篇) / geo-gap-rewrite(2 条) 均正确展开建任务

**P14.2 健康与降噪治理**
- `GET /api/health`：依赖(LLM/Sanity 缓存 10min) + 队列 + 噪音(条目/终态/僵尸/任务/会话/草稿/磁盘/24h BLOCK) + 级别 ok/warn/bad；总览页健康卡
- `housekeeping()`：终态条目 >14d 归档 · 僵尸(S3-creating/draft >24h) 标记 failed · 批量任务 >14d · 会话 >30d · citations 留 200 · 孤儿草稿只报数；dry-run/幂等/审计；**每日 03:20 自动线程**
- 设置页「维护 · 降噪治理」区（预览/立即清理/历史）；实测 dry-run 与真实执行均正确（新数据全 0=幂等）

**P14.3 上下文预算**
- `context_rules(limit=1200, query=...)`：按意图相关性取 ≤4 规则文件（必含 RULES-00/70）→ 实测「质检」意图规则字符 1200（原 1320 全量）
- 库命中 ≤3；会话历史 ≤6 轮；回复展示上下文用量

**文档**：`docs/onboarding.md`（0 门槛 3 步：看健康 → 选预设 → 用对话）+ `docs/stability.md`（噪音分类表/健康/上下文预算/执行侧稳定性/日常建议）

## 待办（进矩阵 T3/T5）
- 执行器连续失败自动暂停（熔断）；按用户统计 token/任务量（防滥用）
