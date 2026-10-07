# AI Video Agent — 关键词拓展与 Features 草稿

生成时间：2026-06-03

## 核心词（枢纽）

| 英文关键词 | 建议 slug | 状态 |
| --- | --- | --- |
| ai video agent | `ai-video-agent` | 本批生成 |
| ai video generator agent | `ai-video-agent`（同页覆盖） | — |
| agentic video creation | `autonomous-ai-video-agent` | 本批生成 |

## 长尾 / 场景词（本批）

| 英文关键词 | slug | 故事线 |
| --- | --- | --- |
| ai video agent | `ai-video-agent` | features-grid-bento6 |
| ai video agent marketing | `ai-video-agent-for-marketing` | features-grid-bento6 |
| ai video agent ecommerce | `ai-video-agent-for-ecommerce` | features-grid-bento6 |
| multimodal ai video agent | `multimodal-ai-video-agent` | features-grid-bento6 |
| autonomous ai video agent | `autonomous-ai-video-agent` | features-grid-bento6 |
| ai video agent workflow | `ai-video-agent-workflow` | features-grid-bento6 |
| ai video agent tiktok | `ai-video-agent-for-tiktok` | features-grid-bento6 |
| ai video agent youtube | `ai-video-agent-for-youtube` | features-grid-bento6 |

## 相关已有页（避免重复 import）

reflow 中已有：`ai-video-generator`、`seedance-2-ai-video-generator-agent`、`all-in-one-ai-video-generator`、`ai-video-generator-workflow` 等。本批补 **agent** 语义与渠道/工作流长尾。

## 下一批可拓展（未生成）

- `ai-video-agent-for-instagram-reels`
- `ai-video-agent-for-ads`
- `text-to-video-agent`
- `image-to-video-agent`
- `ai-video-agent-api`（若产品支持）

## 发布前

```bash
cd sanity-studio
node scripts/preflight-content.js --dir "../Pages/drafts/ai-video-agent-expansion/Features/en"
# 确认后
node scripts/import-page.js --import --missing --dir "../Pages/drafts/ai-video-agent-expansion/Features/en"
```
