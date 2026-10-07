---
title: "AirTranslate：macOS 系统音频实时转录翻译"
slug: airtranslate-macos-system-audio-translation
date: 2026-05-29
updated: 2026-05-29
tags: [AirTranslate, macOS, 实时翻译, 字幕, Swift]
categories: [AI工具]
summary: AirTranslate 捕获 Mac 系统内放音频（无需麦克风），实时转写并翻译，悬浮字幕覆盖会议、讲座与直播。支持 Apple Speech/Translation 与 GPT 模式，需较新 macOS。
focus_keyword: AirTranslate
source: https://github.com/himomohi/AirTranslate
status: draft
---

# AirTranslate：macOS 系统音频实时转录翻译

> 299+ stars | Swift | Apache-2.0 | 指南站 + DMG 安装

## 这是什么

[AirTranslate](https://github.com/himomohi/AirTranslate) 是开源 **macOS** 应用：直接捕获**系统正在播放的音频**（不走麦克风），实时转写成文字并翻译，以**悬浮字幕**显示在其它窗口之上。

适合：线上会议、外语视频、讲座、采访、直播等「声音在电脑里、不方便外放录麦」的场景。

- 用户指南：https://himomohi.github.io/AirTranslate/
- 最新版：[GitHub Releases](https://github.com/himomohi/AirTranslate/releases/latest)（推荐 DMG，亦提供 ZIP）

## 适合谁 / 不适合谁

| 人群 | 是否推荐 | 原因 |
|------|----------|------|
| Mac 用户看无字幕外语视频/会议 | ✅ 强烈推荐 | 系统音频直采 |
| 需要悬浮双语字幕 | ✅ 推荐 | Overlay 不挡操作 |
| Windows / Linux 用户 | ❌ 不支持 | 仅 macOS |
| 旧版 macOS | ❌ 需核对 | 指南要求较新系统（见官网 Requirements） |

## 安装与前置条件

- macOS（以[指南站 Requirements](https://himomohi.github.io/AirTranslate/) 为准，发布说明提及需较新版本）
- 下载 [AirTranslate.dmg](https://github.com/himomohi/AirTranslate/releases/latest/download/AirTranslate.dmg) 或 ZIP
- 系统需授予**屏幕录制/音频**等相关权限（安装后按引导开启）
- GPT 模式需自行配置 API Key（若启用）

## 核心用法

### 工作流

1. 启动 AirTranslate
2. 播放会议/视频/直播（系统音频）
3. 实时转写 + 翻译 → 悬浮窗显示
4. 按指南切换目标语言与引擎模式

### 转写与翻译引擎

- **Apple Speech**：系统级实时转写
- **Apple Translation**：系统翻译
- **GPT 模式**：可接入 OpenAI 兼容 API（以设置为准）

### 场景

- 开会听不懂外语 → 边看字幕边参与
- 看直播/课程无字幕 → 系统声轨直译

## 注意事项与风险

- **隐私**：系统音频涉及会议内容，勿在敏感场景误开悬浮窗录屏分享。
- **准确率**：口音、专业术语、BGM 会影响识别；GPT 模式有 API 费用。
- **仅 macOS**：无法替代 Win 上的同类工具。
- **权限**：未授权音频捕获时可能无输出，需在系统设置中检查。

## 与你现有工具的关系

- 与 [[Violin：开源视频翻译与配音 Skill]] 不同：Violin 是**文件级**配音导出；AirTranslate 是**实时听译**。
- 发布会后可把转写文本整理进 Obsidian，再用 [[../01-AI-Agent生态/给 Obsidian 接上免费 AI：opencode + 国产模型配置指南]] 润色。

## FAQ

### Q: 为什么要系统音频而不是麦克风？
A: 避免外放失真、回声，适合耳机听会、内录直播源。

### Q: 和同屏翻译插件区别？
A: 独立 App + 悬浮层，不依赖浏览器，捕获全系统音频。

### Q: 开源协议？
A: Apache-2.0；DMG 仅为安装介质，源码在仓库。

## 相关链接

- GitHub：https://github.com/himomohi/AirTranslate
- 指南站：https://himomohi.github.io/AirTranslate/
- Releases：https://github.com/himomohi/AirTranslate/releases
