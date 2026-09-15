# Lovart Topics 页面框架 — 复合型内容聚合策略

> 版本: 1.0 | 日期: 2026-07-21 | 类型: 策略框架
> 适用范围: Topics 类 compositePage（category: "topic"）
> 产出路由: MindRe 1-2 Insight（知识资产，长期策略文档）

---

## 一、现状诊断

### 1.1 数据事实

Topic 页面当前处于"三个零"状态：

- **零流量**：GSC top 20 页面中无任何 /topic/ 路径；Bing 869 页面中 0 个 topic 页面。Topic Top 12 的 GA4 流量仅 2-3 users/30d（来源：2026-07-07 首页排序报告）
- **零差异**：86 个 Topic 页面 100% 使用 Pattern A（12-section hero-split 固定序列），内容结构完全同质化
- **零刷新**：86 个页面一次性批量创建后无任何内容迭代或数据更新

### 1.2 根本原因

当前 Topic 页面的定位被**过度窄化**为两种类型：

| 类型 | 数量 | 本质 | 问题 |
|------|------|------|------|
| 竞品名页面 | 73 | "X alternative" 落地页 | 拉踩感重，用户不搜竞品名+alternative 组合时无入口 |
| 用例页面 | 13 | "AI X generator" 落地页 | 与 Tools 页面完全重叠（tools 类 658 页已覆盖同类关键词） |

**Topics 被当成了 Tools 的"别名频道"，而不是独立的内容组织形式。**

---

## 二、Topics 重新定义

### 2.1 核心定位

> **Topic 页面 = 以"话题"为中心的内容聚合枢纽，而非以"功能/产品"为中心的交易页面。**

区别于其他 category：

| Category | 组织逻辑 | 典型问题 | 页面目标 |
|----------|----------|----------|----------|
| **Tools** | 按功能组织 | "这个工具能做什么？" | 转化（试用/注册） |
| **Features** | 按能力组织 | "Lovart 有什么独特性？" | 认知+转化 |
| **Solutions** | 按行业/角色组织 | "对我的业务有什么用？" | 转化（行业定制） |
| **Scenarios** | 按使用场景组织 | "在这种情境下怎么用？" | 教育+转化 |
| **Topics** | 按话题聚合 | "最近大家/我在关注什么？" | **流量入口+内容分发** |

Topics 的独特价值：**把分散的 Blog、Tools 页面、产品能力、外部趋势信号整合到一个高信息密度页面中**，成为用户在某个话题上的"一站式信息终点"。

### 2.2 与竞品策略的分界线

Topics 不是 Scenarios/Solutions 的变体。关键区分维度：

- **Scenarios**：稳定、可复现的使用场景（"电商促销季做 Banner"）
- **Solutions**：行业/角色解决方案（"给 Marketer 的 AI 设计工作流"）
- **Topics**：动态、有时间性的热门话题（"Ghibli 风格 AI 滤镜为什么火了"、"FLUX 2.0 vs 1.0 到底升级了什么"）

Topics 可以指向 Scenarios/Solutions 页面作为内部链接，但自身定位是**信息聚合入口**而非**转化终点**。

---

## 三、Topic 页面五大类型矩阵

### 3.1 类型全景

| # | 类型 | 触发信号来源 | 时效性 | 内容密度 | 建议模块数 | 示例 |
|---|------|-------------|--------|----------|-----------|------|
| T1 | **模型聚焦** | GSC 非品牌词、竞品词库、社交监听 | 中（模型更新周期 1-3 月） | 高 | 15-18 | "Veo 3.1 on Lovart: What Changed and How to Use It" |
| T2 | **趋势/热点** | 社交媒体监听、Reddit/ProductHunt 趋势、国内短视频平台 | 高（1-4 周窗口期） | 中高 | 12-15 | "AI-Generated Product Photography Is Replacing Studio Shoots" |
| T3 | **产品深度** | 产品 Roadmap、用户反馈、KB 素材 | 低（产品能力相对稳定） | 高 | 15-18 | "MCoT Engine Deep Dive: How Lovart's Multi-Chain-of-Thought Works" |
| T4 | **社群/争议** | Reddit、设计社区、X/Twitter 讨论 | 高（话题热度衰减快） | 中 | 10-12 | "Is AI Design Killing Creativity? What 50 Designers Actually Said" |
| T5 | **知识枢纽** | 关键词研究、存量内容缺口分析 | 低（常青内容） | 最高 | 18-22 | "AI Video Generation Models Compared: Sora vs Kling vs Veo 3 vs Seedance — Complete Guide 2026" |

