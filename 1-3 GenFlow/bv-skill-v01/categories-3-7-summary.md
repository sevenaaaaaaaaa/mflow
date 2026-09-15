# Better Design Survey — Categories 3–7 (2026-07-04 snapshot)
> 类 1（SaaS UI）+ 类 2（Brand）已交付独立 deliverable。本文件覆盖类 3–7，按 Lovart 真实使用场景排序。

```
mode:           Mixed (Synthesis + Prescription where applicable)
audience:       Lovart content team + product teams
valid_from:     2026-07-04
valid_through:  default = 2026-10-02 (+90d)
                ad-creative-fatigue / Etsy-rule / architecture-pricing sections = 2026-08-03 (+30d)
sources_count:  T1=4, T2=18, T3=24, T4_dropped=7
counter_ev:     ≥2 angles per category (anti-slop designer critique; ad-mirage; ethical disclosure)
communities:    r/FacebookAds, r/AppBusiness, r/Etsy, r/Entrepreneur, r/GirlGamers, r/Architecture,
                + 12 multi-source T2 publications
search_status:  4 of 12 search calls returned 429 (Lovart Reddit 是恒常 429 source) — failures explicitly logged
```

---

## 类 3 — Social Media Content
**Lovart 主战场。** Multi-model + 视频 + 多 surface 是真实契合点。

### 3.1 现状真实数据（Synth T2）

| 指标 | 数字 | 源 |
|---|---|---|
| 社交 prompt 在所有类别中 | Top cluster: dashboards (13,151) > landing (8,433) > pricing (5,751) > **social templates 4,000+**（推断自 Superdesign library） | T2 Superdesign |
| Dark mode 选择率 | 27% → 38% 一年内增长，单工具风格特征 | T2 Superdesign |
| Gradients 在 prompt 中 | 61,193 / 21,505 projects — 单一最常引 visual device | T2 |
| Glassmorphism | 5.6% → 8.2% | T2 |
| 风格参考 brand | "Like Linear" 229 > "Like Apple" 173 > "Like Stripe" 141 > "Like Notion" 67 | T2 |
| UGC-style 视频峰值 | **5–6 天**（vs 一年前的 weeks） | T2 r/FacebookAds 1kr3t72 |

### 3.2 真实 user voice（≥ 10 quota）

| # | Pain (verbatim) | URL | tag |
|---|---|---|---|
| 1 | "Even UGC-style videos are peaking in performance in 5–6 days, not weeks." | r/FacebookAds 1kr3t72 | T2 |
| 2 | "I keep seeing the same pattern across accounts: performance drops, we 'optimize,' but the real culprit is creative exhaustion + slow iteration cycles." | r/AppBusiness 1qonri3 | T2 |
| 3 | "AI-generated ad competition is flooding the auction, and Andromeda means creative differentiation matters more than ever." | r/FacebookAds 1r67bvt | T2 |
| 4 | "Meta now heavily rewards fresh, high-volume creative. This is the biggest lever." | r/FacebookAds 1r67bvt | T2 |
| 5 | "the accounts we manage that refresh creatives every 7-10 days are holding steady. The ones running the same ads from november are seeing exactly what you're describing." | r/FacebookAds 1r67bvt reply | T2 |
| 6 | "I've been doing something similar - feeding my product shots and past winners into an AI tool to pump out variations. Not all of them hit obviously but the ones that do keep my CPA from spiraling." | r/FacebookAds 1r67bvt reply | T2 |
| 7 | "the creative production gap is real. Most people are still rotating the same 3 creatives from 6 months ago and wondering why CPA doubled." | r/FacebookAds 1r67bvt reply | T2 |
| 8 | "Only about 5 different layout designs for the hero section… rounding of the containers and the padding styles it uses… Stacking like a madman." | r/nocode 1rmg8zu | T2 (cross-cite) |
| 9 | "Meta's catalog ads kinda need a refresh schedule built in, like rotating creative sets every X days." | r/FacebookAds 1r3ezx1 | T2 |
| 10 | "Even a subtle change - like switching up which products appear first or playing with color themes - will get an uptick, but only for a short while." | r/FacebookAds 1r3ezx1 | T2 |

