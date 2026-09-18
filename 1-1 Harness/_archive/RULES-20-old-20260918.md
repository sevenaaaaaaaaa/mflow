---
type: rule
version: 1.1
updated: 2026-07-17
scope: "profile-creation-active"
tools: [hermes, opencode, claude]
status: active
path: 1-1 Harness/02-rules/RULES-20-creation.md
generator: 1-1 Harness/11-knowledge/scripts/fm-fix.py
changelog:
  - 1.1 (2026-07-17): add Column-Writer Lane + Banned Template-Phrase Registry; multi-turn state machine now default-on for ≥5,000-word Blog
  - 1.0 (2026-07-05): initial
---
# Lovart RULES — 20 创作类（Creation）

> 适用路线：Blog 创作、Features/Tools/Solution/Product/Scenario/Landing/Topic 落地页
> 加载 Profile：`lovart-creation`

---

## 故事线为总纲（页面生成第一原则，2026-07-05）

页面生成以**故事线**为总纲。选定故事线后，以下 6 个维度全部以该故事线为准，禁止各写一套：

| 维度 | 以故事线为准的来源 |
|------|--------------------|
| 文案 | 故事线 copy 绑定：landing/solution/scenarios JSON 的 `copy`/`copyDefault`；feature/tool/product/topic 见 `page-copy-bindings.json` |
| 模块 | 故事线 `sections`（`type` 顺序） |
| 个性化 | 故事线 `audience` + `intent` → Persona Matrix |
| 配图 | 故事线 `sections` + card title → `image_pool`（选图范围由该故事线模块集界定） |
| CRO | 故事线 `intent` + `ctaStyle` → 流量阶段 / CTA / 紧迫感 |
| 质检 | `COPY-PREFLIGHT`（storyline-driven）+ 质量门禁 |

**执行顺序**：`PAGE-BRIEF → 选故事线 → 读该故事线全维度绑定 → 生成 → COPY-PREFLIGHT`。

**禁止**：绕开故事线自定义 intent、模块序列或文案要求；在 skill 里另写一套与故事线冲突的规则。

**要迭代任一维度**：改故事线绑定（结构改 `sections`；文案/CRO/个性化改 `copy`/`copyDefault`；intent 词汇改 `page-copy-bindings.json` 的 `masterIntents`+`intentCrosswalk`），脚本与文档自动跟随。

机器约定见 `page-copy-bindings.json` 的 `governedDimensions`；权威结构见 `STORYLINE-BY-DIRECTION.md`。

---

## 创作前路由（必做）

每次创作前先判断页面类型，走对应的 Skill 和模板：

| 页面类型 | Skill | 模板 | Sanity 类型 |
|---------|-------|------|------------|
| Blog | `lovart-blog` / `lovart-blog-signal-writer` 父链 | frontmatter spec + writing-spec | `blog` |
| Tools | `lovart-landing-page` 父入口 | composite-v2 + T1–T-long | `compositePage` |
| Features/legacy | `lovart-landing-page` 父入口 | 10 个 section_xx key | `compositePage` |
| Landing Page | `lovart-landing-page` 父入口 | 7 条故事线 + 12-15 段 | `compositePage` |
| Product/Solution/Scenario | `lovart-landing-page` 父入口 | composite-v2 | `compositePage` |
| Topic | `lovart-composite-page-design` | 33 模块不拉踩 | `compositePage` |

**禁止混用**：Tools 故事线写 Landing、legacy 长链写 Tools。

**入口收敛**：`lovart-page-serp-writer` 与 `refresh-page-page-generator` 只能由 `lovart-landing-page` 内部调用；不得作为用户请求的直接入口。

## Blog 创作规范

- 结构：problem hook → Part 1 竞品分析 → Part 2 Lovart 解决方案 → FAQ(3-5条) → cluster footer
- Frontmatter 必含：slug、category（Sanity 合法值）、cover_url、image_briefs
- Category 陷阱：`Better Design`/`Comparison`/`Segment` 是 writer type，不是 Sanity category。正确映射：Better Design→Branding, Comparison→How-To, Segment→Industry Solution
- 内链仅 `/blog/{slug}`，禁止 `/博客文章/`、`.md)`、`#` 占位
- 封面：`blogcover-011~065` 池，pick-cover.py stable hash，禁止 liblib 随机 URL
- 禁止 IMAGE PLACEHOLDER 入正文，image_briefs 不上屏
- `publishedAt`=null 时用 `_createdAt`

