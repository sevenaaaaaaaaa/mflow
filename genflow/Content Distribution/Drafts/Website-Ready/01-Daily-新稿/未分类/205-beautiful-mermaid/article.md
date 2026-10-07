---
title: "beautiful-mermaid：AI 时代的 Mermaid 渲染引擎"
slug: beautiful-mermaid-render-engine
date: 2026-05-25
updated: 2026-05-29
tags: [beautiful-mermaid, Mermaid, SVG, 可视化, npm]
categories: [AI工具]
summary: beautiful-mermaid 将 Mermaid 同步渲染为 SVG 或终端 ASCII，零 DOM 依赖，15 种主题，适合 Agent 生成图表与 React 无闪烁嵌入。npm install beautiful-mermaid 即可使用。
focus_keyword: beautiful-mermaid
source: https://github.com/lukilabs/beautiful-mermaid
author: Craft Team (@lukilabs)
status: draft
---

# beautiful-mermaid：AI 时代的 Mermaid 渲染引擎

> 零 DOM | 同步渲染 | SVG + ASCII 双输出

## 这是什么

[beautiful-mermaid](https://github.com/lukilabs/beautiful-mermaid) 把 Mermaid 语法渲染成精美 **SVG** 或 **ASCII 终端图**，纯 TypeScript，专为 AI Agent 与 React 设计：同步、无闪烁、`useMemo` 友好。

## 适合谁 / 不适合谁

| 人群 | 是否推荐 | 原因 |
|------|----------|------|
| Agent 生成架构图/流程图 | ✅ 推荐 | 返回纯字符串，无 DOM |
| React/Next 文档站 | ✅ 推荐 | CSS 变量主题切换 |
| 需要 mermaid.js 全语法兼容 | ⚠️ 核对 | 支持子集见下文 |
| 仅偶尔一张图 | ⚠️ 可用在线 demo | 不必装 npm |

## 安装与前置条件

```bash
npm install beautiful-mermaid
# 或 bun / pnpm
```

## 核心用法

```typescript
import { renderMermaidSVG, renderMermaidASCII, THEMES, fromShikiTheme } from 'beautiful-mermaid'

const svg = renderMermaidSVG(code, THEMES['tokyo-night'])
const ascii = renderMermaidASCII(code, { useAscii: false })
```

### 主题

- **15 种内置**：Tokyo Night、Catppuccin、Dracula、Nord、GitHub 等  
- **双色 Mono**：仅 `bg` + `fg`，其余 `color-mix()` 衍生  
- **Shiki**：`fromShikiTheme()` 复用 VS Code 主题  
- **CSS 变量**：`bg: 'var(--background)'` 实现零重渲染换肤  

### 支持图表

Flowchart（全方向）、State、Sequence、Class、ER、XY Chart（含 horizontal、交互 tooltip）。

### React 模式

`useMemo` + try/catch + `dangerouslySetInnerHTML`；`code` 变才重渲染。

### Agent 集成要点

1. 输出纯 SVG 字符串  
2. 终端用 `renderMermaidASCII`  
3. 解析失败友好报错  
4. 支持 `linkStyle` 行内覆盖  

## 注意事项与风险

- **语法覆盖**：不等于官方 mermaid.js 100%；复杂图表先验证。  
- **XY Chart 交互**：`interactive: true` 仅部分环境适用。  
- **字体**：默认 Inter，CJK 场景需自行指定 `font`。  
- **上游**：基于 mermaid 生态，重大版本需跟进 breaking changes。

## 与你现有工具的关系

- Agent 写文档时可替代截图 Mermaid；与 [[../01-AI-Agent生态/html-anything：AI 时代的 HTML 编辑器]]、[[DESIGN.md：AI 写前端的新语法——用 Markdown 定义视觉风格]] 同属内容生产链。  
- 在线演示：https://agents.craft.do/mermaid

## FAQ

### Q: 和 mermaid.js 官方 CLI 区别？
A: 同步、主题系统、ASCII 输出、无 DOM，偏嵌入与 Agent。

### Q: 100+ 张图性能？
A: 文档称 100+ 图 < 500ms（环境相关）。

### Q: NPM 包名？
A: `beautiful-mermaid`

## 相关链接

- GitHub：https://github.com/lukilabs/beautiful-mermaid  
- 演示：https://agents.craft.do/mermaid  
- 上游：https://mermaid.js.org/
