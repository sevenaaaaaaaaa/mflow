# Content Production Ledger — 内容生产台账

> 用途：在生成过程中逐节记录「必须写什么」，防止漏模块、后半缩水、续写失忆。  
> 上游：[Anti-Slop.md](./Anti-Slop.md)、SERP brief  
> 配对：[Content-Quality-Rubric.md](./Content-Quality-Rubric.md)（Rubric 判好坏；Ledger 保完整）  
> 下游：Blog / Page skills、`lovart-content-quality-gates`、preflight、样本库

---

## 1. 为什么需要 Ledger

Rubric 解决「这篇内容好不好」，Ledger 解决「生成过程中有没有漏写、缩水、失忆」。

常见失败模式：

- 大纲写了 8 个 H2，成稿只剩 5 个，后 3 个变成 FAQ 填充。
- 多轮续写后，Agent 忘记前半已承诺的例子、证据、内链。
- 多语言批量生成时，只翻译正文，标题 / FAQ / CTA 仍是英文结构。
- Landing 页 hero 写满，后半 proof / workflow / FAQ 被省略。

Ledger 是**生成前的计划表 + 生成中的状态表 + 成稿前的核对表**，必须在动笔前创建，每写完一节更新，续写前回读。

---

## 2. 使用时机

| 阶段 | 动作 |
|---|---|
| SERP brief 完成后 | 创建 Ledger，列出全部 H2 / section |
| 开始写第一节前 | 确认 Ledger 已覆盖 brief 中的 proof、FAQ、内链 |
| 每写完一节 | 更新该节状态为 `done`，填写实际字数与密度标记 |
| 上下文将满 / 任务中断 | 保存 Ledger，标注 `next_section` |
| 续写前 | **必须先回读 Ledger**，禁止凭对话记忆继续 |
| 成稿前 | 跑防缩水检查（§6）与完整性核对（§7） |

**规则：没有 Ledger，不得开始长文或批量多语言生成。**

短内容豁免：Product copy 单屏文案、Digest/Glossary 条目、少于 3 个 H2 的短文可不建完整 Ledger，但仍需记录读者、意图、CTA。

---

## 3. Blog Ledger

### 3.1 文档头

每篇 Blog 先填：

```markdown
## Blog Production Ledger

- Slug:
- Language:
- Content type:
- Funnel:
- Focus query:
- Reader:
- Expert angle:
- SERP page type:
- Planned H2 count:
- Target word range:
- Internal links (planned):
- Facts to verify:
- Status: [planning | drafting | reviewing | done]
```

### 3.2 每个 H2 的 Ledger 行

每个 H2 在动笔前必须登记以下字段。成稿后回填 `status` 和 `density`。

| 字段 | 说明 | 必填 |
|---|---|:---:|
| `h2` | 标题（应是微型结论，不是概念词） | ✓ |
| `judgment` | 本节核心判断（一句话） | ✓ |
| `mechanism` | 为什么成立 / 怎么运作 | ✓ |
| `example` | 具体场景、案例、数字、截图机会 | ✓ |
| `counterexample` | 反例、边界、不适用场景 | 对比/选型文必填 |
| `evidence` | 来源、测试方法、产品机制、限制 | ✓ |
| `visual` | 流程图 / 对比表 / 矩阵 / 截图 brief | 建议 |
| `cta_or_next` | 读者本节后应做什么 | ✓ |
| `serp_gap` | 相比 Top 页新增的认知 | 建议 |
| `status` | `planned` / `drafted` / `verified` | ✓ |
| `density` | `high` / `medium` / `low` | 成稿后填 |

**H2 密度门槛**：每个主要 H2 成稿后，`judgment`、`mechanism`、`example`、`evidence`、`cta_or_next` 五项中至少满足三项，且 `density` 不得为 `low`。

### 3.3 Blog Ledger 模板

