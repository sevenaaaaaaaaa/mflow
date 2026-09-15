---
session_date: 2026-08-23
session_topic: "盘点并整理 Daily、Cluster 与 Tags 网站上传稿"
session_slug: "website-drafts-inventory-and-reorganization"
profiles_used: [profile-lovart-distribution]
tools_used: [lovart-core, lovart-distribution, lovart-session-log, organize_website_ready.py]
agents: [codex]
duration_min: 45
files_changed_count: 675
kb_units_added: 0
schema_bumps: 0
related_sessions: []
related_prs: []
status: ready
---

# Context

- 用户要把本地 Drafts 文稿迁移到网站，先识别可上传正文，再按来源和主题重新归类。
- Daily 与 Cluster 的序号目录含母版和平台变体；Tags 是旧站存量稿，存在来源站品牌、导航、链接和图片热链。

# Solution

- 新增非破坏性整理脚本，在 `Drafts/Website-Ready/` 生成独立上传准备目录，不修改原始稿。
- Daily、Cluster 每个序号目录优先选择一个平台中性 T1/T2/T3 母版；Tags 清除可识别的旧站痕迹，并把残留风险稿隔离到人工复核区。
- 生成逐篇 manifest，按规范化正文哈希跨来源去重，并保留原分类和文章附件。

# Files Changed

| 路径 | 操作 | 备注 |
|------|------|------|
| `1-3 GenFlow/Content Distribution/Drafts/organize_website_ready.py` | add | 可重复执行的筛选、清洗、分类和去重脚本 |
| `1-3 GenFlow/Content Distribution/Drafts/Website-Ready/` | add | 674 个生成文件，含 530 篇 ready、58 篇 review、manifest 和报告 |
| `1-1 Harness/11-knowledge/sessions/2026-08-23-website-drafts-inventory-and-reorganization.md` | add | 本轮会话记录 |

# Decisions Made

- D1: 原始 Daily、Cluster、Tags 全部只读，网站稿通过独立 staging 目录生成。
- D2: 文件名不含知乎/百家号只是初筛；管理文档、选品稿和其他平台专版不作为网站母版。
- D3: Daily 与 Cluster 的标准 T1/T2/T3 平台中性母版优先；多母版目录使用可追溯 heuristic 并在 manifest 标记。
- D4: Tags 只有在旧发布站痕迹清除且正文不短于 500 字符时进入 ready，否则进入人工复核。
- D5: `ready` 只代表本轮结构与旧站痕迹筛查通过，不替代 CMS schema、事实、版权、链接和图片终检。

# Patterns Observed

- P1: “无知乎/百家号后缀”不足以唯一识别母版；同目录可能同时有旧站原文、T2 新稿和其他平台版本。
- P2: Daily、Cluster、Tags 之间存在大量正文重复，网站迁移必须在分类之后再做跨来源去重。
- P3: Tags 的旧站痕迹不只在文件名，也会出现在 frontmatter、正文导航、来源链接和远程图片中。

# Open Questions

- Q1: 58 篇人工复核稿是否重写、补充正文，还是排除出首批迁移。
- Q2: Cluster 的 8 个多母版目录是否需要人工指定最终网站母版。
- Q3: 网站 CMS 的 title、slug、summary、日期、封面和分类字段映射尚未执行。

# Cross-References

- entities: []
- decisions: [MEMORY-PROJECT.md § 5]
- skills: [lovart-core, lovart-distribution, lovart-session-log]

# Tags

- relevant-tags: #content-migration #website-upload #draft-inventory #distribution #deduplication
