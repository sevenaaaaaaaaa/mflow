# Page Drafts Index

> 日期：2026-06-08  
> 范围：`1-3 Content Gen/Page Gen/Pages/drafts/`  
> 原则：只读索引；未移动、未删除、未导入 Sanity、未修改 draft JSON。

---

## 一、管理结论

`Pages/drafts/` 不是单一发布队列，而是多个来源混放的候选池与参考池：

- 全量文件：2643 个。
- JSON 页面资产：2631 个。
- 支持文档 / manifest / ndjson / 压缩包：12 个。
- 最大桶是 `_pull`（已迁移到 `~/Documents/Lovart Local Dev/Output/Page Gen/_pull/`），共 2530 个文件，管理状态应是 `pulled-reference`，不能直接提升发布。
- 可进入后续人工挑选或 preflight 的候选池约 105 个，但仍需逐个确认 slug、noIndex、目标类型与线上冲突。

这批资产的正确处理方式是“分型 + 挑选 + preflight + 用户确认导入”，而不是批量改名、批量搬运或批量发布。

---

## 二、按来源桶统计

| bucket | count |
| --- | --- |
| _pull | 2530 |
| scenarios-storyline | 72 |
| composite-v2 | 18 |
| features-storyline | 10 |
| ai-video-agent-expansion | 9 |
| landing-storyline | 4 |

---

## 三、按目标类型统计

| target_type | count |
| --- | --- |
| feature | 2548 |
| scenario | 70 |
| supporting-file | 16 |
| tool | 6 |
| topic | 2 |
| landing | 1 |

---

## 四、按管理状态统计

| management_status | count |
| --- | --- |
| pulled-reference | 2530 |
| local-only-draft | 80 |
| synced-noindex-experiment | 15 |
| expansion-candidate | 8 |
| supporting-doc | 7 |
| storyline-candidate | 2 |
| draft-candidate | 1 |

---

## 五、seo.noIndex 分布

| seo_noindex | count |
| --- | --- |
| false | 2076 |
| true | 402 |
| (blank) | 156 |
| undefined | 9 |

---

## 六、候选样本

这些文件可以作为后续人工挑选和 preflight 的入口，但不代表已经 Ready。

