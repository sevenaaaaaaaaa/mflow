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

## 一、硬条款（违反即停）

1. **必须**所有分发稿先过 `preflight-distribution.js`（--draft/--canonical/--platform/--source-title/--source-word-count）
2. **禁止**未 `approved: true` 就发布；dispatch 单**必须**显式设 approved
3. **必须**发布先 `--dry-run`，确认后才实发
4. **必须** DEV.to 用 `published: false` 建草稿（**禁止**直接 `published: true`）
5. **禁止**用 sed 替换凭证文件（会被脱敏损坏）——**必须**用 Node.js/Python 脚本
6. **必须**写 `.env` 用 heredoc（避免终端脱敏）
7. **必须**发布后归档到 `03-Published/` 并记录 `wp_post_id` / `devto_id`
8. **必须**每次分发绑定 canonical 与原文字数（preflight 校验项）
9. 凭证缺失时**必须**按序查找：iCloud 归档 → `mdfind` → 问用户（**禁止**跳过前两步直接问）
10. 每篇分发稿**必须**符合 RULES-70 数量预算（摘要类 ≤600 字，**禁止**整篇搬运）

## 二、参数表

### 四条分发轨道

| 轨道 | 工具 | 平台 | 模型 |
|------|------|------|:---:|
| 国内自动 | Wechatsync（文章同步助手） | 知乎/百家号/掘金/头条/CSDN/豆瓣/思否等 15 平台 | 国内 |
| 海外 API | Node 脚本 | DEV.to / GitHub Issues / Blogger | 海外 |
| 海外扩展 | 爱贝壳 / 文章同步助手 | Medium / X | 海外 |
| 人工 | 手动 | Hacker News / Hacker Noon | 海外 |

### 标准步骤

1. `python3 scripts/score-pages-for-distribution.py --days 28`
2. 读 `queue/pending.json` Top 5
3. 按 `channels/{platform}.md` 写摘要草稿到 `drafts/`
4. `node scripts/preflight-distribution.js --draft PATH --canonical URL --platform NAME --source-title TITLE --source-word-count N`
5. 创建 `queue/dispatch-*.json`（`approved: true`）
6. `node scripts/dispatch-publish.js --manifest queue/dispatch-XXX.json --dry-run`
7. `node scripts/dispatch-publish.js --manifest queue/dispatch-XXX.json --global-only --approved`

### 周度节奏与优先级

| 类型 | 用途 | 平台变体 |
|------|------|---------|
| T1 精选推荐 | 工具横评/合集推荐 | 知乎/百家号/什么值得买/全链接/英文 |
| T2 单品深测 | 单个工具深度实测 | 知乎/百家号 |
| T3 场景工作流 | 完整创作流程方案 | 知乎/51CTO/Quora英文 |

每周 3-7 个母版 × 2-6 个平台变体。优先级：①赛道缺口最大（AI设计/AI营销/角色一致性）②与产品关联度 ③热度（GitHub Stars）④平替/白嫖类

### 凭证

| 变量 | 用途 |
|------|------|
| `DEVTO_API_KEY` | DEV.to 发布 |
| `GITHUB_TOKEN` | GitHub Issues（`public_repo`） |
| `GOOGLE_CLIENT_ID` + `GOOGLE_CLIENT_SECRET` + `GOOGLE_REFRESH_TOKEN` | Blogger |
| `BLOGGER_BLOG_ID` | Blogger 博客 ID |
| `WECHATSYNC_TOKEN` | 文章同步助手 |

### 极限铺量模式（用户反复要求"加量"时）

- ≤5 篇：逐篇 humanizer
- 5-50 篇：模板化 + patch 关键篇
- 50+ 篇：Python 批量 + 仅 top 5 hero 全量质量
