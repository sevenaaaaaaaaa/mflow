# Lovart SEO Q3 可执行战术计划（Jul-Sep 2026）

> **编制日期**：2026-06-13
> **数据基线**：2026-05-27 ~ 06-07 GSC/i18n 关键词情报
> **目标周期**：2026年 Q3（7-9月）

---

## 📊 数据基线诊断

### 当前状态 vs OKR 目标

| 指标 | 当前基线 | OKR 目标 | 缺口 | 难度 |
|------|---------|---------|------|------|
| **非品牌词点击占比** | **~2.2%**（unmatched sample） | **30%** | **-27.8pp** | 🔴 极高 |
| **品牌词点击占比** | **97.8%** | 逐步降低 | — | — |
| **GSC 曝光量** | 待确认（估算200-230k） | **280k** | ~50-80k | 🟡 中 |
| **Tools 页面数** | **7篇**（Docs）+ 部分Landing | **50+** | **43+** | 🔴 高 |
| **Tools 总点击** | 待确认 | **10,000** | — | 🔴 高 |
| **Tools CTR** | 待确认（估算<1%） | **3%** | — | 🟡 中 |
| **收录率** | 待确认 | **55%** | — | 🟡 中 |
| **收录页面数** | 待确认 | **10,000+** | — | 🔴 高 |
| **首页曝光占比** | 待确认（估算>90%） | **75%** | 降15pp+ | 🟡 中 |
| **i18n本地化页面** | **0页** | 各语言5-10页 | — | 🟢 低 |

### 非品牌词现状深度分析

#### 高展示低点击机会词（🔴 最优先攻坚）

| 关键词 | 展示量 | 点击率 | 排名 | 机会诊断 |
|--------|--------|--------|------|----------|
| **luma dream machine** | 1,402 | 0.3% | 8.7 | 竞品词，排名低→需独立对比页 |
| **hedra ai** | 1,259 | 0.2% | 6.6 | 竞品词，排名低→需独立对比页 |
| **veo 3.1** | 418 | 0.7% | 9.1 | 产品词，排名低→需独立工具页 |
| **veo ai free** | 390 | 1.0% | 8.6 | 意图词，排名低→需独立工具页 |
| **nano banana free** | 345 | 2.0% | 8.8 | 产品词，排名低→需独立工具页 |
| **nano banana ai free** | 200 | 3.0% | 10.3 | 产品词，排名低→需独立工具页 |
| **nano banana ai** | 180 | 1.7% | 6.9 | 产品词，排名低→需独立工具页 |
| **veo 3.1 free** | 128 | 6.2% | 5.9 | 意图词→需独立工具页 |
| **art ai** | 115 | 5.2% | 6.2 | 泛词→需Pilar Page |
| **nano banana pro free unlimited** | 94 | 9.6% | 6.6 | 意图词→需独立工具页 |

**核心问题：这些非品牌词页面关联到了博客/首页，而非专用工具落地页，导致 CTR 极低。**

---

## 🎯 O2 — 转化率驱动增长（CRO + 扩量）

> **目标**：通过精细化用户分组和页面级CRO，新增注册人数提升28.4%（155k→200k），新增付费人数提升133.4%（1,714→4,000），新增付费金额提升130%（$99k→$220k）

### O2 数学模型

| 指标 | 基线 | O2 目标 | 增幅 | 驱动力 |
|------|------|---------|------|--------|
| 新增注册 | 155,000 | 200,000 | +29.0% | KR1 CRO + KR2 扩量 |
| 新增付费 | 1,714 | 4,000 | +133.4% | KR1 注册→付费率 + KR2 新页面高转化 |
| 新增付费金额 | $99,000 | $220,000 | +122.2% | 付费人数驱动（ARPPU 维持 ~$55） |
| UV→注册率 | 14.4% | 18.0%+ | +25.0% | KR1 首页/非品牌词页面 CRO |
| 注册→付费率 | 1.11% | 1.50% | +35.6% | KR1 付费漏斗优化 |

### KR 拆解逻辑

