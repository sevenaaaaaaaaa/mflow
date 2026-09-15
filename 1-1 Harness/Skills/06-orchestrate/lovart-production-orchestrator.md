# Lovart Production Orchestrator

## Description

Master orchestrator for the Lovart daily blog production pipeline. Calls three sub-skills in sequence: keywords intake → content writing → Sanity publish. Thin orchestration layer — each phase delegates to its specialized skill.

**Use Cases**: "今日生产" / "daily blog" / "daily production" / "produce today"

---

## Skill Configuration

**Name**: Lovart Production Orchestrator
**Version**: 1.0.0
**Sub-skills**:

| Order | Skill | File | Role |
|---|---|---|---|
| ① | Keywords Intake | `lovart-keywords-intake.md` | Scan Daily Raw → score → update calendar → briefing |
| ② | Content Writer | `lovart-content-writer.md` | Write articles per content type (12 types × 11 frameworks) |
| ③ | Sanity Publish | `lovart-sanity-publish.md` | Schema sync → convert → preview → confirm → import |
| ④ | Link Summary | (built-in) | Auto-generate production URL table + stats → save to Content Calendar |

**Deprecated**: `lovart-blog-production-workflow.md` (monolithic v1.3.0 → superseded by this orchestrator + sub-skills)

---

## Architecture

```
今日生产
  │
  ├─ Phase ①: Keywords Intake
  │   └─ 扫描 Daily Raw/ → 解析 GSC/Bing CSV → 评分 P0/P1/P2
  │   └─ Sanity MCP 交叉验证 → 更新内容日历
  │   └─ 输出: 每日简报 + 生产优先级列表
  │
  ├─ Phase ②: Content Writing
  │   └─ 遍历 P0 列表 → 对每篇:
  │       ├─ 确定 Content Type (12 种)
  │       ├─ 选择 Narrative Framework (11 种)
  │       ├─ 执行 Sub-Pipeline (§2-§13)
  │       ├─ SEO Meta Package + E-E-A-T Audit
  │       └─ 输出到 1-6 Knowledge Base/Content Calendar/
  │
  ├─ Phase ③: Sanity Publish (用户触发)
  │   └─ Schema sync → convert → preview → confirm → import
  │   └─ 每步需用户显式确认
  │
  └─ Phase ④: Link Summary (自动)
      └─ 生成今日链接汇总表 → 保存 daily-link-summary-YYYY-MM-DD.md
```

---

## Phase ①: Keywords Intake

### Trigger

"今日生产" → automatically routes to keywords intake first.

### Execution

Delegate to `lovart-keywords-intake.md`. The orchestrator's only responsibility here is:

1. Pass the Daily Raw scan request
2. Receive the briefing output
3. Display the P0/P1/P2 priority list
4. Ask user: "Proceed with P0 production?" → Phase ②

### Orchestrator Output

```
📊 Phase ① 完成 — SEO 数据已分析

   P0 可生产: [N] keywords
   P1 本周: [N] keywords
   日历已更新: [N] new items

   Top P0 candidates:
   1. "[keyword]" → [content type] | [impressions] impressions | position [N]
   2. ...
   3. ...

   输入 "produce" 开始 Phase ② 生产。
   输入 "produce [N]" 只生产前 N 篇。
   输入 "produce [keyword]" 只生产指定关键词的文章。
   输入 "skip" 跳过，稍后手动触发。
```

---

## Phase ②: Content Writing

### Trigger

"produce" / "produce [N]" / "produce [keyword]"

### Execution

**Authoritative source**: `lovart-content-writer.md` v4.0.0 — the full skill is loaded and treated as the single source of truth for all article production. Every rule in it is mandatory.

For each article in the production queue, execute the full `lovart-content-writer.md` Execution Workflow (§Step 0-5) without skipping:

