---
title: "codex-ppt-skill：图片式 PPT 生成 Skill"
slug: codex-ppt-skill-image-ppt
date: 2026-05-25
updated: 2026-05-29
tags: [codex-ppt, PPT, Codex, skill, gpt-image]
categories: [AI工具]
summary: codex-ppt-skill 用 gpt-image-2 生成 16:9 整页幻灯片图片并组装为 PPTX，支持 9 种视觉风格与论文原图插入。适合演示稿，不适合需要逐元素编辑的母版。
focus_keyword: codex-ppt-skill
source: https://github.com/ningzimu/codex-ppt-skill
author: "@ningzimu"
status: draft
---

# codex-ppt-skill：图片式 PPT 生成 Skill

> 339 stars | MIT | Codex / Claude Code / OpenClaw / Hermes

## 这是什么

[codex-ppt-skill](https://github.com/ningzimu/codex-ppt-skill) 实现**整页图片式 PPT**：每页一张 `gpt-image-2` 生成的 16:9 图，Python 脚本组装 `.pptx`。牺牲可编辑性，换视觉上限。

> 「请使用 codex-ppt skill 把这篇文章做成 10 页左右的 PPT」

枢纽：[[AI Agent 工具生态：从 184 个专业 Agent 到一键 PPT]]。

## 适合谁 / 不适合谁

| 人群 | 是否推荐 | 原因 |
|------|----------|------|
| 分享会、路演快速出稿 | ✅ 推荐 | 样张确认后批量生成 |
| 论文答辩（需插图） | ✅ 推荐 | 支持原图/截图插入 |
| 需后期改字体布局的 PPT | ❌ 不推荐 | 页为位图 |
| 无 Codex 且不愿配生图 API | ⚠️ 可用 fallback | Claude/Hermes 走 API |

## 安装与前置条件

| Agent | 安装 |
|-------|------|
| Codex | `npx skills add ... --agent codex`（优先内置 gpt-image-2） |
| Claude Code | `--agent claude-code` |
| OpenClaw | `openclaw skills install codex-ppt` |
| Hermes | `--agent hermes-agent` |

## 核心用法

### 10 步工作流

```
读内容 → 出大纲 → 确认页数 → 推荐 2-3 风格 → 确认生图方式
→ 1 页样张 → 确认 → 逐页生成 → 质量检查 → speech.md → assemble_ppt.py
```

每步向用户确认，非一把梭。

### 9 种视觉风格

清爽专业 / 创意杂志 / 电子墨水 / 数据仪表盘 / 复古插画 / 手绘技术 / 手绘白板 / 温暖手工 / 科研答辩

### 输出结构

```
{PPT名称}/
├── origin_image/slide_01.png ...
├── outline.md
├── speech.md
└── {PPT名称}.pptx
```

### 亮点

- 论文原图/截图指定页插入  
- 满意风格可存入 `references/`  
- 单页修改不重做全部  
- 默认 2K，文字多可 4K  
- speech.md 写入备注  

## 注意事项与风险

- **可编辑性**：无法在 PowerPoint 里改单个文本框，只能重生成该页。  
- **API 与版权**：生图内容需合规；非 Codex 环境需自备 API。  
- **token/费用**：多页 2K/4K 生图成本显著。  
- **品牌一致性**：多份 PPT 需统一 `references/` 风格库。

## 与你现有工具的关系

- 在 Obsidian opencode 中：`请使用 codex-ppt skill...` — 见 [[给 Obsidian 接上免费 AI：opencode + 国产模型配置指南]]。  
- 与 [[html-anything：AI 时代的 HTML 编辑器]] 的 Keynote 模板路线不同：前者位图 PPT，后者 HTML 演示。

## FAQ

### Q: 和 PowerPoint Copilot 有何不同？
A: 全页 AI 生图美学，非基于母版的元素编辑。

### Q: 能否只用中文？
A: 可以，大纲与 speech 支持中文；生图 prompt 建议明确语言要求。

### Q: 单页失败怎么办？
A: 支持单页重生成，无需重做全套。

## 相关链接

- GitHub：https://github.com/ningzimu/codex-ppt-skill  
- 本库：[[AI Agent 工具生态：从 184 个专业 Agent 到一键 PPT]]
