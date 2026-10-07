---
title: "LLM Wiki：让 AI 替你维护个人知识库"
slug: llm-wiki-personal-knowledge-base
date: 2026-05-24
updated: 2026-05-29
tags: [LLM Wiki, AI, 知识管理, Obsidian, 效率工具]
categories: [AI工具]
summary: LLM Wiki 基于 Karpathy 理念，把 PDF、网页等材料自动转为带 wikilink 的结构化知识库，兼容 Obsidian。适合文献积累与收藏消化，不适合临时单次问答。
focus_keyword: LLM Wiki
source: https://github.com/nashsu/llm_wiki
author: nashsu
status: draft
---

# LLM Wiki：让 AI 替你维护个人知识库

> GPL v3 | Tauri v2 + React | 兼容 Obsidian vault

## 这是什么

[LLM Wiki](https://github.com/nashsu/llm_wiki) 是跨平台桌面应用，理念来自 Andrej Karpathy 的 [llm-wiki.md](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)。

> 你往里面丢文档 → AI 逐份分析 → 生成结构化 wiki 页面 → 自动 `[[wikilink]]` → 持续生长的知识网络。

不是 RAG 式「搜完即忘」，而是**增量式知识沉淀**。wiki 目录**本身就是 Obsidian vault**（含 `.obsidian/`、frontmatter、双向链接）。

## 适合谁 / 不适合谁

| 场景 | 适配度 | 说明 |
|------|--------|------|
| 长期积累研究文献，需交叉关联 | ★★★★★ | 图谱 + Deep Research |
| 把收藏的文章/PDF 消化成笔记 | ★★★★★ | 多格式摄入 |
| 团队知识库建设 | ★★★★☆ | 需评估协作流程 |
| 日常轻量笔记 | ★★★☆☆ | Obsidian 原生更合适 |
| 临时查一份文档 | ★★☆☆☆ | 传统 RAG 更直接 |

## 安装与前置条件

- **预构建包**：[GitHub Releases](https://github.com/nashsu/llm_wiki/releases)（macOS / Windows / Linux）  
- **源码**：Node.js 20+、Rust 1.70+  
- **可选**：Tavily / SerpApi / SearXNG（Deep Research）、视觉 LLM（图片）

```bash
# 从 Releases 下载安装包即可；源码构建见仓库 README
```

## 核心用法

### 两步思维链摄入

1. **分析**：提取实体、概念、论证，与已有 wiki 冲突检测  
2. **生成**：摘要、实体页、更新 `index.md` / `overview.md` / `log.md`  
- SHA256 增量缓存：文件未变不重复处理  

### 支持格式

PDF、DOCX、PPTX、XLSX、图片、音视频、网页（Chrome 剪藏 + Readability）等。

### 知识图谱

4 信号关联模型（直接链接、来源重叠、Adamic-Adar、类型亲和）+ sigma.js 可视化 + Louvain 社区检测 + Graph Insights（意外关联、知识缺口、一键 Deep Research）。

### 与 Obsidian

> LLM Wiki = AI 写初稿；Obsidian = 你精修延伸。

### 其他能力

- 异步审核队列（冲突/缺口待人工）  
- 多轮对话，4K～1M token 上下文预算  
- 本地 API `127.0.0.1:19828` + [llm_wiki_skill](https://github.com/nashsu/llm_wiki_skill)  
- 中英文界面  

## 注意事项与风险

- **GPL v3**：衍生分发需遵守开源义务。  
- **LLM 成本**：大批量 ingest 消耗 token；缓存可缓解。  
- **隐私**：本地优先，但 Deep Research 会访问外网搜索 API。  
- **质量**：AI 生成内容需人工审核，尤其冲突与实体合并。

## 与你现有工具的关系

- 与 **Obsidian + opencode**（见 [[给 Obsidian 接上免费 AI：opencode + 国产模型配置指南]]）天然衔接：同一 vault 格式。  
- 与 **GBrain**（见 [[GBrain：AI Agent 的个人大脑层]]）对比：LLM Wiki 偏人工阅读流；GBrain 偏 Agent 自动化记忆与 `think` 合成答案。

## FAQ

### Q: 和 Obsidian 插件 RAG 有何不同？
A: LLM Wiki 先「读完写 wiki」再查阅；RAG 多为临时检索，不沉淀图谱。

### Q: 能否给 Claude Code 用？
A: 可通过 llm_wiki_skill 与本地 HTTP API 查询知识库。

### Q: 团队能用吗？
A: 可以，但协作权限与冲突解决需自行约定流程。

## 相关链接

- GitHub：https://github.com/nashsu/llm_wiki  
- Karpathy 理念 gist：https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f  
- agent skill：https://github.com/nashsu/llm_wiki_skill
