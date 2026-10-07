---
title: "Jellyfish：开源 AI 短剧工作流，解决人物漂移"
slug: jellyfish
date: 2026-06-15
updated: 2026-06-15
tags: [AI短剧, 角色一致性, 工作流]
categories: [AI工具]
summary: "Jellyfish：开源 AI 短剧工作流，解决人物漂移。平台：Web/Docker。"
focus_keyword: "Jellyfish"
source: https://github.com/Forget-C/Jellyfish
author: ""
status: draft
---

# Jellyfish：开源 AI 短剧工作流，解决人物漂移

> 3.9k stars | Apache-2.0 | Docker/自托管

## 这是什么

[Jellyfish](https://github.com/Forget-C/Jellyfish) 是一个**端到端的 AI 短剧生产工作坊**。它不是简单的「文本生成视频」工具，而是覆盖从剧本理解 → 分镜拆解 → 角色/场景/道具一致性管理 → 图片视频生成 → 任务追踪的**完整制片管线**。

核心解决 AI 短剧最大的痛点——**人物漂移**：在多镜头短剧中，同一个角色在不同镜头里长相不同、衣服变了、场景对不上。Jellyfish 把角色、场景、道具、服装作为「共享资产」集中管理，每个镜头关联这些资产确保一致性，从工程上把一致性当作一等公民问题来解决。

与单个 AI 图片/视频工具（如 Midjourney、Runway）不同，Jellyfish 是**工作流层**的产品——它调度底层模型来完成生成，但提供剧本分析、资产复用、任务队列、生成状态追踪等制片管理能力。技术栈：React + Vite 前端，FastAPI + MySQL + Redis 后端，Docker Compose 一键部署。

## 适合谁 / 不适合谁

| 人群 | 是否推荐 | 原因 |
|------|----------|------|
| 短剧/微短剧创作者（个人或小团队） | ✅ 推荐 | 完整管线 + 角色一致性格外有用 |
| AI 视频工作室批量生产内容 | ✅ 推荐 | 统一任务中心 + 资产复用，适合规模化 |
| 教育/培训团队制作教学视频 | ✅ 推荐 | 结构化分镜 + 资产库方便迭代 |
| 只想生成单张 AI 图片或单个视频 | ❌ 不推荐 | 这工具太重了，直接用 Midjourney/Runway 更快 |
| 需要实时渲染或 3D 动画 | ❌ 不推荐 | Jellyfish 调度的是扩散模型，不是渲染引擎 |

## 安装

**Docker Compose（推荐）**：

```bash
git clone https://github.com/Forget-C/Jellyfish
cd Jellyfish
cp deploy/compose/.env.example deploy/compose/.env
# 编辑 .env 填入你的 API Key 和数据库配置
docker compose --env-file deploy/compose/.env -f deploy/compose/docker-compose.yml up --build
```

**本地开发**：

```bash
# 后端
cd backend
cp .env.example .env
uv sync
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 前端
cd front
pnpm install
pnpm dev
```

端口：前端 `:7788`，后端 `:8000`（Swagger 文档在 `/docs`），MySQL `:3306`，Redis `:6379`。

## 核心用法

整个工作流走的是：**剧本导入 → 分镜拆解 → 分镜准备 → 确认就绪 → 生成工作区 → 导出**。

**1. AI 剧本理解与分镜拆解**：输入章节剧本，AI 自动拆解为分镜（shot），提取每个分镜中的角色、场景、道具、服装、对话。支持剧本优化、精简和角色一致性检查。

**2. 分镜准备与确认**：系统提取候选资产（角色候选、对话候选等）供你审核——接受、忽略或关联已有资产。用统一的「就绪状态」标记分镜是否准备好进入生成阶段。

**3. 资产一致性与复用**：全局共享角色/场景/道具/服装模型。跨分镜引用同一角色自动保持外观一致。角色有专门的形象图管理，名称查重机制鼓励复用已有资产。

**4. 分镜级生成工作区**：每个就绪分镜进入独立生成工作区——管理关键帧和参考图、预览视频 Prompt、发起图片/视频生成任务、单镜头和批量生成均支持。

**5. 统一异步任务中心**：所有文字处理、图片生成、视频生成任务进入统一队列，可查看状态/进度/耗时、取消任务、从任务跳回对应项目/章节/分镜。

**6. 模型与基础设施管理**：多供应商/多模型管理，按类别设置默认模型，Prompt 模板管理，文件与生成媒体管理，OpenAPI 驱动前后端契约。

## 注意事项与风险

- **需要 API Key**：Jellyfish 是工作流调度器，不内置 AI 模型。你需要自行配置 OpenAI/Claude 等 LLM API 以及图片/视频生成服务（如 Midjourney API、DALL-E 等）。
- **硬件要求**：Docker Compose 部署需要至少 4GB 内存（MySQL + Redis + 前后端）。生成任务的计算由远程 API 完成，本地不跑模型推理。
- **中文优先**：项目文档和界面目前以中文为主，英文 README 有但功能细节以中文为准。
- **版本迭代快**：截至 2026 年 4 月最新版 v0.3.2，功能仍在快速迭代中，升级时注意检查 `.env` 和配置兼容性。

## 与你现有工具的关系

- 与 [[Toonflow：开源 AI 短剧生成工具]] 和 [[deep-printfilm：剧本角色关键帧串联的 AI 漫剧工场]] 同属 AI 视频/短剧赛道——Jellyfish 侧重**制片级工作流管理**，ToonFlow 偏一键生成，deep-printfilm 偏关键帧串联。
- 角色参考图可从 [[../01-AI-Agent生态/Lumimi：免费无版权AI图片生成]] 或 [[../01-AI-Agent生态/StockCake：免费无版权AI图片库]] 获取素材。
- 视频字幕可对接 [[MioSub：开源 AI 字幕工具，视频转录翻译与压制]] 或 [[Violin：开源 AI 视频翻译，33 种语言本地自动化]]。
- 如果只是做单张图，Jellyfish 太重了；但如果做系列短剧，它能省掉你在 Figma/Notion 里手动追踪角色和分镜的时间。

## FAQ

### Q: 和直接用 ComfyUI 做视频有什么区别？
A: ComfyUI 是节点式图像/视频生成工具，强在单次生成的可控性。Jellyfish 是制片管理系统——它帮你管理剧本、分镜、角色资产和生成任务，底层仍然调用生成模型。两者的关系类似于「Airtable + API 调度」vs「Photoshop」。

### Q: 角色一致性真的能解决吗？
A: Jellyfish 从工程层面解决：统一角色形象库 + 分镜引用同一角色 ID + 约束 Prompt 模板。但最终效果取决于底层模型的 IP 一致性能力（如 Midjourney 的 cref 参数）。Jellyfish 保证的是「Process 一致性」而非「Pixel 一致性」——前者是管理的必要条件，后者是目前所有 AI 工具的短板。

### Q: 免费还是付费？
A: Jellyfish 本身开源免费（Apache-2.0）。但你需要为调用的 AI API（LLM、图片生成、视频生成）付费。成本取决于你的生成量和选用的 API 供应商。

## 相关链接

- GitHub：https://github.com/Forget-C/Jellyfish
- 在线文档：https://forget-c.github.io/Jellyfish
- 来源：https://www.ahhhhfs.com/79774/
