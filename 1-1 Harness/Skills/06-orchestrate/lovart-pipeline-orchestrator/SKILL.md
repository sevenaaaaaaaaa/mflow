---
name: lovart-pipeline-orchestrator
description: Lovart 内容自动化 Pipeline 主编排器 v2.0 — Sentinel 报告落地自动触发 8 步闭环。Step 1 由 Trident Data Engine 提供三引擎 SEO 数据，下游对接 18 个 Skill。
---

# lovart-pipeline-orchestrator

## 路径契约

| 层 | 路径 |
|----|------|
| 文档 SSOT | `1-1 GEO Readme/` |
| Sanity 脚本 | `1-4 Dev/lovart.sanity.studio/scripts/` |
| SEO/Sentinel 脚本 | `1-4 Dev/scripts/` |
| 自动化 | `1-4 Dev/automation/` |
| 本 Skill | `1-1 Harness/Skills/lovart-pipeline-orchestrator/SKILL.md` |

> **Current structure note（2026-06-07）**：本文件是 pipeline 历史总控和编排心智模型，保留旧结构信息用于自动化排障与迁移追溯。当前执行入口以 `1-1 GEO Readme/README.md`、`WORKFLOWS.md`、`1-4 Dev/scripts/`、`1-4 Dev/lovart.sanity.studio/`、`1-1 Harness/Skills/` 为准。
>
> **Legacy structure note**：下文出现的旧 `Skills/`、`Lovart/`、`sanity-studio/`、`Wordpress/Lovart-Blogs/` 等路径是迁移前快照，不代表可直接删除或废弃；涉及自动化、Skill、SOP、production import 的内容必须先审计依赖。

Lovart 内容自动化 Pipeline 主编排器 v2.0 — Sentinel 报告落地自动触发 8 步闭环。Step 1 由 Trident Data Engine 提供三引擎 SEO 数据，下游对接 18 个 Skill。

## Triggers

- "运行完整 pipeline" / "run full pipeline"
- "内容生产全流程" / "end-to-end content flow"
- **自动触发**：Sentinel 报告落地到 `1-2 Insight/Lovart ORM/`

## Folder Monitoring

```
监控目录: 1-2 Insight/Lovart ORM/
触发条件: 新 Lovart-Sentinel-YYYY-MM-DD-daily.md 落地
动作: 自动启动 Step 1 → Full Pipeline
```

---

## 全系统架构 v2.0

```
                   Sentinel 报告落地（外部生成）
                            │
                            ▼ (自动检测)
┌──────────────────────────────────────────────────────────────────────────┐
│                       LOVART CONTENT PIPELINE v2.0                        │
│                                                                           │
│  Step 1       Step 2        Step 3        Step 3.5    Step 4    Step 5    Step 7
│  三引擎采集    日历更新       内容创作       图片生成     质量门禁   分发推送   Sitemap
│                                                                           │
│  ┌──────────┐ ┌──────────┐ ┌────────────────────┐ ┌──────────┐ ┌───────┐ │
│  │Trident   │ │content-  │ │ Sanity 三条管道:     │ │image-    │ │multi- │ │
│  │Data      │ │calendar  │ │                     │ │generation│ │platfm │ │
│  │Engine    │ │          │ │ sanity-content-     │ │          │ │push   │ │
│  │          │ │          │ │ publish（路由）      │ │Lovart    │ │       │ │
│  │┌───────┐ │ │          │ │  ├ sanity-publish   │ │API       │ │bridge │ │
│  ││GSC API│ │ │          │ │  ├ features-publish │ │→CDN回写  │ │→Feishu│ │
│  ││GA4 API│ │ │          │ │  └ tools-publish    │ │          │ │Bitable│ │
│  ││Bing   │ │ │          │ │                     │ └──────────┘ │  ↓    │ │
│  │└───────┘ │ │          │ │ content-writer v4   │              │content│ │
│  │    ↓     │ │          │ │ features-page v2.3  │              │-dist  │ │
│  │unified   │ │          │ │ landing-page        │              │engine │ │
│  │brief     │ │          │ │ blog-automation     │              │22 API │ │
│  │          │ │          │ │                     │              │平台   │ │
│  │kw-intake │ │          │ └────────────────────┘              └───────┘ │
│  │+sentinel │ │          │                                               │
│  └──────────┘ └──────────┘                                               │
│                                                                           │
│  质量门禁: L1 preflight-content → L2 verify-blog-publish → L3 audit       │
│                                                                           │
│  ▸ 串行 ▸ BLOCK 回退 Step 3 ▸ 失败重试 3 次后标记手动                      │
└──────────────────────────────────────────────────────────────────────────┘
                            │
                            ▼
                   Output/Pipeline Reports/
```

