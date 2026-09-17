# Agent 任务台（对话 → 任务规格 → 执行）

> 位置：工作台「Agent 任务台」。定位：把"自然语言需求"翻译成**可执行、可审计、受门禁约束**的批量任务。
> 边界：规划器不直接写生产库；所有规格默认 dry-run；真实执行需显式确认（force）并留审计。

## 一轮对话的完整链路

```
用户消息
  → 上下文组装（harness 规则摘要 + 相关 skills + 内容库命中 + GEO 缺口）
  → LLM 规划器（输出严格 JSON：say / questions / spec）
  → 规格门禁 spec_guard（类型白名单 · 字段白名单 · 规模上限 · dry-run 强制）
  → 用户批准（dry-run / 真实执行 force）
  → 批量任务执行器执行（P12.3）→ 结果回流对话 + 批量任务页
```

## 上下文注入（三类）

| 类型 | 来源 | 用途 |
|------|------|------|
| **harness 规则** | `1-1 Harness/02-rules/RULES-*.md` 中编号/项目符号的「禁止/必须/不可/一律/永远/不得」条款（≤4000 字符） | 规划时约束方案；执行侧同样由门禁强制 |
| **skills** | `1-1 Harness/Skills/**/SKILL.md`（45 个，名称+描述+分组），按关键词重合度取 Top5 | 让规划器理解流程规范；结果显示 `skills_used` |
| **内容库 + GEO** | `run/library/{site}/**` 命中（文件名+正文头 500 字符）；`geo_summary` 的缺口查询 | 定位真实对象（doc_id/slug/path），避免编造 |

> 规划器被明确要求：**不确定就反问、不编造 doc_id/数字**。实测有效（"帮我改一下落地页的图片"→ 反问 2 条，未编造规格）。

## 规格门禁（硬约束）

| 规则 | 说明 |
|------|------|
| 类型白名单 | 仅 `asset_replace` / `field_patch` / `gen` / `rewrite` |
| 字段白名单 | 每类 items 只允许既定字段，多一个即拒绝 |
| 规模上限 | asset_replace/field_patch ≤200 项；gen/rewrite ≤20 项 |
| dry-run 强制 | 规格默认 `dry_run=true`；真实执行必须 `force=true`（UI 二次确认）且记审计 |
| 无副作用原则 | 规划器不直接调用写接口——只产出规格，写入统一走批量执行器 |

## API

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/agent/sessions` · `/api/agent/session?id=` | 会话列表 / 详情 |
| POST | `/api/agent/chat` | `{session_id?, message}` → `{say, questions, spec, guard_error, context}` |
| POST | `/api/agent/execute` | `{session_id, spec, force}` → 创建批量任务 |

## 实测（2026-09-17）

| 用例 | 结果 |
|------|------|
| "帮我改一下落地页的图片"（信息不足） | ✅ 反问 2 条、`spec=null`、明确声明不会编造 doc_id；上下文：4 skills / 规则 1320 字符 |
| 具体 SEO 标题改写（2 个 doc） | ✅ 产出 `field_patch` 规格（2 项，dry_run=true），并在 say 里引用 RULES-20 的 slug 关键词提醒 |
| 批准执行（dry-run） | ✅ 任务 `batch-…` 2/2 done，结果回流对话 |
| 真实执行但未 force | ✅ 拒绝："真实执行需显式确认" |
| 非法类型 `delete_everything` | ✅ 拒绝："不允许的任务类型" |

## 与其它模块的关系

- **复用** P12.3 批量执行器（4 类执行器、并发、重试、暂停续跑、审计）
- **约束来自** harness 规则（规划时注入 + 执行时门禁）
- **上下文来自** 内容库（P11 多站点镜像）与 GEO 闭环（P6/7）
- **不做**：不代替人做发布授权；不自动改生产库；不发明任务类型
