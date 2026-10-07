# WordPress ID Reconciliation

> 日期：2026-06-08  
> 范围：`03-Published/` 中缺 `wp_post_id`、或带 `wp_status: draft` 的历史资产。  
> 原则：只读反查准备；未联网、未调用 WordPress、未发布、未移动、未删除。

---

## 一、管理结论

当前剩余 Blog / WordPress 元数据问题分两类：

- 23 篇 `additional-published` 旧资产缺 `wp_post_id`，但多数已经有 `wp_status: publish`、`wp_id` 或 `wp_link`。
- 4 篇 `rewrite-*` 历史资产带 `wp_status: draft`，但同时有 `wp_post_id`、`publish_date` 和 `wp_link`。

这批文件不能直接删除，也不应重新发布。正确做法是按 `wp_link` / `wp_id` / `wp_post_id` 向 WordPress 做线上反查，确认每个旧 post 与 rewrite post 的真实关系后再修元数据。

---

## 二、成对反查清单

| kind | old file | old wp id | old status | rewrite file | rewrite post id | rewrite status | score | action |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| possible-old-new-pair | post-415-how-lovarts-edit-elements-outpaces-photoshop-dall-e-3-and-outdated-design-habits.md | 415 | publish | rewrite-post-415-edit-elements-vs-photoshop.md | 18115 | draft | 1.00 | verify whether old post was superseded by rewrite; do not delete either file |
| missing-wp-post-id | post-417-ai-design-wars_-spell-check-real-text-brand-consistency-and-prompt-discipline.md | 417 | publish |  |  |  | 0.15 | lookup WordPress by wp_link or slug and fill wp_post_id only after confirmation |
| missing-wp-post-id | post-422-how-lovart-outperforms-freelancers-templates-and-image-search.md | 422 | publish |  |  |  | 0.15 | lookup WordPress by wp_link or slug and fill wp_post_id only after confirmation |
| missing-wp-post-id | post-424-bubble-tea-branding-capturing-gen-zs-attention-with-ai-powered-visuals.md | 424 | publish |  |  |  | 0.09 | lookup WordPress by wp_link or slug and fill wp_post_id only after confirmation |
| missing-wp-post-id | post-428-the-logic-of-a-bestseller-designing-high-ctr-amazon-listings-and-a-content.md | 428 | publish |  |  |  | 0.08 | lookup WordPress by wp_link or slug and fill wp_post_id only after confirmation |
| possible-old-new-pair | post-430-common-prompting-mistakes-that-are-ruining-your-ai-results-and-how-to-fix-them.md | 430 | publish | rewrite-post-430-common-prompting-mistakes.md | 18116 | draft | 0.50 | verify whether old post was superseded by rewrite; do not delete either file |
| possible-old-new-pair | post-432-raster-png-vs-vector-svg-when-to-use-which.md | 432 | publish | rewrite-post-432-raster-vs-vector.md | 18117 | draft | 1.00 | verify whether old post was superseded by rewrite; do not delete either file |
| possible-old-new-pair | post-516-the-over-prompting-trap-why-novel-length-prompts-confuse-generative-ai.md | 516 | publish | rewrite-post-516-over-prompting-trap.md | 18118 | draft | 0.90 | verify whether old post was superseded by rewrite; do not delete either file |
| missing-wp-post-id | post-520-why-editable-ai-assets-are-the-new-stock-photography.md | 520 | publish |  |  |  | 0.11 | lookup WordPress by wp_link or slug and fill wp_post_id only after confirmation |
| missing-wp-post-id | post-522-why-talking-to-an-ai-agent-feels-less-intimidating-than-using-a-toolbar.md | 522 | publish |  |  |  | 0.08 | lookup WordPress by wp_link or slug and fill wp_post_id only after confirmation |
| missing-wp-post-id | post-524-ai%e8%ae%be%e8%ae%a1%e8%b5%84%e6%ba%90%e5%ba%93-ai%e8%89%b2%e5%bd%a9%e5%bf%83%e7%90%86%e5%ad%a6%e4%b8%8e%e5%93%81%e7%89%8c%e7%ad%96%e7%95%a5%ef%bc%9a%e5%88%a9%e7%94%a8ai%e8%ae%be%e8%ae%a1%e4%bb%a3.md | 524 | publish |  |  |  | 0.00 | lookup WordPress by wp_link or slug and fill wp_post_id only after confirmation |
| missing-wp-post-id | post-526-a-mastering-ai-design-prompts_-negative-space-object-isolation-editable-menus-line-weight-control.md | 526 | publish |  |  |  | 0.13 | lookup WordPress by wp_link or slug and fill wp_post_id only after confirmation |
| missing-wp-post-id | post-528-from-isolating-transparent-stickers-to-editable-menus-and-precise-line-weight-control.md | 528 | publish |  |  |  | 0.08 | lookup WordPress by wp_link or slug and fill wp_post_id only after confirmation |
| missing-wp-post-id | post-530-how-lovart-automatically-crops-images-for-maximum-impact.md | 530 | publish |  |  |  | 0.13 | lookup WordPress by wp_link or slug and fill wp_post_id only after confirmation |
| missing-wp-post-id | post-532-deleting-too-soon-why-your-bad-generation-is-actually-just-one-click-away-from-perfect.md | 532 | publish |  |  |  | 0.00 | lookup WordPress by wp_link or slug and fill wp_post_id only after confirmation |
| missing-wp-post-id | post-534-the-first-co-create-ai-design-agent-driven-canvas-for-digital-marketing-manager.md | 534 | publish |  |  |  | 0.08 | lookup WordPress by wp_link or slug and fill wp_post_id only after confirmation |
| missing-wp-post-id | post-536-the-first-co-create-ai-design-agent-driven-canvas-for-registered-investment-advisor.md | 536 | publish |  |  |  | 0.08 | lookup WordPress by wp_link or slug and fill wp_post_id only after confirmation |
| missing-wp-post-id | post-538-the-first-co-create-ai-design-agent-driven-canvas-for-content-creator.md | 538 | publish |  |  |  | 0.09 | lookup WordPress by wp_link or slug and fill wp_post_id only after confirmation |
| missing-wp-post-id | post-540-the-first-co-create-ai-design-agent-driven-canvas-for-content-creator-2.md | 540 | publish |  |  |  | 0.08 | lookup WordPress by wp_link or slug and fill wp_post_id only after confirmation |
| missing-wp-post-id | post-542-the-first-co-create-ai-design-agent-driven-canvas-for-coach.md | 542 | publish |  |  |  | 0.10 | lookup WordPress by wp_link or slug and fill wp_post_id only after confirmation |
| missing-wp-post-id | post-56-the-death-of-the-render-farm-how-agentic-design-is-rewiring-the-go-to-market-stack-for-intelligent-hardware.md | 56 | publish |  |  |  | 0.18 | lookup WordPress by wp_link or slug and fill wp_post_id only after confirmation |
| missing-wp-post-id | post-59-the-algorithmic-atelier-rewiring-the-fashion-supply-chain-with-agentic-design.md | 59 | publish |  |  |  | 0.10 | lookup WordPress by wp_link or slug and fill wp_post_id only after confirmation |
| missing-wp-post-id | post-61-the-culinary-algorithm-how-independent-restaurateurs-are-using-agentic-design-to-outperform-franchises.md | 61 | publish |  |  |  | 0.25 | lookup WordPress by wp_link or slug and fill wp_post_id only after confirmation |

