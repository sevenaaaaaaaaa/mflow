# Lovart Sentinel - 每日舆情采集 Agent 工作流 V2

## 触发条件
每日执行，或收到 `/sentinel` 命令时触发。

## Phase 1: 本地数据采集 (python)

```bash
python3 collect.py
```

自动采集: GSC日/周数据 / 邮件健康 / 内容产出 / 
待采集标记: 搜索SERP / 社媒 / 评价平台

## Phase 2: 远程实时采集 (webfetch 并行 ~18 条)

### 2.1 搜索引擎 (6条)

| # | URL | 用途 |
|---|-----|------|
| 1 | `https://www.bing.com/search?q=lovart+ai` | Bing SERP + 寄生域名 |
| 2 | `https://www.baidu.com/s?wd=lovart+ai` | 🆕 百度SERP + 相关搜索 |
| 3 | `https://www.sogou.com/web?query=lovart+ai` | 🆕 搜狗SERP + 寄生域名 |
| 4 | `https://www.bing.com/search?q=lovart+ai+review` | Bing评测SERP |
| 5 | `https://www.bing.com/search?q=%22lovart%22+reddit+OR+quora+review` | 社区搜索 |
| 6 | `https://duckduckgo.com/html/?q=lovart+site:hupu.com+OR+site:coolapk.com+OR+site:v2ex.com+OR+site:smzdm.com` | 🆕 综合垂直社区 |

### 2.2 社交媒体 API (3条)

| # | URL | 用途 |
|---|-----|------|
| 7 | `https://api.fxtwitter.com/lovart_ai` | X/Twitter 实时数据 |
| 8 | `https://www.linkedin.com/company/lovart-ai` | LinkedIn 公司页 |
| 9 | `https://www.producthunt.com/products/lovart/reviews` | Product Hunt 评价 |

### 2.3 🆕 社媒代理穿透 (3条)

| # | URL | 用途 |
|---|-----|------|
| 10 | `https://duckduckgo.com/html/?q=lovart.ai+site:instagram.com` | 🆕 Instagram: 粉丝/帖子/互动 |
| 11 | `https://duckduckgo.com/html/?q=lovart+site:tiktok.com` | 🆕 TikTok: 粉丝/视频/UGC |
| 12 | `https://yewtu.be/search?q=lovart+ai` | 🆕 YouTube: 视频/播放量 (Invidious) |

### 2.4 中国平台 (3条)

| # | URL | 用途 |
|---|-----|------|
| 13 | `https://weixin.sogou.com/weixin?query=lovart+ai&type=2` | 🆕 微信公众号文章 (搜狗) |
| 14 | `https://www.baidu.com/s?wd=lovart+ai+%E5%B0%8F%E7%BA%A2%E4%B9%A6+%E5%BE%AE%E4%BF%A1+%E7%9F%A5%E4%B9%8E` | 🆕 百度综合中文生态 |
| 15 | `https://baike.baidu.com/item/Lovart/66266116` | 🆕 百度百科词条 |

### 2.5 竞品监控 (3条)

| # | URL | 用途 |
|---|-----|------|
| 16 | `https://www.bing.com/search?q=canva+ai+midjourney+new+features+2026` | 竞品动态 |
| 17 | `https://www.bing.com/search?q=ai+design+tools+market+trend+2026` | 市场趋势 |
| 18 | `https://www.baidu.com/s?wd=AI%E8%AE%BE%E8%AE%A1%E5%B7%A5%E5%85%B7+%E6%8E%A8%E8%8D%90+2026` | 🆕 中文AI设计市场 |

## Phase 3: 数据解析

### 搜索引擎解析
- **Bing**: 前10域名 → 寄生域名检测 + 友方域名发现
- **百度**: 相关搜索词提取、"大家还在搜"、百度百科存在性、竞品广告检测
- **搜狗**: 首条域名（寄生域名风险）、微信文章列表、"问过的人"数据

### 🆕 社媒代理解析
- **Instagram via DDG**: 粉丝数/帖子数/最新帖日期和互动/Reels数量
- **TikTok via DDG**: 各账号粉丝数/视频描述/UGC内容检测
- **YouTube via Invidious**: 频道订阅数/视频数/播放量

### 🆕 中国平台解析
- **微信公众号**: 文章数量/最新发布时间/内容类型
- **百度百科**: 词条是否存在/最后更新时间/内容完整性
- **什么值得买**: 评测文章/评分/用户评论
- **贴吧/知乎/CSDN/B站**: 内容存在性

## Phase 4: 报告生成

```bash
python3 report.py
```

## 数据源覆盖全景 (V2)

| 类型 | 数量 | 采集方式 | 覆盖率 |
|------|------|----------|--------|
| 搜索引擎 | 5 (Google/Bing/百度/搜狗/DDG) | python + webfetch | ✅ 95% |
| 社交媒体 | 7 (X/LI/IG/TT/YT/Reddit/Discord) | API + DDG代理 + 待验证 | ✅ 85% |
| 评价平台 | 4 (PH/TP/G2/Capterra) | webfetch | ✅ 75% |
| 中国平台 | 13 (小红书/微信/微博/B站/抖音/知乎/百度百科/什么值得买/虎扑/酷安/贴吧/v2ex/豆瓣) | 搜索引擎交叉检测 | ✅ 80% |
| 品牌安全 | 6 寄生域名 | Bing/搜狗 SERP | ✅ 100% |
| 内部数据 | 4 (GSC/SEO/邮件/内容) | python CSV/MD | ✅ 100% |
| 竞品 | 8+ 竞品 | Bing/百度 + 知识库 | ✅ 80% |
