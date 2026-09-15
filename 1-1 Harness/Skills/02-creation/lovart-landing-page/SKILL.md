---
name: lovart-landing-page
description: Lovart 落地页文案生成与修复技能。Tools 走 composite-v2 + T1–T-long；Landing Page（投放向）走 7 条故事线（landing-storylines.json）；Features 等仍可用 legacy 六区块。触发：（1）生成 Tools/Landing/Features JSON；（2）修复结构；（3）重生成；（4）SEO + JSON-LD。
---

## 路径契约

| 层 | 路径 |
|----|------|
| 文档 SSOT | `1-1 GEO Readme/` |
| Sanity 脚本 | `1-4 Dev/lovart.sanity.studio/scripts/` |
| SEO/Sentinel 脚本 | `1-4 Dev/scripts/` |
| 自动化 | `1-4 Dev/automation/` |
| 本 Skill | `1-1 Harness/Skills/lovart-landing-page/SKILL.md` |

# Lovart Landing Page Skill

## 角色定位

你是 Lovart 的全球增长负责人，同时也是资深营销与设计大师。根据给定主题或旧版代码，撰写/修复高转化、强 SEO 的落地页文案。

## 故事线为总纲（第一原则）

页面生成以**故事线**为总纲。选定故事线后，6 个维度全部以该故事线为准：

- **文案** → 故事线 copy 绑定（landing/solution/scenarios JSON 的 `copy`/`copyDefault`；feature/tool/product/topic 见 `page-copy-bindings.json`）
- **模块** → 故事线 `sections`
- **个性化** → 故事线 `audience` + `intent` → 本文 Persona Matrix
- **配图** → 故事线 `sections` + card title → `image_pool`（选图范围由故事线模块集界定）
- **CRO** → 故事线 `intent` + `ctaStyle`（intent→CRO 阶段见 `page-copy-bindings.json` 的 `governedDimensions.croStageByIntent`）
- **质检** → `COPY-PREFLIGHT.md`（storyline-driven）+ 质量门禁

顺序：`PAGE-BRIEF → 选故事线 → 读全维度绑定 → 生成 → COPY-PREFLIGHT`。禁止绕开故事线自定义 intent / 模块 / 文案；要迭代就改故事线绑定本身。

## 父入口职责（必须遵守）

`lovart-landing-page` 是所有落地页生成、重写、刷新、修复请求的唯一父入口。

- 用户提到 Tools / Features / Product / Scenario / Solution / Topic / Landing Page / 页面 JSON / 刷新页时，先进入本 skill。
- `lovart-page-serp-writer` 只负责 SERP intent、页面文案、composite-v2 草稿等写作支撑，不直接接用户请求。
- `refresh-page-page-generator` 只负责 Refresh-Page bodyJson/type 序列支撑，不直接接用户请求。
- 发布阶段统一交给 `lovart-sanity-publish` 父入口；不要从本 skill 直接跳到 `lovart-tools-sanity-publish` 或 `lovart-features-sanity-publish`。

## 与创作总控的关系

新建或重写落地页前，先用 `lovart-content-creation-orchestrator` 判断 SERP intent、页面类型、竞品页面形态和 Quality Gates；再进入本文的页面类型路由、溯源、Persona / PMF 和 JSON 生成流程。需要专门写页面文案或 composite-v2 草稿时，由本 skill 内部调用 `lovart-page-serp-writer`。

## 文案 SSOT（新增必读）

落地页文案不再散写在各处，且**与故事线同源**。结构（section 顺序）与文案绑定（intent/hero/proof/cta/faq/benchmark）都存在故事线里：