| bucket | type | lang | slug | draft status | noIndex | status |
| --- | --- | --- | --- | --- | --- | --- |
| ai-video-agent-expansion | feature |  | ai-video-agent |  | true | expansion-candidate |
| ai-video-agent-expansion | feature |  | ai-video-agent-for-ecommerce |  | true | expansion-candidate |
| ai-video-agent-expansion | feature |  | ai-video-agent-for-marketing |  | true | expansion-candidate |
| ai-video-agent-expansion | feature |  | ai-video-agent-for-tiktok |  | true | expansion-candidate |
| ai-video-agent-expansion | feature |  | ai-video-agent-for-youtube |  | true | expansion-candidate |
| ai-video-agent-expansion | feature |  | ai-video-agent-workflow |  | true | expansion-candidate |
| ai-video-agent-expansion | feature |  | autonomous-ai-video-agent |  | true | expansion-candidate |
| ai-video-agent-expansion | feature |  | multimodal-ai-video-agent |  | true | expansion-candidate |
| composite-v2 | feature | en | draft-ai-logo-maker-f1 | local-only | true | synced-noindex-experiment |
| composite-v2 | feature | en | draft-ai-logo-maker-f2 | local-only | true | synced-noindex-experiment |
| composite-v2 | feature | en | draft-ai-logo-maker-f4 | local-only | true | synced-noindex-experiment |
| composite-v2 | feature | en | draft-ai-logo-maker-f5 | local-only | true | synced-noindex-experiment |
| composite-v2 | feature | en | draft-ai-logo-maker-f6 | local-only | true | synced-noindex-experiment |
| composite-v2 | feature | en | draft-ai-sales-deck-ppt-generator-f1 | local-only | true | synced-noindex-experiment |
| composite-v2 | feature | en | draft-ai-sales-deck-ppt-generator-f2 | local-only | true | synced-noindex-experiment |
| composite-v2 | feature | en | draft-ai-sales-deck-ppt-generator-f7 | local-only | true | synced-noindex-experiment |
| composite-v2 | feature | en | draft-ai-sales-deck-ppt-generator-s1 | local-only | true | synced-noindex-experiment |
| composite-v2 | tool | en | draft-ai-logo-maker-t1 | local-only | true | synced-noindex-experiment |
| composite-v2 | tool | en | draft-ai-logo-maker-t2 | local-only | true | synced-noindex-experiment |
| composite-v2 | tool | en | draft-ai-logo-maker-t4 | local-only | true | synced-noindex-experiment |
| composite-v2 | tool | en | draft-ai-sales-deck-ppt-generator-n5 | local-only | true | synced-noindex-experiment |
| composite-v2 | tool | en | draft-ai-sales-deck-ppt-generator-t1 | local-only | true | synced-noindex-experiment |
| composite-v2 | tool | en | draft-ai-sales-deck-ppt-generator-t2 | local-only | true | synced-noindex-experiment |
| features-storyline | feature | en | draft-ai-logo-maker-features-grid-bento6 | local-only | true | local-only-draft |
| features-storyline | feature | en | draft-ai-logo-maker-features-grid-feature | local-only | true | local-only-draft |
| features-storyline | feature | en | draft-ai-logo-maker-features-main | local-only | true | local-only-draft |
| features-storyline | feature | en | draft-ai-logo-maker-features-tab-b | local-only | true | local-only-draft |
| features-storyline | feature | en | draft-ai-sales-deck-ppt-generator-features-grid-bento6 | local-only | true | local-only-draft |
| features-storyline | feature | en | draft-ai-sales-deck-ppt-generator-features-grid-feature | local-only | true | local-only-draft |
| features-storyline | feature | en | draft-ai-sales-deck-ppt-generator-features-main | local-only | true | local-only-draft |
| features-storyline | feature | en | draft-ai-sales-deck-ppt-generator-features-tab-b | local-only | true | local-only-draft |
| features-storyline | supporting-file |  |  |  |  | storyline-candidate |
| landing-storyline | topic | en | draft-lovart-creative-studio-landing-B | local-only | true | local-only-draft |
| landing-storyline | topic | en | draft-lovart-shopify-growth-landing-A | local-only | true | local-only-draft |
| landing-storyline | landing |  |  |  |  | storyline-candidate |
| scenarios-storyline | scenario | en | draft-brand-manager-scenarios-a | local-only | true | local-only-draft |
| scenarios-storyline | scenario | en | draft-brand-manager-scenarios-b | local-only | true | local-only-draft |
| scenarios-storyline | scenario | en | draft-brand-manager-scenarios-before-after | local-only | true | local-only-draft |
| scenarios-storyline | scenario | en | draft-brand-manager-scenarios-bento2 | local-only | true | local-only-draft |
| scenarios-storyline | scenario | en | draft-brand-manager-scenarios-bento6 | local-only | true | local-only-draft |
| scenarios-storyline | scenario | en | draft-brand-manager-scenarios-blog | local-only | true | local-only-draft |
| scenarios-storyline | scenario | en | draft-brand-manager-scenarios-cinematic | local-only | true | local-only-draft |
| scenarios-storyline | scenario | en | draft-brand-manager-scenarios-journey | local-only | true | local-only-draft |
| scenarios-storyline | scenario | en | draft-brand-manager-scenarios-portrait | local-only | true | local-only-draft |
| scenarios-storyline | scenario | en | draft-brand-manager-scenarios-reviews4 | local-only | true | local-only-draft |
| scenarios-storyline | scenario | en | draft-brand-manager-scenarios-showcase | local-only | true | local-only-draft |
| scenarios-storyline | scenario | en | draft-brand-manager-scenarios-stacked | local-only | true | local-only-draft |
| scenarios-storyline | scenario | en | draft-brand-manager-scenarios-testimonial | local-only | true | local-only-draft |
| scenarios-storyline | scenario | en | draft-brand-manager-scenarios-vertical | local-only | true | local-only-draft |
| scenarios-storyline | scenario | en | draft-ecommerce-operator-scenarios-a | local-only | true | local-only-draft |
| scenarios-storyline | scenario | en | draft-ecommerce-operator-scenarios-b | local-only | true | local-only-draft |
| scenarios-storyline | scenario | en | draft-ecommerce-operator-scenarios-before-after | local-only | true | local-only-draft |
| scenarios-storyline | scenario | en | draft-ecommerce-operator-scenarios-bento2 | local-only | true | local-only-draft |
| scenarios-storyline | scenario | en | draft-ecommerce-operator-scenarios-bento6 | local-only | true | local-only-draft |
| scenarios-storyline | scenario | en | draft-ecommerce-operator-scenarios-blog | local-only | true | local-only-draft |
| scenarios-storyline | scenario | en | draft-ecommerce-operator-scenarios-cinematic | local-only | true | local-only-draft |
| scenarios-storyline | scenario | en | draft-ecommerce-operator-scenarios-journey | local-only | true | local-only-draft |
| scenarios-storyline | scenario | en | draft-ecommerce-operator-scenarios-portrait | local-only | true | local-only-draft |
| scenarios-storyline | scenario | en | draft-ecommerce-operator-scenarios-reviews4 | local-only | true | local-only-draft |
| scenarios-storyline | scenario | en | draft-ecommerce-operator-scenarios-showcase | local-only | true | local-only-draft |

