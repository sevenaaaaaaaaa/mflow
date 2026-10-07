---
title: "garden-skills：告别 AI 味网页的 Agent Skills 合集"
slug: garden-skills-conardli-agent-skills
date: 2026-05-26
updated: 2026-05-29
tags: [garden-skills, Agent Skills, ConardLi, Cursor, Claude Code, Codex, 网页设计]
categories: [AI工具]
summary: garden-skills 是 ConardLi 开源的 4 件套 Agent Skills：web-design-engineer 用 25 种风格配方告别千篇一律的蓝紫卡片，另有网页演示视频、图像提示词与本地知识库检索；一行 npx 可装，兼容 Claude Code、Cursor、Codex 等六大 Agent 运行时。
focus_keyword: garden-skills
source: https://x.com/IndieDevHailey/status/2059210992077119878?s=20
status: draft
---

# garden-skills：告别 AI 味网页的 Agent Skills 合集

> 7k+ stars | MIT | 4 Skills | `npx skills add` 一行安装 | 附 37s 演示视频

## 这是什么

[garden-skills](https://github.com/ConardLi/garden-skills) 是 **ConardLi** 维护的生产级 [Agent Skills](https://agentskills.io) 合集，面向 Claude Code、Cursor、Codex、OpenCode、Gemini CLI、Claude.ai 等支持 `SKILL.md` 规范的编码 Agent。

[@IndieDevHailey](https://x.com/IndieDevHailey) 于 2026-05-26 推介该仓库，核心主张是：**用结构化 Skill 把 AI 生成网页/前端的「模板味」换成可复现的高级审美**，而非继续堆千篇一律的蓝紫渐变卡片。

仓库当前包含 **4 个 Skill 模块**：

| Skill | 作用（推文 + README 归纳） |
|-------|---------------------------|
| **web-design-engineer** | 设计系统、配色与排版；输出 polished 落地页、仪表盘、原型；内置**反模板清单** + **25 种风格配方**（Linear、Aesop、Pentagram 等参考风格） |
| **web-video-presentation** | 一句话或长文 → 可点击驱动的 **16:9** 网页演示（录屏友好）；**23 个内置主题** + 可插拔 **TTS**（MiniMax / OpenAI 等） |
| **gpt-image-2** | 专业级图像生成/编辑**提示词引擎**；支持本地与多平台调用 |
| **kb-retriever** | **本地知识库**精准检索，控制上下文体积（「不炸上下文」） |

推文称仓库已 **6k+ star**；建档时 GitHub API 显示约 **7k+**（星标随时间变化，以仓库页为准）。

## 适合谁 / 不适合谁

| 人群 | 是否推荐 | 原因 |
|------|----------|------|
| 用 Cursor / Claude Code / Codex 做落地页、仪表盘、原型 | ✅ 推荐 | `web-design-engineer` 直接约束审美与反模板 |
| 需要把文章/脚本变成可录屏的网页演示 | ✅ 推荐 | `web-video-presentation` + 多主题 + TTS |
| 已在多 IDE 混用、Skill 目录分散 | ✅ 推荐 | 可配合 [[skills-manage：20+ 平台 Agent Skills 中央统一管理]] 做中央库分发 |
| 只想用 Markdown 定义视觉规范、不装 Skill | ⚠️ 并行 | 可参考 [[DESIGN.md：AI 写前端的新语法——用 Markdown 定义视觉风格]] |
| 需要企业级设计令牌 / Figma 法务级资产 | ⚠️ 酌情 | Skill 偏 Agent 工作流，非完整 Design Ops |
| 期望一键 PPT 位图幻灯片 | ⚠️ 另选 | 演示视频 Skill ≠ [[codex-ppt-skill：图片式 PPT 生成 Skill]] |
| 不使用任何 Agent Skills 体系的工具 | ❌ 不适用 | 依赖各 Agent 的 Skills 目录约定 |

## 安装与前置条件

- **Node.js**（用于 `npx skills` CLI）
- 目标 Agent 已启用 Skills（路径因平台而异，见仓库「兼容性」表）
- 部分 Skill（如 TTS、图像）可能需要额外 API Key 或本地 CLI——以各 Skill 子目录 README 为准

### 方式 A：`skills` CLI（推文强调的「一条 npx」）

```bash
# 安装全部 4 个 Skill（最新）
npx skills add ConardLi/garden-skills

# 只安装某一个
npx skills add ConardLi/garden-skills -s web-design-engineer

# 安装到全局 ~/.skills
npx skills add ConardLi/garden-skills -s kb-retriever --global
```

### 其他方式（README 亦支持）

- **Claude Code 插件市场**（可钉版本）
- **Releases 钉版本 `.zip`**（CI / 内网）
- **手动拷贝**或 **Git Submodule**（需自行跟进 `main`）

## 核心用法

### web-design-engineer

- 激活后 Agent 按 Skill 内**风格配方**与**反 AI 模板清单**生成页面，目标是从「通用 SaaS 蓝紫卡」切换到 Linear / Aesop / Pentagram 等明确审美方向。
- 适合：营销落地页、内部仪表盘、可点击原型；与 [[html-anything：4.6k 星从 Markdown 到精美 HTML]]、[[DESIGN.md：AI 写前端的新语法——用 Markdown 定义视觉风格]] 可组合——前者偏 HTML 输出管线，后者偏项目根 `DESIGN.md` 规范。

### web-video-presentation

- 工作流：文稿 → 旁白脚本 → 分镜大纲 → 1920×1080 舞台场景 → 点击/键盘推进 `(chapter, step)` → 可选 TTS。
- **23 个内置主题**（如 editorial、terminal、Swiss 等）；适合产品演示、课程、演讲录屏。

### gpt-image-2

- 作为**提示词与调用约定**的 Skill，统一图像生成/编辑任务描述；与 [[codex-ppt-skill：图片式 PPT 生成 Skill]] 中使用的 `gpt-image-2` 场景相近，但 garden-skills 版覆盖更广的前端/设计工作流。

### kb-retriever

- 面向**本地知识库**检索，减少把整库塞进上下文；可与 [[LLM Wiki：让 AI 替你维护个人知识库]]、Obsidian 本地库等搭配（具体索引方式见 Skill 文档）。

## 注意事项与风险

- **星标与版本**：推文「6k+」为推介时点；安装时可用 Releases 或 tag URL **钉版本**，避免 `main` 漂移。
- **审美参考**：风格名（Linear、Aesop、Pentagram 等）为设计方向参考，非官方品牌资产包；商用需自行审查版权与商标。
- **TTS / 图像 API**：`web-video-presentation`、`gpt-image-2` 可能产生第三方费用；内网环境优先 `.zip` 或 Submodule 安装。
- **平台路径**：六大 Agent 的 Skills 目录不同（如 Cursor `.agents/skills/`、Codex `.codex/skills/`）；装错目录会导致 Agent 找不到 Skill。
- **推介帖非作者**：推文来自 @IndieDevHailey，仓库维护方为 **ConardLi**；功能细节以 GitHub README 为准。

## 与你现有工具的关系

- **Skill 资产管理**：装好后可用 [[skills-manage：20+ 平台 Agent Skills 中央统一管理]] 把 `~/.agents/skills/` 等中央库软链接到 Cursor、OpenCode、Claude Code，避免四套副本。
- **Codex 桌面**：UI/快捷键 tweak 见 [[codex-plusplus：给你的 Codex 装上插件系统]]；garden-skills 补的是 **Skill 能力层**。
- **Obsidian + OpenCode**：OpenCode 在兼容性表中已验证；免费模型接入可参考 [[给 Obsidian 接上免费 AI：opencode + 国产模型配置指南]]、[[../03-效率生产力/Claudian × opencode：免费模型接入 Obsidian 的三通道架构]]。
- **Agent 行为**：生成代码时仍可对照 [[Karpathy 编码行为准则：AI Agent 的 4 条铁律]]，避免 Skill 放大后的过度发挥。
- **生态总览**：[[AI Agent 工具生态：从 184 个专业 Agent 到一键 PPT]] 可作为同类 Skill/PPT 工具索引。

## FAQ

### Q: 和 skills-manage 有什么区别？
A: **garden-skills** 提供 4 个具体能力 Skill（设计、演示视频、图像提示、本地检索）；**skills-manage** 是管理多平台 Skill 目录的桌面工具。二者可并用：前者安装内容，后者同步路径。

### Q: 「25 种风格配方」在哪里？
A: 主要在 **web-design-engineer** Skill 的 reference/配方文档中；Agent 按 `SKILL.md` 描述按需加载，而非单一 JSON 配置文件。

### Q: 推文说「六大平台」指什么？
A: 仓库 README 兼容性表列有：Claude Code、Claude.ai、Cursor、Codex CLI、Gemini CLI、OpenCode（均已标注验证）。

### Q: 必须 npx 吗？
A: 否。也可用 Claude 插件市场、Releases `.zip`、手动拷贝或 Submodule；npx 是最快的跨 Agent 方式。

## 相关链接

- 官方仓库：https://github.com/ConardLi/garden-skills
- 中文 README：https://github.com/ConardLi/garden-skills/blob/main/README.zh-CN.md
- 推文原文：https://x.com/IndieDevHailey/status/2059210992077119878?s=20
- 本库相关笔记：[[skills-manage：20+ 平台 Agent Skills 中央统一管理]]、[[DESIGN.md：AI 写前端的新语法——用 Markdown 定义视觉风格]]、[[html-anything：4.6k 星从 Markdown 到精美 HTML]]、[[codex-plusplus：给你的 Codex 装上插件系统]]、[[codex-ppt-skill：图片式 PPT 生成 Skill]]、[[AI Agent 工具生态：从 184 个专业 Agent 到一键 PPT]]
