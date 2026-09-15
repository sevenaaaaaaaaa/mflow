# 🕷️ 四工具协同抓取管线 — 使用说明书

> **一句话**：用 4 个工具协作抓任意网站，先试最便宜的方式，逐级降级，5 行代码出结果。

---

## 📋 快速启动

```bash
cd "/Users/seveno/Documents/Lovart Local Dev"

# 跑全套管线（四个工具各显神通）
python four_tool_pipeline.py

# 或只测 Scrapling（最常用的一个）
python test_scrapling.py
```

---

## 🎯 能干什么

| 你要做的事 | 用什么 | 代码量 |
|-----------|--------|:------:|
| 抓一个静态页面（如 nownexts.com 文章） | Scrapling Fetcher | 3 行 |
| 抓有 Cloudflare 保护的页面 | Scrapling StealthyFetcher | 3 行 |
| 批量爬 500 个页面，暂停续爬 | Scrapling Spider | 15 行 |
| 让 AI 理解页面，自己找内容 | Agent-Browser | 1 行命令 |
| 发现隐藏的 JSON API，绕过反爬 | Unbrowse | 1 行命令 |
| 复杂登录+交互后抓数据 | Playwright | 10 行 |
| **全自动降级：先试 API → 再 HTTP → 再隐身 → 再 AI → 再兜底** | 管线脚本 | **1 条命令** |

---

## 🧱 四个工具各自是什么

