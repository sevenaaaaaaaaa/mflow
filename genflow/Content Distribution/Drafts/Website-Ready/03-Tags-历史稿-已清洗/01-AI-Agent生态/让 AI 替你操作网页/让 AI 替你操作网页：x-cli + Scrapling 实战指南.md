---
title: "让 AI 替你操作网页：x-cli + Scrapling 实战指南"
slug: x-cli-scrapling-web-automation-guide
date: 2026-05-24
updated: 2026-05-29
tags: [x-cli, Scrapling, 网页抓取, 自动化, CLI, AI工具]
categories: [AI工具]
summary: x-cli 驱动真实 Chrome 完成需登录的网页操作，Scrapling 用 Python 绕过反爬抓取公开数据。一文讲清二者分工、安装与组合实战，让 AI 从手动点网页升级到一句话自动化。
focus_keyword: x-cli Scrapling
source: https://github.com/better-world-ai/x-cli
status: draft
---

# 让 AI 替你操作网页：x-cli + Scrapling 实战指南

> x-cli：登录态浏览器自动化 | Scrapling：54k+ stars 自适应抓取框架

## 这是什么

两个开源项目覆盖「网页自动化」的两条路径：

- **[x-cli](https://github.com/better-world-ai/x-cli)**：把反复做的网页操作做成 CLI，用 kimi-webbridge 驱动**你已登录的 Chrome**，不走 API。
- **[Scrapling](https://github.com/D4Vinci/Scrapling)**：Python 自适应抓取框架，擅长反爬绕过、自适应选择器、Spider 与 MCP 集成。

二者互补，而非替代。详见 [[x-cli：AI Agent 一句话操控网页的 CLI 工具集]]。

## 适合谁 / 不适合谁

| 人群 | 是否推荐 | 原因 |
|------|----------|------|
| Agent 用户需订酒店、比价格、批量出图 | ✅ x-cli | 依赖真实登录态 |
| 数据采集、竞品监控、研究爬虫 | ✅ Scrapling | 公开页面 + 反爬 |
| 只会用 GUI、不愿写 Python | ⚠️ 仅 x-cli | Scrapling 需 Python |
| 企业级合规爬虫平台 | ❌ 需评估 | 二者均为个人/小团队工具 |

## 安装与前置条件

### x-cli

- 安装 [kimi-webbridge](https://www.kimi.com/zh-cn/features/webbridge)
- 克隆 x-cli 或从 Releases / Homebrew 安装各子 CLI

已安装示例：

```bash
~/x-cli/baidu-cli          # 百度搜索
~/x-cli/google-cli         # Google 搜索
~/x-cli/chatgpt-image-cli  # ChatGPT 批量生图
~/x-cli/nanobanana-cli     # Gemini 批量生图
```

### Scrapling

```bash
pip install scrapling
# 交互式 Shell
scrapling shell
```

## 核心用法

### x-cli 现成场景

| 场景 | CLI | 示例指令 |
|------|-----|----------|
| 旅行规划 | ctrip-cli + booking-cli | 「帮我规划 6 月京都 5 天行程」 |
| 租房找房 | 58-cli + anjuke-cli | 「上海张江两室一厅，月租 5000」 |
| AI 画图批量 | chatgpt-image-cli | 「画 30 张排版用的封面图」 |
| 话题深度研究 | google-cli + baidu-cli | 「搜 AI 模型前 10 篇，拿回正文」 |

### Scrapling 三大能力

**1. 反爬绕过**

```python
from scrapling.fetchers import StealthyFetcher
StealthyFetcher.adaptive = True
page = StealthyFetcher.fetch('https://example.com', headless=True)
```

**2. 自适应解析**

```python
products = page.css('.product', auto_save=True)
products = page.css('.product', adaptive=True)
```

**3. Spider 框架** — 支持暂停/恢复、多 session、流式输出、开发模式缓存响应。

### CLI 一行抓取

```bash
scrapling extract get 'https://example.com' content.md
scrapling extract stealthy-fetch 'https://nopecha.com/demo/cloudflare' captchas.html --solve-cloudflare
```

### MCP Server（AI Agent 集成）

内置 MCP，已上架 ClawHub：[scrapling-official](https://clawhub.ai/D4Vinci/scrapling-official)。先提取再喂给 AI，减少 token。

### 二者分工

| | x-cli | Scrapling |
|---|------|-----------|
| 适用场景 | 需登录态的操作 | 公开数据抓取 |
| 驱动方式 | 你的真实 Chrome | Playwright/HTTP |
| 门槛 | 零代码（Agent 生成 CLI） | Python 编程 |
| 典型任务 | 订酒店、比价格、批量生图 | 数据采集、竞品监控、研究 |

## 注意事项与风险

- **x-cli**：受目标网站改版与 ToS 限制；勿用于未授权批量爬取。
- **Scrapling**：Cloudflare 等反爬场景需 StealthyFetcher，仍有失败可能。
- **性能**：Scrapling 在 5000 元素提取测试中约 2ms，远快于 BeautifulSoup（文档自称 784×），但实际取决于页面复杂度。
- **合规**：抓取公开数据仍需遵守 robots.txt 与当地法律。

## 与你现有工具的关系

- x-cli 与 `baoyu-url-to-markdown`、`mavis-browser` 等 skill 互补，见 [[x-cli：AI Agent 一句话操控网页的 CLI 工具集]]。
- Scrapling 可在 opencode 的 Python 环境中直接 `from scrapling.fetchers import Fetcher`，见 [[../01-AI-Agent生态/给 Obsidian 接上免费 AI：opencode + 国产模型配置指南]]。

## FAQ

### Q: 能否只用 Scrapling 登录后抓小红书？
A: 公开页可以；强登录态、复杂交互更适合 x-cli + 真实 Chrome。

### Q: Scrapling 和 Playwright 怎么选？
A: Scrapling 在自适应选择器、反爬、Spider 断点续跑上封装更完整；纯脚本 Playwright 更轻。

### Q: x-cli 的 CLI 谁维护？
A: 社区 + agent-cli-creator 生成；站点变更需自行更新或重新生成。

## 相关链接

- x-cli：https://github.com/better-world-ai/x-cli
- Scrapling：https://github.com/D4Vinci/Scrapling
- 本库笔记：[[x-cli：AI Agent 一句话操控网页的 CLI 工具集]]
