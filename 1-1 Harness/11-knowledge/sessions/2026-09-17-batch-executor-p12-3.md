---
type: session-log
session_date: 2026-09-17
session_slug: batch-executor-p12-3
status: ready
---

# Session Log — Phase 12.3 批量任务执行器

## 交付
1. **任务模型**：`run/batch/{id}.json`（type/title/status/dry_run/concurrency/items[]/stats/log；原子写临时+rename）
2. **四类执行器**：
   - `asset_replace`：Sanity patch（cover.url/alt、coverUrl、bodyJson[].media）——`ifRevisionID` 并发保护，支持 dry-run
   - `field_patch`：任意字段改写（seoTitle/description…）
   - `gen`：LLM 生成 → 落盘 → post-write + geo 门禁 → 状态机推进
   - `rewrite`：读既有内容 → 按指令改写 → 同上（衰减页/低 CTR 页刷新）
3. **执行语义**：任务内并发 2、全局单任务；失败按 max_attempts=2 重试；暂停/继续/取消；**断点续跑**（重启自动续）；审计 approvals.log
4. **工作台「批量任务」页**：创建（4 类型 + JSON items 模板提示）/ 进度条 / 详情（条目级 status·attempts·result·error）/ 从物料计划一键建任务 / 暂停·继续·重试失败·取消
5. **API**：`/api/batch/{list,detail}`（GET）· `/api/batch/{create,action}`（POST，admin）
6. **文档** `docs/batch.md`（模型/四执行器/语义/API/典型用法/实测）

## 验证（线上真实）
- field_patch dry-run 2 条 → 2/2 done
- asset_replace（内容库计划 3 处 cover）dry-run → 3/3 done
- gen 1 篇 → 1/1 done：hook PASS + geo PASS → **推进 S4-qa**（修复后）
- 暂停→继续 4 项 gen：暂停 0/4 → 继续 4/4 done
- 测试残留全清（管线 6 条 + 草稿 6 篇 + 测试任务 4 个）

## 踩坑（重要）
- **状态机顺序**：`gen` 初版漏了 `S3-creating`，S0-todo 直达 S3-draft 被状态机拒绝 → 结果里 `advanced` 假报 true 而实际停在 S0-todo。修：先 advance S3-creating（与 Loop 引擎一致）+ 按真实 rc 判定 advanced。**教训：状态机驱动的流程，每步 advance 都要检查 rc，不能默认成功。**
- HTML 误输入全角 `＋`、JS 括号错位 → node --check 门禁逮住（门禁持续生效）

## 下一步
- **P12.2 Agent 任务台（对话入口）**：对话 → 任务规格 JSON → 复用本执行器；harness 规则注入为硬约束；skills 作为可检索上下文
- **P12.4 QA→修复编排**：QA 结果 → finding → 自动建批量修复任务 → 执行 → 复检
