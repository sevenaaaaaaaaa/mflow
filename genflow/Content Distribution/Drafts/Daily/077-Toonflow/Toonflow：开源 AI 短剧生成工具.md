---
title: "Toonflow：开源 AI 短剧生成工具"
slug: toonflow
date: 2026-06-15
updated: 2026-06-16
tags: [AI短剧, 开源, 全链路]
categories: [AI工具]
summary: "Toonflow 是开源一站式 AI 短剧创作工具，将小说、剧本快速转化为动画短剧。集成 AI 编剧、智能分镜、角色与视频生成，跨平台桌面端轻量部署，10.1k Stars，Apache-2.0 协议。"
focus_keyword: "Toonflow"
source: https://github.com/HBAI-Ltd/Toonflow-app
author: "HBAI-Ltd（北京爱阿科技有限公司）"
status: draft
---

# Toonflow：开源 AI 短剧生成工具

> 一站式 AI 短剧工作台，从文本到角色、分镜到出片 | 10.1k Stars | Apache-2.0 | TypeScript + Electron + Docker

## 这是什么

Toonflow 是一个开源的一站式 AI 短剧创作工作台，由北京爱阿科技有限公司（HBAI-Ltd）开发维护。它的核心能力是将小说、剧本等文本内容快速转化为动画短剧，覆盖"策划 → 编剧 → 分镜 → 出片"的完整闭环。

从技术架构看，Toonflow 采用三层 Agent 协作体系（决策层、执行层、监督层），支持基于本地 ONNX 的持久化 Agent 记忆、可编程的模型供应商系统（在设置中心直接编写 TypeScript 逻辑即可接入新模型），以及基于章节事件图谱的结构化改编流程。整套系统以 Electron 桌面客户端形态交付，同时支持 Docker 和云服务器部署，内置前端页面，不需要额外的 Web 服务。

与同类工具（如对外发布的 AI 视频生成 API）的差异在于：Toonflow 将剧本分析、角色管理、分镜编排、素材生成、视频拼接整合在同一个本地工作台内，配合类无限画布的节点化操作界面，让创作者可以自由编排、回溯和并行生产，不受线性步骤限制。制作一个约 2 分钟的 Demo 短剧（使用 Claude Opus 4.6 + Seedance 2.0 + GPT Image 2），总成本约 ¥130。

## 适合谁 / 不适合谁

| 人群 | 是否推荐 | 原因 |
|------|----------|------|
| 短视频创作者 / 自媒体 | ✅ 推荐 | 小说转短剧、快速原型出片，2 小时完成一条 Demo 的成本远低于人工制作 |
| 独立开发者 / AI 爱好者 | ✅ 推荐 | 开源可自托管，支持 Docker 和云部署，可编程供应商系统方便接入私有模型 |
| 小型内容团队 | ✅ 推荐 | 三层 Agent 协作 + 审核流程，适合多人协作生产短剧内容 |
| 专业影视制作团队 | ⚠️ 酌情 | 输出质量取决于底层视频模型，目前适合快速原型而非商业级成片；但可作前期剧本/分镜辅助 |
| 无 GPU 的个人用户 | ⚠️ 酌情 | 视频和图片生成依赖外部模型 API，需承担 API 调用费用 |
| 仅需单一功能（如翻译字幕） | ❌ 不推荐 | Toonflow 是全链路工具，单一需求用它的学习成本过高 |

## 安装与前置条件

- **Node.js**：23.11.1+
- **AI 服务接口**：大语言模型 API（OpenAI 兼容或 Anthropic 等）、视频生成服务（豆包/Sora 兼容）、图片生成服务（Nano Banana Pro 兼容）
- **可选 Docker**：20.10+

```bash
# 克隆仓库
git clone https://github.com/HBAI-Ltd/Toonflow-app.git
cd Toonflow-app

# 安装依赖并启动开发环境（Electron GUI）
yarn install
yarn dev:gui

# 或 Docker 部署
yarn docker:local
# 访问 http://localhost:10588/index.html
# 默认账号 admin / admin123
```

