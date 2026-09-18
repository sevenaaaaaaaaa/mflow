---
name: lovart-content-calendar
description: Step 2 of Lovart Content Pipeline — 根据 intelligence-brief 分析结果，更新主站点（lovart.ai/blog via Sanity）、子站点（blogs.lovart.ai via WordPress）、分发平台的内容日历。
---

# lovart-content-calendar

## 路径契约

| 层 | 路径 |
|----|------|
| 文档 SSOT | `1-1 GEO Readme/` |
| Sanity 脚本 | `1-4 Dev/lovart.sanity.studio/scripts/` |
| SEO/Sentinel 脚本 | `1-4 Dev/scripts/` |
| 自动化 | `1-4 Dev/automation/` |
| 本 Skill | `1-1 Harness/Skills/lovart-content-calendar/SKILL.md` |

Step 2 of Lovart Content Pipeline — 根据 intelligence-brief 分析结果，更新主站点（lovart.ai/blog via Sanity）、子站点（blogs.lovart.ai via WordPress）、分发平台的内容日历。

## Triggers

- "更新内容日历" / "update content calendar"
- "安排本周内容" / "plan this week's content"
- "内容排期" / "content scheduling"
- Pipeline Orchestrator 调用 Step 2

## Prerequisites

- Step 1 (`lovart-data-ingestion`) 已完成，`1-2 Insight/Trident Insights/reports/YYYY-MM-DD/intelligence-brief.md` 存在
- Content Calendar 目录结构存在：`1-3 Content Gen/Content Calendar/`
- 关键词分类委托给 `lovart-keywords-intake`（旧版 v1.0，8 种分类器）
- 内容类型矩阵来自 `lovart-content-writer`（v4.0，12 类型 x 11 框架）

## Workflow (sequential)

### Phase 1: 读取情报摘要

```bash
cat "1-2 Insight/Trident Insights/reports/$(date +%Y-%m-%d)/intelligence-brief.md"
```

提取以下决策信号：
- 上升关键词 → 优先产出相关内容
- 下降关键词 → 需要内容刷新或新角度
- 竞品动态 → 需要响应性内容
- 内容缺口 → 新选题来源

### Phase 2: 扫描现有日历状态

遍历 14 个品类目录，统计状态（实际路径：`1-3 Content Gen/Content Calendar/`）：

| # | 品类 | 翻译 |
|---|------|------|
| 01 | How-To | en/zh/ja/zhtw/pt/ru |
| 02 | Comparison | en/zh/ja/zhtw/pt/ru |
| 03 | Industry-Segment | en/zh/ja/zhtw |
| 04 | Career | en/zh/ja/zhtw |
| 05 | Insight-Trend | en/zh/ja/zhtw |
| 06 | Case-Study | en/zh/ja/zhtw |
| 07 | Seasonal | en/zh/ja/zhtw |
| 08 | Best-Practice | en/zh/ja/zhtw |
| 09 | Better-Design | en/zh/ja/zhtw |
| 10 | Ethics-Legal | en/zh/ja/zhtw |
| 11 | Programmatic-SEO | en/zh/ja/zhtw/pt/ru |
| 12 | Digest | en/zh/ja/zhtw |
| 13 | Onboarding | en/zh/ja/zhtw |
| 14 | Product-Update | en/zh/ja/zhtw |

**统计方法**（per category）：
```bash
find "1-3 Content Gen/Content Calendar/01-How-To/" \
  -name "*.md" ! -name "*-ja.md" ! -name "*-zh.md" ! -name "*-zhtw.md" ! -name "*-pt.md" ! -name "*-ru.md" | wc -l
```

### Phase 3: 更新三大日历

#### 3.1 主站日历（Sanity — lovart.ai/blog）

Sanity 博客面向全球用户，优先级：
1. **SEO 驱动**：关键词上升 → 加速对应 cluster 的文章产出
2. **产品驱动**：新功能发布 → 产品更新 + How-To 文章
3. **竞品驱动**：竞品有重大更新 → Comparison 文章

输出到 `Output/Content Calendar/sanity-calendar-YYYY-WW.md`：

```markdown
# Sanity Blog Calendar — Week WW

| 优先级 | Slug | 类型 | 语言 | 状态 | 依据 |
|--------|------|------|------|------|------|
| P0 | {slug} | How-To | en,zh,ja | 待写 | 关键词 "{kw}" 上升 +15 位 |
| P1 | {slug} | Comparison | en,zh | 待写 | 竞品 {X} 发布新功能 |
| P2 | {slug} | Best Practice | en | 翻译 | 仅有英文，缺 zh/ja |
```

#### 3.2 子站日历（WordPress — blogs.lovart.ai）

WordPress 博客侧重 SEO 长尾流量，优先级：
1. **Programmatic SEO**：批量工具对比、行业方案
2. **长尾关键词**：Content Calendar 中的 Bing SEO 系列
3. **内容刷新**：过期文章的更新版本

输出到 `Output/Content Calendar/wordpress-calendar-YYYY-WW.md`

#### 3.3 分发平台日历

| 平台 | 内容类型 | 频率 | 来源 |
|------|---------|------|------|
| X/Twitter | 功能亮点 + 博客摘要 | 3/周 | 从博客提取 |
| LinkedIn | 行业洞察 + 产品更新 | 2/周 | 从 Insight/Product Update 提取 |
| Product Hunt | 版本更新通知 | 按需 | 产品更新 |
| Discord | 教程 + 社区互动 | 5/周 | 从 How-To 提取 |
| 小红书 | 设计教程（中文） | 3/周 | 从中文博客提取 |
| YouTube | 视频教程 | 1/周 | 从 How-To 改编 |

输出到 `Output/Content Calendar/distribution-calendar-YYYY-WW.md`

### Phase 4: 生成创作任务清单

将三大日历合并为统一的 **创作任务清单**，标注每篇内容应调用哪个创作 skill：

```
Output/Content Calendar/
└── creation-tasks-YYYY-WW.md
```

```markdown
# Creation Tasks — Week WW

## Sanity Blog (lovart.ai)
- [ ] `{slug}` → 调用 `lovart-content-writer` (type: blog)

## Features Page
- [ ] `{slug}` → 调用 `lovart-features-page` (type: feature)

## Tools Page
- [ ] `{slug}` → (tools JSON 生成)

## Landing Page
- [ ] `{slug}` → 调用 `lovart-landing-page`

## WordPress Blog (blogs.lovart.ai)
- [ ] `{slug}` → 调用 `lovart-blog-automation`

## Distribution
- [ ] X thread from `{slug}` → 分发草稿生成
- [ ] LinkedIn article from `{slug}` → 分发草稿生成
- [ ] 小红书 from `{slug}` → 分发草稿生成
```

## Output

```
Output/Content Calendar/
├── sanity-calendar-YYYY-WW.md
├── wordpress-calendar-YYYY-WW.md
├── distribution-calendar-YYYY-WW.md
└── creation-tasks-YYYY-WW.md        ← 下游 Step 3 的输入
```

## Downstream

完成后自动触发 → `lovart-content-writer` / `lovart-features-page` / `lovart-blog-automation` (Step 3)


## 预算（RULES-70 强制）

本 skill 产出同样受 RULES-70 数量预算约束。

- **必须**过质量门禁（post-write-check + geo-check）

- **禁止**绕过质量门禁直接发布