---

## 七、需要注意的样本

这些不是要删除，而是后续处理时必须先判断用途。

| bucket | type | filename | status | notes |
| --- | --- | --- | --- | --- |
| _pull | supporting-file | _manifest.json | pulled-reference | do-not-promote-directly; missing-title; missing-bodyJson |
| _pull | feature | ai-ad-thumbnail-generator-en.json | pulled-reference | do-not-promote-directly; slug-without-draft-prefix; seo-noIndex-not-true |
| _pull | feature | ai-affiliate-ads-generator-en.json | pulled-reference | do-not-promote-directly; slug-without-draft-prefix; seo-noIndex-not-true |
| _pull | feature | ai-avatar-streaming-seedance-en.json | pulled-reference | do-not-promote-directly; slug-without-draft-prefix; seo-noIndex-not-true |
| _pull | feature | ai-background-swap-no-masking-en.json | pulled-reference | do-not-promote-directly; slug-without-draft-prefix; seo-noIndex-not-true |
| _pull | feature | ai-bakery-menu-maker-en.json | pulled-reference | do-not-promote-directly; slug-without-draft-prefix; seo-noIndex-not-true |
| _pull | feature | ai-brochure-design-tool-en.json | pulled-reference | do-not-promote-directly; slug-without-draft-prefix; seo-noIndex-not-true |
| _pull | feature | ai-business-card-maker-en.json | pulled-reference | do-not-promote-directly; slug-without-draft-prefix; seo-noIndex-not-true |
| _pull | feature | ai-carousel-generator-en.json | pulled-reference | do-not-promote-directly; slug-without-draft-prefix; seo-noIndex-not-true |
| _pull | feature | ai-commercials-seedance-en.json | pulled-reference | do-not-promote-directly; slug-without-draft-prefix; seo-noIndex-not-true |
| _pull | feature | ai-company-logo-maker-en.json | pulled-reference | do-not-promote-directly; slug-without-draft-prefix; seo-noIndex-not-true |
| _pull | feature | ai-coupon-ad-generator-en.json | pulled-reference | do-not-promote-directly; slug-without-draft-prefix; seo-noIndex-not-true |
| _pull | feature | ai-design-agent-en.json | pulled-reference | do-not-promote-directly; slug-without-draft-prefix; seo-noIndex-not-true |
| _pull | feature | ai-design-agent-for-freelancers-en.json | pulled-reference | do-not-promote-directly; slug-without-draft-prefix; seo-noIndex-not-true |
| _pull | feature | ai-design-marketing-agency-en.json | pulled-reference | do-not-promote-directly; slug-without-draft-prefix; seo-noIndex-not-true |
| _pull | feature | ai-facebook-ad-creative-generator-en.json | pulled-reference | do-not-promote-directly; slug-without-draft-prefix; seo-noIndex-not-true |
| _pull | feature | ai-facebook-post-designer-en.json | pulled-reference | do-not-promote-directly; slug-without-draft-prefix; seo-noIndex-not-true |
| _pull | feature | ai-facebook-poster-generator-en.json | pulled-reference | do-not-promote-directly; slug-without-draft-prefix; seo-noIndex-not-true |
| _pull | feature | ai-giveaway-poster-generator-en.json | pulled-reference | do-not-promote-directly; slug-without-draft-prefix; seo-noIndex-not-true |
| _pull | feature | ai-google-ads-banner-generator-en.json | pulled-reference | do-not-promote-directly; slug-without-draft-prefix; seo-noIndex-not-true |
| _pull | feature | ai-illustration-generator-vector-nano-banana-en.json | pulled-reference | do-not-promote-directly; slug-without-draft-prefix; seo-noIndex-not-true |
| _pull | feature | ai-image-generator-en.json | pulled-reference | do-not-promote-directly; slug-without-draft-prefix; seo-noIndex-not-true |
| _pull | feature | ai-image-generator-text-to-image-en.json | pulled-reference | do-not-promote-directly; slug-without-draft-prefix; seo-noIndex-not-true |
| _pull | feature | ai-instagram-feed-planner-en.json | pulled-reference | do-not-promote-directly; slug-without-draft-prefix; seo-noIndex-not-true |
| _pull | feature | ai-instagram-post-generator-en.json | pulled-reference | do-not-promote-directly; slug-without-draft-prefix; seo-noIndex-not-true |
| _pull | feature | ai-instagram-post-maker-en.json | pulled-reference | do-not-promote-directly; slug-without-draft-prefix; seo-noIndex-not-true |
| _pull | feature | ai-instagram-story-layout-generator-en.json | pulled-reference | do-not-promote-directly; slug-without-draft-prefix; seo-noIndex-not-true |
| _pull | feature | ai-linkedin-infographic-generator-b2b-en.json | pulled-reference | do-not-promote-directly; slug-without-draft-prefix; seo-noIndex-not-true |
| _pull | feature | ai-logo-maker-brand-agent-en.json | pulled-reference | do-not-promote-directly; slug-without-draft-prefix; seo-noIndex-not-true |
| _pull | feature | ai-meta-ads-generator-en.json | pulled-reference | do-not-promote-directly; slug-without-draft-prefix; seo-noIndex-not-true |
| _pull | feature | ai-mockup-generator-en.json | pulled-reference | do-not-promote-directly; slug-without-draft-prefix; seo-noIndex-not-true |
| _pull | feature | ai-paid-social-ad-generator-en.json | pulled-reference | do-not-promote-directly; slug-without-draft-prefix; seo-noIndex-not-true |
| _pull | feature | ai-picture-generator-en.json | pulled-reference | do-not-promote-directly; slug-without-draft-prefix; seo-noIndex-not-true |
| _pull | feature | ai-pinterest-pin-maker-en.json | pulled-reference | do-not-promote-directly; slug-without-draft-prefix; seo-noIndex-not-true |
| _pull | feature | ai-poster-design-agent-nano-banana-en.json | pulled-reference | do-not-promote-directly; slug-without-draft-prefix; seo-noIndex-not-true |
| _pull | feature | ai-poster-generator-illustration-optimization-en.json | pulled-reference | do-not-promote-directly; slug-without-draft-prefix; seo-noIndex-not-true |
| _pull | feature | ai-presentation-slides-generator-en.json | pulled-reference | do-not-promote-directly; slug-without-draft-prefix; seo-noIndex-not-true |
| _pull | feature | ai-product-catalog-maker-en.json | pulled-reference | do-not-promote-directly; slug-without-draft-prefix; seo-noIndex-not-true |
| _pull | feature | ai-product-display-generator-en.json | pulled-reference | do-not-promote-directly; slug-without-draft-prefix; seo-noIndex-not-true |
| _pull | feature | ai-product-image-generator-en.json | pulled-reference | do-not-promote-directly; slug-without-draft-prefix; seo-noIndex-not-true |
| _pull | feature | ai-product-video-seedance-en.json | pulled-reference | do-not-promote-directly; slug-without-draft-prefix; seo-noIndex-not-true |
| _pull | feature | ai-promotion-landing-page-generator-en.json | pulled-reference | do-not-promote-directly; slug-without-draft-prefix; seo-noIndex-not-true |
| _pull | feature | ai-retargeting-ad-generator-en.json | pulled-reference | do-not-promote-directly; slug-without-draft-prefix; seo-noIndex-not-true |
| _pull | feature | ai-short-video-generator-en.json | pulled-reference | do-not-promote-directly; slug-without-draft-prefix; seo-noIndex-not-true |
| _pull | feature | ai-social-media-content-generator-en.json | pulled-reference | do-not-promote-directly; slug-without-draft-prefix; seo-noIndex-not-true |
| _pull | feature | ai-social-media-post-maker-en.json | pulled-reference | do-not-promote-directly; slug-without-draft-prefix; seo-noIndex-not-true |
| _pull | feature | ai-subscribe-ad-generator-en.json | pulled-reference | do-not-promote-directly; slug-without-draft-prefix; seo-noIndex-not-true |
| _pull | feature | ai-subscription-fatigue-utility-en.json | pulled-reference | do-not-promote-directly; slug-without-draft-prefix; seo-noIndex-not-true |
| _pull | feature | ai-text-to-image-generator-en.json | pulled-reference | do-not-promote-directly; slug-without-draft-prefix; seo-noIndex-not-true |
| _pull | feature | ai-tiktok-thumbnail-maker-en.json | pulled-reference | do-not-promote-directly; slug-without-draft-prefix; seo-noIndex-not-true |
| _pull | feature | ai-twitch-overlay-generator-en.json | pulled-reference | do-not-promote-directly; slug-without-draft-prefix; seo-noIndex-not-true |
| _pull | feature | ai-twitter-header-creator-en.json | pulled-reference | do-not-promote-directly; slug-without-draft-prefix; seo-noIndex-not-true |
| _pull | feature | ai-twitter-x-post-generator-en.json | pulled-reference | do-not-promote-directly; slug-without-draft-prefix; seo-noIndex-not-true |
| _pull | feature | ai-video-background-remover-en.json | pulled-reference | do-not-promote-directly; slug-without-draft-prefix; seo-noIndex-not-true |
| _pull | feature | ai-video-enhancer-remaster-veo3-en.json | pulled-reference | do-not-promote-directly; slug-without-draft-prefix; seo-noIndex-not-true |
| _pull | feature | ai-video-generator-en.json | pulled-reference | do-not-promote-directly; slug-without-draft-prefix; seo-noIndex-not-true |
| _pull | feature | ai-video-generator-no-templates-en.json | pulled-reference | do-not-promote-directly; slug-without-draft-prefix; seo-noIndex-not-true |
| _pull | feature | ai-video-generator-text-to-video-en.json | pulled-reference | do-not-promote-directly; slug-without-draft-prefix; seo-noIndex-not-true |
| _pull | feature | ai-video-generator-tools-en.json | pulled-reference | do-not-promote-directly; slug-without-draft-prefix; seo-noIndex-not-true |
| _pull | feature | ai-video-generator-workflow-by-lovart-en.json | pulled-reference | do-not-promote-directly; slug-without-draft-prefix; seo-noIndex-not-true |
| _pull | feature | ai-video-generator-workflow-en.json | pulled-reference | do-not-promote-directly; slug-without-draft-prefix; seo-noIndex-not-true |
| _pull | feature | ai-video-optimization-en.json | pulled-reference | do-not-promote-directly; slug-without-draft-prefix; seo-noIndex-not-true |
| _pull | feature | ai-video-prompt-generator-veo-sora-en.json | pulled-reference | do-not-promote-directly; slug-without-draft-prefix; seo-noIndex-not-true |
| _pull | feature | ai-webtoon-comic-generator-seedance-en.json | pulled-reference | do-not-promote-directly; slug-without-draft-prefix; seo-noIndex-not-true |
| _pull | feature | ai-youtube-banner-maker-en.json | pulled-reference | do-not-promote-directly; slug-without-draft-prefix; seo-noIndex-not-true |
| _pull | feature | ai-youtube-thumbnail-generator-en.json | pulled-reference | do-not-promote-directly; slug-without-draft-prefix; seo-noIndex-not-true |
| _pull | feature | album-cover-design-en.json | pulled-reference | do-not-promote-directly; slug-without-draft-prefix; seo-noIndex-not-true |
| _pull | feature | all-in-one-ai-models-en.json | pulled-reference | do-not-promote-directly; slug-without-draft-prefix; seo-noIndex-not-true |
| _pull | feature | all-in-one-ai-video-generator-en.json | pulled-reference | do-not-promote-directly; slug-without-draft-prefix; seo-noIndex-not-true |
| _pull | feature | amazon-listing-design-optimization-en.json | pulled-reference | do-not-promote-directly; slug-without-draft-prefix; seo-noIndex-not-true |
| _pull | feature | amazon-listing-image-generator-en.json | pulled-reference | do-not-promote-directly; slug-without-draft-prefix; seo-noIndex-not-true |
| _pull | feature | anniversary-card-design-en.json | pulled-reference | do-not-promote-directly; slug-without-draft-prefix; seo-noIndex-not-true |
| _pull | feature | baby-shower-invitation-design-en.json | pulled-reference | do-not-promote-directly; slug-without-draft-prefix; seo-noIndex-not-true |
| _pull | feature | bakery-menu-design-en.json | pulled-reference | do-not-promote-directly; slug-without-draft-prefix; seo-noIndex-not-true |
| _pull | feature | banner-design-en.json | pulled-reference | do-not-promote-directly; slug-without-draft-prefix; seo-noIndex-not-true |
| _pull | feature | bar-menu-design-en.json | pulled-reference | do-not-promote-directly; slug-without-draft-prefix; seo-noIndex-not-true |
| _pull | feature | best-ai-image-generator-2026-en.json | pulled-reference | do-not-promote-directly; slug-without-draft-prefix; seo-noIndex-not-true |
| _pull | feature | birthday-invitation-design-en.json | pulled-reference | do-not-promote-directly; slug-without-draft-prefix; seo-noIndex-not-true |
| _pull | feature | blog-post-to-instagram-ai-repurposing-en.json | pulled-reference | do-not-promote-directly; slug-without-draft-prefix; seo-noIndex-not-true |
| _pull | feature | book-cover-design-en.json | pulled-reference | do-not-promote-directly; slug-without-draft-prefix; seo-noIndex-not-true |

---

## 八、CSV

机器可读索引：

`page-drafts-index-2026-06.csv`

字段：

`filename,path,ext,bucket,target_type,language,slug,title,draft_status,seo_noindex,management_status,notes`

---

## 九、下一步建议

1. 先从 `composite-v2`、`features-storyline`、`scenarios-storyline`、`landing-storyline` 各抽 5 个样本做人工页面质量判断。
2. 对 `_pull` 保持 `pulled-reference`，用于重排/对照，不直接进入 import。
3. 对候选 JSON 执行 preflight 前，确认 slug 是否应去掉 `draft-`、`seo.noIndex` 是否仍为 true、目标类型是否对应 Tools / Features / Scenarios / Landing。
4. 任何 Sanity import 都必须先 dry-run，并等用户明确授权。
