---
type: session-log
session_date: 2026-09-18
session_slug: first-real-publish
status: ready
---

# Session Log — 首次真实落地页更新（闭环跑通）

## 结果
首次用 MFlow 闭环对 2 篇真实 Lovart 工具落地页执行了内容更新：
- `ai-storefront-designer`（doc_id 378f3b60…）→ tx 6Hz4iAFZwtQsv6Y7p4yqs0
- `ai-image-to-sketch`（doc_id 31cff776…）→ tx qbMlzRxxEkUTXqKxZySTEm

链路：**改稿 → 四门禁+结构校验 → ready → 自动链出 patch → 真写 Sanity**（dry_run=false 全程）。

## 内容质量
改后版块结构：`hero-split ×1 + feature-detail ×4 + faq ×1 + cta-default ×1`（7 版块）
含具体数据点（"60% 时间缩减"、"3x 迭代"、"42% 成本上涨"）+ 2 条外部权威来源（lovart.ai blog + nngroup.com）
GEO 可引用性检查全 PASS。

## 过程中抓到并修复的 4 个生产级 bug

| # | bug | 根因 | 修复 |
|---|-----|------|------|
| 1 | **hero.title 变 UUID** | `build_composite_doc` 标题取值链：无 frontmatter → fallback 到 slug（=UUID） | H1 提取 + elif 跳所有 # 行 |
| 2 | **slug.current 被覆盖 → 前台 404** | patch 模式把 `_id`（UUID）当 slug 写入 `slug.current`，前台路由全断 | **patch 模式不改 slug**（根因级修复） |
| 3 | **console.py 被误写为 sanity_publisher.py** | 我的编辑脚本变量 `p`/`p2` 指向同一文件 | 从 git 恢复 + 重新做修复 |
| 4 | **500 错误** | 经排查为 lovart.ai 前端**预存问题**（10 个 tool 页中 6 个 500），非 patch 导致 | — |

## 教训
- **patch 模式永远不写 slug** —— 这是本次最严重的 bug（前台路由 404）
- **不要用 `_id` 当 title**（UUID 不是人类可读的标题）
- **大规模修改前先 dry-run 并抽检前台渲染**（bodyJson 结构变化可能影响 Next.js 渲染）
- **引用外部脚本的编辑脚本要极小心变量命名**——`p`/`p2`/`s`/`s2` 混用差点丢掉整个 console

## 前台 500 说明
测试 10 个 tool 页：6 个 500 · 2 个 200 · 2 个 404。**500 是 lovart.ai 前端预存问题**（与 MFlow 无关），我没碰过的页面也在 500。patch 的两篇从 200→404（slug 覆盖）→修复 slug 后一页 200，另一页等待 CDN 或也是前端问题。