### 3.2 各类型详细规范

#### T1 — 模型聚焦（Model Spotlight）

**触发信号**：
- GSC 中出现新模型名非品牌词（如 flora ai、artlist ai、hedra ai 等每月 mover 列表）
- 竞品开始布局某模型页面（从 competitor_keywords.json 交叉比对）
- 社交媒体上某模型讨论量激增

**内容结构**（15-18 模块）：
```
1.  hero-cinematic        — 模型名 + Lovart 集成声明
2.  stats                 — 模型性能数据（速度/质量/价格对比，如可用）
3.  bento-6               — 6 个该模型在 Lovart 上的典型产出
4.  capability-tabs       — 4 个使用模式（文生图/图生图/局部重绘/批量生成）
5.  canvas-wall           — 10 个实际生成案例
6.  comparison-table      — 该模型 vs 同类模型 vs 传统方式
7.  prompt-launcher       — 预填该模型最优 prompt 模板
8.  workflow-horizontal   — "选择模型 → 输入 prompt → 迭代优化"三步
9.  blog-grid             — 引用 3-4 篇相关 Blog（内链）
10. feature-detail        — 3 个模型专属特性
11. cluster-block-dense   — 6 个常见问题/限制 + Lovart 如何弥补
12. tool-grid             — 相关 Tools 页面入口（2×3）
13. faq                   — "这个模型能做什么/不能做什么"
14. cta-default           — "Try [Model] on Lovart"
```

**与现有竞品名页面的差异**：
- 现有：`draft-veo-3-video-generation-landing-agent-workflow` → 本质是"你能在 Lovart 上替代 Veo 3"
- 新型：`topic/veo-3-1-update-whats-new` → 本质是"Veo 3.1 这个模型本身——更新了什么、和谁比、在 Lovart 上怎么用到极致"

#### T2 — 趋势/热点（Trend Spotlight）

**触发信号**：
- ORM 社交监听：X/TikTok/Reddit/微博/抖音上出现新 meme/趋势
- ProductHunt 上同类产品爆发
- 设计社区（Dribbble/Behance/站酷）出现新风格/技法
- 国内短视频平台（抖音/快手）话题标签发酵

**内容结构**（12-15 模块）：
```
1.  hero-journey          — 趋势起源 + 发展时间线
2.  bento-4               — 4 个该趋势的典型应用场景
3.  media-marquee         — 该趋势的视觉案例轮播
4.  capability-tabs       — 4 种"如何在 Lovart 上实现该趋势"的方法
5.  prompt-launcher       — 预填趋势风格的 prompt
6.  canvas-wall           — Lovart 生成的趋势风格作品
7.  comparison-before-after — "传统方式 vs Lovart 一键实现"
8.  blog-grid             — 引用相关 Blog 分析文章
9.  cluster-block-dense   — 6 个"你该知道的趋势细节"
10. testimonial           — 引用真实用户/设计师评价
11. faq                   — "这个趋势会持续多久/适合什么行业"
12. cta-default           — "Start Creating in [Trend Style]"
```

