---
title: "VisionCull Pro：本地 AI 选片工具，筛出模糊闭眼废片"
slug: visioncull-pro
date: 2026-06-15
updated: 2026-06-15
tags: [图片筛选, 本地AI, 摄影]
categories: [AI工具]
summary: "VisionCull Pro：本地 AI 选片工具，筛出模糊闭眼废片。平台：Mac/Win/Linux。"
focus_keyword: "VisionCull Pro"
source: https://github.com/YuChiHuaCheng/vision-cull-pro
status: draft
---

# VisionCull Pro：本地 AI 选片工具，筛出模糊闭眼废片

> Mac/Win/Linux | [53 Stars](https://github.com/YuChiHuaCheng/vision-cull-pro/stargazers)

## 这是什么

VisionCull Pro 是一款专为摄影师设计的**本地 AI 选片工具**，面向婚礼、活动、跟拍等高量照片场景。它运用本地 ONNX 模型（YuNet 人脸检测 + OCEC 闭眼识别），自动筛选出跑焦、模糊、闭眼、欠曝/过曝等废片，将数百张照片的精筛工作从人工数小时压缩到几分钟。

核心策略偏保守：**无法确认质量的照片不会直接淘汰，而是进入"待复核"队列**，避免误删好片。筛选结果**无损生成兼容 Lightroom 的 XMP 星级标签**，摄影师可直接在 Lightroom 中按评分排序、批量处理，完美融入现有工作流。

与 Excire、AfterShoot 等同类工具相比，VisionCull Pro 的最大差异在于**完全本地运行**——所有图像处理在你的电脑上完成，原片不会上传到任何云端服务器。架构为 Electron + React（前端）+ Python 图像分析器（后端），目前已支持 Mac/Win/Linux 三大平台。

## 适合谁 / 不适合谁

| 人群 | 是否推荐 | 原因 |
|------|----------|------|
| 婚礼/活动摄影师，每次出片数千张需快速初筛 | ✅ 推荐 | 本地 AI 自动标记废片并生成 XMP 标签，直接进入 Lightroom 精修流程，节省数小时人工 |
| 注重隐私、不愿将客户原片上传云端的摄影师 | ✅ 推荐 | 全流程本地运行，原片不离开电脑，无需登录账号或订阅付费 |
| 仅偶尔拍照、单次筛选量不足 50 张的用户 | ⚠️ 酌情 | 安装配置有一定门槛（Node.js + Python），少量照片手动筛选效率更高 |

## 安装

```bash
git clone https://github.com/YuChiHuaCheng/vision-cull-pro
cd vision-cull-pro

# 安装 Node.js 依赖
npm install

# 创建 Python 虚拟环境并安装依赖
uv venv .venv --python 3.11
uv pip install --python .venv/bin/python -r python/requirements.txt

# 启动开发模式
npm run dev:app
```

需要 Node.js 18+ 和 Python 3.10/3.11。RAW 文件处理需安装 exiftool（项目本地 `.local-tools/exiftool` 提供）。

## 核心用法

1. **创建项目**：启动应用后创建新项目，选择包含照片的文件夹
2. **开始筛选**：点击分析按钮，Python 分析器将依次对每张照片做人脸检测、闭眼识别、曝光评估
3. **查看结果**：结果分为三类——保留（Keep）、淘汰（Reject）、待复核（Needs Review）
4. **人工复核**：在"待复核"队列中快速浏览，手动确认保留或淘汰
5. **导出 XMP**：筛选完成后导出 XMP sidecar 文件（星级标签），Lightroom 可直接读取
6. **导出照片**：按偏好设置选择输出位置，可将保留的照片复制/移动到指定目录
7. **命令行评测**：`npm run eval:local -- /path/to/photos 200` 可对样例集跑基准评测，输出详细报表到 `reports/` 目录

## 注意事项与风险

- v1 阶段为**本机稳定版**，不包含签名安装包和跨机器分发能力
- 本地引擎偏保守，跑焦/模糊阈值可调节，但默认设定下部分边缘情况会进入待复核
- RAW 文件支持依赖 exiftool，若 exiftool 不可用，RAW 预览和元数据读取会降级
- 不支持云端 AI provider，无法使用 GPT-4V 等高级视觉模型做语义理解
- Python 分析器目前主要针对人像场景优化，风景/静物筛选能力较弱
- macOS 首次启动可能会提示安全警告，需在系统设置中放行

## 与你现有工具的关系

- **与 Lightroom 的关系**：VisionCull Pro 是 Lightroom 的前置选片工具，生成 XMP 星级标签后，你可以在 Lightroom 中按评分排序，直接开始精修。不替代 Lightroom，而是补全其缺失的 AI 初筛能力
- **与 Lovart/LibTV**：职责互补。Lovart/LibTV 面向 AI 图像生成，VisionCull Pro 面向已有照片的筛选管理。可以搭配使用：拍摄完成后先用 VisionCull Pro 选片，然后用 Lovart 对保留照片做 AI 增强或风格化处理
- **与 Excire/AfterShoot**：功能目标相似但路线不同。Excire 是付费 Lightroom 插件、AfterShoot 是订阅制，VisionCull Pro 完全免费开源、本地部署

## 常见问题（FAQ）

**Q: VisionCull Pro 的闭眼检测准确率如何？**
A: 闭眼检测基于 OCEC ONNX 模型，在正面、光线充足的肖像场景下准确率较高。侧脸、墨镜、极端低光等场景可能漏检，会进入"待复核"队列而非直接淘汰。

**Q: 和直接用人脸识别 API（如 AWS Rekognition）有什么区别？**
A: VisionCull Pro 完全本地运行，原片不上传任何服务器。云端 API 方案需要付费且涉及客户隐私问题。本地方案的缺点是模型能力受限于设备性能，不适合需要语义级理解（如"表情是否自然"）的场景。

**Q: 支持视频截帧选片吗？**
A: 当前 v1 版本仅支持 JPG/PNG 等静态图片格式，不支持视频截帧。RAW 文件支持受 exiftool 可用性影响，计划在后续版本扩展。

## 相关链接

- GitHub：https://github.com/YuChiHuaCheng/vision-cull-pro
