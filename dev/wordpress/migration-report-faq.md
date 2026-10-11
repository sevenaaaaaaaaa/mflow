# faq 迁移报告

- 目标微件：`eael-adv-accordion`
- 字段映射：
```
  A 组 · 重复器 ['settings']['eael_adv_accordion_tab'] · 2 个字段槽
      第1列 → eael_adv_accordion_tab_title
      第2列 → eael_adv_accordion_tab_content
```
- 命中 13 页 / 替换 12 块 / 跳过 1 块 / 共 76 行
- 模式：写出到 elem-migrated

| 页面 | 结果 | 说明 |
|---|:--:|---|
| composite-replica-all.json | — | LR_FAQ_ANSWERS 里没有 'composite-replica-all' 这一项 |
| replica-comparison-hub.json | ✓ | A组8行 |
| replica-product-launch.json | ✓ | A组8行 |
| replica-solution-ai-design-for-fitness-wellness-hub.json | ✓ | A组6行 |
| replica-solution-ai-design-for-small-business-hub.json | ✓ | A组6行 |
| replica-solution-ai-design-solution-for-agencies.json | ✓ | A组5行 |
| replica-solution-ai-design-solution-for-creators.json | ✓ | A组6行 |
| replica-solution-ai-design-solution-for-marketing-teams.json | ✓ | A组6行 |
| replica-solution-ai-design-solution-for-nonprofits.json | ✓ | A组5行 |
| replica-solution-ai-design-solution-for-saas.json | ✓ | A组6行 |
| replica-solution-ai-design-solution-for-shopify.json | ✓ | A组6行 |
| replica-solution-good-design-for-business-owners.json | ✓ | A组7行 |
| replica-solution-good-design-for-marketers.json | ✓ | A组7行 |

## 替换成功后的收尾

导入验证无误后，删掉 `assets-src/lovart-replica.js` 里对应的运行时注入（faq → `initFaqFill`，comparison-table → `initCompareFill`，pricing-block → `initPricingRender`）及其硬编码数据表（`LR_FAQ_ANSWERS` / `LR_COMPARE` / `LR_PRICING`），并 bump 版本号。
**replica.js 行数单调下降 = 这条路走对了。**
