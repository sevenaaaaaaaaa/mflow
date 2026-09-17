---
name: lovart-blog-signal-writer
description: >-
  舆情(ORM/Sentinel)+GSC 信号驱动的 blogs.lovart.ai 博客自动撰写。从舆情报告与
  GSC 数据中挖掘选题/角度 → 按 blogs 子站内容生产规范撰写英文长文（全分类 ≥7,500 词，
  multi-turn，禁脚本灌字）→ 过质量门禁 → status: ready，停在发布前等人工授权。
  Use for "根据舆情和GSC写博客"、"signal-driven blog"、"挖选题写博客"、
  "舆情+GSC 内容生产"、"写一篇 blogs.lovart.ai 博客".
budget_profile: longform  # 长文豁免（RULES-70 §五）
---
## 预算（RULES-70 强制）

- 字数：Blog 1200–1800（**绝不超 2160**）；落地页文案 600–1000；摘要/分发稿 ≤600
- H2 4–7 · FAQ 3–5 · 每千字 1–3 数据点（同数据不重复）· 外部来源 2–5 条（完整 URL）
- 列表块 ≤4 处且不连续；单段 ≤300 字符；**禁止**同义反复 / 复述式总结 / 模板过渡词堆砌 / 形容词堆叠
- 字数不足时**优先删冗余**，绝不补形容词
- 长文（7500 词级）如需豁免：本 skill frontmatter 声明 `budget_profile: longform`，调用时显式传参（见 RULES-70 §五）
- 交付前必须过：`post-write-check.sh` · `geo-check.sh` · `quota-check.sh` · `lang-check.sh`

## 路径契约

| 层 | 路径 |
|----|------|
| 文档 SSOT | `1-1 GEO Readme/` |
| Sanity 脚本 | `1-4 Dev/lovart.sanity.studio/scripts/` |
| SEO/Sentinel 脚本 | `1-4 Dev/scripts/` |
| 自动化 | `1-4 Dev/automation/` |
| 本 Skill | `1-1 Harness/Skills/lovart-blog-signal-writer/SKILL.md` |

# Lovart Blog Signal Writer

信号 → 选题 → 按规范撰写 → 质检 ready。发布终端 **blogs.lovart.ai（WordPress）**。
自动化止步于 `status: ready` + 质量门禁，**发布前必须人工授权**（见 Phase 4）。

## Triggers

- 「根据舆情和 GSC 写博客」「挖一批选题写博客」
- 「写一篇 blogs.lovart.ai 博客」「signal-driven blog」
- 拿到新的 Sentinel 舆情报告 / GSC 数据后，想转成内容

## 三类输入（SSOT 路径）

| 输入 | 路径 | 取什么信号 |
|------|------|-----------|
| **舆情** | `1-2 Insight/Lovart ORM/{daily,weekly,monthly}/Lovart-Sentinel-*.md` | §二 搜索舆情（品牌/非品牌 Top10、地域）、§四 品牌形象（正/负议题）、§六 风险与机遇、§八 行动清单 |
| **GSC** | `1-2 Insight/Trident Insights/reports/gsc-full.json`（28d/100 词）；回退 `Lovart ORM/raw/<date>/gsc_*.json` | 高曝光低点击词、排名 8–20 的可提升词、新出现的非品牌词、竞品对比词 |
| **生产规范** | `1-Project/1-3 Content Gen/Lovart-Blog-Pipeline/Lovart-Blogs/` | `cursor-lovart-blog-system-prompt.md`（人设/术语/结构模板/已验证内链）+ `LOVART-BLOG-LOCAL-SPEC.md`（frontmatter）+ `BATCH-WORKFLOW.md`（验收） |
| **封面池** | `2-Area/Content Archive/Cover Url 随机调取.md`（56 URL） | `python3 scripts/pick-cover.py {slug}` |

GSC 数据过期时先刷新：`cd "1-1 Harness/Skills/lovart-trident-data-engine" && bash scripts/run_all.sh`（见该 Skill）。

---

## Workflow（串行，不达标不进下一阶段）

### Phase 0 — 信号摄取 → 选题候选

读取**最近一期** Sentinel 日/周/月报 + `gsc-full.json`，按下表把信号转成候选选题，写到
`01-Drafts/_signal-queue-{YYYY-MM-DD}.md`（一张表：候选标题 / 角度 / 信号来源 / focus_keyword / 写作类型）。

