---
title: "ClipSketch AI：视频瞬间转手绘故事板"
slug: clipsketch-ai-video-storyboard
date: 2026-05-29
updated: 2026-05-29
tags: [ClipSketch, 视频创作, Gemini, B站, 小红书]
categories: [AI工具]
summary: ClipSketch AI 解析 B 站与小红书链接，帧级标记精彩瞬间，用 Gemini 生成手绘故事板、三种种草文案与竖屏封面。适合二创与社媒运营，需 Google Gemini API Key。
focus_keyword: ClipSketch AI
source: https://github.com/RanFeng/clipsketch-ai
author: RanFeng
status: draft
---

# ClipSketch AI：视频瞬间转手绘故事板

> 1,747+ stars | React 19 + Gemini | 剪辑·素描

## 这是什么

[ClipSketch AI](https://github.com/RanFeng/clipsketch-ai)（剪辑·素描）是面向**视频创作者、社媒运营、二创爱好者**的 AI 工作台：

解析 **Bilibili / 小红书** 链接 → 帧级播放与标记 → 用 **Google Gemini** 将多帧合成**手绘风故事板** → 自动生成 **3 种小红书风格文案** → 可选角色融合与竖屏封面。

> 将视频瞬间转化为手绘故事。

## 适合谁 / 不适合谁

| 人群 | 是否推荐 | 原因 |
|------|----------|------|
| B 站/小红书二创、种草号 | ✅ 强烈推荐 | 链路为平台定制 |
| 需要故事板+文案+封面一条龙 | ✅ 推荐 | AI 工作室集成 |
| 不做中文社媒、无 Gemini Key | ❌ 不推荐 | 强依赖 Gemini |
| 只要专业 PR 时间轴剪辑 | ❌ 非剪辑替代 | 偏「瞬间→图文」 |

## 安装与前置条件

- Node.js 18+  
- [Google Gemini API Key](https://aistudio.google.com/)

```bash
git clone https://github.com/RanFeng/clipsketch-ai.git
cd clipsketch-ai
npm install
# .env.local
GEMINI_API_KEY=your_api_key_here
npm run dev
# http://localhost:3000
```

Docker：

```bash
docker run -d --restart=always --name clipsketch-ai -p 3000:3000 earisty/clipsketch-ai:latest
```

## 核心用法

### 1. 导入视频

粘贴 B 站或小红书分享链（可含文案）→ 导入 → 自适应竖屏/横屏布局。

### 2. 帧级标记

- 空格播放/暂停，`←` `→` 逐帧或智能步长  
- **`T` 键**快速打点，毫秒级时间轴  
- 可导出 TXT 时间轴或 ZIP 帧图包  

### 3. AI 工作室

| 步骤 | 模型（README） | 产出 |
|------|----------------|------|
| 故事板 | `gemini-3-pro-image-preview` | 多帧合一手绘分镜 |
| 文案 | `gemini-3-pro-preview` | 情感/干货/短句三风格 |
| 封面 | 同上 | 竖屏封面 |
| 精修 | 可 Batch API | 单格高清重绘 |

- **角色融合**：上传头像融入分镜  
- 响应式：PC / 平板 / 手机  

## 注意事项与风险

- **平台 ToS**：解析与二创需遵守 B 站、小红书服务条款与版权。  
- **API 费用**：多图生成 + 批量精修消耗 Gemini 额度；Batch 可省钱。  
- **模型 ID**：README 中的模型名随 Google 更新可能变化，以仓库为准。  
- **链接失效**：短链、私密视频可能解析失败。

## 与你现有工具的关系

- 长文/HTML 发布：[[html-anything：AI 时代的 HTML 编辑器]]、[[AIMedia：全自动 AI 媒体创作与多平台发布]]  
- 视频译制：[[../02-内容创作媒体/Violin：开源视频翻译与配音 Skill]]、[[../02-内容创作媒体/MioSub：一站式 AI 字幕生成与压制]]  
- PPT：[[codex-ppt-skill：图片式 PPT 生成 Skill]]（位图幻灯片，与故事板场景不同）

## FAQ

### Q: 支持抖音吗？
A: 当前 README 仅列 B 站与小红书，其它平台需自行验证或等更新。

### Q: 没有 Key 能预览播放器吗？
A: 导入与标记可能可用；AI 绘图/文案需 Gemini Key。

### Q: 和截图拼九宫格区别？
A: AI 将多帧**合成一张连贯手绘分镜**并写配套种草文案。

## 相关链接

- GitHub：https://github.com/RanFeng/clipsketch-ai  
- 多语言 README：en / ja / ko 版本在仓库
