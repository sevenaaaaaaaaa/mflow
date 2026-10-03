---
name: blog-writer
description: >-
  品牌 Blog 创作唯一入口（2026-10-03 整合：content-writer 方法论 + blog-signal-writer 信号链 +
  8 类型子技能结构 + blog-automation 发布遗产，四合一）。
  信号驱动选题 → 方法论写作 → 质量门禁 → status: ready 止步待人工授权。
  Use for 「写博客」「根据舆情和GSC写博客」「挖选题」「signal-driven blog」、翻新旧文、
  长文（≥7500 词）、博客类型结构、E-E-A-T、多语言博客、博客 QA。
---

## 预算（双轨，勿混）

| 轨道 | 口径 | 适用 |
|---|---|---|
| RULES-70 默认 | 1200–1800 词（绝不超 2160） | 短格式、摘要、分发稿、非 ready 中间稿 |
| **长文生产铁律（生产铁律，全分类统一）** | **进 `status: ready` 前英文正文 ≥7,500 词**（`len(text.split())`，不计 frontmatter） | 一切要发布的博客；旧分类型字数表已废止 |

- 通用硬数：H2 4–7 · FAQ 3–5 · 每千字 1–3 数据点（同数据不重复）· 外部来源 2–5 条完整 URL · 列表块 ≤4 不连续 · 单段 ≤300 字符
- **长文写法**：禁止单次灌出全文，走 RULES-20 Multi-Turn / Column-Writer Lane（`OUTLINE → DRAFT_PART* → INTEGRATE_QA`），单次输出硬顶约 3,000 词；Lane（Deep/Medium/Light）只定 effort 不降 7,500 地板；禁 script padding / 模板句灌字（RULES-20 Banned Template-Phrase Registry）
- 字数不足时**优先删冗余**，绝不补形容词
- 交付前必须过：`post-write-check.sh` · `geo-check.sh` · `quota-check.sh` · `lang-check.sh`（长文 `post-write-check.sh --target-words 7500`）

## 定位与边界

本 skill 是 **Lovart 博客创作唯一入口**。2026-10-03 起以下技能已并入本 skill，不再独立存在：
`lovart-content-writer.md`（→ references/methodology-content-writer.md）、`lovart-blog-signal-writer`（→ references/signals-and-phases.md）、8 个类型子技能（→ references/types/）、`lovart-blog-automation`（→ references/wp-publishing.md 及 references/ 规范文件）、`blog-serp-writer`（弃用，存 `02-creation/_archived-blog-skills/`）。

- 页面类请求（Tools/Features/Landing/Topic…）→ `landing-page` / `page-serp-writer`，不在本 skill
- 发布前深度审计 → `03-review/content-audit`
- 主站 Sanity 发布 → `sanity-publish`；本 skill 默认终端是子站 WordPress（见 Step 6）

## 链路（六步，串行，不达标不进下一步）

### Step 0 · 路由与类型宣布
会话开头 `router decide`（pipeline-state 意识）。写作前宣布（来自 methodology Step 0）：
```
> Content type: [12 类型矩阵]  > Blog category: [Sanity 12 类]
> Funnel: [TOFU|MOFU|BOFU|Post-Purchase]  > Framework: [11 框架库]
> Languages: [Tier 1 | +2 | +3]  > Lane: [Deep|Medium|Light]（长文）
```

### Step 1 · 信号 → 选题候选
读 `references/signals-and-phases.md` §Phase 0：舆情表（`1-2 Insight/ORM/{daily,weekly,monthly}/品牌-Sentinel-*.md`）+ GSC 表（`gsc-full.json`）→ 信号→类型映射 → 写 `01-Drafts/_signal-queue-{date}.md`。
GSC 过期先刷：`trident-data-engine`（`scripts/run_all.sh`）。

### Step 2 · 选题定稿
两层去重（子站 WP API slug 查重 + `03-Published/` 本地查重）→ ICE 优先级（Impact=搜索量×商业价值 / Confidence=可排名性 / Ease=写作成本）→ category 映射（写作类型 ≠ Sanity category，按 LOVART-BLOG-LOCAL-SPEC §1.1）。

