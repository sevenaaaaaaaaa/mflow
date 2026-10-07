---
title: "UniClipboard：端到端加密的跨设备剪贴板同步"
slug: uniclipboard-e2ee-clipboard-sync
date: 2026-05-29
updated: 2026-05-29
tags: [UniClipboard, 剪贴板, 隐私, Rust, Tauri]
categories: [AI工具]
summary: UniClipboard 用 Rust+Tauri 实现跨设备剪贴板同步，端到端加密、无云账号、P2P 与中继回落，支持文本图片文件。适合多机办公，不适合要云端剪贴板历史的用户。
focus_keyword: UniClipboard
source: https://github.com/uniclipboard/uniclipboard
status: draft
---

# UniClipboard：端到端加密的跨设备剪贴板同步

> 601+ stars | Rust + Tauri | 无账号、无中心服务器

## 这是什么

[UniClipboard](https://github.com/uniclipboard/uniclipboard) 是**隐私优先**的跨设备剪贴板同步工具：

> 一台 Ctrl+C，另一台 Ctrl+V——哪怕跨互联网。无需云账号，剪贴板不以明文离开你的设备。

支持同一 Wi-Fi、跨网、广域网；传输与本地存储均 **XChaCha20-Poly1305** 加密，中继只见密文。同步**文本、图片、文件**（大文件流式传输）。

## 适合谁 / 不适合谁

| 人群 | 是否推荐 | 原因 |
|------|----------|------|
| Mac/Win/Linux 多机办公 | ✅ 推荐 | 桌面 ↔ 桌面实时双向 |
| 重视隐私、排斥云剪贴板 | ✅ 推荐 | 邀请码+口令建「空间」，无邮箱注册 |
| 手机与电脑常在不同网络 | ⚠️ 手机仅 LAN | iOS TestFlight / Android APK 为局域网伴侣 |
| 需要官方云同步与网页历史 | ❌ 不推荐 | 本产品 local-first |

## 安装与前置条件

- [GitHub Releases](https://github.com/UniClipboard/UniClipboard/releases) 下载：Windows / macOS / Linux
- **移动端（LAN）**：
- iOS：[TestFlight 公测](https://testflight.apple.com/join/nyNQ8dQe) 或快捷指令
- Android：[uc-android](https://github.com/UniClipboard/uc-android) APK，协议兼容 SyncClipboard
- CLI：`uniclip` 可在无 GUI 环境使用
- 项目仍在积极开发，可能有不稳定功能

## 核心用法

### 配对与空间

设备通过**邀请码 + 口令**加入同一加密「空间」，无需云账号。

### 主要功能

- 跨网络 NAT 穿透 + 加密中继回落
- **加密空间**内本地加密全文搜索（数万条历史）
- **快捷面板**：快捷键唤出，预览文本/链接/图片/代码/文件
- 多设备管理：在线状态、吊销丢失设备

### 平台矩阵

| 平台 | 能力 |
|------|------|
| Win / macOS / Linux | 全功能跨网同步 |
| iOS / Android | 局域网伴侣，二维码配对 |

## 注意事项与风险

- **开发阶段**：README 警告可能存在不稳定或缺失功能。
- **手机跨网**：当前手机端以同一 Wi-Fi 为主，与桌面跨网能力不对等。
- **密钥管理**：丢失口令/设备吊销策略需自行备份理解。
- **企业环境**：部分网络可能限制 P2P/中继，需实测。

## 与你现有工具的关系

- 与 AI 工具链无强绑定；多机使用 [[../01-AI-Agent生态/给 Obsidian 接上免费 AI：opencode + 国产模型配置指南]] 时，可复制配置片段与日志跨机。
- 若已用 iCloud/Universal Clipboard，UniClipboard 适合**非苹果生态或要 E2EE 文件**场景。

## FAQ

### Q: 和 Apple 通用剪贴板比？
A: UniClipboard 跨平台、E2EE、支持文件与大历史加密搜索，不依赖 Apple ID。

### Q: 服务器能看到内容吗？
A: 设计为端到端加密，中继仅传密文。

### Q: 命令行怎么用？
A: 安装 `uniclip` CLI，与 GUI 同一套配对流程，适合 SSH/tmux。

## 相关链接

- GitHub：https://github.com/uniclipboard/uniclipboard
- 中文说明：仓库 `README_ZH.md`
- Android：https://github.com/UniClipboard/uc-android
