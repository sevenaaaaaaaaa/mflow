---
name: lovart-blog-automation
description: End-to-end Lovart Blog (blogs.lovart.ai) content production: market research → writing → publishing.
---

## 预算（RULES-70 强制）

- 字数：Blog 1200–1800（**绝不超 2160**）；落地页文案 600–1000；摘要/分发稿 ≤600
- H2 4–7 · FAQ 3–5 · 每千字 1–3 数据点（同数据不重复）· 外部来源 2–5 条（完整 URL）
- 列表块 ≤4 处且不连续；单段 ≤300 字符；**禁止**同义反复 / 复述式总结 / 模板过渡词堆砌 / 形容词堆叠
- 字数不足时**优先删冗余**，绝不补形容词
- 长文（7500 词级）如需豁免：本 skill frontmatter 声明 `budget_profile: longform`，调用时显式传参（见 RULES-70 §五）
- 交付前必须过：`post-write-check.sh` · `geo-check.sh` · `quota-check.sh` · `lang-check.sh`

# lovart-blog-automation

## 路径契约

| 层 | 路径 |
|----|------|
| 文档 SSOT | `1-1 GEO Readme/` |
| Sanity 脚本 | `1-4 Dev/lovart.sanity.studio/scripts/` |
| SEO/Sentinel 脚本 | `1-4 Dev/scripts/` |
| 自动化 | `1-4 Dev/automation/` |
| 本 Skill | `1-1 Harness/Skills/lovart-blog-automation/SKILL.md` |

End-to-end Lovart Blog (blogs.lovart.ai) content production: market research → writing → publishing.

This workflow must defer to `lovart-blog-signal-writer` as the active blog-writing backbone.
`lovart-blog-serp-writer` is deprecated for blog work and should not be used.
The parent blog workflow should decide the blog category first, enforce blog-level requirements, and then route into exactly one category subskill for category-specific writing rules.

> **Current status（2026-06-07）**：Blog 写作、封面分配和 WordPress 发布脚本已在当前结构中恢复。WordPress 发布仍标记为 `blocked-until-dry-run-verified`：实际发布前必须先跑 `--dry-run`，确认 WP 凭证、分类、标签、slug 与移动到 `03-Published/` 的行为符合预期。Feishu wiki integration 仍为 `blocked-by-missing-source`，不得当作可用发布通道。

## Triggers

- "write a blog post about {topic}"
- "publish drafts to Lovart blog"
- "research {keyword} for Lovart blog"
- "plan content calendar"

## Workflow (sequential)

### Phase 0A: Category routing (mandatory before writing)

Before outlining or drafting, classify the article into exactly one primary blog type:

- `Lovart 101`
- `How-To`
- `Best Practice`
- `Better Design`
- `Insight & Trend`
- `Review`
- `Complete Guide`
- `Stack × Stack`

Blog-level rules such as metadata completeness, cover/date/category integrity, FAQ hygiene, title hierarchy, layout checks, and publish-readiness belong to this parent workflow and should not be reimplemented independently in every category skill.

### Phase 0B: Market Research (MANDATORY before writing)

For new content creation, first use `lovart-content-creation-orchestrator` to produce the SERP + competitor brief, then continue with this Blog workflow. This keeps the older Blog pipeline aligned with current SERP intelligence, anti-slop rules, and i18n gates.

Before writing any article, complete ALL of these steps. Write findings to `01-Drafts/{slug}-research.md`:

1. **Duplicate check**: verify the slug/topic doesn't already exist on blogs.lovart.ai
   ```bash
   curl -s "https://blogs.lovart.ai/wp-json/wp/v2/posts?slug={slug}&per_page=1" | python3 -c "import sys,json; d=json.load(sys.stdin); print('EXISTS' if d else 'available')"
   ```

2. **Competitor SERP scan**: for the focus keyword, review the top 3-5 ranking pages:
   - What questions do they answer that we don't?
   - What content depth do they achieve (word count, H2 structure)?
   - What unique angle can Lovart bring (MCoT, ChatCanvas, Touch Edit)?
   - Record URLs, word counts, and H2 outlines

