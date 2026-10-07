---
title: "Image Provenance：纯浏览器端 AI 图片溯源，检测签名与 EXIF"
slug: image-provenance
date: 2026-06-15
updated: 2026-06-15
tags: [图片溯源, EXIF, AI检测]
categories: [AI工具]
summary: "Image Provenance：纯浏览器端 AI 图片溯源，检测签名与 EXIF。平台：Web。"
focus_keyword: "Image Provenance"
source: https://github.com/863401402/image-provenance
status: draft
---

# Image Provenance：纯浏览器端 AI 图片溯源，检测签名与 EXIF

> 185 stars | MIT | 100% 客户端，图片不上传

## 这是什么

[Image Provenance](https://github.com/863401402/image-provenance) 是一款**纯浏览器端的 AI 图片溯源分析工具**。你拖入一张图片，它从三个维度告诉你这张图的来历：AI 生成签名（C2PA/SynthID/DALL-E/Midjourney 等）、EXIF/XMP/IPTC 元数据全展开、以及频域分析（65 个特征 + FFT 热图检测 AI 生成痕迹）。

核心特点：零构建、单 HTML + ES Modules，仅依赖两个 CDN 库（`exifr` 读元数据、`piexifjs` 注入 EXIF），其余 FFT/DCT/DWT、JUMBF 嗅探、8 项水印扰动全部手写。数据 100% 在浏览器本地处理，图片从不离开你的设备。

与在线 AI 检测网站不同：它不是深度学习分类器，而是基于 Corvi 2023 等研究的频域特征 + 规则判定，准确率约 70-85%。但它提供**三层信号**（强：C2PA 签名直接声明的 AI 来源；中：EXIF 中软件名暗示；频域：自己看热图判断），让你不盲信单一数字。

## 适合谁 / 不适合谁

| 人群 | 是否推荐 | 原因 |
|------|----------|------|
| 社交媒体编辑核实新闻图片真伪 | ✅ 推荐 | 查看 EXIF 时间/地点/GPS，检测 AI 签名 |
| AI 创作者检查自己的生成图元数据 | ✅ 推荐 | 确认 C2PA/Content Credentials 签名是否完整 |
| 摄影社区管理员审核 AI 生成图 | ✅ 推荐 | 频域分析 + 元数据交叉验证 |
| 需要 100% 准确判断 AI 图的法务场景 | ❌ 不推荐 | 非深度分类器，准确率约 70-85%，不能做法庭证据 |
| 单纯想看 EXIF 信息 | ⚠️ 酌情 | 功能比纯 EXIF 查看器重，但可作为一站式工具 |

## 安装

```bash
# 克隆仓库
git clone https://github.com/863401402/image-provenance
cd image-provenance
# ES Modules + Web Worker 需要 HTTP 协议，file:// 打不开
python3 -m http.server 8000
# 然后打开 http://localhost:8000
```

也可以直接使用在线演示：[863401402.github.io/image-provenance](https://863401402.github.io/image-provenance/)

## 核心用法

1. 打开在线演示或本地部署页面
2. 拖入或选择一张图片
3. 查看四个面板：

**溯源检测主视图**——显示 AI 生成签名检测结果：
- C2PA / Content Credentials（Adobe/徕卡等相机签名）
- Google SynthID
- OpenAI DALL-E / Sora
- Midjourney、Stable Diffusion / Flux、Adobe Firefly

带强/中/弱置信度徽标，只有强中信号才报"命中"。

**元数据详情**——EXIF / XMP / IPTC / ICC 全展开，GPS 坐标带隐私警告和 OpenStreetMap 地图链接，XMP 编辑历史完整时间线。

**频域分析**——Web Worker 中跑 65 个特征 + viridis FFT 热图 + 对数径向谱 + 12 条启发式规则的加权判定。

**图片转换**——字节级剥 C2PA → Canvas 重编码 → 可选水印扰动 → 注入 17 款真实相机 EXIF（iPhone 17 Pro Max / Sony α1 II / Leica Q3 等）。

**水印扰动 v2**——8 项技术（含真 2D-FFT 相位扰动）+ 4 档预设（轻量/推荐/强力/极限），用于学术研究用途的去识别与鲁棒性评估。

## 注意事项与风险

- **准确率有限**：频域分析对现代扩散模型的二分类准确率约 70-85%，不高不低。强信号（C2PA/EXIF 直接声明）可靠，频域信号仅供参考，不盲信。
- **水印扰动伦理**：工具设计用于隐私去识别与鲁棒性评估，不鼓励用于虚假信息传播、身份伪造或欺诈。立场参考 WAVES (NeurIPS 2024)。
- **浏览器兼容**：ES Modules + Web Worker 需要现代浏览器，`file://` 协议无法运行。
- **GPS 隐私**：EXIF 中的 GPS 坐标会自动标记隐私警告，并链接到 OpenStreetMap 地图，方便确认拍摄地点是否有意暴露。

## 与你现有工具的关系

- 与 [[../05-开发技术栈/Privacy Filter：本地隐私脱敏，发给 AI 前清理敏感文本]] 同为「浏览器端零上传」安全工具：一个管文本脱敏，一个管图片溯源，组合使用覆盖图文隐私。
- 在社交媒体运营流程中，先经 Image Provenance 核验图片来源，再用 [[AIMedia：全自动 AI 媒体创作与多平台发布]] 进行内容分发。
- 如果处理视频，可配合 [[FunClip：开源精准视频剪辑]] 提取关键帧再做溯源分析。

## FAQ

### Q: 能 100% 判断一张图是不是 AI 生成的吗？
A: 不能。这类工具当前技术的二分类准确率约 70-85%。C2PA 数字签名（如徕卡相机）和 EXIF 中明确的 AI 软件名（如 "DALL-E"）是强信号，基本不会错。纯频域分析只能作为参考——建议结合图片内容的常识判断。

### Q: 水印扰动功能有什么用？
A: 学术研究用途为主。例如：测试自己的图片在各种水印攻击下的鲁棒性，或者在上传/分享前移除可识别个人身份的隐写水印（隐私去识别）。不鼓励用于造假或欺诈。

### Q: 为什么拖入图片后部分检测显示"无信号"？
A: 正常现象。大部分普通图片没有 AI 签名或 C2PA 元数据。只有经过 Adobe Camera Raw、Midjourney 等特定工具处理或生成的图片才会写入这些信息。无信号不代表是假图。

## 相关链接

- 在线演示：https://863401402.github.io/image-provenance/
- GitHub：https://github.com/863401402/image-provenance