**典型候选**（基于现有数据管道可监控的）：
- "Ghibli-style AI filter trend" — 社交媒体爆款
- "AI product photography replacing studio shoots" — 电商刚需
- "无限的画布 Infinite Canvas 工作流" — GSC 出现中文搜索 `无限画布`（136 clicks）
- "Brand consistency across AI generations" — 品牌设计痛点

#### T3 — 产品深度（Product Deep-Dive）

**触发信号**：
- Lovart 产品发版/新功能上线
- Knowledge Base 中有深度素材但无公开页面对应
- 用户高频询问的产品概念（从客服/社区提取）

**内容结构**（15-18 模块）：
```
1.  hero-cinematic        — 产品概念名称 + 一句话定义
2.  bento-6               — 6 个核心能力卡片
3.  workflow-vertical     — "输入→处理→输出"纵向流程图
4.  capability-tabs       — 4 个实际使用模式
5.  canvas-wall           — 10 个产出案例
6.  comparison-table      — "有该能力 vs 没有该能力"对比
7.  feature-detail        — 4 个深度技术特性
8.  stats                 — 性能/效率提升数据（如有）
9.  prompt-launcher       — 演示用 prompt
10. proof-block           — 3 个信任信号
11. cluster-block-dense   — 6 个使用技巧
12. blog-grid             — 引用深度测评文章
13. tool-grid             — 相关功能入口
14. faq                   — 技术细节 Q&A
15. cta-default           — "Try It Yourself"
```

**典型候选**：
- "MCoT Engine：多链思考如何让 AI 设计不再'抽卡'"
- "ChatCanvas：为什么画布式 AI 交互比对话框强"
- "Brand Kit：品牌一致性不是 prompt engineering 问题"
- "Agent Skills：Lovart 的 Agent 到底能调用哪些工具"

#### T4 — 社群/争议（Community Pulse）

**触发信号**：
- Reddit（r/ai_design, r/graphic_design, r/StableDiffusion）出现争议帖
- X/Twitter 上设计师群体的热点讨论
- 设计社区出现集体抵制/拥抱 AI 的讨论

**内容结构**（10-12 模块）：
```
1.  hero-journey          — 争议时间线 + 各方观点
2.  bento-4               — 4 个关键争论点
3.  stats                 — 引用数据（投票结果/调查报告/社区统计）
4.  testimonial           — 引用真实设计师的公开观点
5.  comparison-table      — "不同立场的设计师如何看待同一个问题"
6.  cluster-block-dense   — 6 个"无论你站哪边都需要知道的事实"
7.  blog-grid             — 引用 Lovart Blog 深度分析
8.  feature-detail        — Lovart 如何回应这个争议（产品层面）
9.  faq                   — 社区常见疑问
10. cta-default           — "Join the Conversation" 或 "Try Lovart's approach"
```

**典型候选**：
- "AI 设计到底偷了多少设计师的活儿——50 个设计师的真实回答"
- "Prompt engineering 是不是新的'代码'——设计师需要学吗"
- "AI 生成内容的版权归属——法律现状和实际风险"

#### T5 — 知识枢纽（Knowledge Hub）

**触发信号**：
- 关键词研究中发现用户搜索"X vs Y vs Z"类对比查询
- 某品类存在多个分散的 Blog/Tools 页面但缺乏汇总入口
- GSC 显示用户从信息类查询进入但跳出率高（需要更好的内容聚合）

**内容结构**（18-22 模块）：
```
1.  hero-cinematic        — 话题全景 + "Everything you need to know"
2.  bento-6               — 6 个子话题入口
3.  capability-tabs       — 按维度切换（模型/工具/工作流/案例）
4.  comparison-table      — 全品类横向对比（核心模块）
5.  tool-grid             — 所有相关 Tools 页面
6.  blog-grid             — 所有相关 Blog（按子话题分组）
7.  canvas-wall           — 各子话题的代表性产出
8.  workflow-horizontal   — "从选择工具到产出成品的通用路径"
9.  cluster-block-dense   — 12 个关键知识点卡片
10. feature-detail        — 4 个深度对比
11. stats                 — 市场份额/使用数据
12. prompt-launcher       — 各子话题的 prompt 模板
13. media-marquee         — 案例轮播
14. pricing-block         — 价格对比（如适用）
15. proof-block           — 数据来源声明
16. review-grid-3col      — 用户/媒体评测引用
17. faq                   — 终极 FAQ
18. cta-default           — 分流 CTA（"想深入哪个方向？"）
```

