# Obsidian ↔ Notion 双轨同步架构

> **核心原则**:Obsidian 管"机器读的"(规则/脚本/数据/agent 记忆),Notion 管"人看的"(报告/日历/状态/协作)。互为备份,不互替代。

---

## 一、分工原则

```
Obsidian (SSOT)                    Notion (展示层)
─────────────────                  ─────────────────
Rules / Skills / Scripts           Content Calendar (Board/Timeline)
Pipeline State JSON                SEO Reports (Gallery)
Agent Memory (MEMORY-PROJECT)      Sentinel ORM (Board)
Knowledge Graph (entities)         Keywords Research (Table)
Session Logs                       OKR (Timeline)
Sanity Config / Credentials        异常记录 (Table)
草稿 / JSON 输入                   素材规格 (Table)
                                   分发状态 (Board)
```

**谁写,谁 SSOT**:
- Agent 生成的内容 → Obsidian 是 SSOT → 推到 Notion 展示
- 人工在 Notion 改了状态/评论 → 拉回 Obsidian 更新对应字段
- 冲突规则: **Notion 的 Status/Comment 字段以 Notion 为准**; 其他字段以 Obsidian 为准

## 二、同步方向

```
Obsidian → Notion (推):
  - 新增/修改的 .md → 对应 Notion Database 记录
  - pipeline-state.json → Notion Board (可视化)
  - TOOLS-REGISTRY.md → Notion Table

Notion → Obsidian (拉):
  - Status 字段变更 (Published/Archived/In Progress)
  - Comment/Notes 字段更新
  - 人工新增的记录 (需确认后写入 Obsidian)
  - 优先级调整 (Priority/Score)
```

## 三、4 个 P0 Database Schema

### 1. Content Calendar (已有,需增强)

Notion Database ID: `37afc0c7-1bd5-8124-a031-ca4eca128da2`

已有 20 个字段。需要新增:
- **Last Synced** (Date) — 上次同步时间
- **Sync Source** (Select) — obsidian / notion / manual
- **Conflict Flag** (Checkbox) — 双向冲突标记

### 2. SEO Reports (新建)

```
Database Name: Lovart SEO Reports
Fields:
  - Report Name (Title) — "2026-07 月报" / "W28 周报"
  - Report Type (Select) — monthly / weekly / daily / special
  - Period (Date Range) — 报告覆盖时间段
  - Status (Select) — draft / reviewing / published / archived
  - Key Metrics (Rich Text) — 核心指标摘要
  - File Path (Rich Text) — Obsidian 内的 .md 路径
  - Notion Link (URL) — 报告的 Notion 页面链接
  - Last Synced (Date)
  - Sync Source (Select)
```

### 3. Sentinel ORM (新建)

```
Database Name: Lovart Sentinel Daily
Fields:
  - Date (Date) — 舆情日期
  - Brand (Select) — lovart / competitor
  - Sentiment (Select) — positive / neutral / negative / mixed
  - Alert Level (Select) — info / warning / critical
  - Summary (Rich Text) — 一句话摘要
  - Source Count (Number) — 信息源数量
  - File Path (Rich Text) — Obsidian 内的 .md 路径
  - Action Required (Checkbox)
  - Last Synced (Date)
```

### 4. OKR (新建)

```
Database Name: Lovart OKR
Fields:
  - Objective (Title) — 目标描述
  - Quarter (Select) — Q1/Q2/Q3/Q4 2026
  - Status (Select) — on-track / at-risk / behind / done
  - Progress (Number 0-100) — 完成百分比
  - Key Results (Rich Text) — 关键结果列表
  - File Path (Rich Text) — Obsidian 内的 .md 路径
  - Last Synced (Date)
```

## 四、同步机制

### 方向 1: Obsidian → Notion (推)

```
触发: 每周日 03:00 (launchd) / 手动 / 发布后
脚本: 1-4 Dev/scripts/sync-to-notion.py
逻辑:
  1. 扫描 Obsidian 中变更的文件 (git diff 或 mtime)
  2. 对比 Notion 中已有记录 (by File Path)
  3. 新增 → Notion API create
  4. 已有且 Obsidian 更新 → Notion API update (只改非 Status 字段)
  5. 记录同步日志到 sync-pushed.jsonl
```

### 方向 2: Notion → Obsidian (拉)

```
触发: 每周一 09:00 (launchd) / 手动
脚本: 1-4 Dev/scripts/sync-from-notion.py
逻辑:
  1. 查询 Notion Database 中 Status/Comment/Priority 有变更的记录
  2. 对比 Obsidian 中对应文件的 frontmatter
  3. 差异 → patch Obsidian .md 的 frontmatter
  4. 人工新增的 Notion 记录 → 生成 .md 草稿到 Obsidian
  5. 记录同步日志到 sync-pulled.jsonl
```

### 冲突检测

```
每个记录有 Last Synced + Sync Source:
  - 如果 Notion 的 Sync Source = "notion" 且 Obsidian 也改了 → 标记 Conflict Flag
  - Conflict Flag = true 的记录不自动同步,等人手动解决
  - 解决方式: 在 Notion 里看差异,决定保留哪个版本
```

## 五、文件结构

```
1-4 Dev/scripts/
├── sync-to-notion.py          # Obsidian → Notion 推
├── sync-from-notion.py        # Notion → Obsidian 拉
├── sync-conflict-resolve.py   # 冲突检测+解决
├── sync-local-dev.sh          # (已有) Local Dev ↔ Obsidian
└── sync-manifest.json         # 同步配置(Database ID 映射)

1-4 Dev/notion-sync/           # (已有) 历史脚本,保留参考
```

## 六、验证清单

- [ ] 4 个 P0 Database 在 Notion 中创建完成
- [ ] 每个 Database 分享给 Notion 集成
- [ ] sync-to-notion.py 能读取 Obsidian 文件并推送到 Notion
- [ ] sync-from-notion.py 能读取 Notion Status 变更并拉回 Obsidian
- [ ] 冲突检测能正确标记双向修改
- [ ] launchd 每周日 03:00 推 + 每周一 09:00 拉
