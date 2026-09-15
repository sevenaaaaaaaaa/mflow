---
type: rule
version: 1.0
updated: 2026-07-05
scope: "profile-distribution-active"
tools: [hermes, opencode, claude]
status: active
path: 1-1 Harness/02-rules/RULES-50-distribution.md
generator: 1-1 Harness/11-knowledge/scripts/fm-fix.py
---
# Lovart RULES — 50 分发类（Distribution）

> 适用路线：国内内容分发、国外内容分发
> 加载 Profile：`lovart-distribution`

---

## 四条分发轨道

| 轨道 | 工具 | 平台 | 模型 |
|------|------|------|:---:|
| 国内自动 | Wechatsync（文章同步助手） | 知乎/百家号/掘金/头条/CSDN/豆瓣/思否等 15 平台 | 国内 |
| 海外 API | Node 脚本 | DEV.to / GitHub Issues / Blogger | 海外 |
| 海外扩展 | 爱贝壳 / 文章同步助手 | Medium / X | 海外 |
| 人工 | 手动 | Hacker News / Hacker Noon | 海外 |

## 分发步骤

1. `python3 scripts/score-pages-for-distribution.py --days 28`
2. 读 `queue/pending.json` Top 5
3. 按 `channels/{platform}.md` 写摘要草稿到 `drafts/`
4. `node scripts/preflight-distribution.js --draft PATH --canonical URL --platform NAME --source-title TITLE --source-word-count N`
5. 创建 `queue/dispatch-*.json`，设 `approved: true`
6. `node scripts/dispatch-publish.js --manifest queue/dispatch-XXX.json --dry-run`
7. `node scripts/dispatch-publish.js --manifest queue/dispatch-XXX.json --global-only --approved`

## 周度内容生产节奏

| 类型 | 用途 | 平台变体 |
|------|------|---------|
| T1 精选推荐 | 工具横评/合集推荐 | 知乎/百家号/什么值得买/全链接/英文 |
| T2 单品深测 | 单个工具深度实测 | 知乎/百家号 |
| T3 场景工作流 | 完整创作流程方案 | 知乎/51CTO/Quora英文 |

每周产出 3-7 个母版，每个母版生成 2-6 个平台变体。

## 排期优先级（自动推导）

1. 赛道缺口最大的类别（当前：AI设计、AI营销、角色一致性）
2. 与 Lovart 产品关联度最高的工具
3. 热度高的工具（GitHub Stars 排序）
4. 平替/白嫖类（用户最近关注的）

## 凭证管理

| 变量 | 用途 |
|------|------|
| `DEVTO_API_KEY` | DEV.to 发布 |
| `GITHUB_TOKEN` | GitHub Issues（需 `public_repo` scope） |
| `GOOGLE_CLIENT_ID` + `GOOGLE_CLIENT_SECRET` + `GOOGLE_REFRESH_TOKEN` | Blogger |
| `BLOGGER_BLOG_ID` | Blogger 博客 ID |
| `WECHATSYNC_TOKEN` | 文章同步助手 |

凭证丢失时：先搜 iCloud 归档（`~/iCloud云盘（归档）/`），再 `mdfind`，最后才问用户。

## 发布铁律

- DEV.to API 用 `published: false` 创建草稿，勿直接 `published: true`
- 勿用 sed 直接替换凭证文件（path 内容会被脱敏损坏），用 Node.js 或 Python 脚本
- `write_file` 写 `.env` 时优先用 heredoc（避免 terminal redaction）
- 发布后归档到 `03-Published/`，记录 `wp_post_id` 或 `devto_id`

## 极限铺量模式

触发：用户反复要求"加量"。不要问角度，直接进 5×3×3 话题矩阵模式。
- ≤5 篇：逐篇 humanizer
- 5-50 篇：模板化 + patch 关键篇
- 50+ 篇：Python 批量 + 仅 top 5 hero 全量质量