---

## 三、CSV

机器可读清单：

`wordpress-id-reconciliation-2026-06.csv`

字段：

`kind,old_file,old_slug,old_wp_status,old_wp_id,old_wp_link,new_file,new_slug,new_wp_status,new_wp_post_id,new_wp_link,match_score,recommended_action`

---

## 四、只读核对队列

已新增本地只读脚本：

```bash
python3 scripts/build-wp-readonly-lookup-queue.py
```

脚本原则：

- 不联网。
- 不读取 `wp-auth.local.env`。
- 不发布、不移动、不修改 Markdown。
- 只合并 reconciliation CSV 与 `03-Published/` 本地 frontmatter。

生成文件：

- `WORDPRESS_READONLY_LOOKUP_QUEUE.md`
- `wordpress-readonly-lookup-queue-2026-06.csv`
- `wordpress-readonly-lookup-queue-2026-06.json`

当前队列统计：

| lookup_mode | count | 管理动作 |
| --- | ---: | --- |
| `verify-old-new-pair` | 4 | 先确认旧文与 rewrite post 的线上关系；不删除任一文件 |
| `lookup-by-link-then-id` | 19 | 通过 `wp_link` / 旧 `wp_id` 只读反查，确认后再补元数据 |

---

## 五、建议执行顺序

1. 先用 WordPress 只读 API 或后台搜索 `wp_link` / `wp_id`，确认 23 篇旧资产是否仍在线。
2. 再用 `wp_post_id` 查询 4 篇 rewrite 资产当前真实状态，确认是否为 publish。
3. 如果确认旧 post 被 rewrite 替代，只更新元数据与索引，不删除旧 Markdown。
4. 如果确认某篇旧 post 仍在线，只补 `wp_post_id` 或反查备注，不移动文件。
5. 任何真实发布、取消发布、删除线上文章，都需要单独授权。
