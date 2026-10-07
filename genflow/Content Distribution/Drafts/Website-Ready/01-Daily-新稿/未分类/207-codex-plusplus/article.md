---
title: "codex-plusplus：给你的 Codex 装上插件系统"
slug: codex-plusplus-codex-plugins
date: 2026-05-24
updated: 2026-05-29
tags: [codex-plusplus, Codex, 插件, Tweak, macOS]
categories: [AI工具]
summary: codex-plusplus 通过 patch Codex.app 注入 Tweak 插件系统，支持自定义快捷键与 UI 改进。Tweak 存于应用外可热重载，但不自动更新，需手动审查。macOS/Windows 均支持。
focus_keyword: codex-plusplus
source: https://github.com/b-nnett/codex-plusplus
author: b-nnett
status: draft
---

# codex-plusplus：给你的 Codex 装上插件系统

> 2.2k+ stars | Loader + Runtime + Tweaks 三层架构

## 这是什么

[codex-plusplus](https://github.com/b-nnett/codex-plusplus) 为 **OpenAI Codex 桌面应用** 提供 Tweak（插件）系统：不重建 Codex.app，在设置里管理插件，修改外部 ESM 即刷新。

| 组件 | 位置 |
|------|------|
| Loader | `Codex.app/.../app.asar` |
| Runtime | `~/Library/Application Support/codex-plusplus/runtime/` |
| Tweaks | `.../tweaks/` |
| Config | `config.json` |

## 适合谁 / 不适合谁

| 人群 | 是否推荐 | 原因 |
|------|----------|------|
| 重度 Codex 桌面用户 | ✅ 推荐 | 快捷键、UI 微调 |
| 愿接受 patch 与本地重签名 | ✅ macOS/Win | 有 watcher 自动 re-patch |
| 企业禁止修改应用 bundle | ❌ 不推荐 | 需 patch app.asar |
| 只用网页版 ChatGPT | ❌ 不适用 | 仅 Codex 桌面 |

## 安装与前置条件

```bash
brew install b-nnett/codex-plusplus/codexplusplus
codexplusplus install
```

安装会：定位 Codex.app → 备份 → patch asar → 重算 SHA-256 → macOS 重签名 → 安装 watcher（官方更新后 re-patch）。

**Windows**：Store 版镜像到 `%LOCALAPPDATA%/codex-plusplus/store-apps/`，需启动 **Codex++** 快捷方式而非 Store 版。

## 核心用法

### 编写 Tweak

```
my-tweak/
├── manifest.json   # 含 githubRepo
└── index.js
```

```typescript
import type { Tweak } from "@codex-plusplus/sdk";
export default {
  start(api) {
    api.settings.register({ id: "my-tweak", title: "My Tweak", render: (root) => { ... } });
  },
  stop() {},
} satisfies Tweak;
```

### 常用命令

```bash
codexplusplus status
codexplusplus doctor
codexplusplus repair
codexplusplus update-codex      # macOS 安全升级 Codex
codexplusplus create-tweak
codexplusplus validate-tweak
codexplusplus dev
codexplusplus safe-mode         # 禁用所有 tweaks
codexplusplus uninstall
```

默认附带：自定义快捷键、UI improvements（从 Releases 拉取）。

## 注意事项与风险

- **Tweak 不自动更新**：每日最多检查 GitHub Release，需**手动**审查 diff 后升级。  
- **安全**：每个 tweak 需 `githubRepo`；见 [SECURITY.md](https://github.com/b-nnett/codex-plusplus/blob/main/SECURITY.md)。  
- **Codex 官方更新**：依赖 watcher re-patch；失败时 `doctor` / `repair`。  
- **签名**：macOS 本地自签名，非 Apple 公证。

## 与你现有工具的关系

- 与 [[codex-ppt-skill：图片式 PPT 生成 Skill]] 同属 Codex 生态：plusplus 改壳，ppt-skill 改能力。  
- 与 [[Karpathy 编码行为准则：AI Agent 的 4 条铁律]] 配合：Tweak 也应「外科手术式」改动。

## FAQ

### Q: 升级 Codex 后插件会丢吗？
A: watcher 应自动 re-patch；异常用 `update-codex` 或 `repair`。

### Q: safe-mode 做什么？
A: 一键禁用所有 tweaks 排查问题。

### Q: 能否分发闭源 Tweak？
A: 技术上可以；安全模型要求 manifest 含 githubRepo 便于审计。

## 相关链接

- GitHub：https://github.com/b-nnett/codex-plusplus  
- SECURITY：https://github.com/b-nnett/codex-plusplus/blob/main/SECURITY.md
