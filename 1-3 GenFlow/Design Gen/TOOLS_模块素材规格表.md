# Tools 模块素材规格表

> 基于 Sanity compositePage 14-section 标准框架 | 更新: 2026-06-16

---

## 一、Section → Media Slot 映射

每页 14 个 section，共 **15 个 media.src 槽位**：

| # | Section Type | Slot 数 | 位置 | 建议尺寸 | 用途 |
|---|-------------|---------|------|---------|------|
| 1 | hero-split | **1** | `media.src` | 1200×630px | 主视觉/OG 图 |
| 2 | bento-4 | **4** | `features[0-3].media.src` | 600×400px | 功能卡片图 |
| 3 | bento-2 | **2** | `features[0-1].media.src` | 800×500px | 对比展示图 |
| 4 | capability-tabs | **4** | `tabs[0-3].content.media.src` | 800×500px | Tab 切换图 |
| 5 | prompt-launcher | 0 | — | — | 无图片 |
| 6 | logo-loop | 0 | — | — | 无图片 |
| 7 | cta-default | 0 | — | — | 无图片 |
| 8 | workflow-horizontal | 0 | — | — | 无图片 |
| 9 | comparison-table | 0 | — | — | 无图片 |
| 10 | cluster-block-dense | 0 | — | — | icon 类 |
| 11 | feature-detail | **4** | `items[0-3].media.src` | 800×500px | 详情图 |
| 12 | proof-block | 0 | — | — | icon 类 |
| 13 | faq | 0 | — | — | 无图片 |
| 14 | cta-default | 0 | — | — | 无图片 |

**总计**：每页 **15 个 media.src 槽位**，443 slug × 15 = **6,645 个槽位**（仅 TOOL 分类）

---

## 二、全站素材需求

| 分类 | Slug | 槽位/页 | 总槽位 | 已填充(URL) | 去重URL | 缺口 |
|------|------|---------|--------|-----------|---------|------|
| **TOOL** | 443 | 15 | 6,645 | 908 | ~50 | 5,737 |
| **FEATURE** | 246 | 14 | 3,444 | 3,041 | 146 | 403 |
| **TOPIC** | 48 | 21 | 987 | 410 | ? | 577 |
| **SCENARIO** | 70 | 12 | 840 | 695 | ? | 145 |
| **SOLUTION** | 10 | 17 | 170 | 140 | 51 | 30 |
| **PRODUCT** | 2 | 15 | 30 | 20 | 15 | 10 |
| **LANDING** | 3 | 19 | 57 | 72 | ? | 0 |
| **合计** | **822** | — | **12,173** | **5,286** | **~206** | **6,887** |

---

## 三、按槽位类型的需求分布

| 槽位类型 | 每页数量 | 全站总数(TOOL) | 建议图片类型 |
|---------|---------|---------------|-------------|
| **hero-split** | 1 | 443 | 1200×630 横向产品展示图 |
| **bento-4 features** | 4 | 1,772 | 600×400 功能特写图 |
| **bento-2 features** | 2 | 886 | 800×500 对比/场景图 |
| **capability-tabs** | 4 | 1,772 | 800×500 UI/能力展示图 |
| **feature-detail** | 4 | 1,772 | 800×500 深度功能图 |

---

## 四、按品类的图片风格建议

| 品类 | Slug数 | Hero 风格 | Feature 风格 |
|------|--------|----------|-------------|
| video | 42 | 视频播放界面/时间线 | 剪辑/特效/音频/导出 |
| social-media | 26 | 社媒帖子 mockup | 各平台尺寸模板 |
| marketing | 24 | 广告 banner 展示 | CTA/转化/AB测试 |
| brand-identity | 22 | Logo/VI 展示 | 配色/字体/规范 |
| print-design | 29 | 印刷品实物 mockup | 海报/传单/名片/手册 |
| design-tool | 38 | 设计界面截图 | 工具功能截图 |
| ai-capability | 31 | AI 生成结果对比 | 输入→输出对比 |
| photo-editing | 17 | 前后对比图 | 工具效果展示 |
| product-ecommerce | 16 | 产品场景图 | 电商场景 |

---

## 五、当前图片重用严重度

| 指标 | 数值 |
|------|------|
| 全站去重URL | ~206 个 |
| 全站槽位 | ~12,173 个 |
| 平均每个URL被 | **59 页**使用 |
| TOOL 最热 URL | 被 246 页同时使用 |
| FEATURE 最热 URL | 被 246 页同时使用 |

> 同一批 206 个 URL 循环复用，视觉效果极度同质化。

---

## 六、建议素材制作优先级

| 优先级 | 品类 | 页数 | 需新图(去重) | 理由 |
|--------|------|------|-------------|------|
| P0 | video | 42 | 15×42=630 | 高搜索量，视频品类 visual 需求强 |
| P0 | print-design | 29 | 435 | 印刷品需要实物 mockup |
| P0 | brand-identity | 22 | 330 | Logo/VI 需独特展示 |
| P1 | social-media | 26 | 390 | 社媒需各平台 mockup |
| P1 | marketing | 24 | 360 | 广告需真实 banner 效果 |
| P1 | ai-capability | 31 | 465 | AI 能力需前后对比图 |
| P2 | design-tool | 38 | 570 | 可用通用产品截图 |
| P2 | photo-editing | 17 | 255 | 可用效果对比图 |
| P2 | 其他 | 214 | 3,210 | 按需逐步覆盖 |
