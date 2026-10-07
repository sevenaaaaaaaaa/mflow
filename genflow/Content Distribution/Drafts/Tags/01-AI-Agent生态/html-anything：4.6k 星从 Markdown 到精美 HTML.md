---
title: "html-anything：4.6k 星从 Markdown 到精美 HTML"
slug: html-anything-wechat-markdown-to-html
date: 2026-06-01
updated: 2026-05-29
tags: [html-anything, Markdown, HTML, 内容创作, 微信公众号, AI工具]
categories: [AI工具]
summary: 公众号「大朝」介绍开源 html-anything：本地写好 Markdown 草稿，选模板一键生成精美 HTML，约 4.6k GitHub stars、75 套模板；30 秒 pnpm 跑通，长文推荐 doc-kami-parchment，小红书卡图可用 card-xiaohongshu。
focus_keyword: html-anything
source: https://mp.weixin.qq.com/s?__biz=MzI1NTc0MDg0Ng==&mid=2247485048&idx=1&sn=6cff1d13d1d8b1553121f6616ef347a2&chksm=eb65e0f77548f4727beecb2de2b1f7f439ebba3548c18215ab0a5fa35304ecdd11b0088cf0e8&mpshare=1&scene=24&srcid=0601jf34VXLJE5IwmMcNedal&sharer_shareinfo=d1deb7c47b8a632a77f3ced270586195&sharer_shareinfo_first=d1deb7c47b8a632a77f3ced270586195#rd
author: 大朝
status: draft
---

# html-anything：4.6k 星从 Markdown 到精美 HTML

> 约 4.6k GitHub stars | 本地 Agent 编辑器 | 75 模板 | 三栏：编辑 / 选模板 / 预览

## 这是什么

