![[../1-2 Insight/Trident Insights/reports/monthly/Lovart-SEO-2026-05]]# GSC / GA4 / Bing 可查询字段速查表

> **用途**：Lovart SEO 报告拉数前的字段 SSOT。  
> **站点**：`https://www.lovart.ai/`  
> **GA4 Property**：`properties/403618427` · **Stream**：`10524753059`  
> **更新**：2026-06-07

---

## 一、Google Search Console

### 1. Search Analytics（`searchanalytics.query`）

**端点**：`POST /webmasters/v3/sites/{siteUrl}/searchAnalytics/query`

#### 请求参数

| 参数 | 说明 |
|------|------|
| `startDate` / `endDate` | 必填，`YYYY-MM-DD`（PST） |
| `dimensions[]` | 分组维度，见下表 |
| `type` | `web`（默认）/ `image` / `video` / `news` / `discover` / `googleNews` |
| `aggregationType` | `auto` / `byPage` / `byProperty` |
| `dataState` | `FINAL` / `ALL`；按 `hour` 时用 `HOURLY_ALL` |
| `rowLimit` | 最大 25,000 |
| `startRow` | 分页偏移 |
| `dimensionFilterGroups[]` | 维度过滤（可不 group） |

#### 可分组维度

| 维度 | API 值 | 取值示例 | Lovart 已接 |
|------|--------|----------|-------------|
| 查询词 | `query` | 任意搜索词 | ✅ |
| 页面 | `page` | 完整 URL | ✅ |
| 国家 | `country` | `usa` `chn` `gbr`（ISO alpha-3） | ✅ |
| 设备 | `device` | `DESKTOP` `MOBILE` `TABLET` | ❌ |
| 日期 | `date` | `YYYY-MM-DD` | ❌ |
| 小时 | `hour` | `0–23`（近 10 天） | ❌ |
| 搜索外观 | `searchAppearance` | `RICH_RESULT` `AMP_BLUE_LINK` 等 | ❌ |

#### 返回指标（每行固定）

| 字段 | 含义 |
|------|------|
| `keys[]` | 维度值数组（顺序同 `dimensions`） |
| `clicks` | 点击 |
| `impressions` | 曝光 |
| `ctr` | 点击率 |
| `position` | 平均排名（曝光加权） |

#### 常用 dimension 组合（Lovart）

| 组合 | 脚本入口 | 用途 |
|------|----------|------|
| `query` | `seo_monthly_v2.fetch_gsc_full` | 月报 §四 5K 词 |
| `country` | 同上 | 分国家汇总 |
| `country` + `query` | 同上 | 大区品牌/非品牌 Top 词 |
| `country` + `page` | 同上 + `weekly_review_v3` | 分地区 Top 页 |
| `page`（分页） | `lovart_indexing_metrics.paginate_pages_with_traffic` | 收录率 / Top 页 |
| `query` | `weekly_review_v3.gsc_q` | 复盘周关键词 |
| `query` | `historical/seo_daily.render_day` | 日报 Top 200 词 |

#### 请求示例

```json
{
  "startDate": "2026-05-01",
  "endDate": "2026-05-31",
  "dimensions": ["country", "query"],
  "rowLimit": 5000,
  "type": "web"
}
```

```json
{
  "startDate": "2026-06-01",
  "endDate": "2026-06-07",
  "dimensions": ["device"],
  "rowLimit": 10
}
```

```json
{
  "startDate": "2026-06-06",
  "endDate": "2026-06-07",
  "dimensions": ["hour"],
  "dataState": "HOURLY_ALL",
  "rowLimit": 48
}
```

#### 维度过滤示例

```json
{
  "dimensionFilterGroups": [{
    "filters": [{
      "dimension": "country",
      "operator": "equals",
      "expression": "usa"
    }]
  }],
  "dimensions": ["query"],
  "startDate": "2026-05-01",
  "endDate": "2026-05-31"
}
```

---

### 2. Sitemaps（`sitemaps.list`）

| 字段 | 含义 | Lovart 映射 |
|------|------|-------------|
| `path` | Sitemap URL | — |
| `lastSubmitted` | 最后提交 | — |
| `lastDownloaded` | Google 最后抓取 | — |
| `warnings` / `errors` | 警告/错误数 | — |
| `contents[].submitted` | 提交 URL 数 | `sitemap_submitted` |
| `contents[].indexed` | 已索引 URL 数 | `sitemap_indexed` |

**脚本**：`lovart_indexing_metrics.fetch_sitemap_counts` / `fetch_indexing_bundle`

---

### 3. URL Inspection（`urlInspection.index.inspect`）

单 URL 诊断，非批量报表。