```markdown
### H2 Ledger

| # | h2 | judgment | mechanism | example | counterexample | evidence | visual | cta_or_next | serp_gap | status | density |
|---:|---|---|---|---|---|---|---|---|---|---|---|
| 1 | | | | | | | | | | planned | |
| 2 | | | | | | | | | | planned | |

### Global Modules

| Module | Planned | Status | Notes |
|---|---|---|---|
| Opening hook | | planned | 非百科定义开头 |
| Reader promise | | planned | |
| FAQ (3-5) | | planned | 真实长尾问题 |
| E-E-A-T block | | planned | 经验/方法/来源/限制 |
| Lovart angle | | planned | 仅写已核实能力 |
| Internal links | | planned | 验证 slug |
| image_briefs | | planned | frontmatter，正文无占位符 |
| Closing next step | | planned | 非「未来可期」 |
```

### 3.4 Blog 类型附加要求

| 类型 | Ledger 额外字段 |
|---|---|
| Comparison | 每竞品一行：优势、劣势、适用人群、fair verdict |
| How-To | 每步骤：输入、操作、预期输出、常见错误 |
| Case Study | 背景、约束、做法、结果、可复用方法 |
| Glossary / Digest | 可省略 counterexample；每条需定义 + 使用场景 |
| Test / Review | `test_method` 列：怎么测、样本、限制 |

---

## 4. Landing / Page Ledger

### 4.1 文档头

```markdown
## Page Production Ledger

- Slug:
- Language:
- Category: [tool | feature | product | solution | scenario | topic]
- Storyline: [F/T/P/S/C/K/N + id]
- Focus query:
- SERP intent:
- Audience:
- Status: [planning | drafting | reviewing | done]
```

### 4.2 每个 Section 的 Ledger 行

Landing / Tools composite-v2 按 **section / module** 记账，不按 H2。

| 字段 | 说明 | 必填 |
|---|---|:---:|
| `section` | 模块名（hero / workflow / features / proof / faq / cta 等） | ✓ |
| `module_job` | 该模块要帮用户完成什么判断 | ✓ |
| `input` | 用户输入什么 | 工具页必填 |
| `output` | 用户得到什么 | 工具页必填 |
| `workflow` | 生成 → 编辑 → 导出路径 | 工具/功能页必填 |
| `proof` | 示例、规格、限制、商用说明 | ✓ |
| `cta` | 按钮文案与降低风险的副文案 | ✓ |
| `faq_items` | 本节关联的 FAQ 问题（可指向全局 FAQ） | FAQ 模块必填 |
| `seo_entities` | 要自然覆盖的实体词 / 同义词 | 建议 |
| `storyline_slot` | 对应 storyline 槽位 | ✓ |
| `status` | `planned` / `drafted` / `verified` | ✓ |

### 4.3 Page Ledger 模板

```markdown
### Section Ledger

| # | section | module_job | input | output | workflow | proof | cta | faq_items | seo_entities | storyline_slot | status |
|---:|---|---|---|---|---|---|---|---|---|---|---|
| 1 | hero | | | | | | | | | | planned |
| 2 | workflow | | | | | | | | | | planned |
| 3 | proof | | | | | | | | | | planned |
| 4 | faq | | | | | | | | | | planned |
| 5 | cta | | | | | | | | | | planned |

### Page Global Checks

| Check | Planned | Status |
|---|---|---|
| First screen answers query | | |
| Edit + export path named | | |
| ≥3 FAQ high-intent questions | | |
| No legacy section types (Tools v2) | | |
| Facts verified or [待考证] | | |
| i18n file `{slug}-{lang}.json` match | | |
```

### 4.4 Storyline 默认 Section 清单

按 storyline 预填 Ledger，避免漏模块：

| Storyline | 建议 section 顺序 |
|---|---|
| `T1` | hero → prompt/workflow → capabilities → proof → faq → cta |
| `T2` | hero → 3-step → output spec → faq → cta |
| `T4` | hero → comparison matrix → fair verdict → use cases → faq → cta |
| `T5` | hero → education blocks → examples → related tools → faq |
| `F7` | hero → agent workflow → capabilities → proof → faq → cta |
| `P1-P3` | hero → value prop → workflow → proof → pricing path → faq |

完整 storyline 定义见 `1-3 Content Gen/Page Gen/Refresh-Page/STORYLINES.md`。