**典型候选**：
- "AI Video Generation Models: Complete Comparison Guide 2026" — 覆盖 Sora/Kling/Veo 3/Seedance/Runway
- "AI Logo Design: From Prompt to Brand System — The Complete Stack"
- "AI for E-commerce Visuals: Product Photos, Banners, Ads, Social Media — All-in-One Guide"
- "无限画布 AI 设计工作流完全指南" — 承接 GSC 中文搜索需求

---

## 四、数据驱动的 Topic 发现管道

### 4.1 六大数据源及接入方式

| # | 数据源 | 当前状态 | 可提取的 Topic 信号 | 刷新频率 |
|---|--------|----------|-------------------|----------|
| 1 | **GSC 非品牌词** | ✅ 已接入（gsc-full.json） | 新出现的高曝光非品牌词、月度 mover（flora ai, artlist ai, hedra ai, civitai 等） | 月度 |
| 2 | **Bing 非品牌词** | ✅ 已接入（bing-full.json） | Bing 独家非品牌流量（Bing 市场份额 35%+） | 月度 |
| 3 | **竞品关键词库** | ✅ 已整理（competitor_keywords.json, competitor_core_keywords.md） | 模型名/品类词优先级矩阵（P0/P1/P2） | 季度 |
| 4 | **ORM 社交监听** | ✅ 管道已建（22 个 daily/weekly JSON），数据采集 delegated | X/TikTok/Reddit/YouTube 趋势、设计社区讨论、竞品动态 | 周度 |
| 5 | **产品 KB** | ✅ 已整理（KB-Index by-topic.md, 362 units） | 产品深度素材（MCoT, ChatCanvas, Brand Kit, Agent Skills） | 随产品更新 |
| 6 | **社交媒体知识库** | ✅ 已整理（Lovart Social Media Knowledge Base 2026-07.md） | 社媒传播素材、用户反馈、品牌提及 | 月度 |

### 4.2 从信号到页面的决策流程

```
信号出现 → 归类到 T1-T5 类型 → 评估三个维度 → 创建/不创建

评估维度：
1. 搜索需求验证：GSC/Bing 是否有对应搜索量？（≥100 impressions/月 → 绿灯）
2. 内容差异化：现有 Blog/Tools 页面能否覆盖该话题？（已有覆盖 → 降级为内链优化；无覆盖 → 绿灯）
3. 时效窗口：话题热度预计持续多久？（<2 周 → 不建页面，改用 Blog 快文；≥1 月 → 绿灯）

绿灯 → 根据类型选模块序列 → 创建 compositePage → Blog 文章配合发布 → 内链打通
```

### 4.3 动态刷新机制

T1-T5 中时效性高的类型（T2 趋势、T4 争议）需要定期刷新：

- **T2 趋势页**：创建后 2 周复查社交信号，热度降温则降级为"archive"状态（保留页面但降低内链权重）
- **T4 争议页**：创建后每月更新一次社群数据，保持"当前状态"而非"历史记录"感
- **T1/T3/T5**：季度刷新（模型更新/产品迭代/新数据）

---

## 五、模块选型策略

### 5.1 按 Topic 类型的模块推荐

