---
session_date: 2026-08-05
session_topic: "KO Blog 前排正文语言错配：分层止血 + 14篇重写/专栏深修"
session_slug: "ko-blog-body-language-tier-and-rewrite"
profiles_used: [profile-lovart-quality, profile-lovart-creation]
tools_used: [lovart-core, lovart-blog-signal-writer, lovart-quality-gates, sanity-query, md_to_portable_text]
agents: [cursor]
duration_min: 180
files_changed_count: 25
kb_units_added: 0
schema_bumps: 0
related_sessions: []
related_prs: []
status: draft
cross_refs:
  entities: []
  decisions: ["1-2 Insight/AGENTS.md RULE 11 releaseDate 分层"]
  skills: [lovart-blog-signal-writer, lovart-quality-gates, lovart-session-log]
  related_sessions: []
---

# Context

- 用户要查线上 Blog 前 100 各语言版正文是否与 language 字段一致。
- 发现 KO 等前排大量 EN 壳后，批准分层止血 + 按 signal-writer 重写，并分批专栏深修至原 14 篇收工。

# Solution

- 各语言 top100 语言错配审计；KO/PT/RU/DE/FR/IT 等用 releaseDate 三层分层（C 沉底，A 保留时间序）。
- KO 前排 14 篇韩语重写 → PT patch；再按前排流量分批专栏深修（去注水头、重写核心）。
- 终态：原 14 篇 hangul≥0.55；KO top100 正文错配 **0**。

# Files Changed

| 路径 | 操作 | 备注 |
|------|------|------|
| `1-2 Insight/QA/2026-08-03-blog-top100-body-language-mismatch.md` | add/modify | 审计结论 + 止血/重写/深修进度 |
| `Local Dev/.../blog_language_quality_tier_sort.py` | add | 语言质量分层脚本 |
| `Local Dev/.../polish_ko_top14_blogs.py` | add | 首轮精修 |
| `Local Dev/.../deep_polish_ko_top3.py` | add | 前三深修入口 |
| `Local Dev/.../01-Drafts/ko-{wave,polished,deep}/` | add | KO 草稿 |
| `Local Dev/.../QA-Memo/ko-rewrite-2026-08-03/` | add | 审计/patch/复扫 JSON |
| Sanity production `blog` ×14 KO | patch | body + seo + releaseDate |

# Decisions Made

- D1：排序只改 `releaseDate`（RULE 11），Tier A 不整库压成同一天。
- D2：KO 正文走 signal-writer 约束（≥7500어절、非机翻），落库用 PT patch 非整库 replace。
- D3：深修按列表前排分批（3 篇一组）推进至原 14 齐套。

# Patterns Observed

- P1：非 EN 前排脏数据主形态是「title 本地化 + body EN 壳」，分层止血 ROI 高于立刻全量重写。
- P2：凑字数时「编号노트/城市克隆」会立刻破坏专栏感；深修应先重写核心再扩写。
- P3：合格母语正文不足 100 时，分层后 top100 仍可能吸入 Tier C（KO 曾 14→0 靠重写补齐）。

# Open Questions

- Q1：深修后半段「运营 심화」扩写块是否还要再压成纯人工专栏（按 GSC 流量挑 Top）。
- Q2：KO 以外拉丁语系 EN body 是否启动同款重写（当前多为分层止血）。
- Q3：liblib 封面池 URL 是否统一换成 blogcover 池（本轮未动封面）。