| 子对象 | 主要字段 |
|--------|----------|
| `indexStatusResult` | `verdict` `coverageState` `indexingState` `lastCrawlTime` `pageFetchState` `googleCanonical` |
| `mobileUsabilityResult` | `verdict` + 问题列表 |
| `richResultsResult` | `verdict` + 检测项 |
| `ampResult` | `verdict` + AMP 问题 |

**Lovart**：未接入（收录主口径 = 有曝光 URL 分页）。

---

### 4. UI 导出 CSV（Sentinel 本地读）

路径：`1-2 Insight/Keywords Research/Daily Raw Data/`

| 文件 | 列（中文） |
|------|-----------|
| `查询数.csv` | 热门查询、点击次数、展示、CTR、排名 |
| `国家_地区.csv` | 国家/地区、点击、展示、CTR、排名 |
| `网页.csv` | 网页、点击、展示、CTR、排名 |
| `设备.csv` | 设备、点击、展示、CTR、排名 |

**脚本**：`sentinel/sources/gsc_daily.py`

---

## 二、Bing Webmaster API

**协议**：SOAP / JSON / POX  
**端点**：`https://ssl.bing.com/webmasterapi/api.svc/soap?apikey={KEY}`  
**入参**：几乎所有流量接口仅 `siteUrl`，**无日期范围参数**。

### 1. GetQueryStats — 关键词

| 字段 | 类型 | 含义 | Lovart 映射 |
|------|------|------|-------------|
| `Query` | string | 搜索词 | `q` |
| `Date` | datetime | 周桶（约 top~100/周） | → `keywords_monthly` |
| `Clicks` | int | 点击 | `clicks` |
| `Impressions` | int | 曝光 | `impr` |
| `AvgImpressionPosition` | float | 平均曝光排名 | `pos` |
| `AvgClickPosition` | float | 平均点击排名 | 未用 |

**派生**：`ctr` = clicks / impressions（客户端）  
**脚本**：`trident/bing_fetch.py` → `bing-full.json`

### 2. GetPageStats — 页面

结构同 `QueryStats`，`Query` = 页面 URL → `url`。

### 3. GetRankAndTrafficStats — 站点日流量

| 字段 | 含义 | Lovart 映射 |
|------|------|-------------|
| `Date` | 日级（约 13 个月） | `traffic_daily[].date` |
| `Clicks` | 全站点击（多 vertical 合计） | `traffic_monthly` |
| `Impressions` | 全站曝光 | 同上 |

**月报 §13.1** 用此接口按月聚合。

### 4. GetCrawlStats — 爬虫/索引

| 字段 | 含义 | Lovart 已用 |
|------|------|-------------|
| `Date` | 日期 | ✅ |
| `CrawledPages` | 爬取页数 | ✅ |
| `CrawlErrors` | 爬取错误 | ✅ |
| `InIndex` | 索引 URL 数 | ✅ §13.2 |
| `InLinks` | 入链数 | ❌ |
| `Code2xx` / `Code301` / `Code302` | HTTP 状态 | ❌ |
| `Code4xx` / `Code5xx` | HTTP 错误 | ❌ |
| `BlockedByRobotsTxt` | robots 拦截 | ❌ |
| `ContainsMalware` | 恶意软件 | ❌ |
| `AllOtherCodes` | 其他状态码 | ❌ |

---

## 三、Google Analytics 4（GA4 Data API）

### 1. `runReport`（主接口）

**端点**：`POST https://analyticsdata.googleapis.com/v1beta/properties/403618427:runReport`

#### 请求参数

| 参数 | 说明 |
|------|------|
| `dateRanges[]` | `startDate` / `endDate`（`YYYY-MM-DD` 或 `NdaysAgo`） |
| `dimensions[]` | 分组维度，`{"name": "..."}` |
| `metrics[]` | 指标，`{"name": "..."}` |
| `dimensionFilter` | 维度过滤（`andGroup` / `orGroup` / `notExpression`） |
| `metricFilter` | 指标过滤 |
| `limit` | 返回行数（默认 10,000，可更高） |
| `offset` | 分页偏移 |
| `orderBys[]` | 排序 |

#### Lovart 固定过滤

| 过滤器 | 字段 | 值 | 说明 |
|--------|------|-----|------|
| 数据流 | `streamId` | `10524753059` | 仅 lovart.ai Web 流 |
| 自然搜索 | `sessionDefaultChannelGroup` | `Organic Search` | 月报 §五、周报主体 |
| 引荐 | `sessionDefaultChannelGroup` | `Referral` | 周报 OKR 估算 |

> **口径注意**：GA4 `country` 为英文国名（`United States`），GSC 为三位码（`usa`）。大区映射用 `seo_monthly_v2.country_group()`，勿混用。

---

#### 已接维度（Lovart 脚本实际使用）