| 信号 | 写作类型（→ 见 §结构模板） | 角度 |
|------|---------------------------|------|
| GSC 非品牌词「X vs Y / X alternative」有曝光 | Comparison | 竞品对比 kill-shot：我们做 X，对手做不到因为 Y |
| GSC 高曝光低点击（impression↑ click≈0） | How-To / Best Practice | 补一篇真正解答该 query 的实操文，优化标题吸点 |
| GSC 排名 8–20 + 月曝光 >100 | Content Refresh（旧文翻新） | 翻新已发文章而非新写（见 §与现有 Skill 衔接） |
| 舆情 §二 非品牌词有竞品在「蹭」Lovart | Comparison / Insight | 正面迎击该竞品话题 |
| 舆情 §四 负面议题（如 hallucination、版权、模板感） | Insight & Trend / Better Design | 用第一性原理回应顾虑，建立 thought leadership |
| 舆情 §六 机遇 / §八 P0-P1 行动 | Segment / How-To | 把舆情建议直接落成对应行业/场景内容 |
| 舆情 地域分布显示某市场在搜 | Segment | 针对该市场的行业场景文 |

### Phase 1 — 选题定稿

1. **去重**（两层）：
   - 子站线上：`curl -s "https://blogs.lovart.ai/wp-json/wp/v2/posts?slug={slug}&per_page=1" | python3 -c "import sys,json; d=json.load(sys.stdin); print('EXISTS' if d else 'available')"`
   - 本地：检索 `1-3 Content Gen/Lovart-Blog-Pipeline/Lovart-Blogs/03-Published/` 是否已有同集群文章
2. **优先级**：ICE 或 P0/P1/P2（Impact=搜索量×商业价值 / Confidence=能否排名 / Ease=写作成本）。
3. **category 映射**：写作类型 ≠ Sanity category。按 `LOVART-BLOG-LOCAL-SPEC.md` §1.1 填合法 12 类（Comparison→`How-To`，Segment→`Industry Solution`，Better Design→`Branding` 等）。

### Phase 2 — 撰写

输出到 `1-3 Content Gen/Lovart-Blog-Pipeline/Lovart-Blogs/01-Drafts/{category-prefix}-{slug}.md`，严格遵循
`cursor-lovart-blog-system-prompt.md` 与 `LOVART-BLOG-LOCAL-SPEC.md`：

- **Frontmatter**：必填字段齐全（title/slug/date/language/category/author/description/keywords/tags/cover_url/alt_text/seo_title/seo_description/status/content_cluster）。模板见 `templates/frontmatter.example.yaml`。
- **封面**：`python3 scripts/pick-cover.py {slug}` 取 `cover_url`，**勿编造**；`alt_text = {focus_keyword} — Lovart AI Design Agent blog cover`。
- **正文结构**：H1 仅标题；三段式（第一性原理→策略→Lovart 工具实操）；每大节 ≥2 子节。
- **字数下限（用户铁律 2026-07-17，全分类统一）**：**任何写作类型 / Sanity category 的 Blog，进 `status: ready` 前英文正文必须 ≥ 7,500 词**（`len(text.split())`，不计 frontmatter）。旧表（How-To 1800 / Comparison 3600 / Insight 2800 等）**已废止**，不得再当出门标准。
- **长文写法**：禁止单次灌出全文。必须走 `RULES-20-creation.md` Multi-Turn + Column-Writer Lane（OUTLINE → DRAFT_PART* → INTEGRATE_QA）；单次输出硬顶约 3,000 词。禁止 script padding / 模板句灌字凑 7500（见 RULES-20 Banned Template-Phrase Registry）。
- **Lane 只定effort，不降地板**：Deep / Medium / Light 决定 multi-turn 轮次与 cascade，**不**允许 ready 稿低于 7,500 词。
- **必含块**：Derivative Scenarios、FAQ（按 PAA 提问）、E-E-A-T 表、Internal Links 表、Image Appendix 表、footer cluster 行。
- **术语**：严格用 system prompt「LOVART TERMINOLOGY REFERENCE」拼写（Lovart、MCoT、ChatCanvas、Nano Banana Pro、Identity Lock…）。
- **内链**：只用 system prompt「VERIFIED INTERNAL LINKS」里的 slug + `https://lovart.ai/signup` + `https://lovart.ai/pricing`，**禁止编造 `/blog/` slug**。生产已存在但列表未更新的 slug，以 production 存活校验为准，仍禁止虚构。
- **footer**：`*Article for blogs.lovart.ai. Part of [Content Cluster Name] content cluster.*`
- 英文、US spelling；正文不用 emoji；不写 `Note:`/`TODO` 标记。

