---
type: knowledge-tree-narrative
version: 1.0
updated: 2026-07-05
companion: tree.yaml
audience: [Hermes, OpenCode, Cursor, Claude, Codex]
---

# Knowledge Tree — Lovart MFlow

> 这是项目级 SSOT 的"叙事索引"。任意 agent 启动时第一份必读。
> 当机器要查"谁依赖谁"时，去 `tree.yaml`；
> 当你要知道"这些东西是怎么分类、为什么分"时，留在这里。

---

## 三大层 — 自顶向下

```
Layer 0  Tools        : 5 个 AI agent 入口（Hermes / OpenCode / Cursor / Claude / Codex）
Layer 1  Harness      : 1-1 Harness/ = 项目控制中枢（rules / skills / workflows / knowledge）
Layer 2  Vault        : Obsidian vault 三层目录（Project / Resource / Dev）
Layer 3  Delivery     : Sanity / GitHub / Wechatsync / DEV.to / Medium / WP（外部触点）
```

**铁律**：任意 agent 启动时 = Layer 0 → Layer 1 → Layer 2 → Layer 3 顺序加载。
反之写动作时 = Layer 3 → Layer 2 → Layer 1（先生产，再归位，最后看知识树）。

---

## Layer 1 — Harness 内部九宫格

```
01-project/   = 项目介绍、PRD、季度计划          → 谁读：新人 / 管理层
02-rules/     = RULES-00*60 + SESSION-ROUTING   → 谁读：所有 Profile 必须
03-workflows/ = WORKFLOWS.md + workflow-chain   → 谁读：操作时查 SOP
04-setup/     = README + 凭证清单 + 路径契约     → 谁读：首次部署时
05-skills/    = Skill 实体（Hermes SSOT）        → 谁读：Hermes（仅它）
06-cron/      = 12 个定时任务                    → 谁读：运维
07-okr/       = 月度 OKR                        → 谁读：管理 / 月初
08-storyline/ = 落地页故事线 SSOT                → 谁读：创作
09-scripts/   = 运维脚本（check-deps, sync-skills）→ 谁读：运维
10-config/    = 凭证 / 集成的导引               → 谁读：首次部署
11-knowledge/ = 知识树 + 记忆 + 梦境 + 审计（本目录）→ 谁读：所有
Docs/         = 阶段 S1-S6 详细 SOP            → 谁读：操作时按阶段
```

> ⚠️ `05-skills/` 仅 Hermes 写；其他工具的技能库在 `.claude/skills/` / `.cursor/skills/` / `~/.hermes/skills/lovart/`，与 05 同源不同形，由 `09-scripts/sync-skills.sh` 双向同步。

---

## Layer 1.5 — 6 工作线到文件（极简映射）

读这张图就足够回答 "我这条工作线会碰哪些文件"：

| 工作线 | Profile | 关键 Rules | 关键 Skills | 关键路径 |
|--------|---------|------------|-------------|---------|
| 报告 | lovart-reports | RULES-10 | sentinel / trident / data-ingestion | `1-2 Insight/`, GSC exports |
| 创作 | lovart-creation | RULES-20 | blog-signal-writer / page-serp-writer / landing-page / refresh-page-generator / image-generation | `1-3 GenFlow/`, Sanity drafts |
| 质量 | lovart-quality | RULES-30 | content-quality-gates / content-audit / anti-slop | preflight reports |
| 运维 | lovart-ops | RULES-40 | sanity-publish / sitemap / IndexNow | `1-4 Dev/scripts/`, `1-3 GenFlow/CONTENT_LINK_INDEX.md` |
| 分发 | lovart-distribution | RULES-50 | multi-platform-push / content-distribution | `1-3 GenFlow/Content Distribution/` |
| 管理 | lovart-management | RULES-60 | project-architecture / knowledge-graph-query / dream-orchestrator | `1-1 Harness/11-knowledge/` |

---

## Layer 2 — Vault 三层（更细）

```
1-Project/Lovart MFlow/   ← 源码层（skills/rules/scripts，全量版本控制）
1-2 Insight/              ← 资源层（情报资产：ORM / Trident / Keywords / Knowledge Base / Page Analytic / 审计报告）
1-3 GenFlow/              ← 创作层（Content Strategy / Content Calendar / Page Gen / Blog Pipeline / Distribution）
1-4 Dev/                  ← Dev 层（automation / notion-sync / scripts / Sanity Composite README 等）
```

**生产关系**：1-2 喂选题 → 1-3 写产出 → 1-4 发布。
**回流**：1-4 发布的 Sanity 状态回写 1-3 GenFlow/CONTENT_LINK_INDEX.md；监控（GSC/Sentinel）回流 1-2。

---

## Layer 3 — External Delivery 触点