| 维度 | API 名 | 取值示例 | 脚本 | 报告位置 |
|------|--------|----------|------|----------|
| 日期 | `date` | `20260531` | 月报/周报/ga4_fetch | §五 日趋势 |
| 默认渠道组 | `sessionDefaultChannelGroup` | `Organic Search` `Referral` `Direct` | 月报/周报 | §五 渠道、OKR 参考 |
| 新老用户 | `newVsReturning` | `new` `returning` | 月报/周报 | §五 用户分层 |
| 国家 | `country` | `United States` `China` | 月报/周报 | §五/§十一 GA4 地区 |
| 会话来源 | `sessionSource` | `google` `bing` `yahoo` | 月报 | §5.4 引擎拆分 |
| 国家×来源 | `country` + `sessionSource` | 组合 | 月报 | §11.10 Bing 地区近似 |

#### 已接指标（Lovart 脚本实际使用）

| 指标 | API 名 | 含义 | 报告用途 |
|------|--------|------|----------|
| 会话数 | `sessions` | Sessions | §五 主 KPI、OKR 参考行 |
| 用户数 | `totalUsers` | Users（去重） | §五、周报 |
| 新用户 | `newUsers` | 首次访问用户 | §五 新客占比 |
| 平均时长 | `averageSessionDuration` | 秒 | §五 质量 |
| 页/会话 | `screenPageViewsPerSession` | Pages/Session | §五 深度 |
| 跳出率 | `bounceRate` | 0–1 小数 | §五 质量（脚本 ×100 展示） |

#### 派生字段（客户端计算）

| 派生 | 公式 | 用途 |
|------|------|------|
| `return_users` | totalUsers − newUsers | 回访用户 |
| `new_user_pct` | newUsers / totalUsers | 新客占比 |
| `share` | channel sessions / total sessions | 渠道占比 |
| 引擎归类 | sessionSource → google/bing/其他 | §5.4 |
| 大区聚合 | country → 北美/大中华/… | §11.10 |

---

#### SEO 相关、可接未接维度（GA4 API 支持）

| 维度 | API 名 | 用途建议 |
|------|--------|----------|
| 设备 | `deviceCategory` | desktop/mobile/tablet 拆分 |
| 落地页 | `landingPage` / `landingPagePlusQueryString` | 页面级 Organic 表现 |
| 页面路径 | `pagePath` / `pagePathPlusQueryString` | Top 着陆页 |
| 语言 | `language` | i18n 内容雷达 |
| 地区/城市 | `region` / `city` | 细粒度地区 |
| 媒介 | `sessionMedium` | organic/cpc 校验 |
| 活动 | `sessionCampaignName` | UTM _campaign |
| 操作系统 | `operatingSystem` | 移动端占比 |
| 浏览器 | `browser` | 兼容性观察 |

#### SEO 相关、可接未接指标

| 指标 | API 名 | 用途建议 |
|------|--------|----------|
| 参与会话 | `engagedSessions` | 质量替代跳出率 |
| 参与率 | `engagementRate` | 会话质量 |
| 屏幕浏览 | `screenPageViews` | 页面浏览量 |
| 活跃用户 | `activeUsers` | 日活近似 |
| 事件数 | `eventCount` | 关键事件漏斗 |
| 转化 | `conversions` | 注册/付费代理（需配置事件） |
| 收入 | `totalRevenue` | 付费金额（电商属性） |

---

#### 常用 dimension 组合（Lovart）

| 组合 | 脚本入口 | 用途 |
|------|----------|------|
| `date` + Organic 过滤 | `fetch_ga4_full` | 月报 §五 汇总 |
| `sessionDefaultChannelGroup` | 同上 | 全渠道占比 |
| `newVsReturning` + Organic | 同上 | 新老用户 |
| `country` + Organic | 同上 / `weekly_review_v3` | 分国家/大区 |
| `sessionSource` + Organic | 同上 | Google/Bing 引擎拆分 |
| `country` + `sessionSource` + Organic | 同上 | Bing 分地区 GA4 近似 |
| 无维度 + 渠道过滤 | `weekly_review_v3.ga4_single_ch` | 单值 Users/Sessions |

#### 请求示例

```json
{
  "dateRanges": [{"startDate": "2026-05-01", "endDate": "2026-05-31"}],
  "dimensions": [{"name": "sessionSource"}],
  "metrics": [
    {"name": "sessions"},
    {"name": "totalUsers"},
    {"name": "newUsers"},
    {"name": "averageSessionDuration"},
    {"name": "bounceRate"}
  ],
  "dimensionFilter": {
    "andGroup": {
      "expressions": [
        {"filter": {"fieldName": "streamId", "stringFilter": {"matchType": "EXACT", "value": "10524753059"}}},
        {"filter": {"fieldName": "sessionDefaultChannelGroup", "stringFilter": {"matchType": "EXACT", "value": "Organic Search"}}}
      ]
    }
  },
  "limit": 80
}
```

