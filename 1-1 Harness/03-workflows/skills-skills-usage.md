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
| **S1 数据采集** | `01-strategy/` | `trident-data-engine` | 三引擎数据采集（GSC+GA4+Bing） |
| | | `data-ingestion` | 数据摄入（简化版） |
| **S2 内容策略** | `01-strategy/` | `选题计划（strategy-content.md）+ 自动排程` | 内容日历排期（关键词 intake 并入，不保留独立入口） |
| | | `kb-ingest` | 知识库摄取（KB units） |
| **S3 内容创作** | `02-creation/` | `blog-writer` | **Blog 唯一入口**：所有语言所有 Blog，不翻译不走 i18n 管线（2026-10-03 四合一） |
| | | ~~`blog-serp-writer` / `blog-automation` / 8 类型子技能~~ | ⛔ 已并入 `blog-writer` |
| | | `landing-writer` | **落地页唯一父入口**：Tools/Features/Product/Scenario/Solution/Topic 生成与刷新 |
| | | `hub-writer` | **聚合页唯一入口**：目录/榜单/主题 Hub，策略性 SEO 页（≥8 详情页前置） |
| | | ~~`page-serp-writer` / `refresh-page-page-generator` / `features-page.md`~~ | ⛔ 已并入 `landing-writer` references |

| | | 类型结构 | 内置于 `blog-writer/references/types/`（8 类 GUIDE） |
| | | `image-generation` | 封面/横幅图片生成 |
| | | `kb-mine` | 写作前 KB 挖掘 |
| **S4 质量审核** | `03-review/` | `content-quality-gates` | L1-L7 质量门禁（含 Anti-Slop, i18n L5） |
| | | `content-audit` | 深度审计 |
| | | ~~`sanity-preflight`~~ | ⚠️ 已废弃，合并到 quality-gates |
| **S5 发布部署** | `04-publish/` | `sanity-publish` | **Sanity 发布唯一父入口**：Blog/Features/Tools/Product/Scenarios |
| | | `sanity-content-publish` / `mflow-features-*` / `mflow-tools-*` / `mflow-product-*` / `mflow-scenarios-*` | support-only：各分类执行管道 |
| | | `multi-platform-push` | 多平台分发父入口 |
| | | `content-distribution` | 分发渠道管理 |
| | | `ai-self-media-article` | 站外自媒体写作父入口（T2 加深：`mflow-t2-deep-dive`） |
| **S6 监控分析** | `05-monitor/` | `mflow-sentinel` (40-sentinel/) | 品牌舆情监控 |
| | | `sitemap-update` | Sitemap/llms.txt/robots.txt 更新 |

### 编排层（06-orchestrate/，12 个）

**现代三件套（有代码 + 有测试，生产依赖）**：

| 技能 | 说明 | 验证 |
|------|------|------|
| `pipeline-state` | 12-stage 状态机 SSOT（`1-3 GenFlow/.pipeline/`），8 个子命令，非法转换 exit 2 | smoketest 39/39 |
| `router` | stage+scenario → profile/skills 路由决策（23 条矩阵），6 个 active profile | smoketest 15/15 |
| `new-tool-governance` | 新脚本 6-gate 门禁 + TOOLS-REGISTRY 注册 | governance_check.py |

**质量与记忆**：`quality-cascade`（writer→critic 循环，explicit-only）、`universal-prompt`（全 profile 行为基座）、`dream-memory`、`dream-orchestrator`（梦境手动入口）

**会话与编排**：`session-log`（收尾必写）、`session-recap`（40 词回顾）、`content-creation-orchestrator`（创作总控，Step 0 = pipeline_state next + router decide）、`knowledge-graph-query`

> `pipeline-orchestrator` 为历史遗留（v2.0 心智模型），仅作参考不再作为执行入口。
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
│   └── better-design/       ← 顶层独立 skill
├── 11-knowledge/                ← 知识/记忆/梦境/审计 SSOT
└── Docs/                        ← S0-S6 阶段手册
```

---

## 跨目录依赖

| 本目录 | 引用自 | 说明 |
|--------|--------|------|
| Skills | `02-rules/RULES-*.md` | 规则 SSOT |
| Skills | `1-4 Dev/scripts/` | SEO/Sentinel/hooks 脚本 SSOT |
| Skills | `1-4 Dev/品牌.sanity.studio/scripts/` | Sanity 脚本 |
| Skills | `~/Documents/MFlow Local Dev/` | 运行时输出/凭证/缓存（`$MFLOW_LOCAL_DEV_ROOT`） |
