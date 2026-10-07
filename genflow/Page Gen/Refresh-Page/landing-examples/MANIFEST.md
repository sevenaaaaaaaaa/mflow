# Landing Page 参考案例

> 通用 7 篇：`node scripts/generate-landing-examples.js`  
> **非品牌词 41 篇**：`node scripts/generate-keyword-landing-examples.js`（默认 `--batch=all`）  
> Batch：`--batch=google`（13）｜`--batch=bing`（16）｜`--batch=model`（12）

---

## 一、通用故事线参考（7 篇）

| # | 故事线 | 主题 | 文件 | Sections |
|---|--------|------|------|----------|
| 1 | `landing-gallery-detail` | Shopify 增长 | `en/draft-lovart-shopify-growth-landing-gallery-detail-en.json` | 12 |
| 2 | `landing-gallery-funnel` | Creative Studio | `en/draft-lovart-creative-studio-landing-gallery-funnel-en.json` | 12 |
| 3 | `landing-brand-trust` | Brand Campaign | `en/draft-lovart-brand-campaign-landing-brand-trust-en.json` | 12 |
| 4 | `landing-trial-now` | Tool Trial | `en/draft-lovart-tool-trial-landing-trial-now-en.json` | 12 |
| 5 | `landing-vs-competitor` | Competitor Alt | `en/draft-lovart-competitor-alt-landing-vs-competitor-en.json` | 12 |
| 6 | `landing-offer-close` | Promo Retarget | `en/draft-lovart-promo-retarget-landing-offer-close-en.json` | 12 |
| 7 | `landing-full` | Platform Demo | `en/draft-lovart-platform-landing-full-en.json` | **15** |

---

## 二、非品牌核心词案例（13 篇 · 5月 SEO 报告驱动）

> **词源**：[Lovart-SEO-2026-05.md §8.5](../../../insight-data/Trident Insights/reports/monthly/Lovart-SEO-2026-05.md) — GSC 5,000 词中 **Google 完全无排名** 的 13 个核心非品牌词  
> **报告 P0 行动**：「针对 13 个缺失核心词建 landing page」  
> **不是**竞品品牌对比页（Canva alternative 等走 `landing-vs-competitor`，另批）

### 13 词 × 故事线映射

| # | 核心词 | 故事线 | 选线依据（5月报告语境） | 文件 |
|---|--------|--------|------------------------|------|
| 1 | AI Ad Generator | `landing-gallery-funnel` | 广告变体 + 漏斗场景 | `en/keywords/draft-ai-ad-generator-landing-gallery-funnel-en.json` |
| 2 | AI Commercial | `landing-gallery-funnel` | 商业/促销视频，全漏斗 | `en/keywords/draft-ai-commercial-landing-gallery-funnel-en.json` |
| 3 | AI Design Generator | `landing-brand-trust` | Agent 定位，品牌信任 | `en/keywords/draft-ai-design-generator-landing-brand-trust-en.json` |
| 4 | AI Logo Generator | `landing-trial-now` | 工具 Search，prompt 试用 | `en/keywords/draft-ai-logo-generator-landing-trial-now-en.json` |
| 5 | Brand Video | `landing-brand-trust` | 上漏斗品牌视频 | `en/keywords/draft-brand-video-landing-brand-trust-en.json` |
| 6 | Character Consistency | `landing-gallery-detail` | 差异化功能，深讲 | `en/keywords/draft-character-consistency-landing-gallery-detail-en.json` |
| 7 | DALL-E | `landing-trial-now` | 模型名搜索，即时试用 | `en/keywords/draft-dall-e-image-generation-landing-trial-now-en.json` |
| 8 | Marketing Video AI | `landing-gallery-funnel` | 营销视频漏斗 | `en/keywords/draft-marketing-video-ai-landing-gallery-funnel-en.json` |
| 9 | Product Video | `landing-gallery-detail` | 电商 SKU 场景 | `en/keywords/draft-product-video-landing-gallery-detail-en.json` |
| 10 | Social Media Video | `landing-gallery-funnel` | 社交视频规模化 | `en/keywords/draft-social-media-video-landing-gallery-funnel-en.json` |
| 11 | Talking Avatar | `landing-trial-now` | 工具型，prompt 试用 | `en/keywords/draft-talking-avatar-landing-trial-now-en.json` |
| 12 | UGC Generator | `landing-gallery-funnel` | 投放 UGC 变体循环 | `en/keywords/draft-ugc-generator-landing-gallery-funnel-en.json` |
| 13 | Workflow Automation | `landing-brand-trust` | 企业创意自动化 | `en/keywords/draft-workflow-automation-landing-brand-trust-en.json` |

### 选词 → 故事线路由逻辑

| 词类 / 意图 | 典型词 | 推荐故事线 |
|-------------|--------|------------|
| 工具型 Search（try / generate / free） | AI Logo Generator, DALL-E, Talking Avatar | `landing-trial-now` |
| 功能 hub / 多能力认知 | Character Consistency, Product Video | `landing-gallery-detail` |
| 营销 / 漏斗场景 | AI Ad Generator, Marketing Video AI, UGC | `landing-gallery-funnel` |
| Agent / 品牌信任 | AI Design Generator, Brand Video, Workflow Automation | `landing-brand-trust` |

