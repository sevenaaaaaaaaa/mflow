---
title: "AirTranslate：Mac 系统音频实时翻译，悬浮字幕"
slug: airtranslate
date: 2026-06-15
updated: 2026-06-15
tags: [翻译, 实时字幕, macOS]
categories: [AI工具]
summary: "AirTranslate：Mac 系统音频实时翻译，悬浮字幕。平台：Mac。"
focus_keyword: "AirTranslate"
source: https://github.com/himomohi/AirTranslate
status: draft
---

# AirTranslate：Mac 系统音频实时翻译，悬浮字幕

> Mac | [331 Stars](https://github.com/himomohi/AirTranslate/stargazers)

## 这是什么

AirTranslate 是一款专为 macOS 设计的系统音频实时翻译工具。它通过 ScreenCaptureKit 直接捕获 Mac 上正在播放的系统音频（如 YouTube 视频、Zoom 会议、在线课程、直播等），实时转为文字并同步翻译成目标语言，最终以**悬浮字幕窗口**叠加在任意应用上方显示。

默认采用 **Apple 本地框架**（Apple Speech + Apple Translation）完成转写与翻译，完全离线运行、数据不出机器。同时也支持可选的 **OpenAI Realtime** 和 **Gemini Live** API 模式，在需要更高质量翻译时按需启用。所有 API Key 存储在 macOS 钥匙串中，不上传至任何服务器。

与 MacWhisper、Buzz 等通用语音转文字工具不同，AirTranslate 的核心差异在于"系统音频优先"——你不需要用麦克风对着扬声器录音，也不需要配置虚拟声卡（如 BlackHole）来做音频路由。启动即捕获，字幕即浮现，彻底解决跨语言会议、外语课程、无字幕视频等场景的听懂难题。

## 适合谁 / 不适合谁

| 人群 | 是否推荐 | 原因 |
|------|----------|------|
| 经常参加英文会议、外语课程、观看无字幕视频的 Mac 用户 | ✅ 推荐 | 系统音频直接捕获，悬浮字幕叠加任何应用，零配置即可实时翻译 |
| 需要本地隐私优先、不依赖云端的翻译方案 | ✅ 推荐 | Apple 模式完全离线，所有转录文件为本地纯文本 `.txt`，API Key 存于 Keychain |
| Windows 用户或需要专业人工精翻的场景 | ⚠️ 酌情 | 仅支持 macOS 26+，API 翻译模式依赖网络且质量不及人工翻译 |

## 安装

```bash
# 方式一：直接下载 DMG（推荐）
# 从 GitHub Releases 下载最新 AirTranslate.dmg
# https://github.com/himomohi/AirTranslate/releases/latest
# 打开 DMG，将 AirTranslate.app 拖入 Applications

# 方式二：从源码构建
git clone https://github.com/himomohi/AirTranslate
cd AirTranslate
./script/build_and_run.sh
```

首次打开时 macOS 可能提示"无法验证开发者"，右键点击应用选择"打开"即可。macOS 26.0+ 为系统要求，需授予屏幕录制、系统音频录制、语音识别三项权限。

## 核心用法

1. **选择语言**：在侧边栏分别选择源语言和目标语言，中间按钮可一键互换方向
2. **选择模式**：Apple 模式（本地免费）、GPT 模式（需 OpenAI API Key）、Gemini Live 模式（需 Google API Key）
3. **配置 API**（可选）：若使用 API 模式，点击齿轮图标进入设置，输入对应的 API Key，Key 自动存入系统钥匙串
4. **启动捕获**：点击 Start 按钮，然后播放 Mac 上的任意音频（会议/视频/课程）
5. **读取翻译**：主界面同时展示原文和译文，或打开悬浮字幕窗口让翻译浮在视频上方
6. **停止保存**：点击 Stop 后，当前转录自动保存为纯文本文件，路径为 `~/Library/Application Support/AirTranslate/Transcripts/`
7. **回看历史**：在 Transcript Library 中管理、编辑、删除历史转录记录

## 注意事项与风险

- 系统要求 **macOS 26.0 或更高版本**（2026 年发布），旧版本 Mac 无法使用
- Apple 翻译模式需提前在系统设置 → 通用 → 语言与地区 → 翻译语言中下载对应语言包
- GPT/Gemini API 模式按 token 计费，需自行承担 API 调用成本
- ScreenCaptureKit 权限为系统级要求，若翻译无法启动请检查隐私与安全性设置
- 悬浮字幕窗口在部分全屏应用中可能层级异常，可切换为非全屏模式使用
- 项目目前不支持 Windows/Linux，无跨平台计划

## 与你现有工具的关系

- **与 MacWhisper/Buzz**：AirTranslate 侧重点不同——MacWhisper 是本地音频文件转写，AirTranslate 是系统音频实时流翻译。两者互补，可以用 MacWhisper 做文件批量转写，用 AirTranslate 做实时场景
- **与 Lovart/LibTV**：职责完全不同。Lovart/LibTV 面向视频/图像生成，AirTranslate 面向音频翻译。可搭配使用：用 Lovart 生成视频后，用 AirTranslate 验证多语言字幕效果
- **与 Language Reactor（原 LLN）**：Language Reactor 是浏览器扩展，只能在浏览器内为 YouTube/Netflix 加字幕；AirTranslate 是系统级 App，覆盖所有 Mac 音频来源

## 常见问题（FAQ）

**Q: AirTranslate 和对着麦克风用 Google 翻译有什么区别？**
A: AirTranslate 直接从系统音频通道捕获声音，零音质损失、无环境噪声干扰。用麦克风对着扬声器会导致回声和音质下降，翻译准确率明显更低。

**Q: Apple 模式翻译质量如何？需要联网吗？**
A: Apple 翻译完全离线运行，质量足以应付日常会议和课程理解。GPT/Gemini 模式翻译更流畅自然，但需要联网和 API Key。Apple 翻译语言包需提前下载（系统设置中操作），不下载则无法使用对应语言对。

**Q: 支持中英文互译以外的语言吗？**
A: 支持 Apple 翻译覆盖的全部语言对（含中日韩德法西等主流语言），具体取决于系统版本。GPT/Gemini 模式理论上支持模型所覆盖的所有语言。

## 相关链接

- GitHub：https://github.com/himomohi/AirTranslate
