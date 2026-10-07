---
session_date: 2026-07-21
session_topic: "Obsidian + Lovart Local Dev 双向 sync 机制"
session_slug: "obsidian-localdev-sync"
profiles_used: [profile-lovart-management]
tools_used: [sync-local-dev.sh]
agents: [hermes]
duration_min: 20
files_changed_count: 2
schema_bumps: 0
status: ready
---

# Context
- Obsidian vault 和 Lovart Local Dev 两个目录始终配合不好
- Local Dev 有 350M 内容,其中 327M 在 Output/
- 根目录有 20+ 个 .md 策略文档只在 Local Dev,不在 Obsidian
- features/ 有 55 个 JSON 只在 Local Dev

# Solution
**写 `sync-local-dev.sh` 双向同步脚本**:

Sync 方向:
- Local Dev → Obsidian: 有价值的新文件推过去
- Obsidian → Local Dev: 过时文件拉回来(放到 Backup/)

映射规则:
- 根 .md → insight-data/ (策略/报告)
- features/*.json → genflow/Page Gen/features/
- tools/*.py → dev/tools/
- Output/SEO-Reports → insight-data/SEO Reports/
- Output/Knowledge Base → insight-data/Knowledge Base/
- Output/Lovart-Blog-Pipeline → genflow/Lovart-Blog-Pipeline/
- seo-documents/sitemap-latest → insight-data/SEO Reports/sitemap/

跳过规则:
- .hermes / .openharness / Logs / Temp / Backup / .git / __pycache__
- .env / .token_* / *.pyc / credentials*

**执行结果**:
- dry-run: 79 个文件待同步
- apply: 79 个文件全部同步成功
- 验证: 22 个根 .md + 55 个 features JSON + 2 个 tools Python = 79/79 ✓

# Files Changed
| 路径 | 操作 | 备注 |
|------|------|------|
| `dev/scripts/sync-local-dev.sh` | add | 双向同步脚本 |
| `insight-data/*.md` (22 个) | add | 从 Local Dev 根目录同步 |
| `genflow/Page Gen/features/*.json` (55 个) | add | 从 Local Dev features/ 同步 |
| `dev/tools/*.py` (2 个) | add | 从 Local Dev tools/ 同步 |

# Decisions Made
- D1: Obsidian vault = SSOT for rules/skills/knowledge; Local Dev = SSOT for runtime data
- D2: sync-local-dev.sh 默认 dry-run, 需要 --apply 才执行
- D3: 过时文件不删除, 移到 Local Dev/Backup/{YYYY-MM-DD}/
- D4: SSOT 文件(harness/, AGENTS.md, entities.*)不归档

# Patterns Observed
- P1: Local Dev 根目录有 22 个 .md 策略文档——这些是"生产过程中的决策记录",应该在 Obsidian 里可搜索
- P2: features/ 55 个 JSON 是 zh-TW 修复版——这些是 Sanity import 的输入,应该在 genflow/ 里
- P3: sync 脚本可以接 cron 每周跑一次,保持两个目录同步

# Tags
- relevant-tags: #obsidian-sync #local-dev #bidirectional-sync #file-management #2026-07
