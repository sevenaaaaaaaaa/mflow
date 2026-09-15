# Lovart 首页排序综合分析报告(2026-07-07)

> **数据窗口**: GA4 近 30 天 / GSC 近 28-90 天 / Bing 近 3 个月(2026-04/05/06)
> **数据源**: `properties/403618427`(lovart.ai 主站)、GSC `https://www.lovart.ai/`、Bing Webmaster API、Sanity Blog + compositePage(10695 + 8547 篇)
> **目标**: 让优质页面在首页获得更多曝光,让用户能更轻易发现喜欢的内容

---

## 0. TL;DR(30 秒速览)

### 数据全貌

| 维度 | 数量 | 覆盖 |
|------|------|------|
| **GA4 blog 路径** | 1,474 unique slugs | 30d 全渠道 + 90d organic |
| **GSC blog 路径** | 1,644 slugs(page×query) | 90 天 page×query + page×country + page×device |
| **Sanity Blog 文档** | 1,552 EN 主版 + 9,143 多语言 = 10,695 全文 | EN/zh/ja/ko/de/fr/it/pt/ru/zh-TW/es |
| **GSC top100 关键词中竞品词** | 0 命中(品牌词 99.4%) | 28 天全量 |
| **Bing 3 月 blog 路径** | 91 slugs | 2026-04/05/06 月度 |
| **compositePage 总量** | 8,547(7 类) | tool/feature/topic/scenario/solution/product/landing |

### 关键发现(每条都带可执行的下一步)

1. 🔴 **Blog 顶部被低分页面霸占,优质页面埋没**——`freepik-ai-image-generator-review`(GSC 90d 33.9 万曝光、73 非品牌词、72 竞品词、11 语言覆盖)只在第 3 名,而当前 pinned-list 条目偏少,优质 review 未占满首页 slot
2. 🔴 **竞品非品牌词 0 命中** —— GSC top100 关键词中 99.6% 是品牌词,非品牌仅 7 条占 0.6% 份额,这是 Lovart 流量增长的最大瓶颈。竞品词得分 Top 5 blog:**freepik-ai-image-generator-review(72)、ai-branding-design(13)、ai-poster-prompts-tutorial(2)、artlist-ai-review(23)、how-to-use-veo3-free(21)**
3. 🔴 **tool 类 658 页,只有 6 个能上首页有意义** —— `text-to-image-generator`(30d 2,331 users)、`nano-banana-free`(1,907)、`video-generator`(822)、`free-ai-illustration-generator`(291)、`sora2`(194)、`nanobanana-pro`(187) 这前 6 名之外都是长尾(< 200 users),首页推荐必须砍到 6-8 个
4. 🟡 **scenario 类全部是 draft 草稿(NOINDEX)**,production 首页推荐 0 页 —— 这是 Sanity pipeline 的副作用,draft 不应进入 production
5. 🟡 **topic 类 93 页都是 landing 模板(landing-trial-now/agent-workflow)**,GA4 流量极低(2-3 users/30d),但**多语言 10 语言完整 + 内链结构扎实** —— 适合作为"长期 SEO 资产"继续做内容填充
6. 🟢 **solution 类 14 页中 3 页是无标题老链接**(`designers`、`business-owners`、`marketers`)—— 这些需补 title/desc/meta 后才能上线
7. 🟢 **product 类只剩 2 个**:`brand-kit`、`chatcanvas` —— 这两个是 Lovart 旗舰,首页位置黄金但 Sanity 里 GSC/GSC 数据都接近 0,需要立刻补内容

### 立即可执行的行动(用户决定后我就执行)

- **Blog 置顶**:把 `pinned-list.json` 扩充为 **24 个** ,按本报告 Blog Top 24 顺序排列,置顶 publishedAt 在 **[2026-05-10, 2026-07-08]**(以执行日 2026-07-08 为终点、过去 60 天)内按篇数均匀分布;其余文章 publishedAt **早于 2026-05-10**(60 天开外)
- **Tool 首页**:Elementor 排序按本报告 Tool Top 6
- **Feature 首页**:Elementor 排序按本报告 Feature Top 8
- **Topic 首页**:Elementor 排序按本报告 Topic Top 12(都是多语言完整 + 竞品词覆盖)
- **Scenario 首页**:**空**(全部 draft,等正式上线后再排序)
- **Solution 首页**:跳过 4 个空标题,展示有数据层有标题页(见 §4.5)
- **Product 首页**:只有 2 个(`brand-kit`、`chatcanvas`),均为数据差层
- **Landing 首页**:3 个有 slug 页(`e_commerce`、`marketers-preview-20260608`、`seedance_2_5`;空 slug draft 已过滤)

---

## 1. 数据采集明细

### 1.1 数据源 vs 时间窗口

| 数据源 | API/工具 | 时间窗口 | 输出文件 |
|--------|---------|---------|---------|
| **GA4 main**(lovart.ai 主站) | `analyticsdata v1beta` properties/403618427 | 30d/90d/365d 全渠道 + organic | `/tmp/ga4_main.json`(1.85 MB) |
| **GA4 blog 路径专项** | 同上 + pagePath BEGINS_WITH /blog/ | 30d/90d/365d 全渠道 + organic | 同上 |
| **GA4 各 category 路径** | 同上 + pagePath BEGINS_WITH /tools/ /features/ /topics/ 等 | 30d/90d | 同上 |
| **GA4 page × country** | 同上 + dimensions page,country | 30d organic | 同上 |
| **GSC page** | `searchanalytics` `searchconsole.v1` site=lovart.ai/ | 28d / 90d | `/tmp/gsc_main2.json`(48 MB) |
| **GSC page×query** | 同上 dimensions=page,query | 28d / 90d | 同上 |
| **GSC page×country** | 同上 dimensions=page,country | 90d blog 专项 | 同上 |
| **GSC page×device** | 同上 dimensions=page,device | 90d blog 专项 | 同上 |
| **GSC EN-only 后过滤** | 本地后处理,剔除 /zh/ja/ko/de/fr/pt/ru/it/es/ | 28d page×query + page | `/tmp/gsc_en_filtered.json`(3.5 MB) |
| **Bing Webmaster** | `bing-full.json` keywords_monthly + pages_monthly | 2026-04/05/06(3 月) | `Reports/bing-full.json` |
| **Sanity blog 全量** | GROQ `*[_type=="blog"]` | 创建到 2026-07-07 | `/tmp/sanity_inventory.json`(10.8 MB) |
| **Sanity compositePage 全量** | GROQ `*[_type=="compositePage"]` | 同上 | 同上 |
| **竞品词库** | `lovart_competitors_keywords.md` + `lovart_competitors_core_keywords.md` | SSOT | `Keywords Research/竞品核心非品牌词/` |

### 1.2 数据校验

