---
title: "tools.video：不上传文件的在线视频处理工具集"
slug: tools.video
date: 2026-06-15
updated: 2026-06-16
tags: [视频处理, 在线工具, 隐私, 纯浏览器]
categories: [在线工具]
summary: "tools.video 是 SubEasy.ai 出品的纯浏览器端音视频处理工具箱，26 种工具覆盖压缩、转换、剪辑、字幕、音频提取等，100% 本地处理不上传文件，最大支持 50GB 文件，基于 ffmpeg.wasm 多线程硬件加速。"
focus_keyword: "tools.video"
source: https://tools.video
author: "SubEasy.ai"
status: draft
---

# tools.video：不上传文件的在线视频处理工具集

> 26 种视频/音频/图像处理工具，100% 浏览器本地运算 | 最大 50GB 文件 | 无需注册 | ffmpeg.wasm 驱动

## 这是什么

tools.video 是由 SubEasy.ai 团队打造的一套纯浏览器端音视频处理工具箱，包含 26 种常用工具，涵盖视频压缩、格式转换、剪辑、变速、裁剪、缩放、合并、补帧、静音、旋转、滤镜、截图、倒放、水印、字幕，以及音频提取/剪辑/转换/合并/变速等。所有处理都在浏览器本地完成，文件不会上传到任何服务器。

底层技术基于 mediabunny 和 ffmpeg.wasm，支持多线程和硬件加速，号称比传统纯 JavaScript 方案快 10 倍。支持 MP4、MOV、MKV、WebM、AVI、FLAC、WAV、AAC、OGG、M4A 等主流格式，以及 5.1/7.1 环绕声保留。

与同类在线工具（如 CloudConvert、Online-Convert）的最大区别在于：tools.video 完全不需要上传文件，对于涉及隐私的视频素材（如公司内部培训录像、未发布的创作素材）尤为适用。此外，免费且无需注册的设计大幅降低了使用门槛。

## 适合谁 / 不适合谁

| 人群 | 是否推荐 | 原因 |
|------|----------|------|
| 需要快速转换/压缩视频格式的普通用户 | ✅ 推荐 | 即开即用，零学习成本，常用格式全覆盖 |
| 对隐私敏感的内容创作者 | ✅ 推荐 | 文件不上传服务器，私密素材不离开本机 |
| 处理大文件（4K/8K/长视频）的用户 | ✅ 推荐 | 最大支持 50GB，多线程处理速度有保障 |
| 需要批量自动化处理的专业用户 | ⚠️ 酌情 | 基于浏览器单文件操作，不支持批量 / API 调用 |
| 需要专业调色/多轨编辑的用户 | ❌ 不推荐 | 这是基础工具箱，不是 DaVinci Resolve 或 Premiere 的替代品 |
| 使用低性能设备（老手机/上网本）的用户 | ⚠️ 酌情 | 本地运算依赖设备性能，大文件在旧设备上可能很慢 |

## 安装与前置条件

无需安装。打开浏览器访问 https://tools.video 即可使用。

- **浏览器要求**：支持 WebAssembly 的现代浏览器（Chrome/Firefox/Edge/Safari 最新版）
- **网络要求**：首次访问需加载 ffmpeg.wasm (~30MB)，后续可离线使用（缓存后）
- **无需注册、无需登录**

## 核心用法

### 视频压缩

1. 打开 https://tools.video/video-compress
2. 拖拽或选择视频文件（最大 50GB）
3. 选择压缩质量（可预览）
4. 等待本地处理后下载

### 视频格式转换

1. 打开 https://tools.video/video-convert
2. 上传文件，选择目标格式（MP4/MOV/MKV/WebM/AVI 等）
3. 下载转换后的文件

### 音频提取

1. 打开 https://tools.video/audio-extract
2. 上传视频文件
3. 自动提取音频并下载（WAV/MP3/AAC 等格式可选）

### 完整工具列表

| 类别 | 工具 |
|------|------|
| 视频 | 压缩、转换、剪辑、变速、裁剪、缩放、合并、补帧、静音、旋转、滤镜、截图、倒放、水印、字幕 |
| 音频 | 提取、剪辑、转换、合并、变速 |
| 图像/其他 | 图片转视频、视频转 GIF、色彩视频、动态照片、动态照片合并、媒体信息 |

## 注意事项与风险

- **性能取决于本机**：ffmpeg.wasm 在浏览器中运行，大文件处理速度取决于 CPU 和内存，老设备可能很慢
- **不支持批量**：每次只能处理一个文件，无批处理/API 接口
- **Safari 兼容性**：WebCodecs 在 Safari 上可能无法启用硬件加速，性能不如 Chrome/Edge
- **隐私边界**：虽然文件不上传，但浏览器扩展或恶意脚本理论上可能访问页面数据，处理敏感文件时注意浏览器环境安全
- **GitHub 仓库**：`github.com/terryops/tools.video-site` 仅为官网前端源码，核心处理逻辑（ffmpeg.wasm）来自社区项目

## 与你现有工具的关系

- 与 [[纯前端音视频转文字：浏览器端讯飞 API 长音频识别]] 同属纯浏览器端处理工具，可配合使用：先用 tools.video 提取音频，再用语音转文字工具识别
- 与 [[../01-AI-Agent生态/Claude Code 自动化剪辑：基于 Claude Code 的自动化剪辑工作流]] 互补：tools.video 做手动快速处理，Claude Code Skills 做自动化语义剪辑
- 速处理后素材可导入 [[../02-内容创作媒体/Toonflow：开源 AI 短剧生成工具]] 或 Lovart 做进一步 AI 生产

## FAQ

### Q: 真的完全不上传吗？
A: 是的。所有处理通过 ffmpeg.wasm（编译为 WebAssembly 的 FFmpeg）在浏览器本地执行，文件不会离开你的设备。可以断网后测试验证（缓存后）。

### Q: 免费吗？有文件大小限制吗？
A: 完全免费，无需注册。最大支持 50GB 文件，实际上受限于浏览器的内存管理能力。

### Q: 和 CloudConvert 等在线转换工具有什么区别？
A: CloudConvert 等需要上传文件到云端服务器再下载，tools.video 全程在浏览器本地完成，隐私性更好，但受限于本机性能。

### Q: 支持哪些格式？
A: 视频：MP4、MOV、MKV、WebM、AVI、TS、FLV、GIF、AIFF、OPUS、3GP、VOB、ASF、WMV。音频：FLAC、WAV、AAC、OGG、M4A、MP3。支持 5.1 和 7.1 环绕声保留。

## 相关链接

- 官网：https://tools.video
- 来源：https://www.ahhhhfs.com/80908/
- GitHub（官网源码）：https://github.com/terryops/tools.video-site
- ffmpeg.wasm 项目：https://github.com/ffmpegwasm/ffmpeg.wasm
- SubEasy.ai（母公司）：https://www.subeasy.ai