---

## Step → Skill 映射

| Step | Skill | 职责 |
|------|-------|------|
| **1** | `lovart-trident-data-engine` | GSC+GA4+Bing 三引擎采集 → 统一情报摘要 |
| **1b** | `lovart-keywords-intake` | v1.0 — 8 种关键词分类器 + P0/P1/P2 评分 |
| **1c** | `lovart-sentinel` | 舆情数据采集 (15 条并行 webfetch) |
| **2** | `lovart-content-calendar` | 14 品类 × 5 语言 → 三大日历 → creation-tasks |
| **3a** | `lovart-content-writer` | v4.0 — 12 类型 × 11 框架 → Sanity Blog MD |
| **3b** | `lovart-features-page` | v2.3 — 5 组件 × 11 语言 × 6 角色 → Features JSON |
| **3c** | `lovart-landing-page` | 6 区块 × 10 语言 × 5 维定制 → Landing Page JSON |
| **3d** | `lovart-blog-automation` | WordPress 博客 (publish-to-wp.py) |
| **3.5** | `lovart-image-generation` | Lovart API 生成封面/配图 + CDN 回写 |
| **4a** | `lovart-content-quality-gates` | L1 预检 + L2 落库抽查 |
| **4b** | `lovart-content-audit` | L3 审计 (质量/SEO/全球合规/文化敏感/品牌一致性) |
| **5** | `lovart-multi-platform-push` | 写入飞书 Bitable → content-distributor 引擎 |
| **5r** | `lovart-sanity-content-publish` | 三条 Sanity 管道路由器 |
| **7** | `lovart-sitemap-update` | generate-all.py → deploy → ping Google/Bing |

---

## Step 1 详解: Trident Data Engine

### 一键执行

```bash
cd 1-1 Harness/Skills/lovart-trident-data-engine && bash scripts/run_all.sh
```

### 产出

| 文件 | 来源 | 典型大小 |
|------|------|---------|
| `gsc-full.json` | Google Search Console (28d, 100 关键词) | 21KB |
| `ga4-full.json` | Google Analytics 4 (30d, 有机流量全景) | 24KB |
| `bing-full.json` | Bing Webmaster：`keywords_monthly`/`pages_monthly`（每周 top~100 词按月聚合，键名对齐 GSC）+ `traffic_monthly`（站点级）+ crawl | 620KB |
| `intelligence-brief.md` | 三源统一情报摘要 | 2KB |

### 独立 Skill

详见 `1-1 Harness/Skills/lovart-trident-data-engine/SKILL.md` — 含完整配置引导、维度矩阵、报告标准。

**SEO 正式报告（日/周/月/季/年）额外强制：**
- 所有维度环比（见 `AGENTS.md` A0；月报 5 月 vs 4 月，周报 vs 上同型窗）
- GSC 关键词：点击+曝光+CTR + 三者环比；细分含点击/曝光占比
- **跑报告前 Agent 须问用户 OKR 是否更新**（默认 2026-05 版）
- **月报必须用** `seo_monthly_v2.py`（见 `AGENTS.md` **A0d–A0h**）：§一 含 **30秒速览+🔴P0+TL;DR**；§三 卡 A–F + **C-Bing/D-Bing/E-Bing**；§四–§十一 **Google+Bing 结构对称**（§4.12–4.16、§8.7–8.11、§9.4–9.6、§11.10）；每节 💡 引擎差异；`--resume` 可补 GA4 `bing_region_ga4`
- **Bing 硬限制（须在报告脚注）**：词样本~200+/月（非 GSC 5K）；分地区用 GA4 `country×sessionSource(bing)` 行为近似；收录仅 InIndex 参考
- 月报命令：`--month YYYY-MM`；中断 `--resume`；改模板 `--render-only`；重拉收录 `--refresh-indexing`
- 代码 SSOT：`seo_report_standards.py`；月报扩展：`seo_monthly_extras.py`