- 全部 `seo.noIndex: true`，slug 前缀 `draft-`
- **尚未入库 Sanity / 未上线**
- Batch 2（Bing + Tools）见 **§三**

---

## 三、Batch 2 — Bing 差集 + Tools 配对（16 篇）

> **词源**：`Lovart-SEO-2026-05 §8.11`（Bing 34 核心词零排名，相对 Batch1 增量）+ `§9`（Tools 高流量页互导）  
> **双引擎策略**：报告 §4.16 / §8.6 — Google Core 63.9% vs Bing Core 5.6%，同一 landing 结构共用

| # | 核心词 | 故事线 | Tools 配对 | 文件 |
|---|--------|--------|------------|------|
| 1 | AI Image Generator | trial-now | `/tools/text-to-image-generator` | `draft-ai-image-generator-landing-trial-now-en.json` |
| 2 | AI Video Generator | trial-now | `/tools/video-generator` | `draft-ai-video-generator-landing-trial-now-en.json` |
| 3 | AI Photo Generator | trial-now | — | `draft-ai-photo-generator-landing-trial-now-en.json` |
| 4 | Background Remover | trial-now | — | `draft-background-remover-landing-trial-now-en.json` |
| 5 | Image to Video | gallery-detail | — | `draft-image-to-video-landing-gallery-detail-en.json` |
| 6 | Text to Video | gallery-detail | `/tools/text-to-image-generator` | `draft-text-to-video-landing-gallery-detail-en.json` |
| 7 | AI Avatar | trial-now | — | `draft-ai-avatar-landing-trial-now-en.json` |
| 8 | AI Poster | gallery-detail | — | `draft-ai-poster-landing-gallery-detail-en.json` |
| 9 | AI Banner | gallery-funnel | — | `draft-ai-banner-landing-gallery-funnel-en.json` |
| 10 | AI Shorts | gallery-funnel | — | `draft-ai-shorts-landing-gallery-funnel-en.json` |
| 11 | Lip Sync | trial-now | `/tools/ai-lip-sync-generator` | `draft-lip-sync-landing-trial-now-en.json` |
| 12 | Cinematic Video | brand-trust | — | `draft-cinematic-video-landing-brand-trust-en.json` |
| 13 | Graphic Design | brand-trust | — | `draft-graphic-design-landing-brand-trust-en.json` |
| 14 | FLUX | trial-now | — | `draft-flux-image-generation-landing-trial-now-en.json` |
| 15 | Kling | trial-now | `/tools/veo3.1` | `draft-kling-video-generation-landing-trial-now-en.json` |
| 16 | Veo 3 | trial-now | `/tools/veo3.1` | `draft-veo-3-video-generation-landing-trial-now-en.json` |

### 汇总

| Batch | 来源 | 篇数 | 命令 |
|-------|------|------|------|
| google-13 | §8.5 Google 零排名核心词 | 13 | `--batch=google` |
| bing-delta | §8.11 + §9 Tools 配对 | 16 | `--batch=bing` |
| model-ctr | §4.5 + §8.3/8.4 模型与高曝光词 | 12 | `--batch=model` |
| **合计** | | **41** | 默认 `--batch=all` |

---

## 四、Batch 3 — 模型流量 + 高曝光低 CTR（12 篇）

> **词源**：`§8.3/8.4` GSC 模型命中 + `§4.5` 高曝光低 CTR  
> **原则**：捕获搜索意图，**不是** Canva/Freepik alternative 对比页

| # | 核心词 | 故事线 | 5月信号 | 配对 |
|---|--------|--------|---------|------|
| 1 | Sora | trial-now | sora2 66 点击 | `features/ai-video-prompt-generator-veo-sora` |
| 2 | Seedance | trial-now | seedance 2.0 free 113 点击 | `features/seedance-2-0-ai-video-generator` |
| 3 | Seedream | trial-now | seedream 4.5 free 34 点击 | — |
| 4 | Midjourney | trial-now | 模型名搜索 | — |
| 5 | Motion Control | gallery-detail | 核心词 P2 | — |
| 6 | Text to Image | trial-now | 核心 P0 | `tools/text-to-image-generator` |
| 7 | Image to Image | gallery-detail | CTR 8.6% | — |
| 8 | Freepik AI Image Generator | gallery-detail | **65K 曝光 / 0.1% CTR** | — |
| 9 | Canva AI Image Generator | trial-now | Bing 部分命中 | — |
| 10 | Hailuo AI Video Generator | trial-now | GSC 15 点击 | — |
| 11 | AI Design Agent | brand-trust | Agent 类 | — |
| 12 | AI Illustration Generator | trial-now | GSC 28 点击 | `tools/free-ai-illustration-generator` |

### 下一批候选（未生成）

| 信号 | 建议 |
|------|------|
| §11 大区 Top15 非品牌词 | ja / zh-TW / pt 本地化 landing |
| nano-banana / veo 3.1 free | 已有 Tools 流量，补 agent 扩展 landing |

---

## Type 顺序速查

- **gallery-detail**: `hero-gallery → … → feature-detail → faq → cta-default`
- **gallery-funnel**: `hero-gallery → … → showcase-horizontal → faq → cta-default`
- **brand-trust**: `hero-cinematic → … → logo-loop → testimonial → … → feature-detail`
- **trial-now**: `hero-split → bento-4 → … → prompt-launcher → bento-2 → …`

完整序列见 `landing-storylines.json`。