## 核心用法

### 快速上手流程

1. 启动应用并登录（默认 `admin` / `admin123`）
2. 在设置中心配置模型供应商（文本/图像/视频模型）
3. 新建项目并导入原著，执行章节事件提取
4. 进入 ScriptAgent 生成故事骨架、改编策略与结构化剧本
5. 切换到 ProductionAgent，在无限画布中组织分镜、素材与视频节点
6. 对分镜图进行节点化精调后回流工作台，完成视频拼接与导出

### 关键特性

| 特性 | 说明 |
|------|------|
| 无限画布工作台 | 以节点形式组织剧本、角色、分镜、素材，支持自由编排和回溯 |
| 三层 Agent 协作 | 决策层、执行层、监督层协同，覆盖任务拆解、内容生成、质量审阅 |
| 持久化 Agent 记忆 | 基于本地 ONNX 向量检索，支持短期消息、长期摘要和语义召回 |
| 可编程供应商系统 | 在设置中心编写 TypeScript 逻辑即时生效，无需改源码或重启 |
| Skill 文件化配置 | ScriptAgent 与 ProductionAgent 的核心提示词外化为 Markdown 文件，在线编辑即可调优 |
| 多语言界面 | 支持简体中文、繁体中文、English、ไทย、Tiếng Việt、日本語、Русский |

## 注意事项与风险

- **模型费用**：视频生成是主要成本来源，Demo 中视频模型约 ¥120/条，批量生产需预算规划
- **商业授权**：Apache-2.0 基础协议，但分发产品给 2 个及以上独立第三方需取得商业授权（年销售额 < ¥10 万可免费申请）
- **macOS 安全提示**：安装后需到「设置 → 隐私与安全性」允许运行，否则因证书问题无法打开
- **Node.js 版本要求严格**：必须 23.11.1+，低于此版本可能无法构建
- **首次登录后务必修改默认密码**（admin/admin123）

## 与你现有工具的关系

- 与 [[../01-AI-Agent生态/CyberVerse：开源数字人 Agent 平台，照片生成实时视频通话]]、[[Jellyfish：开源 AI 短剧工作流，解决人物漂移]] 同属 AI 短剧赛道，Toonflow 侧重「文本→成片」全链路，CyberVerse 侧重数字人实时交互，Jellyfish 侧重人物一致性
- 成品短剧素材可导入 [[FreeCut：开源浏览器视频编辑器，免安装本地剪辑]] 做后期精剪，或 [[../01-AI-Agent生态/Claude Code 自动化剪辑：基于 Claude Code 的自动化剪辑工作流]] 做字幕处理

## FAQ

### Q: Toonflow 免费吗？
A: 软件本身开源免费（Apache-2.0），但使用时需要自行承担 AI 模型 API 的调用费用。商业分发（给 2 个及以上第三方提供产品）需取得商业授权。

### Q: 需要什么样的硬件？
A: 推荐有 GPU 的机器运行本地推理（ONNX），但视频/图片生成依赖远程模型 API，实际不需要本地 GPU。2GB+ 内存、Node.js 23.11.1+ 即可运行。

### Q: 支持哪些视频模型？
A: Demo 使用 Seedance 2.0，但系统通过可编程供应商机制支持任意兼容接口的视频模型，包括豆包视频服务、Sora 兼容接口等。

### Q: 一次能生成多长的短剧？
A: Demo 成片约 2 分钟（原始素材 3 分钟），实际长度取决于模型上下文窗口和项目设置，理论上可分段拼接更长内容。

## 相关链接

- 来源：https://www.ahhhhfs.com/79380/
- GitHub：https://github.com/HBAI-Ltd/Toonflow-app
- 官网：https://toonflow.net
- Gitee（国内）：https://gitee.com/HBAI-Ltd/Toonflow-app
- 前端仓库：https://github.com/HBAI-Ltd/Toonflow-web
- 视频教程：https://www.bilibili.com/video/BV1oXD7BqEqJ
- Discord：https://discord.gg/HEjKmpNpAZ