```
O2 目标 = KR1（CRO 提升，UV 不变）+ KR2（扩量，新增 UV）

KR1 单独效果（假设 UV 不变 ≈ 1,076k/月）:
  注册: 1,076k × 18% = 193,750     → 缺口 6,250（3.1%）
  付费: 193,750 × 1.5% = 2,906     → 缺口 1,093（27.3%）
  金额: 2,906 × $55 = $159,856     → 缺口 $60,144（27.3%）

KR2 需补足:
  额外 UV: 34,722/月（落地页翻倍 +100%）
  额外注册: 6,250
  额外付费: 1,093
  额外金额: $60,144

KR1 + KR2 = O2 ✅
```

---

### 🎯 O2-KR1 — 页面级 CRO（转化率优化）

> **目标**：UV→注册率从 14.4% 提升至 18%+，注册→付费率从 1.11% 提升至 1.5%

#### T-CRO.1 首页 CRO 优化

| Task | Owner | Week | 预期效果 |
|------|-------|------|----------|
| **首页注册漏斗审计**：热力图分析（Hotjar/Clarity）用户行为路径，定位流失点 | SEO+Dev | W1 | 数据基线 |
| **Hero 区 CTA 优化**：A/B 测试不同 CTA 文案（"Try Free" vs "Start Creating" vs "Design with AI"） | SEO+Content | W1-W3 | UV→注册率 +1-2pp |
| **Social Proof 强化**：首页添加用户数、生成量、国家数等数据指标 | Dev | W2 | 信任感提升 |
| **注册流程简化**：减少注册步骤（Google/GitHub 一键登录优先展示） | Dev | W2-W3 | 注册流失率降低 |
| **定价页引导优化**：从首页到定价页的路径优化，突出免费试用 | SEO+Dev | W3-W4 | 注册→付费率提升 |

#### T-CRO.2 非品牌词落地页 CRO

| Task | Owner | Week | 预期效果 |
|------|-------|------|----------|
| **Tools 页面 CTA 统一化**：每个 Tools 页底部增加「Try in Lovart」强 CTA | Dev | W2-W4 | Tools 页注册转化提升 |
| **Before/After 展示优化**：关键 Tools 页面增加「生成效果对比」模块 | Content+Design | W3-W6 | 说服力提升 |
| **Landing 页面首屏优化**：重点 Landing 页首屏增加「Start Free」按钮 + 价值承诺 | Dev | W3-W5 | 首屏注册率提升 |
| **P0 关键词页面 CRO**：Top 10 高展示非品牌词页面逐一优化注册漏斗 | SEO+Content | W4-W8 | 非品牌词页面转化率提升 |

#### T-CRO.3 注册→付费转化优化

| Task | Owner | Week | 预期效果 |
|------|-------|------|----------|
| **新用户 Onboarding 优化**：注册后引导用户完成首次创作（降低 Activation 摩擦） | Product+Dev | W2-W6 | 注册→激活率提升 |
| **Paywall 策略调整**：优化免费额度限制，在用户「尝到甜头」后触发付费提示 | Product | W3-W6 | 注册→付费率 +0.2-0.3pp |
| **邮件 Drip Campaign**：注册后 1/3/7/14 天自动邮件，引导深度使用→付费 | Marketing | W4-W6 | 长周期转化提升 |
| **用户分群策略**：按来源渠道（SEO/Referral/GEO）分组，针对性优化付费路径 | SEO+Product | W4-W8 | 分群转化率差异化提升 |

---

### 🎯 O2-KR2 — 落地页扩量（+100%）

> **目标**：落地页数量翻倍，新增 UV 34,722/月，补足 KR1 CRO 后的注册和付费缺口

**执行载体**：O2-KR2 通过下方 **KR2（Tools 页面矩阵 55+）** 和 **KR3（非品牌词+竞品覆盖）** 联合落地，不再独立拆战术。具体执行细节见：

| O2-KR2 子目标 | 执行层 | 产出 |
|---------------|--------|------|
| 用户偏好类非品牌词布局 | **KR3** T3.2 非品牌词增长引擎 + PSEO 长尾页 | 175 篇 PSEO + 博客/Glossary |
| 竞品高流量词落地页 | **KR3** T3.1 竞品非品牌词覆盖矩阵 | 13 竞品 80+ 词覆盖 |
| Tools 页面扩建 | **KR2** T2.1-T2.2 Tools 页面架构 + 分批执行 | 7→55 篇 Tools 页 |
| 落地页质量保障 | **KR2** T2.3 SEO 规范 + T2.4 CTR 提升 | 统一模板 + Schema |

