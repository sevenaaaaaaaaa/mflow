# playwright/

登录态抓取 + 重 JS 渲染适配器。给 web_router 补齐最后 1/5 力所不及的拼图(Gmail/Slack/Notion workspace)。

## 两种 adapter

| 文件 | 何时用 | 依赖 |
|---|---|---|
| `python_adapter.py` | **推荐**。本地 Python Playwright,完全控制,cookie 持久化最简单 | `~/Library/Caches/lovart-tools-venv`(已装好) |
| `mcp_adapter.py` | Claude/Cursor 已配 `@playwright/mcp` 时,通过 JSON-RPC 复用 | `npx -y @playwright/mcp` |

`web_router` 默认走 `python`(失败时降级到 mcp)。

## 安装(已完成,本机已就绪)

```bash
# 1. 建独立 venv(避开 Hermes 全局 PYTHONPATH 污染 + 系统 Python ensurepip 缺位)
/opt/homebrew/bin/python3.13 -m venv ~/Library/Caches/lovart-tools-venv

# 2. 装 playwright + chromium
~/Library/Caches/lovart-tools-venv/bin/pip install playwright
~/Library/Caches/lovart-tools-venv/bin/playwright install chromium
```

**为什么不装到 Hermes 自带 venv**:`/Users/seveno/.hermes/hermes-agent/venv/lib/python3.11/site-packages/greenlet` 的 C 扩展坏掉了,任何 import `playwright.sync_api` 都会 ModuleNotFoundError。独立 venv 完全隔离。

## 用法

### 直接用 adapter(不走 router)
```bash
PYTHONPATH= ~/Library/Caches/lovart-tools-venv/bin/python \
  tools/playwright/python_adapter.py https://www.notion.so/product \
  --wait-ms 3000 \
  --out notion-product.json
```

### 通过 web_router 自动选
```python
from web_router import fetch_url

# 默认路由:notion.so 进 SPA hint → firecrawl。
# 加 use_login=True 强制走 playwright(适合 workspace 私有页)
result = fetch_url("https://www.notion.so/my-workspace-page", use_login=True)

# 强制 playwright
result = fetch_url("https://app.slack.com/", force_tool="playwright")
```

### 登录一次复用(nice trick)
adapter 默认用 `~/Library/Caches/lovart-browser-profile` 当 Chromium user-data-dir。
**第一次手动跑一次 headless=false** 完成登录,之后所有 headless 调用都自动复用 cookie。

```bash
# 第一次:无头模式关掉,会弹出浏览器,登录 Gmail/Slack,然后关浏览器
PYTHONPATH= ~/Library/Caches/lovart-tools-venv/bin/python \
  tools/playwright/python_adapter.py https://gmail.com/ --headless false
```

之后:
```bash
PYTHONPATH= ~/Library/Caches/lovart-tools-venv/bin/python \
  tools/playwright/python_adapter.py https://mail.google.com/inbox --wait-ms 4000
```

## 决策图(扩展自 web_router README)

```
           你要抓一个 URL
                │
       URL 在 login 列表? ──yes──► playwright(use_login)
       (gmail/slack/notion ws/github private)
                │no
       URL 在 Firecrawl 黑名单? ──yes──► hermes_curl
                │no
       URL 是 SPA? ──yes──► firecrawl(JS 渲染)
                │no
       Hermes curl 试一次 ──够用(>400 chars)──► 返回
                │不够
                ▼
            firecrawl ──够用──► 返回
                │不够
                ▼
            playwright(last resort,处理任何 JS 渲染 / 反爬)
```

## MCP 模式(可选)

如果你已经在 Claude/Cursor 里配置了 `@playwright/mcp`,可以直接复用:

```json
{
  "mcpServers": {
    "playwright": {
      "command": "npx",
      "args": ["-y", "@playwright/mcp"]
    }
  }
}
```

router 检测到 `PLAYWRIGHT_MCP_URL` 环境变量或 `localhost:8931` 端口就切到 HTTP 模式;
否则降级到 `npx @playwright/mcp --stdio` 单次调用。

## 限制 / 已知问题

- **每次启动开新浏览器**:Python adapter 每次都启动 chromium(2-3 秒)。需要并发请改 `async_api`。
- **Memory**:headless chromium 约 150MB/进程。批量抓大量页面时注意。
- **CAPTCHA / 高级反爬**:Playwright 默认能过大部分,但遇到 Cloudflare Turnstile/形状验证码仍需手动。
- **Chrome.app vs headless shell**:`playwright install chromium` 装的是 `chromium-headless-shell`,看不到 GUI;需要可视化登录请改用系统 Chrome.app(设置 `executable_path=/Applications/Google Chrome.app/Contents/MacOS/Google Chrome`)。