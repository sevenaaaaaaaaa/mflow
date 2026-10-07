---
title: "Hermes Slate Desk：Hermes Agent 桌面 GUI 客户端"
slug: hermes-slate-desk-gui
date: 2026-05-25
updated: 2026-05-29
tags: [Hermes, Tauri, 桌面应用, AI Agent, GUI]
categories: [AI工具]
summary: Hermes Slate Desk 是 Hermes Agent 的 Tauri 2 桌面客户端，提供对话、AI 笔记、定时任务、文件管理与终端，工作区切换时状态全隔离。需本地 Hermes Agent（默认 8642 端口）。
focus_keyword: Hermes Slate Desk
source: https://gitee.com/8187735/Hermes-Slate-Desk
author: MeeJoy
status: draft
---

# Hermes Slate Desk：Hermes Agent 的桌面 GUI 客户端

> 14 stars | MIT | Tauri 2 + React 19

## 这是什么

[Hermes Slate Desk](https://gitee.com/8187735/Hermes-Slate-Desk) 是 **Hermes Agent 的极简桌面管理界面**——对话、工作区、文件、Cron、终端一条龙，做减法不堆砌。相当于 Hermes 版的「ChatGPT Desktop」。

## 适合谁 / 不适合谁

| 人群 | 是否推荐 | 原因 |
|------|----------|------|
| 已部署 Hermes Agent + skills 的用户 | ✅ 强烈推荐 | GUI 层即插即用 |
| 不想在终端操作 Hermes 的用户 | ✅ 推荐 | 图形化 Cron、笔记、文件 |
| 未安装 Hermes Agent | ❌ 需先装 | Gateway 默认 8642 |
| 只要 DeepSeek / Codex 官方客户端 | ❌ 换 [[DeepSeek GUI：桌面智能体工作台]] 等 |

## 安装与前置条件

- Node.js ≥ 20、Rust  
- **本地运行 Hermes Agent**（默认 `8642`）

```bash
git clone https://gitee.com/8187735/Hermes-Slate-Desk.git
cd Hermes-Slate-Desk
npm install
npm run tauri dev
```

平台：macOS ✅ / Windows ✅ / Linux 🔄

## 核心用法

### 8 大模块

| 模块 | 功能 |
|------|------|
| 首页 | 仪表盘、工作区切换、最近会话 |
| 对话 | 流式、thinking 链、附件、上下文裁剪 |
| AI 笔记 | Milkdown、导出 DOCX/MD |
| 定时任务 | Cron 图形化、执行历史 |
| 文件管理 | 文件树、100+ 语言高亮 |
| 终端 | xterm.js + PTY，多标签 |
| Hermes 设置 | Agent、Skills 市场、Memory、Channels |
| 应用设置 | Gateway、主题、语言 |

### 工作区隔离

切换工作区时：会话、文件、cwd、任务、Cron、环境变量、Memory **全部独立**。

技术栈：Tauri 2.10 + React 19 + Vite 8 + Tailwind 4 + shadcn/ui + Framer Motion + xterm.js

## 注意事项与风险

- **Gitee 源**：国内访问友好，海外用户注意 clone 速度。  
- **Agent 版本**：GUI 与 Hermes Agent API 需版本匹配。  
- **Linux**：官方标注 🔄，生产使用前先验证。  
- **安全**：终端与文件管理具备本机权限，注意工作区目录范围。

## 与你现有工具的关系

你已有 Hermes Agent + Hermes skills。与 [[codex-ppt-skill：图片式 PPT 生成 Skill]]（Hermes 安装路径）、[[GBrain：AI Agent 的个人大脑层]]（Garry Tan 亦为 Hermes 用户）同属 Agent 生态。

## FAQ

### Q: 和网页聊 Hermes 有何不同？
A: 本地集成笔记、文件、终端、Cron，工作区隔离更完整。

### Q: 能否不接 Hermes 单独用？
A: 不能，依赖 Hermes Agent Gateway。

### Q: 与 DeepSeek GUI 怎么选？
A: 已投资 Hermes → Slate Desk；已用 DeepSeek TUI → DeepSeek GUI。

## 相关链接

- Gitee：https://gitee.com/8187735/Hermes-Slate-Desk  
- 本库 Hermes skills：`1-Project/Skills/20-hermes/`