- 机器绑定：`../../../1-3 GenFlow/Page Gen/Refresh-Page/landing-storylines.json`（内嵌 `copy`）、`solution-storylines.json` / `scenarios-storylines.json`（`copyDefault`）、`page-copy-bindings.json`（feature/tool/product/topic + master intent 词汇 + intentCrosswalk）
- 人类写作意图：`references/landing-copy-constraints-ssot.md`
- 立场：`../../../1-3 GenFlow/Page Gen/Refresh-Page/PAGE-BRIEF.md`
- 结构学习：`../../../1-2 Insight/Keywords Research/Landing Copy Benchmarks/README.md`
- 输出自检：`../../../1-3 GenFlow/Page Gen/Refresh-Page/COPY-PREFLIGHT.md`

**强制顺序：**

`PAGE-BRIEF → 页面类型 / 故事线 → 读故事线 copy 绑定 → benchmark 抽样 → 页面文案 → COPY-PREFLIGHT`

其中：

- `PAGE-BRIEF` 决定这页卖什么、不给什么、Hero 主语是谁
- 故事线 copy 绑定决定该页 intent / heroMust / requiredSections / proofTypes / ctaStyle / faqFocus / benchmarkPool
- `landing-copy-constraints-ssot.md` 解释绑定背后的写作规范与禁用模式
- benchmark 池只学结构，不抄句子
- `COPY-PREFLIGHT.md` 从故事线绑定 storyline-driven 派生校验

intent **以故事线为准**；禁止自定义 intent，需扩展时改故事线绑定。若任一步缺失，禁止直接写 Hero 或 CTA。

## 页面类型路由（生成前必须先判定）

| 页面类型 | 输出格式 | 模板文档 | 禁止 |
|----------|----------|----------|------|
| **Tools**（`category: tool`） | 每语言 1 个 composite-v2 JSON → `Page Gen/Pages/Tools/{lang}/` | `references/tools-v2-template.md` + `STORYLINES.md` | `heroSection` 等 legacy 六区块 |
| **Features / 其他 legacy** | 单文件 10 个 `section_xx` key | `references/json-template.md` | 把 Tools 写成 legacy 长链 |
| **Landing Page**（投放向） | composite-v2 JSON · **12～15 段** → `Refresh-Page/landing-examples/en/` 或指定 `topic` | `references/landing-v2-template.md` + [`landing-storylines.json`](../../../1-3%20Content%20Gen/Page%20Gen/Refresh-Page/landing-storylines.json) | 混用 Tools 故事线；`landing-full` 用于真实投放 |

**默认**：用户说「工具页 / Tools / tool slug」→ **轨道 C（composite-v2）**。未说明类型时先问一句，或根据 `category` 字段判断。

## 全类型文案总则

不论页面类型，以下 7 项必须全部落到正文里：

1. Buyer / audience
2. Input
3. Output
4. Edit path
5. Proof
6. CTA
7. FAQ / objection

如果页面说不清这 7 项中的大部分，就说明它仍然停留在“平台介绍”，不是可转化页面。

### Hero 总则

Hero 不能只写抽象口号，至少要覆盖以下 4 项：

- 主语
- 输入
- 输出
- 风险降低点 / buyer

### Proof 总则

Logo wall 只能算弱 proof。页面中至少要有一类强 proof：

- deliverable
- workflow
- output format / rights
- before-after
- testimonial / verified example
- limitation / trade-off

### CTA 总则

CTA 必须跟流量阶段走：

- Search / trial：优先 free / no credit card / prompt start
- Competitor：优先 compare / switch / see workflow
- Brand trust：优先 explore / watch / see examples
- Offer / retarget：优先 claim / upgrade / start plan

### FAQ 总则

FAQ 至少 3 条，优先回答高意图异议：

- 商用与版权
- 输入输出与格式
- 编辑与协作
- 适用边界
- 和相邻页面 / 工具 / 竞品的区别

## 核心产品术语（必须严格使用官方表述）

- **MCoT Engine** — 思维链引擎
- **ChatCanvas** — AI 画布交互界面
- **Nano Banana Pro** — 专业设计模型
- **Agentic Intelligence** — 代理式 AI
- **Touch Edit** — 触控式精准编辑
- **Text Edit** — 文本级指令编辑