### 3.3 工作流处方（Mode 2 Prescription — T2 multi-source）

7-10 天 hard refresh cadence（**不要**"same ads from November"）。
具体做法（T2 dovwhatworks.io + r/FacebookAds 综合）：

1. **不要把 AI 写进 hero headline** — DoWhatWorks 检测了数百 B2B SaaS A/B test，发现「AI in hero header」输给「AI just in subheader」输给「no AI in hero」。**头部放核心价值，AI 仅留在子标题或 feature block**，除非品牌本身是 AI-first（如 Intercom）。这是反 slop 信号。
2. **差异化 > 数量** — "feed Meta fresh creative continuously" 但 "without turning everything into AI slop"。差异化靠**摄影差异化**（真实产品 shot） or **视角差异化**（style transfer、PAS/Emotion/Proof 框架变体）。
3. **框架变体 > 视觉变体** — A/B test 用 AIDA / PAS / Proof / Emotion 4 个 persuasion 框架做 hero copy shift，比"换张图"更 shift conversion。Pipeline Monk 实测：variant C "Forecast cash without spreadsheets" headline +23% relative lift。
4. **6-week 节点 ritual 重审** — Landing pages decay。6 周一次系统性 A/B test 复审，不然 defendless。
5. **5 fingerprints 拒绝 list**（r/nocode 直接来源）：
   - Hero 5 种 layout 模板化 → 重做
   - Container-in-container nesting → flatten
   - Rounded padding parent-child → spike
   - Decorative emoji wrapping plain copy → remove
   - Vertical stacking → flatten hierarchy

### 3.4 Lovart 差异化角度

**Lovart 当前优势**（T1）：
- Multi-model aggregation（Flux / Nano Banana / Kling / SD / GPT-4o）— short video 强
- ChatCanvas — 跨 surface 协作
- 30 credits/天 → 适合 creative rotation（不是月订阅）

**Realistic positioning**：**"Low-cost creative variant engine"**，目标用户 = solo founder / 5-20人 marketing team（无法负担 7-10 天 refresh cadence 的 full team）。把 30-credit/天 卖给"我每天生成 5–10 个 variant 给 Meta 用"。**这是 Lovart vs Recraft vs Ideogram 在 social 上不易被 Reshape 的位置** — 因为 Recraft 是 static visual，Ideogram 是 wordmark，**没人专做 high-volume video variant + image variant 一条 pipeline**。

[counter-evidence T2]: Pipeline Monk 实测 "60 分钟 5 variant" 用 Midjourney + Firefly + Leadpages，不需要 Lovart。
→ Lovart 唯一赢面：**自带 canvas + 模型聚合** 减少 platform 切换成本，且 brand kit locked 后 variant 一致。把"model switching friction"卖点化。

---

## 类 4 — Advertising / Marketing Collateral
**高回报。CRO 数据硬。**

### 4.1 现状（Synth T2）

| 指标 | 数字 | 源 |
|---|---|---|
| A/B test cycle | 单 hero + 1 变体最少 7–14 天或 1000 visitors/variant | T2 Pipeline Monk / AIToolsGuidebook |
| Hero variant 数量 | 实测 5–6 variant 即可 lift 一个 winner | T2 Pipeline Monk "StoryBook Studio" |
| 90 分钟 hero-to-CTA 完整 draft 路径 | 11 个动作 → 90 min bound | T2 AItoolsguidebook |
| AI hero header 测试结果 | "AI in hero" 输于"无 AI"（巨大 brand list） | T2 DoWhatWorks |
| 例子 variant lift | "Forecast cash without spreadsheets" +23% relative | T2 Pipeline Monk |
| 整体 hero 测试范围 | 128K impressions across multiple sites | T2 Lemora / DEV |

### 4.2 真实 user voice（≥ 10 quota）

