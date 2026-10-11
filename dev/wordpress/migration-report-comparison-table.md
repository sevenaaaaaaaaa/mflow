# comparison-table 迁移报告

- 目标微件：`eael-adv-data-table`
- 字段映射：
```
  A 组 · 重复器 settings['settings']['ea_adv_data_table_header'] · 1 个字段槽
      第1列 → ea_adv_data_table_header_col
  B 组 · 重复器 settings['settings']['ea_adv_data_table_rows'] · 4 个字段槽
      第1列 → col_1
      第2列 → col_2
      第3列 → col_3
      第4列 → col_4
```
- 命中 9 页 / 替换 6 块 / 跳过 3 块 / 共 54 行
- 模式：写出到 elem-migrated

| 页面 | 结果 | 说明 |
|---|:--:|---|
| composite-replica-all.json | — | LR_COMPARE 里没有 'composite-replica-all' 这一项（该页对比表是空壳，需先补数据） |
| replica-comparison-hub.json | — | LR_COMPARE 里没有 'comparison-hub' 这一项（该页对比表是空壳，需先补数据） |
| replica-solution-ai-design-for-small-business-hub.json | — | LR_COMPARE 里没有 'ai-design-for-small-business-hub' 这一项（该页对比表是空壳，需先补数据） |
| replica-solution-ai-design-solution-for-agencies.json | ✓ | A组4行 + B组5行 |
| replica-solution-ai-design-solution-for-marketing-teams.json | ✓ | A组4行 + B组5行 |
| replica-solution-ai-design-solution-for-nonprofits.json | ✓ | A组4行 + B组5行 |
| replica-solution-ai-design-solution-for-saas.json | ✓ | A组4行 + B组5行 |
| replica-solution-ai-design-solution-for-shopify.json | ✓ | A组4行 + B组5行 |
| replica-solution-good-design-for-marketers.json | ✓ | A组4行 + B组5行 |

## 替换成功后的收尾

导入验证无误后，删掉 `assets-src/lovart-replica.js` 里对应的运行时注入（faq → `initFaqFill`，comparison-table → `initCompareFill`，pricing-block → `initPricingRender`）及其硬编码数据表（`LR_FAQ_ANSWERS` / `LR_COMPARE` / `LR_PRICING`），并 bump 版本号。
**replica.js 行数单调下降 = 这条路走对了。**
