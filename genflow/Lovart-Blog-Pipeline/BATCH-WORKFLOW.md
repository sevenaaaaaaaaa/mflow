# Lovart Blog Batch Production Workflow

> 用户确认：按批生产，不逐篇等待确认；禁止内容缩水。

## 每篇硬性验收（不通过不进入下一篇）

| 检查项 | 标准 |
|--------|------|
| 词数 | **≥ 7,500 words**（全分类统一地板，2026-07-17；旧 Comparison/101/How-To 分档已废止；`<7500` 不得标 ready） |
| frontmatter | 见 `LOVART-BLOG-LOCAL-SPEC.md` |
| 封面 | `python3 scripts/pick-cover.py <slug>`，写入 `cover_url` |
| 必含块 | Derivative Scenarios、FAQ、E-E-A-T、Internal Links、Image Appendix、footer cluster |
| 内链 | 仅 verified slugs + signup + pricing |
| 保存 | `01-Drafts/comparison-{slug}.md` |

## 批次节奏（Batch 1 竞品对比 #1–23）

- 每对话优先完成 **2–4 篇**（视上下文），单篇不达标则扩写后再继续
- 完成后更新 `PRODUCTION-PLAN.md` 状态为 `draft-done (~Nw)`
- 不在同一封面 URL 重复分配（slug 哈希碰撞时手动改 `cover_url`）

## 当前进度

见 `PRODUCTION-PLAN.md`（93 行清单）。**2026-05-26：** 93/93 已标 `draft-done`（Branding/Insight 约 2800w，系统目标 3000w 可再润色；101-4–15 建议人工去模板感）。