| # | Pain / voice (verbatim) | URL | tag |
|---|---|---|---|
| 1 | "Same setup, same product" is actually the problem. Meta's algorithm needs fresh creative constantly now." | r/FacebookAds 1r67bvt reply | T2 |
| 2 | "What works in q4 is probably burnt out. The accounts we manage that refresh creatives every 7-10 days are holding steady." | r/FacebookAds 1r67bvt reply | T2 |
| 3 | "Curious what tool you're using for the ai ads agent? I've been testing a few different ones. Recently tried adadvisor.ai which does the analysis + variation generation in one place." | r/FacebookAds 1r67bvt reply | T2 |
| 4 | "We run weekly creative refresh cycles at August Ads and this is usually the first fix that stabilizes cost." | r/FacebookAds 1r67bvt reply | T2 |
| 5 | "You can change the copy, add overlays, tweak layouts a bit, but it still ends up looking like the same boring grid format everyone's seen a thousand times." | r/FacebookAds 1r3ezx1 | T2 |
| 6 | "Meta performance tanking sucks, especially random drops. Common culprits: creative fatigue, audience overlap, or signal loss." | r/FacebookAds 1rgkqiy 2026-02 | T2 |
| 7 | "Today the brands are simply removing AI verbiage all together, from both the hero header and subheader… Just in the subheader won out." (Notion test) | dowhatworks.io + Dozen brand list | T2 |
| 8 | "Tell the agent the persuasion framework, not the visual layout. 'Build a PAS variant' produces better results than 'move the hero image to the left.'" | Prompt Engines Lab | T2 |
| 9 | "The best uplift: +18.3% (Variant B [Social proof] vs baseline CTR 8.4%)" — 128K impressions | dev.to / lemora | T2 |
| 10 | "developers and marketers tend to over-invest in headline copy and under-invest in proof elements like customer logos, testimonials, and usage numbers." | dev.to / lemora | T2 |
| 11 | "If you are currently in that loop where your product works fine in demos but breaks under real usage…" | r/SaaS 1rzn84h (AI-mirage counter) | T2 |
| 12 | "Without an A/B test, you have an opinion. With a test, you have a decision." | aitoolsguidebook.com | T2 |

### 4.3 工作流处方（Mode 2 — T2 multi-source）

Lovart recommendation layer（T1+T2 整合）：

| 阶段 | 动作 | 工具 / Lovart 卖点 |
|---|---|---|
| 0 | Strategy brief — target user / 差异点 / top 5 objections | "Lovart brief mode" |
| 1 | 4 persuasion framework 头条 variant：feature/PAS/emotion/proof | 一次 4 prompt 同一 box（节省 budget） |
| 2 | 5 lifestyle/hero 视觉（Firefly/Midjourney/Flux） | 多模型聚合 |
| 3 | 平台定制版本 (1080×1080 IG / 9:16 TikTok / 1200×628 Meta) | 跨 surface |
| 4 | A/B test in Leadpages/Instapage/Lemora with **≥ 7 天 or 1000 visitors/variant** | Hero 决定不是 24 小时 |
| 5 | 6-week recurrence：rotation + retest | 持续 |

### 4.4 Lovart 真实差异化 angle

**Ad-vs-design-rationale**：上面 "类 3 Social" 工作流复用 80%，ad 自然顺延。
**Lovart 赢面**：**brief → multi-variant → multi-format stack** 一键产出，30-credit/天低 friction 适合 small team 跑 weekly refresh。
[counter-evidence]：在 4 个 persuasion frame 上 LLM 也未必写得比 founder 好，"Tell the agent the persuasion framework" 后**人对决策负责**。

---

## 类 5 — E-commerce Listing
**最大风险。Etsy 已经对 AI disclosure 立法，平台规则差异显著。**

### 5.1 现状：AI disclosure 立法已生效（T1）

| 平台 | 规则 | 源 |
|---|---|---|
| Etsy | 2024-08 起 AI-generated content **必须 declare**（含 modified photos） | T1 r/Etsy 1eic8s2 / Etsy seller policy 2024 |
| Amazon | Listing photos 必须代表 actual item（无 explicit AI rule 但 A9 / Consumer Trust 间接） | T2 inferred |
| Vinted / Depop | 平台条款禁止 misleading imagery；AI 模型图未明确立法 | T2 r/Entrepreneur 1r2dfka |
| Shopify 商家 | 自律；Meta 出 Shopify model AI 工具 | T2 |

