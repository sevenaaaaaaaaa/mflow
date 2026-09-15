# LifeOS/PARA 云端迁移实施方案

> 目标：把当前依赖 Obsidian 文件夹/文件的工作流，迁移为以 Notion 对象数据库为主、Markdown/Git 可回退的 LifeOS 系统。第一阶段只迁移活跃对象和正在运行的工作流，不搬运历史噪音。

---

## 1. 当前系统盘点

### 1.1 现有目录职责

| 目录 | 当前职责 | 迁移判断 |
|---|---|---|
| `1-1 GEO Readme/` | 文档中枢、系统总览、角色手册、质量规则、自动化状态 | 迁移为 Resources、SOP、Automation Catalog |
| `1-2 Insight/` | SEO、ORM、关键词、DataWorks 等报告产出 | 活跃报告进入 Reports/Insights；历史报告保留 Markdown 归档 |
| `1-3 Content Gen/` | 内容源、Calendar、Page Gen、Blog Pipeline | 迁移为 Content Pipeline 主对象 |
| `1-4 Dev/` | 工程 SSOT、Sanity Studio、脚本、自动化入口 | 只迁移项目/脚本索引；代码与脚本继续留本地/Git |
| `1-1 Harness/` | Skills、Agent 规则、控制配置 | 迁移为 Skills Catalog、Agent Workflow、Automation Runs |
| `1-6 Knowledge Base/` | 语料库和长期知识 | 只迁移高价值索引，正文继续 Markdown 或外部归档 |
| `1-7 Output/` | 审计、报告、生成结果 | 近期输出进入 Reports/Automation Runs；历史输出保留归档 |
| `1-8 Backup/` | 历史副本、旧版本、archives | 不迁移为 Notion 主对象，只建立 Archive Index |

### 1.2 活跃工作流

| 工作流 | 当前入口 | Notion 化对象 |
|---|---|---|
| SEO 周报/月报 | `weekly_review_v3.py`、`seo_monthly_v2.py` | Report、Automation Run、Task |
| Sentinel 舆情日报 | `scripts/sentinel/` | Report、Automation Run、Monitoring Signal |
| Tools Pull | `automation/tools-pull/`、Cursor Automation 草稿 | Automation、Automation Run |
| 内容健康检查 | `automation/content-health/weekly-health-check.sh` | Automation、Quality Gate、Run |
| Blog/Features/Tools 发布 | `Content Gen` + `Sanity` 管道 | Content Item、Publish Task、Quality Gate |
| Skills/Agent 工作流 | `1-1 Harness/Skills/` | Skill、Workflow、SOP |

### 1.3 不迁移原则

- `node_modules`、临时构建产物、`.tmp`、历史 archives 不进入 Notion 主数据库。
- 脚本、源码、Sanity Studio 继续以 Git/本地工程为 SSOT，Notion 只记录入口、负责人、状态、运行记录。
- 长篇历史报告不全文搬入 Notion；只迁移标题、周期、指标摘要、链接、结论和归档路径。

---

## 2. Notion 核心数据库

### 2.1 Areas

长期责任领域，用来替代 PARA 中的 Area 文件夹。

| 字段 | 类型 | 说明 |
|---|---|---|
| Name | Title | 领域名称，如 GEO、Content、Automation、Knowledge System |
| Status | Select | Active、Paused、Archived |
| Owner | Person/Text | 负责人 |
| Operating Cadence | Select | Daily、Weekly、Monthly、Ad hoc |
| Related Projects | Relation | 关联 Projects |
| Related Resources | Relation | 关联 Resources |
| Success Metrics | Text | 领域判断指标 |
| Source Path | URL/Text | 原 Obsidian 路径 |

### 2.2 Projects

活跃项目和阶段性目标，不承载所有历史文件夹。

| 字段 | 类型 | 说明 |
|---|---|---|
| Name | Title | 项目名 |
| Area | Relation | 所属 Area |
| Status | Select | Planning、Active、Waiting、Done、Archived |
| Priority | Select | P0、P1、P2、P3 |
| Outcome | Text | 项目要达成的结果 |
| Owner | Person/Text | 负责人 |
| Start Date | Date | 开始时间 |
| Due Date | Date | 截止时间 |
| Tasks | Relation | 关联 Tasks |
| Content Items | Relation | 关联 Content Pipeline |
| Resources | Relation | 关联 Resources |
| Automations | Relation | 关联 Automations |
| Source Path | URL/Text | 原始目录或主文档路径 |
| Archive Policy | Select | Keep in Notion、Markdown archive、Do not migrate |

