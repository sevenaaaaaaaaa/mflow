# Blog Published Index

> 日期：2026-06-08  
> 范围：`03-Published/`、`PRODUCTION-PLAN.md`、Blog 状态目录。  
> 原则：只读对账；未发布、未移动、未修改正文、未删除旧 SOP。  
> 本轮更新：已将 93 篇带 `wp_post_id` 的 Published 文章 frontmatter `status: draft` 修正为 `status: published`；原文已备份到 `1-8 Backup/governance-backups-2026-06-08/blog-published-status-frontmatter/`。

---

## 一、管理结论

- `PRODUCTION-PLAN.md` 记录 93 篇计划。
- `03-Published/` 实际已有 159 篇 Markdown。
- 其中 93 篇能和生产计划按 filename / slug 对上。
- 另外 66 篇属于 Published 中的额外历史发布资产，不应删除，应保留为 `additional-published`。
- 本轮已收敛计划内 Published 的 frontmatter 状态：当前非空且非 `published` 的 frontmatter `status` 为 0 篇。
- 仍有 23 篇缺 `wp_post_id`，另有 4 篇历史 rewrite 资产带 `wp_status: draft`，需要线上反查后再处理。

---

## 二、数量对账

| 项 | 数量 | 判断 |
|---|---:|---|
| Production Plan rows | 93 | 计划表规模 |
| Published markdown files | 159 | 实际 Published 库 |
| Planned rows found in Published | 93 | 与计划匹配 |
| Published not in plan | 66 | 历史发布资产，保留 |
| Plan rows missing from Published | 0 | 需复查 |
| Published missing wp_post_id | 23 | 需复查是否已真实发布 |
| Published frontmatter status mismatch | 0 | 非空且非 published |
| Historical wp_status mismatch | 4 | 需要线上反查，不直接改 |

---

## 三、frontmatter status 分布

| status | count |
| --- | --- |
| published | 93 |
| (blank) | 66 |

---

## 四、计划内 Published 样本

| # | filename | slug | fm status | wp status | wp post id | notes |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | comparison-adobe-firefly-vs-lovart.md | adobe-firefly-vs-lovart | published |  | 18022 |  |
| 2 | comparison-figma-ai-vs-lovart-design-agent.md | figma-ai-vs-lovart-design-agent | published |  | 18024 |  |
| 3 | comparison-microsoft-designer-vs-lovart.md | microsoft-designer-vs-lovart | published |  | 18035 |  |
| 4 | comparison-kittl-vs-lovart.md | kittl-vs-lovart | published |  | 18031 |  |
| 5 | comparison-recraft-vs-lovart.md | recraft-vs-lovart | published |  | 18039 |  |
| 6 | comparison-designs-ai-vs-lovart.md | designs-ai-vs-lovart | published |  | 18023 |  |
| 7 | comparison-leonardo-ai-vs-lovart.md | leonardo-ai-vs-lovart | published |  | 18032 |  |
| 8 | comparison-ideogram-vs-lovart.md | ideogram-vs-lovart | published |  | 18028 |  |
| 9 | comparison-freepik-ai-vs-lovart.md | freepik-ai-vs-lovart | published |  | 18025 |  |
| 10 | comparison-playground-ai-vs-lovart.md | playground-ai-vs-lovart | published |  | 18037 |  |
| 11 | comparison-runway-gen4-vs-lovart.md | runway-gen4-vs-lovart | published |  | 18040 |  |
| 12 | comparison-pika-vs-lovart.md | pika-vs-lovart | published |  | 18036 |  |
| 13 | comparison-luma-dream-machine-vs-lovart.md | luma-dream-machine-vs-lovart | published |  | 18033 |  |
| 14 | comparison-synthesia-vs-lovart.md | synthesia-vs-lovart | published |  | 18041 |  |
| 15 | comparison-heygen-vs-lovart.md | heygen-vs-lovart | published |  | 18027 |  |
| 16 | comparison-invideo-ai-vs-lovart.md | invideo-ai-vs-lovart | published |  | 18029 |  |
| 17 | comparison-adcreative-ai-vs-lovart.md | adcreative-ai-vs-lovart | published |  | 18021 |  |
| 18 | comparison-jasper-art-vs-lovart.md | jasper-art-vs-lovart | published |  | 18030 |  |
| 19 | comparison-predis-ai-vs-lovart.md | predis-ai-vs-lovart | published |  | 18038 |  |
| 20 | comparison-vizcom-vs-lovart.md | vizcom-vs-lovart | published |  | 18043 |  |
| 21 | comparison-meshy-vs-lovart.md | meshy-vs-lovart | published |  | 18034 |  |
| 22 | comparison-uizard-vs-lovart.md | uizard-vs-lovart | published |  | 18042 |  |
| 23 | comparison-galileo-ai-vs-lovart.md | galileo-ai-vs-lovart | published |  | 18026 |  |
| 24 | lovart-101-lovart-chatcanvas-101-complete-getting-started-guide.md | lovart-chatcanvas-101-complete-getting-started-guide | published |  | 18111 |  |
| 25 | lovart-101-mcot-101-lovart-mind-chain-of-thought.md | mcot-101-lovart-mind-chain-of-thought | published |  | 18112 |  |