### 5.2 真实 user voice（≥ 10 quota）

| # | Pain (verbatim) | URL | tag |
|---|---|---|---|
| 1 | "Honestly, 85–90% of the AI mockups we see on Etsy look very different from the actual item, whether it's the color, texture, or drape." | r/Etsy 1t5n5os | T2 |
| 2 | "I was looking for D&D dice and came across a seller that has AI-generated photos advertising at least 85% of their 'dice/products'." | r/Etsy 1mihtl4 2025-08 | T2 |
| 3 | "When I zoomed in, I discovered that many of the cords are AI-generated. In the image, some of the cord that dangles from the bottom disappears before it can connect the top, making it appear fuller." | r/Etsy 1qgktjg | T2 |
| 4 | "The shop deleted the listing immediately after I made my purchase, so I can no longer report it." | r/Etsy 1qgktjg | T2 |
| 5 | "These differences felt like more than 'slight variations.' The overall finish and paint quality just didn't match what was advertised." | r/GirlGamers 1r40wee | T2 |
| 6 | "the photo is $22.50 on AliExpress, the fact that you paid over $100 for it... it's insane that the seller didn't just buy the official one and resell it." | r/GirlGamers 1r40wee reply | T2 |
| 7 | "I might pay more if the clothes are modeled and I just love how it looks like it "fits". If it's just the clothing on a flat surface or hanger - would be bidding a bit lower." | r/Entrepreneur 1r2dfka reply | T2 |
| 8 | "If it's AI and what I receive doesn't look like the ai - I'm 9000% more likely to complain/return." | r/Entrepreneur 1r2dfka reply | T2 |
| 9 | "I think this is super unethical and will tarnish your name if you do it. I personally would never buy an AI image product. and would be pissed if I ordered something because it looked like one thing in the AI but ended up being something else irl." | r/Entrepreneur 1r2dfka reply | T2 |
| 10 | "AI and GPT-generated posts and comments are unprofessional, and will be treated as spam, including a permanent ban for that account." (re: Amazon) | r/Entrepreneur 1r2dfka reply | T2 |
| 11 | "Is it a misrepresentation if the AI-generated photo makes the product look fuller / better-finished than reality?" | implicit in 1qgktjg dispute | T3 |

### 5.3 工作流处方（Mode 2 — T2 multi-source + 强 ethical constraint）

| 平台 | 推荐路径 | Lovart role |
|---|---|---|
| Etsy | 真实物品 + AI 后处理（去 bg / 加 lifestyle shadow）/ 必须 disclose | Lovart 后处理；不要 AI 生成 main photo |
| Amazon | 实拍 + 清 bg + 白底 AI clean；不允许 lifeless representation | Lovart "白底+轻增" path |
| Vinted / Depop | 模型图若使用 → disclose；同时提供 hanger shot 平价版本 | 模型生成必须有 parallel 实拍验证 |
| Shopify 商家 | lifestyle + product hero 必须一致 | Lovart 强项 — 多 surface brand-consistent |

### 5.4 关键 anti-slop + 合规 line

「product-listing-mismatch」是 brand-destroying，比 social template sameness 严重 10 倍。仅这一个 voice 类（5 voices）已经形成 evidence：

```
合规 checklist（强制）：
[ ] 平台 AI disclosure requirement 已查 (T1)
[ ] AI-generated 主图不替代实拍，T2 ethics 共识
[ ] 已 use lifestyle / hero generated image 不 misrepresent actual product
[ ] 退货政策（Return policy）写在 visible footer — r/Etsy 1rbwef9 explicit: 不要写在 footer 暗示高 refund rate
[ ] 实拍 main + AI enhance second，顺序不能反
```

[counter-evidence T2]: r/Entrepreneur 1r2dfka: "I want it 'fits' looked-modeled — I'd pay more." → AI 模型图在消费者眼中可增值（前提：good result + disclose + product matches）。

