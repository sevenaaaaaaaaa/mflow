## Imported Claude Cowork project instructions

Lovart 自动化内容生产流程，包括情报监测、内容生产、内容分发、各种质检。情报监测，包括舆情监测\SEO报告\SERP实时抓取；内容生产，包括Blog生产、各类落地页生产（Feature\Tool\Product\Scenario\Solution\Topic）的生产；内容分发，包括国内外各类自媒体和内容社区内容分发，主要内容是每日抓取github上的优质项目与本地知识库结合。质检系统，实际上分为anti bug\anti slop\blog和落地页显示错误、排版错误\CRO影响因素等。

## Cursor Agent 技能库

Skill 实体唯一真相在 `1-1 Harness/Skills/`（45 个 SKILL.md，6 分组 + 编排层）。Cursor 侧规则由 `1-4 Dev/scripts/harness_sync.py` 每日编译到 `.cursor/rules/*.mdc`（lovart-core / quality-gates / blog / landing-page / sanity-publish / seo-report-iron-rules）；不存在独立的 `.cursor/skills/` 或 `.claude/skills/` 目录。Cursor 任务从 `lovart-core` 起步，按阶段加载对应 skill；细节 SOP 以 Harness 为准。站外 T1/T2/T3 自媒体写作父入口：`ai-self-media-article`（T2 专用加深：`lovart-t2-deep-dive`）。

## 会话启动门禁（所有工具必做）

每段会话**开始时**先跑：

```bash
bash "1-4 Dev/scripts/session-init.sh"
```

4 道门禁（pipeline-state / router / next / governance）全过才开工。调度真相：launchd `com.lovart.daily-pipeline`（每日 08:00）/ `com.lovart.weekly-pipeline`（周一 07:00）/ `com.lovart.dream`（02:30）。

## Knowledge · Memory · Dream · Audit（Codex 与所有工具必读）

> **首先读这里**：1-1 Harness/11-knowledge/README.md → KNOWLEDGE-TREE.md → MEMORY-PROJECT.md。
> 知识树 + 记忆 + 梦境 + 一致性审计的 SSOT。
> 任意 agent 启动时应当先读 `1-1 Harness/00-INDEX.md` 选 Profile，再读本目录刷新上下文。
> 工具切换 / Profile 切换 / 大改动之前，调用 skill `lovart-dream-orchestrator` 跑一次 audit。

## Session 收尾（所有工具必做！）

每段会话**结束前**自动或主动触发 skill **`lovart-session-log`** — 写结构化 Session Log 到 `1-1 Harness/11-knowledge/sessions/{YYYY-MM-DD}-{slug}.md`。

**触发信号**（任一即可）：
- 用户说"这轮可以收尾"、"写日志"、"归档"、"wrap up"、"log this"、"session 完结"、"本轮收尾"
- Agent 自己判断：触达 ≥ 5 个文件 / 做了 ≥ 1 个 schema 改动 / ≥ 1 个新 skill/rule 落地

**触发后**：写 draft 状态 log → 给用户看 → 用户确认 → status: ready → 写入磁盘。

不写日志 = silent loss（会话 lessons 全部流失）。**不允许跳过**。