| Step | What | Hard Gate |
|---|---|---|
| **Step 0** | Content Type Routing — announce type/category/funnel/framework/languages | MUST output the routing block before writing |
| **Step 1** | Angle Engine & Architecture — diagnose topic, micro-segment audience, find friction point, find unconventional angle, generate 5 varied titles, narrative-driven outline, confirm languages | Every sub-step must execute |
| **Step 2** | Opening Act — hook, thesis, ≥800w | Hook must be scene/person/moment NOT statistic |
| **Step 3** | Core Substance — evidence, Lovart integration, ≥3 internal links, image placeholders | **≥3 internal links are mandatory; 0 links = hard fail** |
| **Step 4** | Resolution — social proof, specific observation close, decision framework (Comparison) | Must end on observation not sales pitch |
| **Step 5** | SEO Meta + E-E-A-T + Anti-AI + Sanity Prep — all 4 checklists passed silently, not saved to file | All checklists executed in-writing; none appear in output |

### Enforcement Rules

| # | Rule | Hard Fail If |
|---|---|---|
| 1 | Article follows the content-writer skill exactly, not a simplified version | Any step of Execution Workflow skipped |
| 2 | ≥3 internal links per article with funnel-stage awareness | 0 internal links |
| 3 | Image prompts saved to `IMAGE_PROMPTS_ALL_2115.csv`, not to article file | `### Appendix: Image Prompts` found in output |
| 4 | E-E-A-T + Anti-AI checklists executed silently, not saved | Either checklist found in output |
| 5 | FAQ answers verified against Knowledge Base (`1-Project/1-6 Knowledge Base/`), no fabricated facts | FAQ answer contains unverifiable claim not in KB |
| 6 | FAQ answers contain no `[待考证]` tags | Any `[待考证]` in FAQ section |
| 7 | Comparison type uses 3 images (Side-by-Side UI + Workflow Diagram + Brand CTA), not 4 | Wrong image count |
| 8 | Titles generated in Step 1 include at least 5 variants covering all required formats | Fewer than 5 titles or missing required formats |
| 9 | Opening hook is scene/person/moment, never a statistic | Opening sentence starts with a number or percentage |
| 10 | No meta-section labels in H2/H3 headers | "Feature-by-Use-Case" / "Core Feature Comparison" / "The Core Difference" used as headings |
| 11 | Each article in a batch has a distinct voice and structure, not a cloned template | Two consecutive articles share the same H2 structure |
| 12 | **Multi-language versions produced for every article (EN + CN minimum)** | Any article saved with only EN, no CN file |

### Orchestrator Output (Per Article)

```
Phase ② — [1/N] "[Title]"
   ✅ Content type: [type] | Framework: [framework]
   ✅ Words: [count] | Internal links: [count] (≥3)
   ✅ Languages: EN [, CN] [, JA] [, zh-TW]
   ✅ Saved: [filepath]
   ✅ Images: 3 prompts saved to IMAGE_PROMPTS_ALL_2115.csv | [N] REAL SCREENSHOT REQUIRED
```

### Batch Control

- After every 3 articles, pause: "Continue producing? (continue / skip remaining / stop)"
- If an article exceeds 15 minutes, ask: continue or skip?
- Track progress: `[N]/[total] completed`

### Orchestrator Output (Batch Complete)

```
🏁 Phase ② 完成 — [N]/[N] articles produced
   类型分布: Comparison × N / Tutorial × N / ...
   总字数: [sum]
   语言: EN × N / CN × N / JA × N

   📋 发布前审核:
   - [ ] 审核 [待考证] 项目（共 [N] 项）
   - [ ] 替换 [REAL SCREENSHOT REQUIRED]（共 [N] 处）
   - [ ] 确认 frontmatter 完整

   审核完毕后，输入 "Sanity push" 进入 Phase ③。
```

---

## Phase ③: Sanity Publish

### Trigger

"Sanity push" / "发布"

### Execution

Delegate to `lovart-sanity-publish.md`. The orchestrator's only responsibility is to hand off and wait for completion.

