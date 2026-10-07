---
title: "CyberVerse：开源数字人 Agent 平台，照片生成实时视频通话"
slug: cyberverse
date: 2026-06-15
updated: 2026-06-15
tags: [数字人, 视频通话, Agent]
categories: [AI工具]
summary: "CyberVerse：开源数字人 Agent 平台，照片生成实时视频通话。平台：Web/Docker。"
focus_keyword: "CyberVerse"
source: https://github.com/dsd2077/CyberVerse
status: draft
---

# CyberVerse：开源数字人 Agent 平台，照片生成实时视频通话

> 1.2k stars | GPL-3.0 | 自托管 | WebRTC 实时通话

## 这是什么

[CyberVerse](https://github.com/Lynpoint/CyberVerse) 是一个**开源自托管的实时数字人 Agent 平台**。一张照片就能驱动一个能看、能听、能说的数字人，与你进行实时视频通话级别的语音/视频交互。

架构核心：**多 Agent 架构 + WebRTC 实时通信 + 可插拔模块**。PersonaAgent 在前台维持流畅对话、响应打断、处理上下文切换；后台 SubAgent 异步执行搜索、整理、摘要等长任务。WebRTC 管道支持直接 P2P 或 LiveKit SFU 模式，可接收用户摄像头画面实现「面对面」交互。

与 D-ID、HeyGen 等商业数字人平台不同：CyberVerse 完全自托管、开源（GPL-3.0），数据 100% 在你自己的服务器上。可选开启数字人视频（需 GPU），也可关闭视频以纯语音 Agent 模式运行（无需 GPU）。支持 FlashHead 和 LiveAct 两种 Avatar 后端，语音克隆、自定义角色人格、知识库 RAG。

## 适合谁 / 不适合谁

| 人群 | 是否推荐 | 原因 |
|------|----------|------|
| 想做 AI 虚拟伴侣/角色扮演 | ✅ 推荐 | 角色记忆 + 人格配置 + 语音克隆，体验完整 |
| 企业搭建客服/前台数字人 | ✅ 推荐 | 自托管保护数据，RAG 知识库可加载业务文档 |
| 想做直播数字人 | ✅ 推荐 | 支持音视频直播输出 |
| 只有轻量服务器（无 GPU） | ⚠️ 酌情 | 纯语音模式 OK，但视频模式需要 GPU（见硬件表） |
| 只想简单生成一个会说话的图片 | ❌ 不推荐 | 这套太重了，用 D-ID Studio 一键搞定更快 |

## 安装

**前置条件**：Node 18+、Go 1.25、Conda、Python 3.10+、FFmpeg、libopus-dev 等。

```bash
# 1. 克隆
git clone https://github.com/dsd2077/CyberVerse.git
cd CyberVerse

# 2. Python 环境
conda create -n cyberverse python=3.10
conda activate cyberverse

# 3. 配置环境变量
cp infra/.env.example .env
# 编辑 .env，填入通义千问或豆包 API Key

# 4. 纯语音模式（无需 GPU）
cp infra/cyberverse_config.example.yaml cyberverse_config.yaml
# 编辑 cyberverse_config.yaml，设置 inference.avatar.enabled: false

# 5. 安装依赖
make setup
pip install -e ".[all]"

# 6. 启动（3 个终端）
make inference  # 终端1：推理服务
make server     # 终端2：Go API 服务
make frontend   # 终端3：前端 dev server
```

打开 `http://localhost:5173`，Web UI 中配置角色和 API 密钥即可开始对话。

## 核心用法

**纯语音 Agent（零 GPU）**：`inference.avatar.enabled: false` 即可。通过麦克风与 Agent 实时对话，支持打断、暂停恢复、混合语音+文本输入，角色对话记录持久化到本地磁盘。

**数字人视频（需 GPU）**：启用 Avatar 推理后，一张角色参考图驱动实时面部动画和口型同步。支持 FlashHead（1.3B，RTX 4090 可跑 Lite 模式 25 fps）和 LiveAct（18B，RTX PRO 6000 双 GPU 可跑 20 fps）。[GPU 基准表见 README](https://github.com/Lynpoint/CyberVerse#avatar-hardware-benchmarks)。

**角色管理**：创建角色 → 设置参考图、语音（支持豆包语音克隆）、个性化欢迎语、System Prompt、标签 → 导入知识库文档（自动索引，增强 RAG 回答）。

**多 Agent 任务**：对话中可发起后台子任务（搜索、研究、整理、生成 HTML 报告），PersonaAgent 保持前台流畅对话，SubAgent 完成后返回结果。

**可插拔模块**：Brain/Voice/Hearing/Tools/Memory/Face 全部可替换。通过 YAML 配置文件 + Web UI `/settings` 切换不同供应商的 Omni 模型、LLM、TTS、ASR、Embedding、Avatar 后端。

**嵌入集成**：提供 Web 组件/SDK，可将自托管实例嵌入自己的网站。

## 注意事项与风险

- **GPU 门槛**：视频模式需要 NVIDIA GPU（CUDA 12.8+）。FlashHead Lite 最低 RTX 4090 一张可达实时 25 fps，LiveAct 18B 需要 RTX PRO 6000 或更高。纯语音模式无此要求。
- **网络要求**：WebRTC 需要服务器 `8443/TCP` 端口可被客户端访问。若服务器有防火墙/NAT，需配置 SSH 隧道或设置 `pipeline.ice_public_ip`。
- **GPL-3.0 许可**：开源但你若修改并分发，需要开源你的修改。自用不受影响。
- **合规注意**：数字人视频可能涉及肖像权、深度合成合规。项目 Demo 角色仅作演示，不提供商用。
- **尚在早期**：v0.1.0 版本，功能在快速迭代中。多 Agent 网络等高级功能仍在 Roadmap 上。

## 与你现有工具的关系

- 与 [[../05-开发技术栈/OpenLess：开源语音输入，口述需求整理成 AI Prompt]] 和 [[../05-开发技术栈/SpokenType：支持自动润色的 AI 语音输入工具]] 互补：它们是人→AI 的语音输入，CyberVerse 是 AI→人的语音/视频输出。
- 角色形象素材可从 [[Lumimi：免费无版权AI图片生成]] 或 [[StockCake：免费无版权AI图片库]] 获取参考图。
- 若需多语言数字人，可配合 [[../02-内容创作媒体/Violin：开源 AI 视频翻译，33 种语言本地自动化]] 和 [[../02-内容创作媒体/MioSub：开源 AI 字幕工具，视频转录翻译与压制]] 生成多语种字幕。
- 与 [[AiMaMi：OpenAI Codex 桌面管理工具]] 的思路一致：都是把 AI 能力封装成「可管理、可配置」的本地化工具，CyberVerse 偏语音/视频交互，AiMaMi 偏 Codex 工作流管理。

## FAQ

### Q: 一定要有 GPU 才能用吗？
A: 不需要。设置 `inference.avatar.enabled: false` 即为纯语音 Agent 模式，无需 GPU。数字人视频才需要 GPU，且不同画质/模型对 GPU 要求不同（FlashHead Lite 可在 RTX 4090 上实时运行）。

### Q: 和 HeyGen/D-ID 有什么区别？
A: CyberVerse 是开源自托管方案，数据在你自己服务器，不按分钟/视频收费。HeyGen/D-ID 是 SaaS，开箱即用但需要上传数据到对方服务器。CyberVerse 强在可定制性和隐私，弱在开箱体验（需要自己部署和调优）。

### Q: 能给角色喂自己的文档做知识库吗？
A: 可以。导入知识库文档和角色背景资料后，系统自动索引用于 RAG（检索增强生成），角色的回答会更贴合其背景设定。

## 相关链接

- GitHub：https://github.com/Lynpoint/CyberVerse
- 官网：https://www.cyberverse.cc
- Avatar 模型：FlashHead (https://huggingface.co/Soul-AILab/SoulX-FlashHead-1_3B) · LiveAct (https://huggingface.co/Soul-AILab/LiveAct)
