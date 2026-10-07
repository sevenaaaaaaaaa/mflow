---
title: "CyberVerse：自托管实时数字人 Agent 平台"
slug: cyberverse-digital-human-agent-platform
date: 2026-05-29
updated: 2026-05-29
tags: [CyberVerse, 数字人, WebRTC, 语音Agent, 自托管]
categories: [AI工具]
summary: CyberVerse 是自托管实时数字人 Agent 框架：WebRTC 低延迟语音、人设记忆、RAG、工具调用与可选数字人视频。一张参考图即可驱动形象，纯语音模式无需 Avatar GPU。
focus_keyword: CyberVerse
source: https://github.com/dsd2077/CyberVerse
status: draft
---

# CyberVerse：自托管实时数字人 Agent 平台

> 977+ stars | GPL v3 | Go + Python + WebRTC

## 这是什么

[CyberVerse](https://github.com/dsd2077/CyberVerse) 是开源 **实时数字人 Agent 框架**：以**语音交互**为主，支持 WebRTC 低延迟对话、可打断、人设记忆、RAG、工具调用；可选**数字人视频**（单张参考图驱动口型与表情）。

> One Photo. A Living Digital Human. — 一张照，让角色「活」起来。

架构：**PersonaAgent** 前台流畅对话 + **SubAgent** 后台异步执行搜索、研报、整理等长任务，不阻塞语音轮次。

## 适合谁 / 不适合谁

| 人群 | 是否推荐 | 原因 |
|------|----------|------|
| 要自建语音/数字人助手团队 | ✅ 推荐 | 全栈可自托管，模块可换 |
| 有 GPU 想做形象互动 | ✅ 推荐 | FlashHead / LiveAct 等后端 |
| 只想快速 ChatGPT 网页聊天 | ❌ 过重 | 需 Node/Go/Python/Conda |
| 无法接受 GPL v3 | ❌ 需注意 | 许可证为 GPL v3 |

## 安装与前置条件

- Node 18+、Go 1.25（`protoc-gen-go` 等）、Conda、Python 3.10+、FFmpeg
- **纯语音模式**：`inference.avatar.enabled: false` 时**不需要**本地 Avatar GPU
- API：支持阿里云 DashScope（Qwen）、火山 Doubao 等，可在 Web `/settings` 配置

```bash
git clone https://github.com/dsd2077/CyberVerse.git
cd CyberVerse
conda create -n cyberverse python=3.10 && conda activate cyberverse
cp infra/.env.example .env
cp infra/cyberverse_config.example.yaml cyberverse_config.yaml
# 编辑 .env 与 cyberverse_config.yaml（voice-only 设 avatar.enabled: false）
make setup
pip install -e ".[all]"
```

三终端启动：`make inference` | `make server` | `make frontend`

## 核心用法

### 实时语音 Agent

- 麦克风连续对话、打断 TTS、语音+文字混合输入
- 每角色独立音色、欢迎语、人格；支持**声音克隆**
- 纯语音模式仅推音频流，无 Avatar GPU

### WebRTC 与多模态

- P2P（内置 TURN）或 LiveKit SFU
- 支持摄像头/屏幕帧作为视觉输入（部分 omni 会话）

### 记忆与 RAG

- 对话历史本地持久化；可导入知识库、文档、传记材料做 RAG

### 数字人视频（可选）

- `inference.avatar.enabled: true` + GPU：参考图驱动实时面部与 lip-sync
- 无 GPU 可关闭，同一角色配置仍可用于语音

### 插件化栈

Brain、Voice、ASR、TTS、Tools、Memory、Face 均在 `cyberverse_config.yaml` 与 Web UI 切换供应商。

## 注意事项与风险

- **部署复杂度高**：多语言栈 + 三进程，生产需运维经验。
- **GPL v3**：衍生分发需遵守开源义务。
- **演示角色**：README 示例人物**不捆绑**、**非商用**。
- **API 成本**：实时语音 + 可选视频推理持续计费。
- **合规**：数字人仿真人像需尊重肖像权与当地法规。

## 与你现有工具的关系

- 团队形态产品可对比 [[Helio：AI 即同事的团队工作空间]]（SaaS 队友）vs CyberVerse（自托管）。
- 个人知识：角色 RAG 与 [[../01-AI-Agent生态/GBrain：AI Agent 的个人大脑层]]、[[../01-AI-Agent生态/LLM Wiki：让 AI 替你维护个人知识库]] 思路相近、实现分离。

## FAQ

### Q: 没有 GPU 能玩吗？
A: 能，关闭 avatar 即为纯语音 Agent，核心对话完整。

### Q: 支持哪些国内模型？
A: 文档示例含 DashScope、火山 Doubao，具体以 `cyberverse_config.yaml` 与 `/settings` 为准。

### Q: 和 LiveKit/OpenAI Realtime 区别？
A: CyberVerse 是带人设、记忆、可选数字人形象的一体化角色平台，而非单一 API 封装。

## 相关链接

- GitHub：https://github.com/dsd2077/CyberVerse
- 中文 README：`README.zh-CN.md`
- Demo 视频：仓库内 YouTube 链接（Alice / Lina / 小龙女等）
