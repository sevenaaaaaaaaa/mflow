# faq 迁移报告

- 目标微件：`eael-adv-accordion`
- 重复器：`settings.eael_adv_accordion_tab`，标题 `eael_adv_accordion_tab_title`，正文 `eael_adv_accordion_tab_content`
- 命中 13 页 / 替换 12 块 / 跳过 1 块
- 模式：写出到 elem-migrated

| 页面 | 结果 | 说明 |
|---|:--:|---|
| composite-replica-all.json | — | LR_FAQ_ANSWERS 里没有 'composite-replica-all' 这一项 |
| replica-comparison-hub.json | ✓ | 8 条 |
| replica-product-launch.json | ✓ | 8 条 |
| replica-solution-ai-design-for-fitness-wellness-hub.json | ✓ | 6 条 |
| replica-solution-ai-design-for-small-business-hub.json | ✓ | 6 条 |
| replica-solution-ai-design-solution-for-agencies.json | ✓ | 5 条 |
| replica-solution-ai-design-solution-for-creators.json | ✓ | 6 条 |
| replica-solution-ai-design-solution-for-marketing-teams.json | ✓ | 6 条 |
| replica-solution-ai-design-solution-for-nonprofits.json | ✓ | 5 条 |
| replica-solution-ai-design-solution-for-saas.json | ✓ | 6 条 |
| replica-solution-ai-design-solution-for-shopify.json | ✓ | 6 条 |
| replica-solution-good-design-for-business-owners.json | ✓ | 7 条 |
| replica-solution-good-design-for-marketers.json | ✓ | 7 条 |

## 替换成功后的收尾

导入验证无误后，删掉 `assets-src/lovart-replica.js` 里对应的运行时注入函数（faq → `initFaqFill`），并 bump 版本号。
**replica.js 行数单调下降 = 这条路走对了。**