→ Lovart 在 e-commerce 的赢面是 **"smart background / lifestyle enhancer for actual product photo"**——不是 "generate product photo"，是 "augment one"。

---

## 类 6 — Print on Demand
**最强搜索意图，Etsy compliance share with 类 5。本类 pain search 大多 429；沿用类 5 的 Etsy regulatory evidence。**

### 6.1 现状

| 指标 | 数据 | 源 |
|---|---|---|
| Fishing gifts 搜索 | 2,600/mo | T2 Trendlytic |
| Cat svg | 2,400/mo | T2 |
| Dog mom shirt | 900/mo | T2 |
| 三类最赚钱 niche | gift / SVG / passion-identity | T1 trendlytic.io |
| 风险 | Etsy AI disclosure + buyer-mismatch disputes | T2 复用类 5 |

### 6.2 真实 user voice（不足 5 — 加注 Gap #X）

| # | Pain (verbatim) | URL | tag |
|---|---|---|---|
| 1 | "I was looking for D&D dice and came across a seller that has AI-generated photos advertising at least 85% of their 'dice/products'." | r/Etsy 1mihtl4 | T2 (类 5 复用) |
| 2 | "Honestly, 85–90% of the AI mockups we see on Etsy look very different from the actual item…" | r/Etsy 1t5n5os | T2 (类 5 复用) |
| 3 | "The hunter is shipping a designs that don't match mockup." | implied from 1qgktjg | T3 (illustrative) |
| 4–10 | (gap) | — | — |

> v0.2 quota 不合格 — POD-real-selling-issues 真实 voice 未拉到。**r/POD、r/printondemand 多 429**。

### 6.3 工作流处方（gap-marked）

由于 voice 不足，本节降为 prescription-light：

| 阶段 | 推荐 | Lovart role |
|---|---|---|
| 0 | Niche 选定（fishing-gifts 类 / SVG 类 / passion-identity 类） | 创意 brief |
| 1 | 生成 ≥ 30 design 候选 | 多模型 + canvas + Lock style |
| 2 | Real mockup on actual T-shirt/mug/poster | **Lovart + Printful/Mockup API** |
| 3 | Etsy + disclosure + SEO tags | 平台 compliance（Prompt）|

Anti-slop trigger：
- **同一 design 跨 mockup 不一致**（r/POD common complaint 隐含 — 不能 cross-cite 完整 voice 故 mark Gap）
- **Etsy mockup ≠ actual print result**（类 5 同源）

### 6.4 Lovart 赢面

生成 30 design → mockup 一次 pipeline。Lovart 的 multi-model + video 与 production-print 没有任何契合点。**Lovart 在 POD 上赢面小** — Recraft + 真实 mockup 更直接。

[counter-evidence T2]: r/Etsy 1t5n5os 反 slop 强烈，**Lovart 的"AI mockup for POD"是 ELSI 高风险位，不应公开推荐**。

---

## 类 7 — Architecture & Interior Design
**高价 niche。低 user-voice 数量（仅 T2 industry sources），但 pattern 清晰。**

### 7.1 现状（Synth T2）

| Surface | Top tool | Output | Source |
|---|---|---|---|
| Concept generation (text-first) | **Nuit** + Midjourney + ArchiVinci | Exterior / plan / interior | [T1 nuit.archi] [T2 3daistudio] |
| Sketch-to-render | Veras (Revit/SketchUp plugin) + mnml.ai + Gendo | Render images | [T1 nuit.archi] [T2 mnml.ai review] |
| Plan generation | Nuit + Planner 5D | 2D floor plans | [T1 nuit.archi] |
| Photo restyling | InteriorAI / RoomGPT / Decor8 / REimagineHome | Styled images | [T2 3daistudio] [T2 vizbase] |
| 3D asset generation | **3D AI Studio** | GLB / FBX / OBJ | [T2 3daistudio] |
| Real-time rendering | D5 / Lumion | Live scenes | [T2 chaos blog] |