**额外补充任务**（KR2/KR3 未覆盖）：

| Task | Owner | Week | 说明 |
|------|-------|------|------|
| **新落地页 CRO 模板**：统一 Hero+Steps+Social Proof+CTA+FAQ 结构 | Dev+SEO | W1 | 确保新页面自带转化基因 |
| **落地页→注册漏斗统一**：所有新页面注册入口统一为「Try Free → Google Login → Canvas」 | Dev | W2 | 注册路径标准化 |
| **场景化落地页**：按职业/行业定制（设计师/营销人/电商卖家/自媒体），每类 3-5 篇 | Content | W4-W10 | 20-30 篇（KR2/KR3 未覆盖的场景页） |

---

### O2-KR1 + KR2 合计效果模拟

| 指标 | KR1（CRO） | KR2（扩量） | 合计 | O2 目标 | 达成 |
|------|-----------|-----------|------|---------|------|
| 新增注册 | 193,750 | +6,250 | **200,000** | 200,000 | ✅ |
| 新增付费 | 2,906 | +1,093 | **3,999** | 4,000 | ✅ |
| 新增付费金额 | $159,856 | +$60,144 | **$220,000** | $220,000 | ✅ |

### O2 关键风险

| 风险 | 概率 | 影响 | 应对 |
|------|------|------|------|
| **CRO 提升幅度不达预期** | 中 | 高 | Phase 1 先在首页和 Top 5 Tools 页验证，数据确认后再全面铺开 |
| **新落地页质量参差不齐** | 中 | 中 | 统一 CRO 模板 + 上线前 QA checklist |
| **注册→付费率提升困难** | 高 | 高 | 优先优化 Onboarding + Paywall 策略，非单纯靠流量驱动 |
| **扩量页面被判定低质量** | 中 | 中 | 每篇页面必须有独特价值（非模板套壳），参考 PSEO 质量标准 |

---

## 🎯 KR1 — 收录率与排名优化

> **目标**：收录率55%，收录页面破1w；首页曝光占比95%→75%；Top10 1806→2100；Top10-20 3429→3800；Top20-50 4156→4400

### 战术拆解

#### T1.1 首页曝光占比稀释（95% → 75%）

| Task | Owner | Week | 产出 | 预期效果 |
|------|-------|------|------|----------|
| **启动 PSEO Phase 1**：4模板×5篇=20篇验证页 | Content+SEO | W1-W2 | 20篇 landing page 上线 | +20新页面分流首页曝光 |
| **启动 PSEO Phase 2**：P0 20个 niche × 4模板 = 80篇 | Content+SEO | W3-W6 | 80篇 landing page 上线 | +80新页面，首页曝光占比降至~85% |
| **启动 PSEO Phase 3**：P1 40个 niche × 主要模板 = 60篇 | Content+SEO | W7-W12 | 60篇 landing page 上线 | +60新页面，首页曝光占比降至~75% |
| **Glossary 批量上线**：ai-design-terms + design-terms 2篇 → 扩展至10篇 | Content | W3-W8 | 10篇 glossary | 长尾词覆盖 |
| **Resource 页面扩展**：现有3篇 → 扩至8篇 | Content | W5-W10 | 5篇 resource | 长尾词覆盖 |

**合计新增页面**：20+80+60+10+5 = **175篇**

#### T1.2 收录率提升（→ 55%）

| Task | Owner | Week | 产出 | 预期效果 |
|------|-------|------|------|----------|
| **Sitemap 优化**：确保所有新页面自动进入 sitemap | Dev | W1 | 更新 sitemap 生成逻辑 | 收录速度提升 |
| **内链结构化**：按 Silo Structure 为所有新页面配置内链 | Content+SEO | W2-W12 | 每篇至少3条上下文内链 | 爬虫深度优化 |
| **Google Indexing API 推送**：新页面上线24h内推送 | Dev | W1-W12 | 自动化推送脚本 | 收录速度提升2-3x |
| **死链/404 排查**：全站链接健康检查 | Dev | W1-W2 | 修复所有404 | 收录率提升 |
| **Canonical 规范化**：检查所有页面 canonical 标签 | Dev | W2-W3 | 无重复收录问题 | 收录质量提升 |

#### T1.3 排名区间提升

