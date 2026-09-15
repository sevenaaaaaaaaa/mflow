# Lovart Harness — 主索引 v3.1

> 最后更新：2026-09-13（v3.1 现状校准：全部条目已对照磁盘实存核验；v3.0 及以前引用的已删除文件已清理）
> 定位：Lovart GEO 全自动内容营销项目的「控制中枢」。本文档是 Harness 目录的编号索引与入口指南。

---

## 会话启动门禁（任何 agent 先跑这个）

```bash
bash "1-4 Dev/scripts/session-init.sh"        # 4 道门禁：pipeline-state / router / next / governance
```

- GATE 1-3 全过 = 会话可以开工；状态机 SSOT：`1-3 GenFlow/.pipeline/pipeline-state.json`
- 创作任务先问路由器：`python3 "1-1 Harness/Skills/06-orchestrate/lovart-router/router.py" decide --stage S3 --scenario blog`
- 调度真相：launchd 三任务（daily 08:00 / weekly 周一 07:00 / dream 02:30），定义见 `1-4 Dev/automation/automation-manifest.json`

---

## 目录编号体系（v3.1 实存核验版）

| 编号 | 目录 | 定位 | 必读 |
|:---:|------|------|:---:|
| **00** | `00-INDEX.md` | 本文件 — 主索引 | — |
| **01** | `01-project/` | 项目背景、季度计划、迁移 PRD | ✅ |
| **02** | `02-rules/` | RULES-00~60 + SESSION-ROUTING | ✅ |
| **03** | `03-workflows/` | 部署上线方案 PRD | — |
| **04** | `04-setup/` | 首次部署、路径契约 | ✅ |
| **05** | `05-skills/` | 技能使用指南 + 入口治理 | — |
| **06** | `06-cron/` | 月度任务 + macOS 自动化 + 运行看板 | — |
| **07** | `07-okr/` | OKR 与半年总结 | — |
| **08** | `08-storyline/` | 落地页故事线 SSOT | — |
| **09** | `09-scripts/` | TOOLS-REGISTRY + profile 同步 | — |
| **10** | `10-config/` | GSC/Notion/双轨/产出路由配置导引 | — |
| **11** | `11-knowledge/` | **Knowledge · Memory · Dream · Audit**（5 工具共享 SSOT） | ✅（任意工具启动时） |
| **Skills/** | `Skills/` | **45 个 skill 实体**（6 分组 + 编排层） | 按需 |
| **Docs/** | `Docs/` | 按阶段的详细操作手册（S0-S6） | — |

---

## 01 — 项目介绍（实存 7 文件）

| 文件 | 内容 |
|------|------|
| `项目背景与利益方沟通.md` | 项目背景、业务目标、利益方 |
| `Lovart-SEO-Q3-Tactical-Plan-2026.md` | Q3 SEO 战术计划 |
| `PRD-codebox-deployment.md` | codebox 内网平台部署 PRD（骨架已建，推进搁置） |
| `PRD-本地到线上迁移.md` | 本地→云端容器化迁移 PRD（Draft，未评审） |
| `迁移说明-codebox.md` / `迁移说明-本地到线上.md` | 两套迁移的操作说明 |
| `url-utm-custom.md` | UTM 参数备忘 |

## 02 — 核心规则（按工作线分层加载）

### 全局铁律（所有 Profile 必载）

| 文件 | 内容 |
|------|------|
| `02-rules/RULES-00-iron.md` | **不可违反的铁律**：Sanity 管道 / 行为 / Anti-Slop / SEO 通用 / 路径 |
| `02-rules/SESSION-ROUTING.md` | 会话路由：一条会话只做一类事 |
| `../Docs/S4-质量审核/Anti-Bugs.md` | 已知 bug 注册表（原 ANTI-BUGS-REGISTRY 实体在 Docs/S4） |

### 工作线规则（按 Profile 加载）

| 文件 | Profile | 路线 |
|------|---------|------|
| `02-rules/RULES-10-reports.md` | `lovart-reports` | SEO报告 / 舆情 / SERP / OKR（必须环比） |
| `02-rules/RULES-20-creation.md` | `lovart-creation` | Blog / Landing / Topic（v1.1 含 Column-Writer Lane） |
| `02-rules/RULES-30-quality.md` | `lovart-quality` | 三层门禁 L1/L2/L3 + Anti-Slop |
| `02-rules/RULES-40-ops.md` | `lovart-ops` | Sitemap / IndexNow / CRO / 素材 |
| `02-rules/RULES-50-distribution.md` | `lovart-distribution` | 四条分发轨道 |
| `02-rules/RULES-60-management.md` | `lovart-management` | 三层目录 / Profile / Cron / 知识管理 |

## 03 — 工作流

| 文件 | 内容 |
|------|------|
| `03-workflows/PRD-部署上线方案.md` | 部署上线方案 |
| `../1-4 Dev/automation/automation-manifest.json` | **调度自动化 SSOT**：3 primary + 4 extended + legacy 清单 |
| `../1-4 Dev/automation/run-daily-pipeline.sh` | 每日管线：GSC → Sentinel → 飞书 → harness 汇总/同步 |
| `../1-4 Dev/automation/run-weekly-pipeline.sh` | 每周管线（周一 07:00） |
| `../1-4 Dev/automation/run-monthly-pipeline.sh` | 每月管线（每月 3 号 06:00） |

> 注：v3.0 引用的 `WORKFLOWS.md` / `workflow-chain.md` 已不存在；操作 SOP 以 `Docs/` 各阶段手册 + 各 skill 的 SKILL.md 为准。

## 04 — 首次部署（实存 2 文件）

| 文件 | 内容 |
|------|------|
| `04-setup/README.md` | 新人自搭建指南 |
| `04-setup/路径契约.md` | Lovart Local Dev 目录结构约定（⚠️ 2026-09-13 校准：vault 根 = `~/Obsidian/MindRe/MindRe`，Local Dev = `~/Documents/Lovart Local Dev`） |

> 凭证位置：`1-1 Harness/Skills/01-strategy/lovart-trident-data-engine/credentials/`（GSC/GA4/飞书/service-account）+ `1-4 Dev/scripts/sentinel/{gsc,ga4,bing}_credentials/` + `1-4 Dev/Google Cloud Oath/`（OAuth client）。

## 05 — 技能树

| 文件 | 内容 |
|------|------|
| `05-skills/skills-usage.md` | 技能使用指南（按 S1-S6 阶段映射） |
| `05-skills/skill-entrypoint-governance.md` | 入口治理：每场景唯一父入口 + support-only 规则 |
| `Skills/` | 45 个 skill 实体（01-strategy 4 / 02-creation 15 / 03-review 3 / 04-publish 8 / 05-monitor 2 / 06-orchestrate 12 / 顶层 1） |

> Skill 真相 = 本 vault `Skills/` 目录。`~/.hermes/` 运行时由 `1-4 Dev/scripts/harness_sync.py` 从 vault 重新生成（每日管线 D07 步骤）。

## 06 — 定时任务

| 文件 | 内容 |
|------|------|
| `06-cron/03-每月任务.md` | 月度 SEO 报告 |
| `06-cron/04-macos本机自动化.md` | launchd 混合调度 |
| `06-cron/自动化运行看板.md` | 自动化运行看板 |
| `../1-4 Dev/automation/automation-manifest.json` | 调度 SSOT（见 03 节） |

> 当前生效（2026-09-13 重接）：launchd `com.lovart.daily-pipeline`（08:00）/ `com.lovart.weekly-pipeline`（周一 07:00）/ `com.lovart.dream`（02:30）。Cursor Automations 方案保留在 manifest，待用户在 Cursor UI 保存后可替代 launchd。

## 07 — OKR

| 文件 | 内容 |
|------|------|
| `07-okr/OKR.md` | 当前 OKR 主文件 |
| `07-okr/2026 年 1-2 月总结.md` | 上半年复盘 |
| `07-okr/2026 年 3-4 月总结.md` | 季中复盘 |

> 月度 OKR 文件已并入 `OKR.md`；月度目标数值见 `1-2 Insight/Trident Insights/reports/monthly/` 最新月报。

## 08 — 故事线

| 文件 | 内容 |
|------|------|
| `08-storyline/STORYLINES.md` | 7 类页面故事线速查 |
| `08-storyline/STORYLINE-BY-DIRECTION.md` | 完整故事线体系（25 条，含 Topic 6 条） |
| `08-storyline/FEATURES-PRODUCTION.md` | Features 生产规范（同名带 " 2" 后缀的是 iCloud 冲突副本，待清理） |

## 09 — 运维脚本

| 文件 | 内容 |
|------|------|
| `09-scripts/TOOLS-REGISTRY.md` | **脚本注册表 SSOT**（新脚本创建前必查重） |
| `09-scripts/sync-profile-skills.sh` | Profile ↔ Skill 同步 |
| `09-scripts/lovart-data-flow-map.md` | 数据流地图 |

## 10 — 配置

| 文件 | 内容 |
|------|------|
| `10-config/lovart-gsc-api-setup-guide.md` | GSC API 配置 |
| `10-config/lovart-notion-config.md` | Notion 集成 |
| `10-config/obsidian-notion-dual-track.md` | Obsidian ↔ Notion 双轨制 |
| `10-config/产出路由规则.md` | 产出路由四问规范（RULES-00 配套） |
| `10-config/README-Lovart-SEO-Toolkit.md` | SEO 工具箱 |
| `10-config/hermes-lovart-profiles.md` | Hermes Profile 说明 |

## 11 — Knowledge · Memory · Dream · Audit

> **5 工具共享 SSOT**。任何 agent 启动时或大改之前先来本目录刷新上下文。

| 文件 | 内容 |
|------|------|
| `11-knowledge/README.md` | 架构总览：知识树 / 记忆 / 梦境 / 审计 |
| `11-knowledge/KNOWLEDGE-TREE.md` | 三层叙事索引（Layer 0-3） |
| `11-knowledge/MEMORY-PROJECT.md` | 项目事实速查（用户纠正/踩坑/状态机协议） |
| `11-knowledge/entities.yaml` + `relationships.yaml` | 实体库（98）/ 关系库（111）SSOT |
| `11-knowledge/scripts/kg` | 图查询 CLI（stats / list / related-to / orphans） |
| `11-knowledge/scripts/fm-check.py` | frontmatter 校验 |
| `11-knowledge/dream/` | 梦境（consolidate.sh / audit.sh / lovart.dream.plist） |
| `11-knowledge/audit/` | 审计报告（checks/ + reports/） |
| `11-knowledge/sessions/` | 会话日志（每段会话收尾必写，见 skill `lovart-session-log`） |

---

## Docs/ — 阶段操作手册

| 编号 | 目录 | 内容 |
|:---:|------|------|
| S0 | `Docs/00-系统总览.md` | 系统架构全景 |
| S1 | `Docs/S1-数据采集/` | GSC·GA4·Bing·Sentinel 采集 |
| S2 | `Docs/S2-内容策略/` | 内容复盘与缺口分析 |
| S3 | `Docs/S3-内容创作/` | Blog·Features·Tools·i18n 创作 |
| S4 | `Docs/S4-质量审核/` | Anti-Slop·Anti-Bugs·Content Quality |
| S5 | `Docs/S5-发布部署/` | Sanity 管道·Sitemap·部署方案 |
| S6 | `Docs/S6-监控分析/` | SEO 报告标准 |
| — | `Docs/分发自动化/` | 多平台分发 SOP |
| — | `Docs/参考配置/` | 环境配置·跨平台迁移 |
| — | `Docs/03-角色手册/` | 按角色的操作指南 |

---

## 快速入口（新人 5 分钟路径）

1. 读 `01-project/项目背景与利益方沟通.md` — 这是什么项目
2. 读 `11-knowledge/README.md` + `KNOWLEDGE-TREE.md` — 项目知识架构
3. 读 `02-rules/RULES-00-iron.md` — 铁律（必须遵守）
4. 跑 `bash "1-4 Dev/scripts/session-init.sh"` — 确认管线门禁全绿
5. 按 `02-rules/SESSION-ROUTING.md` 选工作线，加载对应 RULES

---

## Agent 自动加载清单

| 优先级 | 文件 | 用途 |
|:---:|------|------|
| P0 | `11-knowledge/README.md` | 知识/记忆/梦境/审计 SSOT |
| P0 | `11-knowledge/KNOWLEDGE-TREE.md` | 三层架构叙事索引 |
| P0 | `11-knowledge/MEMORY-PROJECT.md` | 项目事实速查 |
| P0 | `02-rules/RULES-00-iron.md` | 铁律 |
| P1 | `00-INDEX.md` | 本文件 — 全局导航 |
| P1 | `bash 1-4 Dev/scripts/session-init.sh` | 启动门禁（可执行检查） |
| P2 | `05-skills/skills-usage.md` | Skill 路由 |

---

## 维护规则

- **新增文档**：按编号体系放入对应目录，更新本索引
- **废弃文档**：移至 `1-8 Backup/archives/`（vault 外）或 Local Dev Backup，勿留 `_old` / `_v2` 后缀文件
- **Skill 更新**：改 vault `Skills/`（真相），运行时副本由 `harness_sync.py` 重新生成
- **新脚本**：先查 `09-scripts/TOOLS-REGISTRY.md` 防重复，创建后走 `lovart-new-tool-governance` 注册
- **路径引用**：禁止硬编码绝对路径，统一用 `$LOVART_RESOURCE_ROOT` / `$LOVART_LOCAL_DEV_ROOT`（定义见 `1-4 Dev/automation/local-dev-env.sh`）
