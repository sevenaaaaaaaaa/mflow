# MFlow 内容体系说明（同事版）

> 写给接手/协作的同事：这套系统是什么、按什么逻辑分类、质量怎么保证、个性化怎么做、当前还差什么。
> 更新：2026-10-07。本文是人类长期资产，架构与规则细节以各 SSOT 文件为准（文末索引）。

---

## 一、这是一套什么系统

MFlow 是 GEO（生成式引擎优化）自动内容生产系统：**信号监测 → 策略选题 → 内容生产 → 质检 → 止步待授权 → 发布 → 体验回流**。当前服务两个品牌站点：Lovart Global（www.lovart.ai，Sanity + WordPress 子站）与 Moodio Global（moodio.art，CMS 接入中）。

最重要的一条工作约定：**自动化止步 `status: ready`，发布永远由人工授权**。机器负责把内容做到「可发布」，人负责按下发布键。

---

## 二、核心架构：四层 + 一个状态机 + 一个后台循环

**① 工程管理层（Harness）** —— 管约束，全程拦截，不跑偏。
规则分层加载（RULES-00 全局铁律 + 各工作线 RULES-10~60）；会话启动六门禁（session-init）；pipeline-state 状态机（12 个 stage / 4 个 phase，原子写入，非法状态转换直接拒绝）；router 路由器（23 条决策，把任务路由到 6 个 Profile，省 87-92% token 且零漏失）；四钩子机器检查（pre-write / post-write / pre-import / post-generation）；内容契约层（34 型 section 注册表 + 故事线顺序门禁，87 项测试）。

**② 品牌层** —— 一个品牌一份的差异资产。
brand profile（10 组字段）、品牌知识库 KB（Lovart 750+ 份 / Moodio 9 份）、两份策略真值（词群作战地图 + 内容选题计划）、子站继承机制（subsites：新品牌/子站继承五项能力后按需覆盖）。

**③ 执行层** —— 三个创作入口。
blog-writer（博客唯一入口）、landing-writer（落地页唯一入口）、hub-writer（聚合页唯一入口）。每个入口内置「策略对齐钩子」：选题必须过**三重 trace**——词群 ∩ 人群格 ∩ 集群位置，缺一不写。

**④ 体验层** —— 发布后的质量闭环。
page-experience 按频率跑三张清单（每周机器全自动 / 每月 GSC 后 / 每季人工+机器），发现问题走工单分流：渲染 bug 回创作修复、转化问题进 CRO、流量信号回流选题信号表。

**Loop（后台 console）** —— 执行层的机器化。
107 个 API：loop 引擎（并发 2）批量生产、schedule_executor 自动排程（每天 2 次）、automations 剧本编排 + 9 个 preset（内链审计/多语言覆盖/QA 扫描/低 CTR 刷新等）、GEO 探针（每日 AI 引用监测）、selfcheck/self-evolve 自检迭代。

**数据流一句话**：信号（舆情 Sentinel + GSC/Trident）→ 策略（词群 + 选题计划）→ 创作（multi-turn 状态机）→ 质检（钩子 + 三层门禁 + cascade 互评）→ **ready 止步** → 人工授权 → 发布（WP dry-run 闸 / Sanity `--missing` 增量）→ 体验层信号回流。

---

## 三、Blog 分类体系（精细化策略的四个维度）

博客精细化不是「换个标题写法」，而是四个正交维度共同决定一篇文章怎么写。全部收敛在唯一入口 `blog-writer` 里。

**维度 1：内容类型（12 型矩阵）**
Narrative/Insight、Tutorial (How-To)、Awesome Prompt Tutorial、Comparison/Alternative、Case Study、Best Practice、Pillar Page/101、Better Design、Segment Deep-Dive、Podcast Show Notes、Digest、Glossary。每型有固定的漏斗位、语言层级与写作骨架。

