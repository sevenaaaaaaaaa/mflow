# cta-default 迁移报告

- 目标微件：`eael-cta-box`
- 字段映射：
```
  A 组 · 平铺字段 · 5 个字段槽
      第1列 → settings.eael_cta_title
      第2列 → settings.eael_cta_btn_text
      第3列 → settings.eael_cta_btn_link.url
      第4列 → settings.eael_cta_secondary_btn_text
      第5列 → settings.eael_cta_secondary_btn_link.url
```
- 命中 17 页 / 替换 10 块 / 跳过 7 块 / 共 10 行
- 模式：写出到 elem-migrated

| 页面 | 结果 | 说明 |
|---|:--:|---|
| composite-replica-all.json | — | CTA 全是死链 #，且文案疑似跑错主题（见交接文档 §零）——需人工确认文案与目标后再迁 |
| replica-comparison-hub.json | — | 该页 CTA 块吞进了站点页脚（19 个链接）——换成微件会让页脚消失。页脚请用 Elementor Theme Builder 单独做，拆出来后再迁 |
| replica-content-hub.json | — | 该页 CTA 块吞进了站点页脚（19 个链接）——换成微件会让页脚消失。页脚请用 Elementor Theme Builder 单独做，拆出来后再迁 |
| replica-people-reviews.json | — | CTA 全是死链 #，且文案疑似跑错主题（见交接文档 §零）——需人工确认文案与目标后再迁 |
| replica-product-launch.json | — | 该页 CTA 块吞进了站点页脚（19 个链接）——换成微件会让页脚消失。页脚请用 Elementor Theme Builder 单独做，拆出来后再迁 |
| replica-showcase-gallery.json | — | 该页 CTA 块吞进了站点页脚（19 个链接）——换成微件会让页脚消失。页脚请用 Elementor Theme Builder 单独做，拆出来后再迁 |
| replica-solution-ai-design-for-fitness-wellness-hub.json | ✓ | A组1行 |
| replica-solution-ai-design-for-small-business-hub.json | ✓ | A组1行 ⚠ 次链接「See local examples」原本是死链 #，迁移后需补目标 |
| replica-solution-ai-design-solution-for-agencies.json | ✓ | A组1行 |
| replica-solution-ai-design-solution-for-creators.json | ✓ | A组1行 |
| replica-solution-ai-design-solution-for-marketing-teams.json | ✓ | A组1行 |
| replica-solution-ai-design-solution-for-nonprofits.json | ✓ | A组1行 |
| replica-solution-ai-design-solution-for-saas.json | ✓ | A组1行 |
| replica-solution-ai-design-solution-for-shopify.json | ✓ | A组1行 |
| replica-solution-good-design-for-business-owners.json | ✓ | A组1行 |
| replica-solution-good-design-for-marketers.json | ✓ | A组1行 |
| replica-tool-directory.json | — | 该页 CTA 块吞进了站点页脚（19 个链接）——换成微件会让页脚消失。页脚请用 Elementor Theme Builder 单独做，拆出来后再迁 |

## 替换成功后的收尾

导入验证无误后，删掉 `assets-src/lovart-replica.js` 里对应的运行时注入（faq → `initFaqFill`，comparison-table → `initCompareFill`，pricing-block → `initPricingRender`）及其硬编码数据表（`LR_FAQ_ANSWERS` / `LR_COMPARE` / `LR_PRICING`），并 bump 版本号。
**replica.js 行数单调下降 = 这条路走对了。**
