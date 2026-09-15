---
type: tool-entrypoint/claude
version: 1.0
updated: 2026-07-05
scope: "tool-claude"
tools: [claude]
status: active
path: 1-1 Harness/CLAUDE.md
generator: 1-1 Harness/11-knowledge/scripts/fm-fix.py
---
# Lovart MFlow — Claude

Claude 打开 `1-1 Harness/` 时的项目记忆。技能库见 `.claude/skills/`（Claude 专用副本，与 Hermes 的 `Skills/` 独立）。

## 启动顺序（每次会话开头执行）

1. **强制首读**：`1-1 Harness/11-knowledge/README.md`（30 秒浏览）→ `KNOWLEDGE-TREE.md`（按需细读）→ `MEMORY-PROJECT.md`（事实速查）
2. **选 Profile**：依据用户意图选 6 条工作线之一，对应加载 `RULES-00-iron.md` + `RULES-{10..60}.md`
3. **再读**：`1-1 Harness/00-INDEX.md` 选章节
4. **改前后 audit**：在改 entities/relationships/入口文件之前/之后跑 `bash 1-1 Harness/11-knowledge/dream/audit.sh`

知识图查询用 `bash 1-1 Harness/11-knowledge/scripts/kg <subcommand>`，梦境编排用 `bash 1-1 Harness/11-knowledge/dream/consolidate.sh`，详见对应 SKILL.md：`lovart-knowledge-graph-query` + `lovart-dream-orchestrator`。

## 会话收尾（重要！）

每段会话**结束前**自动或主动触发 skill **`lovart-session-log`** — 写结构化 Session Log 到 `1-1 Harness/11-knowledge/sessions/{YYYY-MM-DD}-{slug}.md`。

**触发信号**（任一即可）：
- 用户说"这轮可以收尾"、"写日志"、"归档"、"wrap up"、"log this"、"session 完结"、"本轮收尾"
- Agent 自己判断：触达 ≥ 5 个文件 / 做了 ≥ 1 个 schema 改动 / ≥ 1 个新 skill/rule 落地

**触发后**：写 draft 状态 log → 给用户看 → 用户确认 → status: ready → 写入磁盘。

不写日志 = silent loss（会话 lessons 全部流失）。**不允许跳过**。

## 规则

- Sanity：仅 `import --missing`；**禁止** `deploy` / `--replace` / 删 production。
- 发布类技能停在发布前等人工授权（`status: ready`），不自动无人值守发布。
- WordPress 发布前必须先 `--dry-run`。
- 飞书凭证、Sanity token 等不提交 git。

## 技能库

- **Cursor 体系**：`../.cursor/skills/`（Cursor Agent 执行入口，精简版）
- Claude 体系：`.claude/skills/`（本会话自动发现，全部带 frontmatter）
- Hermes/OpenCode 原件：`Skills/`（SSOT，勿改，供 Hermes 继续使用）
- 阶段与技能索引：`.claude/skills/README.md`、`../.cursor/skills/README.md`、`05-skills/skills-usage.md`

## 常用入口

- 舆情监测：`lovart-sentinel`
- 数据/SEO：`lovart-data-ingestion`、`lovart-trident-data-engine`
- 内容日历：`lovart-content-calendar`
- Blog 生产：`lovart-blog-automation`、`lovart-blog-signal-writer`、`lovart-complete-guide`
- 落地页：`lovart-landing-page`、`lovart-page-serp-writer`、`refresh-page-page-generator`
- 质检：`lovart-content-quality-gates`、`lovart-content-audit`
- 发布：`lovart-sanity-content-publish`（路由）→ 各 `*-sanity-publish`
- 分发：`lovart-multi-platform-push`、`lovart-content-distribution`
- 编排：`lovart-pipeline-orchestrator`、`lovart-content-creation-orchestrator`

## 角色子代理（≈Hermes 档案）

位于 `.claude/agents/`，各预载对应阶段技能到独立上下文（省主线程 token）。用法：说"用 lovart-blog 写…"或 `@agent-lovart-blog`；`--agent lovart-intel` 可整场只用该角色。

- `lovart-intel` — 情报监测（sentinel + trident；data-ingestion 可发现）
- `lovart-blog` — Blog 生产（blog-signal-writer；blog-automation/image-generation 可发现）
- `lovart-page` — 落地页生产（landing-page + page-serp-writer；refresh-page 可发现）
- `lovart-qa` — 质检（content-quality-gates；content-audit 可发现）
- `lovart-publisher` — Sanity 发布路由（sanity-content-publish → 各 *-sanity-publish）
- `lovart-distributor` — 多平台分发（multi-platform-push；content-distribution 可发现）
- `lovart-orchestrator` — 全流程编排（pipeline + content-creation-orchestrator；content-calendar）

改动 agent 文件后需重启会话生效；用 `/agents` 界面创建/编辑则即时生效。

## 路径契约（SSOT）

- 文档 SSOT：`1-1 GEO Readme/`
- Sanity 脚本：`1-4 Dev/lovart.sanity.studio/scripts/`
- SEO/Sentinel 脚本：`1-4 Dev/scripts/`
- 自动化：`1-4 Dev/automation/`
