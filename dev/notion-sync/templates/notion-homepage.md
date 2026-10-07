# LifeOS/PARA Command Center

> Notion 主控页模板。创建后把下列数据库作为 linked database 或原始 database 放在本页下。

---

## 今日入口

- Today Tasks：筛选 `Tasks.Status` 为 `Next`、`Doing`、`Blocked`
- Active Projects：筛选 `Projects.Status` 为 `Active`
- Running Automations：筛选 `Automations.Status` 为 `Active`
- Needs Confirmation：筛选所有数据库中 `Sync Status` 或补录状态为 `needs-confirmation`

---

## 核心数据库

1. Areas
2. Projects
3. Tasks
4. Resources
5. Content Pipeline
6. Automations
7. Automation Runs
8. Assets
9. Reports/Insights

---

## 推荐视图

### Projects

- Active by Area
- P0/P1 Roadmap
- Waiting or Blocked
- Archived

### Tasks

- Today / Next
- By Project
- Blocked
- Review Queue

### Content Pipeline

- Kanban by Status
- P0/P1 Content
- Needs Refresh
- Published This Month

### Automations

- Active Automations
- Needs Setup
- High Risk
- By Runtime

### Automation Runs

- Latest Runs
- Failed Runs
- Runs With Follow-up Tasks

### Reports/Insights

- Latest Reports
- SEO Reports
- Sentinel Reports
- Quality Audits

---

## 同步操作区

- Backfill Queue：从本地 `notion-sync/backfill-queue.csv` 导入或同步
- Export Log：记录每次 Notion → Local 导出
- Conflict Review：所有 `conflict` 项集中处理

---

## 维护规则

- Notion 不保存密钥、token、完整日志和大体量正文。
- 本地 `Source Path` 是回到 Markdown/Git 的主入口。
- 每周导出核心数据库 CSV；每月导出关键页面 Markdown。
- 同一个字段两边都修改时，不自动覆盖，先标记 `conflict`。
