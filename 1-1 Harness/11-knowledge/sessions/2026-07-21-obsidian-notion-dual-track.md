---
session_date: 2026-07-21
session_topic: "Obsidian ↔ Notion 双轨同步架构 + P0 迁移分析"
session_slug: "obsidian-notion-dual-track"
profiles_used: [profile-lovart-management]
tools_used: [sync-to-notion.py, sync-from-notion.py]
agents: [hermes]
duration_min: 40
files_changed_count: 4
schema_bumps: 0
status: ready
---

# Context
- 用户不想用 Notion 替代 Obsidian,而是双轨互为备份
- Obsidian 管"机器读的"(规则/脚本/数据/agent 记忆)
- Notion 管"人看的"(报告/日历/状态/协作)
- 已有 4 个 Notion Database (Content Calendar / Daily Keyword Tracker / Skill Index / Home)

# Solution
**双轨架构设计 + 2 个同步脚本**:

**架构原则**:
- Obsidian = SSOT for agent data (rules, scripts, code)
- Notion = 展示层 for human collaboration (reports, calendars, status)
- 冲突规则: Notion 的 Status/Comment 以 Notion 为准; 其他以 Obsidian 为准

**4 个 P0 Database**:
1. Content Calendar (已有,需增强 Last Synced/Sync Source/Conflict Flag)
2. SEO Reports (新建)
3. Sentinel ORM (新建)
4. OKR (新建)

**同步方向**:
- Obsidian → Notion (推): 新增/修改的 .md → Notion Database 记录
- Notion → Obsidian (拉): Status/Comment/Priority 变更 → patch frontmatter
- 冲突检测: Last Synced + Sync Source 双向标记

**执行结果**:
- sync-to-notion.py dry-run: 3280 本地文件 vs 479 Notion 页面, 3280 待创建
- sync-from-notion.py dry-run: 479 Notion 页面, 0 待拉回 (无 Status 变更)

# Files Changed
| 路径 | 操作 | 备注 |
|------|------|------|
| `1-1 Harness/10-config/obsidian-notion-dual-track.md` | add | 双轨架构设计文档 |
| `1-4 Dev/scripts/sync-to-notion.py` | add | Obsidian → Notion 推 |
| `1-4 Dev/scripts/sync-from-notion.py` | add | Notion → Obsidian 拉 |

# Decisions Made
- D1: Notion 不替代 Obsidian,而是双轨互为备份
- D2: Notion 的 Status/Comment 字段以 Notion 为准; 其他字段以 Obsidian 为准
- D3: 冲突检测用 Last Synced + Sync Source 双向标记
- D4: 4 个 P0 Database: Content Calendar / SEO Reports / Sentinel ORM / OKR

# Patterns Observed
- P1: Content Calendar 已有 479 个 Notion 页面 + 3280 个本地文件——差距很大,说明之前同步不完整
- P2: 已有 notion-sync/ 目录有 40+ 个脚本——历史尝试很多,但没有统一的双向机制
- P3: Notion API rate limit 3 req/s — 3280 个文件需要 ~18 分钟同步

# Tags
- relevant-tags: #notion-sync #dual-track #obsidian #bidirectional #2026-07
