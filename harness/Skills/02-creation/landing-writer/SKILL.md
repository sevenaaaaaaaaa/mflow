---
name: landing-writer
description: >-
  品牌落地页/页面创作唯一入口（深度整合版：分类→故事线→模块文案→按钮文字 四层决策内置 + CRO 五维 +
  7 条转化向故事线）。止步发布前（发布走 sanity-publish）。
  Use for 「生成/修复/重写/刷新 Tools、Features、Product、Solution、Scenario、Topic、Landing」。聚合页/Hub/目录/榜单 → `hub-writer`（独立技能，生成逻辑不同）、
  页面 SERP 文案、composite-v2、页面 SEO/JSON-LD、配图、CTA 按钮。
---

## 预算（RULES-70 强制）

落地页文案 600–1000 词 · H2 4–7 · FAQ 3–5 · 每千字 1–3 数据点 · 外部来源 2–5 条 · 列表 ≤4 不连续 · 单段 ≤300 字符 · 字数不足删冗余不补形容词。
交付前四门禁：`post-write-check.sh` · `geo-check.sh` · `quota-check.sh` · `lang-check.sh`。

## 第零层 · 策略对齐（先于四层决策）

- 页面主词： 词群（共享，不另建）
- 投放承接页：——渠道→故事线→CTA 语气匹配；白名单页资格 = cro-audit ≥80
- 黑名单词命中 → 不建页，退回词群评审

## 四层决策（生成任何页面前逐层过，全部留痕到"策略说明"）

### 第一层 · 分类（页面类型 → 轨道）

| 页面类型 | 轨道 | 输出格式 | references/ 模板 |
|---|---|---|---|
| **Tools**（category: tool，单工具页） | C | composite-v2 JSON，每语言 1 文件 → `Page Gen/Pages/Tools/{lang}/` | `tools-v2-template.md` |
| **Landing**（投放向） | D | composite-v2，12–15 段 | `landing-ssot/landing-v2-template.md` + 故事线 JSON |
| **聚合页 / Hub**（目录/榜单/主题入口） | → **`hub-writer`** | 独立技能：聚合=拓扑+分发逻辑，与转化页不同 | — |
| **Features / legacy** | A | 单文件 10 个 `section_xx` key | `json-template.md` + `pages/features-legacy.md` |
| **JSON 修复/诊断** | B | 诊断报告 + 重建 | `landing-master.md` §轨道B |
| **存量页刷新**（storyline-driven） | 隶属 C/D/E | bodyJson/type 序列 | `pages/refresh-page-generator.md` |

判断口诀：单 job 转 → C；买量/竞品词落地 → D；"best/all/榜单/大全" → **hub-writer（不在本技能）**；旧六区块体系 → A；拿到 JSON 报错 → B。未说明类型先问一句。

### 第二层 · 故事线（7 条，intent 以故事线为准，禁止自定义）

| 故事线 | intent | 叙事 | 何时用 | routingSignals 关键词 |
|---|---|---|---|---|
| `landing-trial-now` | search-convert | 分屏首屏→prompt 试用→三步上手 | 搜索转化、工具词、"try free" | try free / free trial / prompt / tool keyword |
| `landing-vs-competitor` | competitor-conquest | 首屏→对比→before-after | 竞品词、"vs/alternative" | competitor / alternative / vs / versus |
| `landing-brand-trust` | brand-upper-funnel | 电影感首屏→logo→testimonial | 品牌词、upper-funnel、信任建设 | brand awareness / upper funnel / trust |
| `landing-offer-close` | retarget-offer | journey 首屏→定价→评论墙 | 再营销、offer、回收犹豫流量 | offer / discount / retarget / pricing intent |
| `landing-gallery-detail` | acquire-broad | gallery 首屏→能力→工具矩阵 | 泛需求、看案例驱动的访客 | gallery / examples / showcase |
| `landing-gallery-funnel` | acquire-educate | gallery→能力→流程教育 | 教育型泛需求 | learn / how it works / education |
| `landing-full` | internal-demo | 15 段满配 | **仅内部 demo/QA**，禁作投放 | — |

