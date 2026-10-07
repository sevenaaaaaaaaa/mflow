---
title: "MioSub：一站式 AI 字幕生成与压制"
slug: miosub-ai-subtitle-automation
date: 2026-05-29
updated: 2026-05-29
tags: [MioSub, 字幕, 翻译, Electron, AI工具]
categories: [AI工具]
summary: MioSub（原 Gemini-Subtitle-Pro）覆盖下载、转录、翻译、时间轴对齐与压制全流程，内置 CTC 对齐与上下文感知 AI 编辑，粘贴链接即可出双语成片，适合 UP 主与字幕组。
focus_keyword: MioSub
source: https://github.com/corvo007/MioSub
author: corvo007
status: draft
---

# MioSub：一站式 AI 字幕生成与压制

> 531+ stars | Electron + React 19 | 曾名 Gemini-Subtitle-Pro

## 这是什么

[MioSub](https://github.com/corvo007/MioSub) 是**真正读懂上下文的 AI 字幕编辑器**， slogan：「世界的内容，你的语言。」

一站式覆盖：**下载 → 转录 → 翻译 → 校对 → 时间轴 → 压制**，粘贴视频/音频链接后全自动出成品，也可在编辑器里边看边改。v3.0 内置 **CTC 毫秒级对齐**、NotoSans 中日文渲染，支持播客与纯音频。

- 文档：https://miosub.app/docs  
- 在线体验：https://demo.miosub.app  

## 适合谁 / 不适合谁

| 人群 | 是否推荐 | 原因 |
|------|----------|------|
| UP 主、字幕组、译制爱好者 | ✅ 推荐 | 30 分钟视频约 8 分钟出片（官方宣传） |
| 需要 SRT/ASS 双语导出与成片压制 | ✅ 推荐 | 导入导出齐全 |
| 只要简单机翻、不需时间轴 | ⚠️ 可选 | 功能偏重全流程 |
| 无法配置 AI API / 本地算力极弱 | ❌ 需自评 | 依赖云端或本地推理能力 |

## 安装与前置条件

- 从 [GitHub Releases](https://github.com/corvo007/Gemini-Subtitle-Pro/releases) 或官网下载桌面端  
- 技术栈：Electron 39、React 19、TypeScript、Tailwind 4  
- v2.x 升级见[迁移指南](https://miosub.app/docs/guide/migration)  
- 需按文档配置所用 AI/转录服务（以官方文档为准）

## 核心用法

### 全自动流程

粘贴链接 → 自动下载/转录/翻译/对齐 → 返回可编辑成品；支持 **100+ 语言**互译，中/英/日界面。

### 编辑器能力

- 实时字幕预览、自动滚动、说话人标注  
- 术语自动提取、搜索替换  
- SRT/ASS 导入，双语导出，**一键压制成片**  

### v3.0 亮点

| 特性 | 说明 |
|------|------|
| CTC 对齐 | 毫秒级，无需外部对齐工具 |
| 纯音频 | 播客、电台、有声书可直接处理 |
| 界面重构 | 设置与编辑面板 v3 焕新 |

## 注意事项与风险

- **版权**：翻译/转载视频需遵守平台与著作权规定。  
- **AI 质量**：专名、梗、口语仍需人工过一眼编辑器。  
- **仓库命名**：Release 仍可能挂在 `Gemini-Subtitle-Pro` 路径下，以 Releases 页为准。  
- **API 费用**：若使用付费模型，批量长视频成本需自行估算。

## 与你现有工具的关系

- 视频配音翻译可配合 [[Violin：开源视频翻译与配音 Skill]]（重配音轨）或 MioSub（重字幕条）。  
- 长文创作与发布流水线见 [[../01-AI-Agent生态/给 Obsidian 接上免费 AI：opencode + 国产模型配置指南]]、[[AIMedia：全自动 AI 媒体创作与多平台发布]]。

## FAQ

### Q: 和传统 Aegisub + 机翻 workflow 区别？
A: MioSub 强调链接一键全流程 + AI 上下文翻译 + 内置对齐，减少工具来回切换。

### Q: 只有音频可以吗？
A: v3 支持播客/有声书等纯音频。

### Q: 在线 demo 和桌面版一样吗？
A: demo 适合体验；大批量与压制建议桌面版 + 文档配置。

## 相关链接

- GitHub：https://github.com/corvo007/MioSub  
- 文档：https://miosub.app/docs  
- Demo：https://demo.miosub.app