### Phase 3 — 质量门禁 → ready（STOP）

对照 `BATCH-WORKFLOW.md` + `LOVART-BLOG-LOCAL-SPEC.md` §6 + `RULES-20-creation.md` 逐项核：

- [ ] `category` 为 Sanity 合法 12 类之一
- [ ] `cover_url` 来自 `pick-cover.py`，未与其他稿撞车
- [ ] `seo_title` ≤60 / `seo_description` 150–160 / `description` ≤300 字符
- [ ] `keywords` 含 `focus_keyword`
- [ ] 六大必含块齐全
- [ ] **词数 ≥ 7,500**（正文 words；`< 7500` → 不得 `ready`）
- [ ] 无 Banned Template-Phrase / Anti-Slop 禁用词；非脚本灌字
- [ ] 内链全部来自 verified 列表或 production 存活 slug，无编造
- [ ] 子站/本地去重已通过
- [ ] 建议：`post-write-check.sh --file … --target-words 7500` PASS

全部通过 → 把 frontmatter `status` 改为 `ready`，把候选行在 `_signal-queue` 标 `ready`。
**到此停下**，向用户报告：本批 ready 篇目清单 + 选题对应的舆情/GSC 信号来源，等待发布授权。

### Phase 4 — 发布（仅在用户明确授权后）

发布到 blogs.lovart.ai 沿用 [`lovart-blog-automation`](../lovart-blog-automation/SKILL.md) 与 `1-3 Content Gen/Lovart-Blog-Pipeline/Lovart-Blogs/scripts/publish-to-wp.py`（凭据：`scripts/wp-auth.local.env`，已 gitignore）。

---

## 与现有 Skill 的衔接

| 需求 | 用哪个 |
|------|--------|
| 刷新 GSC/GA4/Bing 数据 | `lovart-trident-data-engine`（`scripts/run_all.sh`） |
| 翻新旧文而非新写 | Content Refresh 路径（`README.md` 方式 C，按 GSC 8–20 位筛选） |
| 发到主站 www.lovart.ai/blog（Sanity） | `lovart-sanity-publish`（本 Skill 不走 Sanity，目标是子站 WordPress） |
| 发布前深度审计长文 | `lovart-content-audit` |

## 关键路径

```
1-Project/
├── 1-2 Insight/Lovart ORM/{daily,weekly,monthly}/   ← 舆情输入
├── 1-2 Insight/Trident Insights/reports/gsc-full.json ← GSC 输入
└── 1-3 Content Gen/Lovart-Blog-Pipeline/Lovart-Blogs/
    ├── cursor-lovart-blog-system-prompt.md   ← 人设/术语/结构/已验证内链
    ├── LOVART-BLOG-LOCAL-SPEC.md             ← frontmatter 规范
    ├── BATCH-WORKFLOW.md                      ← 验收门禁
    ├── templates/frontmatter.example.yaml
    ├── scripts/pick-cover.py                  ← 封面分配
    ├── 01-Drafts/                             ← 草稿 + _signal-queue
    └── 03-Published/                          ← 去重比对
```

## Pitfall #62 — 表格五层 `_key` 误读 vs Lovart schema

**症状**：Blog 上传后表格丢格式 / Studio 校验失败。

**根因（2026-08-03 纠正）**：把通用 Sanity `@sanity/table` 文档里的 `tableCell` 五层树当成了 Lovart 规范。  
`o11tm2qe` 已部署 schema 实际是 `tableRow.cells: string[]`，**没有** `tableCell` 类型。生产可渲染样本（pillar ja 等）全部是 string cells。

**正确做法**：

1. 一律 `from md_to_portable_text import md_to_portable_text`
2. 表格形态：`table(_key) → tableRow(_key) → cells: ["文本", ...]`
3. import 前 `validate_pt_body.py` 必须 `BLOCK=0`

详见：`references/portable-text-table-syntax.md`