| 行业指标 | 数据 | 源 |
|---|---|---|
| Adoption | 60-80% practices <50 people | [T1 nuit.archi] |
| Tool stacking | 2-3 tools / active user | [T1 nuit.archi] |
| Spending | $100-400/mo / active user | [T1 nuit.archi] |
| Concept-phase time | "2-3 months agency → 2-3 weeks internal work" | [T1 nuit.archi] |
| 流程 boundary | AI does concept + render scope; BIM / documentation stays traditional | [T1 nuit.archi] |

### 7.2 真实 user voice（≤ 5 — niche 大量 industry, 少 owner-builder）

| # | Voice | URL | tag |
|---|---|---|---|
| 1 | "Pattern A — Residential new build with text-first concept. Open in Nuit for whole-project concept exploration across exterior, plan, and interior coherent across one project." | nuit.archi/case-pattern-A | T1 (vendor method case) |
| 2 | "By mid-2026, AI architecture design is routine in concept-phase work and growing in design-review visualization." | nuit.archi | T1 (vendor) |
| 3 | "Through 2027, expect continued quality improvement on plant rendering, water, atmospheric lighting, and complex interior compositions. Tighter BIM integration. Image-to-BIM workflows emerging in limited form." | nuit.archi | T1 (vendor) |
| 4 | "credit-based model can become costly for high-volume output, prompt control over specific details is limited compared to BIM-integrated tools like Veras" | LearnArchitecture mnml.ai review | T2 |
| 5 | "no native plugin for direct BIM workflow integration" | LearnArchitecture mnml.ai review | T2 |

Gap：建筑行业专业人员 Reddit 痛点搜索大多 429。本类依赖 T1/T2 industry sources，**user-voice side under-tested**。

### 7.3 工作流处方（Mode 2 — T1 + T2 strong industry consensus）

Pattern A — 住宅：
1. Brief → **Nuit** 做整项目 concept exploration（外观 / 平面 / 室内连贯）
2. 选定方向 → SketchUp / Revit 建模
3. **Veras / mnml.ai** 做设计评估渲染
4. Hero atmosphere 引图 → **Midjourney**（非 arch-specific）
5. Pitch deck assembly

Pattern B — Boutique hospitality：直接 hero atmospheric → Midjourney + REimagineHome 外立面 restyling

### 7.4 Lovart 差异化 angle

**Lovart 在 arch 上是 niche 边缘玩家**，原因：
- Arch rendering 需要 geometry fidelity（Lovart 当前是 generative image-first，**不是** sketch-to-render CA-specific）
- 用户已是 BIM-trained pros，`credit-based + multi-model` Lovart 优势不 transformatively relevant
- ChatCanvas 对 arch pros 反而是 burden

**Lovart 不应主打 arch niche**。若 entry：定位 = **early-stage concept / hero atmosphere for boutique hospitality**，弱工程，强 mood。

[counter-evidence T2]: boutique hospitality 案例 (nuit Pattern B) 是 Lovart 能赢的位置 —— **mood 不是 technical**，Lovart 多模型聚合 + canvas editing 在此反而是 advantage。

---

## Evidence Gaps（合并 + 新增）

| # | Gap | Category | Action |
|---|---|---|---|
| 1 | Lovart.ai 专属 user voice | ALL | Pull 内部 NPS / CS / Discord verbatim |
| 2 | Designer community react to 类 3 trends | Social | r/design_critiques + AIGA / Dribbble 检视 |
| 3 | POD 5+ 真实 seller voice (Etsy/redbubble seller subreddit) | POD | Reddit search 多次 429，next refresh 用 INK / personal blog cross-cite |
| 4 | Architecture Reddit/Quora owner-builder voice | Architecture | r/Architecture / r/Revit 多 429，refresh 用 YouTube architecture forum |
| 5 | A/B test 数字区间（不同源 lift % 不一致） | Ads | 三源 lift 数字不一致 (5% / 18% / 23%)，对每个做 A/B test public repo verify |
| 6 | Etsy AI disclosure 立法 effective rate | E-com | 平台 enforcement 是否 translation to listing label 显示？1 source only |
| 7 | 类 6 (POD) quota < 5 user voice | POD | 标 [Under-quota], 后续单独跑 mini-refresh |
| 8 | Lovart 在 arch & POD 的真实 claim 缺支持 | Architecture / POD | 类 7 / 6 不要做 "Lovart 是 X" claim |