规则：`PAGE-BRIEF → 选故事线 → 读全维度绑定 → 生成 → COPY-PREFLIGHT`。6 维绑定（文案/模块/个性化/配图/CRO/质检）全以故事线为准；迭代改故事线绑定（`genflow/Page Gen/Refresh-Page/landing-storylines.json` + `page-copy-bindings.json`），不另写规则。

### 第三层 · 模块文案规则（七要素打底 + 模块细则）

**七要素**（每页必须全落到正文）：Buyer / Input / Output / Edit path / Proof / CTA / FAQ。
**Hero 四件套**：主语 + 输入 + 输出 + 风险降低点（hub 页第三件套替换为 inventory=资产清单 + navigation=导航承诺 + startHere=从哪开始）。禁抽象口号。
**Proof 六类强证明**（logo wall 只算弱）：deliverable / workflow / output format·rights / before-after / verified example / limitation·trade-off。每页 ≥1 类强。
**FAQ 异议优先级**：商用版权 → 输入输出格式 → 编辑协作 → 适用边界 → 与竞品/相邻页区别；hub 页加"从哪个工具开始"。≥3 条。
**模块细则**：
- `prompt-launcher`（trial 页 required）：给**真实可试**的输入样例，不放空占位
- `tool-grid`（hub/trial/vs required 核心矩阵）：每卡 = 子页主词 title + 1 句差异化描述 + 标签；**禁复述子页原文**；卡链到对应 Tools 子页
- `comparison-table`：只列可验证差异；vs 页用 `comparison-before-after` 叙事化，禁"类别/我方/竞品"三列表格当主结构
- `cluster-block-dense`：集群内链块，每链 = 已验证 slug + 一句"这页解决什么"
- `blog-grid`：卡 = 文章 title + 收益句；链到已发布博客
- `workflow-horizontal`（3 步）vs `workflow-vertical`（详叙）：快速上手用横、深度流程用竖
- `canvas-wall` / `showcase-*`：案例墙 = 强 proof；配图走 image_pool，禁编造
- `faq` 永远在 `cta-default` 之前（O1 收口序）

### 第四层 · 按钮文字（流量来源 × 阶段，ctaStyle 由故事线决定）

| ctaStyle（故事线） | 主按钮语气 | 示例 button_text |
|---|---|---|
| `trial`（trial-now/tools） | 消除风险、立即上手 | "Start Free — No Credit Card" / "Try Brand Free for 14 Days" |
| `compare`（vs-competitor） | 并排比较、随时可切换 | "Compare side by side" / "See the workflow before you switch" |
| `brand`（brand-trust） | 信任先行、看真实案例 | "See real campaigns" / "Watch the workflow" |
| `offer`（offer-close） | 稀缺+行动 | "Claim your plan" / "Upgrade now" |
| `educate` / `solution` / `default` | 教育转化 | 按引擎默认分支 |

**流量来源微调**：Google 付费广告 → 消除风险（No Credit Card）；SEO/内容 → 价值先行（Free for 14 Days）；社交 → 速度效果（in Seconds）；邮件 → 便捷（Your Free Account）；联盟 → 好奇（Explore）。
**注入字段**：CTA → `hero-split.buttons` / `cta-default.buttons` / `prompt-launcher.cta`；紧迫感 → 拉新 `hero.tip`、激活 `contentSection[].title`、转化 `testimonial.description`。按钮引擎按 ctaStyle 生成（`scripts/lib/landing-copy-rules.js` buildCtaSection），人工写时对齐上表语气。

## CRO 五维（Persona Matrix）

