---
name: lovart-sentinel
description: Lovart 品牌声誉舆情监测系统 — 每日自动采集多渠道数据，生成符合企业级标准的7板块品牌声誉舆情报告。
---

# lovart-sentinel

## 路径契约

| 层 | 路径 |
|----|------|
| 文档 SSOT | `1-1 GEO Readme/` |
| Sanity 脚本 | `1-4 Dev/lovart.sanity.studio/scripts/` |
| SEO/Sentinel 脚本 | `1-4 Dev/scripts/` |
| 自动化 | `1-4 Dev/automation/` |
| 本 Skill | `1-1 Harness/Skills/lovart-sentinel/SKILL.md` |

Lovart 品牌声誉舆情监测系统 — 每日自动采集多渠道数据，生成符合企业级标准的7板块品牌声誉舆情报告。

## Triggers

- "生成舆情报告" / "generate sentiment report"
- "run sentinel" / "运行哨兵"
- "品牌舆情" / "brand monitoring"
- "每日舆情" / "daily sentiment"
- "Lovart 品牌分析" / "Lovart brand analysis"

## Workflow

### Phase 0: 本地数据采集

```bash
cd "1-Project/Lovart" && python3 scripts/sentinel/daily.py
```

自动采集 4 个本地源：GSC CSV / SEO周报 / 邮件复盘 / 内容产出。
并生成委托指令供后续 webfetch 使用。

### Phase 1: 远程实时采集 (并行 ~18 条 webfetch)

#### 搜索引擎 SERP (5条)

| # | URL | 用途 |
|---|-----|------|
| 1 | `https://www.bing.com/search?q=lovart+ai` | Bing SERP + 寄生域名 |
| 2 | `https://www.baidu.com/s?wd=lovart+ai` | 百度SERP + 竞品广告 + 相关搜索 |
| 3 | `https://www.sogou.com/web?query=lovart+ai` | 搜狗SERP + 微信文章 |
| 4 | `https://www.bing.com/search?q=site:36kr.com+OR+site:techcrunch.com+OR+site:theverge.com+OR+site:geekpark.com+lovart+ai` | 🆕 媒体库轮询 |
| 5 | `https://www.bing.com/search?q=lovart+ai+site:douyin.com+OR+site:weibo.com` | 🆕 抖音/微博 |

#### 社交媒体 API (4条)

| # | URL | 用途 |
|---|-----|------|
| 6 | `https://api.fxtwitter.com/lovart_ai` | X/Twitter |
| 7 | `https://www.linkedin.com/company/lovart-ai` | LinkedIn |
| 8 | `https://duckduckgo.com/html/?q=lovart.ai+site:instagram.com` | 🆕 Instagram via DDG |
| 9 | `https://duckduckgo.com/html/?q=lovart+site:tiktok.com` | 🆕 TikTok via DDG |

#### 评价与社区 (3条)

| # | URL | 用途 |
|---|-----|------|
| 10 | `https://www.producthunt.com/products/lovart/reviews` | PH 评价 |
| 11 | `https://duckduckgo.com/html/?q=lovart+site:reddit.com` | Reddit 社区 |
| 12 | `https://duckduckgo.com/html/?q=lovart+site:youtube.com` | YouTube |

#### 中国生态 (3条)

| # | URL | 用途 |
|---|-----|------|
| 13 | `https://www.baidu.com/s?wd=lovart+ai+%E5%B0%8F%E7%BA%A2%E4%B9%A6+%E5%BE%AE%E4%BF%A1+%E7%9F%A5%E4%B9%8E` | 小红书/微信/知乎 |
| 14 | `https://www.sogou.com/web?query=lovart+site:weibo.com` | 🆕 微博 via 搜狗 |
| 15 | `https://www.bing.com/search?q=site:dribbble.com+OR+site:behance.net+OR+site:figma.com+lovart` | 🆕 设计社区 |

#### 竞品监控 (3条)

