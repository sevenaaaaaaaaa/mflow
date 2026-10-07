# Lovart SEO 内链优化全景方案

> **编制日期**：2026-06-16
> **数据基线**：2026年5月 GSC / GA4 / Sanity CMS
> **覆盖范围**：1,339 篇 EN 博客 + 273 个 Tools/Features 页 + GSC 关键词语料

---

## 一、已完成项

### 1.1 竞品词 Meta 优化（方向 A：修复 Review → Alternative）

| 指标 | 数值 |
|------|------|
| 优化博客数 | **60 篇** |
| Title 改法 | `XXX Review` → `XXX Alternative — Free AI XX + Design Agent \| Lovart` |
| Description 改法 | 竞品替代 + 免费 + 价值承诺 |
| 预期 CTR 提升 | 0.1-0.3% → 2-4% |
| 预期月增量 | +5,994 点击，+863 注册 |

**首批高价值词**：freepik ai（28K 展示）、flora ai（13K）、artlist ai（8.9K）、luma dream machine（5.7K）

### 1.2 新建竞品落地博客（方向 B：缺失关键词覆盖）

| 指标 | 数值 |
|------|------|
| 新建博客数 | **23 篇** |
| P0 竞品词 | Ideogram、Runway Gen-3、MiniMax、Remini、FaceApp |
| P1 竞品词 | Playground AI、NightCafe、VistaCreate、Descript、Opus Clip、Topaz AI |
| P2 竞品词 | Evoto、BeautyPlus、Facetune、Submagic、Crello、Luma Ray |
| GSC 缺口词 | Civitai（21.9K 展示）、SeaArt AI（18.9K）、Medeo（6.4K）、Deevid AI（4.6K）、ImageFX（3.2K）、Veed.io（3.1K） |
| 每篇结构 | Hero → CTA → 对比 → CTA + 交叉链接 |
| 发布日期 | 2025-11-20 至 2026-04-29，均匀分布 |

### 1.3 全局 CTA 链接升级

#### 第一阶段：清洗统一（1,332 → 1,332 篇）

| 指标 | 旧版 | 新版 |
|------|------|------|
| CTA 链接类型 | 全部指向首页 | 指向具体高表现落地页 |
| 首页指向比例 | 100% | 0% |
| 目标页数量 | 1 | 17 |

#### 第二阶段：重平衡（17 → 46 个目标）

| 指标 | 旧版 | 新版 |
|------|------|------|
| CTA 目标页 | 17 | **46** |
| Tools 页覆盖 | 7 | **21** |
| Features 页覆盖 | 4 | **22** |
| 单页最大链接数 | 270 | **74**（避免权重过度集中） |
| 高展示零内链页面 | 162 个 Tools + 104 个 Features | **大幅减少** |

#### CTA 类型（每篇 2 个）

1. **文字 CTA**：`"Lovart is the AI design agent trusted by 10M+ creators. [链接文案] →"`
2. **按钮 CTA**：结构化按钮，4 种样式（action / action-outline / ghost / link），指向具体落地页

### 1.4 博客交叉内链

#### 第一阶段：粗粒度（1,241 篇）

| 指标 | 数值 |
|------|------|
| 主题分类 | 5 个（design/image/video/brand/ecommerce） |
| 每篇交叉链接 | 2 篇同主题博客 |
| general:design 兜底 | 475 篇（35%） |

#### 第二阶段：细粒度升级（1,339 篇，替换第一版）

| 指标 | 数值 |
|------|------|
| 主题分类 | **40+ 个**细粒度标签 |
| 分类体系 | 6 个大类：content（内容类型）/ feature（功能）/ topic（AI Agent）/ type（文体）/ industry（行业）/ model（模型） |
| general:design 兜底 | 降至 120 篇（9%） |
| 模型词分组 | 20+ 组（seedance/veo/nano banana/kling/sora/flux/midjourney/runway/pika/luma/hailuo/firefly/leonardo/ideogram/recraft/pixai/freepik/seedream/minimax/civitai/seaart/openart） |
| 功能词分组 | 20+ 组（touch-edit/text-edit/bg-removal/upscaling/expand/mockup/batch/brand-kit/canvas/compare/export/prompting/layers/face/3d/animation/video-editing/subtitles/color/typography/composition/social-media/thumbnail/carousel/infographic/sticker） |
| 行业词分组 | 15+ 组（ecommerce/food/realestate/beauty/fitness/education/events/travel/healthcare/legal/agency/smb/photography/gaming/fashion） |
| 内容类型分组 | 15+ 组（logo/poster/banner/flyer/business-card/brochure/certificate/menu/album-cover/avatar/illustration/anime/clipart/wallpaper/product-photo） |

