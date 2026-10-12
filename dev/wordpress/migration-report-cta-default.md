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
- 命中 7 页 / 替换 0 块 / 跳过 7 块 / 共 0 行
- 模式：预演（未写文件）

| 页面 | 结果 | 说明 |
|---|:--:|---|
| composite-replica-all.json | — | CTA 全是死链 #，且文案疑似跑错主题（见交接文档 §零）——需人工确认文案与目标后再迁 |
| replica-comparison-hub.json | — | CTA 全是死链 #，且文案疑似跑错主题（见交接文档 §零）——需人工确认文案与目标后再迁 |
| replica-content-hub.json | — | CTA 全是死链 #，且文案疑似跑错主题（见交接文档 §零）——需人工确认文案与目标后再迁 |
| replica-people-reviews.json | — | CTA 全是死链 #，且文案疑似跑错主题（见交接文档 §零）——需人工确认文案与目标后再迁 |
| replica-product-launch.json | — | CTA 全是死链 #，且文案疑似跑错主题（见交接文档 §零）——需人工确认文案与目标后再迁 |
| replica-showcase-gallery.json | — | CTA 全是死链 #，且文案疑似跑错主题（见交接文档 §零）——需人工确认文案与目标后再迁 |
| replica-tool-directory.json | — | CTA 全是死链 #，且文案疑似跑错主题（见交接文档 §零）——需人工确认文案与目标后再迁 |

## 替换成功后的收尾

导入验证无误后，删掉 `assets-src/lovart-replica.js` 里对应的运行时注入（faq → `initFaqFill`，comparison-table → `initCompareFill`，pricing-block → `initPricingRender`）及其硬编码数据表（`LR_FAQ_ANSWERS` / `LR_COMPARE` / `LR_PRICING`），并 bump 版本号。
**replica.js 行数单调下降 = 这条路走对了。**