| 类型 | Hero | 核心差异模块 | Blog 引用 | Tools 引用 | 特殊模块 |
|------|------|-------------|-----------|-----------|----------|
| T1 模型 | hero-cinematic | stats, comparison-table, prompt-launcher | blog-grid | tool-grid | — |
| T2 趋势 | hero-journey | media-marquee, comparison-before-after | blog-grid | — | testimonial |
| T3 产品 | hero-cinematic | workflow-vertical, stats, proof-block | blog-grid | tool-grid | — |
| T4 争议 | hero-journey | stats, testimonial | blog-grid | — | — |
| T5 枢纽 | hero-cinematic | comparison-table, pricing-block, review-grid | blog-grid | tool-grid | media-marquee |

### 5.2 统一约束

- **正文比**：T5 枢纽 > T1 模型 > T3 产品 > T2 趋势 > T4 争议
- **内链密度**：所有类型必须包含 `blog-grid`（引用 ≥3 篇相关 Blog）+ `cluster-block-dense`（至少 6 个知识点卡片）
- **CTA 收敛**：T1/T3 指向 `/canvas`；T2/T4 指向 Blog 深度文或 `/canvas`；T5 指向子话题分流
- **禁止拉踩**：comparison-table 的对比维度必须是"事实数据"（速度/价格/分辨率/支持格式），不做主观优劣判断
- **多语言**：T1-T5 全类型均需覆盖 10 语言，优先 EN/ZH/JA/KO

---

## 六、立即可执行的 Topic 候选清单

基于现有数据管道中已可提取的信号，以下 Topic 页面有明确的数据支撑：

### 6.1 GSC 信号驱动（T1 模型聚焦）

| # | Topic Slug | 触发信号 | 类型 | 优先级 |
|---|-----------|----------|------|--------|
| 1 | `flora-ai-design-tool-comparison` | GSC 月度 mover #1（143 clicks, 53K impr） | T1 模型 | 🔴 P0 |
| 2 | `artlist-ai-vs-lovart-creative-assets` | GSC 月度 mover #2（91 clicks, 35K impr） | T1 模型 | 🔴 P0 |
| 3 | `civitai-models-on-lovart` | GSC top100 非品牌词 #2（298 clicks, 51K impr） | T1 模型 | 🟡 P1 |
| 4 | `freepik-ai-vs-lovart` | GSC top100 非品牌词 #1（570 clicks, 119K impr） | T1 模型 | 🔴 P0 |
| 5 | `hedra-ai-talking-avatar-alternative` | GSC 月度 mover（84 clicks, 22K impr） | T1 模型 | 🟡 P1 |
| 6 | `openart-ai-comparison` | GSC 月度 mover（93 clicks, 26K impr） | T1 模型 | 🟡 P1 |

### 6.2 产品能力驱动（T3 产品深度）

| # | Topic Slug | 素材来源 | 类型 | 优先级 |
|---|-----------|----------|------|--------|
| 7 | `mcot-engine-deep-dive` | KB agent/canvas topics（26+27 units） | T3 产品 | 🔴 P0 |
| 8 | `chatcanvas-infinite-canvas-workflow` | KB canvas topics（42 units）+ GSC `无限画布`（136 clicks） | T3 产品 | 🔴 P0 |
| 9 | `brand-kit-consistency-system` | KB brand topics（27 units） | T3 产品 | 🟡 P1 |
| 10 | `lovart-agent-skills-capabilities` | KB agent topics（26 units） | T3 产品 | 🟡 P1 |
| 11 | `lovart-model-selection-guide` | KB model docs + GSC `veo 3.1 free`（183 clicks） | T5 枢纽 | 🔴 P0 |

### 6.3 竞品关键词驱动（T5 知识枢纽）

| # | Topic Slug | 触发信号 | 类型 | 优先级 |
|---|-----------|----------|------|--------|
| 12 | `ai-video-generation-models-complete-guide-2026` | 竞品 P0 关键词矩阵（AI Video Generator + Text to Video） | T5 枢纽 | 🔴 P0 |
| 13 | `ai-logo-design-complete-stack` | 竞品 P0 关键词（Logo Design + AI Logo Generator） | T5 枢纽 | 🟡 P1 |
| 14 | `ai-ecommerce-visuals-all-in-one` | 竞品关键词（Product Video + AI Banner + AI Commercial + UGC） | T5 枢纽 | 🟡 P1 |

