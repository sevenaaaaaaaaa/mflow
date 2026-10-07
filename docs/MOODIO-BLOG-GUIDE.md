# Moodio Global 博客创作总指南

> 面向：老板 / 市场负责人 / 内容运营一线。目标：看完知道**博客怎么批量创作、每个分类怎么写、系统做到哪一步、人工要接管哪些事**。
> 更新：2026-10-07。纯段落表述（项目规范禁表格）。规则细节以 harness SSOT 为准（文末索引）。

---

## 一、三分钟版（先结论）

Moodio 生产当前的真实状态：**系统已就绪，等待接入**。内容生产流水线（选题 → 生成 → 质检 → 止步待审）已在后台跑通并实测出 9 篇草稿；品牌资产（知识库 9 份、12 个词群地图、4 个 KR、行业红线模板）已填满。当前卡住全自动闭环的只有一件事：**CMS 项目未接入**（发布落库没有目标），以及 GSC 未接入（站点未上线，流量信号为零）。

分工一句话：**机器负责把文章从 0 写到「可发布的 ready」，产出永远停在人工审这一步；老板/市场负责人负责拍板发布 + 提供只有人能提供的东西（案例授权、真实数据、品牌判断）**。

当前预算纪律：一篇要进入 ready 的博客正文 **≥7,500 英文词**（全分类一体适用，包括词汇表和摘要类——按内容特性把短类型写厚，不灌水）。这是铁律，机器门禁会硬拦。

---

## 二、博客分类矩阵（四个维度，正交使用）

我们不用「一类文章一个写法」的粗分类，而是四个维度交叉定位每一篇文章。动笔之前，机器会在工作日志里先先宣布一行定位声明：

> Content type: [12 类之一] | Funnel: [TOFU/MOFU/BOFU] | Framework: [11 框架之一] | Cluster: [12 词群之一]

**维度 1 · 内容类型（12 类）与 Moodio 落位**

- **101 / Pillar Page**（百科全书型长文）——TOFU 锚点，全站约 3,000-5,000 词的页面级视角，Moodio 首月面向「AI 时代电影摄制组是什么」这类定义级文章。
- **How-To / Tutorial**——MOFU 主力，"从小说剧本到分镜"这类工作流文。
- **Comparison / vs**——BOFU 转化主力（Moodio vs Runway / Sora / Kling / LTX Studio），必须遵守 05-competitors 的实测数据规则，未验证的数字一律禁写。
- **Case Study**——BOFU 证据文。当前可引用案例仅《了不起啊！朋友》（上线状态复核后）。
- **Best Practice**——适合"资产库维护"这类留存型交付。
- **Insight & Trend**——行业趋势评论（短视频工业化、AI previz 普及）。
- **Complete Guide**——GEO 品牌词锚（分镜全流程）。
- **Better Design / Segment / Podcast / Digest / Glossary**——按需启动；Glossary 是 GEO 摘录型 talking point（DEF 系列）。

**维度 2 · 漏斗配比（内测期冻结值，改动需走策略会）**

TOFU 50%（抢占空档词：分镜/摄制组/短片）、MOFU 30%（工作流文）、BOFU 20%（对比与转化）。所有 CTA 只有一个出口：**申请内测码（app.moodio.art）**，禁写免费注册或购买。

**维度 3 · 12 个词群（我们打哪些词，哪些词不碰）**

P0 空档（实测无对手，首批主力）：分镜列表（shot list）、分镜生成（storyboard generator）、短剧制作（short drama production）。
P0 竞争：角色一致性（character consistency in AI video）——商业意图最强。
P1：广告（ad storyboard / TVC）、对比（moodio vs…）、初学者（first AI short film）、预演可视化（previz）、定义词群（AI-native film set / AI filmmaking terms）、GEO 记录。
P2：3D 世界模型、参考检索（按镜头运动搜参考）、交付互操作（导出达芬奇/勿免 Final Draft / FCP）。
**黑名单（三条纪律，机器会拦）**：不碰"AI video generator 大词"（被 699 万月自然访问量的 Higgsfield 垄断，调研裁定不碰词）；不做竞品模型名截流（pika/即梦图生视频）；不做"免费无水印"流量农场。

**维度 4 · 语言分层**

EN 为源语言，其他市场按信号驱动独立重写（不是翻译）。内测期：EN 主发，ZH 中文作为第二市场预留（策略待 GSC 上线后定）。

**「选题三重 trace」强制铁律**：一篇文章同时落在①某个词群、②某个漏斗位置、③某个集群位置（pillar / spoke / hub）。缺任一不写。这条由机器门禁执行：写之前没有先看词群地图和选题计划的，会被路由器拒绝。

---

## 三、每个分类怎么写（机器执行标准）

**叙事框架 = 11 个，按类型强制配对**。配对表全文在 methodology-content-writer.md，常用五组：