---

## 五、Published 额外历史资产样本

这些文件已在 Published 目录，但不属于当前 93 篇计划。管理上应标为 `additional-published`，保留并等待线上 URL / WordPress ID 反查。

| filename | slug | fm status | wp status | wp post id | notes |
| --- | --- | --- | --- | --- | --- |
| ai-logo-vs-human-designer.md | ai-logo-generator-vs-human-designer-2026 |  |  | 18007 | not-in-production-plan |
| batch-generate-social-media-content-ai.md | batch-generate-30-days-social-media-content-ai |  |  | 18008 | not-in-production-plan |
| best-practice-brand-kit-setup-5-minutes.md | brand-kit-setup-5-minutes-lovart-best-practice |  |  | 18009 | not-in-production-plan |
| best-practice-nano-banana-consistent-results.md | nano-banana-consistent-results-lovart-best-practice |  |  | 18010 | not-in-production-plan |
| best-practice-touch-edit-3-gestures.md | touch-edit-best-practice-3-gestures-lovart |  |  | 18011 | not-in-production-plan |
| build-complete-brand-kit-from-scratch.md | build-complete-brand-kit-from-scratch-ai |  |  | 18019 | not-in-production-plan |
| canva-vs-lovart-comparison.md | canva-vs-lovart-template-vs-generative-ai-design-2026 |  |  | 18006 | not-in-production-plan |
| color-psychology-brand-design-guide.md | color-psychology-brand-design-complete-guide |  |  | 18020 | not-in-production-plan |
| composition-rules-design-guide.md | composition-rules-design-rule-of-thirds-golden-ratio |  |  | 18044 | not-in-production-plan |
| create-google-ads-ai.md | create-google-ads-with-ai-2026 |  |  | 18045 | not-in-production-plan |
| create-infographics-ai.md | create-infographics-with-ai |  |  | 18046 | not-in-production-plan |
| create-packaging-design-ai.md | create-packaging-design-with-ai |  |  | 18047 | not-in-production-plan |
| create-tiktok-videos-ai.md | create-tiktok-videos-ai-design-agent |  |  | 18048 | not-in-production-plan |
| dall-e-vs-lovart-comparison.md | dall-e-vs-lovart-ai-image-model-design-agent-2026 |  |  | 18049 | not-in-production-plan |
| design-business-cards-ai.md | design-business-cards-with-ai |  |  | 18050 | not-in-production-plan |
| design-presentations-ai.md | design-presentations-with-ai |  |  | 18051 | not-in-production-plan |
| design-restaurant-menu-ai.md | design-restaurant-menu-with-ai |  |  | 18052 | not-in-production-plan |
| flux-vs-nano-banana-comparison.md | flux-vs-nano-banana-ai-image-model-comparison-2026 |  |  | 18053 | not-in-production-plan |
| how-to-ai-lip-sync-characters.md | ai-lip-sync-characters-speak-any-language |  |  | 18057 | not-in-production-plan |
| how-to-ai-shorts-generator.md | ai-shorts-generator-viral-short-form-video |  |  | 18058 | not-in-production-plan |
| how-to-brand-style-guide-ai.md | create-brand-style-guide-with-ai |  |  | 18067 | not-in-production-plan |
| how-to-image-to-video-ai.md | image-to-video-ai-static-designs-into-motion |  |  | 18075 | not-in-production-plan |
| how-to-product-videos-ai.md | how-to-create-product-videos-with-ai |  |  | 18082 | not-in-production-plan |
| midjourney-vs-lovart-comparison.md | midjourney-vs-lovart-ai-design-showdown-2026 |  |  | 18113 | not-in-production-plan |
| nano-banana-ai-complete-guide.md | nano-banana-ai-complete-guide-lovart-image-model |  |  | 18114 | not-in-production-plan |
| post-415-how-lovarts-edit-elements-outpaces-photoshop-dall-e-3-and-outdated-design-habits.md | how-lovarts-edit-elements-outpaces-photoshop-dall-e-3-and-outdated-design-habits |  | publish |  | not-in-production-plan; missing-wp-post-id |
| post-417-ai-design-wars_-spell-check-real-text-brand-consistency-and-prompt-discipline.md | ai-design-wars_-spell-check-real-text-brand-consistency-and-prompt-discipline |  | publish |  | not-in-production-plan; missing-wp-post-id |
| post-422-how-lovart-outperforms-freelancers-templates-and-image-search.md | how-lovart-outperforms-freelancers-templates-and-image-search |  | publish |  | not-in-production-plan; missing-wp-post-id |
| post-424-bubble-tea-branding-capturing-gen-zs-attention-with-ai-powered-visuals.md | bubble-tea-branding-capturing-gen-zs-attention-with-ai-powered-visuals |  | publish |  | not-in-production-plan; missing-wp-post-id |
| post-428-the-logic-of-a-bestseller-designing-high-ctr-amazon-listings-and-a-content.md | the-logic-of-a-bestseller-designing-high-ctr-amazon-listings-and-a-content |  | publish |  | not-in-production-plan; missing-wp-post-id |
| post-430-common-prompting-mistakes-that-are-ruining-your-ai-results-and-how-to-fix-them.md | common-prompting-mistakes-that-are-ruining-your-ai-results-and-how-to-fix-them |  | publish |  | not-in-production-plan; missing-wp-post-id |
| post-432-raster-png-vs-vector-svg-when-to-use-which.md | raster-png-vs-vector-svg-when-to-use-which |  | publish |  | not-in-production-plan; missing-wp-post-id |
| post-516-the-over-prompting-trap-why-novel-length-prompts-confuse-generative-ai.md | the-over-prompting-trap-why-novel-length-prompts-confuse-generative-ai |  | publish |  | not-in-production-plan; missing-wp-post-id |
| post-520-why-editable-ai-assets-are-the-new-stock-photography.md | why-editable-ai-assets-are-the-new-stock-photography |  | publish |  | not-in-production-plan; missing-wp-post-id |
| post-522-why-talking-to-an-ai-agent-feels-less-intimidating-than-using-a-toolbar.md | why-talking-to-an-ai-agent-feels-less-intimidating-than-using-a-toolbar |  | publish |  | not-in-production-plan; missing-wp-post-id |
| post-524-ai%e8%ae%be%e8%ae%a1%e8%b5%84%e6%ba%90%e5%ba%93-ai%e8%89%b2%e5%bd%a9%e5%bf%83%e7%90%86%e5%ad%a6%e4%b8%8e%e5%93%81%e7%89%8c%e7%ad%96%e7%95%a5%ef%bc%9a%e5%88%a9%e7%94%a8ai%e8%ae%be%e8%ae%a1%e4%bb%a3.md | ai%e8%ae%be%e8%ae%a1%e8%b5%84%e6%ba%90%e5%ba%93-ai%e8%89%b2%e5%bd%a9%e5%bf%83%e7%90%86%e5%ad%a6%e4%b8%8e%e5%93%81%e7%89%8c%e7%ad%96%e7%95%a5%ef%bc%9a%e5%88%a9%e7%94%a8ai%e8%ae%be%e8%ae%a1%e4%bb%a3 |  | publish |  | not-in-production-plan; missing-wp-post-id |
| post-526-a-mastering-ai-design-prompts_-negative-space-object-isolation-editable-menus-line-weight-control.md | a-mastering-ai-design-prompts_-negative-space-object-isolation-editable-menus-line-weight-control |  | publish |  | not-in-production-plan; missing-wp-post-id |
| post-528-from-isolating-transparent-stickers-to-editable-menus-and-precise-line-weight-control.md | from-isolating-transparent-stickers-to-editable-menus-and-precise-line-weight-control |  | publish |  | not-in-production-plan; missing-wp-post-id |
| post-530-how-lovart-automatically-crops-images-for-maximum-impact.md | how-lovart-automatically-crops-images-for-maximum-impact |  | publish |  | not-in-production-plan; missing-wp-post-id |
| post-532-deleting-too-soon-why-your-bad-generation-is-actually-just-one-click-away-from-perfect.md | deleting-too-soon-why-your-bad-generation-is-actually-just-one-click-away-from-perfect |  | publish |  | not-in-production-plan; missing-wp-post-id |
| post-534-the-first-co-create-ai-design-agent-driven-canvas-for-digital-marketing-manager.md | the-first-co-create-ai-design-agent-driven-canvas-for-digital-marketing-manager |  | publish |  | not-in-production-plan; missing-wp-post-id |
| post-536-the-first-co-create-ai-design-agent-driven-canvas-for-registered-investment-advisor.md | the-first-co-create-ai-design-agent-driven-canvas-for-registered-investment-advisor |  | publish |  | not-in-production-plan; missing-wp-post-id |
| post-538-the-first-co-create-ai-design-agent-driven-canvas-for-content-creator.md | the-first-co-create-ai-design-agent-driven-canvas-for-content-creator |  | publish |  | not-in-production-plan; missing-wp-post-id |
| post-540-the-first-co-create-ai-design-agent-driven-canvas-for-content-creator-2.md | the-first-co-create-ai-design-agent-driven-canvas-for-content-creator-2 |  | publish |  | not-in-production-plan; missing-wp-post-id |
| post-542-the-first-co-create-ai-design-agent-driven-canvas-for-coach.md | the-first-co-create-ai-design-agent-driven-canvas-for-coach |  | publish |  | not-in-production-plan; missing-wp-post-id |
| post-56-the-death-of-the-render-farm-how-agentic-design-is-rewiring-the-go-to-market-stack-for-intelligent-hardware.md | the-death-of-the-render-farm-how-agentic-design-is-rewiring-the-go-to-market-stack-for-intelligent-hardware |  | publish |  | not-in-production-plan; missing-wp-post-id |
| post-59-the-algorithmic-atelier-rewiring-the-fashion-supply-chain-with-agentic-design.md | the-algorithmic-atelier-rewiring-the-fashion-supply-chain-with-agentic-design |  | publish |  | not-in-production-plan; missing-wp-post-id |
| post-61-the-culinary-algorithm-how-independent-restaurateurs-are-using-agentic-design-to-outperform-franchises.md | the-culinary-algorithm-how-independent-restaurateurs-are-using-agentic-design-to-outperform-franchises |  | publish |  | not-in-production-plan; missing-wp-post-id |
| rewrite-post-415-edit-elements-vs-photoshop.md | how-lovarts-edit-elements-outpaces-photoshop-dall-e-3-and-outdated-design-habits |  | draft | 18115 | not-in-production-plan; wp-status-draft-requires-online-check |
| rewrite-post-430-common-prompting-mistakes.md | common-ai-prompting-mistakes-design-results-how-to-fix |  | draft | 18116 | not-in-production-plan; wp-status-draft-requires-online-check |