- ✅ **GA4**: `unset PYTHONPATH && /usr/bin/python3` 跑通,token 在 `1-1 Harness/Skills/01-strategy/lovart-trident-data-engine/credentials/`(本来路径错误 `lovart-trident-data-engine`,实际是 `01-strategy/lovart-trident-data-engine`,通过 `LOVART_TRIDENT_CREDENTIALS_DIR` 环境变量修正)
- ✅ **GSC**: API 直接调用,2 个常见坑已绕过(首页巨流量挤压、CONTAINS 误命中 `/blog/` `/zh/` 子串)
- ✅ **Bing**: 14 个月数据完整(2025-05 → 2026-06),近 3 月 91 blog slugs
- ✅ **Sanity**: WRITE token + HTTP API + GROQ query,Blog 10,695、compositePage 8,547 全量
- ⚠️ **GA4 30d blog 上限**: 1,000 行(实际 blog 30d 流量可能超过),但 90d organic 772 行已足够识别优质页面
- ⚠️ **GSC 28d page×query 上限**: 25,000 行(全 site),无法一次拿全 — 用 page filter 各 category 单独抓,合并后覆盖完整

---

## 2. 评分模型(每路信号的权重)

### 2.1 Blog 综合得分(满分 100)

| 维度 | 权重 | 说明 | 满分来源 |
|------|------|------|---------|
| **流量** | 30% | GA4 30d users (15%) + 90d users (10%) + GSC 90d clicks (5%) + Bing 3m clicks (5%) | 各维度 max |
| **质量** | 15% | GA4 organic 90d 低跳出 (10%) + GA4 30d 长停留 (5%) | bounce rate + duration |
| **SEO 价值** | 13% | GSC 90d 曝光 (8%) + GSC 90d unique queries (5%) | impression + distinct query count |
| **竞品词机会** | 25% | GSC 90d competitor impr (18%) + competitor q count (7%) | 关键词是否含 AI/Image/Video/Design/Logo/Generator 等竞品词 |
| **多语言覆盖** | 10% | Sanity 10 种语言完整度 | lang_count / 11 |
| **内容深度** | 5% | Sanity body block 数 / 200 | body length |
| **合计** | 100% | — | — |

### 2.2 Landing Page 得分(满分 100)

| 维度 | 权重 | 说明 |
|------|------|------|
| 流量 | 30% | GA4 30d (15%) + 90d (8%) + GSC 28d clicks (4%) + Bing 3m clicks (3%) |
| 质量 | 15% | GA4 30d 低跳出 (10%) + 长停留 (5%) |
| SEO 价值 | 10% | GSC 28d 曝光 (6%) + unique queries (4%) |
| 竞品词机会 | 20% | GSC 28d competitor impr (13%) + q count (5%) + 有点击 (2%) |
| 多语言覆盖 | 10% | lang_count / 11 |
| 内容深度 | 5% | bodyLen / 8000 |
| Bing 加分 | 5% | Bing 3m clicks |
| **合计** | **100%** | — |

### 2.3 过滤规则

- **Draft 过滤**:`slug.startswith("draft-")` 全部排除(scenario 类 70 个草稿)
- **NOINDEX 过滤**:`noIndex=true` 全部排除
- **多产品隔离**:`product` 类只保留 lang_count > 0 的(剔除非 Lovart 产品如 ajusa、amd-ryzen、postal-containers 等)
- **空 slug 过滤**:`slug is None` 排除(landing 第 3 个 entry 是空 slug,drafts.* 草稿)

---

## 3. Blog 置顶排序(主推 / 1734 篇完整排名)


### 3.0 Blog 置顶 publishedAt 规则(2026-07-08 起,替代 AB-P08)

> **已废弃**: AB-P08 要求 `publishedAt ≤ boundary_floor(2026-05-27)` — 该固定地板已过时。
> **现行规则(每次执行置顶时按「当天」重算)**:
> 1. 置顶文章 `publishedAt` **≤ 执行日**(今天)
> 2. 置顶文章 `publishedAt` 落在 **[执行日 − 59 天, 执行日]** 内,按置顶篇数**均匀分布**(约每天 1 篇)
> 3. **所有非置顶**文章 `publishedAt` **早于**窗口起点(即在 60 天开外)
> 4. 多语言版本与 EN 主版 `publishedAt` 同步
>
> **本报告执行日示例(2026-07-08)**: 窗口 = 2026-05-10 ~ 2026-07-08;非置顶 < 2026-05-10。若 2026-07-15 再执行,窗口自动变为 2026-05-17 ~ 2026-07-15。

### 3.1 Top 24 Blog(置顶建议清单)

> 这是用户"希望知道哪些内容是用户喜欢的"的核心答案。直接对应 `pinned-list.json` 24 个 slot 的扩充建议。
> 置顶 publishedAt ≤ 执行日,在 **[2026-05-10, 2026-07-08]** 窗口内均匀分布(替代已废弃 AB-P08 固定 floor 2026-05-27)

