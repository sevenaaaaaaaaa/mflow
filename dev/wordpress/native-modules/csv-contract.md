# LR Native / LPagery CSV contract v1

LPagery placeholders use single braces: `{column_name}`. One CSV row creates one
page. Column headers must exactly match the placeholders used by the Elementor
seed page.

## Required columns

- `page_title`, `slug`, `industry`, `audience`
- `hero_eyebrow`, `hero_title`, `hero_subtitle`, `hero_body`
- `hero_media_url`, `hero_media_alt`
- `primary_cta_label`, `primary_cta_url`
- `secondary_cta_label`, `secondary_cta_url`
- `seo_title`, `meta_description`, `canonical_url`

## Repeatable fixed slots

- Stats: `stat_1_value`, `stat_1_label` through `stat_4_*`
- Proof cards: `proof_1_title`, `proof_1_body` through `proof_4_*`
- Reviews: `review_1_quote`, `review_1_name`, `review_1_role` through `review_4_*`
- Portraits: `portrait_1_image_url`, `portrait_1_image_alt`,
  `portrait_1_title`, `portrait_1_body` through `portrait_4_*`
- FAQ: `faq_1_question`, `faq_1_answer` through `faq_6_*`
- Final CTA: `final_cta_title`, `final_cta_body`, `final_cta_label`,
  `final_cta_url`

## Validation rules

1. UTF-8 CSV with one header row; `slug` must be unique.
2. URL fields must be absolute HTTPS URLs (except intentionally relative
   internal links).
3. Every image URL requires a non-empty matching alt field.
4. Rich text is allowed only in `*_body` and `faq_*_answer`; scripts, iframes,
   shortcodes, and event-handler attributes are rejected.
5. A generated page fails validation if any `{column_name}` token remains.
6. `page_title`, `seo_title`, and `meta_description` are independent fields.
7. LPagery pages are generated as drafts first; publishing is a separate gate.