### Step 3 · 方法论写作
**全文必读 `references/methodology-content-writer.md`**，强制继承：
- 12 类型矩阵 + 11 叙事框架库 + 类型↔框架配对
- **Anti-AI Writing Rules v4（全部强制）**：开头禁统计句；禁 "Part 1/2/3" 标签；禁 "There are three reasons…" 列表旗标；禁三明治段落节奏；禁 PAS 模板块；[Comparison] 禁三列表格为主结构；数据必有上下文、禁假精确、未验证标 `[待考证]`
- Angle Engine：微观人群切片 → 摩擦点 → 反共识角度 → 5 标题法（1 观点/1 人物/1 数字/1 SEO/对比带 verdict）
- 执行流 Step 0–5（Routing → Angle → Hook 开场 → 核心实证 → 收口）

### Step 4 · 类型结构
所选类型的专属结构/骨架查 `references/types/{type}/GUIDE.md`（101 / best-practice / better-design / complete-guide / insight-trend / review / stack-by-stack / thought-leadership）。

### Step 5 · 输出规范（生产硬要求）
- **Frontmatter 15 字段齐全**（title/slug/date/language/category/author/description/keywords/tags/cover_url/alt_text/seo_title/seo_description/status/content_cluster），模板 `1-3 Content Gen/blog-pipeline/品牌方-Blogs/templates/frontmatter.example.yaml`
- **封面**：`python3 …/scripts/pick-cover.py {slug}`，勿编造；alt_text = `{focus_keyword} — 品牌 AI Design Agent blog cover`
- **三段式正文**：第一性原理 → 策略 → 品牌工具实操；每大节 ≥2 子节
- **六大必含块**：Derivative Scenarios / FAQ（按 PAA）/ E-E-A-T 表 / Internal Links 表 / Image Appendix 表 / footer cluster 行
- **术语**：只用 system prompt「BRAND TERMINOLOGY REFERENCE」拼写（以 system prompt 术语表为准（Lovart 生产环境=MCoT/ChatCanvas/Nano Banana Pro；Moodio=KB Moodio/01 能力词））
- **内链**：只用 system prompt「VERIFIED INTERNAL LINKS」slug + `example.com/signup` + `example.com/pricing`，禁止编造 `/blog/` slug
- **表格**：Portable Text 用 Lovart schema（`tableRow.cells: string[]`，非五层 tableCell）——见 `references/portable-text-table-syntax.md`，import 前 `validate_pt_body.py` BLOCK=0
- 英文 US spelling；正文无 emoji；无 `Note:`/`TODO` 标记；Markdown 兼容规则见 methodology

### Step 6 · 门禁 → ready（STOP）
对照 `BATCH-WORKFLOW.md` + `MFLOW-BLOG-LOCAL-SPEC.md` §6 + RULES-20 逐项核：
- [ ] category 合法 12 类 · cover 未撞车 · seo_title ≤60 / description 150–160 · keywords 含 focus_keyword
- [ ] 六大必含块齐全 · **词数 ≥7,500** · 无 Banned Phrase/Anti-Slop、非灌字 · 内链零编造 · 去重通过 · 四钩子 PASS
全部通过 → frontmatter `status: ready`，`_signal-queue` 标 ready，**到此停下**，报告 ready 篇目 + 信号来源，**等待发布授权**。

### Phase 4 · 发布（仅人工授权后）
子站 WordPress：`references/wp-publishing.md`（`publish-to-wp.py`，凭据 `scripts/wp-auth.local.env` gitignore；状态 blocked-until-dry-run-verified）。主站 Sanity 走 `sanity-publish`。

## 关键路径

```
1-Project/
├── 1-2 Insight/Lovart ORM/{daily,weekly,monthly}/    ← 舆情输入
├── 1-2 Insight/Trident Insights/reports/gsc-full.json ← GSC 输入
└── 1-3 Content Gen/blog-pipeline/品牌方-Blogs/
    ├── cursor-mflow-blog-system-prompt.md  ← 人设/术语/结构/已验证内链
    ├── MFLOW-BLOG-LOCAL-SPEC.md            ← frontmatter 规范
    ├── BATCH-WORKFLOW.md                    ← 验收门禁
    ├── templates/frontmatter.example.yaml
    ├── scripts/pick-cover.py · publish-to-wp.py
    ├── 01-Drafts/（草稿 + _signal-queue） · 03-Published/（去重）
```

## Subskill Governance（对本 skill 内部类型节的约束）

- 类型 GUIDE 的结构规则是**骨架参考**，与本 SKILL 冲突时以本 SKILL + RULES-20 为准
- 不得绕过：category 标注 / publish-date 一致性 / cover 策略 / 内链路由 / FAQ 与版式完整性 / anti-slop 与 publish-ready 检查
- 结构要求稳定：无破损层级、无重复核心节或重复 FAQ 块
