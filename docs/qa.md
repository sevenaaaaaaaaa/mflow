# QA 编排（扫描 → findings → 修复任务 → 复检）

> 位置：工作台「QA 编排」。目标：把质检从"单文件手工跑"变成"批量扫描 + 可执行修复 + 闭环复检"。

## 闭环

```
① 扫描（批量 QA 任务）
    ├─ kind=sanity：字段规则（确定性，不需 LLM）
    └─ kind=md    ：门禁钩子（post-write-check + geo-check）
② findings（结构化）
    {target, rule, severity(block|warn), detail, fix{type, set/…}}
③ 编排修复（一键）
    字段问题 → field_patch 任务
    alt 缺失 → asset_replace 任务
    草稿 block → rewrite 任务
    全部走 P12.3 批量执行器（并发/重试/暂停/dry-run/审计）
④ 复检
    同目标新建 QA 任务（parent 指向原任务）→ qa_delta 对比
    输出：已解决 N 项 / 新增 M 项 / 修复前后严重度分布
```

## 字段规则（确定性，v1）

| 规则 | 判定 | 修复建议 |
|------|------|---------|
| `seoTitle.missing` | 空 | 用 title 截断（CJK 30 / 其他 60 字符） |
| `seoTitle.too_long` | 超限 | 按词边界截断 |
| `description.missing` | description 与 seo.description 都空 | 用 title 生成 |
| `description.too_long` | 超限（CJK 80 / 其他 160） | 截断 |
| `cover.alt_missing` | 有 cover.url 无 alt | 用 title 作 alt（asset_replace） |
| 草稿钩子 | post-write-check / geo-check 的 ✗（block）与 !（warn） | block → 生成 rewrite 任务 |

## API

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/qa/create?kind=sanity-filter&page_type=&lang=&max=` | 建扫描任务（服务端展开范围；`kind=drafts` 扫本项目草稿） |
| GET | `/api/qa/tasks` · `/api/qa/findings?task=` | QA 任务列表 / findings 汇总（含 fixable 计数） |
| GET | `/api/qa/cycles` · `/api/qa/delta?parent=&child=` | 闭环历史 / 复检对比 |
| POST | `/api/qa/orchestrate` | `{task, dry_run}` → 生成修复任务（可按类型拆多个） |
| POST | `/api/qa/recheck` | `{task, dry_run}` → 新建复检任务（parent 关联） |

## 实测（2026-09-17，真实 Sanity 数据）

| 步骤 | 结果 |
|------|------|
| 扫描 tools/en 前 60 篇 | 60/60 done，**84 findings**（seoTitle.missing 60 + description.too_long 24），**全部带可执行修复** |
| 编排修复（dry-run） | 生成 `field_patch` 任务：84/84 done |
| 复检 | 新建同目标 QA 任务 → delta：修复前 84 → 复检 84、已解决 0（**dry-run 未写库，如实报告未闭环，不伪造**） |

## 与其它模块关系

- **执行**：复用 P12.3 批量执行器（并发/重试/暂停/续跑/审计）
- **可被 Agent 调用**：Agent 任务台已支持 `qa` 类型（items: `{kind:"sanity"|"md", doc_id|path}`）
- **修复动作**：字段/物料类走确定性规则（无需 LLM、零成本、可预测）；草稿类走 rewrite（LLM）
- **铁律**：生产写入默认 dry-run；真实修复需显式批准并记审计
