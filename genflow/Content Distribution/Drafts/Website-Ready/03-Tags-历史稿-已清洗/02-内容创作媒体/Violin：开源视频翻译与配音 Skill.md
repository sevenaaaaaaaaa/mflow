---
title: "Violin：开源视频翻译与配音 Skill"
slug: violin-open-source-video-translation
date: 2026-05-29
updated: 2026-05-29
tags: [Violin, 视频翻译, 配音, Claude Code, skill]
categories: [AI工具]
summary: Violin 将视频转写、翻译、TTS 配音并回灌成片，支持 33 种目标语言、CLI/Web/Claude Code skill。需 Python 3.10+、ffmpeg 与 Together 等 API Key。
focus_keyword: Violin
source: https://github.com/shang-zhu/violin
status: draft
---

# Violin：开源视频翻译与配音 Skill

> 842+ stars | MIT | CLI + FastAPI + Claude Code skill

## 这是什么

[Violin](https://github.com/shang-zhu/violin) 是**开源视频翻译 Skill**：上传视频 → 转写 → 翻译 → 合成目标语言配音 → 重新封装 MP4，可选 SRT 字幕。

提供三种入口：**CLI**、**Web/API**（`violin-api`）、**Claude Code skill**（`violin --install-skill`）。
在线演示：https://www.violin-ai.com

## 适合谁 / 不适合谁

| 人群 | 是否推荐 | 原因 |
|------|----------|------|
| 需整段视频外语配音的创作者 | ✅ 推荐 | 端到端 pipeline |
| Claude Code / Cursor 用户 | ✅ 推荐 | 自然语言调 skill |
| 只要字幕条、不重配音 | ⚠️ 用 [[MioSub：一站式 AI 字幕生成与压制]] | Violin 偏音轨替换 |
| 不愿配 API Key / 无 ffmpeg | ❌ 不推荐 | 依赖外部 STT/LLM/TTS |

## 安装与前置条件

- **Python 3.10+**、**ffmpeg** 在 PATH
- 推荐：`uv tool install violin`
- API Key（示例）：`export TOGETHER_API_KEY=...`（[Together](https://api.together.ai)）
- 可插拔栈：Together / OpenAI / ElevenLabs 等，**一个 YAML** 配置各阶段

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
uv tool install violin
export TOGETHER_API_KEY=...
```

## 核心用法

### CLI

```bash
violin lecture.mp4 lecture_zh.mp4 --language Chinese
```

### Web

```bash
violin-api
# http://127.0.0.1:8000  UI
# http://127.0.0.1:8000/docs  API
```

### Claude Code skill

```bash
violin --install-skill
# 会话中：please use the violin skill to translate ... into Chinese
```

### 特性摘要

- **33 种目标语言**；16 种常用语精选原生感声音（Cartesia Sonic 3 + ElevenLabs）
- **片内 Q&A**：基于字幕 + 采样帧回答视频内容问题
- 自然语言选声、6 种风格配置（实验）
- Pipeline：ffmpeg 抽音频 → Whisper Large v3 → LLM 翻译 → TTS → ffmpeg 对齐合成

### 路线图（README）

- 语音克隆、口型同步（进行中/计划中）

## 注意事项与风险

- **成本**：长视频 ×（转写 + LLM + TTS）API 费用显著。
- **版权**：翻译传播他人视频需授权。
- **口型**：当前非 lip-sync，观感为配音/字幕向。
- **质量**：快语速、多人重叠语音可能对齐困难。

## 与你现有工具的关系

- 字幕条工作流：[[MioSub：一站式 AI 字幕生成与压制]]
- Agent 生态：与 [[../01-AI-Agent生态/The Agency：105k Star 的 AI Agent 专家库]]、[[../01-AI-Agent生态/给 Obsidian 接上免费 AI：opencode + 国产模型配置指南]] 同类 skill 安装方式
- 博客：[Together.ai 介绍文](https://www.together.ai/blog/violin-open-source-translation-skill)

## FAQ

### Q: 和 MioSub 怎么分工？
A: MioSub 偏字幕编辑与压制；Violin 偏**替换音轨**的译制成片。

### Q: 必须 Together 吗？
A: 否，栈可换 OpenAI/ElevenLabs 等，见项目 YAML 配置。

### Q: 最短试用方式？
A: 打开 violin-ai.com 上传短 clip，或本地 `violin-api`。

## 相关链接

- GitHub：https://github.com/shang-zhu/violin
- Demo：https://www.violin-ai.com
- Blog：https://www.together.ai/blog/violin-open-source-translation-skill
