---
title: "axton-obsidian-visual-skills：Obsidian 可视化技能包"
slug: axton-obsidian-visual-skills
date: 2026-06-16
updated: 2026-06-16
tags: [Obsidian, Claude Code, 可视化, Canvas, Excalidraw, Mermaid]
categories: [AI工具]
summary: "axton-obsidian-visual-skills 是 Axton Liu 开发的 Obsidian 可视化技能包，基于 Claude Code Skills，可将文字内容一键生成 Canvas 思维导图、Excalidraw 手绘图表和 Mermaid 流程图。3k Stars，MIT 协议。"
focus_keyword: "axton-obsidian-visual-skills"
source: https://github.com/axtonliu/axton-obsidian-visual-skills
author: "Axton Liu（axtonliu）"
status: draft
---

# axton-obsidian-visual-skills：Obsidian 可视化技能包

> 文字转 Canvas 思维导图、Excalidraw 手绘图表、Mermaid 流程图 | 3k Stars | MIT | Claude Code Skills

## 这是什么

axton-obsidian-visual-skills 是由 AI 教育者 Axton Liu 开发的 Obsidian 可视化技能包，以 Claude Code Skills 形态运行。它包含三个子技能，可以将文字内容一键转化为 Obsidian 支持的三种视觉格式：

1. **Excalidraw Diagram Generator**：生成手绘风格的图表，支持 8 种图表类型（流程图、思维导图、层级图、关系图、对比图、时间线、矩阵图、自由排列），三种输出模式（Obsidian Markdown 内嵌 / 标准 .excalidraw 文件 / 动画 .excalidraw 文件）
2. **Mermaid Visualizer**：将文本内容转化为专业的 Mermaid 图表，支持流程图、圆形流程图、对比图、思维导图、序列图、状态图，内置语法错误预防机制
3. **Obsidian Canvas Creator**：创建交互式 Obsidian Canvas（.canvas 文件），支持思维导图布局和自由排列布局，含智能节点大小调整、自动边创建、6 种预设配色

项目定位是实验性原型（README 标注 Experimental），质量受模型版本和输入结构影响，适合作为灵感启发和快速原型工具使用。

## 适合谁 / 不适合谁

| 人群 | 是否推荐 | 原因 |
|------|----------|------|
| Obsidian 重度用户 | ✅ 推荐 | 与 Obsidian 生态深度绑定，生成的文件直接在 Obsidian 中打开编辑 |
| 需要快速将文字/文章转为思维导图的知识工作者 | ✅ 推荐 | 读长文后一键生成 Canvas 思维导图，快速梳理知识结构 |
| 已有 Claude Code 环境的用户 | ✅ 推荐 | 即装即用，无需额外配置 |
| 需要做技术文档/演示图表（Mermaid）的开发者 | ✅ 推荐 | 内置语法纠错，避免常见的 Mermaid 渲染错误 |
| 对生成图表有高精度/自定义需求的用户 | ⚠️ 酌情 | 实验性项目，输出质量不稳定，可能需手动调整 |
| 不使用 Obsidian 的用户 | ⚠️ 酌情 | Mermaid 技能通用，但 Excalidraw 和 Canvas 需要 Obsidian 生态 |
| 需要商业级图表输出的团队 | ❌ 不推荐 | 实验性质，不受商业支持，作者声明维护精力有限 |

## 安装与前置条件

- **Claude Code CLI** 已安装
- **Obsidian**（Canvas 和 Excalidraw 技能需要）
- **Excalidraw 插件**（Excalidraw 技能在 Obsidian 中使用需要）

```bash
# 方式一：插件市场安装（推荐）
# 在 Claude Code 中执行：
# /plugin marketplace add axtonliu/axton-obsidian-visual-skills
# /plugin install obsidian-visual-skills

# 方式二：手动安装
git clone https://github.com/axtonliu/axton-obsidian-visual-skills.git
cp -r axton-obsidian-visual-skills/excalidraw-diagram ~/.claude/skills/
cp -r axton-obsidian-visual-skills/mermaid-visualizer ~/.claude/skills/
cp -r axton-obsidian-visual-skills/obsidian-canvas-creator ~/.claude/skills/
```