### 2.3 Tasks

执行层对象，替代散落在 Markdown 中的 TODO。

| 字段 | 类型 | 说明 |
|---|---|---|
| Name | Title | 任务名 |
| Status | Select | Inbox、Next、Doing、Blocked、Review、Done、Archived |
| Project | Relation | 所属项目 |
| Area | Rollup/Relation | 来自 Project 或手动指定 |
| Priority | Select | P0、P1、P2、P3 |
| Due Date | Date | 截止时间 |
| Context | Multi-select | Cursor、Sanity、SEO、Writing、Review、Ops |
| Definition of Done | Text | 完成标准 |
| Source | URL/Text | 来源文档、聊天、脚本或报告 |
| Run Required | Checkbox | 是否需要脚本/自动化 |
| Related Run | Relation | 关联 Automation Runs |

### 2.4 Resources

长期资料、SOP、规则、方法论、prompt、外部链接。

| 字段 | 类型 | 说明 |
|---|---|---|
| Name | Title | 资料名 |
| Type | Select | SOP、Rule、Prompt、Research、Reference、Template、Decision |
| Area | Relation | 所属 Area |
| Status | Select | Current、Needs Review、Deprecated、Archived |
| Source Path | URL/Text | Markdown 源路径 |
| Canonical Location | Select | Notion、Markdown、Git、External |
| Related Projects | Relation | 相关项目 |
| Tags | Multi-select | 主题标签 |
| Last Reviewed | Date | 最近审阅时间 |
| Summary | Text | 只写摘要，不复制长文全文 |

### 2.5 Content Pipeline

内容生产主数据库，覆盖 Blog、Tools、Features、Pages、SEO Brief、Refresh。

| 字段 | 类型 | 说明 |
|---|---|---|
| Title | Title | 内容标题 |
| Content Type | Select | Blog、Tool、Feature、Page、Brief、Refresh、Programmatic |
| Status | Select | Idea、Brief、Draft、Review、Ready、Published、Refresh Needed、Archived |
| Priority | Select | P0、P1、P2、P3 |
| Target Keyword | Text | 主关键词 |
| Slug | Text | URL slug |
| Language | Select | en、de、zh、zh-TW、ja、ko、fr、ru、pt、it |
| Project | Relation | 关联 Project |
| Owner | Person/Text | 负责人 |
| Quality Gate | Relation | 关联 Quality Gates 或 Tasks |
| Publish Target | Select | Sanity、WordPress、Static、Other |
| Published URL | URL | 线上地址 |
| Source Path | URL/Text | 原 Markdown 或 JSON 路径 |
| Sanity ID | Text | 如适用 |
| Last Performance Review | Date | 最近复盘时间 |

### 2.6 Automations

自动化定义，不记录每次运行结果。

| 字段 | 类型 | 说明 |
|---|---|---|
| Name | Title | 自动化名称 |
| Status | Select | Active、Paused、Needs Setup、Deprecated |
| Runtime | Select | launchd、Cursor Automation、CLI、Manual、External |
| Cadence | Select/Text | Daily、Weekly、Monthly、Manual |
| Entry Command | Text | 可复制入口命令或脚本 |
| Owner | Person/Text | 负责人 |
| Related Project | Relation | 关联项目 |
| Related Area | Relation | 关联领域 |
| Output Path | Text | 输出目录或报告路径 |
| Risk Level | Select | Low、Medium、High |
| SOP | Relation | 关联 Resources |

### 2.7 Automation Runs

每次 AI、脚本、发布、审计、报告生成的运行日志。

| 字段 | 类型 | 说明 |
|---|---|---|
| Name | Title | `{Automation} - {YYYY-MM-DD HH:mm}` |
| Automation | Relation | 自动化定义 |
| Status | Select | Queued、Running、Succeeded、Failed、Partial、Skipped |
| Started At | Date | 开始时间 |
| Finished At | Date | 结束时间 |
| Trigger | Select | Schedule、Manual、Agent、Webhook |
| Input | Text/Files | 关键输入，不粘贴大正文 |
| Output Summary | Text | 结果摘要 |
| Output Path | URL/Text | 日志或报告路径 |
| Error | Text | 错误摘要 |
| Follow-up Tasks | Relation | 关联 Tasks |

### 2.8 Assets

图片、设计稿、代码片段、账号配置说明、外部素材等可复用资产。密钥和 token 不进入 Notion，只记录保管位置和使用边界。

