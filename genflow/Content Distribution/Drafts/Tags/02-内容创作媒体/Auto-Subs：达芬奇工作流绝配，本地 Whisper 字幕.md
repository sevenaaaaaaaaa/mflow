---
title: "Auto-Subs：达芬奇工作流绝配，本地 Whisper 字幕"
slug: auto-subs
date: 2026-06-15
updated: 2026-06-15
tags: [字幕, 达芬奇, Whisper]
categories: [AI工具]
summary: "Auto-Subs：达芬奇工作流绝配，本地 Whisper 字幕。平台：Mac/Win/Linux。"
focus_keyword: "Auto-Subs"
source: https://github.com/tmoroney/auto-subs
author: ""
status: draft
---

# Auto-Subs：达芬奇工作流绝配，本地 Whisper 字幕

> Mac/Win/Linux | [3.6k Stars](https://github.com/tmoroney/auto-subs/stargazers)

## 这是什么

Auto-Subs 是一款**完全本地运行的 AI 字幕生成工具**，不需要云端 API，不需要订阅付费。它使用 Whisper、Moonshine、Parakeet 等本地语音识别模型（基于 whisper-rs 和 ONNX Runtime），将音视频文件转写为字幕，支持 100+ 语言识别和即时翻译。

它的核心竞争力在于**直接集成专业视频编辑软件**：可作为 DaVinci Resolve 的内置脚本使用（Workspace → Scripts → AutoSubs），也支持 Adobe Premiere Pro 和 After Effects（通过 CEP 扩展）。生成的字幕可以直接作为 Resolve 的标题轨道、Premiere 的 caption track 或 After Effects 的文本图层，**无需任何导出/导入的中间步骤**。

最新 v3.5+ 版本新增了**说话人分离**（Speaker Diarization，支持按说话人分别着色）、字幕自由编辑和自动重新计时、词级动画宏（per-word highlighting）等功能。跨平台支持 macOS（Apple Silicon/Intel）、Windows（Vulkan/DirectML）、Linux，已上架 Homebrew Cask (`brew install --cask auto-subs`)。

## 适合谁 / 不适合谁

| 人群 | 是否推荐 | 原因 |
|------|----------|------|
| DaVinci Resolve/Premiere Pro 视频创作者 | ✅ 推荐 | 直接在剪辑软件中生成字幕，零导入导出，支持说话人分离和多语言翻译 |
| 需要批量生成本地字幕、注重隐私的用户 | ✅ 推荐 | 完全离线运行，音频/视频文件不离开本机，无需账号或 API Key |
| 仅需简单字幕、不想安装任何软件的用户 | ⚠️ 酌情 | 网页端工具（如剪映/CapCut）更轻量，Auto-Subs 适合已有专业剪辑工作流的用户 |

## 安装

```bash
# 方式一：macOS Homebrew（推荐）
brew install --cask auto-subs

# 方式二：从 GitHub Releases 下载安装包
# macOS Apple Silicon: AutoSubs-Mac-ARM.pkg
# macOS Intel:        AutoSubs-Mac-Intel.pkg
# Windows:            AutoSubs-windows-x86_64.exe
# Linux:              AutoSubs-linux-x86_64.deb / .rpm
# https://github.com/tmoroney/auto-subs/releases/latest

# 方式三：从源码构建
git clone https://github.com/tmoroney/auto-subs
cd auto-subs
# 详见 CONTRIBUTING.md 获取完整开发环境搭建步骤
```

注意：DaVinci Resolve 集成功能不支持 Mac App Store 版本，请从 blackmagicdesign.com 下载官方版本。

## 核心用法

1. **独立模式**：启动 AutoSubs → 选择音视频文件 → 选择识别模型（Whisper/Moonshine/Parakeet）和语言 → 点击 Transcribe → 编辑说话人标签和字幕文本 → 导出为 SRT/TXT 或复制到剪贴板
2. **DaVinci Resolve 模式**：打开 Resolve → Workspace → Scripts → AutoSubs → 选择时间线/音频源 → 设置语言和模型 → 点击 Transcribe → 在 AutoSubs 界面编辑后 Send 回 Resolve 时间线
3. **Premiere Pro/After Effects 模式**：启动 AutoSubs 和 Adobe 软件（CEP 扩展自动加载）→ 在 AutoSubs 中选择 Adobe 集成 → 导出时间线音频进行转录 → 导入生成的字幕到项目
4. **说话人分离**：在设置中启用 Speaker Diarization，转录完成后可为每位说话人指定不同颜色和标签
5. **字幕编辑**：在转录结果界面自由编辑文本，AutoSubs 会自动调整对应的时间戳；支持预设字幕样式（字体/颜色/背景），也可自定义
6. **高级设置**：VAD（语音活动检测）降噪、词级时间戳、模型下载管理器、多语言 UI 切换

## 注意事项与风险

- 本地 Whisper 模型需要下载（首次使用自动下载），模型越大识别越准确但处理越慢（large > medium > small > base > tiny）
- **Mac App Store 版 DaVinci Resolve 不受支持**，因沙箱限制无法加载外部脚本，请使用官网版本
- 说话人分离功能对音质敏感，嘈杂环境中准确率下降明显
- Windows 版推荐 Vulkan/DirectML 加速（NVIDIA GPU 用户可用 CUDA），纯 CPU 模式下大型模型处理速度较慢
- Apple Silicon Mac 上使用 CoreML 推理可获得最佳性能

## 与你现有工具的关系

- **与 DaVinci Resolve 内建字幕**：Resolve 内建字幕功能需手动输入，AutoSubs 自动化了 AI 识别+时间轴对齐+说话人分离的全流程，是 Resolve 工作流的强力补充
- **与 Lovart/LibTV**：完全互补。Lovart 生成视频内容 → Auto-Subs 为视频生成多语言字幕 → 最终作品可直接在 Resolve 中完成剪辑和字幕合流。还可以搭配 Voice-Pro 做多语言配音
- **与 MacWhisper/Buzz**：功能类似但面向不同工作流。MacWhisper 是通用音频转写工具，Auto-Subs 的优势在于直接嵌入专业剪辑软件。如果你主要用 DaVinci Resolve，Auto-Subs 是无缝选择；如果只是偶尔转写音频文件，MacWhisper 更轻量
- **与剪映/CapCut 自动字幕**：剪映的字幕功能更傻瓜化但需联网且仅支持有限语言，Auto-Subs 本地运行、支持 100+ 语言、隐私更可控

## 常见问题（FAQ）

**Q: Auto-Subs 和 DaVinci Resolve Studio 内建的自动字幕有什么区别？**
A: Resolve Studio 18.5+ 虽已加入 AI 字幕功能，但仅限 Studio 付费版且不支持说话人分离。Auto-Subs 免费开源，支持说话人分离、100+ 语言翻译、字幕自由编辑后自动重新计时、词级动画导出等更丰富的功能。

**Q: 字幕识别准确率如何？**
A: 准确率取决于模型大小：large 模型最佳但需要更多 VRAM/RAM，tiny 模型最快但准确率较低。对于清晰语音，medium 模型已能达到 95%+ 的准确率。在嘈杂环境或多说话人场景中建议开启去噪和说话人分离提升效果。

**Q: 支持哪些导出格式？能在 Final Cut Pro 中使用吗？**
A: 支持 SRT 和纯文本导出。Final Cut Pro 可以通过导入 SRT 文件的方式使用，但不支持 AutoSubs 的直接集成（目前仅支持 DaVinci Resolve 和 Adobe 的直接集成）。

## 相关链接

- 来源：https://www.ahhhhfs.com/79267/
- GitHub：https://github.com/tmoroney/auto-subs