| 排名区间 | 当前 | 目标 | 差额 | 策略 |
|----------|------|------|------|------|
| **Top 10** | 1,806 | 2,100 | +294 | 优化已有Top 10-20关键词→推入Top 10 |
| **Top 10-20** | 3,429 | 3,800 | +371 | 新建 Tools + PSEO 页面抢占新关键词 |
| **Top 20-50** | 4,156 | 4,400 | +244 | PSEO长尾词 + Glossary大规模铺量 |

| Task | Owner | Week | 产出 |
|------|-------|------|------|
| **Top 10-20 → Top 10 提升**：筛选100个排名11-20的关键词，逐页优化TDK+内容+内链 | SEO | W3-W8 | 100篇页面优化 |
| **竞品非品牌词 Top 10 攻占**：定位竞品核心非品牌词（见KR3），创建对比/替代页面 | Content+SEO | W3-W10 | 20-30篇对比页 |
| **长尾词批量覆盖**：PSEO Phase 2-3 的长尾关键词自动匹配 | Content+SEO | W4-W12 | 140篇自动覆盖 |

---

## 🎯 KR2 — Tools 页面矩阵扩建（50+）

> **目标**：新增 Tools 50+页面，总点击提升至10,000，CTR提升至3%

### 现有 Tools 盘点（7篇 Docs）

| 现有页面 | 类别 |
|----------|------|
| AI Image Generator (Nano Banana Pro & Flux 2) | 图片生成 |
| AI Video Generator (Sora 2, Veo 3 & Kling) | 视频生成 |
| Canvas Guide — Shapes, Masks & Layout Grids | Canvas |
| Canvas Guide — Upload Images, Videos & Use Frames | Canvas |
| Canvas Tools — Touch Edit, Smart Select & Hand Tool | Canvas |
| ChatCanvas Vector Tools — Pencil (B) & Pen (P) | Canvas |
| Text Tool Guide — Headlines, Labels & AI Typography | 文字 |

**缺口**：现有7篇被归类为 "Docs/Help" 而非独立 SEO 优化的 Tools 页面。需要补建43+篇。

### 战术拆解

#### T2.1 Tools 页面架构设计（3层结构）

```
/tools/                          ← Tools Hub（聚合页）
  ├── /tools/ai-image-generator/   ← 已有，需SEO优化
  ├── /tools/ai-video-generator/   ← 已有，需SEO优化
  ├── /tools/ai-logo-maker/        ← 新建
  ├── /tools/ai-mockup-generator/  ← Landing已有，迁移
  ├── /tools/ai-banner-maker/      ← Landing已有，迁移
  ├── /tools/ai-poster-generator/  ← Landing已有，迁移
  ├── /tools/ai-flyer-maker/       ← Landing已有，迁移
  ├── /tools/ai-menu-design/       ← Landing已有，迁移
  ├── /tools/ai-business-card/     ← Landing已有，迁移
  ├── /tools/ai-infographic/       ← Landing已有，迁移
  ├── /tools/ai-avatar-generator/  ← Landing已有，迁移
  ├── /tools/ai-photo-enhancer/    ← Landing已有，迁移
  ├── /tools/ai-upscaler/          ← Landing已有，迁移
  ├── /tools/ai-background-remover/   ← 新建
  ├── /tools/ai-text-to-speech/    ← Landing已有，迁移
  ├── /tools/ai-voice-generator/   ← Landing已有，迁移
  ├── /tools/ai-tshirt-design/     ← Landing已有，迁移
  ├── /tools/ai-interior-design/   ← Landing已有，迁移
  ├── /tools/ai-stock-photo/       ← Landing已有，迁移
  ├── /tools/ai-video-upscaler/    ← Landing已有，迁移
  ├── /tools/ai-video-translation/ ← Landing已有，迁移
  ├── /tools/ai-photo-to-cartoon/  ← Landing已有，迁移
  ├── /tools/ai-resume-maker/      ← Landing已有，迁移
  ├── /tools/ai-expand-tool/       ← 新建
  ├── /tools/ai-remove-object/     ← 新建
  ├── /tools/ai-mockup-tool/       ← 新建
  ├── /tools/ai-social-media/      ← 新建（聚合）
  ├── /tools/ai-thumbnail-maker/   ← 新建
  ├── /tools/ai-brand-kit/         ← 新建
  ├── /tools/ai-color-palette/     ← 新建
  ├── /tools/ai-font-pairing/      ← 新建
  ├── /tools/ai-design-templates/  ← 新建
  ├── /tools/nano-banana/          ← 新建（产品子品牌页）
  ├── /tools/veo-3/                ← 新建（竞品词攻占）
  ├── /tools/sora-2/               ← 新建（竞品词攻占）
  ├── /tools/kling-ai/             ← 新建（竞品词攻占）
  ├── /tools/ai-video-ad-generator/ ← 新建
  ├── /tools/ai-instagram-post/    ← 新建
  ├── /tools/ai-youtube-thumbnail/ ← 新建
  ├── /tools/ai-linkedin-banner/   ← 新建
  ├── /tools/ai-email-header/      ← Landing已有，迁移
  ├── /tools/ai-product-photo/     ← 新建
  ├── /tools/ai-logo-generator/    ← 新建
  ├── /tools/ai-image-to-image/    ← 新建
  └── /tools/ai-video-to-video/    ← Landing已有，迁移
```

