---
title: "Buzz：离线 Whisper 音视频转录与翻译"
slug: buzz-offline-whisper-transcription
date: 2026-06-01
updated: 2026-06-01
tags: [Buzz, Whisper, 转录, 字幕, 离线, 开源]
categories: [AI工具]
summary: Buzz 基于 OpenAI Whisper，在本地离线转录/翻译音视频、YouTube 与麦克风实时录音，导出 SRT/VTT，支持 CUDA/Apple Silicon/Vulkan 加速与说话人识别，适合注重隐私的创作者。
focus_keyword: Buzz
source: https://github.com/chidiwilliams/buzz
author: chidiwilliams
status: draft
---

# Buzz：离线 Whisper 音视频转录与翻译

> MIT | OpenAI Whisper | 跨平台桌面 + CLI | 官方文档：https://chidiwilliams.github.io/buzz/

## 这是什么

[Buzz](https://github.com/chidiwilliams/buzz)（Buzz Captions）是在**个人电脑上离线**完成音频/视频**转录与翻译**的开源工具，引擎为 OpenAI [Whisper](https://github.com/openai/whisper)。

> Transcribe and translate audio offline on your personal computer.

与纯云端听写不同：模型在本地跑，适合会议录音、课程、播客、采访等**不愿把原始音频上传第三方**的场景。支持文件批量、YouTube 链接、麦克风**实时转写**，以及监视文件夹自动处理。

中文文档：https://chidiwilliams.github.io/buzz/zh/docs

## 适合谁 / 不适合谁

| 人群 | 是否推荐 | 原因 |
|------|----------|------|
| 需要离线 SRT/VTT、本地隐私 | ✅ 强烈推荐 | 默认离线 Whisper |
| 会议/演讲实时字幕（演示窗口） | ✅ 推荐 | Live 录音 + Presentation 模式 |
| 嘈杂音频、多人对话 | ✅ 推荐 | 语音分离 + 说话人识别 |
| 要一键链接→双语成片压制 | ⚠️ 用 [[MioSub：一站式 AI 字幕生成与压制]] | Buzz 偏转录导出，非全流程压制 |
| 仅 macOS 系统内放实时翻译 | ⚠️ 用 [[AirTranslate：macOS 系统音频实时转录翻译]] | AirTranslate 抓系统声+悬浮译 |
| 无 GPU、超大模型极慢 | ⚠️ 选小模型 | 可换 Whisper.cpp + Vulkan |

## 安装与前置条件

### macOS

```bash
brew install --cask buzz
```

或 [SourceForge](https://sourceforge.net/projects/buzz-captions/files/) / [GitHub Releases](https://github.com/chidiwilliams/buzz/releases) 下载 `.dmg`。

### Windows

SourceForge / Releases 安装包（**未签名**，安装时选「更多信息」→「仍要运行」）。

### Linux

```bash
flatpak install flathub io.github.chidiwilliams.Buzz
# 或
sudo apt-get install libportaudio2 libcanberra-gtk-module libcanberra-gtk3-module
sudo snap install buzz
```

### PyPI（开发者）

- **Python 3.12**、已安装 **ffmpeg**

```bash
pip install buzz-captions
python -m buzz
```

Nvidia GPU（Windows PyPI）需按 README 安装带 CUDA 的 `torch` 与相关 `nvidia-*` 包。

## 核心用法

### 输入来源

- 本地音频/视频文件  
- **YouTube 链接**  
- **麦克风实时转录**（含演示用 Presentation 窗口）  
- **监视文件夹**：新文件自动排队转录  

### 能力与导出

| 能力 | 说明 |
|------|------|
| 多后端 | Whisper；CUDA（Nvidia）、Apple Silicon、Whisper.cpp + **Vulkan** |
| 增强 | 转录前**语音分离**；**说话人识别** |
| 导出 | TXT、**SRT**、**VTT** |
| 查看器 | 搜索、播放控制、调速 |
| 自动化 | 快捷键、**CLI** 脚本批处理 |

### 典型流程

1. 导入文件或粘贴 YouTube URL → 选择模型与语言  
2. 转录完成 → 在高级查看器中校对  
3. 导出 SRT/VTT → 交给 [[MioSub：一站式 AI 字幕生成与压制]] 或 [[Violin：开源视频翻译与配音 Skill]] 做后续翻译/配音  

## 注意事项与风险

- **算力**：大模型（如 large）在 CPU 上很慢；有 GPU 时开启对应加速。  
- **Windows 安装包未签名**：企业环境可能拦截，需策略放行。  
- **PyPI 版本**：需 Python 3.12；与 Flatpak/Snap 为不同分发渠道。  
- **翻译质量**：依赖 Whisper 与所选模型，专业术语仍需人工校对。  
- **YouTube**：下载与使用须遵守平台服务条款与版权。  

## 与你现有工具的关系

| 工具 | 分工 |
|------|------|
| [[MioSub：一站式 AI 字幕生成与压制]] | 链接一键：下载→翻译→对齐→压制；Buzz 可作**本地转录源** |
| [[AirTranslate：macOS 系统音频实时转录翻译]] | Mac **系统内放**实时听译；Buzz 偏**文件/麦录+离线导出** |
| [[Violin：开源视频翻译与配音 Skill]] | 整段视频**配音回灌**；Buzz 产出字幕后可再接 Violin |
| [[../01-AI-Agent生态/LLM Wiki：让 AI 替你维护个人知识库]] | 转录稿可导入 vault，由 LLM Wiki 做结构化沉淀 |

## FAQ

### Q: Buzz 需要联网吗？
A: 转录/翻译在本地运行；首次可能需下载模型。YouTube 功能需网络拉取音源。

### Q: 和 Whisper 命令行有何区别？
A: Buzz 提供 GUI、实时录、监视目录、说话人/分离、多后端与 SRT 导出，降低上手成本。

### Q: 实时会议用 Buzz 还是 AirTranslate？
A: Mac 只听系统声、要悬浮译 → AirTranslate；要本地录音存档+字幕文件 → Buzz Live。

## 相关链接

- GitHub：https://github.com/chidiwilliams/buzz  
- 文档（中文）：https://chidiwilliams.github.io/buzz/zh/docs  
- 文档（英文）：https://chidiwilliams.github.io/buzz/docs  
- SourceForge：https://sourceforge.net/projects/buzz-captions/files/  
- Flathub：https://flathub.org/apps/io.github.chidiwilliams.Buzz