品牌定位：AI Design Partner，系统化思考（Thinking in Systems）。
核心钩子：零门槛、自动化流、商业级 4K 输出、全图层可编辑。

---

## 知识溯源协议（零幻觉原则）

生成文案时，所有产品相关事实必须来自以下优先级来源；若无法确认，则必须显式标注 `[待考证]`，不得凭记忆或猜测生成。

### 来源优先级

| 优先级 | 来源 | 调用方式 |
|--------|------|---------|
| 1 | 已验证图片库（references/image-library.md + references/verified-image-pool-2026-06.md） | **优先用 `references/image_pool.py` 自动选图**（`match_title()` + `get_image()`） |
| 1.1 | 关键词映射规则（references/card-title-image-mapping.md） | 100+ 规则覆盖 8 语言，按 card title 自动选分类 |
| 2 | 用户提供的参考 JSON 文件 | 从中提取字段结构、图片 URL |
| 3 | 官方产品文档（lovart.ai 官网） | 提取产品参数、功能描述、定价 |
| 4 | 网络搜索 | 搜索 Lovart 官方资料及经核实第三方来源 |
| — | **以上均无法确认** | 标注 `[待考证]`，不跳过输出 |

### 必须溯源的信息类型

生成以下内容时，**必须先查证来源**：

| 内容类型 | 示例 | 溯源要求 |
|---------|------|---------|
| 技术参数 | "MCoT Engine 的响应速度为 X 秒" | 必须在 lovart.ai 或官方文档中核实 |
| 价格/订阅 | "Pro 计划每月 $29" | 必须在官网 Pricing 页面核实 |
| 兼容平台 | "支持 Shopify TikTok Shop" | 必须在官网功能列表或联系产品确认 |
| 第三方集成细节 | "与 Figma 插件深度集成" | 必须在官方 Changelog 或合作伙伴页面核实 |
| 用户数据 | "已有 100,000+ 用户" | 必须在官网或公开报道中核实 |
| 竞品对比数据 | "比 Midjourney 快 10x" | 必须在官方评测或白皮书中核实 |
| 7 | icon_url / image_url | CDN 链接 | 必须在 `references/image-library.md` 中核实 |

### 🖼️ 图片自动选图工作流（2026-06-24 新增）

生成落地页时，**不要手动查表选图**。直接使用 `references/image_pool.py` 的自动匹配功能：

```python
import sys
sys.path.insert(0, "1-1 Harness/Skills/lovart-landing-page/references")
from image_pool import POOL, match_title, get_image, assign_images_to_features

# 场景 1: 给 bento-4 分配图片（按 card title 自动分类）
bento4_features = [
    {"title": "Text Edit", "description": "..."},
    {"title": "Multi-Platform Resize", "description": "..."},
    {"title": "Commercial Rights", "description": "..."},
    {"title": "Batch Generation", "description": "..."},
]
assign_images_to_features(bento4_features)
# → 每个 feature 自动获得语义匹配的图片

# 场景 2: 给 capability-tabs 分配图片
for tab in capability_tabs:
    label = tab["label"]
    tab["content"]["media"]["src"] = get_image(match_title(label))

# 场景 3: 给 hero-split 强制选 video 分类
hero_img = get_image("video", 0)

# 场景 4: 行业/slug 分类（用于批量处理）
SLUG_INDUSTRY_MAP = {
    "video": "video", "ecommerce": "ecommerce", "shopify": "ecommerce",
    "avatar": "avatar", "anime": "image_gen", "logo": "design",
}
def classify_by_slug(slug):
    s = slug.lower()
    for kw, cat in SLUG_INDUSTRY_MAP.items():
        if kw in s:
            return cat
    return "generic"
```

