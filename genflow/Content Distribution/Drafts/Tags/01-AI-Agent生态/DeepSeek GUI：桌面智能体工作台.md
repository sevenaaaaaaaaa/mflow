---
title: "DeepSeek GUI：桌面智能体工作台"
slug: deepseek-gui-desktop-agent
date: 2026-05-25
updated: 2026-05-29
tags: [DeepSeek, Electron, 桌面应用, AI Agent, 飞书]
categories: [AI工具]
summary: DeepSeek GUI 将 DeepSeek TUI 封装为 Electron 桌面应用，支持多会话、项目工作区、diff 审查、Skill/MCP 与飞书 Claw 后台 Agent。安装后若显示「运行时离线」多为本地二进制缺失。
focus_keyword: DeepSeek GUI
source: https://github.com/XingYu-Zhong/DeepSeek-GUI
author: XingYu-Zhong
status: draft
---

# DeepSeek GUI：把 DeepSeek 智能体带进桌面的本地工作台

> 254 stars | MIT | Electron + Vite + React + TypeScript

## 这是什么

[DeepSeek GUI](https://github.com/XingYu-Zhong/DeepSeek-GUI) 把 [DeepSeek TUI](https://github.com/Hmbown/DeepSeek-TUI) 终端智能体封装成 **Electron 桌面应用**——不是聊天壳，而是能绑定本地项目、审查 AI 改动的开发工作台。

## 适合谁 / 不适合谁

| 人群 | 是否推荐 | 原因 |
|------|----------|------|
| 已用 DeepSeek API / 兼容端点的开发者 | ✅ 推荐 | 本地优先、可审 diff |
| 需飞书/Lark IM 后台 Agent | ✅ 推荐 | Claw 模式 |
| 只要网页版 Chat | ❌ 不推荐 | 安装与 runtime 较重 |
| Linux 仅要安装包 | ⚠️ 注意 | 官方 Linux 需源码构建 |

## 安装与前置条件

- macOS `.dmg`、Windows `.exe`  
- Linux：从源码构建  
- 支持 DeepSeek API 与 OpenAI 兼容 Base URL  
- 底层 runtime：`deepseek-tui` npm 包会下载 `deepseek` + `deepseek-tui` 两个二进制（macOS arm64）

## 核心用法

### 核心模块

| 模块 | 说明 |
|------|------|
| 聊天工作台 | 多会话、流式、推理可视化、工具调用、审批 |
| 项目工作区 | 绑定目录、文件预览、Git 分支 |
| 变更审查 | inline diff + 侧边审查 |
| 权限控制 | 只读 / 工作区可写 / 完全访问 |
| Skill & MCP | 图形化配置 |
| Claw 后台 | 飞书/Lark、webhook、定时任务 |
| 首次引导 | 语言 → API Key → 工作目录 |

### Claw 模式（飞书/Lark）

- 每连接可配 Agent 名、人设、模型、工作目录  
- 本地 webhook/relay、定时任务  
- 与 lark-cli 生态互补  

技术栈：Electron + electron-vite + React + Tailwind + node-pty

## 注意事项与风险

### 「运行时：离线 2」排错要点

GUI 显示离线**不一定是网络问题**，常见为本地 **runtime 二进制不齐**：

| 层面 | 问题 | 处理 |
|------|------|------|
| 配置 | `binaryPath` 为空 | 检查 `~/Library/Application Support/deepseek-gui/deepseek-gui-settings.json` |
| 二进制 | 只下了 `deepseek`，缺 `deepseek-tui` | 从 **v0.8.24** Release 补全（勿拉 latest `codewhale-tui`） |
| 验证 | `deepseek doctor` 报错 companion 缺失 | 手动 `curl` 下载 `deepseek-tui-macos-arm64` 并 `chmod +x` |

```bash
# 示例：补全 deepseek-tui（路径按本机调整）
curl -fSL -o "$DOWNLOAD_DIR/deepseek-tui" \
  "https://github.com/Hmbown/DeepSeek-TUI/releases/download/v0.8.24/deepseek-tui-macos-arm64"
chmod +x "$DOWNLOAD_DIR/deepseek-tui"
```

**教训**：Electron 说「运行时离线」→ 先查 Rust 二进制是否成对存在。

- **API Key**：存于本机，注意备份与权限。  
- **飞书集成**：需合规配置 webhook 与机器人权限。

## 与你现有工具的关系

- Runtime 底层：DeepSeek-TUI  
- IM 参考：LobsterAI  
- 与 [[Hermes Slate Desk：Hermes Agent 桌面 GUI 客户端]] 同为「Agent 桌面壳」，选型看你是否已深度用 Hermes 或 DeepSeek 生态。

## FAQ

### Q: 和 DeepSeek 网页版区别？
A: 绑定本地项目、diff 审查、Skill/MCP、Claw 后台，偏开发工作台。

### Q: 离线 2 重装整个 App 有用吗？
A: 往往只需补全 `deepseek-tui` 二进制，无需重装。

### Q: 支持哪些模型？
A: DeepSeek 官方 API + OpenAI 兼容 Base URL。

## 相关链接

- DeepSeek GUI：https://github.com/XingYu-Zhong/DeepSeek-GUI  
- DeepSeek TUI：https://github.com/Hmbown/DeepSeek-TUI  
- LobsterAI（IM 参考）：https://github.com/netease-youdao/LobsterAI