| Persona | 谁 | 核心指标 | FAQ 第一优先 | 语气 |
|---|---|---|---|---|
| `ecom` | 电商卖家（Shopify/TikTok Shop） | 周产出×时间成本 | 商业版权/转售权 | 直接、数字优先 |
| `saas` | 产品/设计团队负责人 | 迭代周期、一致性 | 团队协作与权限 | 专业、结果导向 |
| `brand` | 品牌/内部创意工作室 | 跨市场部署 | 企业授权与 SLA | 高端、创意总监 |
| `agency` | 代理商/自由设计师 | 客户吞吐量 | 白标与客户报告 | 共情、伙伴 |
| `creator` | 个人创作者 | 速度、触达 | 变现与收益 | 社区感、轻松 |
| `generic` | 混合 | 速度+质量 | 免费试用 | 中立平衡 |

行业信任信号：电商=转化率数据 / 广告=A-B 测试 / 媒体=版权合规 / 建筑=渲染速度+4K / 游戏=风格一致 / 服装=批量上新。
**Social Proof 数字**必须溯源（官网/官方报告），无出处 → `[待考证]`，禁编造。

## 轨道速览（细节 → references/landing-master.md）

- **A legacy 六区块**：JSON 骨架 `json-template.md`；6 区块齐 + heroSection 第 1 位 faqSection 末位 + 10 语言（`section`/`_zh-CN`/`_zh-TW`/`_ja`/`_ko`/`_de`/`_fr`/`_ru`/`_pt`/`_it`）+ 分批协议（≤3 语言/批）+ Banned Patterns
- **B 诊断修复**：判型（composite-v2 vs legacy）→ 结构/完整性/资源三类诊断 → 报告（Critical/Copy/Resource/Language）→ 重建
- **C Tools**：单 job 页面原则；prompt-launcher 真实样例；每批 ≤3 语言文件；C5 自检 `preflight-content.js --type tools --strict` + `convert-tools.js --dry-run`
- **D Landing**：12–15 段；copy 必须与故事线意图严格对齐（trial=上手路径 / vs=可比较差异 / trust=品牌级结果 / offer=少教育多 why-now / gallery=Hero 与矩阵间要有桥）

## 溯源与配图（零幻觉）

来源优先级：① 已验证图片库（`references/image-library.md`）+ 自动选图 `references/landing-ssot/image_pool.py`（match_title/get_image/assign_images_to_features；hash 不截断/词边界正则/CJK 精确子串/同页同语言一套 URL）② 用户参考 JSON ③ 官方文档 ④ 网络核实 → 无法确认标 `[待考证：… — 建议联系产品团队确认]`。技术参数/价格/兼容/集成/用户数据/竞品对比六类必先查证。

## 术语（官方）

MCoT Engine · ChatCanvas · Nano Banana Pro · Agentic Intelligence · Touch Edit · Text Edit。
品牌定位：AI Design Partner，Thinking in Systems。核心钩子：零门槛、自动化流、商业级 4K、全图层可编辑。

## 元数据输出（JSON 后必须）

SEO TDK（slug / title≤60 / description≤160 / keywords 5–8）+ OG/Twitter Card + FAQPage JSON-LD（仅英文，name/text 与 section 原文逐字一致）。

## 自检清单（交付前逐项）

composite-v2（C/D/E）：schemaVersion · storylineTemplate 合法 · bodyJson 无 legacy type · 模块序列与故事线 sections 一致 · 10 语言齐 · media.src 来自图库或 [待考证]。
Legacy（A/B）：6 区块齐 · hero 首位 faq 末位 · 10 语言齐 · image_url 全图库 · 无 Banned Patterns · Persona 已声明 · FAQ 含商用版权+操作门槛 · JSON-LD 逐字一致 · 分批格式正确。
跨轨道：`genflow/Page Gen/Refresh-Page/COPY-PREFLIGHT.md`（storyline-driven）。

## 关键路径

```
genflow/Page Gen/Refresh-Page/          ← 故事线 SSOT（landing-storylines.json 9 条 + page-copy-bindings.json + COPY-PREFLIGHT + PAGE-BRIEF）
dev/品牌.sanity.studio/scripts/          ← Sanity 脚本
harness/Skills/03-review/sanity-preflight  ← 发布前结构校验
```