3. **Internal gap analysis**: check what Lovart content already exists in this cluster
   - Search `03-Published/` for similar articles
   - Confirm this article adds net-new coverage

4. **Data gathering**: collect concrete data points:
   - Lovart-specific: supported features, pricing, use cases
   - Competitor-specific: pricing, feature limitations, workflows
   - Industry benchmarks: market size, adoption rates, trends

5. **Angle decision**: based on research, choose one of:
   - **Comparison kill-shot**: we do X; competitor can't because Y
   - **Better Design**: conventional approach vs Lovart MCoT approach
   - **How-To gap fill**: teach something nobody else covers well
   - **Insight/Trend**: data-backed prediction with Lovart relevance

### Phase 1: Content Planning

- Check `PRODUCTION-PLAN.md` for existing assignment or create new row
- Allocate cover via `scripts/pick-cover.py <slug>`
- Confirm category mapping per `references/writing-spec.md`
- Set target word count: **≥7,500 words for every category** (universal floor 2026-07-17; old Comparison/101/How-To ladders abolished). Use multi-turn per RULES-20; no script padding.

### Phase 2: Writing

Write to `01-Drafts/` following `references/writing-spec.md`. Hard requirements:
- Frontmatter with ALL required fields
- H2 structure: problem hook → Part 1 competitor analysis → Part 2 Lovart solution → FAQ → cluster footer
- Derivative Scenarios (3+ concrete use cases)
- FAQ section (3-5 Q&A pairs)
- E-E-A-T signals (mention MCoT, ChatCanvas, Touch Edit, Nano Banana)
- Internal links: only verified slugs + `https://lovart.ai/signup` + `https://lovart.ai/pricing`
- Image appendix at end of article
- Footer cluster links (3-4 related articles)

### Phase 3: Publishing

状态：`blocked-until-dry-run-verified`。脚本存在于规范落点，但 production 发布前必须先 dry-run。

```bash
cd "1-3 Content Gen/Lovart-Blog-Pipeline/Lovart-Blogs"
python3 scripts/publish-to-wp.py --dry-run --file "{filename}.md"

# 用户确认 dry-run 后才允许实际发布：
python3 scripts/publish-to-wp.py --file "{filename}.md"
```

Auth: `WP_USER` / `WP_PASS` 环境变量，或 `scripts/wp-auth.local.env`（不得提交 Git）。Post goes live immediately. File moves to `03-Published/` with `wp_post_id` added.

## Project Structure

```
1-Project/1-3 Content Gen/Lovart-Blog-Pipeline/
├── Lovart-Blogs/   # 发布脚本规范落点 Lovart-Blogs/scripts/publish-to-wp.py（已恢复；发布前需 dry-run 验证）
│   ├── 01-Drafts/                      # staging (articles + research notes)
│   ├── 03-Published/                   # published (with wp_post_id)
│   ├── LOVART-BLOG-LOCAL-SPEC.md       # frontmatter spec
│   ├── PRODUCTION-PLAN.md              # article inventory (93 rows)
│   ├── BATCH-WORKFLOW.md               # batch rules + quality gates
│   ├── scripts/                        # pick-cover.py
│   └── templates/                      # frontmatter.example.yaml
```

## Anti-Bugs（禁止再犯）

> 全量目录：[ANTI-BUGS-REGISTRY.md](../../../1-1%20GEO%20Readme/ANTI-BUGS-REGISTRY.md)

| ID | 本 Skill 门禁 |
|----|--------------|
| AB-S01 | 写作时占位写 `imageBriefs`/附录 brief，**禁止** `IMAGE PLACEHOLDER` 进正文 |
| AB-S02 | frontmatter 必含 `slug`；缺则 convert 从文件名推断（须与线上一致） |
| AB-S03 | category 用 Sanity 合法名；别名由 `blog-taxonomy.js` 映射 |
| AB-I08 | 新稿封面用 `blog-cover-pool.js` / `pick-cover.py`；禁止随机 liblib URL |
| AB-U02 | 内链仅 `/blog/{slug}`；禁止 `/博客文章/`、`.md)` 路径 |
