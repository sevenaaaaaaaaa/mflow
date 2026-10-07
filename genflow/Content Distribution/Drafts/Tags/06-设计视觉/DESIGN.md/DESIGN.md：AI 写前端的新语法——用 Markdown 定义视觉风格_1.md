---
title: "DESIGN.md：AI 写前端的新语法——用 Markdown 定义视觉风格"
slug: design-md-ai-frontend-visual-spec
date: 2026-05-24
updated: 2026-05-29
tags: [DESIGN.md, 设计系统, AI前端, Google Stitch, VoltAgent]
categories: [AI工具]
summary: DESIGN.md 用 Markdown+YAML 向 AI 描述 UI 审美，无需 Figma 导出。VoltAgent 合集含 73 个品牌范例，复制到项目根目录即可让 Agent 生成风格一致的界面。
focus_keyword: DESIGN.md
source: https://github.com/VoltAgent/awesome-design-md
author: VoltAgent / Google Stitch
status: draft
---

# DESIGN.md：AI 写前端的新语法——用 Markdown 定义视觉风格

> Google Stitch 标准 | 73 品牌范例 | Markdown + YAML

## 这是什么

**DESIGN.md** 是 Google Stitch 提出的纯文本设计系统：一个 Markdown 文件，AI coding agent 读后生成视觉一致的 UI。

| 文件 | 谁读 | 定义什么 |
|------|------|----------|
| `AGENTS.md` | Coding agent | 怎么构建（技术规范） |
| `DESIGN.md` | Design agent | 长什么样（视觉规范） |

- 无 Figma 导出、无 JSON schema、无特殊工具链——**LLM 最擅长读 Markdown**。  
- 合集：[VoltAgent/awesome-design-md](https://github.com/VoltAgent/awesome-design-md)（73 个品牌）。

## 适合谁 / 不适合谁

| 人群 | 是否推荐 | 原因 |
|------|----------|------|
| 用 Cursor/Codex 生成前端的开发者 | ✅ 推荐 | 解决「每次 UI 随机」 |
| 需要快速对齐 Stripe/Claude 等风格 | ✅ 推荐 | 复制即用 |
| 已有完整 Figma Design Tokens 流水线 | ⚠️ 并行 | DESIGN.md 是 Agent 消费层 |
| 需严格品牌法务复刻 logo/资产 | ❌ 不够 | 仅 CSS 可表达部分 |

## 安装与前置条件

两步：

```bash
cp awesome-design-md/design-md/stripe/DESIGN.md ./my-project/DESIGN.md
# 告诉 AI：「用 DESIGN.md 规范做支付成功页」
```

无需 npm 安装；可选 Discord / 请求新品牌：https://getdesign.md/request

## 核心用法

### DESIGN.md 九个部分（标准格式）

1. **Visual Theme & Atmosphere** — 氛围与审美方向（非具体 px）  
2. **Color Palette & Roles** — YAML 语义色（`primary`、`ink`、`canvas`…）  
3. **Typography Rules** — 字号/字重/行高/用途表  
4. **Component Stylings** — 按钮/卡片等含交互态，`{token.ref}` 引用  
5. **Layout Principles** — 间距尺度、网格、折叠  
6. **Depth & Elevation** — 阴影或「表面色彩对比」层级  
7. **Do's and Don'ts** — 防 AI 跑偏的护栏  
8. **Responsive Behavior** — 断点与触控目标  
9. **Agent Prompt Guide** — 可直接粘贴的 prompt 模板  

### 色彩示例（片段）

```yaml
# Claude
colors:
  primary: "#cc785c"
  canvas: "#faf9f5"
  ink: "#141413"

# Stripe
colors:
  primary: "#533afd"
  canvas: "#ffffff"
```

### 73 品牌分类（节选）

- **AI & LLM**：Claude、Mistral、OpenCode AI、xAI…  
- **开发者工具**：Cursor、Vercel、Raycast…  
- **金融**：Stripe、Coinbase、Wise…  
- **设计工具**：Figma、Framer、Webflow…  
- 完整列表见仓库 README  

### 为什么有效

- **AI 时代痛点**：逻辑强、审美随机 → DESIGN.md 作「视觉宪法」  
- **设计师×工程师**：`Figma → 标注 → 手写 CSS` 变为 `DESIGN.md → Agent 生成`  
- **格式选择**：Markdown+YAML 比 DTCG/JSON 更贴 LLM 训练分布  

### 实际效果

> Copy a DESIGN.md into your project, tell your AI agent "build me a page that looks like this" and get pixel-perfect UI that actually matches.

与 `AGENTS.md` 并列 = 技术 + 设计双核。可配合 [[html-anything：AI 时代的 HTML 编辑器]]、[[Karpathy 编码行为准则：AI Agent 的 4 条铁律]]（简洁、外科手术式修改）。

## 注意事项与风险

- **字体许可**：Sohne、Copernicus 等需用开源替代（Inter、Cormorant Garamond 等，文件内通常注明）。  
- **Stripe 渐变**：签名渐变网格常需 SVG/位图，非纯 CSS。  
- **品牌 IP**：仓库 MIT，但品牌视觉归品牌方；DESIGN.md 是「描述」非授权复制。  
- **不要替代**：Figma、Style Dictionary 仍负责完整设计系统；DESIGN.md 是 **Agent 视觉锚点**。

## 与你现有工具的关系

- 写 Obsidian/博客最终 HTML：[[html-anything：AI 时代的 HTML 编辑器]]  
- 图表：[[../05-开发技术栈/beautiful-mermaid：AI 时代的 Mermaid 渲染引擎]]  
- 发布：vault `opencode-WP-SEO` 流水线  

## FAQ

### Q: 和 Tailwind config 区别？
A: DESIGN.md 给 LLM 读「为什么这样设计」；Tailwind 是实现层，可并存。

### Q: 能否混用两个品牌的 DESIGN.md？
A: 不推荐；Do/Don't 会冲突。选主品牌或合并前人工删减。

### Q: 格式规范在哪？
A: https://stitch.withgoogle.com/docs/design-md/format/

## 相关链接

- 合集：https://github.com/VoltAgent/awesome-design-md  
- 格式标准：https://stitch.withgoogle.com/docs/design-md/format/  
- 请求新站：https://getdesign.md/request  
- Discord：https://s.voltagent.dev/discord