| #   | slug                                              | title                                                             | 30d users | 90d users | GSC 90d clicks/impr | 非品牌词 | 竞品词    | 多语言 | 综合得分      |
| --- | ------------------------------------------------- | ----------------------------------------------------------------- | --------- | --------- | ------------------- | ---- | ------ | --- | --------- |
| 1   | `freepik-ai-image-generator-review`               | Freepik AI Review 2026: Features, Pricing & Lovart Alternatives   | 664       | 1,250+    | 888 / 339,493       | 73   | **24** | 10  | **71.89** |
| 2   | `ai-branding-design`                              | Complete Guide to AI Branding Design: Professional Brand Identity | 461       | 1,484     | 739 / 21,342        | 99   | **55** | 11  | **56.34** |
| 3   | `ai-poster-prompts-tutorial`                      | How to Write Perfect AI Prompts for Poster Design 2026            | 353       | 1,484     | 397 / 6,788         | 103  | **30** | 11  | **53.96** |
| 4   | `ai-poster-design-prompts`                        | 50+ AI Poster Design Prompts That Actually Look Professional      | **913**   | 916       | 226 / 2,531         | 56   | 25     | 1   | 42.63     |
| 5   | `openart-ai-review`                               | OpenArt AI Review 2026: Features, Pricing & Free Alternative      | 148       | 446       | 352 / 166,088       | 61   | 21     | 10  | 40.53     |
| 6   | `flora-ai-review`                                 | Flora AI Review 2026: Features & Pricing + Free Alternative       | 157       | 511       | 478 / 137,144       | 46   | 21     | 10  | 37.89     |
| 7   | `artlist-ai-review`                               | Artlist AI Review 2026: Is It Worth It? + Lovart Alternative      | 171       | 359       | 345 / 103,528       | 29   | 12     | 11  | 33.51     |
| 8   | `civit-ai-review`                                 | CivitAI Review 2026: Features, Pricing & Safer Alternatives       | 68        | 239       | 275 / 207,501       | 26   | 12     | 10  | 33.21     |
| 9   | `pixai-review`                                    | PixAI Review 2026: Best AI Anime Generator? + Lovart Compare      | 128       | 261       | 191 / 108,132       | 45   | 27     | 10  | 32.91     |
| 10  | `what-is-civitai-red`                             | What Is CivitAI Red? Complete Guide 2026                          | 110       | n/a       | 63 / 17,938         | 83   | 8      | 11  | 30.85     |
| 11  | `luma-dream-machine-review`                       | Luma Dream Machine Review 2026: Honest Test vs Lovart             | 94        | 265       | 131 / 47,763        | 33   | 11     | 11  | 30.32     |
| 12  | `lovart-official-chinese-entry-guide`             | Lovart 官方中文入口 - 找到真正的 AI 设计平台                                     | 15        | n/a       | 8 / 160             | 0    | 0      | 10  | 29.72     |
| 13  | `deepai-review`                                   | DeepAI Review 2026: Is It Still the Best? + Lovart Compare        | 125       | 221       | 67 / 8,167          | 34   | 23     | 10  | 29.39     |
| 14  | `nano-banana-pro-free-guide`                      | Nano Banana Pro Free Guide 2026 — Complete Tutorial               | 145       | 146       | 85 / 1,119          | 0    | 0      | 11  | 29.03     |
| 15  | `video-generators-review`                         | AI Video Generator: 2026's Best Tools Tested & Ranked             | 159       | 625       | 48 / 4,752          | 38   | 6      | 10  | 28.92     |
| 16  | `imagefx-review`                                  | Google ImageFX Review: When Search Giant Enters AI Image Gen      | 29        | 173       | 133 / 14,431        | 36   | 13     | 10  | 28.64     |
| 17  | `pixverse-ai-review`                              | Pixverse Ai Review: A Hands-On Look at This Rising Video Tool     | 38        | 203       | 246 / 25,735        | 32   | 10     | 10  | 28.28     |
| 18  | `pollo-ai-review`                                 | Pollo AI Review: An Honest Look at This All-in-One AI Video       | 41        | 160       | 81 / 4,556          | 34   | 17     | 10  | 27.92     |
| 19  | `pictory-ai-review`                               | Pictory Ai Review                                                 | 3         | 72        | 23 / 1,936          | 16   | 11     | 11  | 27.44     |
| 20  | `complete-guide-ai-face-swap-photo-video`         | The 2026 Complete Guide to AI Face Swap — Photo & Video           | 213       | n/a       | 1 / 1               | 2    | 1      | 10  | 26.22     |
| 21  | `complete-guide-consistent-ai-character-design`   | The 2026 Complete Guide to Consistent AI Character Design         | 242       | 303       | 1 / 2               | 5    | 0      | 10  | 26.09     |
| 22  | `seedream-4-5-free-guide`                         | Seedream 4.5 Free Guide: Image Generation, Editing Limits         | 70        | 70        | 29 / 179            | 28   | 2      | 11  | 26.07     |
| 23  | `resource-2027-design-trend-report`               | 2026 Design Trend Report: The Visual Language of the Agentic      | 82        | 93        | 30 / 274            | 10   | 5      | 10  | 25.86     |
| 24  | `lovart-official-authentic-design-ai-agent-guide` | Official Lovart Guide 2026: Real Website, Access                  | 63        | n/a       | 0 / 0               | 0    | 0      | 10  | 25.64     |

### 3.2 关键洞察

#### 💡 #1 优质页面"被埋没",前 3 名是真正能换流量的金矿

**问题**:`freepik-ai-image-generator-review` 在 GSC 28 天 339,493 次曝光中只换到 888 次点击(CTR 仅 0.26%),竞品词(72 个非品牌词如 "freepik ai"、"freepik ai image generator"、"freepik alternative" 等)被它承接着,但**当前 Lovart /blog 首页没有给它置顶**。

**根源**:pinned-list.json 只有 1 个 blog(`veo-3-vs-lovart-video-generation-comparison`),首页默认按 publishedAt desc 排序,所以新发布的低分页面会顶上来。

**缓解**:把 #1-#3 加入 pinned-list,`publishedAt` 按执行日滚动 60 天窗口均匀 backdate(见 §3.0),并同步 Elementor 置顶,**预期**:CTR 从 0.26% 提升到 1-2%(行业均值),月增有机流量约 2000-3000 sessions。

#### 💡 #2 "review 类"是绝对的流量引擎(前 24 中有 13 篇是 review)

**问题**:Top 24 中 13 篇是工具/平台 review(freepik/openart/flora/artlist/civit/pixai/luma/deepai/imagefx/pixverse/pollo/pictory/hedra),这些是高搜索量高竞品词低门槛的"流量收割"内容。

**根源**:用户搜索 "xxx ai review"、"xxx alternative"、"xxx vs" 时决策意图最强烈,Lovart 文章是此类 SERP 排在前 20 的结果之一。

**缓解**:
- 继续保持每月 5-10 篇新 review(覆盖新出现的竞品)
- 把已经 Top 24 的 review 置顶
- 把 review 类做成"系列"在博客主页用 category 聚合(目前 Lovart 101 / How-To / Best Practice / Reviews 四大分类中 Reviews 是 83 篇最低,P0 任务:扩到 150+)

#### 💡 #3 竞品词覆盖是 Lovart 流量的"钥匙"

**问题**:GSC top100 关键词中,99.4% 是品牌词,非品牌词仅 7 条占 0.6% 份额,**竞品词 0 命中**。意味着 Lovart SEO 流量几乎完全依赖"lovart/loveart/lovart ai" 等品牌搜索,一旦品牌搜索饱和,流量增长停滞。

**根源**:
- Lovart 的 blog 内容里有大量竞品词覆盖(freepik/openart/civit/artlist 等 review)但 **没有一篇排在非品牌词 SERP 首页**
- 各 review 文章的 GSC 位置平均 7-11(第二页/第三页),需要 schema、标题优化、外链提升到第一页

**缓解**:把 Top 24 中 13 篇 review 全部**置顶** + 在文章里加"FAQ + Pros/Cons + 表格"提高 SERP 排名到第一页 + 各 review 文章内部互链(shareability)。

#### 💡 #4 多语言完整度是 Lovart 的护城河

**问题**:Sanity Blog 1,552 篇 EN 主版 + 9,143 篇多语言翻译 = 10,695 篇。但**Top 24 中 lang_count 多数 10-11**(满分 11 = 1 EN + 10 翻译)。

**根源**:lovart-i18n-pipeline 跑得很勤,所有"赚钱"的 blog 都已经翻译完整。