安装后重启 Claude Code 即可使用。

## 核心用法

### Excalidraw 手绘图表

```text
# 基础流程图
"Create an Excalidraw flowchart showing the CI/CD pipeline"

# 中文支持（注意：手写中文字体需要联网加载 Excalifont）
"用 Excalidraw 画一个商业模式关系图"

# 动画模式
"用 Excalidraw 画一个产品迭代时间线动画"
```

支持的图表类型：Flowchart（流程图）、Mind Map（思维导图）、Hierarchy（层级图）、Relationship（关系图）、Comparison（对比图）、Timeline（时间线）、Matrix（矩阵图）、Freeform（自由排列）。

### Mermaid 图表

```text
# 流程图
"Visualize this process as a Mermaid diagram"

# 序列图
"Create a sequence diagram for the API authentication flow"

# 中文
"把这个工作流程转成 Mermaid 图表"
```

内置语法错误预防：列表冲突检测、子图命名规范、特殊字符转义。

### Canvas 思维导图

```text
# 文章转 Canvas
"Turn this article into an Obsidian Canvas"

# 思维导图
"Create a mind map canvas for project planning"

# 中文
"把这篇文章整理成 Canvas 思维导图"
```

支持 MindMap 布局（从中心辐射）和 Freeform 布局（自定义位置），自动计算节点大小和间距，6 种预设颜色 + 自定义十六进制色。

## 注意事项与风险

- **Excalidraw 中文字体问题**：Excalifont（fontFamily: 5）仅覆盖拉丁字符，中文字体（Xiaolai）需从 Excalidraw.com 动态加载。离线环境或无法访问 Excalidraw.com 时中文可能不显示手写效果。解决方案：下载 CJK 字体文件放入 vault 的 Excalidraw/CJK Fonts 目录
- **实验性项目**：作者明确声明"主要精力在演示工具和系统的协同工作，而非维护此代码库"，输出质量因模型版本和输入结构不同而异
- **Feature 请求可能不被响应**：README 明确声明"因维护精力有限，功能请求可能不被处理"
- **输出需手动调整**：生成图表可能不够精确，建议作为草稿使用后在 Obsidian 中手动编辑

## 与你现有工具的关系

- 与 [[Claude Code Humanizer：用 Claude Code Humanizer 提升文章可读性]]、[[Claude Code 自动化剪辑：基于 Claude Code 的自动化剪辑工作流]] 同属 Claude Code Skills 生态，可在同一工作流中串联使用
- 生成的 Canvas 思维导图可直观呈现本 Tags 目录中各工具的关联关系
- 阅读本目录下的长文章笔记后，用 Canvas/Mermaid 快速生成知识结构图

## FAQ

### Q: 免费吗？
A: 开源免费（MIT）。但使用时需有 Claude Code 环境（需要 Anthropic API 订阅或付费）。

### Q: 支持中文吗？
A: 三个技能都支持中文输入。Excalidraw 的中文手写效果需要联网加载字体（参见注意事项）；Mermaid 和 Canvas 中文支持良好。

### Q: 生成的图表可以直接在 Obsidian 中编辑吗？
A: 可以。Excalidraw 文件用 Excalidraw 插件编辑，Canvas 文件原生支持编辑，Mermaid 代码块可直接修改源码后刷新渲染。

### Q: 与直接在 Claude 中要求生成 Mermaid 有什么区别？
A: 这个 Skill 包内置了优化的提示词、语法错误预防规则、布局算法和配色方案，生成质量通常比直接问 Claude 更稳定。

### Q: 作者还会继续维护吗？
A: 项目标注 Experimental，作者 Axton Liu 的主要业务是 AI Agent 课程教育（MAPS框架），本工具定位为演示项目，建议不要依赖长期维护承诺。

## 相关链接

- GitHub：https://github.com/axtonliu/axton-obsidian-visual-skills
- 作者网站：https://www.axtonliu.ai
- 演示视频：https://youtu.be/TUJ_3G1cylc
- Excalidraw 官方：https://excalidraw.com
- Mermaid 官方：https://mermaid.js.org
- JSON Canvas 规范：https://jsoncanvas.org