**维度 2：漏斗阶段（4 段配比）**
TOFU 50%（抢词占位）/ MOFU 30%（工作流）/ BOFU 20%（对比与转化）/ Post-Purchase（留存）。冷启动偏 TOFU，增长期调向 MOFU/BOFU——配比改动写回选题计划并版本递增。

**维度 3：叙事框架（11 框架库 + 强制配对）**
Myth-Buster / Journey / Economist / Visionary / Field Guide / Co-Host / Cookbook / Duel / Proof / Encyclopedia / Curator。每种内容类型有主框架 + 备选框架（如 Comparison → The Duel），禁止全程默认一个框架。动笔前必须输出一行路由声明：`Content type | Category | Funnel | Framework | Because`。

**维度 4：词群归属（词群作战地图）**
每篇必须落在某个词群（Lovart 10 词群/3 KR；Moodio 12 词群/4 KR），写进 frontmatter 的 `content_cluster`；命中黑名单词的选题不写。

**在此之上还有两个横切分级：**

- **Lane 三档**（按 GSC 信号定写作投入）：Deep（曝光>1k、排名 4-10，3+ 轮多轮写作）/ Medium（500-1k、排名 11-20）/ Light（低信号，单轮）。Lane 只定投入力度，**不降 7,500 词地板**。
- **语言分层**：EN 为源，按信号决定 Tier 1 / +2 / +3 市场；各语言是**按信号独立重写**，不是机器翻译。

**五条选题轴**（季度复盘优先级）：季节性 / 行业深度 / 职业工作流 / 企业级 / 伦理与法律。每轴对应历史策略文档（00-09 十份 + 竞品覆盖 + 程序化 SEO），条目矩阵落到具体选题 ID。

**给同事的决策路径一句话**：先查词群（打哪个词）→ 查选题计划（给谁写、在哪条线）→ 定类型和框架（12 型 × 11 框架配对）→ 按漏斗配比排产 → 信号决定投入档位 → 止步 ready 等授权。

**文档索引**（同事自查用）：
- `harness/Skills/02-creation/blog-writer/SKILL.md` — 六步链路与铁律
- `.../references/methodology-content-writer.md` — 12 类型矩阵 + 11 框架库 + Anti-AI Rules v4
- `.../references/strategy-content.md` — 内容选题计划 SSOT（漏斗配比/五轴/条目矩阵）
- `.../references/keyword-clusters.json` — 词群作战地图
- `.../references/signals-and-phases.md` — 信号→选题映射 + Lane 分档
- `.../references/types/{type}/GUIDE.md` — 8 个类型骨架（101/best-practice/better-design/complete-guide/insight-trend/review/stack-by-stack/thought-leadership）
- `genflow/Content Strategy/00-09-*.md` — 五轴历史策略文档
- 相邻入口：`landing-writer`（落地页）、`hub-writer`（聚合页）、`moodio-film-content`（Moodio 品牌路由）

---

## 四、质量体系：为什么我们的批量内容不「AI 味」

**字数铁律（已拍板，全类型统一）**：进 `status: ready` 前英文正文 **≥7,500 词**，**全部分类一体适用**——包括 Glossary、Digest 这类传统上的短类型。规则是「根据内容特性把短类型写出不灌水的 7,500+ 词」（如 Glossary 条目群深度展开、Digest 深度解读），而不是放宽地板。禁止脚本扩字灌水（Banned Template-Phrase Registry 25 个触发词机器拦截）。

**四道机器门禁**（长文必须全过）：
- pre-write（写前：路径/frontmatter/占位符）
- post-write（写后：H2 密度/词数 ≥7,500/模板残留/AI 自介）
- geo-check / quota-check / lang-check（GEO 要素/数量预算/语言纯度）
- pre-import（导入前：状态机在 S4-ready + BLOCK 全 0 + 日期双写 + 多语言覆盖）

**三层人工/机器混合门禁**：L1 preflight（BLOCK>0 即停）→ L2 发布后抽查 → L3 发布前五维审计（合规/文化/可读性/SEO/品牌）。