---

## 5. i18n Ledger

本土化不是翻译任务，而是**按本地搜索意图重写**。每种语言单独一张 i18n Ledger。

### 5.1 i18n Ledger 模板

```markdown
## i18n Ledger — {lang}

- Source slug:
- Target file:
- Localization mode: [rewrite | adapt | light-touch]
- Local focus query:
- Status: [planned | drafting | reviewing | done]

| Field | Source (EN) | Local rewrite needed? | Local query / term | Status | Notes |
|---|---|---|---|---|---|
| title | | yes | | planned | |
| meta description | | yes | | planned | |
| hero / opening | | yes | | planned | |
| H2 / section titles | | yes | | planned | |
| examples / pain points | | yes | | planned | |
| CTA | | yes | | planned | |
| FAQ | | yes | | planned | |
| brand terms | Lovart / MCoT / ChatCanvas | consistent | | planned | |

### i18n BLOCK checks

- [ ] 非逐句直译
- [ ] 无 `(section_xx)` marker
- [ ] `zh-TW` 非简中繁转
- [ ] `ja` 无中文语序
- [ ] 文件名 `{slug}-{lang}` 与 `language` 字段一致
```

### 5.2 批量多语言规则

- 每批最多 3 种语言；每语言独立 Ledger 行。
- 禁止「先写 EN 成稿 → 一次翻译全部语言」而不更新各语言 Ledger。
- 若某语言搜索意图与 EN 不同（如 `ja` 更重流程、`de` 更重规格），在 `Local query / term` 列写明差异。

---

## 6. 长文防缩水检查（30 / 40 / 30）

成稿前将全文按篇幅分为三段，对比**信息密度**，不是比字数。

| 区段 | 篇幅 | 检查项 |
|---|---|---|
| 前 30% | 开头 + 前 1/3 主要模块 | 承接意图、建立读者、给出结构承诺 |
| 中 40% | 主体论证 / 工作流 / 对比 | 机制、例子、证据最密集区 |
| 后 30% | 收尾、FAQ、CTA、总结 | **不得低于前 30% 的密度** |

### 6.1 密度记分（每段 0-3）

每段各记：

| 分 | 信号 |
|---:|---|
| 0 | 空话、提纲、重复前文 |
| 1 | 有信息但缺例子或证据 |
| 2 | 有判断 + 例子或机制 |
| 3 | 判断 + 机制 + 例子/证据 + 行动价值 |

**及格线**：

- 后 30% 得分 ≥ 2。
- 后 30% 得分不得低于前 30% 得分。
- 中 40% 应是全文最高分区域（Blog 尤其如此）。

### 6.2 缩水 BLOCK 信号

触发任一项，必须回写，不得发布：

- 后 30% 只有「综上所述」「未来可期」「总之」类收束。
- 计划中的 H2 / section 有 `planned` 但未 `drafted`。
- FAQ 用模板问题凑数，未覆盖 SERP brief 中的真实异议。
- 后半 H2 全部 `density: low`。
- 续写后新增内容与 Ledger 计划严重偏离，且未回写 Ledger。

### 6.3 防缩水记录表

```markdown
## Shrinkage Check

| Segment | Word % | H2/section count | Density (0-3) | Thin modules | Action |
|---|---:|---:|---:|---|---|
| First 30% | | | | | |
| Middle 40% | | | | | |
| Last 30% | | | | | |

Verdict: [pass | rewrite last third | rewrite middle | full restructure]
```

---

## 7. 续写与中断规则

上下文将满、任务跨会话、或用户要求「继续写」时：

### 7.1 续写前（强制）

1. 读取完整 Ledger（不是对话摘要）。
2. 确认 `next_section` 与 `status` 列。
3. 回读上一节末尾 200-400 字或上一 section JSON。
4. 声明：`Resuming from Ledger section #N: {name}`。

### 7.2 禁止行为

- 禁止不读 Ledger 直接「接着上文写」。
- 禁止为省 token 跳过后半 section 或 H2。
- 禁止用「剩余内容类似前文」代替实际撰写。
- 禁止在续写时压缩已 `planned` 的模块为 bullet list。

