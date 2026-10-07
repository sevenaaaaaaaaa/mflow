# dev/tools — Web Data Acquisition Stack

把 Firecrawl / Tavily / Hermes curl 三件套接进 品牌方 现有项目,**用 web_router 自动选工具**。

## 目录结构

```
tools/
├── README.md                       ← 你正在看
├── web_router.py                   ← 入口:给定 URL 自动选最便宜/最合适的工具
├── firecrawl/
│   ├── brand_changelog.py         ← 单点示例:抓 example.com/changelog → 结构化 JSON
│   ├── README.md
│   └── output/
├── tavily/
│   └── tavily_search.py            ← 语义搜索:无 URL 时用,返回 cleaned content
├── hermes_curl/
│   └── hermes_curl.py              ← stdlib fallback:黑名单站点 / 静态 HTML
└── web_router/                     ← (预留:Playwright MCP 适配器,登录态抓取)
```

## 决策图

```
           你要抓一个 URL
                │
       URL 在 login 列表? ──yes──► playwright
       (gmail/slack/notion ws/github private)
                │no
       URL 在 Firecrawl 黑名单? ──yes──► hermes_curl
       (linkedin / instagram / fb)
                │no
       URL 是 SPA? ──yes──► firecrawl(JS 渲染)
       (notion / vercel / framer)
                │no
       Hermes curl 试一次 ──够用(>400 chars)──► 返回
                │不够
                ▼
            firecrawl ──够用──► 返回
                │不够
                ▼
            playwright(last resort)
```

## 路由规则(在 web_router.py 里硬编码)

- **黑名单 → hermes_curl**:`linkedin.com / instagram.com / facebook.com / messenger.com / whatsapp.com`
- **SPA 直跳 firecrawl**:`notion.so / vercel.com / framer.com / webflow.io / react.app`
- **其他**:先 `hermes_curl`,visible text < 400 字符则升级到 `firecrawl`
- **纯搜索 query**:有 `TAVILY_API_KEY` 用 tavily,否则 firecrawl /v2/search

## 用法

```bash
# 1. 自动选工具
python3 web_router.py https://www.example.com/changelog --out result.json

# 2. 强制 firecrawl + JSON schema(结构化抽取)
python3 web_router.py https://www.example.com/changelog \
  --tool firecrawl \
  --schema schema.json \
  --out changelog.json

# 3. 黑名单站点走 hermes_curl
python3 web_router.py https://www.linkedin.com/ --tool hermes_curl

# 4. 搜索 query(走 tavily)
python3 web_router.py "best AI design agent 2026" --tool tavily

# 5. 单点脚本
python3 firecrawl/brand_changelog.py
python3 tavily/tavily_search.py "品牌 alternative"
python3 hermes_curl/hermes_curl.py https://example.com
```

## 环境变量

| 变量 | 必须 | 提供方 |
|---|---|---|
| `FIRECRAWL_API_KEY` | 用 firecrawl 时 | firecrawl.dev |
| `TAVILY_API_KEY` | 用 tavily 时 | tavily.com |

## 落盘位置

所有抓取结果落到 `dev/Output/{Tool}/{date}-{domain}.json`(由各脚本自建)。

## 与 品牌方 现有管线集成

`web_router.fetch_url(url, schema=..., prompt=...)` 返回 dict,可直接喂给:
- `genflow/Content Calendar/scripts/`(选题生成)
- `genflow/Content Distribution/`(多语言分发)
- `genflow/blog-pipeline/`(Blog 写作)

调用方只需 `from web_router import fetch_url`,不需要关心走哪个工具。

## 下一步(待你确认)

1. 写 `web_router/playwright_adapter.py`,搞定登录态抓取(Gmail/Slack/Notion workspace)
2. 加 `tools/web_router/cli.py` 的并行批量模式(`--urls file.txt`)
3. 接进 `harness/06-cron/`,每周一 09:00 跑 `brand_changelog.py` 自动对比上周