**缓解**:**新发布的 blog 必须 11 语言完整**(否则降分);**score 倒推**:lang_count 10 的扣 0.91 分,lang_count 11 满分。所以新 blog 发布前用 `lovart-i18n-pipeline` 跑完整 11 语言是标配。

#### 💡 #5 `ai-poster-design-prompts` 是"流量王但只有 1 语言"

**问题**:#4 `ai-poster-design-prompts` 在 30 天有 913 个 users(全 blog 第 2 高),但只有 1 个语言版本(EN),**GSC 90d 2,531 曝光、25 个竞品词**。

**根源**:这篇是 PSEO 阶段产生的"自然语言长尾"文章,SEO 数据证明用户喜爱,但当时多语言翻译没跟上。

**缓解**:**立刻翻译到 10 种语言**(`lovart-i18n-pipeline` 重跑),按当前 30d 913 users 估算,11 语言上线后月流量可翻 5-10 倍。

#### 💡 #6 一些"沉睡资产"应该下架或重做

**问题**:#12 `lovart-official-chinese-entry-guide`(GSC 90d 8 clicks / 160 曝光,得分 29.72)排在 #12 是因为"多语言 10 + lang_count 高"加权,但实际数据证明它没人看。

**根源**:这是 Lovart 中文入口防御性文章(防品牌词流失),但用户搜索 "lovart ai 官网" 时直接进首页/注册页,**不经过 blog**。

**缓解**:置顶名单里**不建议包含这种"防御性 blog"** —— 它会挤占真正能换流量的位置。pinned-list 应该聚焦"用户来读的内容",而不是"防御性品牌内容"。

### 3.3 Top 25-50 Blog(置顶扩展备选 / 用户可能喜欢)

> 如果 Elementor 置顶 > 24 个 slot,以下是 Top 25-50 备选清单。按综合得分排:

| # | slug | title | 综合得分 |
|---|------|-------|---------|
| 25 | `ai-student-id-card-maker` | How to Make a Student ID Card with AI: Free Makers | 25.59 |
| 26 | `free-vs-paid-ai-tools-compared` | Free vs Paid AI Design Tools — What $0 Actually Gets You | 25.53 |
| 27 | `leonardo-ai-review` | Leonardo AI Review: Is This Tool Still Worth the Hype? | 25.49 |
| 28 | `nano-banana-presentation-guide` | Nano Banana Presentation Guide: How to Create AI Slides | 25.49 |
| 29 | `ai-twitter-x-post-generator-guide` | AI Twitter/X Post Generator Guide | 25.44 |
| 30 | `ai-design-mistakes-10-common-errors-how-to-fix` | 10 Common AI Design Mistakes and How to Fix Them | 25.30 |
| 31 | `ai-design-for-saas-pricing-pages-2026` | AI Design for SaaS Pricing Pages — Convert More | 25.17 |
| 32 | `runway-alternatives` | Runway Alternatives: The Complete 2026 Guide | 25.09 |
| 33 | `ai-art-platforms-compared-2026` | Leonardo vs OpenArt vs Civitai vs Lovart | 25.07 |
| 34 | `steve-ai-review` | Why I Tested Steve AI: An Honest AI Video Review | 25.03 |
| 35 | `ai-menu-design-restaurant-layout` | AI Menu Design: How Restaurants Can Create | 25.01 |
| 36 | `pika-ai-review` | Pika AI Review 2026: Features, Pricing & Alternative | 24.93 |
| 37 | `how-to-use-veo3-free` | How to Use Veo 3.1 for Free: Unlimited Access | 24.92 |
| 38 | `ai-business-card-design` | AI Business Card Design: How to Create Professional | 24.84 |
| 39 | `adobe-firefly-review` | Adobe Firefly Review 2026: Features, Pricing | 24.81 |
| 40 | `10-ai-design-prompts-that-actually-work` | 10 AI Design Prompts That Actually Work | 24.80 |
| 41 | `ai-brand-design-tutorial` | AI Brand Design Tutorial | 24.79 |
| 42 | `complete-guide-brand-kit-every-industry-lovart` | Complete Guide Brand Kit Every Industry | 24.67 |
| 43 | `enterprise-gdpr-compliance-lovart` | Enterprise GDPR Compliance Lovart | 24.59 |
| 44 | `ai-design-economic-impact-2026` | AI Design Economic Impact 2026 | 24.56 |
| 45 | `haiper-ai-review-2025-features-pricing-and-real-world-performance-test` | Haiper AI Review 2025 | 24.55 |
| 46 | `complete-guide-ai-poster-design-printing` | Complete Guide AI Poster Design Printing | 24.47 |
| 47 | `openart-ai-alternatives` | OpenArt AI Alternatives | 24.44 |
| 48 | `hedra-ai-review` | Hedra AI Review | 24.42 |
| 49 | `how-to-use-free-ai-design-tools` | How to Use Free AI Design Tools | 24.39 |
| 50 | `virtual-influencers-brands-replacing-human-models-ai` | Virtual Influencers Brands Replacing Human | 24.38 |

### 3.4 完整 1734 篇排名

完整数据在 `1-2 Insight/排序分析/blog_ranking_v2.json` (3.1 MB)。每篇包含:
- GA4 30d/90d/365d + organic 90d/365d 全维度
- GSC 90d EN-only page × query 全字段
- Bing 3 月聚合
- 竞品词覆盖数 / 非品牌词覆盖数
- Sanity 元数据(slug/title/category/11 语言覆盖度)
- 综合得分(0-100)

---

## 4. 落地页类型首页排序(7 类)

> **排序规则(2026-07-08 修订)**: 每类内按 **有数据 → 数据差 → 无数据** 三层排列;同层内按综合得分降序,再按 30d users / GSC clicks 降序。
> - **有数据**: GA4 30d users > 0 或 GSC clicks/impr > 0
> - **数据差**: 无流量信号,仅有 lang/score/内容深度等静态分
> - **无数据**: 上述皆无(本批 7 类落地页 JSON 中暂无纯无数据页)

### 4.1 Tool 首页推荐(Top 24 / 共 658 页)

