---
name: moodio-film-content
description: Moodio Global 创作父入口（blog + 六类落地页）。Use when planning, researching, writing, rewriting, or QA-ing Moodio content, or when a Moodio content task needs routing. 架构对齐 Lovart 真实创作链：orchestrator 总控 → 信号层选题 → content-writer 方法论 → 类型子技能治理 → 门禁 → S4-qa 止步。品牌事实唯一出处 = KB Moodio 目录。
---

## 预算与铁律（继承，非另写）

- **RULES-70 预算**：Blog 1200–1800 词（绝不超 2160）；落地页 600–1000；H2 4–7；FAQ 3–5；每千字 1–3 数据点；外部来源 2–5 条完整 URL；列表块 ≤4 且不连续；单段 ≤300 字符；字数不足删冗余不补形容词。
- **RULES-20 创作硬条款（Moodio 适用子集）**：每个 Blog ≥1 个可引用观点句（金句）；每 500 字 ≥1 个 H2；slug kebab-case 禁下划线；多语言版本语义等价、字数不低于其他版本 60%；禁编造产品/竞品数据，不确定标 `[待考证]`。
- **交付前四门禁**：`post-write-check.sh` · `geo-check.sh` · `quota-check.sh` · `lang-check.sh`（Moodio 全部已实测适配，见 04 审计记录）。
- **三层门禁体系**（RULES-30）L1 机器钩子 → L2 content-quality-gates skill → L3 人工 QA（清单见 §Phase 4）。

## 品牌事实 SSOT（唯一出处，零幻觉）

- 能力词：`insight-data/Knowledge Base/Moodio/01-capability-glossary.md`
- 数字/事实：`04-product-facts.md`；表达红线：`03-messaging-rules.md`（官方 5 条 Don'ts，违反即 BLOCK）
- 人群/场景：`02-personas-scenarios.md`；团队/融资/案例：`08-team.md`
- **Lovart 术语（MCoT/ChatCanvas/Nano Banana 等）在 Moodio 内容中一概禁止**——两个工具不同，术语不互通。

## 定位与真链路（对齐 Lovart 架构）

本 skill 是 **Moodio 创作父入口**，对应 Lovart 体系中 `blog-writer（总控模式）` 的角色：

```
Step 0 路由（pipeline-state + 判断 blog/page/refresh）
  → Step 1 信号层（选题从哪来——Moodio 适配版，见下）
  → Step 2 方法论（content-writer.md 核心，品牌无关部分直接继承）
  → Step 3 类型路由（8 类博客 taxonomy / 落地页类型）
  → Step 4 写作（模板 moodio-film-studio 注入官方口径）
  → Step 5 门禁（四钩子自动 + L2 gates）
  → Step 6 S4-qa 人工审（自动化止步于此，发布人工授权——与 Lovart 同原则）
```

### Step 1 信号层 —— Moodio 适配版（与 Lovart 的关键差异）

Lovart 博客由 `blog-writer` 驱动（Sentinel 舆情 + GSC 数据 → 选题）。**Moodio 站未上线，无 GSC/舆情存量——信号层降级为三源**：

| Moodio 信号源 | 取什么 | 对应 Lovart 信号 |
|---|---|---|
| `06-seo-keywords.md` 词矩阵 | 主词+辅词+空档标记（⭐） | GSC 词表（上线后切换为真 GSC） |
| `run/projects/moodioglobal/citations.jsonl`（GEO 探针） | 竞品被提及而 Moodio 缺席的查询 → 对比/答案内容 | 舆情 §二 竞品动态 |
| topics.json 队列 | 排程弹题（auto_loop 已开，quota 2/天） | PRODUCTION-PLAN 排期 |

**去重**（同 Lovart Phase 1 两层法）：topics 队列内查重 + `run/projects/moodioglobal/content/` 已生成稿查重。**优先级**：ICE（Impact=词意图×商业价值 / Confidence=空档与竞争度 / Ease=写作成本）。**GSC 上线后**：本节切回 signal 模式（高曝光低点击词/排名 8-20 词/竞品对比词三表照搬 Lovart）。

### Step 2 方法论 —— content-writer.md 直接继承（品牌无关部分）

