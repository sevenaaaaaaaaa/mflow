---
title: "x-cli：AI Agent 一句话操控网页的 CLI 工具集"
slug: x-cli-ai-agent-web-cli
date: 2026-05-25
updated: 2026-05-29
tags: [x-cli, browser-automation, ai-agent, cli, web-scraping, chrome]
categories: [AI工具]
summary: x-cli 用 kimi-webbridge 驱动你已登录的 Chrome，把订酒店、搜房、批量出图等网页操作封装成 Agent 可调用的 CLI，无需 API token，适合需要登录态的自动化场景。
focus_keyword: x-cli
source: https://github.com/better-world-ai/x-cli
author: better-world-ai (@xpzouying)
status: draft
---

# x-cli：AI Agent 一句话操控网页的 CLI 工具集

> 300 stars | MIT | 全 Go | 46 commits

## 这是什么

x-cli 把「你在网页上反复做的事」变成可被 AI Agent 调用的 CLI 工具集。核心范式：

**AI agent + [kimi-webbridge](https://www.kimi.com/zh-cn/features/webbridge)（驱动本地 Chrome）→ 生成/调用 CLI → 操控你已登录的浏览器完成自动化。**

> 不走 API，不折腾 token——直接驱动你真实的 Chrome 登录态。

## 适合谁 / 不适合谁

| 人群 | 是否推荐 | 原因 |
|------|----------|------|
| 需要登录态自动化的开发者 / Agent 用户 | ✅ 推荐 | 小红书、ChatGPT 网页版、携程等必须登录的场景 |
| 已用 opencode / Cursor 编排多工具的用户 | ✅ 推荐 | 可与 agent-cli-creator 配合扩展新 CLI |
| 只需抓取公开网页数据 | ❌ 不推荐 | 用 [[../03-效率生产力/让 AI 替你操作网页：x-cli + Scrapling 实战指南]] 中的 Scrapling 更合适 |
| 不愿安装 Chrome 桥或维护本地浏览器 | ❌ 不推荐 | 强依赖 kimi-webbridge |

## 安装与前置条件

**前置（只需装一次）：** [kimi-webbridge](https://www.kimi.com/zh-cn/features/webbridge)（Chrome 浏览器桥，所有 CLI 共用）。

```bash
# 预构建二进制（GitHub Releases）
# 直接从 Releases 页面下载对应平台归档

# Homebrew（部分 CLI）
brew tap xpzouying/agent-cli
brew install twitter-cli xiaohongshu-cli

# 本地编译
git clone https://github.com/better-world-ai/x-cli
cd x-cli/<某个-cli>
go build -o ./<cli-name> .
```

## 核心用法

### 12+ 个现成 CLI

| CLI | 用途 |
|-----|------|
| `ctrip-cli` | 携程机票酒店搜索 |
| `booking-cli` | Booking.com 海外酒店比价 |
| `58-cli` | 58 同城租房搜索 |
| `anjuke-cli` | 安居客房源搜索 |
| `apartments-cli` | Apartments.com 海外租房 |
| `rightmove-cli` | Rightmove 英国房产 |
| `idealista-cli` | Idealista 西班牙房产 |
| `baidu-cli` | 百度搜索 + 抓正文 |
| `google-cli` | Google 搜索 + 抓正文 |
| `gaokao-cli` | 高考分数线/位次/专业查询 |
| `boss-cli` | BOSS 直聘职位搜索 |
| `chatgpt-image-cli` | ChatGPT 网页版批量出图 |
| `nanobanana-cli` | Gemini 网页版批量出图 |
| `scholar-cli` | Google Scholar 论文搜索 |
| `xiaohongshu-cli` | 小红书内容搜索（brew 安装） |
| `twitter-cli` | Twitter/X 内容抓取（brew 安装） |

### 5 大场景

1. **旅行规划**（ctrip + booking）：「帮我规划 6 月京都 5 天行程」→ 自动比价机票、酒店、排动线  
2. **跨平台找房**（58 + 安居客 + Apartments + Rightmove + Idealista）：五平台对照清单  
3. **高考志愿**（gaokao-cli）：三年录取位次 + 专业，冲稳保三档  
4. **批量 AI 出图**（chatgpt-image / nanobanana）：用已登录网页版批量出图到本地  
5. **深度研究**（google + baidu）：搜 + 抓正文 + 汇总  

### 自己做新 CLI

装 [agent-cli-creator](https://github.com/better-world-ai/agent-cli-creator) skill，对 agent 说「帮我给 example.com 做个 CLI」即可，AI 自动生成 Go 代码并编译。

## 注意事项与风险

- **登录态与合规**：自动化操作需遵守各平台服务条款；批量抓取可能触发风控。  
- **kimi-webbridge 依赖**：未安装或 Chrome 未登录时 CLI 无法工作。  
- **非 API 方案**：稳定性取决于网页 DOM 变化，站点改版可能导致 CLI 失效。  
- **平台差异**：部分 CLI 仅提供 Homebrew 安装，Linux 需自行编译。

## 与你现有工具的关系

你已有 `baoyu-url-to-markdown`、`baoyu-danger-x-to-markdown`、`x-link-reader` 等 web 抓取 skill。x-cli 的不同在于：**不走 API，直接驱动你已登录的 Chrome**。对于需要登录态的网站（小红书、Twitter 登录后内容、ChatGPT 网页版等），x-cli + kimi-webbridge 是低成本替代方案。

对比 `mavis-browser`：x-cli 偏向「把网页操作封装为可被 agent 调用的独立 CLI」；mavis-browser 偏向「实时代理控制浏览器」。两者互补。

## FAQ

### Q: x-cli 和 Scrapling 怎么选？
A: 需登录态、模拟真人操作 → x-cli；公开数据抓取、反爬绕过 → Scrapling。详见 [[../03-效率生产力/让 AI 替你操作网页：x-cli + Scrapling 实战指南]]。

### Q: 必须用什么浏览器？
A: 通过 kimi-webbridge 驱动本机 Chrome，需保持目标站点已登录。

### Q: 如何扩展新网站 CLI？
A: 使用 agent-cli-creator skill，用自然语言描述站点操作即可生成 Go CLI。

## 相关链接

- 官方仓库：https://github.com/better-world-ai/x-cli  
- agent-cli-creator：https://github.com/better-world-ai/agent-cli-creator  
- kimi-webbridge：https://www.kimi.com/zh-cn/features/webbridge  
- 本库笔记：[[../03-效率生产力/让 AI 替你操作网页：x-cli + Scrapling 实战指南]]
