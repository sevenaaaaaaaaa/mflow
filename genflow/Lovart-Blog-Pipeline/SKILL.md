# lovart-blog-automation

End-to-end Lovart Blog (blogs.lovart.ai) content production: market research → writing → publishing.

## Triggers

- "write a blog post about {topic}"
- "publish drafts to Lovart blog"
- "research {keyword} for Lovart blog"
- "plan content calendar"

## Workflow (sequential)

### Phase 0: Market Research (MANDATORY before writing)

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

```bash
# TODO(reorg 2026-06-03/GAP): publish-to-wp.py 随 1-Project/Wordpress/ 在重构中删除（断链已归档），发布前需恢复到下方落点
python3 "1-Project/Lovart-Blog-Pipeline/Lovart-Blogs/scripts/publish-to-wp.py" --file "{filename}.md"
```

Auth: WP cookie session (Seven's credentials in script). Post goes live immediately. File moves to `03-Published/` with `wp_post_id` added.

## Project Structure

```
1-Project/Lovart-Blog-Pipeline/
├── Lovart-Blogs/   # 发布脚本规范落点 Lovart-Blogs/scripts/publish-to-wp.py（TODO: 重构中删除待恢复）
│   ├── 01-Drafts/                      # staging (articles + research notes)
│   ├── 03-Published/                   # published (with wp_post_id)
│   ├── LOVART-BLOG-LOCAL-SPEC.md       # frontmatter spec
│   ├── PRODUCTION-PLAN.md              # article inventory (93 rows)
│   ├── BATCH-WORKFLOW.md               # batch rules + quality gates
│   ├── scripts/                        # pick-cover.py
│   └── templates/                      # frontmatter.example.yaml
```