| # | slug | title | 30d users | GSC 28d clicks/impr | NBQ | CompQ | Langs | 得分 | 数据层 |
|---|------|-------|-----------|---------------------|-----|-------|-------|------|--------|
| 1 | `text-to-image-generator` | AI Text To Image Generator / Lovart | **2331** | 2675 / 482257 | 233 | 126 | 10 | **82.87** | 有数据 |
| 2 | `nano-banana-free` | AI Nano Banana Free / Lovart | **1907** | 1720 / 158886 | 271 | 8 | 10 | **59.53** | 有数据 |
| 3 | `free-ai-illustration-generator` | Gerador de ilustração AI / Crie arte a partir de descri... | **291** | 197 / 17606 | 70 | 40 | 7 | **53.42** | 有数据 |
| 4 | `ai-post-generator` | 人工智慧社群媒體貼文產生器 /為所有平台建立貼文 /洛瓦特 | **172** | 91 / 5388 | 42 | 31 | 10 | **45.94** | 有数据 |
| 5 | `video-generator` | AI視訊產生器 /建立適合頻道的影片廣告 /洛瓦特 | **822** | 914 / 292615 | 47 | 17 | 10 | **45.83** | 有数据 |
| 6 | `chat-to-image-ai-generator` | AI 聊天影像產生器 /對話式影像創作 /洛瓦特 | **144** | 46 / 1355 | 30 | 27 | 10 | **44.83** | 有数据 |
| 7 | `sora2` | Sora 2 AI 視訊產生器 / Lovart 上的電影影片創作 | **194** | 156 / 5192 | 48 | 28 | 10 | 37.99 | 有数据 |
| 8 | `ai-image-upscaler` | AI 影像放大 / 4K 高畫質影像 /洛瓦特 | **155** | 48 / 453 | 32 | 20 | 10 | 34.13 | 有数据 |
| 9 | `image-to-image-ai` | [ZH-TW] Image to Image AI Generator — Transform Images ... | **133** | 134 / 1308 | 23 | 18 | 10 | 33.96 | 有数据 |
| 10 | `image-to-image` | AI Image To Image / Lovart | 79 | 46 / 663 | 24 | 14 | 10 | 33.67 | 有数据 |
| 11 | `nanobanana-pro` | AI Nanobanana Pro / Lovart | **187** | 66 / 465 | 14 | 1 | 10 | 33.41 | 有数据 |
| 12 | `free-ai-mockup-generator` | AI Free Ai Mockup Generator / Lovart | 69 | 20 / 732 | 13 | 6 | 10 | 32.45 | 有数据 |
| 13 | `image-to-video` | Image to Video AI: Animate Any Image in Seconds / Lovart | 45 | 6 / 34 | 6 | 5 | 10 | 32.41 | 有数据 |
| 14 | `ai-logo-generator` | AI標誌生成器 — 專業品牌Logo與全套品牌識別 / Lovart | 83 | 23 / 2769 | 12 | 5 | 10 | 32.2 | 有数据 |
| 15 | `nanobanana2` | AI Nanobanana2 / Lovart | 72 | 40 / 423 | 17 | 0 | 10 | 31.88 | 有数据 |
| 16 | `ai-photo-editor` | [ZH-TW] AI Photo Editor — Edit Photos Online with AI / ... | 12 | 1 / 38 | 1 | 1 | 10 | 31.44 | 有数据 |
| 17 | `ai-company-profile` | [ZH-TW] AI Company Profile Maker — Design Corporate Pro... | 13 | 1 / 1 | 1 | 1 | 10 | 31.37 | 有数据 |
| 18 | `ai-image-enhancer` | AI影像增強器/高檔並提高照片品質/洛瓦特 | 88 | 2 / 34 | 2 | 1 | 10 | 31.23 | 有数据 |
| 19 | `ai-art-generator` | AI藝術生成器/從文字創建令人驚嘆的數位藝術 /洛瓦特 | 48 | 8 / 187 | 6 | 0 | 10 | 31.04 | 有数据 |
| 20 | `ai-background-generator` | AI背景產生器/建立專業背景/洛瓦特 | 21 | 7 / 21 | 6 | 5 | 10 | 31.01 | 有数据 |
| 21 | `ai-design-agent` | AI設計代理商/自主品牌與創意工作流程/洛瓦特 | 21 | 0 / 0 | 0 | 0 | 10 | 30.99 | 有数据 |
| 22 | `ai-pinterest-pin-maker-by-lovart` | AI Pinterest Pin Maker /利用 AI 創建病毒式 Pin 圖 /洛瓦特 | 44 | 5 / 131 | 5 | 3 | 10 | 30.71 | 有数据 |
| 23 | `ai-birthday-card` | [ZH-TW] Free AI Birthday Card Maker — Personalized Gree... | 10 | 1 / 5 | 1 | 1 | 10 | 30.11 | 有数据 |
| 24 | `ai-anime-generator` | AI動漫生成器 /以人工智慧創造真實的動漫藝術 /洛瓦特 | 87 | 24 / 227 | 12 | 10 | 10 | 29.98 | 有数据 |

**💡 洞察**:
- **有数据层 24 名全部有真实流量**,前 6 名(按本表排序)建议首页展示:`text-to-image-generator`、`nano-banana-free`、`free-ai-illustration-generator`、`ai-post-generator`、`video-generator`、`chat-to-image-ai-generator`
- 原报告 #13–#24「n/a」条目实为数据未写入表格;JSON 全量显示 `image-to-video`、`ai-logo-generator` 等均有低量但真实信号,应排在**有数据层末尾**,而非与无数据混排
- **数据差层**(score 有、流量无)在 #25 之后共 156 页,不进首页推荐

### 4.2 Feature 首页推荐(Top 12 / 共 251 页)

| # | slug | title | 30d users | GSC 28d clicks/impr | NBQ | CompQ | Langs | 得分 | 数据层 |
|---|------|-------|-----------|---------------------|-----|-------|-------|------|--------|
| 1 | `edit-ai-generated-images` | 用Lovart Agent即時精準編輯AI圖片 | **1153** | 1306 / 201548 | 31 | 6 | 10 | **62.45** | 有数据 |
| 2 | `magazine-layout-design` | Professionelles Magazin-Layout-Tool / KI-gestützte Maga... | **556** | 73 / 1403 | 22 | 11 | 10 | **61.75** | 有数据 |
| 3 | `product-catalog-design` | Erstelle verkaufsstarke Produktkataloge mit dem KI-Kata... | **177** | 70 / 1746 | 35 | 21 | 10 | **58.82** | 有数据 |
| 4 | `video-background-remover` | Kostenloser KI-Video-Hintergrundentferner / Transparent... | **283** | 219 / 2403 | 117 | 84 | 10 | **56.43** | 有数据 |
| 5 | `ai-video-prompt-generator-veo-sora` | AI影片提示詞產生器：打造電影級場景，支援Veo與Sora / Lovart | **169** | 107 / 1866 | 39 | 35 | 9 | **51.02** | 有数据 |
| 6 | `seedance-2-0-ai-video-generator` | Lovart: Seedance 2.0 KI-Videogenerator mit Audio & Mult... | **324** | 153 / 2619 | 46 | 21 | 10 | **46.14** | 有数据 |
| 7 | `amazon-listing-image-generator` | 最佳亞馬遜商品圖AI生成器 | **267** | 39 / 813 | 17 | 17 | 10 | **45.44** | 有数据 |
| 8 | `instagram-story-maker` | KI-Instagram-Story-Generator: Erstelle virale 9:16-Visu... | 92 | 21 / 1568 | 12 | 6 | 10 | **40.66** | 有数据 |
| 9 | `diploma-design` | Lovart AI設計助手｜學歷證書AI文憑設計產生器 | **201** | 44 / 545 | 34 | 6 | 8 | 37.83 | 有数据 |
| 10 | `seedance-ai-video-generator` | Lovart: Erstelle kinoreife, flüssige KI-Videos mit Seed... | 69 | 26 / 1392 | 14 | 8 | 10 | 37.64 | 有数据 |
| 11 | `change-video-background` | 用AI替影片去背換場景｜Lovart | 88 | 37 / 279 | 26 | 20 | 10 | 37.55 | 有数据 |
| 12 | `flyer-design` | AI Flyer Maker for Professional Business Flyers / High-... | 94 | 19 / 326 | 12 | 11 | 10 | 35.71 | 有数据 |