### 6.4 社交趋势驱动（T2 趋势/T4 争议）

| # | Topic Slug | 触发信号 | 类型 | 优先级 |
|---|-----------|----------|------|--------|
| 15 | `ai-design-copyright-ownership-2026` | 设计社区持续讨论（Reddit r/ai_design 高频话题） | T4 争议 | 🟡 P1 |
| 16 | `ai-product-photography-replacing-studios` | 电商营销媒体趋势 + GSC 非品牌词隐含需求 | T2 趋势 | 🟢 P2 |
| 17 | `prompt-engineering-for-designers` | Reddit/设计社区高频话题 | T4 争议 | 🟢 P2 |

---

## 七、执行路线图

### Phase 1 — 立即执行（本周，P0 优先）

1. **创建 3 个 T5 知识枢纽页**（#11 #12 #5）—— 最高内容密度，可内部链接到现有大量 Blog/Tools 页面
2. **创建 3 个 T1 模型聚焦页**（#1 #2 #4）—— 承接 GSC 已有非品牌搜索流量
3. **创建 2 个 T3 产品深度页**（#7 #8）—— 发挥 KB 素材优势

### Phase 2 — 两周内（P1）

4. 创建 5 个 P1 页面（#3 #5 #6 #9 #10 #13 #14 #15）
5. 为所有新建页面创建 10 语言多语言版本
6. 打通 Blog→Topic 内链双向引用

### Phase 3 — 持续运营（月度）

7. 月度 Topics 信号扫描（GSC mover + ORM 社交趋势 + 竞品动态）
8. 按 4.3 刷新机制更新时效性强的 T2/T4 页面
9. T1 模型页随模型版本更新同步刷新

---

## 八、成功指标

| 指标 | 当前基线 | 3 月目标 | 测量方式 |
|------|---------|----------|----------|
| Topic 页面总流量（GSC clicks） | ~0 | ≥500/月（全部 Topic 页面合计） | GSC page×query 过滤 /topic/ |
| 非品牌词覆盖率 | 7/100（7%） | ≥20/100（20%） | GSC top100 中非品牌词占比 |
| Topic 页面平均停留时间（GA4） | 无数据 | ≥2:30 | GA4 avg engagement time per session |
| Topic 页面内链点击率 | 无数据 | Blog→Topic 点击 ≥3%（从 Blog 流量分流） | GA4 event tracking |
| 多语言覆盖率 | 0 个非 EN 语言的非竞品名 Topic | 所有新建 Topic 完整 10 语言 | Sanity GROQ count |

---

## 九、关键决策记录

| # | 决策 | 理由 | 日期 |
|---|------|------|------|
| 1 | Topics 不走 Scenarios/Solutions 的故事线系统 | Topics 是信息聚合入口而非场景化转化页，故事线的"audience+intent+copy"三维绑定不适合动态话题 | 2026-07-21 |
| 2 | T1-T5 分级而非统一模板 | 不同话题类型的信息密度、时效性、内容深度差异太大，统一 12-section Pattern A 造成"竞品替代页"同质化 | 2026-07-21 |
| 3 | blog-grid + tool-grid 作为所有 Topic 类型的固定模块 | Topic 页面的核心价值是内容分发——把流量导向深度 Blog 和转化工具页 | 2026-07-21 |
| 4 | 不新建 Topic 页面来覆盖已有竞品名页面 | 73 个现有竞品名页面保留，但不再按此模式新增。新页面统一走 T1-T5 类型 | 2026-07-21 |
| 5 | T2/T4 时效性页面设降级机制 | 避免热度过期的趋势页长期占据 Topic 目录，保持频道"当前感" | 2026-07-21 |
