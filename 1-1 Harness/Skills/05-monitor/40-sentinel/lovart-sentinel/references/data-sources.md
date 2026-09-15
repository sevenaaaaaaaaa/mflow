# Lovart Sentinel 数据源说明

## 本地数据源（python 自动采集）

### gsc_daily.py
- **数据**：Google Search Console 日级 CSV 导出
- **路径**：`Keywords Research/Daily Raw/`
- **文件**：`*SearchPerformanceOverview*.csv` + `GSC*/*.csv`
- **列名映射**：
  - 总览：日期 / 点击次数 / 印象数 / 平均 点击率
  - 查询：热门查询 / 点击次数 / 展示 / 点击率 / 排名
  - 地域：国家_地区 / 点击次数 / 展示 / 点击率 / 排名
  - 页面：热门网页 / 点击次数 / 展示 / 点击率 / 排名
  - 设备：设备 / 点击次数 / 展示 / 点击率 / 排名

### gsc_weekly.py
- **数据**：SEO 周报 Markdown
- **路径**：`Keywords Research/SEO Report/SEO*.md`
- **提取指标**：organic_users / brand_clicks / nonbrand_ctr / bing_clicks

### email_health.py
- **数据**：邮件复盘 Markdown
- **路径**：`Lovart/邮件复盘*.md`
- **提取指标**：delivery_rate / open_rate / ctor / bounce_rate / unsub_per_10k
- **告警逻辑**：送达率<85%→P0 / 退订率>40→P0 / >20→P1

### content_production.py
- **数据**：每日产出 summary + 内容日历
- **路径**：`Output/Content Calendar/`
- **提取**：latest_article_count / article_titles

## 远程数据源（webfetch 实时采集）

### serp_bing.py
- **URL**：`https://www.bing.com/search?q=lovart+ai`
- **解析逻辑**：
  1. 正则提取 URL 域名列表
  2. 判定前 10 域名归属（官方/寄生/友方）
  3. 检查已知寄生域名黑名单
  4. 检测新出现的中文友方域名
- **寄生域名黑名单**：lovart-ai.com / lovart.pro / lovart.io / lovart.info / lovart.me / lovart.fyi

### social_x.py
- **URL**：`https://api.fxtwitter.com/lovart_ai`
- **返回 JSON**：followers / tweets / following / likes / media_count / verified / location / joined
- **对比逻辑**：与上次采集的 gsc_daily.json 中的历史数据对比变化量

### social_linkedin.py
- **URL**：`https://www.linkedin.com/company/lovart-ai`
- **解析逻辑**：
  1. 提取 follower_count
  2. 解析最近 5-8 条帖子（内容主题 + reactions + comments）
  3. 计算互动衰减趋势

### product_hunt.py
- **URL**：`https://www.producthunt.com/products/lovart/reviews`
- **解析逻辑**：
  1. 提取 rating + review_count
  2. 检查是否有新评价（对比上次）
  3. 计算 days_since_last_review
  4. 若 > 60 天，触发评价引导告警

## 受限数据源

以下平台因反爬机制无法通过 webfetch 直接采集，需后续接入官方 API：
- Instagram（Meta Graph API）
- TikTok（TikTok API）
- YouTube（YouTube Data API v3）
- Discord（Discord API — 需 bot token）
- 小红书（无公开 API）
- 微信公众号（搜狗微信搜索或 WeChat API）
