# pricing-block 迁移报告

- 目标微件：`htmega-flip-switcher-pricing`
- 字段映射：
```
  A 组 · 重复器 ['settings']['monthly_plans'] · 8 个字段槽
      第1列 → title
      第2列 → price
      第3列 → old_price
      第4列 → badge_off
      第5列 → bill_note
      第6列 → save_note
      第7列 → features
      第8列 → ribbon
  B 组 · 重复器 ['settings']['yearly_plans'] · 8 个字段槽
      第1列 → title
      第2列 → price
      第3列 → old_price
      第4列 → badge_off
      第5列 → bill_note
      第6列 → save_note
      第7列 → features
      第8列 → ribbon
```
- 注意：定价是全站共用一份（非按页），12 页会填成同样内容
- 命中 12 页 / 替换 12 块 / 跳过 0 块 / 共 96 行
- 模式：写出到 elem-migrated

| 页面 | 结果 | 说明 |
|---|:--:|---|
| composite-replica-all.json | ✓ | A组4行 + B组4行 |
| replica-product-launch.json | ✓ | A组4行 + B组4行 |
| replica-solution-ai-design-for-fitness-wellness-hub.json | ✓ | A组4行 + B组4行 |
| replica-solution-ai-design-for-small-business-hub.json | ✓ | A组4行 + B组4行 |
| replica-solution-ai-design-solution-for-agencies.json | ✓ | A组4行 + B组4行 |
| replica-solution-ai-design-solution-for-creators.json | ✓ | A组4行 + B组4行 |
| replica-solution-ai-design-solution-for-marketing-teams.json | ✓ | A组4行 + B组4行 |
| replica-solution-ai-design-solution-for-nonprofits.json | ✓ | A组4行 + B组4行 |
| replica-solution-ai-design-solution-for-saas.json | ✓ | A组4行 + B组4行 |
| replica-solution-ai-design-solution-for-shopify.json | ✓ | A组4行 + B组4行 |
| replica-solution-good-design-for-business-owners.json | ✓ | A组4行 + B组4行 |
| replica-solution-good-design-for-marketers.json | ✓ | A组4行 + B组4行 |

## 替换成功后的收尾

导入验证无误后，删掉 `assets-src/lovart-replica.js` 里对应的运行时注入（faq → `initFaqFill`，comparison-table → `initCompareFill`，pricing-block → `initPricingRender`）及其硬编码数据表（`LR_FAQ_ANSWERS` / `LR_COMPARE` / `LR_PRICING`），并 bump 版本号。
**replica.js 行数单调下降 = 这条路走对了。**