```json
{
  "dateRanges": [{"startDate": "2026-05-01", "endDate": "2026-05-31"}],
  "dimensions": [{"name": "country"}, {"name": "sessionSource"}],
  "metrics": [{"name": "sessions"}, {"name": "totalUsers"}],
  "dimensionFilter": { "...": "streamId + Organic Search" },
  "limit": 500
}
```

---

#### GA4 vs GSC 口径对照（报告写作必读）

| 概念 | GSC | GA4 |
|------|-----|-----|
| 流量单位 | 点击（clicks） | 会话（sessions）/ 用户（users） |
| 国家编码 | `usa` `chn` | `United States` `China` |
| 搜索引擎 | 无直接字段（靠 query/page） | `sessionSource`（google/bing） |
| 自然搜索 | 搜索表现（曝光+点击） | `sessionDefaultChannelGroup=Organic Search` |
| 可与 DataWorks 对比 | ❌（GSC≠产品 UV） | Sessions 仅参考；UV 用 DataWorks `all_uv` |

**月报脚注**：GA4 Sessions 与 DataWorks UV 不可直接对比（见 `seo_report_standards.py` OKR 脚注）。

---

## 四、GSC vs Bing vs GA4 能力对照

| 能力 | GSC | Bing | GA4 |
|------|-----|------|-----|
| 关键词明细 | ✅ 5K+ | ⚠️ 周 top~100 | ❌（无 query 维，靠 GSC） |
| 页面明细 | ✅ 分页 | ⚠️ 周 top~100 | ⚠️ landingPage 可接 |
| 国家/地区 | ✅ 三位码 | ❌ | ✅ 英文国名 |
| 设备 | ✅ | ❌ | ✅ deviceCategory |
| 日趋势 | ✅ | ✅ 仅站点级 | ✅ date 维 |
| 会话质量 | ❌ | ❌ | ✅ 时长/跳出/页深 |
| 渠道拆分 | ❌ | ❌ | ✅ channelGroup |
| 引擎拆分 | ❌ | ❌ | ✅ sessionSource |
| 产品转化 UV | ❌ | ❌ | ❌（用 DataWorks） |

---

## 五、Lovart 脚本索引

| 脚本 | 数据源 | 主要维度/字段 |
|------|--------|---------------|
| `seo_monthly_v2.py` → `fetch_gsc_full` | GSC | query, country, country×query, country×page |
| `lovart_indexing_metrics.py` | GSC | page 分页 + sitemap |
| `weekly_review_v3.py` | GSC | query, country, country×query, country×page, page |
| `historical/seo_daily.py` | GSC | query (200) |
| `trident/gsc_fetch.py` | GSC | query, country, country×query, page |
| `trident/bing_fetch.py` | Bing | QueryStats, CrawlStats, RankAndTrafficStats |
| `sentinel/sources/gsc_daily.py` | GSC CSV | 查询/国家/页面/设备 |
| `seo_monthly_v2.py` → `fetch_ga4_full` | GA4 | date, channel, newVsReturning, country, sessionSource, country×source |
| `weekly_review_v3.py` | GA4 | channel, newVsReturning, date, country（大区聚合） |
| `trident/ga4_fetch.py` | GA4 | 同上 + 日/周/月环比 |
| `historical/seo_daily.py` | GA4 | sessions, totalUsers（Organic 单日） |
| `comprehensive_may_report.py` | GA4 | 月报同等维度 |

**凭证**：`gsc-token.json` / `ga4-token.json` / Bing `api_key`（见 `credential_paths.py`）

**产出**：
- GSC 快照：`1-4 Dev/Output/Data Ingestion/monthly-snapshots/gsc-YYYY-MM.json`
- GA4 快照：`1-4 Dev/Output/Data Ingestion/monthly-snapshots/ga4-YYYY-MM.json`
- Bing 全量：`1-2 Insight/Trident Insights/reports/bing-full.json`
- GA4 全量：`1-4 Dev/Output/Data Ingestion/ga4-full.json`

---

## 六、待扩展（建议优先级）

**GSC**
1. `device` — §十一 设备拆分
2. `date` — 月内日趋势
3. `searchAppearance` — 富结果占比
4. URL Inspection — 单 URL 诊断

**Bing**
5. `AvgClickPosition` — 双引擎排名对比
6. CrawlStats 全量状态码

**GA4**
7. `landingPage` — Organic Top 着陆页（补 GSC page 盲区）
8. `deviceCategory` — 移动端会话质量
9. `language` — i18n 内容生产雷达（日报 §要求）
10. `engagedSessions` / `engagementRate` — 替代单纯跳出率