写前必读 `../content-writer.md`（41KB 核心叙事规则），以下对其**原样继承**：

- **12 类型矩阵 + 11 叙事框架库** + 类型↔框架配对规则
- **Anti-AI Writing Rules v4（全部强制）**：开头禁统计句（用场景/具体的人开）；禁 "Part 1/Part 2" 标签；禁 "There are three reasons…" 式列表旗标；禁三明治段落节奏；禁 PAS 模板块；[Comparison] 禁"类别/我方/竞品"三列表格为主结构（用叙事对比）；数据必须有上下文，禁假精确
- **Angle Engine**：微观人群切片（"senior product designers at Series B SaaS" 级别）→ 摩擦点 → 反共识角度 → 5 标题法（1 观点/1 人物/1 数字/1 SEO/对比加 verdict）
- 执行流 Step 0-5（Routing → Angle → 开场 → 实证 → 收口）

**读法适配**：文中 `品牌方` 占位符 = Moodio；Sanity Output Protocol 节暂不适用（CMS 未定，见"不可迁移清单"）。

### Step 3 类型路由

**Blog 8 类**（继承 Lovart taxonomy，governance 见 `../references-blog-subskill-governance.md`）：101 / How-To / Best Practice / Better Design / Insight & Trend / Review / Complete Guide / Stack×Stack → Moodio 首月主力：How-To、Comparison（=05-competitors 规则）、Insight & Trend、101。类型子技能（content-101/complete-guide 等）结构规则通用可读，但其中 Lovart 案例/术语以 Moodio KB 覆盖。

**落地页六类**（console GEN_TYPES）：features/tools/product/scenario/solution/topic → 走创作中心 + moodio-film-studio 模板 + 四门禁。**注意**：Lovart 的 `landing-writer` skill 完整机器（故事线 6 维绑定/composite-v2 JSON/图片库/Sanity 发布）**依赖 genflow 与 Sanity，Moodio 当前不可迁**——Moodio 页面 = Hero（主词+副标+CTA"申请内测码"）→ 3 Benefit → 场景 2 → FAQ 3 → CTA，七要素总则（buyer/input/output/edit path/proof/CTA/FAQ）照常适用。

### Step 4 写作注入

生成走 console 时 template_id=`moodio-film-studio`（audience/tone/structure/anti_slop_extra 八条官方红线已内置）。人工/agent 写作按本 skill §SSOT + 模板 prompt 同源规则。

### Phase 4 / Step 6 — 人工 QA 清单（S4-qa）

1. 表达红线 5 条逐条对照（03）2. 能力词对表（01）3. 数字对白名单（04）4. 金句存在 + H2 密度 5. 主词落位 H1/首段/slug 6. FAQ 3-5 覆盖真实异议（内测资格/导出格式/与竞品区别/适用边界）7. Anti-AI 抽查（Part 1 标签/三明治段落/假精确）8. 案例仅《了不起啊！朋友》可用且复核上线状态 9. 补外部来源 2-5 10. CTA=申请内测码。

## 不可迁移清单（Lovart 资产 → Moodio 适配状态）

| Lovart 资产 | 状态 | Moodio 替代 |
|---|---|---|
| blog-writer 的 Sentinel 舆情 + GSC 信号 | ⏸ 站点未上线无数据 | 06 词矩阵 + GEO citations 缺口 + topics 队列（上线后切回） |
| 封面池（56 URL）+ pick-cover.py | ⏸ 媒体素材 TBD | image_briefs 字段占位，等素材包 |
| landing-writer 完整故事线机器（6 维绑定/composite-v2/33 组件） | ⏸ 依赖 genflow SSOT | console 模板+门禁生成；CMS 定后建 Moodio 故事线（Phase 2） |
| Sanity 发布链（sanity-publish 12 技能） | ⏸ CMS 未定 | 自动化止步 S4-qa，发布人工（原则同 Lovart"发布前人工授权"） |
| WordPress 终端（blogs.example.com） | ✗ 不适用 | 无 |
| RULES-20/30/70/80、content-writer.md、Anti-AI 规则、governance、四门禁 | ✅ 直接继承 | — |
| 竞品数据（05-competitors v2.0 实测档案） | ✅ Moodio 特有（Lovart 无此版） | — |
