---
type: session-log
session_date: 2026-09-17
session_slug: agent-console-p12-2
status: ready
---

# Session Log — Phase 12.2 Agent 任务台（对话→规格→执行）

## 交付
1. **对话链路**：上下文组装 → LLM 规划器（严格 JSON：say/questions/spec）→ 规格门禁 → 用户批准 → 复用 P12.3 批量执行器 → 结果回流
2. **上下文注入三类**：
   - harness 规则摘要（RULES-*.md 的编号/项目符号「禁止·必须·不可·一律·永远·不得」条款，≤4000 字符）
   - skills（45 个 SKILL.md → 名称+描述+分组；关键词重合 Top5）
   - 内容库命中（文件名+正文头）+ GEO 缺口
3. **规格门禁 spec_guard**：类型白名单（4 类）· 字段白名单 · 规模上限（物料/字段 ≤200；生成/改稿 ≤20）· **dry-run 默认** · 真实执行需 force（UI 二次确认）
4. **工作台「Agent 任务台」页**：会话列表 / 对话线程 / 上下文可见（skills·库命中·规则字符数）/ 规格卡（条目预览 + 批准 dry-run + 真实执行）/ 结果回流（含 task_id）
5. **API** `/api/agent/{sessions,session,chat,execute}`；文档 `docs/agent.md`

## 实测（线上真实）
| 用例 | 结果 |
|------|------|
| "帮我改一下落地页的图片" | ✅ 反问 2 条 + spec=null + 明确不编造 doc_id；上下文 4 skills / 规则 1320 字符 |
| 补充信息后（2 个 doc 的 seoTitle） | ✅ 产出 field_patch 规格（2 项 dry_run=true），say 中引用 RULES-20 slug 关键词提醒 |
| 批准执行 dry-run | ✅ 任务 2/2 done，回流对话 |
| 未 force 真实执行 | ✅ 拒绝 |
| 非法类型 delete_everything | ✅ 拒绝 |

## 踩坑
- 规则摘要初版只匹配 `- ` 项目符号 → RULES 用编号列表，仅得 635 字符；修后 1320 字符（并按 frontmatter 剥离+关键词过滤）
- 规划器偏保守（库命中只认出 1/2 个 doc 时选择反问）——**这是正确行为**（不编造），但提示词可补一句"若用户已明确给出 doc_id 可采信"

## 能力矩阵已建立
`docs/capability-matrix.md`（15 项目标能力 × 现状 × 缺口 × 依赖 + 用户侧待办 U1-U6 + 工程欠账 T1-T4）——治"没一开始对齐目标"的根因。

## 下一步
- P12.4 QA 编排；或先做 U4（物料真实替换 pilot，占位图被用 7,204 次）与 U6（第一个真实批量任务）