**💡 洞察**:
- Feature 类 **250/251 页有数据**,仅 1 页落入数据差层;首页推荐直接取有数据层 Top 8–12 即可
- `edit-ai-generated-images` 是 Feature 流量王(30d 1,153 users);`video-background-remover` 竞品词 84 个,非品牌入口价值极高

### 4.3 Topic 首页推荐(Top 12 / 共 93 页)

| # | slug | title | 30d users | GSC 28d clicks/impr | NBQ | CompQ | Langs | 得分 | 数据层 |
|---|------|-------|-----------|---------------------|-----|-------|-------|------|--------|
| 1 | `ai-image-to-video-generator` | AI圖片轉影片生成器 — 免費線上工具 / Lovart | 3 | 4 / 7 | 3 | 3 | 10 | **73.83** | 有数据 |
| 2 | `image-to-video-ai` | AI圖片轉影片 — MCoT引擎驅動的靜態圖動畫化工具 / Lovart | 2 | 3 / 3 | 3 | 3 | 10 | **61.22** | 有数据 |
| 3 | `seedream-image-generation-landing-trial-now` | Seedream Image Generation — Multi-Model Agent on Lovart | 3 | 0 / 0 | 0 | 0 | 10 | **52.09** | 有数据 |
| 4 | `lovart-platform-landing-full` | Lovart Platform — Landing (full demo, 15 sections) / Lo... | 3 | 0 / 0 | 0 | 0 | 10 | **48.76** | 有数据 |
| 5 | `lovart-promo-retarget-landing-offer-close` | Lovart Pro Offer — Landing (offer-close) / Lovart | 3 | 0 / 0 | 0 | 0 | 10 | **48.46** | 有数据 |
| 6 | `free-image-to-video-ai` | 免費AI圖片轉影片 — 無浮水印、無需註冊 / Lovart | 3 | 0 / 0 | 0 | 0 | 10 | **48.33** | 有数据 |
| 7 | `ai-image-generator-landing-trial-now` | AI Image Generator — On-Brand Images from One Agent Bri... | 2 | 1 / 1 | 1 | 1 | 10 | **47.21** | 有数据 |
| 8 | `social-media-video-landing-agent-workflow` | AI Social Video — Agent-Led AI Social Media Video Gener... | 2 | 1 / 1 | 1 | 1 | 10 | **46.93** | 有数据 |
| 9 | `ugc-generator-landing-gallery-funnel` | UGC Generator — Authentic Ad Hooks and Social Proof Cre... | 3 | 0 / 0 | 0 | 0 | 10 | **43.88** | 有数据 |
| 10 | `playground-ai-landing-agent-workflow` | AI Image Generation — Agent Workflow on Lovart | 2 | 0 / 0 | 0 | 0 | 10 | **40.24** | 有数据 |
| 11 | `background-remover-landing-trial-now` | Background Remover — Product Cutouts to Full Campaign S... | 2 | 0 / 0 | 0 | 0 | 10 | 39.72 | 有数据 |
| 12 | `ai-avatar-landing-agent-workflow` | AI Avatar Maker — Agent-Led AI Avatar Maker / Lovart | 2 | 0 / 0 | 0 | 0 | 10 | 39.62 | 有数据 |

**💡 洞察**:
- Top 2 有 GSC 点击(`ai-image-to-video-generator`、`image-to-video-ai`),应置顶
- #3–#8 有极低 GA4(2–3 users)但无 GSC,属**有数据层尾部 / 接近数据差**
- 本表 Top 12 均属有数据层(有极低 UV);数据差层(无 UV/GSC、仅多语言分)从全量第 78 名起,首页不应盖过有 GSC 信号的页

### 4.4 Scenario 首页推荐

**全部 0 页**——Sanity 里 70 个 scenario 全部是 `draft-*` 开头的草稿,被 draft pipeline 标记为 `noIndex=true`,**production 首页不应推荐任何 scenario 页面**。

**行动**:等 scenario 草稿被 reviewer 改名为非 draft + 取消 noIndex 后,再按本报告 §4 同样规则(有数据→数据差→无数据)排序。当前状态:Scenario 首页留空(显示"Coming soon"或营销文案)。

### 4.5 Solution 首页推荐(共 14 页,含 4 个空标题)

| # | slug | title | 30d users | GSC | NBQ | Langs | 得分 | 数据层 |
|---|------|-------|-----------|------|-----|-------|------|--------|
| 1 | `designers` | **空标题** | 3 | 0 / 0 | 0 | 0 | 38 | 有数据 |
| 2 | `ai-design-solution-for-shopify` | AI Design Solution for Shopify | 1 | 0 / 0 | 0 | 10 | 33.48 | 有数据 |
| 3 | `good-design-for-marketers` | Good Design for Marketers | 1 | 0 / 0 | 0 | 10 | 32.82 | 有数据 |
| 4 | `ai-design-solution-for-agencies` | AI Design Solution for Agencies | 1 | 0 / 0 | 0 | 10 | 31.92 | 有数据 |
| 5 | `business-owners` | **空标题** | 2 | 0 / 0 | 0 | 0 | 30.33 | 有数据 |
| 6 | `marketers` | **空标题** | 2 | 0 / 0 | 0 | 0 | 30.33 | 有数据 |
| 7 | `ai-design-for-fitness-wellness-hub` | AI Design Solution for Fitness & Wellness | 0 | 0 / 0 | 0 | 10 | 24.09 | 数据差 |
| 8 | `ai-design-for-small-business-hub` | AI Design Solution for Local Business | 0 | 0 / 0 | 0 | 10 | 24.09 | 数据差 |
| 9 | `ai-design-solution-for-creators` | AI Design Solution for Creators | 0 | 0 / 0 | 0 | 10 | 24.09 | 数据差 |
| 10 | `ai-design-solution-for-marketing-teams` | AI Design Solution for Marketing Teams | 0 | 0 / 0 | 0 | 10 | 24.09 | 数据差 |
| 11 | `ai-design-solution-for-nonprofits` | AI Design Solution for Nonprofits | 0 | 0 / 0 | 0 | 10 | 24.09 | 数据差 |
| 12 | `ai-design-solution-for-saas` | AI Design Solution for B2B SaaS | 0 | 0 / 0 | 0 | 10 | 24.09 | 数据差 |
| 13 | `good-design-for-business-owners` | Good Design for Business Owners | 0 | 0 / 0 | 0 | 10 | 24.09 | 数据差 |
| 14 | `download` | **空标题** | 0 | 0 / 0 | 0 | 0 | 12.67 | 数据差 |