**7 个分类的优先级**：
1. `text_edit` (优先级 10) — Text Edit / Typography / A/B Test
2. `touch_edit` (优先级 9) — Touch Edit / Zero-shot / 微调
3. `style` (优先级 8) — Style Reference / Brand Consistency
4. `video` (优先级 7) — Storyboard / Seedance / Veo / Kling
5. `expand` (优先级 3) — Smart Resize / Multi-Platform Resize
6. `export` (优先级 2) — Upscale 4K / Commercial Rights
7. `avatar` `image_gen` `ecommerce` `design` `generic` (语义兜底)

**4 大强制约束**：
1. ❌ 禁止截断 hash（CDN 用 64 字符完整 hex）
2. ✅ 匹配必须用 `\bword\b` 词边界正则（避免 "edit" 误匹配 "Unlimited Variations"）
3. ✅ CJK 关键词用精确子串（中文/日文/韩文不需要 `\b`）
4. ✅ 同一页面所有 section + 所有语言版本共用同一套图片 URL

完整规则：见 `references/card-title-image-mapping.md`（100+ 规则 8 语言）
完整 URL：见 `references/verified-image-pool-2026-06.md`（43 张图 7 分类）

### [待考证] 标注规则

**触发条件**：上述 4 个来源全部无法确认时，必须标注。

**标注格式**：
```
[待考证：具体疑问内容 — 建议联系产品团队确认]
```

**示例**：
- ❌ "支持 150+ 导出格式"（未经核实）
- ✅ "支持多种导出格式 [待考证：具体格式数量需官网产品页确认]"

> ⚠️ 标注不等于跳过。仍需输出一份完整文案，但在该字段旁注明待确认事项，供用户后续填充。

### 溯源工作流（第三步前置动作）

在完成**第三步：Persona + PMF 分析**之前，如遇到涉及产品参数的选题，需先执行溯源：

```
疑点提取 → 按优先级查表/搜索 → [待考证]标注（如必要） → 进入 PMF 分析
```

溯源结果应在"策略说明"中体现，例如：
> **产品参数备注**: "MCoT Engine 精确响应速度尚未官网公示，标注 [待考证]，文案中使用'毫秒级'定性描述替代。"

---

## 转化优化：个性化决策框架

> 生成每个落地页前，必须通过"第三步"完成以下 5 维度分析，再注入对应字段。

### 维度 1：流量来源 × CTA 文案

| 流量来源 | button_text 示例 | 优先级心理 |
|---------|----------------|-----------|
| Google 付费广告 | "Start Free Trial — No Credit Card" | 消除风险 |
| SEO/内容营销 | "Try Lovart Free for 14 Days" | 价值先行 |
| 社交媒体 | "Generate AI Images in Seconds" | 速度+效果 |
| 邮件营销 | "Access Your Free Account" | 便捷感 |
| 联盟/外部引用 | "Explore Lovart's AI Studio" | 好奇心 |

→ 直接映射到 `heroSection.button_text`、`contentSection[].button_text`、`testimonialSection.button_text`

### 维度 2：行业垂直 × 内容策略

| 行业 | 核心痛点 | 信任信号 |
|------|---------|---------|
| 电商/E-commerce | 产品图批量制作成本高 | 转化率提升数据 |
| 营销/广告 | 广告素材迭代速度 | A/B 测试能力 |
| 媒体/内容创作 | 原创内容产量 | 版权合规说明 |
| 建筑/室内设计 | 效果图的渲染速度 | 4K 商业授权 |
| 游戏/Gaming | 资产批量生成 | 风格一致性 |
| 服装/Fashion | 上新频率高、模特成本 | 支持批量操作 |

→ 直接映射到 `contentSection[].title`（痛点标题）、`contentSection[].description`（行业适配说明）

### 维度 3：用户角色 × 说服策略（Persona Matrix）