**总计**：7篇现有 + 约25篇 Landing 迁移/改造 + 约20篇新建 = **52篇**

#### T2.2 分批执行计划

| Phase | 任务 | Owner | Week | 数量 | 累计 |
|-------|------|-------|------|------|------|
| **Phase 1** | Landing页迁移至/tools/：ai-mockup-generator, ai-banner-maker, ai-poster-generator, ai-flyer-maker, ai-menu-design, ai-business-card, ai-infographic, ai-avatar-generator, ai-photo-enhancer, ai-upscaler | Content+Dev | W1-W2 | 10篇 | 17 |
| **Phase 2** | 继续迁移：ai-text-to-speech, ai-voice-generator, ai-tshirt-design, ai-interior-design, ai-stock-photo, ai-video-upscaler, ai-video-translation, ai-photo-to-cartoon, ai-resume-maker, ai-email-header, ai-video-to-video | Content+Dev | W2-W3 | 11篇 | 28 |
| **Phase 3** | 新建竞品词Tools：nano-banana, veo-3, sora-2, kling-ai | Content | W3-W4 | 4篇 | 32 |
| **Phase 4** | 新建场景词Tools：ai-background-remover, ai-expand-tool, ai-remove-object, ai-social-media, ai-thumbnail-maker, ai-youtube-thumbnail, ai-instagram-post, ai-linkedin-banner | Content | W4-W6 | 8篇 | 40 |
| **Phase 5** | 新建品牌词Tools：ai-brand-kit, ai-color-palette, ai-font-pairing, ai-design-templates, ai-product-photo, ai-logo-generator, ai-image-to-image | Content | W6-W8 | 7篇 | 47 |
| **Phase 6** | 新建意图词Tools：ai-video-ad-generator, ai-mockup-tool + Tools Hub首页 | Content+Dev | W8-W10 | 3篇 | **50** |
| **Phase 7** | 补充工具：ai-3d-model, ai-svg-generator, ai-presentation, ai-comic-maker, ai-sticker-maker | Content | W10-W12 | 5篇 | **55** |

#### T2.3 Tools 页面 SEO 规范

每篇 Tools 页面必须包含：

```yaml
TDK:
  T: "{Tool Name} — Free AI {Category} Generator | Lovart"
  D: "Create professional {result} in seconds with Lovart's AI {Tool Name}. No design skills needed. Free to try."
  K: "{tool_name}, ai {tool_type}, free ai {tool_type}, {tool_type} online, {tool_type} generator"

页面结构:
  1. Hero (H1 + 一句话价值主张 + CTA)
  2. 操作步骤（3步: Describe → Generate → Download）
  3. Before/After 展示（关键转化元素）
  4. Use Cases（3个场景卡片）
  5. Features（3-4个功能亮点）
  6. 对比表（vs 竞品/传统方式）
  7. FAQ（5个预埋长尾问题）
  8. CTA（免费试用）

内链规则:
  - 每个Tools页面 → Tools Hub（/tools/）
  - 每个Tools页面 → 相关博客文章（2-3篇）
  - 每个Tools页面 → 相关Landing页（1-2个）
  - Tools Hub → 所有子页面（分类排列）
```

#### T2.4 Tools CTR 提升路径（→ 3%）