| 字段 | 类型 | 说明 |
|---|---|---|
| Name | Title | 资产名称 |
| Asset Type | Select | Image、Design、Code Snippet、Credential Pointer、Dataset、Template、External Link |
| Status | Select | Active、Needs Review、Deprecated、Archived |
| Area | Relation | 所属 Area |
| Project | Relation | 相关 Project |
| Content Items | Relation | 相关 Content Pipeline |
| Storage Location | Select | Local、Git、Sanity、Figma、Notion、Cloud Drive、External |
| Source Path | URL/Text | 本地路径、外部链接或管理入口 |
| Usage Notes | Text | 使用方式、限制、授权说明 |
| Last Verified | Date | 最近验证时间 |

### 2.9 Reports/Insights

建议新增，避免把 SEO/ORM 报告塞进 Resources。

| 字段 | 类型 | 说明 |
|---|---|---|
| Name | Title | 报告名 |
| Report Type | Select | SEO Daily、SEO Weekly、SEO Monthly、Sentinel、Audit、Research |
| Period | Date/Text | 报告周期 |
| Area | Relation | 所属领域 |
| Status | Select | Draft、Published、Archived |
| Key Insight | Text | 1-3 条核心结论 |
| Source Path | URL/Text | Markdown 报告路径 |
| Related Run | Relation | 关联 Automation Run |
| Follow-up Tasks | Relation | 关联 Tasks |

---

## 3. 路径到 Notion 字段映射

### 3.1 通用映射

| Obsidian 信号 | Notion 字段 | 规则 |
|---|---|---|
| 一级目录，如 `1-3 Content Gen` | Area | 按目录职责映射到 Area |
| 二级目录，如 `Lovart-Blog-Pipeline` | Project 或 Resource Type | 如果有明确产出/状态，建 Project；否则建 Resource |
| 文件名 | Name/Title | 去掉序号和日期噪音后作为标题 |
| YAML `tags` | Tags/Context | 保留为 Multi-select |
| YAML `created` | Created Date | 如 Notion API 导入可保留 |
| Markdown H1 | Title 备选 | H1 优先于文件名 |
| README.md | Resource/SOP | 作为目录索引或 SOP |
| `workflow`、`SOP`、`指南` | Resource Type | 标为 SOP 或 Workflow |
| `Output`、`reports` | Reports/Insights | 不进入普通 Resources |
| `automation`、`.workflow.json`、`launchd` | Automations | 建自动化定义 |
| 日志、审计 JSON | Automation Runs | 只保留摘要和路径 |

### 3.2 顶层目录映射

| 当前路径 | Area | 默认目标数据库 |
|---|---|---|
| `1-1 GEO Readme/文档/00-系统总览.md` | GEO Operations | Resources |
| `1-1 GEO Readme/文档/06-自动化状态.md` | Automation | Automations、Resources |
| `1-2 Insight/` | Insights | Reports/Insights |
| `1-3 Content Gen/` | Content | Content Pipeline、Projects |
| `1-4 Dev/automation/` | Automation | Automations |
| `1-4 Dev/scripts/` | Engineering | Resources，仅索引入口 |
| `1-1 Harness/Skills/` | Agent System | Resources、Automations |
| `1-7 Output/quality-audits/` | Quality | Reports/Insights、Automation Runs |
| `1-8 Backup/archives/` | Archive | Archive Index，不迁正文 |

### 3.3 对象判定规则

1. 有明确截止、负责人、状态、交付物：建 Project。
2. 可执行的一步动作：建 Task。
3. 可定期运行或被 Agent/脚本触发：建 Automation。
4. 自动化的一次结果：建 Automation Run。
5. 可复用知识、规则、模板：建 Resource。
6. 面向发布的文章、页面、brief、刷新项：建 Content Pipeline。
7. 一次性报告或审计结论：建 Report/Insight。

---

## 4. 第一阶段试迁移批次

### 4.1 批次 A：GEO 自动化主控

| 对象 | 来源 | 目标 |
|---|---|---|
| Area: GEO Operations | `1-1 GEO Readme/` | Areas |
| Project: Lovart GEO Automation | `1-1 GEO Readme/README.md` | Projects |
| Resource: 系统总览/角色手册/质量治理 | `1-1 GEO Readme/文档/` | Resources |
| Automation: Tools Pull | `automation/tools-pull/`、`.cursor/automations/lovart-tools-pull.workflow.json` | Automations |
| Automation: 内容健康检查 | `automation/content-health/` | Automations |
| Task: 确认 launchd 与 Cursor Automation 二选一 | `06-自动化状态.md` | Tasks |