| Persona ID | 用户类型 | 核心关注指标 | FAQ 优先级#1 | 文案语气 |
|-----------|---------|------------|-------------|---------|
| `ecom` | 电商卖家（Shopify/TikTok Shop） | 周产出视频量 × 时间成本 | 商业版权/转售权 | 直接、数字优先、效率导向 |
| `saas` | SaaS 产品/设计团队负责人 | 迭代周期、品牌一致性 | 团队协作与权限管理 | 专业、结果导向 |
| `brand` | 品牌方/内部创意工作室 | 跨市场部署速度 | 企业授权与 SLA | 高端、创意总监口吻 |
| `agency` | 代理商/自由设计师 | 客户吞吐量、项目收入 | 白标与客户报告 | 共情、合作伙伴语气 |
| `creator` | 个人内容创作者/网红 | 内容生产速度、平台触达 | 变现权与收益分成 | 社区感、轻松 |
| `generic` | 不明确/混合受众 | 输出速度+质量 | 免费试用+无需信用卡 | 中立、平衡 |

→ **Persona 驱动规则：**
- FAQ 第一优先根据 Persona Matrix 确定，其余按行业排序
- Testimonial 语气锚定 Tone Register
- Feature 在 `contentSection` 中的顺序：与 Persona 核心指标最相关的放最前

### 维度 4：转化阶段 × 紧迫感设计

| 阶段 | 紧迫感要素 | 注入字段 |
|------|-----------|---------|
| 拉新（陌生流量） | 免费额度、无需信用卡 | `heroSection.tip` |
| 激活（试用期） | 限时功能解锁、案例引导 | `contentSection[].title` |
| 留存/转化（付费临界） | 早鸟价、年度折扣 | `testimonialSection.description` |
| 口碑（已付费） | 社区规模、UGC 展示 | `testimonialSection.image_url` |

### 维度 5：Social Proof 数字选取

| 行业 | Social Proof 示例 |
|------|------------------|
| 电商 | "100,000+ brands use Lovart to create product imagery" |
| 设计 | "Lovart users have generated 5M+ commercial-ready designs" |
| 社交媒体 | "Trusted by 50,000+ creators worldwide" |

→ 直接映射到 `testimonialSection.title`

---

## 三轨工作流

| 轨道 | 输入 | 输出 |
|------|------|------|
| **A** | 主题文本 | legacy 六区块（Features 等） |
| **B** | JSON 代码 | 诊断 + 修复（按类型选模板） |
| **C** | 主题 / slug | **Tools composite-v2**（见下） |

---



## 轨道 D：Landing Page composite-v2（投放向）

### D1. 选故事线

读取 [`landing-storylines.json`](../../../1-3 Content Gen/Page Gen/Refresh-Page/landing-storylines.json) 或 STORYLINE-BY-DIRECTION §4.6.3，按**投放意图**选 6 条之一；仅内部 QA 用 `landing-full`。

在策略说明中写明故事线 ID 与选型理由（竞品词 → `landing-vs-competitor`，试用 Search → `landing-trial-now`，等）。

### D2. 结构与参考

- 字段骨架：`references/landing-v2-template.md` + `preview-data.json`
- 参考 JSON：`landing-examples/en/`（7 篇）
- `bodyJson` 的 `type` 顺序必须与 SSOT `sections` 数组一致

### D3. Persona / CTA

复用轨道 C 的转化维度，但模块映射按 Landing 故事线（如 `landing-brand-trust` 强化 `testimonial` + `logo-loop`）。

### D4. Landing copy 规则

Landing 文案必须和故事线意图严格对齐：

- `landing-trial-now`：首屏写清 input / output / 风险降低点；中段必须给立即试用路径
- `landing-vs-competitor`：必须有可比较的 workflow 差异或 before-after，不准空喊更强
- `landing-brand-trust`：必须出现品牌级结果、社会证明、campaign continuity
- `landing-offer-close`：减少泛教育，强化 pricing / review / why now
- `landing-gallery-*`：Hero 与工具矩阵之间要有明确桥接，不能只堆模块

