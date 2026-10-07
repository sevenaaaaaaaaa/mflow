---
title: "html-anything：AI 时代的 HTML 编辑器"
slug: html-anything-agentic-html-editor
date: 2026-05-24
updated: 2026-05-29
tags: [html-anything, HTML, 编辑器, AI, 内容创作]
categories: [AI工具]
summary: html-anything 用本地 Agent 把 Markdown/CSV 等转为可发布 HTML，75 模板×9 输出形式，一键导出微信/推特/知乎。Claude Code 团队已转向 HTML 作为读者终态，而非仅 Markdown。
focus_keyword: html-anything
source: https://github.com/nexu-io/html-anything
author: nexu-io
status: draft
---

# html-anything：AI 时代的 HTML 编辑器

> 本地 Agent | 75 模板 | 9 种输出形式

## 这是什么

[html-anything](https://github.com/nexu-io/html-anything) 是本地 **Agentic HTML 编辑器**：左侧粘贴 Markdown/CSV/Excel/JSON → 选模板与输出形式 → ⌘+Enter 流式生成 HTML 预览 → 一键导出微信/推特/知乎/PNG。

> Markdown 是草稿。HTML 才是人类读的最终形态。

| Markdown | HTML |
|----------|------|
| 对写作者友好 | 对读者友好 |
| 排版受渲染器限制 | 排版完全可控 |
| 发微信需二次排版 | juice 内联 CSS 直贴 |

## 适合谁 / 不适合谁

| 人群 | 是否推荐 | 原因 |
|------|----------|------|
| 公众号/知乎/小红书多平台分发 | ✅ 推荐 | 专用导出管线 |
| 已有 Claude Code/Codex 等 CLI | ✅ 推荐 | 自动检测 agent |
| 坚持纯 Markdown 静态站 | ⚠️ 可选 | 哲学不同 |
| 不愿本地跑 Node/pnpm | ❌ 需 dev 环境 |

## 安装与前置条件

```bash
git clone https://github.com/nexu-io/html-anything
cd html-anything
pnpm install
pnpm -F @html-anything/next dev
# → http://localhost:3000
```

顶部栏自动检测已安装的 Agent CLI（Claude Code / Codex / Gemini / OpenCode / Cursor 等）。

## 核心用法

### 9 种输出形式

| 形式 | 适合 |
|------|------|
| 杂志文章 | 长文、深度报道 |
| Keynote 演示 | 20 种瑞士/电子墨水/小红书风等 |
| 简历 | A4 |
| 海报 | Sunday-paper 风 |
| 小红书卡片 | 社交分享 |
| 推特卡片 | 引用卡 |
| 网页原型 | Landing/Dashboard |
| 数据报告 | CSV/Excel 可视化 |
| Hyperframes 视频 | Remotion 帧脚本 |

### 6 大设计约束（防 AI 胡来）

1. CJK 优先字体栈  
2. 8px 基线网格  
3. 圆角 + 柔阴影、无纯黑纯白  
4. 对比度 ≥ 4.5  
5. 必须用用户真实数据，禁止 Lorem  
6. 流式可中断，省 token  

### 导出机制

- **微信**：`juice` 内联 CSS  
- **X / 微博 / 小红书**：`modern-screenshot` 2× PNG → 剪贴板  
- **知乎**：LaTeX → `data-eeimg`  
- **.html / .png**：自包含单文件  

可与 [[DESIGN.md：AI 写前端的新语法——用 Markdown 定义视觉风格]] 联用：先定视觉宪法，再 html-anything 出稿。

## 注意事项与风险

- **Agent 费用**：生成长 HTML 消耗各 CLI 额度。  
- **平台规则**：微信/知乎排版以各平台最新编辑器为准，导出后需预览。  
- **版权**：模板与生成图需符合商用许可。  
- **与 codex-ppt**：[[codex-ppt-skill：图片式 PPT 生成 Skill]] 出位图 PPT；html-anything 偏 HTML/多平台图文。

## 与你现有工具的关系

- Obsidian 写 Markdown → html-anything 转发布 HTML → `opencode-WP-SEO` 发 WordPress。  
- 演示类也可选 Keynote 模板，与 codex-ppt 二选一。

## FAQ

### Q: 必须联网吗？
A: 本地 dev；生图/Agent 调用取决于所选 CLI。

### Q: 和 Typora 导出 HTML 区别？
A: Agent 按模板与约束生成，非简单 Pandoc 转换。

### Q: 支持哪些输入？
A: Markdown、CSV、Excel、JSON、纯文本等。

## 相关链接

- GitHub：https://github.com/nexu-io/html-anything  
- 本库：[[DESIGN.md：AI 写前端的新语法——用 Markdown 定义视觉风格]]
