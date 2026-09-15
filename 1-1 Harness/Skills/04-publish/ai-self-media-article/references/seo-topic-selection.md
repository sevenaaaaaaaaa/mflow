# SEO 驱动的选题流程

## 数据源位置

所有 SEO 数据在 Obsidian vault（iCloud 同步）：

```
~/Library/Mobile Documents/iCloud~md~obsidian/Documents/LifeOS Pro PARA Vault/1-Project/
├── 1-2 Insight/
│   ├── Keywords Research/
│   │   ├── SEO Report/
│   │   │   ├── annual/Lovart 关键词终极洞察.md          ← 关键词全景
│   │   │   └── 品牌词非品牌词_May_W1-W4_趋势分析.md    ← 品牌vs非品牌趋势
│   │   ├── SERP Copy Intelligence/
│   │   │   ├── global-en-competitor-landscape-2026-06.md ← 竞品格局
│   │   │   └── global-en-serp-copy-research-2026-06.md   ← SERP 文案研究
│   │   └── Weekly Raw Data/ / Daily Raw Data/            ← GSC/Bing 原始 CSV
│   ├── Trident Insights/
│   │   ├── 竞品核心非品牌词/
│   │   │   ├── lovart_competitors_core_keywords.md       ← 36 核心竞品词
│   │   │   └── lovart_competitors_keywords.md            ← 265 全量竞品词
│   │   └── reports/
│   │       ├── topics/Lovart-SEO-topic-competitor-YYYY-MM.md  ← 竞品词覆盖月报
│   │       ├── monthly/Lovart-SEO-YYYY-MM.md                 ← 月度 SEO 报告
│   │       └── weekly/Lovart-SEO-review-*.md                 ← 周报
│   └── From Datawork/seo_geo_daily_report_YYYYMMDD.csv   ← DataWorks 日报
├── 1-3 Content Gen/
│   └── Content Strategy/
│       ├── Lovart-内容策略-内容日历与关键词布局方案.md     ← 内容策略全景
│       └── 12-公式化变体程序化SEO落地计划.md               ← 程序化 SEO
└── 1-4 Geo Dev/scripts/                                  ← SEO 自动化脚本
```

本地开发目录（working copies / temp data）：
```
~/Documents/Lovart Local Dev/
├── 1-3-content-temp/
│   ├── Refresh-Page/landing-examples/keyword-manifest.json  ← 41 个关键词落地页清单
│   ├── content-calendar-priority-queue-2026-06.csv           ← 内容日历优先队列
│   └── blog-published-index-2026-06.csv                      ← 已发布 160 篇博客索引
└── article-images/                                          ← 文章配图下载目录
```

## 选题决策树

```
1. 读取竞品核心非品牌词清单 → 找到 🟢 低竞争关键词
2. 对照 §8.5「未覆盖核心竞品词」→ 确认该词 Google 零排名
3. 检查该词是否与 Lovart 产品功能直接关联
4. 检查该词是否有足够搜索量（月展示 > 1000）
5. 如果同时满足：低竞争 + 零排名 + 产品关联 + 有搜索量 → 选题成立
```

## 关键指标解读

| 指标 | 含义 | 选题阈值 |
|------|------|---------|
| 竞争度 | 🟢低/🟡中/🔴高 | 选 🟢 或 🟡 |
| Google 排名 | 当前在 SERP 的位置 | 排名 > 10 或零排名 = 机会 |
| 展示量 | GSC 中的曝光次数 | > 1000/月 = 有搜索需求 |
| CTR | 点击/展示 | < 20% = 内容匹配差，有优化空间 |
| 品牌词/非品牌词占比 | 流量结构 | 非品牌词 < 6% = 需要发力非品牌词 |

## 2026-06 确认的高机会关键词

来自 §8.5 未覆盖核心词（Google 零排名）+ 竞品核心非品牌词：

| 关键词 | 竞争度 | 产品关联 | 推荐选题方向 |
|--------|--------|---------|-------------|
| **Character Consistency** | 🟢低 | Brand Kit 2.0 + Style Consistency | 🔴 最佳：横评 6 种方案 |
| AI Ad Generator | 🟢低 | Lovart 广告素材生成 | 电商广告素材自动化 |
| AI Commercial | 🟢低 | Lovart 商业视频 | AI 商业视频制作指南 |
| Brand Video | 🟢低 | Lovart 品牌视频 | 品牌视频一致性方案 |
| UGC Generator | 🟢低 | Lovart 社媒素材 | UGC 风格内容批量生成 |
| Talking Avatar | 🟢低 | （弱关联） | 需要找到切入点 |
| Lip Sync | 🟢低 | （弱关联） | 需要找到切入点 |

## 自媒体文章 → SEO 外链的闭环

```
自媒文章（知乎/掘金/Medium 等）
    ↓ 包含关键词 "character consistency"
    ↓ 自然链接到 lovart.ai/character-consistency
    ↓ 被 Google 索引
    ↓ 填补该关键词的零排名空白
    ↓ 带来非品牌词流量（当前仅 5.28%，目标提升）
```