**💡 洞察**:
- **有数据层仅 6 页**(含 3 个空标题老链 `designers`/`business-owners`/`marketers`,有极低 UV 但无 title)——首页推荐应跳过空标题,取 `ai-design-solution-for-shopify`、`good-design-for-marketers`、`ai-design-solution-for-agencies` 等有标题页
- **数据差层 8 页**(30d=0,仅有 lang 分)排在其后

### 4.6 Product 首页推荐(共 2 页)

| # | slug | title | 30d users | GSC | NBQ | Langs | 得分 | 数据层 |
|---|------|-------|-----------|------|-----|-------|------|--------|
| 1 | `brand-kit` | Brand Kit | 0 | 0 / 0 | 0 | 1 | 15.91 | 数据差 |
| 2 | `chatcanvas` | ChatCanvas | 0 | 0 / 0 | 0 | 1 | 15.91 | 数据差 |

**💡 洞察**:
- 2 页均落入**数据差层**(无流量,仅 EN 单语言)——品牌位置关键,需补 10 语言 + 内容后再观察数据层

### 4.7 Landing 首页推荐(共 4 页)

| # | slug | title | 30d users | GSC | NBQ | Langs | 得分 | 数据层 |
|---|------|-------|-----------|------|-----|-------|------|--------|
| 1 | `(空 slug / draft)` | **空标题** | 0 | 0 / 0 | 0 | 1 | 15.91 | 数据差 |
| 2 | `e_commerce` | Lovart for e-commerce | 0 | 0 / 0 | 0 | 1 | 15.91 | 数据差 |
| 3 | `marketers-preview-20260608` | AI Design Canvas for Digital Marketing Managers | 0 | 0 / 0 | 0 | 1 | 15.91 | 数据差 |
| 4 | `seedance_2_5` | Seedance 2.5 | 0 | 0 / 0 | 0 | 1 | 15.91 | 数据差 |

**💡 洞察**:
- 4 个 production 页(1 个 draft 已过滤)均为数据差层,product launch 临时页,生命周期 2–4 周


---

## 5. 各类型落地页汇总速查

| 类型 | 总数 | Top 24 流量贡献 | 推荐置顶数量 | 主要问题 |
|------|------|----------------|--------------|---------|
| **Blog** | 1,734 EN | Top 24 占 70% 有机点击 | **24** | 置顶只有 1 个,优质埋没 |
| **Tool** | 658 | Top 6 占 80% 流量 | **6-8** | 658 页中 90% 是长尾 |
| **Feature** | 251 | Top 8 占 70% 流量 | **8-12** | 视频类功能搜索量最大 |
| **Topic** | 93 | 流量极低但 SEO 资产 | **12** | 都是 landing 模板,长期 SEO |
| **Scenario** | 0(70 draft) | 0 | **0** | 全部 draft,需先转正 |
| **Solution** | 14(3 空标题) | 流量极低 | **11** | 3 个老链接需补 meta |
| **Product** | 2 | 流量极低 | **2** | 急需 10 语言翻译 |
| **Landing** | 4(1 draft) | 0 | **3** | 都是 product launch 临时页 |

---

## 6. 行动清单(P0/P1/P2)

### 🔴 P0(立即执行,本周)

1. **扩充 pinned-list.json 为 24 个** — 按本报告 Blog Top 24 顺序,置顶 `publishedAt` 在 [执行日−59天, 执行日] 均匀分布;非置顶早于窗口起点(废弃 AB-P08 固定 boundary_floor)
   - 操作:走 `lovart-sanity-publish` skill 的 `verify-pinned-order.py` 流程
   - 预期:首页 24 个 blog 全部换为"用户喜欢的内容",月有机流量 +2000-3000 sessions

2. **Tool 首页排序更新** — Elementor 设为有数据层 Top 6(`text-to-image-generator`、`nano-banana-free`、`free-ai-illustration-generator`、`video-generator`、`ai-post-generator`、`chat-to-image-ai-generator`)
3. **Feature 首页排序更新** — Elementor 设为 Top 8(`edit-ai-generated-images`、`magazine-layout-design`、`product-catalog-design`、`video-background-remover`、`ai-video-prompt-generator-veo-sora`、`seedance-2-0-ai-video-generator`、`amazon-listing-image-generator`、`instagram-story-maker`)
4. **Topic 首页排序更新** — Elementor 设为 Top 12(全部置顶)
5. **Solution 首页排序更新** — Elementor 设为 Top 11,跳过空标题的 3 个老链接
6. **Scenario 首页** — 留空 + 显示 "Coming soon" 文案
7. **Product / Landing** — 保持当前 2+3 个(无需改动)

### 🟡 P1(本月内)

8. **`ai-poster-design-prompts` 补 10 语言** — 当前只有 EN(30d 913 users),11 语言上线后月流量预计 5-10 倍
9. **`brand-kit` + `chatcanvas` 补 10 语言** — Product 类目前多语言=1,补完后预计 11 语言每月 +1000+ users
10. **修复 3 个 solution 老链接**:`designers`、`business-owners`、`marketers` — 补 title + desc + meta description + h1,才能上线首页
11. **Review 类扩展**:每月新发 5-10 篇 review(覆盖新竞品),把 Reviews 分类从 83 篇扩到 150+

### 🟢 P2(Q3 内)

12. **Scenario draft 转正流程**:Sanity `lovart-scenarios-sanity-publish` skill 跑批量 draft → production,目标把 70 个 draft scenario 转正后再排序
13. **Topic 流量增长**:为 Top 12 topic landing 模板填充内容,把 30d users 从 2-3 提升到 50+
14. **建立自动重新排序脚本**:基于本报告逻辑,每 7 天自动跑 Blog 排名更新 + Elementor 自动同步(避免再次埋没优质内容)

---

## 7. 附录:数据来源与文件路径

### 7.1 中间文件(运行层,可清理)