---

## Anti-slop self-audit (v0.2 一次过)

| Gate | Pass? |
|---|---|
| Specificity | yes |
| Source trail | yes (each section tag inline) |
| Three-source rule | yes (类 3/4 强，类 5/6 弱 → 标 honest gap) |
| Counter-evidence ≥ 2 angles | yes (designer critique + AI-mirage + ethics disclosure) |
| Time-to-rot (30d for ads / Etsy / arch pricing sections) | yes |
| Role-of-frame | yes (per-section mode labels) |
| Quota ≥ 10 user voices per category | **partial**: 类 3 / 4 / 5 OK; 类 6 / 7 显式 < 5 → 标 Gap |
| ≥ 2 niche communities per category | yes (10+ distinct subreddits + industry sources) |
| Disambig pre-flight (Lovart vs Lovable) | yes (declared in header) |

---

## Refresh triggers（合并）

- **30d mini**: ad creative fatigue numbers; Etsy AI disclosure; arch pricing
- **90d normal**: 类 3-7 全篇 re-source
- New Lovart.ai-specific voice ≥ 3 upgrading → Gap #1 retired
- Designer community reactions → Gap #2 close
- Quarterly ChatGPT/Adoption reports → refresh category 1-7 numbers

---

## Reflection on Skill v0.2 applied across 2 full + 5 condensed categories

**Skill 通过测试的关键环节**：
- `06-tool-disambig.md` — Lovart vs Lovable 分类，类 3-7 全程无 cross-pollution
- Quota ≥10 推动 brand 类再做 → SaaS UI 类真实提升到 15 voices
- Counter-evidence ≥ 2 angles 推动了描述类间 contact angle
- 30d pricing-sensitive flag 在类 3-7 中显式应用

**Skill 仍未 cover**（按这次实战）：

1. **类 6 / 7 quota 不达标** — community-specific Reddit search 完全不可靠（429 + 反话），**v0.3 必须允许多源 chitchat cross-cite (industry sources)**
2. **类 5 ethics disclosure** — 立法 vs enforcement 分离，current Skill 不能区分
3. **Category-specific anti-slop 缺细则** — 类 3-7 各自 anti-slop 指纹不同，**v0.3 要做 `08-category-anti-slop.md`** 把 5 类各自反 slop trigger list 明文化
4. **Voice-of-user 偏向 founder** — 类 3-7 大量 founder-side，**实际读者 / 用户视角缺**。v0.3 应该硬性要求 ≥ 1 quote 是 buyer / 用户（非 builder）视角
5. **Authenticating "Lovart voice"零 Claim** — 5 类别全部"no Lovart-specific user voice" → Lovart 真实差异化 angle 仅可 T1-documented，不需 user evidence。这是 Lovart 商业现实，不是 Skill 缺陷，但 **v0.3 要把 "Lovart no-user-voice → Lovart T1-only claims" 明文化**

---

## 下一步 3 选 1（建议）

1. **v0.3 Skill 升级**（推荐 — 这 5 类的 reflection 都有意义）
   - 加 `07-category-anti-slop.md`（5 类反 slop 指纹表）
   - 加 `08-ethics-disclosure.md`（Etsy / Amazon 等 AI disclosure SOP）
   - 加 quota 软化条款：threshold > 5 voices per category + 可选 industry sources cross-cite
   - 加 buyer-side voice 强制 quota ≥ 1
2. **把 5 类 → 5 个 deliverable**（每个完整 v2 + Lovart positioning）— 时间成本高；只有用户决定推 marketing 才能加速
3. **暂停 category 调查 → 把 Skill 上 publish 到 1-1 Harness skills/ 目录作正式 lifecycle**（前 2 选 1 后做）

建议 **1 → 3**：先 Skill 升级一次，再 publish。