| # | URL | 用途 |
|---|-----|------|
| 16 | `https://www.bing.com/search?q=canva+ai+new+features+2026` | 竞品动态 |
| 17 | `https://www.bing.com/search?q=best+ai+design+tools+2026` | 市场排名文章 |
| 18 | `https://www.baidu.com/s?wd=AI%E8%AE%BE%E8%AE%A1%E5%B7%A5%E5%85%B7+%E6%8E%A8%E8%8D%90+2026` | 中文AI设计市场 |

### Phase 2: 数据解析

每个 webfetch 返回后，Agent 需提取结构化数据。解析函数位于 `sources/*.py` 各自的 `parse_*()` 中。

**关键提取字段**：
- Bing SERP → 前10域名 + 寄生域名位置/跳转 + 友方域名
- 百度 SERP → 相关搜索词 + 竞品广告检测 + 百度百科存在性
- 搜狗 SERP → 首条域名 + 微信公众号文章
- 社媒 → 粉丝数/互动量/最新内容日期/与上期对比变化
- 评价 → 评分/评价数/距上次评价天数
- 媒体库 → 报道标题/日期/来源/情感倾向（正/中/负）
- 抖音/微博 → 提及数量/话题标签/KOL信号

### Phase 3: 🆕 情感量化分析

在 Phase 2 提取的原始数据基础上，对每条提及执行 **6层复合情感量化**（无需NLP模型）：

| 层级 | 方法 | 输出 |
|------|------|------|
| 1. 规则引擎 | 正向/负向词典匹配 + 否定词翻转 + 程度词缩放 | -100~+100分数 |
| 2. 平台信号 | PH评分/社媒互动率/搜索CTR/寄生域名数量 | 平台原生情感代理 |
| 3. 竞品基准 | Lovart vs Canva/Midjourney 同渠道情感对比 | 相对情感定位 |
| 4. 多维标签 | 功能/价格/服务/对比/信任/易用 6维度归类 | 维度级情感热力图 |
| 5. 时序漂移 | 本周期vs上周期情感分布变化 | 情感拐点检测 |
| 6. 弱信号 | 互动衰减/中性率上升/竞品提及率/提问→抱怨反转 | 负面爆发前预警 |

### Phase 4: 报告生成

```bash
cd "1-Project/Lovart" && python3 scripts/sentinel/report.py --date $(date +%Y-%m-%d)
```

## 报告结构 (7板块 + 可视化方案)

每个板块设计了对应的图表类型和布局位置，详见 `references/visual-plan.md`。

| 板块 | 图表类型 | 位置 |
|------|---------|------|
| **文章总览** | KPI大数字卡片（3×3矩阵）| 第1页顶部 |
| **一、摘要与核心发现** | 三列Agent摘要框（SERP/Social/Insight）| 紧随KPI卡片 |
| **二、品牌声量与影响力** | 2.1.1折线图 + 2.1.2柱状/雷达图 + 2.1.3世界地图热力 | 分别嵌入各小节 |
| **三、关键事件回顾** | 3.1时间轴甘特图 + 3.2四阶段流程框 | 3.1上方 / 3.2各阶段前 |
| **四、情感态度分析** | 4.1双栏证据卡（正/负） + 4.2三层漏斗图 | 嵌入各小节 |
| **五、用户画像** | 5.1五列人群卡片 + 5.3用户旅程流程图 | 5.1上方 / 5.3上方 |
| **六、负面议题追踪** | 6.1.1寄生域名趋势对比表 + 6.1.3四层信任金字塔 | 嵌入各小节 |
| **七、结论与战略建议** | SWOT矩阵表 + 优先级时间线图 + 监测指标仪表盘 | 分节嵌入 |

**图表生成原则**：
- 趋势数据 → 折线图 | 多类对比 → 并列柱状图 | 关系结构 → 漏斗/金字塔 | 时间序列 → 时间轴
- 所有图表标注数据来源和采集时间
- 优先使用 Mermaid（代码生成→直接嵌入）或 Matplotlib（Python自动生成）
- 工具推荐参见 `references/visual-plan.md`

**GSC数据引用原则**：SEO搜索数据引用已有 `SEO周报_*.md` 和 `品牌词趋势分析.md`，不在舆情报告中重复提取GSC CSV。

