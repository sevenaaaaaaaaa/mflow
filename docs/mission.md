# 任务全景（Mission Control）

> 新人入口。侧栏「工作台 → 任务全景」，总览页右上角也有入口。

## 解决什么
新人进系统看不懂：正在执行什么、过程到哪了、产出在哪、为什么做、要多久、收益是什么、QA 和流量反馈如何。
原因是同一件事被拆在 执行画布 / 批量任务 / Loop / QA / 分发 / 报告 多个页面。

## 页面结构
1. **30 秒读懂 MFlow**：一句话 + 6 环链路（情报→决策→生产→门禁→发布→回测），每环带实时数字，点击跳对应页；术语表（dry-run / 待授权 / 门禁 / 多步执行 / 批量 / Loop）。可收起。
2. **KPI 条**：执行中 · 排队 · 失败待处理 · 预演完成待授权 · 今日完成 · 产出 URL · QA 通过率 · 有流量的产出。
3. **任务卡**（Run / 批量 / Loop 统一）：每张卡固定回答 —— 为什么做（原始需求 + 触发来源）· 在做什么 · 要多久（已用 / 剩余 / 同类历史中位数）· 收益与反馈（预期收益 + QA 门禁结果 + GSC 流量）。展开看步骤、主要问题、产出预览表、最近日志，并可下钻到原页面。
4. **产出 URL 汇总**：全部前台链接与草稿，含状态、QA、点击/展示/排名、来源任务；一键复制、导出 CSV。

## 数据口径
| 项 | 来源 |
|---|---|
| 任务 | `run/runs/run-*.json`（含其子批量，不重复出卡）、`run/batch/batch-*.json`、`run/projects/*/loops.json` |
| 为什么 | Run 的 `message` / 剧本 `desc`；批量的 `params.reason|goal`、`from_qa`、标题里的「源 batch-x」、`created_by`；Loop 的 `brief`；都没有时用类型默认动机 |
| 耗时 | 执行中按当前速度外推；否则用同类型已完成批量的单条耗时中位数；无样本用经验值 |
| QA | 条目结果里的 hook/geo/quota/lang rc、落地页结构校验、QA block/warn；失败归因复用 `failure_digest` |
| 流量 | 本地 GSC 页面快照 `gsc-5k-*.json`（1000 页/月）+ `gsc-full.json`（Top20），按「域名去 www + 路径去尾斜杠」匹配。**不在快照里 = 暂无，不是 0** |

「预演完成·待授权」= dry-run 完成未写库；生效需人工关掉 dry-run 重跑（发布人工授权不可协商）。

## 实现
- `dev/console/mission.py`：纯只读聚合，零网络、零写盘；`build(globals(), proj)` + `outputs_csv()`。不往 console.py 堆逻辑。
- 路由：`GET /api/mission`、`GET /api/mission/export`（CSV，UTF-8 BOM，Excel 直接打开）。
- 前端：`console.html` 中 `msn-*` 前缀（`mc-*` 已被小 M 助手占用）。
- 单测：`dev/tests/test_mission.py`（10 例：空数据、七问字段、dry-run=待授权、Run 吸收子批量、ETA、Loop、流量路径匹配、坏文件容错、零副作用、CSV）。

## 已知局限
- 流量只到 GSC 页面级快照，覆盖有限；GA4 转化、AI 引用尚未按 URL 并入卡片。
- 收益是「预期」+「已观测流量」，不做因果归因（改前/改后对比待做）。
- 批量任务没有 `proj` 字段，目前展示全部项目的任务。