验收标准：
- Notion 中能从 Project 打开关联的 SOP、自动化、最近输出路径。
- Tools Pull 和内容健康检查各有一条 Automation 定义。
- 不复制脚本正文，只保留命令、路径、风险和运行记录。

### 4.2 批次 B：内容生产管线

| 对象 | 来源 | 目标 |
|---|---|---|
| Area: Content Production | `1-3 Content Gen/` | Areas |
| Project: Lovart Blog Pipeline | `1-3 Content Gen/Lovart-Blog-Pipeline/` | Projects |
| Content Item: SEO Brief/Draft/Refresh | Blog Pipeline 和 Page Gen 中的活跃项 | Content Pipeline |
| Resource: Blog 写作规范/发布 SOP | README、SOP、Skill 文档 | Resources |
| Automation: Sanity Publish / WordPress Publish | Sanity/WordPress 发布入口 | Automations |

验收标准：
- 选 10 条以内活跃内容进入 Content Pipeline。
- 每条内容至少有 Status、Content Type、Slug、Source Path、Publish Target。
- 历史已发布内容只建索引，不全文搬迁。

### 4.3 批次 C：报告与审计

| 对象 | 来源 | 目标 |
|---|---|---|
| Report: SEO Weekly/Monthly | `1-2 Insight/` 与脚本输出 | Reports/Insights |
| Report: Sentinel | `Lovart ORM` 输出 | Reports/Insights |
| Report: Quality Audit | `1-7 Output/quality-audits/` | Reports/Insights |
| Automation Run | 最近一次报告/审计运行 | Automation Runs |

验收标准：
- 每类报告只迁最近 1-3 个样本。
- 每个 Report 有 Period、Key Insight、Source Path、Follow-up Tasks。
- 审计 JSON 不全文放 Notion，只记录摘要和文件路径。

---

## 5. 备份与导出策略

### 5.1 备份层级

| 层级 | 内容 | 频率 | 存放 |
|---|---|---|---|
| Notion 原生导出 | Workspace HTML/Markdown/CSV | 每周或重大变更前 | 本地备份目录 |
| 数据库 CSV 导出 | Core Databases | 每周 | Git 或云盘 |
| Markdown 归档 | Notion 关键页面导出 | 每月 | Obsidian Archive |
| API 快照 | JSON 化数据库记录 | 每日或每周 | Git ignored raw backup + 加密云盘 |
| Git 版本 | 迁移脚本、schema、索引文档 | 每次改动 | 当前仓库 |

### 5.2 反锁定原则

- 每个 Notion 对象必须有 `Source Path` 或 `External URL`，保证能回到原始资料。
- 每个核心数据库必须能导出为 CSV，并通过 `Name`、`Source Path`、`Created`、`Notion ID` 重新建立映射。
- Notion 中不保存密钥、token、完整日志和大体量正文。
- 长期知识以 Markdown 为耐久副本，Notion 负责索引、状态和关系。

### 5.3 建议导出节奏

| 节奏 | 动作 |
|---|---|
| 每日 | 自动化运行摘要写入 Automation Runs；错误产生 Task |
| 每周 | 导出核心数据库 CSV；抽查 3 条 Source Path 是否有效 |
| 每月 | 导出关键 Notion 页面为 Markdown；归档上月 Reports |
| 每季度 | 清理 Archived 项；校验 Notion 与 Markdown/Git 是否可双向追溯 |

---

## 6. 导入执行顺序

1. 先在 Notion 建 Areas、Projects、Tasks、Resources、Content Pipeline、Automations、Automation Runs、Assets、Reports/Insights 九个数据库。
2. 建 Relation：Projects 关联 Areas/Tasks/Resources/Content/Automations；Runs 关联 Automations 和 Tasks。
3. 手工录入批次 A 的 10-20 个对象，验证字段是否够用。
4. 再导入批次 B 的 10 条以内活跃内容，验证 Content Pipeline 状态流转。
5. 最后导入批次 C 的最近报告和审计样本，验证 Report → Task → Run 的闭环。
6. 字段稳定后再写脚本批量导入，不在第一天全量迁移历史 Markdown。

---

## 7. 迁移完成判定

- 任意活跃项目都能在 Notion 看到目标、任务、资料、自动化和最近输出。
- 任意定期任务都有 Automation 定义和最近 Run 记录。
- 任意内容生产项都有状态、发布目标、源路径和质量门禁。
- 任意报告都能追溯到源文件、运行记录和后续任务。
- 从 Notion 导出 CSV/Markdown 后，仍能重建核心关系，不依赖本地目录树作为唯一工作界面。
