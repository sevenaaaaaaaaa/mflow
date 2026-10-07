---
type: session-log
session_date: 2026-09-17
session_slug: breaker-quota-p15
status: ready
---

# Session Log — Phase 15 熔断（T3）+ 按用户配额（T5）

## 交付
**T3 熔断**
- 任务级：单批连续失败 ≥5（`fail_threshold`）→ 任务 `tripped` 暂停 + 通知 + 可重试
- 致命错误：连续 2 次命中（401/403/invalid key/insufficient/balance/quota/unauthorized）→ 立即 `tripped` **并全局熔断 30 分钟**
- 全局：熔断期 worker 不领任何任务；冷却后半开自动复位；`GET /api/breaker` / `POST /api/breaker/reset`；UI 熔断状态卡 + 批量任务页告警条

**T5 配额与用量**
- 计量 `run/users-usage.json`：按月 tasks/items/tokens/writes；tokens 取真实 usage（含重试轮）
- 配额 `run/quotas.json`：默认 500 条 / 500k tokens / 200 真实写入；admin 不限；per_user 覆盖（`unlimited` 解除）
- 拦截：**建任务前** 429 + 明确提示（批量/预设/Agent 规格/QA 编排/复检 全覆盖）
- UI：设置页「用户配额与用量」表 + 改配额

## 实测（线上）
| 用例 | 结果 |
|------|------|
| 错误 Key 建 gen 任务 | 任务 `tripped`，全局熔断 reason=致命错误 HTTP 401，冷却 30 分钟 ✅ |
| 恢复 Key + 手动解除 | 解除成功，LLM 连通 OK ✅ |
| admin 设 1 条配额建 3 项 | 仍通过（admin 不限）✅ |
| mflow 建 3 项 QA（dry-run） | 用量 tasks=1/items=3/tokens=0/writes=0（dry-run 不计写入）✅ |
| LLM test | OK ✅ |

## 踩坑
1. 熔断初版判定 `status=="failed"` → 漏判：失败项在 max_attempts 内会被重置为 pending（状态非 failed）→ 改为**按本轮 error 计连续失败**
2. 批量改脚本时误用 `str.replace('        ','')` 删掉一处缩进 → session-init 的 ast 门禁没拦（语法检查前就被 Python 抓）——教训：批量替换空格很危险，宁可用精确锚点

## 清理
测试任务 4 个、管线条目 5 条、breaker.json 已清；配额测试覆盖已还原（mflow/marketing → unlimited）
