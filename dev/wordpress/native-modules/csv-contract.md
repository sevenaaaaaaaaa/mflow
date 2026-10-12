# LR Native / LPagery CSV contract v2

> v2（2026-10-12）：按 17 页复刻迁移定稿后的微件形态重写。
> 相对 v1 的重大变化：workflow / capability-tabs / pricing / comparison-table / testimonial
> 进入契约；**comparison-table 是单 HTML blob**、**pricing 是月/年双价列**，两者不可按行拆列。

LPagery placeholders use single braces: `{column_name}`. One CSV row creates one
page. Column headers must exactly match the placeholders used by the Elementor
seed page（`lp-lr-native-v1`）。

> **通道变更（2026-10-13 线上实测）**：LPagery free 版占位符上限 = 3 列
> （`get_placeholder_counts()` 熔断，超出列直接丢弃），本契约 126 列走不通。
> 量产走自建通道 `lr-batch-run.py`：CSV 行 → 本地替换 {col} 进种子 JSON
> → 上传资产服务器 `batch/<slug>.json` → snippet 29 `lr_batch_page` 建页
> （slug/status/SEO meta 由 payload 控制）。LPagery 仅保留作 Page Set 记账备用。

## 0. 端到端链路

```
CSV 一行 → 本地替换种子模板（lp-lr-native-v1）{column} 占位符
→ batch/<slug>.json 上传资产服务器 → lr_batch_page 建 draft 页
→ SSR 渲染探针 + 截图验收 → publish
```

种子模板里的微件全部是**原生具名 settings**（本轮迁移后的形态），没有 `widget-html`
整块嵌入；因此每一列都能落到一个可寻址字段。

## 1. Required columns（页级）

- `page_title`, `slug`, `industry`, `audience`
- `hero_eyebrow`, `hero_title`, `hero_subtitle`, `hero_body`
- `hero_media_url`, `hero_media_alt`
- `primary_cta_label`, `primary_cta_url`
- `secondary_cta_label`, `secondary_cta_url`
- `seo_title`, `meta_description`, `canonical_url`
  （`canonical_url` 建议留空——空值不写 meta，Rank Math 默认 canonical = 实际 permalink；
  自建通道的页面 slug = `slug` 列，填 canonical 时必须与之一致）

## 2. 模块级列（按种子模板实际微件）

### Stats（Counter）
`stat_1_value`, `stat_1_label` … `stat_4_*`

### Proof cards
`proof_1_title`, `proof_1_body` … `proof_4_*`

### Workflow（HT Mega Vertical Timeline，repeater `time_line_content`）
`workflow_1_title`, `workflow_1_desc` … `workflow_4_*`
- 每步描述**必填**（C5 教训：空描述步骤线上直接露白）

### CTA（EA Call to Action，单块）
`final_cta_title`, `final_cta_body`, `final_cta_label`, `final_cta_url`
- 文案必须与页面主题一致（C2 教训：跑题 CTA 全靠 `CTA_OVERRIDES` 兜底，CSV 线直接写对）

### Capability tabs（EA Advanced Tabs，repeater `eael_adv_tabs_tab`）
`tabs_1_title`, `tabs_1_html` … `tabs_4_*`
- `tabs_N_html` 为**整段面板 HTML**（图+h3+p+要点的 tailwind 片段，`.lr` 作用域类）
- 面板数固定 4；`tabs_1_*` 是默认展开面板

### Testimonial（HT Mega Testimonials，repeater `testimonial_items`）
`review_1_quote`, `review_1_name`, `review_1_role`, `review_1_company` … `review_3_*`
- 每页 3 条；`review_N_rating` 可选（缺省 5）
- 字段槽序即模板 `add_control` 顺序：quote → rating → name → role → company → avatar → featured

### Pricing（HT Mega 2026 Pricing，repeater `plan_items`）⚠ 双价列形态
`pricing_{plan}_name`, `pricing_{plan}_monthly`, `pricing_{plan}_annual`,
`pricing_{plan}_tagline`, `pricing_{plan}_features`, `pricing_{plan}_featured`

- `{plan}` ∈ `starter` / `basic` / `pro` / `ultimate`（固定 4 卡；卡组顺序固定）
- **月/年共用一行**：`monthly` 与 `annual` 是两列（单价数字），微件渲染层切换
  `.htm25-pricing--annual` class，**不要**为年付另起一行
- `tagline` 放省钱钩子（允许 `<s>90</s>` 划线 HTML）；**年付 bill 说明放
  `features` 第一行**（模板无独立 billing 字段）
- `featured` 仅 `pro` 行填 `yes`，其余留空（`is_featured` ≠ 'no' 即高亮，**空串也高亮**）
- ⚠ **槽序铁律**：repeater 槽值必须按模板 `add_control` 定义顺序对号
  （`plan_name → is_featured → featured_badge → currency → price_monthly →
  price_annual → period → tagline → features → cta_text → cta_url → cta_variant`）。
  v1 期间曾因自创顺序导致全列错位（currency=16、tagline='yes'），见 HANDOVER §十二。

### Comparison table（EA Advanced Data Table）⚠ 单 blob 形态
`compare_title`, `compare_rows_html`

- 免费层数据源 = **单 HTML 槽** `ea_adv_data_table_static_html`：
  模板自带 `<table>` 外壳，槽内只放 `<thead>+<tbody>`，**没有行列级字段**
- `compare_rows_html` 整块 HTML（5 行 × 4 列），last-col 高亮类 `lr-compare-last`
- 表头/高亮样式走 `replica.css` 的 CSS 变量（`--bg-base-secondary` 亮 `#f2f1ee` /
  暗 `#171612`），不要内联颜色

## 3. Validation rules

1. UTF-8 CSV with one header row; `slug` must be unique.
2. URL fields must be absolute HTTPS URLs（CTA 主按钮统一 `https://www.lovart.ai/canvas`，
   次链接只允许站内真实页：pricing/docs 等，**禁止 `#`**）。
3. Every image URL requires a non-empty matching alt field.
4. Rich text allowed only in `*_html`, `*_body`, `tabs_*_html`, `compare_rows_html`,
   `pricing_*_features`, `faq_*_answer`；scripts / iframes / shortcodes /
   event-handler attributes rejected.
5. A generated page fails validation if any `{column_name}` token remains.
6. `page_title`, `seo_title`, `meta_description` are independent fields.
7. LPagery pages are generated as drafts first; publishing is a separate gate.
8. **No empty repeatable slots**（C5/C3 教训：空面板/空步骤线上直出为空白）。
9. `pricing_*_features` 首行必须是年付账单说明（如 `Billed annually, $192/year`）。

## 4. 迁移期教训映射（为什么是这些列）

| 契约形态 | 教训来源 |
|---|---|
| comparison-table 单 blob | EA 免费层无行列字段，只有 static_html 槽（HANDOVER §十二） |
| pricing 双价列 + 槽序铁律 | 槽错位事故：currency=16 / tagline='yes'（HANDOVER §十二） |
| workflow 描述必填 | C5：9 页 18 段空步骤 |
| tabs 面板 4 段必填 | C3：12 页 3/4 面板空 |
| CTA 文案按页主题 | C2：7 页跑题 Shopify 文案 |