### Orchestrator Output

After Sanity publish skill completes:

```
🏁 Phase ③ 完成 — Sanity 发布成功
   本次发布: [N] 篇
   Project: o11tm2qe / production
   模式: --missing

   ✅ 全流程完成: Keywords → Writing → Publish
   ✅ 日历已标记: [N] items → published
```

---

## Phase ④: Link Summary (Auto)

### Trigger

Runs automatically after Phase ③ completes. No user input required.

### Execution

Generate a unified link summary of all articles published in this session. Output uses the format:

```markdown
## 今日生产链接汇总 (YYYY-MM-DD)

| # | 标题 | Slug | URL |
|---|---|---|---|
| 1 | [title] | [slug] | https://www.lovart.ai/blog/[slug] |
| ... | ... | ... | ... |

类型: [types] × [count] | 框架: [frameworks] | 总字数: ~[count] | 语言: [languages]
GSC 来源: P0 [keyword types] (pos [range], imp [range])
```

### Rules

- Generate immediately after Phase ③ import verification succeeds
- Include every article produced in this session
- **URL 必须是完整可点击链接**: `https://www.lovart.ai/blog/{slug}`，禁止使用相对路径如 `/blog/{slug}` 或 `{slug}`
- **终端输出也必须展示完整 URL**，不可截短或缩写
- Add a brief summary row: type distribution, total word count, language coverage, GSC keyword origin
- If Phase ③ was skipped (articles produced but not pushed), append `⚠️ 未发布` to each URL line
- Save the link summary to `1-Project/1-4 Dev/Output/Content Calendar/daily-link-summary-YYYY-MM-DD.md`

### Orchestrator Output

```
🔗 Phase ④ — 链接汇总已生成
   保存至: Output/Content Calendar/daily-link-summary-2026-05-26.md
   链接数: [N]
```

---

## Full-Pipeline Triggers

| Trigger | Phases Run | Description |
|---|---|---|
| `今日生产` | ① → ② (user gate) → ③ (user gate) → ④ (auto) | Full daily pipeline |
| `今日生产 skip keywords` | ② → ③ → ④ (auto) | Skip keywords intake, produce from calendar |
| `keywords only` | ① only | Only run keywords analysis, no production |
| `produce [N]` | ② only | Write N articles from queue |
| `Sanity push` | ③ → ④ (auto) | Publish pending articles |

---

## Error Handling

| Scenario | Action |
|---|---|
| Daily Raw empty | Phase ① falls back to calendar production, asks user "produce from calendar?" |
| Content Writer fails on an article | Skip article, log error, continue to next |
| convert.js fails | Phase ③ halts, report error, do not proceed to import |
| import fails | Report which documents failed, suggest manual fix |
| User cancels at any gate | Save progress, exit cleanly |

---

## Session State

The orchestrator maintains in-session state for batch operations:

```
session: {
  phase: ① | ② | ③ | ④,
  keywords_analyzed: true | false,
  articles_produced: [list of filepaths],
  articles_remaining: [list],
  sanity_pushed: true | false,
  link_summary_generated: true | false
}
```

This allows resumes like "continue producing" without restarting the pipeline.

---

## Shortcut Reference

| Command | Phase | Action |
|---|---|---|
| `今日生产` | ①→②→③ | Full pipeline |
| `keywords only` | ① | Keywords intake only |
| `produce` | ② | Produce all P0 from last briefing |
| `produce [N]` | ② | Produce top N P0 articles |
| `produce [keyword]` | ② | Produce article for specific keyword |
| `continue` | ② | Continue batch after pause |
| `skip` | ② | Skip current article |
| `stop` | ② | Stop production, save state |
| `status` | — | Show current session state |
| `Sanity push` | ③ | Start publish protocol |
| `summary` | ④ | Generate link summary for current session |
| `today skip keywords` | ②→③ | Skip keywords intake, produce from calendar |