---

## 三条 Sanity 管道

| 管道 | Skill | 脚本 | 类型 | SSOT |
|------|-------|------|------|------|
| Blog | `lovart-sanity-publish` | `convert.js` | `blog` | `Sanity-Blog-发布统合指南.md` (664 行) |
| Features | `lovart-features-sanity-publish` | `convert-features.js` | `compositePage` | 统合指南 |
| Tools | `lovart-tools-sanity-publish` | `convert-tools.js` | `compositePage` | 统合指南 |

**铁律**: `import --missing` only · 永不 `sanity deploy` · 永不改 schema · 首次 `sync-blog-taxonomy` + 小批量 `--dry-run`

## 质量门禁

| 层级 | Skill | 时机 | 脚本 |
|------|-------|------|------|
| L1 | `lovart-content-quality-gates` | convert 前 | `preflight-content.js` |
| L1 | `lovart-content-quality-gates` | import 前 | NDJSON 预检 |
| L2 | `lovart-content-quality-gates` | import 后 | `verify-blog-publish.js` |
| L3 | `lovart-content-audit` | 发布前 | 5 维审计 |

## 执行模式

| 模式 | 触发 | 步骤 | 用时 |
|------|------|------|------|
| **Full** | 自动 (报告落地) 或 `run full pipeline` | 1→7 | ~2-4h |
| **Quick** | `run quick pipeline` | 2→7 | ~1-2h |
| **Data-only** | `trident fetch` | 1 (仅数据) | ~2min |
| **Write-only** | `write and publish {slug}` | 3→7 | ~30min |
| **Audit-only** | `audit {slug}` | 4 | ~5min |
| **Push-only** | `push all drafts` | 5→7 | ~15min |
| **SEO-only** | `update seo assets` | 7 | ~10min |

---

## 关键路径

### 当前结构映射（2026-06）

```text
1-Project/
├── 1-1 GEO Readme/                  ← 文档中枢、治理记录、命令索引
├── 1-2 Insight/                     ← Sentinel / Trident / Keywords 报告产出
├── 1-3 Content Gen/                 ← Blog Pipeline、Content Calendar、Page Gen
├── 1-4 Dev/                     ← 脚本 SSOT、Sanity Studio、自动化、Output
│   ├── scripts/trident/             ← GSC / GA4 / Bing 可执行入口
│   ├── scripts/sentinel/            ← 舆情采集与 fallback plist
│   ├── automation/                  ← tools-pull 等自动化脚本
│   └── lovart.sanity.studio/        ← 当前 Sanity schema + convert/import 脚本
├── 1-1 Harness/Skills/              ← Agent Skill、SOP、历史兼容入口
├── 1-6 Knowledge Base/              ← 语料库
├── 1-7 Output/                      ← 历史输出索引（新重输出默认外置）
└── 1-8 Backup/                      ← 历史副本归档索引（新重备份默认外置）
```

本机重输出、只读线上拉取缓存和 Git 外置维护区默认在 `~/Documents/Lovart Local Dev/`。首次复刻先运行 `bash "1-4 Dev/automation/bootstrap-local-dev.sh"`；迁移 `1-7 Output/`、`1-8 Backup/` 或 `.git` 前必须单独备份并获得确认。

### Legacy 快照（迁移前结构，保留用于追溯）