[html-anything](https://github.com/nexu-io/html-anything) 是运行在本地的 **Agentic HTML 编辑器**：你在左侧写好 Markdown 草稿，选中模板后点生成，由工具按模板排成可直接发布的精美 HTML，而不是简单把 Markdown 渲染成默认样式。

文章引用的背景是 Anthropic Claude Code 团队成员 Thariq 的观察：不少内部文档正从 Markdown 转向 HTML，因为「人真的会打开看」。html-anything 解决的是**怎么生成**这类 HTML——把「Markdown 当草稿、HTML 当读者终态」落到一键工作流里。

与仅做 Pandoc/Typora 导出的区别在于：项目内置大量设计约束与模板（文中称约 **75 个**），每个 skill 还提供 `example.html`，可先双击样例确认效果再生成。

## 适合谁 / 不适合谁

| 人群 | 是否推荐 | 原因 |
|------|----------|------|
| 公众号 / 知乎 / 多平台长文作者 | ✅ 推荐 | 本地草稿 → 模板 HTML，减少二次排版 |
| 希望「写完就能贴进微信编辑器」的创作者 | ✅ 推荐 | 面向发布态 HTML，而非仅预览 Markdown |
| 需要小红书卡图等社交模板 | ✅ 推荐 | 文中点名 `card-xiaohongshu`（本篇未展开细节） |
| 已用 Node/pnpm，能接受本地 dev | ✅ 推荐 | 官方路径为 clone + `pnpm` 启动 Next 应用 |
| 坚持纯 Markdown 静态站、不要 HTML 终态 | ⚠️ 可选 | 理念不同，但可只当排版实验 |
| 不愿本地装依赖、只要在线 SaaS | ❌ 不推荐 | 需本地跑 `@html-anything/next` |
| 需要九种输出形式、导出管线等完整说明 | ⚠️ 见姊妹笔记 | 见 [[html-anything：AI 时代的 HTML 编辑器]]（基于仓库 README 整理） |

## 安装与前置条件

- **环境**：Git、Node.js、pnpm  
- **仓库**：https://github.com/nexu-io/html-anything  
- **可选**：已安装的 Agent CLI（Claude Code / Codex / OpenCode / Cursor 等）——姊妹笔记中说明顶部栏可自动检测；本篇公众号文侧重「点一点生成」，未展开 Agent 配置细节。

### 30 秒跑起来（原文步骤）

```bash
git clone https://github.com/nexu-io/html-anything
cd html-anything
pnpm install
pnpm -F @html-anything/next dev
```

浏览器打开 http://localhost:3000 。界面为三栏：**左编辑、中选模板、右预览**。不确定效果时，可先双击各 skill 自带的 `example.html` 查看样例。

## 核心用法

### 工作流

1. 在左侧粘贴或编写 **Markdown 草稿**  
2. 中间栏选择模板（库内约 75 个；搜 `doc` 或 `article` 可筛长文类）  
3. 触发 **生成**，右侧流式预览 HTML  
4. 满意后按项目导出能力发布（微信内联 CSS、截图卡图等详见 [[html-anything：AI 时代的 HTML 编辑器]]）

### 原文推荐的模板

| 场景 | 模板 ID | 说明 |
|------|---------|------|
| 长文 / editorial | `doc-kami-parchment` | 暖羊皮纸风格，作者自用写长文 |
| 小红书卡图 | `card-xiaohongshu` | 社交卡片；文中邀请读者自行尝试 |

### 关键观点（来自原文）

- **Markdown 是写作者的格式，HTML 是读者会打开的终态**——与 Claude Code 团队内部文档迁移趋势一致。  
- **模板 + 样例先行**：先看 `example.html` 再生成，降低试错成本。  
- **本地优先**：数据与生成在本地 dev 环境完成，适合不愿把草稿交给在线排版 SaaS 的用户。

## 注意事项与风险

- **抓取说明**：自动化请求若省略 URL 中的 `chksm` 等参数，微信可能返回「参数错误」；整理本篇时已用完整分享链接抓取。  
- **Star 数与版本**：文中「约 4.6k 星」会随时间变化，以 GitHub 页面为准。  
- **Agent / token 费用**：若走 Agent 生成长 HTML，消耗取决于你所接 CLI 的计费策略（姊妹笔记有补充）。  
- **平台合规**：导出到微信、知乎、小红书前请在各平台编辑器内预览，遵守排版与版权规则。  
- **与既有笔记分工**：本库 [[html-anything：AI 时代的 HTML 编辑器]] 已覆盖九种输出形式、juice 导出、DESIGN.md 联用等；本篇仅固化公众号原文视角，避免重复编造未在原文出现的功能。

## 与你现有工具的关系

- **姊妹笔记**：[[html-anything：AI 时代的 HTML 编辑器]] — 同一仓库的 GitHub/README 向深度整理（75 模板 × 9 输出、导出机制、6 大设计约束）。  
- **视觉规范**：可与 [[DESIGN.md：AI 写前端的新语法——用 Markdown 定义视觉风格]] 联用——先定 Markdown 视觉宪法，再进 html-anything 出稿。  
- **Obsidian 写作流**：在 Obsidian 写 Markdown 草稿 → html-anything 出 HTML → 若发 WordPress 可参考 [[给 Obsidian 接上免费 AI：opencode + 国产模型配置指南]] 与 SEO 相关流程。  
- **演示 / PPT**：位图 PPT 可选 [[codex-ppt-skill：图片式 PPT 生成 Skill]]；html-anything 的 Keynote 类模板在姊妹笔记中列出。  
- **同类公众号工具文**：[[skills-manage：20+ 平台 Agent Skills 中央统一管理]] 解决多 IDE Skill 同步；html-anything 解决「稿 → 发布 HTML」排版，二者可并存。

## FAQ

### Q: 这篇公众号文和库里的 html-anything 笔记有什么区别？
A: 本篇 `source` 为微信原文（作者「大朝」），侧重 4.6k 星叙事、30 秒安装与 `doc-kami-parchment` / `card-xiaohongshu` 推荐；[[html-anything：AI 时代的 HTML 编辑器]] 基于 GitHub，覆盖导出管线与九种输出形式。

### Q: 必须用 Agent CLI 才能用吗？
A: 公众号文强调「点生成」与模板预览；仓库亦支持多种 Agent CLI 自动检测，详见姊妹笔记。仅想试模板时，可先按上文 `pnpm dev` 跑通界面。

### Q: 为什么 curl 抓微信有时失败？
A: 需使用带 `__biz`、`mid`、`sn`、`chksm` 等参数的**完整分享链接**，并建议加浏览器 User-Agent；省略 `chksm` 时常见「参数错误」空页。

## 相关链接

- 微信原文：https://mp.weixin.qq.com/s?__biz=MzI1NTc0MDg0Ng==&mid=2247485048&idx=1&sn=6cff1d13d1d8b1553121f6616ef347a2  
- GitHub：https://github.com/nexu-io/html-anything  
- 本库深度笔记：[[html-anything：AI 时代的 HTML 编辑器]]  
- 关联：[[DESIGN.md：AI 写前端的新语法——用 Markdown 定义视觉风格]]、[[skills-manage：20+ 平台 Agent Skills 中央统一管理]]