### ① Scrapling — 🎯 主力（最常用）
- **地位**：你 80% 的抓取需求用它就够了
- **特点**：纯 Python，自适应选择器（网站改版自动找），内置 Cloudflare 绕过
- **装一次就永远用**：`pip install "scrapling[all]" && scrapling install`
- **谁写的**：Karim Shoair（GitHub 64k ⭐）
- [官方文档](https://scrapling.readthedocs.io) | [GitHub](https://github.com/D4Vinci/Scrapling)

### ② Agent-Browser — 🤖 AI 帮手
- **地位**：当你不知道页面的 CSS 选择器时
- **特点**：AI 理解页面内容，说人话就能操控浏览器
- **装一次**：`npm install -g agent-browser && agent-browser install`
- **谁写的**：Vercel Labs
- [GitHub](https://github.com/vercel-labs/agent-browser)

### ③ Unbrowse — ⚡ 捷径
- **地位**：最快路径，直接调 JSON API
- **特点**：不爬 HTML，发现网站背后的 Shadow API，速度快 30x
- **装一次**：`npm install -g unbrowse`
- **谁写的**：Unbrowse AI
- [GitHub](https://github.com/unbrowse-ai/unbrowse) | [官网](https://unbrowse.ai)

### ④ Playwright — 🛡️ 兜底
- **地位**：什么都能做的终极方案
- **特点**：微软出品，支持 Chromium/Firefox/WebKit，最灵活的浏览器控制
- **Scrapling 已自带**，不需要单独装
- [官方文档](https://playwright.dev/python/)

---

## 📖 场景化教程

### 场景 1：每天抓 nownexts.com 最新文章

```python
from scrapling.fetchers import Fetcher
import json

Fetcher.adaptive = True  # 打开自适应，网站改版也不崩

page = Fetcher.get('https://nownexts.com')
articles = []

for a in page.css('article h2 a', auto_save=True):  # auto_save 记住结构
    articles.append({
        "title": a.css('::text').get(),
        "url": a.attrib.get('href'),
    })

# 导出 JSON，可直接导入 Notion / Sanity
with open("昨日文章.json", "w") as f:
    json.dump(articles, f, indent=2)

print(f"抓取 {len(articles)} 篇")
```

**如果网站改版了**：把 `auto_save=True` 换成 `adaptive=True`，Scrapling 会自动找回元素。

---

### 场景 2：被 Cloudflare 挡住了

```python
from scrapling.fetchers import StealthyFetcher

page = StealthyFetcher.fetch(
    'https://受保护的网站.com',
    headless=True,
    solve_cloudflare=True,   # 自动绕过 Turnstile
    network_idle=True,
    timeout=60000            # Cloudflare 解谜需要时间长一点
)

data = page.css('.content::text').getall()
print(data)
```

---

### 场景 3：批量爬 500 个话题（可暂停续爬）

```python
from scrapling.spiders import Spider, Response

class TopicSpider(Spider):
    name = "topics"
    start_urls = ["https://目标站.com/topic/1", "https://目标站.com/topic/2"]  # 放你所有 URL
    concurrent_requests = 10  # 并发数

    async def parse(self, response: Response):
        yield {
            "url": response.url,
            "title": response.css('h1::text').get(),
            "content": ' '.join(response.css('.entry::text').getall()),
        }

# 跑！Ctrl+C 自动暂停，重启续跑
result = TopicSpider(crawldir="./topic_cache").start()
result.items.to_json("topics.json")
```

---

### 场景 4：让 AI 帮你在页面上找东西（不用写选择器）

```bash
# 打开页面
agent-browser open "https://目标站.com/tools/某个工具"

# 看页面结构
agent-browser snapshot

# 用自然语言让 AI 找（单次）
agent-browser chat "找出页面上所有价格信息和工具名称"

# 或进入交互模式
agent-browser chat
# 然后开始对话...
```

---

### 场景 5：发现隐藏的 JSON API（完全绕过反爬）

```bash
# 发现 API
npx unbrowse resolve --intent "get product list" --url "https://目标站.com/tools"

# 如果有可用端点，直接拿数据
npx unbrowse execute --endpoint_id xxx

# 或者用本地浏览模式（不需要 API key）
npx unbrowse go "https://目标站.com"
npx unbrowse snap
npx unbrowse text "h2"
```

---

### 场景 6：用 Playwright 做复杂操作后抓取

```python
from playwright.sync_api import sync_playwright
from scrapling.parser import Selector

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    
    # 完成复杂交互
    page.goto("https://目标站.com/login")
    page.fill("#user", "账号")
    page.fill("#pass", "密码")
    page.click("#login-btn")
    page.wait_for_load_state("networkidle")
    
    # 拿 HTML 交给 Scrapling 解析（最快解析器）
    from scrapling.parser import Selector
    doc = Selector(page.content())
    data = doc.css('.protected-data::text').getall()
    
    browser.close()
```

---

## ⚙️ 管线自动降级逻辑

`four_tool_pipeline.py` 的核心机制：

```
目标 URL
    │
    ├─ ① Unbrowse → 发现 Shadow API?  → ✅ 最快路径（比爬快 30x）
    │                  ↓ 无 API
    ├─ ② Scrapling HTTP → 能拿到?     → ✅ 纯 Python，0 浏览器
    │                      ↓ 有反爬
    ├─ ③ Scrapling 隐身 → 绕过了?     → ✅ 内置 Cloudflare 绕过
    │                      ↓ 需要 AI
    ├─ ④ Agent-Browser → AI 理解了?   → ✅ 语义查找
    │                      ↓ 需要极致控制
    └─ ⑤ Playwright → 兜底           → ✅ 什么都能做
```

**每次只跑一个工具**是指定参数可以单独调用：

```python
from four_tool_pipeline import (
    try_unbrowse,       # 发现 Shadow API
    try_scrapling,      # HTTP 抓取（传 use_stealth=True 变隐身模式）
    try_agent_browser,  # AI 语义浏览器
    try_playwright,     # 终极浏览器
    run_pipeline,       # 全自动降级管线
    export_results,     # 结果导出
)

# 只测某一个工具
result = try_scrapling("https://目标站.com", use_stealth=False)

# 全自动降级
results = run_pipeline("https://目标站.com")
```

---

## 🚀 在新电脑/新 Agent 上部署

### 完整部署（3 条命令）

```bash
# 1. 安装 Scrapling（主力）
pip install "scrapling[all]"
scrapling install

# 2. 安装 Agent-Browser（AI 浏览器）
npm install -g agent-browser
agent-browser install

# 3. 安装 Unbrowse（API 发现）
npm install -g unbrowse
```

### 只需核心功能（最小部署）

```bash
pip install "scrapling[all]"
scrapling install
# Scrapling 一个就够 80% 场景
```

### 然后拷贝管线文件

```
从本机复制到新机器：
  four_tool_pipeline.py      ← 主管线脚本
  test_scrapling.py          ← Scrapling 验证脚本
  本说明书                      ← 你正在看的这个
```

---

## 📁 本机文件清单

```
~/Documents/Lovart Local Dev/
├── four_tool_pipeline.py          ← 四工具协同管线脚本
├── test_scrapling.py              ← Scrapling 单独验证脚本
├── scrapling-research-report.md   ← 研究报告（工具对比）
├── 四工具协同管线_便携指南.md      ← 便携部署指南
└── 本说明书                       ← 就是你现在看的
```

---

## 📊 常用命令速查

| 命令 | 作用 |
|------|------|
| `python four_tool_pipeline.py` | 跑整套管线（5 层全跑） |
| `python test_scrapling.py` | 只测 Scrapling 功能 |
| `scrapling extract get <url> 输出.md` | 无代码抓取网页→Markdown |
| `scrapling extract fetch <url> 输出.md` | 浏览器渲染后抓取 |
| `scrapling shell` | 进入交互式爬虫 Shell |
| `agent-browser open <url>` | AI 浏览器打开页面 |
| `agent-browser chat "找所有标题"` | AI 自然语言找内容 |
| `agent-browser snapshot` | 截图+无障碍树快照 |
| `npx unbrowse go <url>` | Unbrowse 打开页面 |
| `npx unbrowse resolve --url <url>` | 发现 Shadow API |
| `scrapling install` | 安装/更新浏览器 |
| `agent-browser install` | 下载 Agent-Browser 用 Chrome |
| `agent-browser doctor` | 诊断 Agent-Browser 状态 |

---

## ⚠️ 常见问题

### Scrapling 安装慢
```bash
# 只装解析器（最快）
pip install scrapling
# 需要浏览器时再加
pip install "scrapling[fetchers]"
scrapling install
```

### "没有这个命令"
```bash
# 检查 PATH
echo $PATH
# Scrapling 是 python 模块，用 python -m scrapling
python -m scrapling extract get <url> output.md
```

### Playwright 报错 "chromium not found"
```bash
scrapling install    # 或
playwright install chromium
```

### Agent-Browser 开不了页面
```bash
agent-browser doctor   # 诊断问题
# 最常见原因：Chrome 没装或路径不对
```

### Unbrowse resolve 返回空
- 本地功能（go/snap/click）**不需要注册**
- API 发现功能需要去 [unbrowse.ai/login](https://unbrowse.ai/login?cli=1) 注册获取 API key
- 先用 `npx unbrowse go <url>` 试本地模式

---

## 🔗 官方链接

| 工具 | 文档 | GitHub |
|------|------|--------|
| Scrapling | [scrapling.readthedocs.io](https://scrapling.readthedocs.io) | [D4Vinci/Scrapling](https://github.com/D4Vinci/Scrapling) |
| Agent-Browser | [agent-browser.dev](https://agent-browser.dev) | [vercel-labs/agent-browser](https://github.com/vercel-labs/agent-browser) |
| Unbrowse | [docs.unbrowse.ai](https://docs.unbrowse.ai) | [unbrowse-ai/unbrowse](https://github.com/unbrowse-ai/unbrowse) |
| Playwright | [playwright.dev/python](https://playwright.dev/python/docs/intro) | [microsoft/playwright-python](https://github.com/microsoft/playwright-python) |

---

*最后更新: 2026-06-16 | 本机四工具已全部就绪 ✅*