### 7.3 分段生成顺序（Blog）

```text
1. SERP brief
2. Blog Ledger（全部 H2 先填 planned）
3. Opening + H2 #1
4. 更新 Ledger → H2 #2 … #N
5. FAQ + closing（独立一步，不并入上一 H2）
6. Shrinkage check
7. Rubric 评分
```

### 7.4 分段生成顺序（Page）

```text
1. SERP brief + storyline 选择
2. Page Ledger（按 storyline 预填 section）
3. hero + workflow（可合并为一批）
4. proof + capabilities
5. faq + cta（独立一批）
6. i18n Ledger（每语言）
7. Shrinkage check + preflight
```

---

## 8. Agent 输出格式

创作任务中，Agent 应在 SERP brief 之后、正文之前输出 Ledger 摘要：

```markdown
## Production Ledger Summary

- Content type: Blog | Page | i18n
- Total sections: N
- Next to write: {section name}
- Pending verification: [list]
- Shrinkage risk: low | medium | high

### Section status

| # | Name | Status | Density |
|---:|---|---|---|
| 1 | | planned | — |
```

成稿后附加：

```markdown
## Ledger Completion Report

- All planned sections drafted: yes/no
- Shrinkage check: pass/rewrite
- Unfinished items: [list]
- Ready for Rubric: yes/no
```

---

## 9. 与 Skills 的集成

| Skill | Ledger 要求 |
|---|---|
| `lovart-content-creation-orchestrator` | brief 后要求创建 Ledger |
| `lovart-blog-serp-writer` | 长文必须先出 H2 Ledger；Final QA 含 Shrinkage check |
| `lovart-page-serp-writer` | 按 storyline 填 Section Ledger；Tools v2 核对 global checks |
| `lovart-content-quality-gates` | CREATE 阶段检查 Ledger 是否存在；TRANSLATE 检查 i18n Ledger |
| `lovart-content-audit` | 深度审计时对照 Ledger 查漏项 |

---

## 10. 与 Rubric / Preflight 的关系

| 机制 | 作用 |
|---|---|
| **Ledger** | 生成中：防漏、防缩水、防失忆 |
| **Rubric** | 成稿后：判质量、给分、BLOCK |
| **Preflight** | 发布前：自动查结构、链接、文件名、占位符 |

Ledger 中可自动化的项（已映射见 [Preflight-Anti-Slop-Gates.md](./Preflight-Anti-Slop-Gates.md)）：

| Ledger 项 | 自动化方向 | 错误码 |
|---|---|---|
| planned vs drafted section 数 | 对比 outline 与成稿 heading | 待实现 |
| FAQ 数量 | section / heading count | `UX_FAQ` |
| 后 30% 字数比 | 分段密度启发式 | `AS_SHRINKAGE` |
| H2 下字数 / 例子 | 每 H2 词数、密度分 | `AS_THIN_H2` / `AS_LOW_DENSITY_H2` |
| i18n 文件名 | `--type tools` / `blog-i18n` | `I18N_FILENAME` |
| section marker | `grep section_` | `I18N_MARKER` |

运行：`1-1 Harness/Skills/lovart-content-quality-gates/scripts/anti-slop-preflight.js`

---

## 11. 快速示例（Blog H2 行）

| # | h2 | judgment | mechanism | example | evidence | cta_or_next | status |
|---:|---|---|---|---|---|---|---|
| 1 | 商业视频 AI 真正难的是一致性，不是第一次生成 | 品牌团队怕的不是生成慢，而是改一帧坏全片 | 多轮迭代中角色/产品/字幕漂移 | 电商 SKU 换色后口型与包装不同步 | Lovart Touch Edit + 分镜锁定；竞品多为单次生成 | 用自家 SKU 试一轮变体流程 | planned |

---

## 12. 维护说明

- Ledger 模板随 storyline、blog taxonomy 更新而更新。
- 样本库中的好稿应附带「成稿 Ledger」供复用。
- 上线后 CTR / 排名 / 转化反馈可回流到 Ledger 默认字段（如某类 page 的 FAQ 必答题）。
