---
type: session-log
session_date: 2026-09-17
session_slug: warning-tests-p16
status: ready
---

# Session Log — Phase 16 配额预警（T6）+ 自动化测试（T4）

## T6 配额预警
- `usage_add` 内置阈值检查：≥80% ⚠ / ≥100% ⛔ → `notify_send` 飞书通知（含用户/指标/用量/百分比 + 处置建议）
- 去重：`warned` 标记（每用户 × 指标 × 每月 × 每档只发一次）→ 实测 5 条配额下 4 条触发 80%、第 5 条触发 100%、tokens 90% 触发 80%（3 条通知，无刷屏）
- 健康报告新增 `quota_alerts`（≥80% 即入），并在总览健康卡展示；级别升 warn/bad
- UI：设置页配额表按 80%/100% 标黄/标红

## T4 自动化测试
- `1-4 Dev/tests/test_console_units.py`：**21 用例**，纯 stdlib unittest，离线 ~3 秒
  覆盖：spec_guard（5）· 熔断（4）· 配额（5）· 降噪幂等（1）· 上下文预算（3）· 预设（3）
- `1-4 Dev/scripts/run-tests.sh` 一键运行（自动用项目 venv；本地缺 markdown 时注入 stub）
- 接入 **session-init GATE 6**：失败即门禁不过 → `sync.sh` 发布链路会自动被挡
- 线上验证：GATE 6 通过（21 用例）

## 踩坑
- `run-tests.sh` 与 `tests/` 未在 sync 清单 → 服务器 GATE 6 直接失败（"No such file"）→ 已补清单（含 run-tests.sh 单文件）
- 通过 ssh 传内联中文 Python 在 py3.6 上 encoding 报错 → 改为传脚本文件执行（老坑，再次印证：远端执行一律用文件）

## 剩余欠账（矩阵）
T1 发布器仅支持 blog（落地页整页发布未做）· T2 内容库增量同步 · T7 执行器端到端测试（临时目录+假 Sanity 端点）
