---
title: "FreeCut：开源浏览器视频编辑器，免安装本地剪辑"
slug: freecut
date: 2026-06-15
updated: 2026-06-15
tags: [视频编辑, 浏览器, 免安装]
categories: [在线工具]
summary: "FreeCut：开源浏览器视频编辑器，免安装本地剪辑。平台：Web。"
focus_keyword: "FreeCut"
source: https://github.com/walterlow/freecut
status: draft
---

# FreeCut：开源浏览器视频编辑器，免安装本地剪辑

> 1.4k+ stars | TypeScript | MIT | 纯浏览器运行，无需安装上传

## 这是什么

## 这是什么

FreeCut 是一个运行在浏览器中的专业级视频编辑器。不需要安装任何软件，不需要把视频上传到云端——所有编辑工作都在你本地的 Chromium 浏览器中完成。它利用 WebGPU、WebCodecs、OPFS（源私有文件系统）和 File System Access API 等现代浏览器能力，实现了多轨道编辑、关键帧动画、实时预览和高品质导出。

核心方案是"把桌面级剪辑体验搬进浏览器"。它支持多轨道时间线（视频、音频、文字、图片、形状、遮罩）、25 种混合模式、GPU 加速的特效和转场、贝塞尔关键帧编辑器、内置 Whisper 转录生成字幕、本地 Kokoro TTS 语音合成和 MusicGen 音乐生成。所有项目文件以纯文本格式保存在你选择的本地文件夹中，媒体素材不会被复制，仅在编辑时引用原始文件。

与 Clipchamp、Canva 等在线剪辑工具的最大差异在于：FreeCut 完全开源（MIT 协议），不上传任何数据，渲染和导出都在本地浏览器中通过 WebCodecs 完成，并且提供接近 Premiere Pro 级别的编辑能力——包括源监视器、三点编辑、滑移/滑动工具、速率伸缩、色度抠像和 GPU 色彩示波器（波形图、矢量图、直方图）。

## 适合谁 / 不适合谁

| 人群 | 是否推荐 | 原因 |
|------|----------|------|
| 需要快速剪辑的创作者/开发者 | ✅ 推荐 | 免安装、免上传，打开即用；基于 WebGPU 的实时预览和导出速度接近原生软件 |
| 对隐私敏感的视频工作者 | ✅ 推荐 | 所有数据本地处理，项目文件以纯文本保存，无需信任任何云端服务 |
| 追求 Premiere/DaVinci 完整工作流的专业人士 | ⚠️ 酌情 | 功能强大但仍在快速迭代中，部分专业特性（如协作、高级调色）尚未达到桌面 DAW 水平 |
| 非 Chromium 浏览器用户（Firefox/Safari） | ❌ 不推荐 | 依赖 WebGPU、WebCodecs、OPFS 等 Chromium 独有 API，Firefox/Safari 无法运行 |

## 安装

FreeCut 提供 [在线版本](https://freecut.net)，打开即用。如需本地开发调试：

```bash
# 要求 Node.js 22+，npm 11+，现代 Chromium 浏览器
git clone https://github.com/walterlow/freecut
cd freecut
npm install
npm run dev
# 浏览器打开 http://localhost:5173（推荐 Chrome/Edge/Brave/Arc 113+）
```

注意：Brave 浏览器默认禁用 File System Access API，需在 `brave://flags/#file-system-access-api` 中启用。

## 核心用法

1. **创建项目**：首次打开后选择一个工作区文件夹（用于保存项目文件），点击"New Project"创建项目。
2. **导入素材**：直接将视频、音频、图片、GIF、SVG 拖入媒体库，素材不会被复制。
3. **时间线编辑**：将素材拖入多轨道时间线，使用 `V` 选择工具、`C` 剃刀工具、`R` 速率伸缩工具等进行剪辑。支持拆分（`Ctrl+K`）、连接（`Shift+J`）、波纹删除（`Ctrl+Delete`）等操作。
4. **特效与关键帧**：在效果面板添加模糊、色彩校正、色度抠像等特效；在关键帧编辑器中设置贝塞尔缓动曲线实现动画。
5. **AI 辅助**：内置 Whisper 自动生成字幕；语义场景搜索可快速定位视频中的特定画面；Kokoro TTS 可本地合成语音旁白。
6. **导出**：支持 MP4/WebM/MOV/MKV 容器，H.264/H.265/VP8/VP9/AV1/ProRes 编码，以及 MP3/AAC/WAV 音频导出，全部在浏览器中本地完成。

快捷键速查：`Space` 播放/暂停，`I`/`O` 标记入/出点，`,`/`.` 插入/覆盖编辑，`Ctrl+Shift+E` 导出，`Ctrl+Shift+F` 打开场景搜索。

## 注意事项与风险

- **浏览器兼容性**：仅支持 Chrome/Edge/Brave/Arc 等 Chromium 113+ 浏览器。Firefox 和 Safari 因缺失 WebGPU/WebCodecs 支持无法使用。
- **GPU 要求**：WebGPU 功能需要较新的显卡和驱动。部分老设备上的效果和转场可能自动降级到 Canvas 2D 备选方案，性能会显著下降。
- **项目不可移植**：项目文件夹结构依赖 File System Access API，移动到其他电脑后可能需要重新链接媒体文件。
- **目前不接受 PR**：项目声明"开源但未开放贡献"，只接受 Issue 和 Discussion。如想参与开发需先关注项目动态。
- **内存占用**：处理高分辨率视频时浏览器内存占用可能较高，建议关闭其他标签页。

## 与你现有工具的关系

- 与 [[../01-AI-Agent生态/FunClip：开源精准视频剪辑]] 互补：FunClip 擅长基于 ASR 的精准裁剪，FreeCut 提供完整的多轨道编辑和特效能力。可以先用 FunClip 粗剪素材，再到 FreeCut 中精编。
- 与 [[LosslessCut：开源跨平台无损视频剪辑]] 的场景不同：LosslessCut 专注无损快速切割，FreeCut 侧重完整的编辑工作流和特效。
- 与 [[../05-开发技术栈/tools.video：不上传文件的在线视频压缩工具]] 配合：在 FreeCut 中完成编辑后，如需进一步压缩可使用 tools.video。
- 导出后的视频素材可用于 [[Toonflow：开源 AI 短剧生成工具]] 或 [[Jellyfish：开源 AI 短剧工作流，解决人物漂移]] 等 AI 视频生成工具。

## FAQ

### Q: FreeCut 和 Clipchamp/Canva 有何不同？
A: FreeCut 完全开源、不上传任何数据、所有渲染在本地浏览器完成。Clipchamp 和 Canva 是商业服务，部分功能需要联网和付费订阅。

### Q: 能在移动端使用吗？
A: 目前不支持。FreeCut 依赖桌面浏览器的 File System Access API 和完整的 WebGPU 支持，移动端浏览器尚不具备这些能力。

### Q: 导出的视频有水印吗？
A: 没有。FreeCut 完全开源免费，导出无任何水印或限制。

## 相关链接

- 官方在线版：https://freecut.net
- 用户文档：https://freecut.net/docs
- GitHub：https://github.com/walterlow/freecut
