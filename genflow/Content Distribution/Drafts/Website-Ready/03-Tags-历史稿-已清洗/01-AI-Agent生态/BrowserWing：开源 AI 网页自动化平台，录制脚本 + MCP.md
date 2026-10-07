---
title: "BrowserWing：开源 AI 网页自动化平台，录制脚本 + MCP"
slug: browserwing
date: 2026-06-15
updated: 2026-06-15
tags: [浏览器自动化, MCP, 录制]
categories: [AI工具]
summary: "BrowserWing：开源 AI 网页自动化平台，录制脚本 + MCP。平台：Web/Docker。"
focus_keyword: "BrowserWing"
source: https://github.com/browserwing/browserwing
status: draft
---

# BrowserWing：开源 AI 网页自动化平台，录制脚本 + MCP

> Web/Docker | [1.3k Stars](https://github.com/browserwing/browserwing/stargazers)

## 这是什么

BrowserWing 是一个开源的浏览器自动化平台，核心理念是**将浏览器操作转化为 AI Agent 可直接调用的 MCP 命令或 Claude Skill**。它提供 78 个内置脚本（覆盖 Bilibili、GitHub、Hacker News、YouTube、知乎、微博等主流网站），一条 CLI 命令即可从任意网页提取结构化 JSON 数据。

与 Selenium、Playwright 等传统浏览器自动化库不同，BrowserWing 面向 **AI Agent 协作**设计：原生支持 MCP（Model Context Protocol）和 Skills 协议，Claude Code、Cursor 等 AI 编程工具可直接将 BrowserWing 作为浏览器控制工具调用，告别 token 消耗巨大的逐帧 DOM 分析。同时提供**可视化录制器**——在浏览器中手动操作，自动生成可回放脚本，并可导出为 MCP 命令或 Skill 文件。

架构为 Go 后端（Chrome CDP 控制 + 26+ HTTP API 端点）+ React/TypeScript 前端。支持通过 CloakBrowser 实现二进制级浏览器指纹伪装，通过 Cloudflare 等反爬检测。

## 适合谁 / 不适合谁

| 人群 | 是否推荐 | 原因 |
|------|----------|------|
| 用 AI 编程工具（Claude Code/Cursor）的开发者和自动化需求者 | ✅ 推荐 | 原生 MCP/Skills 协议集成，AI Agent 可直接调用浏览器执行操作，减少 token 消耗 |
| 需要定期从多个网站批量采集数据的分析师 | ✅ 推荐 | 78 个开箱即用的脚本 + CLI 管道模式，一行命令提取结构化 JSON |
| 仅需简单浏览器自动化且不涉及 AI Agent 的用户 | ⚠️ 酌情 | Selenium/Playwright 生态更成熟，BrowserWing 的优势主要在 AI Agent 集成场景 |

## 安装

```bash
# 方式一：npm 全局安装（推荐）
npm install -g browserwing
browserwing --port 8080
# 打开 http://localhost:8080

# macOS 若出现 "killed" 错误：
xattr -d com.apple.quarantine $(which browserwing)

# 方式二：一行安装脚本
curl -fsSL https://raw.githubusercontent.com/browserwing/browserwing/main/install.sh | bash

# 方式三：从源码构建
git clone https://github.com/browserwing/browserwing
cd browserwing
make install && make build-embedded
./build/browserwing --port 8080
```

需要系统中已安装 Google Chrome 或 Chromium。安装脚本在国内自动使用 Gitee 镜像加速。

## 核心用法

1. **CLI 模式**（AI Agent 友好）：`browserwing ls --format=json` 列出可用脚本 → `browserwing run github-trending` 运行脚本获取结构化数据 → 管道输出到 jq 等工具进一步处理。支持 `--no-headless` 显示浏览器窗口调试、`--keyword` 传参搜索
2. **MCP 集成**：在 AI 工具的 MCP 设置中添加配置 `{"mcpServers": {"browserwing": {"type": "http", "url": "http://localhost:8080/api/v1/mcp/message"}}}`，Agent 即可直接控制浏览器
3. **Skills 集成**：下载项目中的 `SKILL.md` 文件，导入到支持 Skills 协议的 AI 工具中，然后用自然语言指令操作浏览器
4. **可视化录制**：打开 WebUI（`http://localhost:8080`），进入录制模式，在浏览器中手动操作，自动生成可编辑的自动化脚本，支持导出为 MCP 或 Skill 格式
5. **反爬增强**：搭配 CloakBrowser（`pip install cloakbrowser`）实现 C++ 源码级指纹伪装，通过 Cloudflare Turnstile 等检测

## 注意事项与风险

- 需自行安装 Chrome/Chromium，浏览器版本与 CDP 协议兼容性可能影响功能
- 网站结构变更可能导致内置脚本失效，需关注项目更新
- MCP 模式下的浏览器实例生命周期由 Go 后端管理，大量并发可能占用较多系统资源
- CloakBrowser 反爬功能仅用于合法场景，**请勿用于违反网站服务条款的行为**
- 项目声明仅面向个人学习和合法自动化，使用风险自负

## 与你现有工具的关系

- **与 Selenium/Playwright**：BrowserWing 不是替代品，而是更上层的封装。Selenium 适合编写自定义自动化脚本，BrowserWing 适合将自动化能力快速暴露给 AI Agent。可以在 Playwright 写不了的场景用 BrowserWing 的 MCP 模式做补充
- **与 browse-use/Stagehand**：都是 AI Agent 浏览器控制方案。browse-use 通过 LLM 决策 DOM 操作（token 消耗大），BrowserWing 通过预定义脚本和 MCP 命令直接执行（token 消耗小、速度快）。场景不同，可互补使用
- **与 Lovart/LibTV**：BrowserWing 可以从视频平台批量采集素材信息，为 Lovart 生成提供数据输入。例如：用 BrowserWing 抓取 YouTube/B站 热门视频标题和标签，输入 Lovart 做选题参考

## 常见问题（FAQ）

**Q: BrowserWing 和直接让 Claude 操作浏览器有什么区别？**
A: 直接让 Claude 操作浏览器时，每次交互都需要 LLM 读取 DOM、推理下一步、生成操作指令，token 消耗巨大且速度慢。BrowserWing 预编译好常用操作（搜索、翻页、提取）为确定性的 MCP 命令，Agent 只需调用命令名即可，消耗的 token 仅为指令名+参数，速度提升数十倍。

**Q: 内置的 78 个脚本如果没有我需要的网站怎么办？**
A: 使用可视化录制器录制你的操作流程，保存为自定义脚本。脚本支持变量、条件逻辑，录制完成后可导出为 MCP 命令或 Skill 文件，和内置脚本一样使用。

**Q: 在国内网络环境下如何使用？**
A: 安装脚本自动检测 GitHub/Gitee 镜像并选择最快源。内置脚本覆盖了 Bilibili、知乎、微博、百度等国内主流网站。可通过设置环境变量 `BROWSER_CONTROL_URL` 连接指定 CDP 端点来使用自定义浏览器配置（含代理）。

## 相关链接

- GitHub：https://github.com/browserwing/browserwing