| 目的地 | Owner Skill | 凭证 |
|--------|------------|------|
| Sanity (o11tm2qe / prod) | `lovart-sanity-publish` + `*-sanity-publish` 各分支 | `~/.config/sanity/config.json` |
| IndexNow | `lovart-sitemap-update` | 无 |
| GitHub | `lovart-multi-platform-push` | `$LOVART_GH_TOKEN` |
| DEV.to | 同上 | `$DEVTO_API_KEY` |
| Medium | 同上 | `$MEDIUM_TOKEN` |
| Wechatsync（公众号） | `lovart-multi-platform-push` | 飞书 webhook |
| Discord / Reddit / LinkedIn | 同上 | 各自 PAT |

**铁律**：发布落外部前必须先过质量门 + preflight BLOCK=0。详见 RULES-00 与 RULES-30。

---

## 轴：三件事的横切视角

### 1. 数据流（从监测到回流）

1. **采集 S1**：GSC + GA4 + Bing → `1-2 Insight/From Datawork/` → `Trident Insights/`
2. **策略 S2**：Trident 产出 OKR + 内容短板 → `1-3 GenFlow/Content Strategy/` → `Content Calendar/`
3. **创作 S3**：博客（`Lovart-Blog-Pipeline/`）+ 落地页（`Page Gen/`）+ 翻译队列
4. **质检 S4**：preflight + anti-slop → 通过/SLAP？不通过回 S3
5. **部署 S5**：Sanity import + Sitemap + IndexNow + 各平台分发 → `Content Distribution/`
6. **监控 S6**：Sentinel + GSC 月报 → 回流到 1-2 形成闭环

### 2. 控制流（按 agent / Profile）

```
                   ┌─────────────────────────────────────────────┐
                   │  Layer 0: 任意 agent 启动                   │
                   │  → 读 11-knowledge/README.md                │
                   │  → 读 KNOWLEDGE-TREE.md (本文件)            │
                   │  → 按 Profile 决定 Rules 加哪些             │
                   └────────────────┬────────────────────────────┘
                                    │
        ┌──────────┬──────────┬─────┴──────┬──────────┬──────────┐
        ▼          ▼          ▼            ▼          ▼          ▼
     reports    creation    quality       ops       dist       mgmt
        │          │          │            │          │          │
        ▼          ▼          ▼            ▼          ▼          ▼
     RULES-10   RULES-20   RULES-30    RULES-40    RULES-50   RULES-60
        │          │          │            │          │          │
        └──────────┴──────────┴─────┬──────┴──────────┴──────────┘
                                    │
                                    ▼
                   dream/audit.sh 每夜跑 → patch 建议
```

### 3. 生命周期（cron × profile × 数据集）

频率 vs 工作线交叉：

| 频率 | Profile | 工作线 | 产物 |
|------|---------|--------|------|
| 每日 02:30 | dream (no-profile) | 梦境 | MEMORY-PROJECT.md + entity 增量 + Hermes 反推 |
| 每日 08:00 | lovart-seo | 报告 | 舆情日报 |
| 每日 09:00 | lovart-content | 创作 | 自媒体稿件 |
| 每周一 02:00 | lovart-seo | 运维 | Sitemap |
| 每周一 09:00 | lovart-seo | 报告 | 内容健康度 |
| 每周三 20:00 | lovart-seo | 报告 | SEO 复盘周报 |
| 每周五 10:00 | lovart-seo | 报告 | i18n 缺口 |
| 每月 | lovart-seo | 报告 | 月报 + 季度 + 年度 |

完整 12 cron 见 `06-cron/README.md` + `02-rules/RULES-60-management.md`。

---

## 元数据：本文件看了之后还要看什么

- 想知道"X 路径下的全部文件是怎么连的" → `tree.yaml`
- 想查"哪些 skill 在哪些工具里启用" → `queries/cross-tool-skills.md`
- 想知道"用户累积的事实与纠正" → `MEMORY-PROJECT.md` + `~/.hermes/memories/{MEMORY,USER}.md`
- 想动手构造 → `Dream/README.md`（手动触发梦境）
- 担心"工具之间不一致" → `audit/reports/latest.md`
- 想新增工作线/Profile/Skill → 看 `Dream/README.md` 的"append" 章节 + 这本 README 的「六大不」

---

## 元原则：本架构边界

本架构**不**替代：

- 任何 RULES 单文件：RULES-00/RULES-10.../RULES-60 仍是各 Profile 工作时的硬约束
- 任何具体 Skill 的 SOP：每个 skill 仍以自己 `SKILL.md` 为真相
- 任何凭证文件：本目录从不存 token

本架构**只**是：让 5 个 agent 都能在 30 秒内找到 "我在哪、我能碰什么、别人在做什么、今天有没有踩坑"。
