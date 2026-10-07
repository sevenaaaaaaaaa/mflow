---
title: "3DCellForge：AI 驱动的 3D 模型工作室"
slug: 3dcellforge-ai-3d-studio
date: 2026-05-24
updated: 2026-05-29
tags: [3DCellForge, AI, 3D, WebGL, Three.js]
categories: [AI工具]
summary: 3DCellForge 是开源 Web 3D 工作室：上传参考图由 AI 生成 GLB，支持 Hyper3D、Tripo、Fal 等多后端与演示模式。需配置各云 API Key，本地 Hunyuan3D 可作兜底。
focus_keyword: 3DCellForge
source: https://github.com/huangserva/3DCellForge
author: huangserva
status: draft
---

# 3DCellForge：AI 驱动的 3D 模型工作室

> React + Three.js | 多 AI 后端 | WebGL 交互检视

## 这是什么

[3DCellForge](https://github.com/huangserva/3DCellForge) 是 **AI 驱动的交互式 3D 生成、检视与演示工作室**：

上传参考图 → AI 生成 3D GLB → WebGL 交互 → 演示模式导出。

## 适合谁 / 不适合谁

| 人群 | 是否推荐 | 原因 |
|------|----------|------|
| 产品/设计快速 3D 原型 | ✅ 推荐 | 多后端 AUTO 降级 |
| 开发者自建 3D 流水线 | ✅ 推荐 | 开源可改 |
| 需工业级 CAD 精度 | ❌ 不推荐 | AI 生成质量有限 |
| 不愿配置 API Key | ⚠️ 仅本地 GLB/JS Depth | 图生 3D 需 Key |

## 安装与前置条件

```bash
git clone https://github.com/huangserva/3DCellForge
cd 3DCellForge
npm install
npm run dev
```

图生 3D 需 `.env.local`：

```
TRIPO_API_KEY=...
FAL_API_KEY=...
RODIN_API_KEY=...
OPENAI_API_KEY=...   # 可选：图片理解
HUNYUAN_API_BASE=http://127.0.0.1:8081
```

```bash
npm run dev:api   # 后端 127.0.0.1:8787
npm run dev       # 前端
```

## 核心用法

### 三栏工作台

```
┌──────────┬──────────────────┬──────────┐
│ 模型库    │   WebGL 3D 舞台   │ 工具面板  │
└──────────┴──────────────────┴──────────┘
```

### 生成后端

| 后端 | 方式 |
|------|------|
| Hyper3D Rodin / Tripo / Fal.ai | 云端 |
| Hunyuan3D | 本地 API |
| JS Depth | 浏览器浮雕 |
| 本地 GLB | 导入 |

**AUTO 链路**：Hyper3D → Tripo → Fal → Hunyuan3D → JS Depth（兜底）

### 演示模式

按模型类型选镜头：汽车道路、飞机掠过、舰船巡航、生物环绕等。

### 质量评分

自动评估 GLB 大小、面数、纹理、演示就绪度。

### 持久化

- 服务端 `.generated-models/` 缓存  
- 前端 IndexedDB + localStorage 降级  

```bash
npm run test
npm run test:visual
```

## 注意事项与风险

- **API 费用**：Rodin/Tripo/Fal 等按量计费。  
- **生成质量**：复杂拓扑可能失败，AUTO 会降级到 JS Depth。  
- **Key 安全**：勿提交 `.env.local` 到 git。  
- **测试**：`test:visual:update` 仅 UI 有意变更时使用。

## 与你现有工具的关系

- 与 [[html-anything：AI 时代的 HTML 编辑器]]、[[DESIGN.md：AI 写前端的新语法——用 Markdown 定义视觉风格]] 同属「AI + 视觉产出」工具链，面向 3D 而非 2D 页面。  
- 可在 opencode 工作流中调用 API 脚本批量生成资产。

## FAQ

### Q: 没有 API Key 能用什么？
A: 导入本地 GLB、JS Depth 浮雕；完整图生 3D 需至少一个云 Key 或本地 Hunyuan。

### Q: AUTO 模式如何选后端？
A: 按优先级尝试，失败自动下一项直至 JS Depth。

### Q: 模型存在哪？
A: 服务端 `.generated-models/` + 浏览器 IndexedDB。

## 相关链接

- GitHub：https://github.com/huangserva/3DCellForge
