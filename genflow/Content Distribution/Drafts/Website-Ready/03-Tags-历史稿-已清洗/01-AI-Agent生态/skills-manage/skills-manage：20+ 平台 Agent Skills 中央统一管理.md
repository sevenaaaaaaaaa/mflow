---
title: "skills-manage：20+ 平台 Agent Skills 中央统一管理"
slug: skills-manage-agent-skills-hub
date: 2026-06-01
updated: 2026-05-29
tags: [skills-manage, Agent Skills, Cursor, OpenCode, Tauri, AI工具]
categories: [AI工具]
summary: skills-manage 是 Tauri 开源 Agent Skills 桌面管理器，以 ~/.agents/skills/ 为中央库，软链接同步 Cursor、OpenCode 等 20+ 平台，支持 Marketplace 与 GitHub 导入，适合多 AI 编码工具混用的开发者。
focus_keyword: skills-manage
status: draft
---

# skills-manage：20+ 平台 Agent Skills 中央统一管理

> 300+ stars | Tauri v2 + React 19 + Rust | Apache-2.0 | 非官方独立工具

## 这是什么

[skills-manage](https://github.com/iamzhihuix/skills-manage) 是**跨平台 Agent Skills 桌面管理器**，解决「Claude Code、Cursor、OpenCode、Windsurf……各装一套 Skill、版本对不上」的碎片化问题。

核心思路遵循 [Anthropic Agent Skills](https://github.com/anthropics/agent-skills) 开放规范：

- **中央库**：`~/.agents/skills/` 作为 canonical 目录（单一事实来源）
- **软链接分发**：一键安装/卸载到各平台默认 Skills 目录，同一份 Skill 多处生效
- **导入来源**：Marketplace 浏览、GitHub 仓库导入（支持鉴权与重试）、本地项目 Discover 扫描
- **组织方式**：Collections 批量安装、Markdown 预览、AI 解释生成

公众号原文标题为《AI Skills 管理！开源 skills-manage 20+平台中央统一管理全功能详解 + 使用指南》，与下一篇《skills-manage 安装&进阶指南》构成连载（安装细节见 [Releases](https://github.com/iamzhihuix/skills-manage/releases/latest) 与官方 README）。

## 适合谁 / 不适合谁

| 人群 | 是否推荐 | 原因 |
|------|----------|------|
| 同时用 Cursor + Claude Code + OpenCode 等 2+ 工具 | ✅ 推荐 | 中央库 + 软链接，避免重复维护 |
| 常从 Marketplace / GitHub 拉社区 Skill | ✅ 推荐 | 内置浏览、导入、Collections |
| 只用单一 IDE、Skill 很少 | ⚠️ 可选 | 手动复制也能应付 |
| 企业禁止软链接或需集中审计 | ⚠️ 需自评 | 本地 SQLite，无遥测，但非企业级管控 |
| 需要 Linux/Windows 预编译包 | ⚠️ 注意 | 当前 Release 主要提供 Apple Silicon macOS；其他平台需源码构建 |
| 期望官方 Anthropic/OpenAI 背书 | ❌ 不适用 | 独立非官方工具，README 有免责声明 |

## 安装与前置条件

### 桌面端（推荐）

- 从 [GitHub Releases](https://github.com/iamzhihuix/skills-manage/releases/latest) 下载
- **macOS Apple Silicon**：`.dmg` 或 `.app.zip`
- **macOS Gatekeeper**：未 notarize 时若提示「已损坏」，安装后执行：

```bash
xattr -dr com.apple.quarantine "/Applications/skills-manage.app"
```

### 源码开发

- Node.js LTS、pnpm、Rust stable、Tauri v2 系统依赖
- 中央库默认路径：`~/.agents/skills/`
- 元数据 SQLite：`~/.skillsmanage/db.sqlite`

```bash
git clone https://github.com/iamzhihuix/skills-manage.git
cd skills-manage
pnpm install
pnpm tauri dev
```

## 核心用法

### 中央库 → 平台安装

1. 首次启动完成引导，确认中央目录（建议保持 `~/.agents/skills/`）
2. 在 **Central Skills** 查看已安装 Skill
3. 选择目标平台（如 Cursor → `~/.cursor/skills/`、OpenCode → `~/.opencode/skills/`）一键 Install/Uninstall
4. 底层通过**符号链接**同步，无需手动复制

### 导入 Skill

| 方式 | 说明 |
|------|------|
| Marketplace | 浏览发布者与 Skill，一键导入中央库 |
| GitHub 仓库 | 输入 repo URL，支持 PAT 鉴权与重试 |
| Discover | 扫描本地项目级 Skill 目录 |
| Collections | 将常用 Skill 打包，批量安装到多平台 |

### 原生支持平台（节选）

| 类别 | 平台 | Skills 目录 |
|------|------|------------|
| Coding | Claude Code | `~/.claude/skills/` |
| Coding | Cursor | `~/.cursor/skills/` |
| Coding | OpenCode | `~/.opencode/skills/` |
| Coding | Codex CLI | `~/.agents/skills/` |
| Coding | Windsurf / Trae / Qoder | 各平台 `~/.*/skills/` |
| Lobster 生态 | OpenClaw、QClaw、WorkBuddy 等 | 见 README 完整表 |
| Central | 中央技能库 | `~/.agents/skills/` |

Settings 中可**自定义平台**路径。完整列表见 [README_CN.md](https://github.com/iamzhihuix/skills-manage/blob/main/README_CN.md)。

### 其他能力

- 技能详情：Markdown 预览、源码查看、AI 解释（需自行配置 API Key）
- 中英文界面、Catppuccin 主题
- 大规模库：延迟查询、虚拟列表优化搜索

## 注意事项与风险

- **正文抓取限制**：微信正文页触发验证码，本文主要依据公众号**专辑 API 标题**、相邻文章元数据，以及 [GitHub README_CN](https://github.com/iamzhihuix/skills-manage/blob/main/README_CN.md) 与公开转载整理；若与原文有出入，请以仓库文档为准。
- **非官方工具**：与 Anthropic、OpenAI、各 IDE 厂商无隶属关系。
- **凭据安全**：GitHub PAT、AI API Key 存本地 SQLite，**无静态加密**；勿在 issue/截图中泄露。
- **网络与隐私**：无遥测；仅在使用 Marketplace、GitHub 导入、AI 解释时发起外网请求。
- **平台差异**：软链接在 Windows 可能需要开发者模式或管理员权限；部分工具 Skill 目录会随版本变更。
- **同类竞品**：若需 skills.sh 商店 + Git 备份，可对比 [xingkongliang/skills-manager](https://github.com/xingkongliang/skills-manager)、[congwa/skill-manager](https://github.com/congwa/skill-manager)（40+ 工具）。

## 与你现有工具的关系

- **OpenCode 用户**：Skill 安装到 `~/.opencode/skills/`，与 [[给 Obsidian 接上免费 AI：opencode + 国产模型配置指南]]、[[../03-效率生产力/Claudian × opencode：免费模型接入 Obsidian 的三通道架构]] 同一 Agent 栈。
- **Codex 桌面**：与 [[codex-plusplus：给你的 Codex 装上插件系统]] 互补——后者改 Codex UI/快捷键，skills-manage 管 Skill 资产。
- **Skill 内容来源**：社区 Skill 如 [[codex-ppt-skill：图片式 PPT 生成 Skill]]、[[The Agency：105k Star 的 AI Agent 专家库]] 可导入中央库后分发到各 IDE。
- **生态总览**：见 [[AI Agent 工具生态：从 184 个专业 Agent 到一键 PPT]]。

## FAQ

### Q: 和手动复制 Skill 文件夹有什么区别？
A: skills-manage 用中央库 + 软链接做「装一次、多平台生效」，并附带 Marketplace、Collections、项目扫描与卸载工作流，减少版本漂移。

### Q: OpenCode / Cursor 会冲突吗？
A: 不会覆盖源码——各平台读各自目录下的链接，canonical 内容仍在 `~/.agents/skills/`。卸载时按平台移除链接即可。

### Q: Windows 或 Linux 能用吗？
A: 可源码 `pnpm tauri dev/build`；预编译 Release 目前以 Apple Silicon macOS 为主，其他平台以 README 为准。

## 相关链接

- 微信原文：
- GitHub：https://github.com/iamzhihuix/skills-manage
- Releases：https://github.com/iamzhihuix/skills-manage/releases/latest
- Agent Skills 规范：https://github.com/anthropics/agent-skills
- 本库相关笔记：[[给 Obsidian 接上免费 AI：opencode + 国产模型配置指南]]、[[AI Agent 工具生态：从 184 个专业 Agent 到一键 PPT]]