**交叉链接形式**：
```
Related [Topic]: [博客A标题] | [博客B标题]
```

---

## 二、内链架构总览

```
博客层级                    →  落地页层级
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1,339 篇 EN 博客
  ├── 每篇 2 个 CTA（文字+按钮）  →  46 个高表现 Tools/Features 页
  ├── 每篇 2 条交叉内链           →  同主题博客
  └── 每篇 Related 模块           →  同细粒度主题博客
                                   ━━━━━━━━━━━━━━━━━━━
落地页
  ├── 163 个 Tools 页
  ├── 108 个 Features 页  
  ├── 2 个 Landing 页
  └── Pricing / Canvas / Docs
```

### 内链权重分布

| 目标页 | 博客内链数 | 月展示（GSC） |
|--------|-----------|------------|
| `/features/ai-company-logo-maker` | 74 | ~9,000 |
| `/features/ai-brochure-design-tool` | 69 | ~4,000 |
| `/tools/ai-image-upscaler` | 67 | ~4,000 |
| `/tools/nano-banana-free` | 57 | ~658,913 |
| `/tools/text-to-image-generator` | 57 | ~686,896 |
| `/features/ai-carousel-generator` | 57 | ~2,439 |
| `/features/ai-design-agent` | 56 | ~4,240 |
| `/features/ai-business-card-maker` | 56 | ~3,004 |
| `/pricing` | 55 | ~658,913 |
| `/tools/ai-art-generator` | 54 | ~4,171 |
| `/features/ai-youtube-thumbnail-generator` | 40 | ~5,110 |
| `/features/album-cover-design` | 38 | ~2,610 |
| `/canvas` | 37 | ~594,671 |
| `/features/ai-instagram-post` | 37 | ~37 |
| `/features/magazine-layout-design` | 36 | ~14,583 |
| `/features/classroom-poster-design` | 36 | ~2,361 |
| `/tools/ai-background-generator` | 31 | ~2,383 |
| `/tools/ai-background-remover` | 30 | ~1,969 |
| 其余 28 个目标页 | 15-28 | 各 100-10,000 |

---

## 三、预期效果

### 3.1 量化预期

| 维度 | 优化前 | 优化后预期 | 提升幅度 |
|------|--------|-----------|---------|
| CTA 点击率（博客→落地页） | ~0.5% | ~2-3% | +300-500% |
| 落地页 UV（来自博客内链） | ~500/月 | ~3,000-5,000/月 | +500-900% |
| 非品牌词页面 CTR（Meta 优化） | 0.1-0.3% | 2-4% | +500-900% |
| 新增月度注册（Meta + CTA 综合） | — | +1,500-3,000 | — |
| 孤岛页面数（零内链） | 266 | 减少至 ~50 | ↓81% |

### 3.2 权重传递路径

```
博客交叉内链（同主题互相传递权重）
      ↓
博客 CTA 内链（传递到 Tools/Features 落地页）
      ↓
Tools/Features 页获得排名提升
      ↓
非品牌词 CTR 提升 → 点击量增长 → 注册转化增长
```

### 3.3 时间线

| 阶段 | 时间 | 预期变化 |
|------|------|---------|
| Meta 更新后 | 2-4 周 | GSC CTR 可见上升 |
| CTA 内链生效 | 4-8 周 | 落地页 UV 增长 |
| 交叉内链生效 | 6-12 周 | 博客间权重传递，长尾排名提升 |
| 综合效果 | Q3 末 | 非品牌词占比提升，注册转化提升 |