### 长文分段创作状态机 (Multi-Turn Generation Protocol)
由于 LLM 单次输出 Token 限制，**绝对禁止**单次生成超过 3,000 词的长文。所有 Complete Guide (≥7500词) 和 Insight & Trend (≥4500词) 必须强制走以下状态机：
1. **[STATE 1: OUTLINE]**：先生成超详细大纲（包含 H2, H3, 预估字数、核心观点和 ASCII 矩阵设计），等待用户确认。
2. **[STATE 2: DRAFT_PART1]**：仅生成大纲的第 1-3 章节（确保技术细节拉满，无任何总结性缩水），输出当前字数。
3. **[STATE 3: DRAFT_PART2]**：仅生成大纲的第 4-6 章节，输出当前字数。
4. **[STATE 4: DRAFT_PART3]**：生成剩余章节（含 FAQ 和 Golden Closing），输出当前字数。
5. **[STATE 5: INTEGRATE_QA]**：合并全文，运行 Anti-Slop 禁用词自检，输出最终总字数。
*Agent 行为约束：任何时候用户提及"写一篇 Complete Guide"，Agent 必须在首轮回复中强制进入 STATE 1，严禁一揽子直接输出全文！*

### Banned Template-Phrase Registry（脚本扩张黑名单）
2026-07-17 由 `blog-padded-junk` 归档事件沉淀。下列句式是脚本扩字数常出现的"通用 production workflow"模板，任何人工/脚本写出的段落包含以下任一 trigger → 立即 BLOCK。

<!-- HARNESS_BANNED_TEMPLATE_START -->
- `The structured approach described here replaces guesswork with a repeatable process`
- `Teams that follow this approach report`
- `Production volume has a significant impact on the workflow structure`
- `Scaling production workflows successfully requires`
- `Common workflow mistakes and how to avoid them`
- `The practical implementation of this part of the workflow requires`
- `Production metrics that matter`
- `Tooling for production workflows`
- `Team roles in production workflows`
- `Risk mitigation in production workflows`
- `Workflow improvement through feedback`
- `Long-term benefits of workflow adoption`
- `How the workflow applies in practice`
- `The detailed specifications for AI-assisted design production`
- `Review criteria for production output`
- `Delivery and publication`
- `Quality assurance for production workflows`
- `The role of specification templates in production workflows`
- `Specification templates evolve over time based on`
- `Workflow documentation and reference materials`
- `Workflow adoption strategy`
- `Low-volume workflows` / `Mid-volume workflows` / `High-volume workflows`
- `Consider a typical content project: a marketer needs`
- `production-grade workflow pipeline`
<!-- HARNESS_BANNED_TEMPLATE_END -->

任何新 trigger 加进此块：`harness_auto_optimize.py --register-template-phrase "<phrase>"`。
**不得**用这些句式构造段落；写了就是脚本味，preflight TPL_DRIFT = BLOCK。

---

## Column-Writer Lane（专栏作家 lane，2026-07-17 立）

> 适用场景：所有进 `status: ready` 的 Blog。**全分类英文正文统一地板 ≥7,500 词**（用户铁律 2026-07-17；旧 How-To 1800 / Comparison 3600 / Insight 4500 等分档已废止）。
> Skill `lovart-blog-signal-writer` 是合规外壳，column-writer lane 是内容质量内核。
> 两者必须同时满足：skill 出前序信号、规格、链接、封面；column-writer 出正文质量。

### Lane Routing（按 GSC 信号分层）
任何一篇 Blog 写作开始前，先按 GSC 信号分 lane，定 **effort / multi-turn 深度**（不降低词数地板）：

| 信号 | Lane | 流程 | 写作 |
|------|------|------|------|
| impression > 1k, 排名 4–10 | **Deep** | Multi-turn 3+ pass + cascade | **≥7,500** 词，column voice |
| impression 500–1k, 排名 11–20 | **Medium** | Multi-turn 2 pass + 1 polish | **≥7,500** 词，column voice |
| 低信号 | **Light** | Multi-turn 仍须 OUTLINE→PART→INTEGRATE；可减 polish 轮次 | **≥7,500** 词（含 refactor 已有生产稿） |

**硬地板**：任何 category 标 `ready` / 进 Sanity 前，正文 words `< 7500` → BLOCK。
**废止「脚本灌字凑 7500」**：禁止模板句 / pad 段落 / Banned Template-Phrase Registry 里的灌水。Lane 只定轮次与 cascade，**不**允许用更低词数出门。

### OUTLINE 阶段 (State 1) 必含 6 项
任意 ≥5,000 词 Blog 进 State 1，**必须**包含：

1. **一句话立场 (column spine)**：「我认为 / 在测试 N 个项目后我注意到 / 我反对常见观点 X 因为 Y」 — 不是 "This article covers" 这种合规外壳话
2. **3 个反方观点 / 常见误解 (要进攻的靶子)**：写明要打破的具体错误判断
3. **≥5 个具体场景 / 数字 / 引用**：从 SERP/GSC/产品数据/KB 抓出来，**不是 "many teams" 而是 "37 of 142 跑了 14 天"** 这种粒度
4. **H2/H3 字数预算**：每个 H2 ≤2,500 词；总字数符合 lane floor
5. **ASCII 矩阵或流程图**：≥1 个，展示核心数据对比或因果关系
6. **Lovart 在文中的角色图谱**：Lovart 在哪个具体步骤做哪个具体动作 — 不是 "Lovart helps you"

### 每次 DRAFT_PART_N 必含 4 项
任意 Part 写出前，agent 必须自检：