---

## 六、历史 wp_status 待反查样本

| filename | slug | wp status | wp post id | notes |
| --- | --- | --- | --- | --- |
| rewrite-post-415-edit-elements-vs-photoshop.md | how-lovarts-edit-elements-outpaces-photoshop-dall-e-3-and-outdated-design-habits | draft | 18115 | not-in-production-plan; wp-status-draft-requires-online-check |
| rewrite-post-430-common-prompting-mistakes.md | common-ai-prompting-mistakes-design-results-how-to-fix | draft | 18116 | not-in-production-plan; wp-status-draft-requires-online-check |
| rewrite-post-432-raster-vs-vector.md | raster-png-vs-vector-svg-when-to-use-which | draft | 18117 | not-in-production-plan; wp-status-draft-requires-online-check |
| rewrite-post-516-over-prompting-trap.md | over-prompting-trap-novel-length-prompts-confuse-generative-ai | draft | 18118 | not-in-production-plan; wp-status-draft-requires-online-check |

---

## 七、缺 WordPress ID 样本

| filename | slug | fm status | wp status | notes |
| --- | --- | --- | --- | --- |
| post-415-how-lovarts-edit-elements-outpaces-photoshop-dall-e-3-and-outdated-design-habits.md | how-lovarts-edit-elements-outpaces-photoshop-dall-e-3-and-outdated-design-habits |  | publish | not-in-production-plan; missing-wp-post-id |
| post-417-ai-design-wars_-spell-check-real-text-brand-consistency-and-prompt-discipline.md | ai-design-wars_-spell-check-real-text-brand-consistency-and-prompt-discipline |  | publish | not-in-production-plan; missing-wp-post-id |
| post-422-how-lovart-outperforms-freelancers-templates-and-image-search.md | how-lovart-outperforms-freelancers-templates-and-image-search |  | publish | not-in-production-plan; missing-wp-post-id |
| post-424-bubble-tea-branding-capturing-gen-zs-attention-with-ai-powered-visuals.md | bubble-tea-branding-capturing-gen-zs-attention-with-ai-powered-visuals |  | publish | not-in-production-plan; missing-wp-post-id |
| post-428-the-logic-of-a-bestseller-designing-high-ctr-amazon-listings-and-a-content.md | the-logic-of-a-bestseller-designing-high-ctr-amazon-listings-and-a-content |  | publish | not-in-production-plan; missing-wp-post-id |
| post-430-common-prompting-mistakes-that-are-ruining-your-ai-results-and-how-to-fix-them.md | common-prompting-mistakes-that-are-ruining-your-ai-results-and-how-to-fix-them |  | publish | not-in-production-plan; missing-wp-post-id |
| post-432-raster-png-vs-vector-svg-when-to-use-which.md | raster-png-vs-vector-svg-when-to-use-which |  | publish | not-in-production-plan; missing-wp-post-id |
| post-516-the-over-prompting-trap-why-novel-length-prompts-confuse-generative-ai.md | the-over-prompting-trap-why-novel-length-prompts-confuse-generative-ai |  | publish | not-in-production-plan; missing-wp-post-id |
| post-520-why-editable-ai-assets-are-the-new-stock-photography.md | why-editable-ai-assets-are-the-new-stock-photography |  | publish | not-in-production-plan; missing-wp-post-id |
| post-522-why-talking-to-an-ai-agent-feels-less-intimidating-than-using-a-toolbar.md | why-talking-to-an-ai-agent-feels-less-intimidating-than-using-a-toolbar |  | publish | not-in-production-plan; missing-wp-post-id |
| post-524-ai%e8%ae%be%e8%ae%a1%e8%b5%84%e6%ba%90%e5%ba%93-ai%e8%89%b2%e5%bd%a9%e5%bf%83%e7%90%86%e5%ad%a6%e4%b8%8e%e5%93%81%e7%89%8c%e7%ad%96%e7%95%a5%ef%bc%9a%e5%88%a9%e7%94%a8ai%e8%ae%be%e8%ae%a1%e4%bb%a3.md | ai%e8%ae%be%e8%ae%a1%e8%b5%84%e6%ba%90%e5%ba%93-ai%e8%89%b2%e5%bd%a9%e5%bf%83%e7%90%86%e5%ad%a6%e4%b8%8e%e5%93%81%e7%89%8c%e7%ad%96%e7%95%a5%ef%bc%9a%e5%88%a9%e7%94%a8ai%e8%ae%be%e8%ae%a1%e4%bb%a3 |  | publish | not-in-production-plan; missing-wp-post-id |
| post-526-a-mastering-ai-design-prompts_-negative-space-object-isolation-editable-menus-line-weight-control.md | a-mastering-ai-design-prompts_-negative-space-object-isolation-editable-menus-line-weight-control |  | publish | not-in-production-plan; missing-wp-post-id |
| post-528-from-isolating-transparent-stickers-to-editable-menus-and-precise-line-weight-control.md | from-isolating-transparent-stickers-to-editable-menus-and-precise-line-weight-control |  | publish | not-in-production-plan; missing-wp-post-id |
| post-530-how-lovart-automatically-crops-images-for-maximum-impact.md | how-lovart-automatically-crops-images-for-maximum-impact |  | publish | not-in-production-plan; missing-wp-post-id |
| post-532-deleting-too-soon-why-your-bad-generation-is-actually-just-one-click-away-from-perfect.md | deleting-too-soon-why-your-bad-generation-is-actually-just-one-click-away-from-perfect |  | publish | not-in-production-plan; missing-wp-post-id |
| post-534-the-first-co-create-ai-design-agent-driven-canvas-for-digital-marketing-manager.md | the-first-co-create-ai-design-agent-driven-canvas-for-digital-marketing-manager |  | publish | not-in-production-plan; missing-wp-post-id |
| post-536-the-first-co-create-ai-design-agent-driven-canvas-for-registered-investment-advisor.md | the-first-co-create-ai-design-agent-driven-canvas-for-registered-investment-advisor |  | publish | not-in-production-plan; missing-wp-post-id |
| post-538-the-first-co-create-ai-design-agent-driven-canvas-for-content-creator.md | the-first-co-create-ai-design-agent-driven-canvas-for-content-creator |  | publish | not-in-production-plan; missing-wp-post-id |
| post-540-the-first-co-create-ai-design-agent-driven-canvas-for-content-creator-2.md | the-first-co-create-ai-design-agent-driven-canvas-for-content-creator-2 |  | publish | not-in-production-plan; missing-wp-post-id |
| post-542-the-first-co-create-ai-design-agent-driven-canvas-for-coach.md | the-first-co-create-ai-design-agent-driven-canvas-for-coach |  | publish | not-in-production-plan; missing-wp-post-id |
| post-56-the-death-of-the-render-farm-how-agentic-design-is-rewiring-the-go-to-market-stack-for-intelligent-hardware.md | the-death-of-the-render-farm-how-agentic-design-is-rewiring-the-go-to-market-stack-for-intelligent-hardware |  | publish | not-in-production-plan; missing-wp-post-id |
| post-59-the-algorithmic-atelier-rewiring-the-fashion-supply-chain-with-agentic-design.md | the-algorithmic-atelier-rewiring-the-fashion-supply-chain-with-agentic-design |  | publish | not-in-production-plan; missing-wp-post-id |
| post-61-the-culinary-algorithm-how-independent-restaurateurs-are-using-agentic-design-to-outperform-franchises.md | the-culinary-algorithm-how-independent-restaurateurs-are-using-agentic-design-to-outperform-franchises |  | publish | not-in-production-plan; missing-wp-post-id |

---

## 八、CSV

机器可读索引：

`blog-published-index-2026-06.csv`

字段：

`filename,path,slug,title,date,language,category,folder_status,frontmatter_status,wp_status,wp_post_id,plan_slug,plan_index,plan_status,plan_match,source_bucket,notes`

---

## 九、下一步建议

1. 对 23 篇缺 `wp_post_id` 的 `additional-published` 资产建立线上 URL / WordPress ID 反查，不要从计划表里删掉它们。
2. 对 4 篇 `wp_status: draft` 的 rewrite 资产做线上反查，确认 WordPress 当前状态后再改字段。
3. 保持 `02-Ready-to-Publish/` 为空队列的语义：只有通过质量门禁的 Draft 才能进入。
4. 后续如要真实发布，仍需先跑 `publish-to-wp.py --dry-run`，再等用户明确授权。
