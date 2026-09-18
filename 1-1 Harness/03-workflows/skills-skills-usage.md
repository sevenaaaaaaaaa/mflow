# 1-1 Harness — Skills 使用指南（2026-09-13 校准）

> **本目录职责**：Agent 技能使用指南与入口治理规则。Skill 实体在 `../Skills/`（45 个 SKILL.md）。
> **技能按流水线阶段组织**，与 `../Docs/` S1-S6 阶段手册对齐。

---

## 流水线阶段 → 技能映射

入口治理标准：[`skill-entrypoint-governance.md`](skill-entrypoint-governance.md)

```
S1-数据采集 → S2-内容策略 → S3-内容创作 → S4-质量审核 → S5-发布部署 → S6-监控分析
     ↓              ↓              ↓              ↓              ↓              ↓
  01-strategy    01-strategy    02-creation    03-review     04-publish     05-monitor
```

| 阶段 | Skills 目录 | 技能 | 说明 |
|------|------------|------|------|
| **S1 数据采集** | `01-strategy/` | `lovart-trident-data-engine` | 三引擎数据采集（GSC+GA4+Bing） |
| | | `lovart-data-ingestion` | 数据摄入（简化版） |
| **S2 内容策略** | `01-strategy/` | `lovart-content-calendar` | 内容日历排期（关键词 intake 并入，不保留独立入口） |
| | | `lovart-kb-ingest` | 知识库摄取（KB units） |
| **S3 内容创作** | `02-creation/` | `lovart-blog-signal-writer` | **Blog 唯一入口**：所有语言所有 Blog，不翻译不走 i18n 管线 |
| | | ~~`lovart-blog-serp-writer`~~ | ⛔ 已弃用 → 使用 `lovart-blog-signal-writer` |
| | | ~~`lovart-blog-automation`~~ | ⛔ 已弃用 → 使用 `lovart-blog-signal-writer` |
| | | `lovart-landing-page` | **落地页唯一父入口**：Tools/Features/Product/Scenario/Solution/Topic 生成与刷新 |
| | | `lovart-page-serp-writer` | support-only：由 `lovart-landing-page` 内部调用 |
| | | `refresh-page-page-generator` | support-only：bodyJson/type 序列生成器 |
| | | `lovart-complete-guide` / `lovart-insight-trend` / `lovart-best-practice` / `lovart-review` / `lovart-stack-by-stack` / `lovart-thought-leadership` / `lovart-101` | Blog 分类子 skill（必须经 signal-writer 父入口路由） |
| | | `lovart-image-generation` | 封面/横幅图片生成 |
| | | `lovart-kb-mine` | 写作前 KB 挖掘 |
| **S4 质量审核** | `03-review/` | `lovart-content-quality-gates` | L1-L7 质量门禁（含 Anti-Slop, i18n L5） |
| | | `lovart-content-audit` | 深度审计 |
| | | ~~`lovart-sanity-preflight`~~ | ⚠️ 已废弃，合并到 quality-gates |
| **S5 发布部署** | `04-publish/` | `lovart-sanity-publish` | **Sanity 发布唯一父入口**：Blog/Features/Tools/Product/Scenarios |
| | | `lovart-sanity-content-publish` / `lovart-features-*` / `lovart-tools-*` / `lovart-product-*` / `lovart-scenarios-*` | support-only：各分类执行管道 |
| | | `lovart-multi-platform-push` | 多平台分发父入口 |
| | | `lovart-content-distribution` | 分发渠道管理 |
| | | `ai-self-media-article` | 站外自媒体写作父入口（T2 加深：`lovart-t2-deep-dive`） |
| **S6 监控分析** | `05-monitor/` | `lovart-sentinel` (40-sentinel/) | 品牌舆情监控 |
| | | `lovart-sitemap-update` | Sitemap/llms.txt/robots.txt 更新 |

### 编排层（06-orchestrate/，12 个）

**现代三件套（有代码 + 有测试，生产依赖）**：

| 技能 | 说明 | 验证 |
|------|------|------|
| `lovart-pipeline-state` | 12-stage 状态机 SSOT（`1-3 GenFlow/.pipeline/`），8 个子命令，非法转换 exit 2 | smoketest 39/39 |
| `lovart-router` | stage+scenario → profile/skills 路由决策（23 条矩阵），6 个 active profile | smoketest 15/15 |
| `lovart-new-tool-governance` | 新脚本 6-gate 门禁 + TOOLS-REGISTRY 注册 | governance_check.py |

**质量与记忆**：`lovart-quality-cascade`（writer→critic 循环，explicit-only）、`lovart-universal-prompt`（全 profile 行为基座）、`lovart-dream-memory`、`lovart-dream-orchestrator`（梦境手动入口）

**会话与编排**：`lovart-session-log`（收尾必写）、`lovart-session-recap`（40 词回顾）、`lovart-content-creation-orchestrator`（创作总控，Step 0 = pipeline_state next + router decide）、`lovart-knowledge-graph-query`

> `lovart-pipeline-orchestrator` 为历史遗留（v2.0 心智模型），仅作参考不再作为执行入口。
> 质量钩子（bash 层）在 `1-4 Dev/scripts/hooks/`：pre-write / post-write / pre-import / post-generation（smoketest 16/16）。

---

## 目录结构（实存）

```
1-1 Harness/
├── 00-INDEX.md                  ← 主索引（v3.1）
├── 01-project/ ~ 10-config/     ← 见 00-INDEX 编号体系
├── 05-skills/                   ← 本目录（使用指南 + 入口治理）
├── Skills/                      ← 45 个 skill 实体（真相源）
│   ├── 01-strategy/  02-creation/  03-review/
│   ├── 04-publish/   05-monitor/   06-orchestrate/
│   └── lovart-better-design/       ← 顶层独立 skill
├── 11-knowledge/                ← 知识/记忆/梦境/审计 SSOT
└── Docs/                        ← S0-S6 阶段手册
```

---

## 跨目录依赖

| 本目录 | 引用自 | 说明 |
|--------|--------|------|
| Skills | `02-rules/RULES-*.md` | 规则 SSOT |
| Skills | `1-4 Dev/scripts/` | SEO/Sentinel/hooks 脚本 SSOT |
| Skills | `1-4 Dev/lovart.sanity.studio/scripts/` | Sanity 脚本 |
| Skills | `~/Documents/Lovart Local Dev/` | 运行时输出/凭证/缓存（`$LOVART_LOCAL_DEV_ROOT`） |
