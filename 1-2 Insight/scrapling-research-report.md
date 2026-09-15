# Scrapling 深度研究报告

> **GitHub**: [D4Vinci/Scrapling](https://github.com/D4Vinci/Scrapling) | ⭐ **64.1k Stars** | v0.4.9 | BSD-3-Clause  
> **作者**: Karim Shoair | PyPI: `scrapling` | Python 3.10+

---

## 一、核心理念：Undetectable by Design

Scrapling 定位于 **"一站式自适应 Web Scraping 框架"**，从单次请求到全量爬虫，一套库解决所有问题。核心理念有三：

1. **天生隐匿** — 反检测不是"附加"而是"内置"，三个 Fetcher 各有不同级别的隐匿能力
2. **自适应生存** — 网站改版后自动适配选择器，不需改代码
3. **零妥协** — 解析器比 BeautifulSoup 快 784 倍，比 Parsel/Scrapy 还快，同时保持 92% 测试覆盖

---

## 二、三层 Fetcher 架构

Scrapling 提供三个 Fetcher 类，每个都有 Session 和 Async 版本，共享完全相同的 `Response` 对象（继承自 `Selector`）。

### 架构全景

```
┌─────────────────────────────────────────────────┐
│                  Scrapling                       │
├─────────────────────────────────────────────────┤
│  ┌──────────┐  ┌───────────────┐  ┌───────────┐ │
│  │ Fetcher  │  │DynamicFetcher │  │StealthyFe-│ │
│  │          │  │               │  │  tcher    │ │
│  │ 纯HTTP   │  │Playwright     │  │Playwright │ │
│  │HTTP/2/3  │  │Chromium/Chrome│  │+ 反检测层 │ │
│  └────┬─────┘  └──────┬────────┘  └─────┬─────┘ │
│       │               │                 │       │
│  ┌────┴─────┐  ┌──────┴────────┐  ┌─────┴─────┐ │
│  │FetcherSe-│  │DynamicSession │  │StealthySe-│ │
│  │  ssion   │  │               │  │  ssion    │ │
│  └──────────┘  └───────────────┘  └───────────┘ │
│                                                  │
│           Response = Selector + HTTP Meta        │
└─────────────────────────────────────────────────┘
```

### 1. Fetcher（基础 HTTP）— 速度 ⭐⭐⭐⭐⭐

**定位**：无反爬保护的常规网站

```python
from scrapling.fetchers import Fetcher, FetcherSession

# 单次请求
page = Fetcher.get('https://example.com')

# Session 模式 — TLS 指纹模拟
with FetcherSession(impersonate='chrome') as session:
    page = session.get('https://example.com', stealthy_headers=True)
    data = page.css('.quote .text::text').getall()

# 支持 HTTP/3
with FetcherSession(http3=True) as session:
    page = session.get('https://example.com')
```

| 能力 | 说明 |
|------|------|
| TLS 指纹 | `impersonate='chrome'/'firefox135'` 等，模拟浏览器 TLS 指纹 |
| 请求头 | `stealthy_headers=True` 自动补全真实浏览器请求头 |
| 协议 | HTTP/1.1, HTTP/2, HTTP/3 |
| 异步 | `AsyncFetcher` + `async_fetch()` |
| 速度 | 🐇🐇🐇🐇🐇（最快的层级） |

### 2. DynamicFetcher（浏览器渲染）— 速度 ⭐⭐⭐

**定位**：需要 JS 执行的动态网站，中等防护

```python
from scrapling.fetchers import DynamicFetcher, DynamicSession

# 单次请求
page = DynamicFetcher.fetch('https://spa-site.com', headless=True, network_idle=True)
data = page.css('.dynamic-content::text').getall()

# Session 模式
with DynamicSession(headless=True, network_idle=True) as session:
    page1 = session.fetch('https://site1.com')
    page2 = session.fetch('https://site2.com')
```

底层使用 **Playwright** 驱动 Chromium/Google Chrome。主要参数：
- `network_idle`: 等待网络空闲（默认等 500ms 无连接）
- `load_dom`: 等待 JS 执行完毕
- `page_action`: 注入自定义 Playwright 交互函数
- `page_setup`: 页面加载前的 hook
- `capture_xhr`: 捕获 XHR/fetch 响应
- `disable_resources`: 选择性屏蔽资源（提升 ~25% 速度）
- `block_ads`: 内置 ~3500 广告/追踪域名黑名单
- `dns_over_https`: 防止 DNS 泄露

### 3. StealthyFetcher（隐身浏览器）— 隐匿性 ⭐⭐⭐⭐⭐

**定位**：最严苛的反爬保护（Cloudflare / Akamai / PerimeterX）

在 DynamicFetcher 基础上叠加了完整的反检测层：

```python
from scrapling.fetchers import StealthyFetcher

page = StealthyFetcher.fetch(
    'https://nopecha.com/demo/cloudflare',
    solve_cloudflare=True,    # 自动解决 CF Turnstile/Interstitial
    block_webrtc=True,        # 防止 WebRTC IP 泄露
    hide_canvas=True,         # Canvas 指纹噪声
    real_chrome=True,         # 使用真实安装的 Chrome
    google_search=True,       # 设置 Google Referer
    proxy='http://user:pass@host:port'
)
```

**反检测能力清单**：

| 防护层 | 实现方式 |
|--------|----------|
| Cloudflare Turnstile | 自动检测+解决（JS challenge / 交互式 / 隐形三种） |
| CDP 运行时泄露 | 屏蔽 Chrome DevTools Protocol 检测 |
| WebRTC 泄露 | 强制走代理，防止真实 IP 泄露 |
| Canvas 指纹 | 添加随机噪声 |
| Headless 检测 | 自动 patch 已知检测方法 |
| 时区攻击 | `timezone_id` 参数手动设置 |
| Playwright 指纹 | 移除多个 Playwright 暴露的指纹特征 |

**引擎演进**：v0.3.13 之前用 Camoufox → 现在用 Patchright（仍可切换回 Camoufox）

---

## 三、杀手级功能：auto_save + adaptive

这是 Scrapling 区别于所有其他工具的**核心差异化能力**。

### 问题场景

网站改版后，你的 CSS 选择器 `#p1` 失效了——类名变了、DOM 层级变了、属性名也变了。传统做法是手动上去重新找选择器、改代码、重新部署。Scrapling 把这个过程**完全自动化了**。

### 工作原理

```
两阶段自适应引擎:
┌─────────────┐       ┌──────────────────────┐
│ 1. Save Phase│ ────→│  SQLite (默认)        │
│ auto_save     │       │  按 domain + identifier│
│ 提取唯一特征  │       │  存储                    │
└─────────────┘       └──────────────────────┘
                              │
                              ▼
┌─────────────┐       ┌──────────────────────┐
│ 2. Match Phase│ ←───│  检索已存特征         │
│ adaptive       │       │                      │
│ 全页相似度匹配  │       │                      │
└─────────────┘       └──────────────────────┘
```

**存储的唯一特征**：
- 元素：tag name、文本、属性（名+值）、兄弟节点（tag）、路径（tag names）
- 父元素：tag name、属性（名+值）、文本
- **不依赖具体值做精确匹配，而是计算相似度**——连 class name 的书写顺序变化都能容忍

### 使用方式

**方式一：CSS/XPath 选择器（自动 identifier）**
```python
from scrapling.fetchers import Fetcher
Fetcher.adaptive = True  # 全局启用

# 网站改版前：自动保存
page = Fetcher.get('https://example.com')
element = page.css('#p1', auto_save=True)

# 网站改版后：自适应匹配（同样的选择器！）
page = Fetcher.get('https://example.com')
element = page.css('#p1', adaptive=True)  # 自动找到！
```

**方式二：手动 save/retrieve/relocate（不限选择方法）**
```python
# 通过文本找到元素，手动保存
element = page.find_by_text('Tipping the Velvet')
page.save(element, 'my_product')

# N 天后网站改版，直接 relocate
element_dict = page.retrieve('my_product')
found = page.relocate(element_dict, selector_type=True)
print(found.css('::text').getall())  # ['Tipping the Velvet']
```

### 跨域场景

如果目标网站换了域名，用 `adaptive_domain` 参数：
```python
Fetcher.configure(adaptive=True, adaptive_domain='stackoverflow.com')
```

### 真实验证：2010 vs 现在 StackOverflow

用同样的选择器 `#hmenus > div:nth-child(1) > ul > li:nth-child(1) > a` 分别抓取 2010 年和 2025 年的 StackOverflow，Scrapling 在两个完全不同的 DOM 结构中**找到了同一个 "Questions" 按钮**。

---

## 四、Spider 框架（对标 Scrapy）

Scrapling 不仅仅是请求库，还有完整的 Spider 爬虫框架：

```python
from scrapling.spiders import Spider, Request, Response

class QuotesSpider(Spider):
    name = "quotes"
    start_urls = ["https://quotes.toscrape.com/"]
    concurrent_requests = 10
    
    async def parse(self, response: Response):
        for quote in response.css('.quote'):
            yield {
                "text": quote.css('.text::text').get(),
                "author": quote.css('.author::text').get()
            }
        next_page = response.css('.next a')
        if next_page:
            yield response.follow(next_page[0].attrib['href'])

result = QuotesSpider().start()
result.items.to_json("quotes.json")
```

**亮点功能**：
- **暂停/恢复**：`MySpider(crawldir="./crawl_data").start()` → Ctrl+C 优雅暂停 → 重启后自动续接
- **多 Session 混用**：同一个 Spider 可以 HTTP 请求走 `FetcherSession`，受保护页面走 `AsyncStealthySession`
- **开发模式**：首轮缓存响应到磁盘，后续只重跑 `parse()` 逻辑，不重复请求
- **流式模式**：`async for item in spider.stream()` 逐条产出 + 实时统计
- **Proxy 自动轮换**：`ProxyRotator` 支持 cyclic 和自定义轮换策略
- **Blocked 检测**：自动检测被封请求并重试

---

## 五、MCP Server

Scrapling 内置 MCP Server，可以对接 Claude/Cursor 等 AI 工具：

```bash
pip install "scrapling[ai]"
```

AI 可以通过 MCP 调用 Scrapling 的全部能力——抓取、解析、自适应选择器——减少 token 消耗因为 Scrapling 先提取目标内容再传给 AI。

---

## 六、核心性能对比

### 解析器速度（5000 嵌套元素文本提取，100+ 次平均）

| 排名 | 库 | 耗时 (ms) | vs Scrapling |
|------|-----|----------|--------------|
| 1 | **Scrapling** | 2.02 | 1.0x |
| 2 | Parsel/Scrapy | 2.04 | 1.01x |
| 3 | Raw lxml | 2.54 | 1.26x |
| 4 | PyQuery | 24.17 | ~12x |
| 5 | Selectolax | 82.63 | ~41x |
| 6 | MechanicalSoup | 1549.71 | ~767x |
| 7 | BS4 + lxml | 1584.31 | ~784x |
| 8 | BS4 + html5lib | 3391.91 | ~1679x |

### 相似度搜索（对标 AutoScraper）

| 库 | 耗时 (ms) | vs Scrapling |
|----|----------|--------------|
| **Scrapling** | 2.39 | 1.0x |
| AutoScraper | 12.45 | 5.2x |

---

## 七、四工具对比：Scrapling / Playwright / Agent-Browser / Unbrowse

### 定位对比

```
  传统Scraping ←─────────────────────────────→ AI时代
  
  Scrapling     Playwright     Agent-Browser     Unbrowse
  (全能框架)    (浏览器引擎)    (AI代理浏览器)    (Shadow API)
```

### 详细对比表

| 维度 | **Scrapling** | **Playwright** (by Microsoft) | **Agent-Browser** (by Vercel) | **Unbrowse** (by Unbrowse AI) |
|------|:-----------:|:-----------:|:-------------:|:------------:|
| **定位** | 自适应 Scraping 框架 | 通用浏览器自动化引擎 | AI Agent 的浏览器 CLI | Shadow API 发现 + 路由市场 |
| **语言** | Python | JS/TS/Python/Java/.NET | Rust 二进制 + TypeScript 封装 | TypeScript (npm) |
| **开源** | ✅ BSD-3 | ✅ Apache 2.0 | ✅ MIT | ✅ MIT (客户端) |
| **GitHub Stars** | 64.1k | 73k+ | 较新（npm 0.27.3） | 较新（npm 9.3.15） |
| **核心能力** | 解析 + 反检测 + 自适应 + Spider | Chromium/Firefox/WebKit 驱动 | 无障碍树快照 + 语义查找 + 批处理 | API 路由发现 + MCP 市场 |
| **反检测** | ⭐⭐⭐⭐⭐（内置 CF solver） | ⭐⭐（需要 stealth 插件） | ⭐⭐（Headless Chrome） | ⭐⭐⭐⭐⭐（直接 bypass，不走 HTML） |
| **选择器自适应** | ✅ auto_save + adaptive | ❌ | ❌ | ❌（不需要，走 API） |
| **Spider 框架** | ✅ 暂停/恢复/多Session | ❌ | ❌ | ❌ |
| **MCP Server** | ✅ 内置 | ❌（可外接） | ❌ | ✅ 内置 |
| **性能（相对）** | 最快（2ms 解析） | 中等（浏览器开销） | 中等（Rust CLI 快） | 最快路径 ~30x（走 JSON） |
| **Token 消耗** | 低（预提取） | 高（整页 HTML） | 中等（无障碍树） | 极低（40x 减少） |
| **费用** | 免费 + 自己维护 proxy | 免费 + 自己维护 infra | 免费 + 自己跑 Chrome | 免费 + 付费 API 市场 |
| **学习曲线** | 中等（Scrapy 用户友好） | 陡（完整 API surface） | 低（CLI 命令式） | 低（MCP 一键接入） |
| **安装复杂度** | pip + scrapling install | pip/playwright install | npm -g / brew | npx -y unbrowse mcp |
| **生态系统** | Scrapling only | 微软 + 庞大社区 | Vercel 生态 | 独立市场（路由计价） |

### 协同使用场景

```
最佳组合策略：

┌─────────────────────────────────────────────────┐
│  常规网站（无反爬）                                │
│  → Scrapling Fetcher（最快）                      │
├─────────────────────────────────────────────────┤
│  常规 SPAs（需要 JS 渲染）                         │
│  → Scrapling DynamicFetcher                      │
│  → 或 直接 Playwright + stealth 插件             │
├─────────────────────────────────────────────────┤
│  Cloudflare 保护网站                              │
│  → Scrapling StealthyFetcher（内置绕过）          │
├─────────────────────────────────────────────────┤
│  AI Agent 需要浏览网页                            │
│  → Agent-Browser（语义保真度 > 吞吐量）           │
│  → Scrapling MCP（提供结构化数据给 agent）         │
├─────────────────────────────────────────────────┤
│  发现网站 Shadow API / 高频调用                    │
│  → Unbrowse（直接调 JSON API，彻底 bypass）        │
├─────────────────────────────────────────────────┤
│  网站频繁改版 / 长期维护的爬虫                      │
│  → Scrapling adaptive（auto_save + auto_match）   │
├─────────────────────────────────────────────────┤
│  复杂交互流（登录/点击/拖拽）                      │
│  → Playwright（最灵活的浏览器控制）                │
│  → Scrapling page_action 参数（Playwright API）   │
└─────────────────────────────────────────────────┘
```

---

## 八、Scrapling 最佳实践

### 1. 渐进式反检测策略

```python
# 先尝试最快的方式
try:
    page = Fetcher.get(url, stealthy_headers=True)
    if page.status != 200:
        raise ValueError
except:
    # 升级到隐身模式
    page = StealthyFetcher.fetch(url, solve_cloudflare=True)
```

### 2. 自适应管道

```python
Fetcher.adaptive = True
page = Fetcher.get(url)

# 首次抓取时保存
products = page.css('.product', auto_save=True)

# 后续抓取时，用同一个 selector，加 adaptive=True
# 如果元素还在，正常返回；如果消失了，自动搜索匹配
products = page.css('.product', adaptive=True)
```

### 3. Spider + Checkpoint

```python
# 长爬虫加上 crawldir 即可获得暂停/恢复能力
MySpider(crawldir="./my_crawl_data").start()
# Ctrl+C → 自动保存 checkpoint
# 再次运行 → 自动从断点继续
```

### 4. 多 Session 混合

```python
def configure_sessions(self, manager):
    manager.add("fast", FetcherSession(impersonate="chrome"))
    manager.add("stealth", AsyncStealthySession(headless=True), lazy=True)

# 根据 URL 路由到不同 session
if "protected" in link:
    yield Request(link, sid="stealth")
else:
    yield Request(link, sid="fast")
```

### 5. 本地终端快速提取（零代码）

```bash
# 直接输出 Markdown
scrapling extract get 'https://example.com' content.md

# 指定选择器 + 隐身模式
scrapling extract fetch 'https://example.com' content.txt \
  --css-selector '#products' --no-headless

# 解决 Cloudflare + 提取
scrapling extract stealthy-fetch 'https://protected.com' data.html \
  --css-selector '#content a' --solve-cloudflare
```

---

## 九、对 Lovart 项目的价值评估

### 匹配度分析

| Lovart 需求 | Scrapling 覆盖 | 评级 |
|------------|:---:|:---:|
| 多语言站点抓取（10 语言） | ✅ FetcherSession + 多 Session | ⭐⭐⭐ |
| 竞品监测（频繁抓取） | ✅ Spider + Checkpoint 恢复 | ⭐⭐⭐⭐⭐ |
| Sanity CMS 数据填充 | ✅ CLI extract + MCP | ⭐⭐⭐ |
| 内容管线自动化 | ✅ Spider 流式模式 + export | ⭐⭐⭐⭐ |
| 网站改版后维护成本 | ✅ adaptive（杀手级匹配） | ⭐⭐⭐⭐⭐ |
| 绕过 Cloudflare 保护 | ✅ StealthyFetcher built-in | ⭐⭐⭐⭐⭐ |
| 低成本高频调用 | ✅ Fetcher（HTTP，零浏览器开销） | ⭐⭐⭐⭐⭐ |
| AI Agent 集成 | ✅ MCP Server | ⭐⭐⭐⭐ |

### 核心建议

**Scrapling 是 Lovart 项目的天然良配**——尤其是：

1. **adaptive 机制**直接解决了"网站改版 → 管道全崩 → 人工修复"的噩梦
2. **三层 Fetcher**完美适配"90% 常规抓取 + 10% 高难度反绕过"的实际分布
3. **Spider 框架**比裸用 Playwright 维护成本低一个数量级
4. **MCP Server**打通了 AI Agent → Scrapling → CMS 的内容注入管线

**与其他工具的分工**：
- **Playwright** → 保留给需要复杂交互的测试场景（Scrapling 底层也用 Playwright）
- **Agent-Browser** → 当 AI Agent 需要"人类视角操作浏览器"时使用（语义理解优先）
- **Unbrowse** → 发现目标网站的 Shadow API 后，可以直接用 JSON 调用，比任何 Scraper 都快；但需要网站有可用 API

---

## 十、安装和部署

```bash
# 基础（仅解析器）
pip install scrapling

# 完整（解析器 + 所有 Fetchers + Spider）
pip install "scrapling[all]"

# 安装浏览器（Chromium + 系统依赖 + 指纹依赖）
scrapling install

# Docker（包含所有浏览器）
docker pull pyd4vinci/scrapling
docker pull ghcr.io/d4vinci/scrapling:latest
```

---

*报告生成时间：2026-06-16*  
*数据来源：Scrapling GitHub README + 官方文档 + PyPI/npm 仓库*
