# 报告产出标准

## 文件清单

单次 `run_all.sh` 产出 4 个文件：

```
1-6 Knowledge Base/Insight/Keywords Research/SEO Report/
├── gsc-full.json          ← GSC 全维度结构化数据
├── ga4-full.json          ← GA4 全维度结构化数据
├── bing-full.json          ← Bing 全维度结构化数据
└── intelligence-brief.md  ← 人类可读的 Markdown 情报摘要
```

## gsc-full.json 结构

```json
{
  "_date": "2026-05-29",
  "_site": "https://www.lovart.ai/",
  "keyword_tiers": [{ "label": "Top 3", "count": 3, "clicks": 294306, ... }],
  "top100_keywords": [{ "q": "lovart", "clicks": 135521, "impr": 439886, "ctr": 30.8, "pos": 1.0, "type": "brand" }],
  "country_keywords": { "usa": { "clicks": 16348, "queries": [...] } },
  "pages": { "indexed_count": 200, "top20_pages": [...] },
  "country_summary": [{ "country": "usa", "clicks": 16348, "ctr": 1.7, "pos": 7.8 }]
}
```

## ga4-full.json 结构

```json
{
  "_property": "properties/403618427",
  "_stream": "10524753059",
  "organic_daily": [{ "dims": {"date":"20260529"}, "metrics": {"sessions":"34081"} }],
  "organic_summary": { "sessions": 1623944, "users": 1014486, "avg_duration_sec": 431, ... },
  "user_segments": [{ "dims": {"newVsReturning":"returning"}, "metrics": {...} }],
  "geo_top10": [{ "country":"United States", "sessions":"249424", ... }],
  "trend_daily": { "recent": 31945, "prior": 34077, "change_pct": -6.3 },
  "trend_weekly": { ... },
  "trend_monthly": { ... }
}
```

## bing-full.json 结构

```json
{
  "_source": "Bing Webmaster API",
  "keywords": [{ "query": "lovart", "clicks": 1710, "impressions": 3500, ... }],
  "pages": [{ "url": "https://www.lovart.ai/", "clicks": 500, ... }],
  "crawl_daily": [{ "Date": "2026-05-30", "InIndex": 20877, "CrawlErrors": 700, ... }]
}
```

## intelligence-brief.md 标准

5 个部分，每部分有明确的数据来源：

1. **关键词对比: Google vs Bing** — 可横向对比的表格式展现
2. **Top 关键词** — 两平台 Top 10 并行展示 + 非品牌词 Top 5
3. **GA4 自然搜索全景** — 关键指标 + 环比趋势
4. **Bing 爬虫健康** — 索引/错误/拦截仪表盘
5. **核心洞察 + TODO** — 3 个数据驱动洞察，8 个优先级排序的 TODO

### 质量标准

- 所有数字使用千分位格式
- 百分比保留 1 位小数
- TODO 标注 P0/P1/P2 优先级
- 每个洞察附带具体数字证据
