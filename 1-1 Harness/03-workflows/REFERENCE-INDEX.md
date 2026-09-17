# 参考样式 / 故事线 / 约束 统一索引（SSOT）

> 用途：**一处找到所有"写页面/写文章"要用的参考与样式**，避免 agent 各拿一份互不一致的副本。
> 纪律：新增参考必须登记到本索引；发现内容重复 → 只保留一处，另一处改为指针。

## 一、故事线（Storyline SSOT）

| 资产 | 路径 | 用途 | 谁在用 |
|------|------|------|--------|
| 故事线总表 | `1-1 Harness/08-storyline/STORYLINES.md` | 7 类页面 × 25 条故事线定义 | 所有页面生成 skill |
| 方向索引 | `1-1 Harness/08-storyline/STORYLINE-BY-DIRECTION.md` | 按投放方向选故事线 | landing/投放向 |
| Features 生产规范 | `1-1 Harness/08-storyline/FEATURES-PRODUCTION.md` | Features 页专用结构 | features |
| landing 故事线 JSON | 由 `lovart-landing-page` skill 引用（`landing-storylines.json`，随 skill references 提供） | 7 条投放故事线的机读定义 | landing-page skill |

## 二、页面/文章模板与结构（按页面类型）

| 页面类型 | 模板/结构参考 | 位置 |
|---------|--------------|------|
| 落地页（Tools/Landing/Features） | `landing-v2-template.md` | `Skills/02-creation/lovart-landing-page/references/` |
| 落地页文案约束（SSOT） | `landing-copy-constraints-ssot.md` | 同上 |
| 卡片标题↔图映射 | `card-title-image-mapping.md` | 同上 |
| 图池（已校验） | `verified-image-pool-2026-06.md` | 同上 |
| 图池拉取脚本 | `image_pool.py` | 同上 |
| Blog（SERP 向） | `lovart-blog-serp-writer` SKILL + references | `Skills/02-creation/lovart-blog-serp-writer/` |
| Blog（信号/长文） | `lovart-blog-signal-writer` SKILL + references | `Skills/02-creation/lovart-blog-signal-writer/` |
| 101 / Complete Guide / Stack-by-stack / Best Practice / Insight&Trend / Thought Leadership | 各自 `references/` 下模板与样例 | `Skills/02-creation/*/references/` |
| 页面刷新（存量改稿） | `refresh-page-page-generator` SKILL | `Skills/02-creation/refresh-page-page-generator/` |
| 自媒体长文（外部平台） | `ai-self-media-article` SKILL + 14 references | `Skills/04-publish/ai-self-media-article/` |

## 三、创作方法论与质量参考

| 资产 | 路径 | 用途 |
|------|------|------|
| Better Design 方法论 | `Skills/lovart-better-design/SKILL.md` | 研究协议/信源分级/voice/反 slop/伦理披露 |
| Better Design Playbook | `Skills/lovart-better-design/references/lovart-better-design-playbook.md` | 操作手册 |
| 审查清单 | `.../references/lovart-better-design-review-checklist.md` | 自检 |
| Benchmark 种子 v1-v3 | `.../references/benchmark-seed-v1|v2|v3.md` | 对标基线（用最新的 v3） |
| Anti-Slop Preflight 门 | `Skills/06-orchestrate/lovart-content-creation-orchestrator/references/preflight-anti-slop-gates.md` | 硬门 |
| 质量门总表 | `.../references/quality-gates.md` | 三层门禁 |
| 内容样例库 | `.../references/content-sample-library.md` | 正向样例 |
| 内容台账 | `.../references/content-production-ledger.md` | 进度口径 |
| 路由规则（Blog/Page/Scenarios） | `.../references/blog-routing.md` / `page-routing.md` / `scenarios-routing.md` | 派工 |
| 本地化规范 | `.../references/i18n-localization.md` | 多语言（与 RULES-80 配套） |
| 反馈闭环 | `.../references/content-feedback-loop.md` | 回流 |
| SERP 与竞品来源 | `.../references/serp-and-competitor-sources.md` | 情报 |

## 四、主题与写作方法论（策略层）

| 资产 | 路径 |
|------|------|
| 内容策略（漏斗/季节/行业/职业/企业/复用/伦理） | `1-3 GenFlow/Content Strategy/*.md` |
| 关键词研究与竞品词 | `1-2 Insight/Keywords Research/**` |
| 写作方法论（bv-skill-v01） | `1-3 GenFlow/bv-skill-v01/*.md` |

## 五、约束与规则（写之前必读）

| 规则 | 路径 | 说明 |
|------|------|------|
| 全局铁律 | `1-1 Harness/02-rules/RULES-00-iron.md` | 不可违反 |
| 创作规则 | `RULES-20-creation.md` | 选题/结构/流程 |
| 质量规则 | `RULES-30-quality.md` | 15 条硬条款 + 禁用词 |
| **数量限制** | `RULES-70-quota.md` | 防灌水（含长文豁免 §五） |
| **语言规则** | `RULES-80-language.md` | 10 语言细则 |

## 六、维护规则

1. **单一来源**：同一参考只保留一处；重复即合并或改为指针（本轮已归档 5 个 iCloud 冲突副本 → `_archive/icloud-dups-20260917/`）
2. **登记制**：新增 references 文件必须在本索引出现（PR/提交时检查）
3. **版本优先**：多版本参考（benchmark-seed v1-v3）默认用**最高版本**，旧版仅供追溯
4. **与 MFlow 的关系**：MFlow 的内容库（`run/library/`）是**产出**；本索引指向的是**写作依据**