**写作反 AI 机制（Anti-AI Writing Rules v4）**：开头禁统计句、禁 "Part 1/2/3" 标签、禁 "There are three reasons…" 旗标、禁三明治段落节奏、禁 PAS 模板块；数据必有上下文、未验证标 `[待考证]`；每篇必有真实用户视角 + 踩坑段落 + 可引用金句。

**长文生产方式**：禁止单次灌出全文，走 multi-turn 状态机——OUTLINE（列立场、反方观点、场景数据，等确认）→ 分 Part 写作（单次输出硬顶 3,000 词）→ INTEGRATE_QA（全文 banned phrase + 段落 unique 度 + frontmatter 15 字段）。重要文章再加 cascade 互评：writer 写 → critic 按 7 项评 → 不过带理由回炉，最多 3 轮。

---

## 五、个性化体系

- **Persona Matrix**：人群 × 漏斗阶段定位每篇文章的目标读者。
- **Angle Engine**：微观人群切片 → 摩擦点 → 反共识角度 → 5 标题法。
- **品牌隔离**：KB 按品牌隔离 + kb_intent 项目级加权（防止多品牌上下文互相污染）；品牌术语按项目路由（Lovart 术语绝不进 Moodio 稿）。
- **Moodio KB 加强方向（已拍板）**：参考 Lovart KB 的厚度与结构补强，但内容面向**视频、影视、传媒行业从业者**（Moodio 的目标人群），不是照搬 Lovart 面向全体创意工作者的口径——补齐能力词表、人群画像、行业工作流、竞品实测等维度。

---

## 六、当前不足与改进路线（2026-10-07 已拍板）

**P0 · 长任务稳定性（必须解决）**
- playbook runaway（失控重试）前科 → 需要硬性预算上限与熔断
- subagent 失败率高 → 长文批量仍依赖主 agent 兜底，需修复子代理链路
- Sanity 对 200+ block body 的 patch hang bug（b20）→ 未修，大文档 patch 走分段
- 每周/每月定时管线从未实跑过 → 需要一次人工触发验证

**P0 · 批量生产质量薄弱点（必须解决）**
- 质检全是「负面清单」（禁什么），缺「好内容」的正面量化标准 → 建立金句密度/观点原创度等正向指标
- 极限铺量模式（50+ 篇）官方容忍「仅 top5 全量质量」→ 逐步取消双标
- i18n P2 队列积压约 1,500 篇变体 → 按信号分层排产
- cascade 互评成本高（3 轮 token 翻倍）→ 批量场景容易跳过，需纳入机器门禁
- 发布后只有 28 天后置 GSC 信号 → 补 72 小时早期信号（收录/首曝/初始 CTR）

**P1 · 个性化深化**
- persona 目前是写作口径，不是读者数据驱动 → 接 GA4 分人群行为回流
- 缺「哪个人群的文章转化好」的效果闭环 → persona × 转化归因
- loop 批量场景同一词群角度趋同 → 同词群强制 Angle Engine 去重

**P1 · 平台与基建**
- 服务器单点无异地备份 → 建立数据异地备份
- Moodio 四个数据源未接（CMS 项目 ID / GSC / 素材包 / 线上扫描器）→ CMS 接入后后台全自动生产即通
- replication-core 未抽独立仓；WebFlow 适配器等三个场景答案

---

## 七、SSOT 索引

- 架构总控：`harness/00-INDEX.md`（v6 四层模型）
- 全局铁律：`harness/02-rules/RULES-00-iron.md`；创作类 `RULES-20-creation.md`；质量类 `RULES-30-quality.md`
- 状态机：`harness/Skills/06-orchestrate/pipeline-state/`；路由：`.../router/`
- 能力承载矩阵（品牌接入抽象）：`harness/Skills/infra/CAPABILITY-MATRIX.md`
- 博客入口：`harness/Skills/02-creation/blog-writer/`
- 设计复刻产品化：`docs/PRODUCTIZATION-REPLICATION.md`
- 项目记忆：`harness/11-knowledge/MEMORY-PROJECT.md`