## 告警触发规则

| 信号 | 阈值 | 动作 |
|------|------|------|
| 寄生域名进入 Bing 前 3 位 | position ≤ 3 | 法律团队通告 |
| 百度品牌词出现竞品广告 | 出现即触发 | 评估百度品牌专区投放 |
| 邮件送达率 < 85% | delivery_rate < 85 | 邮件团队排查 |
| 退订率 > 40/万 | unsub > 40 | 暂停高频发送 |
| PH 60 天无新评价 | days_since_review > 60 | 启动评价引导 |
| 新寄生域名出现 | new_domain_detected | 立即法律行动 |
| X 连续 7 天互动 < 1 赞/帖 | avg_engagement < 1 | 内容策略转向 |
| 互动率月环比下降 > 30% | engagement_velocity_drop > 0.3 | 🆕 隐性情感变冷预警 |
| 中性评价占比上升 > 15% | neutral_ratio_increase > 0.15 | 🆕 漠不关心预警 |
| 竞品提及率 > 25% | competitor_mention_ratio > 0.25 | 🆕 用户正在决策对比 |

## 报告路径

```
1-Project/
├── 1-2 Insight/Lovart ORM/        # 舆情报告产出（daily/weekly/monthly/quarterly/annual/raw）
│   ├── daily/Lovart-Sentinel-YYYY-MM-DD-daily.md
│   ├── weekly/Lovart-Sentinel-YYYY-MM-DD-weekly.md
│   └── raw/{date}/
├── 1-4 Dev/scripts/sentinel/
│   ├── config.yaml                  # 全量配置 (30+竞品 × 4维度)
│   ├── WORKFLOW.md                  # Agent 工作流 (18条 webfetch)
│   ├── daily.py                     # 每日入口
│   ├── collect.py                   # 编排器 (21 source)
│   ├── report.py                    # 7板块报告生成器
│   └── sources/                     # 21个数据源模块
│       ├── gsc_daily.py             ✅ 本地 CSV
│       ├── gsc_weekly.py            ✅ 本地 MD
│       ├── email_health.py          ✅ 本地 MD
│       ├── content_production.py    ✅ 本地扫描
│       ├── serp_bing.py             ⬜ webfetch
│       ├── serp_baidu.py            ⬜ webfetch 🆕
│       ├── serp_sogou.py            ⬜ webfetch 🆕
│       ├── social_x.py              ⬜ webfetch
│       ├── social_linkedin.py       ⬜ webfetch
│       ├── social_instagram.py      ⬜ webfetch 🆕
│       ├── social_tiktok.py         ⬜ webfetch 🆕
│       ├── social_youtube.py        ⬜ webfetch 🆕
│       ├── social_reddit.py         ⬜ webfetch 🆕
│       ├── china_shortvideo.py      ⬜ webfetch 🆕
│       ├── product_hunt.py          ⬜ webfetch
│       ├── ai_directories.py        ⬜ webfetch 🆕
│       ├── design_communities.py    ⬜ webfetch 🆕
│       ├── competitor_social.py     ⬜ webfetch 🆕
│       ├── media_polling.py         ⬜ webfetch 🆕
│       ├── propagation_tracker.py   ⬜ webfetch 🆕
│       └── sentiment_quantifier.py  ⬜ webfetch 🆕
│   └── references/
│       ├── report-structure.md      7板块结构说明
│       ├── data-sources.md          采集方法 + 列名映射
│       └── alert-rules.md           告警阈值 + 升级规则
```

## References

- `references/report-structure.md` — 7板块详细结构说明 + 图表嵌入位置
- `references/data-sources.md` — 21个数据源的采集方法、列名映射、解析逻辑
- `references/alert-rules.md` — 完整告警规则、阈值、响应机制 + 弱信号规则
- `references/visual-plan.md` — 🆕 12种图表的类型选择、布局位置、数据映射和工具推荐


## 预算（RULES-70 强制）

本 skill 产出同样受 RULES-70 数量预算约束。

- **必须**过质量门禁（post-write-check + geo-check）

- **禁止**绕过质量门禁直接发布
