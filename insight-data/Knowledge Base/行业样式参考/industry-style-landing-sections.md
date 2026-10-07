# 落地页样式分类（按行业/场景）

> 来源：内容库 17.5k 页的 tool/feature 页面结构分析

## 按 storylineTemplate 分

| 模板 | 适用场景 | 现有页面数 |
|------|---------|-----------|
| T-long | 深度工具页（功能多/需要教育） | 大部分 |
| T-short | 简单工具页（单一功能，快速 CTA） | 较少 |

## 按 section 结构分

### 标准工具页（最常见，12 版块）
hero-split → bento-4 → capability-tabs → prompt-launcher → bento-2 → canvas-wall → workflow-horizontal → comparison-table → cluster-block-dense → feature-detail → faq → cta-default

### 简化工具页（7 版块）
hero-split → feature-detail(×4) → faq → cta-default

### 品牌页（加分项）
+ testimonial · pricing-block · logo-loop

## 写样式参考时的规则

1. **hero 必须有**：badge + title + description + highlightedText + buttons + media
2. **bento 版块**的 features 数组每个项必须有 title + description
3. **capability-tabs** 的 tabs 数组每个项必须有 label + content.title + content.description
4. **comparison-table** 的 rows 每行必须有 feature + values[]
5. **faq** 的 items 是 [问题, 回答] 对（数组套数组）
6. **cta-default** 必须有 buttons[]，每个 button 必须有 text + href + variant