| 措施 | Week | 预期CTR提升 |
|------|------|------------|
| **Meta Description 重写**：包含 "Free" + 价值承诺 | W1-W3 | +0.5pp |
| **结构化数据**：添加 HowTo/SoftwareApplication Schema | W2-W3 | +0.3pp |
| **页面速度优化**：Tools 页面 Core Web Vitals 达标 | W4-W6 | +0.2pp |
| **Rich Snippet 优化**：FAQ schema（已在模板中包含） | W2-W3 | +0.5pp |
| **标题A/B测试**：Top 10 Tools 页标题进行 GSC A/B | W6-W12 | +0.5pp |

---

## 🎯 KR3 — 非品牌词占比提升 + 竞品覆盖

> **目标**：GSC曝光量230k→280k，非品牌词点击占比4%→30%，竞品核心非品牌词覆盖80%+

### 战术拆解

#### T3.1 竞品非品牌词覆盖矩阵

**优先级 P0 — 高搜索量竞品词（点击率 <3%）**

| 竞品词 | GSC展示 | 当前排名 | 策略页面 | Owner | Week |
|--------|---------|---------|----------|-------|------|
| **luma dream machine** | 1,402/周 | 8.7 | `/tools/ai-video-generator/` 优化 + `/blog/lovart-vs-luma-dream-machine/` | Content | W2-W4 |
| **hedra ai** | 1,259/周 | 6.6 | `/blog/lovart-vs-hedra-ai/` + Landing页优化 | Content | W2-W4 |
| **veo 3.1** | 418/周 | 9.1 | `/tools/veo-3/` 新建独立工具页 | Content | W3-W4 |
| **veo ai free** | 390/周 | 8.6 | `/tools/ai-video-generator/` 优化 | Content+SEO | W3-W4 |
| **midjourney editing** | 待查 | — | `/blog/lovart-vs-midjourney-editing/` | Content | W5-W6 |
| **canva ai alternative** | 待查 | — | `/blog/canva-vs-lovart/` 已规划，推进 | Content | W5-W6 |
| **sora 2 free** | 待查 | — | `/tools/sora-2/` 新建独立工具页 | Content | W4-W5 |
| **kling ai free** | 待查 | — | `/tools/kling-ai/` 新建独立工具页 | Content | W4-W5 |

**优先级 P1 — 中等搜索量竞品词**

| 竞品词簇 | 目标词数量 | 覆盖策略 | Week |
|----------|-----------|----------|------|
| **Leonardo AI** | 10-15词 | `/blog/lovart-vs-leonardo/` + 功能对比表 | W6-W8 |
| **PixAI** | 8-12词 | `/blog/lovart-vs-pixai/` | W6-W8 |
| **Recraft AI** | 6-10词 | `/blog/lovart-vs-recraft/` | W8-W10 |
| **Ideogram AI** | 6-10词 | `/blog/lovart-vs-ideogram/` | W8-W10 |
| **Adobe Firefly** | 10-15词 | `/blog/adobe-firefly-alternative/` | W8-W10 |

**总计竞品覆盖目标**：P0 8个竞品 + P1 5个竞品 = **13个竞品**，覆盖核心非品牌词 **80+个**

#### T3.2 非品牌词增长引擎

```
非品牌词增量来源:
  ├── 引擎1: 竞品对比页面（8-15篇）       → 预计贡献 +1,500点击/月
  ├── 引擎2: Tools独立页面（50+篇）        → 预计贡献 +3,000点击/月
  ├── 引擎3: PSEO长尾页面（175篇）         → 预计贡献 +2,000点击/月
  ├── 引擎4: 博客How-to/对比文章           → 预计贡献 +1,500点击/月
  └── 引擎5: i18n本地化页面（45篇）        → 预计贡献 +500点击/月
                                  合计 → +8,500点击/月
```

#### T3.3 GSC 曝光量提升路径（230k → 280k）

| 策略 | 预期曝光增量 | Week |
|------|-------------|------|
| **PSEO Phase 1-3**（175篇新页面） | +20,000 | W2-W12 |
| **Tools 50+页面**（43篇新建） | +15,000 | W2-W12 |
| **竞品对比页面**（13篇） | +8,000 | W4-W10 |
| **现有页面TDK优化**（100篇Top 10-20关键词优化） | +5,000 | W3-W8 |
| **i18n首波页面**（9语言×5页=45页） | +5,000 | W8-W12 |
| **博客新发布**（按内容日历） | +5,000 | W2-W12 |
| **合计** | **+58,000** | — |