- How-To → "The Journey"（从读者当前的手忙脚乱起步）
- Comparison → "The Duel"（从决策瘫痪起步，公平裁判，不做粉丝）
- 101 / Pillar → "The Encyclopedia"（用定义性问题开场："AI 视频生成到底是什么"）
- Case Study → "The Proof"（以可审计的结果开场）
- Insight & Trend → "The Economist"（真实事件/具体数据/注明来源开局）

**长文生产状态机（防开产出重置）**：禁止一次输出 7,500 词全文。必须过 4 步：outline（先立柱：一句话主张 + 3 个反方观点 + ≥5 个场景数据点，等确认）→ 分段创作（单次输出硬顶 3,000 词）→ 整合校对。重要文章加“互相评审”（writer 写 → critic 按 7 项评分 → 不及格带具体意见回炉，最多 3 轮）。

**每篇必备（长文铁律）**：第一人称使用经历≥1、\"踩坑/对账\"段≥1、可引用金句≥1、真实工具搭配场景≥1、每千字 1-3 个数据点（同一数据不空表）、外部权威来源 2-5 条完整 URL、H2 每 500 词 1 个、FAQ 3-5 条。**六大必含块**：衍生场景 / FAQ / E-E-A-T 表 / 内部链接表 / 图片附件表 / 集群 footer 行。

**Moodio 八条品牌红线（模板内置，违反即整段重写）**：不声称成片效果优于平台、不比库量、不把协同简化为多人同画布、不绑定“只服务专业团队”、强调各阶段专业格式导出（FDX / XML / FCP / 达芬奇）、不写任何定价/版本号/客户案例名（官方未公布）、禁"一键成片/做 AI 就能赚/颠覆/革命性"、禁止借用 Lovart 设计能力词（两个品牌独立）。

**反 AI 洋重规则（Anti-AI Writing v4）**：开头禁统计句、禁 Part 1/2/3 标签、禁 "There are three reasons" 旗标、禁三明治段落节奏、禁 PAS 模板块。此规则在 pre-write 步骤机器打分。

---

## 四、Skills 与工具orangeland（谁负责什么）

**创作技能**：

- `blog-writer`——博客创作唯一入口（所有语言唯一入口是 skill 本身，无例外）。词群地图 + 选题计划 + 12 类型矩阵 + 8 个类型骨架全在它的 references 里。
- `moodio-film-content`——Moodio 品牌父入口：路由 + MRs 品牌事实页面。它不写文章，负责“该不该写、写哪篇、用什么 GB 事实”，然后转发到 blog-writer。
- `hub-writer`——当某词群 spoke ≥5 篇时自动触发聚合页（防 SEO "doorway" 得到 foo拦截）。
- `landing-writer`——分类推广页；**当前 Moodio 前端结构未定型，此 skill 的完整机器不可迁（Sanity 依赖），页面按"Hero → 3 Benefit → 场景 2 → FAQ 3 → CTA"简经总则手工模板执行**。

**后台能力**（MFlow 后台非智能 agent，是带熔断的确定性流水线）：

- 选题队列 + 之后按语气决定排产的**自动排程**（当前已暂停，遗留说明：为避免生成无人审的草稿烧预测账号，题库和 CMS 接入后再开）。
- **批量改稿/刷新预演**：GEO 缺口改稿、衰减页刷新、低 CTR 刷新。**当前全部免费预演（不调 LLM），确认后才生成**。
- **9 个预设**：每周内链审计 / QA 扫描 / alt 补齐等——大多是“数据源已接才有”的状态，极少数已启用。
- 熔断与预算：全局熔断（生产环境可以手工一键全停）、全局每日运行上限 200 次、单 loop token 预算 90k。**无人工授权不会有任何发布**。

**不适用/不迁移清单**：WordPress 子站线、GEO GEO 探针依赖 Perplexity key（等待接入）、7500 词长文线对 Moodio **适用**（不止 Lovart）。

---

## 五、端到端流程（一篇文章的完整旅程）

1. **信号 → 选题候选**：词群空档 + 应用商店评价/双轻松内容（当前三源：词群地图词条映射、竞品内容实测、社区问答）。
2. **定稿与排期**：两层查重 × ICE 优先级 ≤ 漏斗配比 → 进入选题队列。
3. **生成**：multi-turn 状态机（outline 确认 → 分机器回头隔器（单轮不限 token 端口）→ 全文整合）。
4. **四道机器门禁**：pre-write（路径/字段）→ post-write（≥7,500 词 / H2 密度 / 违禁词）→ GEO 可用性（来源 URL/可摘录性）→ quota（数量预算）+ lang（语言纯度）。任一 BLOCK 不过不进下一步。
5. **mapped into S4-qa 状态**：草稿状态机推进 → **止步 ready**。
6. **人审授权**：老板/市场负责人在工作台点「发布」。**未授权绝不发布**（不自动无人值守）。
7. **发布**：默认接你的 CMS（当前未接）。发布 dry-run 查重 → 真实写库 → sitemap / IndexNow。
8. **复用链**：长文发布即触发衍生计划——摘要稿（≤600 词）→ 社媒卡 → newsletter 段。分发走 multi-platform-push。