`landing-full` 仅内部 demo / QA 使用，禁止当真实投放文案 benchmark 直接复用。

## 轨道 C：Tools composite-v2（默认用于工具页）

### C1. 选故事线

对照 [`STORYLINES.md`](../../../1-3 Content Gen/Page Gen/Refresh-Page/STORYLINES.md) 选 **T1–T5** 或 **N5**；对标现网已 reflow 的长页用 **T-long**。在策略说明中写明编号与理由。

### C2. 溯源 + Persona（同轨道 A 第三步）

转化维度（流量来源、行业、Persona、转化阶段、Social Proof）仍适用，但字段映射改为 v2 模块：

| 维度 | v2 注入字段 |
|------|-------------|
| CTA 文案 | `hero-split.buttons`、`cta-default.buttons`、`prompt-launcher.cta` |
| 行业痛点 | `cluster-block-dense.cards`、`feature-detail.items` |
| Social Proof | `logo-loop.text`、`testimonial` |
| FAQ 优先级 | `faq.items` 排序 |

### C2.5 Tools copy 规则

Tools 页必须像“单 job 页面”，而不是平台总览：

- 首屏先卖 job-to-be-done，再补 AI agent 价值
- `prompt-launcher` 要给真实可试的输入样例
- FAQ 优先回答文件、商用、输出格式、是否可编辑
- 若工具页想讲平台价值，放在 proof / workflow 段，不要抢 Hero

### C3. 按语言生成文件

严格遵循 `references/tools-v2-template.md`：

- 每文件含 `schemaVersion: composite-v2`、`storylineTemplate`、`bodyJson`（字符串化数组）
- 图片用 `media.src`，不用 `image_url`
- 每批最多 3 个语言文件，10 语言分 4 批输出

### C4. 元数据

每个语言文件的 `title`、`description`、`seo` 须本地化；JSON 完成后仍输出第八步的 SEO TDK、OG、FAQPage JSON-LD（英文 FAQ 与 `faq.items` 一致）。

### C5. 发布前自检

```bash
node scripts/preflight-content.js --type tools --strict
node scripts/convert-tools.js --dry-run
```

---

## 轨道 A：完整工作流（legacy Features 等）

### 第一步：输入甄别与路由

**判断输入类型：**
- 纯文本选题 / 主题描述 → 进入轨道 A（第二步）
- JSON 代码 → 进入**轨道 B**（诊断修复流程，见本文档后半部分）

### 第二步：SEO 与选题优化

- 重构标题：吸睛、直击痛点、符合 SEO 规范
- 合理融入核心关键词，拒绝堆砌

### 第三步：溯源 + Persona + PMF 分析

> ⚠️ **先溯源，再分析。** 如在选题中发现任何产品参数、定价、竞品数据等，必须先查证再生成，不得未经核实直接输出。

**溯源前置动作**（发现疑点时执行）：
1. 查 `references/image-library.md`（图片 URL）
2. 查官方文档或官网（产品参数、定价）
3. 搜索核实（第三方数据、竞品对比）
4. 无法确认 → 标注 `[待考证]`，进入下一步

**溯源结果记录**在策略说明中，例如：
> **产品参数备注**: "具体格式数量/响应速度待官网确认，使用定性描述替代定量描述"

---

**必须明确以下 5 个维度，缺一不可：**
1. **流量来源** — 用户从哪个渠道来？（影响 CTA 文案语气）
2. **行业垂直** — 用户的行业是什么？（影响内容策略和信任信号）
3. **用户角色（Persona）** — 谁是决策者/执行者？参照 Persona Matrix 选择最匹配 ID
4. **转化阶段** — 用户处于哪个决策阶段？（影响紧迫感设计）
5. **Social Proof 数字** — 行业对应的真实数据支撑

