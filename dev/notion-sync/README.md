# Notion Sync 工作区

> **目标（2026-06-08 修订）**：Notion = Obsidian 的**全文备份**；本地完善期仍以本地编写，**切换后 Notion 成为主库**。
>
> 控制层文件仍放本地；密钥不进 Notion。

---

## 战略（与旧版 index_only 相反）

| 阶段 | 谁写 | 谁存全文 | 说明 |
|------|------|----------|------|
| **P1 现在** | 本地 Obsidian | **Notion 镜像全文** | 本地改完 → 推完整正文到 Notion |
| **P2 切换** | Notion 为主 | Notion | 本地降为导出/归档副本 |
| **P3 稳定** | Notion | Notion | 任务/状态双向；脚本仍可从 Git 拉 |

**切换门控**（`sync-manifest.json` → `ssot_roadmap.cutover_gate`）：

- 本地目录结构稳定
- B1–B7 批次全文已在 Notion 可检索
- 抽样对账（标题 + 路径 + 正文 hash）通过

---

## 文件说明

| 文件 | 用途 |
|------|------|
| `sync-scope.json` | **纳入/排除清单**（开发环境、备份、过时 vs Skills/知识库/报告） |
| `sync-manifest.json` | **SSOT**：镜像策略与批次 ID |
| `notion-databases.schema.json` | 库字段定义；正文在 **页面 body**，不只属性 |
| `notion-targets.json` | Command Center 与各库 data_source_id |
| `official-records.json` | 已建索引记录（待升级为全文镜像） |
| `backfill-queue.csv` | 历史队列（**待回填 notion_id + 标 synced**） |

---

## 线上入口

- 主控：[LifeOS/PARA Command Center](https://app.notion.com/p/378fc0c71bd581798f67dc2f306257d7)
- 运行日志：[Lovart Ops Reports](https://app.notion.com/p/1d50d2daf96d41b29739b67a80c0e714)（与 Reports/Insights、Automation Runs 合并镜像）

---

## 全文同步规则

1. **每个 `.md` / `.mdc`** → 对应 Notion 页，**整篇正文**写入 page content（非仅 Summary 字段）。
2. **脚本 / JSON / workflow** → 代码块或附件式全文进 Notion 页。
3. **大文件**（>5MB）→ 摘要 + `Source Path` + 外链，不进正文。
4. **密钥** → 永不进 Notion。
5. 每条记录保留：`Local ID`、`Source Path`、`content_hash`、`Last Synced At`。
6. **冲突**：切换前 **local wins**；切换后 **notion wins**。

---

## 纳入 / 排除（见 `sync-scope.json`）

### 纳入 Notion 全文

| 类别 | 本地路径 | Notion 库 |
|------|----------|-----------|
| **关键知识库** | `1-1 GEO Readme/文档/`、`AGENTS.md`、`定期任务/` 等 | Resources |
| **内容链接清单** | `1-3 Content Gen/CONTENT_LINK_INDEX.md`（轻量索引，不含正文草稿） | Resources |
| **确定 Agent Skills** | 24 个 `lovart-*` Skill + Sentinel（仅 SKILL/SOP/references） | Resources |
| **Harness** | `harness/AGENTS.md`、`WORKFLOWS.md`、Skill 枢纽 `.md` | Resources |
| **各类报告** | `insight-data/` 下 `.md` 报告；`~/Documents/Lovart Local Dev/Output/` 仅同步轻量摘要 / Ops Reports | Reports/Insights |
| **自动化文档** | `08/09` 蓝图、`dev/automation/` 说明与脚本 | Automations |

### 明确不同步

| 类别 | 路径/模式 |
|------|-----------|
| 开发环境 | `sanity-studio-copies/`、`dev/lovart.sanity.studio/`、`node_modules/` |
| 备份 / 重输出 | `1-8 Backup/`、`1-7 Output/`、`~/Documents/Lovart Local Dev/Output/` 大 JSON |
| 过时 | 被 `08/09` 取代的 PRD/迁移方案；`*审计*.md`、`*清理记录*.md` |
| 副本/噪音 | `故事线文档副本/`、`Lovart-Automation/`、`00-core/` 通用 Skill |
| 凭证与原始采集 | `credentials/`、`Lovart ORM/raw/*.json` |
| Skill 代码层 | `scripts/`、`samples/`、`_fixtures/`（只同步 SKILL 文档层） |

**本次不在范围**：`1-3 Content Gen/` 正文草稿（除非你后续点名策略文档）。

---

## 优先批次

| 批次 | 内容 | 优先级 |
|------|------|--------|
| K1 | 关键知识库 GEO Readme | P0 |
| S1 | 确定 Agent Skills 全文 | P0 |
| H1 | Harness 枢纽 | P0 |
| R1 | Trident + Sentinel 报告 | P0 |
| R3 | Output 运行/审计 | P0 |
| R2 | Keywords + Page Analytic | P1 |
| A1 | 自动化脚本与蓝图 | P1 |

---

## 标准流程（全文版）

1. 扫描批次内本地文件，算 `content_hash`。
2. 查 Notion 是否已有同 `Local ID` / `Source Path` 页。
3. **新建或更新** Notion 页 body = 本地全文。
4. 更新库属性：Status、Period、Type 等。
5. 本地 frontmatter 回填 `notion_id`、`notion_url`、`sync_status=synced`。
6. 每周：Notion 导出 CSV + 关键页 Markdown 到 `1-8 Backup/notion-exports/`。

---

## 状态约定

| 状态 | 说明 |
|------|------|
| `pending_full_mirror` | 仅有索引或尚未推送正文 |
| `synced` | 全文已镜像，hash 一致 |
| `stale` | 本地已改，Notion 待更新 |
| `conflict` | 两边都改，人工裁决 |
| `skipped` | 明确不同步（密钥/超大文件） |

---

## 当前差距（相对新策略）

| 项 | 现状 | 目标 |
|----|------|------|
| Resources 等 35 条索引 | 只有标题+路径 | 补 **全文 body** |
| Reports/Insights | 1 条占位 | B3：200+ 报告全文 |
| Automation Runs | 0 条 | B8：每次 run 全文 |
| Lovart Ops Reports | 3 条元数据 | 合并为 run 全文 |
| backfill-queue.csv | 全 `needs-confirmation` | 回填 ID，标 `synced` |

---

## 执行方式

- **Agent / Cursor**：按批次调用 Notion MCP `notion-create-pages` / `notion-update-page`，content = 本地文件全文。
- **Automation（待建）**：`lovart-notion-full-mirror-nightly` — 扫 `stale` + 新文件推送。
- **人工**：Command Center → Reports And Audits 视图验收。

旧原则「Notion 管索引、本地管正文」已废弃，见 `sync-manifest.json` → `deprecated_policy`。