```
1-Project/
├── Skills/
│   ├── lovart-trident-data-engine/      ← 三引擎 Skill (Step 1)
│   ├── LOVART-AUTOMATION-WORKFLOW.md     ← 完全体文档 SSOT
│   └── lovart-data-flow-map.md          ← 数据流 SSOT
├── Lovart/
│   ├── 1-6 Knowledge Base/
│   │   └── Sentinel Insights/reports/  ← 监控触发
│   ├── 1-3 Content Gen/Content Calendar/     ← 3,221 篇 Blog MD
│   ├── Pages/                            ← Features/Tools JSON
│   ├── sanity-studio/                    ← convert.js / scripts
│   ├── 1-2 Insight/Trident Insights/reports/            ← 三引擎 JSON 输出
│   ├── Sitemap/                          ← SEO 资产
│   └── scripts/sentinel/                 ← 舆情脚本
└── Wordpress/Lovart-Blogs/               ← WordPress
```

## Onboarding (新人接手指南)

当前新人入口：先读 `1-1 GEO Readme/README.md` → `WORKFLOWS.md` → `SETUP_CHECKLIST.md`。下面 1–6 是迁移前 orchestration 快照，执行命令前需映射到当前结构。

1. 读 `Skills/LOVART-AUTOMATION-WORKFLOW.md` — 完全体文档
2. `bash Skills/check-deps.sh`
3. 配置三引擎: `1-1 Harness/Skills/lovart-trident-data-engine/references/setup-guide.md`
4. Sanity 首次: `Skills/lovart-sanity-publish/references/SOP-Lovart-Sanity-Blog-Features-Tools-换设备交接与首次运行.md`
5. 测试: `cd 1-1 Harness/Skills/lovart-trident-data-engine && bash scripts/run_all.sh`
6. 启动: 说 "运行完整 pipeline" 或等 Sentinel 报告落地

---

## 参考索引

当前路径优先；表内 `Skills/...`、`Lovart/...` 属 legacy 相对路径时，映射到 `1-1 Harness/Skills/...`、`1-4 Dev/...` 或 `1-3 Content Gen/...` 后再执行。

| 文档 | 路径 |
|------|------|
| **完全体工作流** | `Skills/LOVART-AUTOMATION-WORKFLOW.md` |
| Trident Engine SKILL | `1-1 Harness/Skills/lovart-trident-data-engine/SKILL.md` |
| 数据流地图 | `Skills/lovart-data-flow-map.md` |
| Sanity Blog SSOT | `Skills/lovart-sanity-publish/Sanity-Blog-发布统合指南.md` |
| 换设备交接 SOP | `Skills/lovart-sanity-publish/references/SOP-Lovart-Sanity-Blog-Features-Tools-换设备交接与首次运行.md` |
| Notion 配置 | `Skills/lovart-notion-config.md` |
| Lovart API 配置 | `Skills/lovart-api-config.md` |
| GSC API 引导 | `Skills/lovart-gsc-api-setup-guide.md` |
| 内容管道 Cursor 规则 | `Lovart/.cursor/rules/lovart-sanity-content-pipeline.mdc` |
| Sentinel 配置 | `1-4 Dev/scripts/sentinel/config.yaml` |
| **Anti-Bugs SSOT** | `1-1 GEO Readme/ANTI-BUGS-REGISTRY.md` |

---

## Anti-Bugs（禁止再犯）

> 全量目录：[ANTI-BUGS-REGISTRY.md](../../../1-1%20GEO%20Readme/ANTI-BUGS-REGISTRY.md) · AGENTS.md Part B7

**Step 4（质量门禁）额外检查点**

| 步骤 | 必做 | 相关 ID |
|------|------|---------|
| L1 preflight | BLOCK=0 或用户确认 WARN | AB-P04, AB-P05 |
| Blog 深度 audit | PASS / CONDITIONAL | AB-C01~C03 |
| 图片 HTTP（批次后） | `audit-blog-covers` / `audit-composite-images-404` = 0 | AB-I04, AB-I05 |

**Step 5（发布）额外检查点**

| 禁止 | 相关 ID |
|------|---------|
| 跳过 dry-run 直接 production mutate | AB-A01 |
| 无用户授权全量 convert+import | AB-P02, AB-A03 |
| READ token 写库 | AB-E04 |

**BLOCK 回退**：preflight BLOCK 或 audit BLOCK → 回退 Step 3；勿在 Step 5 用 `--replace` 强行覆盖。