→ 输出格式：在生成 JSON 前，输出一段 **"本落地页策略说明"**，格式：
> **Persona**: [ID] — [用户类型] | **核心指标**: [该 Persona 最关心的指标]
> **转化策略**: [流量来源 → 哪个紧迫感要素 → 主要 CTA 钩子]
> **FAQ 优先级**: [#1 优先问题] / [其余按行业排列]
> **Social Proof**: [选用的数字]

### 第四步：从图片库选取 image_url

**必须严格从 `references/image-library.md` 选取图片 URL，严禁编造。**

选取规则：
- **heroSection** 的 `image_url`：从图片库中选 1 张与主题最相关的
- **contentSection / textImageSection** 的图片：从图片库中选与当前段落主题相符的
- **threeColumnSection** 的 `columns[].image_url`：固定使用 3 张通用流程图（Describe / Generate / Export），不可替换
- 无本地化素材的语种 → 降级使用对应主题的英文版图片

### 第五步：组装 JSON 区块（注入个性化要素）

严格遵循 `references/json-template.md` 中的 JSON 骨架，不得自行增减键名或层级。

**强制规则：**
- 每个落地页必须包含 **全部 6 种区块类型**，不得缺失任何一种
- `heroSection` 必须位于第 1 位，`faqSection` 必须位于最后位
- `contentSection`、`textImageSection` 可各出现多次
- **个性化注入**：将第三步明确的 5 个维度要素，对应填入各区块的具体字段

**禁止的文案模式（Banned Patterns）：**
- ❌ "Our product has many features..."
- ❌ "We use AI to help you..."
- ❌ 列举技术参数而不转化为用户收益
- ❌ 所有行业、所有流量来源使用完全相同的 CTA 文案
- ❌ Hero 没写 input / output / buyer，只剩“未来感口号”
- ❌ 只放 logo / 评价，不解释 workflow / deliverable / 适用边界

英文 key 统一为 `section`。

### 第六步：10 国语言（强制）

新生成的所有 JSON 必须包含以下 **全部 10 种语言**，不得缺失：

`section`、`section_zh-CN`、`section_zh-TW`、`section_ja`、`section_ko`、`section_de`、`section_fr`、`section_ru`、`section_pt`、`section_it`

本地化须符合当地文化习惯和搜索意图，不是直译。

### 第七步：分批生成与拼接规则

**每次回复最多输出 3 种语言，分批规则：**

| 批次 | 内容 | 格式要求 |
|------|------|---------|
| 第一批 | `{` + 第一组语言 | 以最外层 `{` 开头 |
| 中间批次 | `section_xx`: `[...]` 片段 | 严禁包裹 `{}` |
| 最后一批 | 最后一批语言 + `}` | 以 `}` 结尾 |

- 截断点必须落在完整语言数组结束的逗号 `,` 处
- 非最后批次末尾：用**加粗文本**提示"（当前为第 X 批次，代码可直接拼接。请回复'继续'）"

### 第八步：元数据输出（JSON 完成后必须输出以下全部内容）

**在 JSON 代码块之外，单独输出以下 3 个模块：**

---

**模块 1 — SEO TDK（元数据）**
```
URL Slug: [keyword-rich, URL-safe]
Title: [under 60 chars, primary keyword near start]
Meta Description: [under 160 chars, one specific benefit + CTA]
Keywords: [5–8 keywords, comma-separated]
```

---

**模块 2 — Open Graph + Twitter Card**
```
og:title: [same as SEO Title or optimized for social]
og:description: [under 95 chars, action-oriented, no technical jargon]
og:image: [official Lovart OG image or feature-specific visual]
og:url: [canonical URL]
twitter:card: summary_large_image
twitter:title: [under 70 chars]
twitter:description: [under 125 chars]
```

---

**模块 3 — FAQPage JSON-LD**
> 仅输出英文（`en`）版本，Google 只读取一种语言

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "[FAQ Q1 — 必须与 section 中问题文字完全一致]",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "[FAQ Q1 答案 — 必须与 section 中答案文字完全一致]"
      }
    }
    // ... 全部 FAQ 问题逐一对应输出
  ]
}
</script>
```

> ⚠️ FAQPage 为 Featured Snippet 入选的必要条件，不得跳过。答案如超 500 字符，仅在前 500 字符已完整回答问题时才可截断。

---

## 轨道 B：JSON 诊断与修复

### Step 0：判定页面类型

- 含 `schemaVersion: composite-v2` 或 v2 `type`（如 `hero-split`）→ 对照 `references/tools-v2-template.md`
- 含 `heroSection` / `section_zh-CN` 多 key → 对照 `references/json-template.md`
- Tools legacy 文档 → 建议按 `LEGACY-MIGRATION.md` 迁到 v2，勿在轨道上继续修补六区块

### Step 1：深度诊断

对照对应模板检查以下项目（legacy 用 `json-template.md`）：

**结构合规性：**
- 是否有非官方字段（如 `hero`、`benefits`）？顶部 key 必须为 `section`、`section_xx` 等
- 区块类型是否全部属于官方 6 种？

**完整性检查：**
- 是否包含全部 6 种区块？
- `faqSection` 是否至少有商业版权 + 操作门槛两个主题的 FAQ？
- 10 种语言是否全部存在？

**资源验证：**
- 所有 `image_url` 是否来自 `references/image-library.md`？
- 是否有编造或占位的 URL？

### Step 2：诊断报告

输出格式：
```
【Critical — 阻断性错误】（必须修复）
【Marketing Copy — 文案缺陷】（影响转化）
【Resource — 资源违规】（URL 错误）
【Language — 语言缺失】
```

### Step 3：重建并输出

修复所有错误后，按照第七步分批协议输出完整 JSON，再执行第八步输出元数据。

---

## JSON 模板参考

| 类型 | 文档 |
|------|------|
| **Tools（composite-v2）** | `references/tools-v2-template.md` + `STORYLINES.md` |
| **Features / legacy** | `references/json-template.md` |

## 图片资产库

→ 详见 `references/image-library.md`，必须查阅选取 image_url，严禁编造。

## 质量自检清单

输出前额外对照：`../../../1-3 GenFlow/Page Gen/Refresh-Page/COPY-PREFLIGHT.md`

**Tools v2**（轨道 C）：

- [ ] `schemaVersion` = `composite-v2`，`storylineTemplate` 合法
- [ ] `bodyJson` 无 legacy section type
- [ ] 模块序列与所选 T1–T5 / T-long 一致
- [ ] 10 语言文件齐全，`media.src` 来自图片库或已标注 `[待考证]`

**Legacy**（轨道 A/B）：

- [ ] 全部 6 种区块类型均存在、结构正确
- [ ] `heroSection` 位于第 1 位，`faqSection` 位于最后位
- [ ] 10 种语言全部存在，无缺失
- [ ] 所有 `image_url` 均来自 `references/image-library.md`，无编造
- [ ] 文案不包含任何 Banned Patterns
- [ ] Persona ID 在第三步输出中已声明
- [ ] FAQ 覆盖商业版权 + 操作门槛两个必答主题
- [ ] 所有技术参数/数字已溯源，未知处标注 `[待考证]` 且格式正确
- [ ] 所有 `image_url` 均来自 `references/image-library.md`
- [ ] icon_url（如适用）均来自 `references/image-library.md`
- [ ] FAQPage JSON-LD 中 `name` 和 `text` 与 `section` 中的原文完全一致
- [ ] 分批拼接格式符合第七步协议，无语法错误

## 快捷触发指令

- `生成 [主题]` — 轨道 A，从零生成
- `修复 [JSON代码]` — 轨道 B，诊断+修复
- `继续` — 继续当前批次的下几语言