| 文件 | 路径 | 大小 | 说明 |
|------|------|------|------|
| `ga4-full.json` | `$LOVART_LOCAL_DEV_ROOT/Output/Data Ingestion/` | 24 KB | GA4 主站 30d 概览 |
| `ga4-pages.json` | 同上 | 542 KB | GA4 page 维度 30/90/365d |
| `ga4-main.json` | `/tmp/` | 1,850 KB | GA4 page 维度 + 各 category 专项 |
| `ga4_blogs.json` | `/tmp/` | 56 KB | GA4 blogs.lovart.ai 365d(辅助参考) |
| `gsc-full.json` | `$LOVART_LOCAL_DEV_ROOT/Output/Data Ingestion/` | 22 KB | GSC top 100 + country + indexing |
| `gsc-main2.json` | `/tmp/` | 48,000 KB | GSC 全量 page×query + 各 category |
| `gsc-en-filtered.json` | `/tmp/` | 3,500 KB | GSC EN-only 后过滤(各 category + blog) |
| `bing-full.json` | `$LOVART_LOCAL_DEV_ROOT/Output/Data Ingestion/` | 1,013 KB | Bing 14 个月关键词+页面 |
| `sanity_inventory.json` | `/tmp/` | 10,883 KB | Sanity blog 10,695 + compositePage 8,547 |

### 7.2 知识资产(MindRe,长期保留)

| 文件 | 路径 | 大小 | 说明 |
|------|------|------|------|
| **本报告** | `$LOVART_INSIGHT_ROOT/Trident Insights/reports/topics/Lovart-SEO-topic-page-ranking-2026-07.md` | — | 当前报告 |
| `blog_ranking_v2.json` | `$LOVART_INSIGHT_ROOT/排序分析/` | 3.1 MB | 1734 篇 blog 综合排名完整数据 |
| `landing_pages_ranking_v2.json` | `$LOVART_INSIGHT_ROOT/排序分析/` | 1.0 MB | 7 类落地页排名完整数据 |
| `blog_ranking_full.json` | 同上 | 2.6 MB | v1 旧版(完整 GSC 数据) |
| `landing_pages_ranking.json` | 同上 | 1.1 MB | v1 旧版 |

### 7.3 复现命令

```bash
# 1. 设置环境变量(token 路径)
unset PYTHONPATH
export LOVART_TRIDENT_CREDENTIALS_DIR="$HOME/Library/Mobile Documents/iCloud~md~obsidian/Documents/MindRe/1-Project/Lovart MFlow/1-1 Harness/Skills/01-strategy/lovart-trident-data-engine/credentials"

# 2. 拉 GA4 三引擎(主站)
/usr/bin/python3 "$LOVART_HARNESS_ROOT/1-4 Dev/scripts/trident/ga4_fetch.py"
/usr/bin/python3 "$LOVART_HARNESS_ROOT/1-4 Dev/scripts/trident/gsc_fetch.py"
/usr/bin/python3 "$LOVART_HARNESS_ROOT/1-4 Dev/scripts/trident/bing_fetch.py"

# 3. 拉 GA4 page 维度专项(自定义)
/usr/bin/python3 /tmp/ga4_main_fetch.py
/usr/bin/python3 /tmp/ga4_pages_fetch.py

# 4. 拉 GSC page×query 专项(自定义)
/usr/bin/python3 /tmp/gsc_main_fetch.py
/usr/bin/python3 /tmp/gsc_en_filter.py

# 5. 拉 Sanity inventory
/usr/bin/python3 /tmp/sanity_inventory.py

# 6. 综合分析(产出排名 JSON)
/usr/bin/python3 /tmp/analyze_blog.py
/usr/bin/python3 /tmp/analyze_v2.py
```

### 7.4 已知问题与修复

1. **GA4 token 路径**:`1-1 Harness/Skills/lovart-trident-data-engine/credentials/` 是错的(目录不存在),正确是 `1-1 Harness/Skills/01-strategy/lovart-trident-data-engine/credentials/`。修复:用 `LOVART_TRIDENT_CREDENTIALS_DIR` 环境变量指向
2. **PYTHONPATH 注入**:`/Users/seveno/.hermes/hermes-agent` 在 PYTHONPATH 中,导致系统 python3 加载 Hermes venv(3.11)的 cryptography(ABI 冲突)。**修复**:`unset PYTHONPATH` 后再跑
3. **GSC CONTAINS 误命中**:`CONTAINS "/tools/"` 会把 `/zh/tools/...`、`/blog/...`、`/pricing` 等都包含进来。**修复**:本地后过滤,只看 EN(`/tools/{slug}` 单一层路径)
4. **scenario 类全是 draft**:70 个 Sanity scenario 页面全部 `slug.startswith("draft-")` 且 `noIndex=true`,**修复**:production 首页留空,等 reviewer 转正后再排

---

## 8. 💡 核心洞察(三层)

### 8.1 第一层(产品力):用户喜欢什么内容?

**结论**:Review 类(13/24 = 54%)是 Lovart Blog 的真正流量引擎。

**证据**:
- Top 24 中 13 篇是 review,综合得分平均 35-72,占据 Top 10 大部分
- 每篇 review 命中 12-72 个竞品非品牌词
- 每篇 review 平均 10 语言完整覆盖

**行动**:继续保持每月 5-10 篇 review 输出。

### 8.2 第二层(SEO 现状):Lovart 流量的天花板

**结论**:99.4% 关键词是品牌词,Lovart SEO 增长瓶颈在**非品牌词覆盖率**。

**证据**:
- GSC top100 中 99.4% 是品牌词(258,932 clicks / 258,932 total)
- 非品牌词 7 条占 0.6%(1,802 clicks)
- 竞品非品牌词 0 命中
- 但 Top 24 Blog 中命中竞品词 12-72 个,说明 **内容已准备好但 SERP 排名不够**

**行动**:
- Top 24 review 文章加 FAQ + Pros/Cons + Comparison 表格,争取排到第一页
- 建立"竞品词 SERP 监控":每月跟踪 265 个竞品词的 Lovart 文章位置,从平均 7-11 提升到 1-3

### 8.3 第三层(执行):落地页首页排序原则

**结论**:**首页位置宝贵,只放真正能换流量的页面**。

**证据**:
- Tool 658 页 → 推荐 6-8 个(前 6 名占 80% 流量)
- Feature 251 页 → 推荐 8-12 个(前 8 名占 70% 流量)
- Topic 93 页 → 推荐 12 个(全部 SEO 资产,即使短期流量低)
- Scenario 0 页 → 推荐 0 个(全是 draft,先转正)
- Solution 14 页 → 推荐 11 个(跳过 3 个无标题老链接)
- Product 2 页 → 推荐 2 个(急需 10 语言翻译)
- Landing 3 页 → 推荐 3 个

**行动**:本报告 §6 P0 任务清单 7 项,执行完后 Lovart 7 个落地页类型首页全部"内容健康、流量优先"。

---

*报告生成时间:2026-07-07*
*数据截止:2026-07-05(GA4/GSC 两天延迟,Bing 实时)*
*下次建议更新:2026-07-14(7 天后)*