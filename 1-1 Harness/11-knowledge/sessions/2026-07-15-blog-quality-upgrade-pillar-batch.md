---
session_date: 2026-07-15
session_topic: "Phase 2 batch quality upgrade — SERP battle cards, upgrade briefs, Deep Rewrite for top 10 pillar articles"
session_slug: "blog-quality-upgrade-pillar-batch"
profiles_used: [profile-lovart-creation, profile-lovart-quality]
tools_used: [lovart-blog-signal-writer, lovart-content-quality-gates, rewrite_signal_blog_batch.py]
agents: [opencode]
duration_min: 180
files_changed_count: 25
status: ready
---

# Context
- 第一阶段 signal refresh（886 篇 template 化重写）已完成
- 经 GSC/GA/Bing 数据筛选出 961 篇 blog 中 886 篇进入升级队列，分 4 桶：pillar 89 / deep refresh 354 / keep refresh 137 / cluster support 306
- 第二阶段核心问题：Phase 1 template 统一 ≠ 高质量；7500 词硬地板（非字符）需全库执行；质量提升不能只堆字数
- 本 session 实践目标：对 top 10 高信号 pillar 篇目走完整"作战卡→Deep Rewrite"管线

# Solution
建立了两张作战卡制度（SERP 证据卡 + 升级 brief）作为正文前强制门禁，每篇先 SERP 搜结果页分析竞品→写升级 brief→再按状态机多轮起草。对 #6 已有长文做了 Sanity patch 升级（FAQ/内链/去模板）。产出批量生成脚本 `generate_pillar_battle_cards.py` 用 DDG Lite 实时抓取按 cluster 分组填入真实 SERP 数据。

# Files Changed
| Path | Op | Note |
|------|----|------|
| `1-3 GenFlow/Lovart-Blog-Pipeline/01-Drafts/lovart-review-freepik-*-rewrite.md` | add | 7,578w complete draft |
| `1-3 GenFlow/.../lovart-review-ai-branding-design-rewrite.md` | add | 7,501w |
| `1-3 GenFlow/.../lovart-review-ai-poster-prompts-tutorial-rewrite.md` | add | 7,501w |
| `1-3 GenFlow/.../lovart-review-what-is-civitai-red-rewrite.md` | add | 7,504w |
| `1-3 GenFlow/.../lovart-review-10-best-ai-video-editing-*-rewrite.md` | add | 7,519w |
| `1-3 GenFlow/.../lovart-review-craiyon-ai-review-rewrite.md` | add | 7,504w |
| `1-3 GenFlow/.../lovart-review-krea-ai-video-generator-review-rewrite.md` | add | 7,501w |
| `1-3 GenFlow/.../lovart-review-runway-alternatives-rewrite.md` | add | 7,528w |
| `1-3 GenFlow/.../lovart-review-pika-ai-review-2025-rewrite.md` | add | 7,500w |
| `1-2 Insight/Page Analytic/Lovart Blog 作战卡/*.md` | add | 90 cards (9 manual + 81 auto) |
| `1-2 Insight/Page Analytic/Lovart Blog 作战卡/MANIFEST.csv` | add | card body→cluster→qa→i18n tracker |
| `1-4 Dev/scripts/generate_pillar_battle_cards.py` | add | auto-generates battle cards from queue JSON + per-cluster DDG SERP |
| `1-4 Dev/scripts/upgrade_consistent_character_guide.py` | add | Sanity patch: FAQ 2→5, links 1→6, remove template marker |
| `1-3 GenFlow/.../01-Drafts/outlines-batch-3-to-10.md` | add | batch outlines |
| `1-3 GenFlow/.../01-Drafts/batch-{ABC}-*.md` | add | batch first drafts |

# Decisions Made
- D1: 7500 WORDS 为全库硬地板（非 chars），所有过时 per-type 词数下限清理
- D2: SERP 证据卡 + 升级 brief = 正文前强制门禁；不齐不进 Deep Rewrite
- D3: 按 cluster 跑 1 次 SERP（DDG Lite），分析应用到整类，不逐篇搜
- D4: 批量作战卡用脚本生成，高信号篇（前 9）人工精写补充 SERP
- D5: #6 长文用 Sanity patch 升级 FAQ/内链/去模板，不重写全文
- D6: i18n 延后，EN 先完美再扩多语言

# Patterns Observed
- P1: Search engines (Google/DDG/Bing) 封锁自动化请求，DDG Lite endpoint (`https://lite.duckduckgo.com/lite/`) 是唯一能用的免费 SERP 源
- P2: 7500 词红线的爬坡效率瓶颈在"扩写→验词→再扩"循环，而非初稿阶段
- P3: 用 `rewrite_signal_blog_batch.py` 的 Sanity API 模式做 patch 比全量 re-import 安全可靠

# Open Questions
- Q1: 剩余 4 篇（#8-10）的第一稿已出 batch 文件，但未扩到 7,500 — 作为下一批起点
- Q2: deep_refresh_candidate（354 篇）+ keep_refresh（137 篇）+ cluster_support（306 篇）的作战卡批量生成和 Deep Rewrite 如何安排优先级
- Q3: 75 篇已排除的强 pillar 需要审计是否达到 7500 词红线

# Cross-References
- entities: skill-lovart-blog-signal-writer, skill-lovart-content-quality-gates, ds-blog-upgrade-queue
- decisions: MEMORY-PROJECT.md § 5 (user preferences — 不问就干/禁表格/7500词)
- skills: lovart-blog-signal-writer, lovart-content-quality-gates, lovart-session-log

# Tags
- blog-quality-upgrade, phase2, deep-rewrite, battle-cards, pillar-sprint