1. **first-person 经历或具体客户案例 ≥1**：不是通用模板
2. **数字 ≥3**（百分比、人数、时长、容量、价格 — 任一）：不是 "many" 而是具体数
3. **真实 Lovart 行为描写 ≥1**：
   - ✅ 好： "I typed 'campaign, vintage, slate blue, 1 hero + 3 variants', the agent..."
   - ❌ 差： "Lovart's powerful AI can generate multiple variants quickly"
4. **段落 unique 度**：写完后跟升级队列其他 791 篇做 n-gram 12 比对，重合度 ≥ 0.7 BLOCK

### Cascade Inspect（默认开启 — `lovart-quality-cascade`）
2026-07-17 起，**任何 ≥5,000 词 Blog 必须跑 cascade**（不再是 experimental/显式开启）：

```
writer (lovart-creation) 写 v(N)
  ↓
critic (lovart-quality) 评 7 项
  - stance 是否清晰（前 200 词有 spine 句？）
  - evidence ≥5（具体数字/案例/引用）
  - voice 是否模板化（被任何 HARNESS_BANNED_TEMPLATE 或 HARNESS_BANNED_EN hit）
  - 段落 unique 度（n-gram 12 比对）
  - H2/H3 嵌套合法
  - Lovart 术语 cluster 化出现 ≥1
  - 字数 = Σ(PART1+PART2+PART3)，而非 padding
  ↓
若 fail → 携 reasons 回 writer v(N+1)，max 3 轮
若 pass → 进 State 5 INTEGRATE_QA
超 3 轮 escalate 人工
```

### Skill Block 与 Column-Writer Lane 对应表

| Skill 硬要求 | Column-Writer Lane 改造 |
|------------|------------------------|
| FAQ (PAA) | 改写 "读者最常问我什么"，3-5 个 derived from real reader pushback；不是 generic template Q&A |
| 三段式 (第一性原理 → 策略 → Lovart 实操) | 改成 "Stance → Approach → When the tool earns its keep"。Column 立场，必须明确反对某个常见观点 |
| Internal Links 表 | 内嵌一句 "we covered X in {title} guide" 引用 + 文末 brief list（≤5）。**禁止** 12-row 表 |
| Image Appendix 表 | 改写 brief inline description（≤2 行）。**禁止** Recommended image set 模板 4 行 |
| Cluster 术语必须出现 | 术语必须**嵌入具体场景**举例。**禁止** 孤词或定义句 |

### Inline Anti-Padding Check
写完 PART 后 agent 必须跑：

```python
import re
text = open('draft.md').read()
# 1. Detect banned template phrases
banned = [...]  # load from HARNESS_BANNED_TEMPLATE registry
for p in banned:
    if p in text:
        BLOCK(f'template phrase: {p}')
# 2. Detect paragraph duplication (n-gram 12)
paras = [p for p in text.split('\n\n') if len(p) > 80]
for i, p1 in enumerate(paras):
    for p2 in paras[i+1:]:
        grams1 = {tuple(p1.split()[k:k+12]) for k in range(len(p1.split())-11)}
        grams2 = {tuple(p2.split()[k:k+12]) for k in range(len(p2.split())-11)}
        if grams1 & grams2:
            BLOCK(f'paragraph reuse: ...')
# 3. Validate H2/H3 structure
import re
headers = re.findall(r'^#{2,3} (.+)$', text, re.M)
from collections import Counter
dupes = {h: c for h, c in Counter(headers).items() if c > 1}
if dupes:
    BLOCK(f'duplicate headings: {dupes}')
```

3 项任一 fail → 不进 State 5。

---

## 落地页创作规范

- Tools：用 `image_pool.py`（43 张图 7 分类）选图，**不用** pick-cover.py
- 图片 7 分类：video/avatar/image_gen/design/edit/ecommerce/generic
- Card title 匹配用 word-boundary regex（`\btext\s+edit\b`），禁用子串匹配
- 多语言：同一 slug 不同 _id（`{id}-{lang}`），bodyJson 共享（改一个语言全改）
- SEO title 模板：slug 主关键词**强制出现**在 title 中，禁止回退到默认 avatar title
- Topic 页 33 模块不拉踩竞品

## 竞品对比公正性

- 竞品对比客观公正，不拉踩
- 多语言禁止 EN 壳子（body 必须翻译，不能只改 title 不改内容）
- CRO 品类不互盖：bento-6/cluster-block-dense/hero-cinematic 各司其职

## 存量改造优先

GSC 3980 零点击 Blog 中 2943 个排名 4-10（首页但跳过），改造 ROI 远高于新建。
公式：**核心关键词 + 限定词 + 价值主张**（限定词=时间/场景/限制/对比/行业）
142+ Blog 改写方案在 `Output/SEO-Reports/改造建议/`

## i18n 多语言

10 语言：en/de/fr/it/ja/ko/pt/ru/zh/zh-TW
翻译 ≠ 直译。品牌术语不翻译。de/fr/it/ja/ko/pt/ru/zh/zh-TW 版本是 SEO+UX 必要组成，不可省略。
