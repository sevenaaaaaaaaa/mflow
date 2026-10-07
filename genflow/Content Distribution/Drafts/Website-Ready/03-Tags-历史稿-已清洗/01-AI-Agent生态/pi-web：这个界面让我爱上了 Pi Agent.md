---
title: "pi-web：这个界面让我爱上了 Pi Agent"
slug: pi-web-pi-agent-browser-ui
date: 2026-06-01
updated: 2026-05-29
tags: [pi-web, Pi Agent, 编码代理, Web UI, AI工具]
categories: [AI工具]
summary: pi-web 为本地 Pi 编码代理提供浏览器 UI：Go 单文件 + Astro 前端，涵盖工作区会话、流式对话、文件编辑、Git 状态与 AG-UI 集成；需预先安装 pi CLI，适合希望用 Web 替代 TUI 的开发者。
focus_keyword: pi-web
status: draft
---

# pi-web：这个界面让我爱上了 Pi Agent

> 5+ stars | Go + Astro 单可执行文件 | MIT | 依赖本地 `pi` CLI

## 这是什么

[pi-web](https://github.com/Epsilondelta-ai/pi-web) 是面向本地 **[Pi 编码代理](https://github.com/earendil-works/pi)**（`pi` / `@earendil-works/pi-coding-agent`）的**浏览器工作台**：把 Astro 前端与 Go 后端打成**单个可执行文件**，在浏览器里完成工作区管理、多会话聊天、文件树编辑、Git 状态查看与 shell 命令执行，而无需单独部署 Node 服务。

与「只在浏览器里调 LLM API」的 Demo 不同，pi-web 通过后端驱动**真实的 pi 会话**（读写工作区、bash、工具调用等），相当于给极简 TUI 代理加了一层可视化外壳。

公众号原文标题为《**pi-web：这个界面让我爱上了 Pi Agent**》，出自「创见AI实验室」的 **Pi Agent 系列**专辑；前一篇为《Pi Agent：一个和 Claude code 不一样的 AI 工具……》，后一篇为《Pi Agent 命令大全：30+ 命令一文搞懂……》。本文技术细节以 [pi-web 官方 README（简体中文）](https://github.com/Epsilondelta-ai/pi-web/blob/main/docs/readmes/README.zh-CN.md) 与 [Pi 主仓库](https://github.com/earendil-works/pi) 为准。

## 适合谁 / 不适合谁

| 人群 | 是否推荐 | 原因 |
|------|----------|------|
| 已用或打算用 Pi Agent，嫌终端 TUI 不直观 | ✅ 推荐 | 浏览器内会话、文件树、Git 面板一体化 |
| 需要平板/手机访问本机 pi（同网段） | ✅ 推荐 | 响应式 UI，默认监听 `0.0.0.0` |
| 希望单文件安装、少折腾前后端分离 | ✅ 推荐 | `curl \| sh` 安装 Release 二进制 |
| 尚未安装 `pi` CLI、也不打算用 Pi 生态 | ❌ 不推荐 | pi-web 是 Pi 的 Web 壳，不是独立聊天产品 |
| 只要云端 SaaS、不想本地跑 Agent | ❌ 不适用 | 必须在本机运行 pi 与工作区 |
| 需要企业级多用户鉴权与审计 | ⚠️ 需自评 | 本地工具，默认无多租户安全模型 |
| 追求与 Cursor / Claude Code 同等「全家桶」功能 | ⚠️ 注意 | Pi 本体极简；复杂能力靠扩展与 CLI 组合 |

## 安装与前置条件

### 前置：Pi 编码代理

pi-web 控制的是本机已安装的 `pi` 命令行代理（来自 [earendil-works/pi](https://github.com/earendil-works/pi)）：

```bash
# 需 Node.js；具体版本以 Pi 仓库为准
npm install -g @earendil-works/pi-coding-agent

# 首次使用需完成模型/OAuth 或 API Key 配置（见 pi 文档）
pi
```

### 安装 pi-web（推荐 Release 二进制）

```bash
curl -fsSL https://raw.githubusercontent.com/Epsilondelta-ai/pi-web/main/scripts/install.sh | sh

# 更新
pi-web update
```

### 启动

```bash
pi-web
# 默认监听 0.0.0.0:8732 → 浏览器打开 http://127.0.0.1:8732

pi-web --port 9999
# 自定义端口 → http://127.0.0.1:9999
```

## 核心用法

### 工作区与会话

- **打开本地文件夹**为工作区，可切换最近工作区、删除记录，或**先 clone Git 仓库再打开**。
- **会话列表**：创建 / 重命名 / 删除会话，恢复历史对话，**流式**查看提示与回复。
- **提示控制**：多附件发送、每会话草稿、取消或 steer 运行中任务，并在 UI 内回答 pi 的 fallback choice 提示。

### 文件、Git 与终端

| 能力 | 说明 |
|------|------|
| 文件树 | Material Icon Theme 图标、搜索、预览、上传、文本编辑并保存 |
| Git | 工作区状态、文件装饰、提交历史与单次提交详情 |
| Shell | 在所选工作区执行命令，查看历史与输出 |
| 转录 | Markdown、代码高亮、工具输出、长对话虚拟滚动 |

### 设置、语音与集成

- **设置**：项目/全局 pi 配置、API Key、Claude / Codex / Copilot 等 **OAuth 订阅登录**、运行时模型与 thinking、配额检查。
- **语音**：朗读回复；浏览器或本地 Whisper 语音输入。
- **通知**：可配置 Discord / Telegram 任务完成通知。
- **语言**：UI 支持英/韩/中/日/西/葡/法/俄/德等。
- **AG-UI**：通过 AG-UI 兼容的 **SSE** 端点暴露会话，便于外部客户端集成。

## 注意事项与风险

- **正文抓取限制**：微信正文页返回「环境异常」验证码；`curl` / WebFetch / Jina 代理均无法获取 HTML 正文。本文标题与系列关系来自微信 **`getappmsgext` 专辑 API**（专辑「Pi Agent 系列」、相邻文章标题），功能与安装步骤来自 [pi-web README.zh-CN](https://github.com/Epsilondelta-ai/pi-web/blob/main/docs/readmes/README.zh-CN.md) 与 [GitHub 仓库元数据](https://github.com/Epsilondelta-ai/pi-web)；**未编造**公众号内的体验描述或截图结论，若与原文有出入请以公众号与仓库为准。
- **监听地址**：默认 `0.0.0.0` 意味着局域网可访问；若机器暴露公网或未设防火墙，存在未授权访问风险，生产环境请限制绑定地址或加反向代理鉴权。
- **依赖链**：pi-web 不替代 pi；模型费用、OAuth 与 API Key 仍遵循 Pi 与各提供商政策。
- **项目成熟度**：截至抓取时 GitHub **约 5 stars**（2026-06-01），属早期社区项目，升级前请阅读 Release 说明。
- **同类 UI**：亦可关注 [pi-dashboard](https://github.com/samfoy/pi-dashboard)、[pi-agent-dashboard](https://github.com/hdkiller/pi-agent-dashboard) 等 Pi 生态 Web 壳，选型按是否需要 iOS、多槽位、Electron 打包等区分。

## 与你现有工具的关系

- **Pi 本体**：极简四工具 Agent 运行时见 [earendil-works/pi](https://github.com/earendil-works/pi)；与 OpenClaw 等「重网关」路线不同，偏可组合底座（参见 [[AI Agent 工具生态：从 184 个专业 Agent 到一键 PPT]]）。
- **Codex / Claude Code 用户**：若主要用桌面 Codex，可对照 [[codex-plusplus：给你的 Codex 装上插件系统]]；pi-web 解决的是 **Pi TUI → 浏览器** 的体验，而非改 Codex.app。
- **OpenCode / 免费模型栈**：Pi 支持多提供商 OAuth；与 [[给 Obsidian 接上免费 AI：opencode + 国产模型配置指南]]、[[../03-效率生产力/Claudian × opencode：免费模型接入 Obsidian 的三通道架构]] 同属「多入口、本地 Agent」思路，但产品形态不同。
- **Skills 资产**：Pi 扩展与 Skills 目录生态可参考 [[skills-manage：20+ 平台 Agent Skills 中央统一管理]]（管理的是各 IDE Skill，不是 pi-web 本身）。
- **系列连载**：同专辑另有 Pi 入门、命令大全、模型切换、oh-my-pi 等篇，可在公众号「Pi Agent 系列」按序阅读。

## FAQ

### Q: pi-web 和官方 pi 自带的 Web UI 包有什么关系？
A: pi-web 是社区项目（Epsilondelta-ai），将 Astro 静态资源嵌入 Go 二进制，专门做「本地 pi 的浏览器控制台」。Pi monorepo 内另有 `@earendil-works/pi-web-ui` 等组件库，二者相关但发布形态不同，以各自 README 为准。

### Q: 不装 pi，只装 pi-web 能聊天吗？
A: 不能。必须先在本机安装并配置好 `pi`（`@earendil-works/pi-coding-agent`），pi-web 只提供 Web 层的工作区与会话界面。

### Q: 和远程 SSH 里跑 pi 怎么配合？
A: pi-web 设计为**本机**控制本地 pi 与工作区。远程开发常见做法是 SSH 端口转发（例如把 `8732` 转到本地）或在远程机启动 pi-web 后仅内网访问；公网直连需自行加固。

## 相关链接

- 微信原文：
- pi-web：https://github.com/Epsilondelta-ai/pi-web
- Pi 主仓库：https://github.com/earendil-works/pi
- pi-web 中文 README：https://github.com/Epsilondelta-ai/pi-web/blob/main/docs/readmes/README.zh-CN.md
- 本库相关笔记：[[AI Agent 工具生态：从 184 个专业 Agent 到一键 PPT]]、[[skills-manage：20+ 平台 Agent Skills 中央统一管理]]、[[给 Obsidian 接上免费 AI：opencode + 国产模型配置指南]]