---

## 四、待推进项

### 4.1 P0（高优先级，1-2 周内）

| 动作 | 背景 | 预期效果 |
|------|------|---------|
| **首页 Social Proof 横幅** | 首页首屏缺少用户数/评分等信任元素 | 首页注册率 +1-2pp |
| **首页 Hero CTA 优化** | 当前 CTA 在页面中下部，首屏无直接注册入口 | 首屏注册点击率提升 |
| **注册流程简化** | Google 一键登录未置顶 | 注册流失率降低 |
| **热力图工具接入** | Hotjar/Clarity 定位用户行为流失点 | 数据驱动 CRO 决策 |

### 4.2 P1（中优先级，Q3 内）

| 动作 | 背景 | 预期效果 |
|------|------|---------|
| **Tools 页面 Phase 1 迁移** | Landing 页内容迁移至 /tools/ 目录 | 10-21 篇高意图页面 |
| **竞品 P0 词独立页** | luma/hedra/veo 已有排名，需独立页面承接 | CTR +2-3pp |
| **现有页面 Meta 优化** | veo3.1、hailuo 等 Tools 页 Title/Description 优化 | CTR +1-2pp |
| **Paywall 策略调整** | 免费额度用完后的付费触发点 | 注册→付费率 +0.2pp |
| **邮件 Drip Campaign** | 注册后 1/3/7/14 天自动邮件 | 长周期付费转化 |
| **博客→Tools 页精准内链** | 当前 CTA 覆盖 46 个目标页，还有 220+ 页面零内链 | 覆盖更多落地页 |
| **GA4 事件追踪** | 追踪 CTA 点击的转化漏斗 | 量化内链 ROI |

### 4.3 P2（Q4 或更远）

| 动作 | 背景 | 预期效果 |
|------|------|---------|
| **PSEO 批量生产（175 篇）** | CRO 模板验证后再铺量 | 非品牌词覆盖 |
| **i18n 本地化首波** | 9 种语言 × 5 页 = 45 页 | 多语言搜索流量 |
| **博客内容类型内链矩阵** | "Related:" 段落下增加更多交叉链接 | 深度语义关联 |
| **Tools 页面间内链** | Tools 页之间互相链接，形成主题集群 | 权重环形传递 |
| **Schema 结构化数据** | HowTo / SoftwareApplication / FAQ Schema | Rich Snippet 展示 +CTR |
| **多语言博客同步内链** | 非 EN 博客也复制内链策略 | 全球搜索流量 |

---

## 五、执行记录

| 日期 | 动作 | 数量 | 状态 |
|------|------|------|------|
| 6/13 | 落地页素材打标 | 200+ 文件 | ✅ |
| 6/13 | Sanity 素材批量替换 | 2,055 页，15,432 处 | ✅ |
| 6/14 | O2 OKR 规划写入战术计划 | 1 份 | ✅ |
| 6/14 | "Review"→"Alternative" Meta | 60 篇 | ✅ |
| 6/14 | 新建竞品 Alternative 博客 | 17 篇 | ✅ |
| 6/14 | 博客 CTA 链接升级（17 目标） | 1,332 篇 | ✅ |
| 6/15 | 新建 GSC 缺口竞品博客 | 6 篇 | ✅ |
| 6/15 | CTA 重平衡（17→46 目标） | 1,339 篇 | ✅ |
| 6/15-16 | 博客交叉内链（粗粒度） | 1,241 篇 | ✅ |
| 6/16 | 交叉内链细粒度升级 | 1,339 篇 | ✅ |

---

## 六、监控指标体系

| 指标 | 数据源 | 频率 |
|------|--------|------|
| 非品牌词 CTR | GSC | 每周 |
| 落地页 UV（来自内链） | GA4 — Referral > Blog | 每周 |
| CTA 点击率 | GA4 事件追踪 | 每周 |
| 新增注册/付费 | GA4 | 每月 |
| 孤岛页面数 | Sanity + GSC 交叉分析 | 每月 |
| 首页跳出率 | GA4 | 每周 |

---

*编制：Hermes Agent / 2026-06-16*
