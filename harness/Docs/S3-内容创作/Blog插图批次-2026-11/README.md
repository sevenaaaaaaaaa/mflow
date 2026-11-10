# Blog 插图批次 · 2026-11

> **口径**：Lovart Global 全站 Blog（Sanity 实时拉取，2026-11-04）。
> **总量**：唯一文章 **2,035 篇** × 各类型规范插图 → **AI 插图 brief 8,081 张 + 截图任务 411 张 = 8,492 槽位**。
> **多语言零增量**：同一篇文章的全部语言版本共用同一套图（master 语言出图，多为 en；单语言文章用自身语言）。
> 风格 SSOT：`STYLE-SYSTEM.md` **v3**（六航道冻结 + 构图原型轮换 + 工艺词汇/光签名 + **正文内容画像锚定** + **分类视觉亲缘**——面向「全球首个 AI 设计 agent」的调性要求）。

## 1. 为什么是这个数

| 依据 | 数值 |
|---|---|
| Sanity 全量 blog 文档 | 8,712（11 语言） |
| 去重唯一文章（去 draft/unpublished） | 2,035 |
| 正文插图现状 | 8,712 篇中仅 6 篇有正文图 → **缺口 ≈ 100%** |
| 封面现状 | 8,045 篇 live 文档中 8,026 已有封面（99.8%）→ **封面不再生成**，仅 18 篇缺口顺手补 |

每篇张数按文章类型规范执行（`blog-writer/references/methodology-content-writer.md` §Per-Content-Type Image Requirements）：

| 分类 | 篇数 | AI 插图 | 截图 | 规范 |
|---|---:|---:|---:|---|
| Lovart 101 / Pillar | 794 | 6/篇 | 0 | Hero + 缩略×3 + 概念图 + CTA |
| Complete Guide | 56 | 6/篇 | 0 | 同 Pillar |
| How-To | 416 | 3/篇 | 0 | 成品 + 步骤对比 + CTA |
| Best Practice | 211 | 1/篇 | 1/篇 | 真实界面 + CTA |
| Reviews | 148 | 2/篇 | 1/篇 | 真实界面 + 双轨对比 + CTA |
| Better Design | 86 | 3/篇 | 0 | 原则形态 + 成品 + CTA |
| Insight & Trend | 48 | 3/篇 | 1/篇 | 人物 + 概念图 + 真实界面 + CTA |
| 类型未定 | 265 | 3/篇 | 0 | 通用：成品 + 概念图 + CTA |
| Branding / Stack | 11 | 3/篇 | 部分 | 同上 |
| **合计** | **2,035** | **8,081** | **411** | |

## 2. 波次与文件

| 波次 | 内容 | 文章 | AI brief | 投喂文件 | 截图任务 |
|---|---|---:|---:|---|---:|
| **W0** | 风格定调（6 航道 × 3 候选） | — | 18 | `batches/W0-style-sheet.jsonl` | — |
| **W1** | How-To | 416 | 1,248 | `W1-001…052` | — |
| **W2** | Reviews + Best Practice + Branding + Stack | 370 | 536 | `W2-001…023` | 363 |
| **W3** | Insight & Trend + Better Design + 类型未定 | 399 | 1,197 | `W3-001…050` | 48 |
| **W4** | Complete Guide | 56 | 336 | `W4-001…014` | — |
| **W5** | Pillar / 101（分 5 段跑） | 794 | 4,764 | `W5-001…199` | — |
| | **合计** | **2,035** | **8,081** | **338+1 个文件** | **411** |

## 3. 内容锚点（这是「按文章内容生成」的机制 · v3）

每条 brief 的 subject 不用模板空话，由四层内容锚点合成：

1. **主题短语**：从文章 slug 提炼（`ai-art-copyright-2026` → `AI art copyright 2026`），标题只用于 alt 文案；
2. **H2 论点锚点**：全部 H2 结构已抓取，概念图/对比槽位优先引用「过程语义」小节标题；
3. **正文内容画像（v3）**：每篇抓取正文前 35 块 + 全部 H2/H3（`inventory/content.json`），提取**交付物形态**（98% 来自正文实测，兜底仅 1.2%）、**目标受众**（84% 命中，Persona 用真实受众）、**实际步骤数**（Diagram 节点数 = 文章真实步骤）；
4. **实体形态映射**：正文 > slug 规则 > 兜底 三级来源；每条 brief 带 `signals` 字段可审计。

数据快照存于 `inventory/`（articles.json + h2.json + content.json），可复跑、可审计。

## 4. 文件索引

| 文件 | 内容 |
|---|---|
| `README.md` | 本文件 |
| **`ALL-PROMPTS.md`** | **全部 Prompt 单一入口（7.7MB）：8,081 条按投喂批分节 + 统一负面词 + 411 截图任务清单** |
| `STYLE-SYSTEM.md` | **风格 SSOT**：调性红线、航道 token、槽位映射、复杂度预算、负面词、W0 定调 |
| `BATCH-PLAN.md` | 执行顺序、每批操作纪律、进度追踪 |
| `batches/W0-style-sheet.jsonl` | 风格定调 18 张（最先跑） |
| `batches/W1…W5-*.jsonl` | 338 个投喂文件（每文件 24 条，独立可投喂） |
| `batches/screenshot-tasks.jsonl` | 411 条真实界面截图任务（非 AI，走实测截图管线） |
| `md/00-总览.md` + `md/{W}-{分类}.md` | 全部 brief 可读版（每篇文章的槽位构成 + 示例 prompt） |
| `gen_blog_illustration_briefs.py` | brief 生成器（SSOT 脚本，改规范后重跑即可） |
| `assemble_inventory.py` | Sanity 数据 → inventory 组装脚本 |
| `gen_md_views.py` | md 可读版生成器 |
| `manifest.json` | 生成结果台账 |

## 5. 通用规范（详见 STYLE-SYSTEM.md）

1. **三条红线**：过时风格（紫蓝渐变/玻璃拟态/等距 SaaS 插画/霓虹赛博）· 嘈杂布局（元素>3、满铺、堆叠阴影）· AI 画 UI（假界面一律禁止）。
2. **统一调性**：warm ivory + soft greige 底 / deep charcoal 墨 / one muted coral 点睛；L2 视频主题例外（teal-and-amber）。
3. **复杂度预算**：主视觉 ×1 + 支撑 ≤2；主体占 55–65%；四边留白 ≥8%。
4. **图内零文字**（含数字）；排版语义用空白几何 token 表达。
5. **规格**：16:9 · 1600×900 · PNG。
6. **命名**：`blog-{slug}-s{槽位}-{类型}-v1.png`。

## 6. 已知边界（明确列出）

| 项 | 说明 |
|---|---|
| 类型未定 265 篇 | Sanity 无 category 且 slug 无法可靠判断类型 → 按通用 3 张执行；后续如补分类，重跑生成器即可增量修正 |
| E-E-A-T 数据图表 | `eeat-system-plan.md` 第 4 层的「关键数据点→真实数据图表」走图表管线（代码渲染），**不在本批次**，避免 AI 编造数据图 |
| 截图任务 411 张 | 依赖产品实测截图管线（eeat 第 2 层），与 AI 批次并行推进 |
| 分类修正 | 个别文章 Sanity 分类与内容类型不完全一致（如 Reviews 归在 How-To），以 Sanity 为准；如需修正先改数据再重跑 |