#### T3.4 i18n 本地化首波计划

| 语言 | 优先级 | 首波页面 | Week | 依据 |
|------|--------|----------|------|------|
| **法语 (fr)** | P0 | 5页（首页片段+Tools×3+博客×1） | W8-W9 | 29 queries/285 impressions, CTR 37% |
| **俄语 (ru)** | P0 | 5页 | W8-W9 | 35 queries/151 impressions, CTR 48% |
| **日语 (ja)** | P0 | 5页 | W9-W10 | 24 queries/121 impressions, CTR 42% |
| **简中 (zh)** | P1 | 5页 | W9-W10 | 51 queries/258 impressions, CTR 16% |
| **韩语 (ko)** | P1 | 5页 | W10-W11 | 5 queries, but high CTR |
| **德语 (de)** | P1 | 5页 | W10-W11 | 2 queries, 12 impressions |
| **阿拉伯语 (ar)** | P2 | 5页 | W11-W12 | 已在 unmatched 中有品牌流量 |
| **葡语 (pt)** | P2 | 5页 | W11-W12 | 1 query, but growth potential |
| **意语 (it)** | P2 | 5页 | W11-W12 | 1 query, 24 impressions |

---

## 📅 12周执行日历总表

### Phase 1: 基础建设（W1-W2）

| Week | KR | Task | Owner | 产出 |
|------|-----|------|-------|------|
| W1 | KR1 | PSEO Phase 1 启动：4模板×5篇=20篇上线 | Content | 20篇新页面 |
| W1 | KR1 | Sitemap优化 + Google Indexing API接入 | Dev | 收录速度提升 |
| W1 | KR2 | Tools Phase 1: 10篇Landing→/tools/迁移 | Content+Dev | 10篇Tools上线 |
| W2 | KR1 | 死链/404全站排查修复 | Dev | 收录率提升 |
| W2 | KR2 | Tools Phase 2: 11篇Landing迁移 | Content+Dev | Tools累计28篇 |
| W2 | KR3 | luma dream machine + hedra ai 对比页启动 | Content | 2篇竞品页 |

### Phase 2: 内容放量（W3-W6）

| Week | KR | Task | Owner | 产出 |
|------|-----|------|-------|------|
| W3 | KR1 | PSEO Phase 2 启动：20 niche × 4模板 = 80篇 | Content | 80篇新页面 |
| W3 | KR1 | Top 10-20关键词优化启动（首批50篇） | SEO | 排名提升 |
| W3 | KR2 | Tools Phase 3: 4篇竞品词Tools（veo-3, sora-2, kling, nano-banana） | Content | Tools累计32篇 |
| W3 | KR3 | veo 3.1 / veo ai free 独立页上线 | Content | 2篇竞品工具页 |
| W3 | KR1 | Canonical规范化全站检查 | Dev | 收录质量 |
| W4 | KR2 | Tools Phase 4: 8篇场景词Tools | Content | Tools累计40篇 |
| W4 | KR3 | 竞品对比页：midjourney editing + canva alternative | Content | 2篇对比页 |
| W5 | KR1 | Glossary 扩展（3→6篇） | Content | +3篇glossary |
| W5 | KR3 | 竞品对比页：sora 2 + kling ai 对比页 | Content | 2篇对比页 |
| W6 | KR2 | Tools Phase 5: 7篇品牌词Tools | Content | Tools累计47篇 |
| W6 | KR3 | 竞品对比页：leonardo + pixai 启动 | Content | 2篇对比页 |

### Phase 3: 深度扩展（W7-W10）

