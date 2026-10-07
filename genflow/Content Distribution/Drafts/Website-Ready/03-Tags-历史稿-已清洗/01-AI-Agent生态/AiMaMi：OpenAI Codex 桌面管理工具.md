---
title: "AiMaMi：OpenAI Codex 桌面管理工具"
slug: aimami
date: 2026-06-15
updated: 2026-06-15
tags: [Codex, Agent管理, MCP]
categories: [AI工具]
summary: "AiMaMi：OpenAI Codex 桌面管理工具。平台：Mac/Win/Linux。"
focus_keyword: "AiMaMi"
source: https://github.com/borawong/AiMaMi
status: draft
---

# AiMaMi：OpenAI Codex 桌面管理工具

> 1.2k stars | Apache-2.0 | Tauri 2 桌面应用

## 这是什么

[AiMaMi](https://github.com/borawong/AiMaMi) 是 **OpenAI Codex 的原生桌面管理工具**。Codex 的账户、会话、MCP 条目、Skills、智能路由、中继配置等分散在 `~/.codex` 下的多个文件（TOML/JSON/SQLite）中，手动编辑这些文件操作繁琐且容易出错——AiMaMi 把这些高频管理操作整合到一个 GUI 中，让你可视化管理 Codex 的一切。

技术栈为 Tauri 2 + React 18 + Rust，原生桌面性能。核心解决 Codex 用户的几个痛点：多账户切换需要手动改 `auth.json`、配额耗尽时无自动切换、中继模型配置复杂、会话清理不透明、MCP/Skills 生命周期管理缺乏 GUI。

与 Codex 内置的终端配置不同，AiMaMi 提供**可视化概览和批量操作**——比如你可以在 UI 中同时管理多个账户、一键切换、查看配额状态、批量清理会话、用诊断工具修复常见配置问题。它直接读写 Codex 本地的 `~/.codex` 目录，不引入额外数据层。

## 适合谁 / 不适合谁

| 人群 | 是否推荐 | 原因 |
|------|----------|------|
| 重度 Codex 用户（多个账户/模型切换） | ✅ 推荐 | 自动切换配额耗尽的账户，智能路由中继模型 |
| 管理多个 MCP 和 Skills | ✅ 推荐 | GUI 管理生命周期 + 备份恢复 |
| 需要定期清理会话释放配额 | ✅ 推荐 | 可视化查看、分析、批量清理本地会话 |
| 偶尔用 Codex、不在乎配置细节 | ❌ 不推荐 | 手动编辑几个 json 文件就够了，不需要装 GUI |
| 非 macOS/Windows 平台 | ⚠️ 酌情 | Linux 标记为 best-effort，部分功能可能不稳定 |

## 安装

**环境要求**：Node.js · pnpm · Rust · [Tauri 前置依赖](https://v2.tauri.app/start/prerequisites/)

```bash
# 从源码构建
git clone https://github.com/borawong/AiMaMi.git
cd AiMaMi
pnpm install
pnpm tauri dev   # 开发模式
pnpm tauri build # 生产构建

# 或从 Releases 页面下载预编译安装包（macOS/Windows）
# https://github.com/borawong/AiMaMi/releases
```

## 核心用法

**账户管理**：可视化查看和管理所有 Codex 账户——切换账户不用打开 `auth.json`，配额状态一目了然，支持导入/导出。

**自动切换**：当一个账户的 5 小时或周配额耗尽时，自动切换到备用账户并重启 Codex——告别「正在写代码突然配额用完」的尴尬。

**智能路由**：配置中继模型，让 Codex Desktop 使用你指定的模型作为中转。中继转发通过 AiMaMi 本地代理实现，需要保持 AiMaMi 运行。

**中继管理**：提供商设置、连通性测试、导入/导出、路由诊断，一站式管理中继配置。

**会话管理**：安全查看、分析、批量清理 `~/.codex` 下的本地会话索引，不用手动操作 SQLite。

**MCP / Skills 管理**：在 UI 中管理 MCP 条目和 Skills 的生命周期，支持备份和恢复。

**插件管理**：统一开关内置扩展（如 Web 工具、图片支持等）。

**自定义指令**：管理 `~/.codex/AGENTS.md` 中 AiMaMi 维护的区块，支持预览和回滚。

**系统维护**：诊断、清理、重建注册表、强制退出 Codex、修复常见配置问题。

**设置与运行时**：主题、语言、配额刷新、API 代理、更新检查；macOS 菜单栏和 Notch 配额显示。

## 注意事项与风险

- **需要保持运行**：智能路由的中继转发依赖 AiMaMi 本地代理，使用中继模型期间 AiMaMi 必须保持运行。
- **非官方工具**：AiMaMi 与 OpenAI 无任何关联。使用第三方中继服务需自行评估风险并遵守其服务条款。
- **直接操作 Codex 数据**：工具直接读写 `~/.codex` 下的本地文件，虽然设计目标是安全操作，但建议在首次使用前备份 `~/.codex` 目录。
- **平台限制**：Linux 支持标记为 best-effort，部分 macOS 特定功能（如 Notch 配额显示）不可用。
- **版本兼容**：Codex 更新可能改变文件格式，若 AiMaMi 版本不匹配可能导致部分功能异常，关注 Release Notes 及时升级。

## 与你现有工具的关系

- [[codex-plusplus：给你的 Codex 装上插件系统]] 与 AiMaMi 互补：codex-plusplus 聚焦插件能力扩展，AiMaMi 聚焦配置管理和工作流优化。
- [[skills-manage：20+ 平台 Agent Skills 中央统一管理]] 可以管理跨平台 Skills，AiMaMi 则专注于 Codex 一个平台的深度管理。
- [[codex-ppt-skill：图片式 PPT 生成 Skill]] 和 [[Claude Code Skills：-last30days 找最近 30 天好用的 Prompt]] 这类 Codex Skills 可通过 AiMaMi 的 Skills 管理模块统一维护。
- 如果你在 Codex 对话中发送敏感数据，先用 [[../05-开发技术栈/Privacy Filter：本地隐私脱敏，发给 AI 前清理敏感文本]] 脱敏，再通过 AiMaMi 配置的智能路由模型发送。

## FAQ

### Q: AiMaMi 会修改我的 Codex 账户数据吗？
A: AiMaMi 读写的是 `~/.codex` 下的本地配置文件和会话索引。它不会直接操作你的 OpenAI 账户——切换账户、清理会话等操作都是通过修改本地文件实现。建议首次使用前备份 `~/.codex` 目录。

### Q: 智能路由和直接用 Codex 选模型有什么区别？
A: 智能路由的核心价值是**自动 fallback**。你可以设置主模型和备用模型，当主模型配额耗尽时自动切换——Codex 原生不支持这个功能。另外，中继模型可以让你接入第三方 API，如通义千问、DeepSeek 等。

### Q: 更新 AiMaMi 后 Codex 配置会丢失吗？
A: 不会。AiMaMi 的应用数据存储在 `~/.codex/codexmate/`，而 Codex 的原生数据在 `~/.codex/` 的其他位置。更新 AiMaMi 只替换应用本身，不会影响你的 Codex 配置。但建议定期备份 `~/.codex` 目录。

## 相关链接

- GitHub：https://github.com/borawong/AiMaMi
- Releases：https://github.com/borawong/AiMaMi/releases
