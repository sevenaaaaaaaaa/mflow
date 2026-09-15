# 知乎 + Quora 双语选题规划

> 更新于 2026-06-12。基于 Lovart 2nd（Quora 151 条）+ Lovart 3RD（知乎 127 条）实际数据。

## 数据源

### Quora — Lovart 2nd
- **数据库 ID**：`37ffc0c7-1bd5-80f7-9055-c9c72624f3df`（nowtonext workspace）
- **条目数**：151 条
- **Schema**：Film (title), Tags (multi_select), Description (rich_text), Artist (rich_text), Live (url), Files & media (rich_text)
- **全部有标题和链接**，可直接用于选题

### 知乎 — Lovart 3RD
- **数据库 ID**：`37ffc0c7-1bd5-80ee-a239-de7c4055c90d`
- **条目数**：127 条
- **大部分有标题**（用户手动补完），少量仍是占位符

## Quora 分类（151 条 → 8 品类）

| 品类 | 数量 | 代表问题 |
|------|------|----------|
| **AI 设计工具推荐** | 32 | What is the best free AI image generator? |
| **Agentic AI** | 18 | What is agentic AI? / How do you create an AI agent? |
| **AI 替代设计师？** | 15 | Will AI replace designers? / Is UI/UX going to be replaced? |
| **AI 内容创作/社媒** | 14 | Can AI create social media posts automatically? |
| **AI 视频生成** | 12 | What are the best AI video generators? |
| **AI 图片生成/人像** | 10 | Is there any AI that can create images of people? |
| **AI 赚钱/副业** | 8 | What is the best way to earn using AI? |
| **行业/技术趋势** | 7 | What are the future trends in AI? |

## 知乎分类（127 条 → 7 品类）

| 品类 | 数量 | 代表问题 |
|------|------|----------|
| **AI 工具推荐（网站/软件）** | 50 | 有哪些堪称神器的网站？/ macOS 必装软件 |
| **AI 工具推荐（通用）** | 25 | 最好用的 AI 工具？/ 国内可用的 AI 工具？ |
| **其他热点** | 27 | Nano Banana / GPT-image 2 / Seedance 2.0 / AI 短剧 / PPT |
| **AI 设计相关** | 12 | 全球优秀设计网站？/ 平面设计素材站 |
| **AI 视频生成** | 6 | 文生视频 AI / AI 做视频用什么软件？ |
| **文生图/图生图** | 5 | 文生图哪个最强？/ Nano Banana 2 亮点 |
| **AI Agent/智能体** | 2 | 如何搭建 AI 智能体？/ 国内有哪些好用的 Agent？ |

## 中英文交叉热点矩阵

| 主题 | Quora | 知乎 | Lovart 植入 | 星流植入 | 优先级 |
|------|-------|------|------------|---------|--------|
| AI 设计工具推荐/对比 | 32 | 75 | ✅ vs Canva/MJ/DALL-E | ✅ 中文版 | ⭐⭐⭐ |
| 免费 AI 工具 | 10 | ~5 | ✅ 免费注册 | ✅ 免费注册 | ⭐⭐⭐ |
| AI 替代设计师？ | 15 | ~3 | ✅ 作为「增强」而非「替代」 | ✅ | ⭐⭐⭐ |
| AI 视频生成 | 12 | 6 | ✅ LibTV | — | ⭐⭐⭐ |
| AI 内容创作/社媒 | 14 | ~5 | ✅ 社媒素材 | ✅ | ⭐⭐ |
| Agentic AI | 18 | 2 | ✅ Design Agent 案例 | ✅ 星流 Agent | ⭐⭐ |
| AI 赚钱/副业 | 8 | ~3 | ✅ OPC 场景 | ✅ | ⭐⭐ |
| AI 图片生成/人像 | 10 | ~5 | ✅ 图片生成 | ✅ | ⭐⭐ |
| 中文独有热点 | 0 | 27 | Nano Banana/Seedance/短剧 | ✅ | ⭐ |

## 四条选题路径

| 路径 | 策略 | 知乎版本 | Quora 版本 |
|------|------|----------|-----------|
| A：直接回答问题 | 回答平台上的热门问题 | 知乎问答 | Quora Answer |
| B：工具对比 | 已有英文 SEO 内容改写 | 中文对比文 | 英文对比文 |
| C：职业场景 | 按目标职业写工作流 | 中文职业指南 | 英文职业指南 |
| D：工作流/行业专题 | 跨工具链的完整方案 | 中文全流程 | 英文全流程 |

## 一个选题 → 4 份内容

```
Quora 英文回答 ──翻译改写──→ 知乎中文回答
       │                           │
       └──→ 博客文章（SEO）──→ 社媒内容
```

## 知乎特别注意事项

- 知乎反爬极严：curl/web_extract/browser/API 全部被拦，无法自动抓取标题
- 需要用户手动在 Notion 里补标题
- 新号前 5 篇不放链接，养号优先
- 用户极度反感软文，语气要像「恰好用过」

## Notion API 注意事项

- Lovart 2nd 和 3RD 在同一个 integration 可访问（nowtonext workspace 已授权）
- Token redaction 问题：写 Python 脚本到 /tmp/ 再用 terminal 执行，不要在 execute_code 里直接拼接
- 详见 `references/notion-pitfalls.md`