| Week | KR | Task | Owner | 产出 |
|------|-----|------|-------|------|
| W7 | KR1 | PSEO Phase 3: 40 niche × 主要模板 = 60篇 | Content | 60篇新页面 |
| W7 | KR1 | Top 10-20关键词优化（第二批50篇） | SEO | 排名提升 |
| W8 | KR2 | Tools Phase 6: Tools Hub首页 + 3篇意图词 | Content+Dev | Tools累计**50篇** ✅ |
| W8 | KR3 | 竞品对比页：recraft + ideogram + firefly | Content | 3篇对比页 |
| W8 | KR3 | i18n 首波：法语 + 俄语 各5页 | Content | 10篇本地化页 |
| W9 | KR3 | i18n 首波：日语 + 简中 各5页 | Content | 10篇本地化页 |
| W9 | KR1 | Glossary 扩展（6→10篇） | Content | +4篇glossary |
| W10 | KR2 | Tools Phase 7: 补充5篇 | Content | Tools累计**55篇** |
| W10 | KR1 | Resource 页面扩展（3→8篇） | Content | +5篇resource |
| W10 | KR3 | i18n 首波：韩语 + 德语 各5页 | Content | 10篇本地化页 |

### Phase 4: 收尾与优化（W11-W12）

| Week | KR | Task | Owner | 产出 |
|------|-----|------|-------|------|
| W11 | KR3 | i18n 首波：阿拉伯语 + 葡语 + 意语 各5页 | Content | 15篇本地化页 |
| W11 | KR1 | 全站内链审计：确保 Silo Structure 闭环 | SEO | 内链健康 |
| W12 | KR2 | Tools 页面 CTR 优化：Schema + Meta A/B 分析 | SEO | CTR提升 |
| W12 | ALL | Q3 数据复盘：GSC/收录/排名/CTR 逐项核验 | ALL | 复盘报告 |

---

## 📊 预期效果模拟

### 页面数量增长

| 页面类型 | 当前 | Q3新增 | Q3末累计 |
|----------|------|--------|----------|
| Landing/Core Pages | ~55 | 0 | ~55 |
| Tools Pages | 7 | +48 | **55** |
| PSEO Pages | 0 | +160 | **160** |
| Blog 新文章 | ~50+ | +15 | ~65+ |
| Glossary | 2 | +8 | **10** |
| Resource | 3 | +5 | **8** |
| 竞品对比页 | 0 | +13 | **13** |
| i18n 本地化页 | 0 | +45 | **45** |
| **合计** | **~117** | **+294** | **~411** |

### 非品牌词点击占比变化

| 来源 | 当前月点击占比 | Q3末月点击占比 |
|------|--------------|---------------|
| 品牌词（lovart + 变体） | ~97.8% | ~70-75% |
| 非品牌词 — Tools 页 | ~0% | ~8-10% |
| 非品牌词 — PSEO 长尾 | ~0% | ~5-8% |
| 非品牌词 — 竞品对比 | ~0.5% | ~5-7% |
| 非品牌词 — 博客/Glossary | ~1.7% | ~5-8% |
| **非品牌词合计** | **~2.2%** | **~25-30%** |

**保守估计** Q3末非品牌词占比可达 **20-25%**，Q4持续优化后达到 **30%**。

---

## ⚠️ 关键风险与应对

| 风险 | 概率 | 影响 | 应对 |
|------|------|------|------|
| **PSEO内容被判定低质量** | 中 | 高 | Phase 1先验证20篇，通过GSC数据确认搜索引擎接受度后再放量 |
| **收录速度跟不上生产速度** | 中 | 中 | 接入Google Indexing API + sitemap自动ping |
| **i18n翻译质量不佳** | 中 | 中 | P0语言（法/俄/日）人工审核，P1-2用AI初译+人工校对 |
| **Tools页面内链过弱** | 高 | 中 | 从首页/Tools Hub/博客建立强力内链网络 |
| **非品牌词排名周期长** | 高 | 中 | 重点攻坚已有排名的词（11-20位），新词需接受3-6个月爬坡 |

---

## 🔧 资源需求

| 角色 | 投入 | 说明 |
|------|------|------|
| **Content（内容生产）** | 全职 | PSEO模板填充 + Tools页面撰写 + 博客文章 |
| **SEO（策略+执行）** | 0.5全职 | TDK优化 + 排名监控 + GSC数据周报 |
| **Dev（技术）** | 0.3全职 | Sitemap/Indexing API/Canonical/Tools Hub页面 |
| **Design（设计）** | 按需 | Tools页面配图（Before/After展示） |
| **i18n（翻译）** | 按需 | AI翻译 + P0语言人工审核 |

---

*本计划基于2026-06-07数据基线编制，建议每周五根据GSC数据review进度并动态调整优先级。*