**内容质量的三层保险**：L1 导入前机审（BLOCK>0 停）→ L2 导入后抽样 → L3 发布前五维（合规/文化/可读性/SEO/品牌）。

---

## 六、真实案例（后台实测记录）

**案例 A · 一次成品（ST1）**：《Script to Shot List: The Agent-Assisted Breakdown》（分镜/镜头清单词群，P0 空档）——走完整链路 2 轮定稿，被门禁验收后进入 S4-qa 等人审。已生成并存档，在后台回路可见。

**案例 B · 门禁打了回去（价值 demonstrating）**：《Short drama storyboard workflow》（10-05 上午）——《短剧分镜流程》同词群，3 轮都过不了质量门禁（词汇/统计密度/组段节奏不达标），机器标记 blocked，要求人工接管重写。**这正是"不会发生 781 篇灌水事故的措施"**——系统的自我诚实比产量重要。两篇都是同一词群，成功的那篇说明门禁不针对题材，只针对质量。

**案例 C · 选题队列现状**：队列中现成 3 条已 trace 的选题——《AI previsualization (previz) for live-action shoots: a practical guide》（cluster-previz · P1）、《How agencies produce TV commercials with AI》（cluster-ads · P1）、《AI short drama production: how teams scale…》（cluster-shortdrama · P0 空档）——CMS 接入后可直接排产。

以上全部案例可在 MFlow 后台「项目 → Moodio Global → 内容」查看原稿（server 路径 run/projects/moodioglobal/content/）。

---

## 七、人工接管清单（老板 / 市场老大要做什么）

**马上需要拍的板（阻塞项，按优先级）**：

1. **CMS 项目接入**：Moodio 的内容来源还是占位 ID（your-project-id）。给我 CMS 类型（Sanity 最顺，其他也行）与项目凭据 → 半天接通 → 后台 preset（内链审计/多语言覆盖/QA 扫描）立刻从配置变成实用。
2. **案例合规确认**：《了不起啊！朋友》状态复核；如果不在公开状态，vs/Case 页的案例证据线暂时用竞品实测（05-competitors 规则）内替代。
3. **预测账号充值/换 key**：DeepSeek 账号已到 0（402），生产/预演均暂停中的生成、以预演免费为主。充值后不用改任何配置。**重要：同 key 在 GitHub 公开仓库历史中曾部署过（Bing key / GCP OAuth 已从仓库删除），建议全部轮换一轮，别复用旧 key**。
4. **token 消耗审计结论**：后台自动化每天实际消耗 <1 美元；大头在 agent 长会话侧。已治理：dry-run 全部零 LLM 生成、Moodio auto_loop 暂停、3 份冗余 QA merged、全局熔断上线。
5. **站点上线节奏**：GSC 上线后流量巡查（低 CTR 刷新/衰减刷新）即刻从"配置"变成"日常"。

**每篇文章人审重点（拿着 S4-qa 稿子往下看）**：

- 品牌事实：有没有八条红线违规、有没有 Lovart 术语渗入、CTA 是否只有"申请内测码"。
- 产品数据：所有数字是否都有来源（未验证的应标 [待考证]），不许有任何可见占位符。
- 金句与 \"翻车\"段：这篇有没有观点（如果通篇安全话，退回）。
- 内链：综述之内部链接是否只指向已验证 slug。
- 案例/证据：开头证据是否可用 vs 用了未经授权案例。
- **通过 → 工作台点发布授权；不通过 → 退回重写指定段落，机器会回流。**

**日常不需要人做的**：词群地图维护（月审自动）、QA 扫描（后台剧本）、alt 补齐、内外链审计、GEO 探针、404 扫描（上线后）、排程与配方的新增（管理员通过剧本 UI）。

---

## 八、SSOT 快速引用

- 词群地图：`harness/Skills/02-creation/blog-writer/references/keyword-clusters.json`（Moodio 12 簇/4 KR/黑名单/baseline）
- 选题计划：`harness/Skills/02-creation/blog-writer/references/strategy-content.md`（漏斗配比/五轴/SD/AD/ST/DEF/VS/EX 系列/Silo/复用链/北极星）
- 方法论：`.../references/methodology-content-writer.md`（12 类型矩阵/11 框架配对/Anti-AI v4）
- 类型骨架：`.../references/types/{type}/GUIDE.md`
- 品牌差异配置：`harness/Skills/infra/gates/brand-profiles/{lovart,moodio}.json`
- Moodio 入口 skill：`harness/Skills/02-creation/moodio-film-content/SKILL.md`（含不可迁移清单）
- 能力抽象：`harness/Skills/infra/CAPABILITY-MATRIX.md`（Lovart→Moodio 承载映射/四类数据源）
- 公司说明（全系统，书一个尤其适合对内同步）：`docs/CONTENT-SYSTEM-GUIDE.md`
