---
name: page-copy-optimizer
description: >-
  专门优化已存在的 Lovart Tools、Features、Product、Solution、Scenario、Topic 与投放页文案。
  当用户要求“优化页面文案”“提升落地页转化”“重写 Hero/CTA/FAQ”“根据 SERP 或竞品改现有页面”
  “诊断页面为什么不转化”“让图文和 CTA 协同”时必须使用。只优化已有页面，不新建页面、不生成图片、
  不批量翻译、不发布 Sanity；需要这些能力时将明确路由给对应 Skill。
---

# Page Copy Optimizer

## 解决什么，不解决什么

本 Skill 的工作是让**已有页面**的承诺、文案、证据、CTA、FAQ 和视觉角色服务同一个用户任务。
它专注“诊断 → 最小必要改写 → 可审计验证”，避免通用 landing-writer 在页面创建、结构、图片、发布、
本地化等任务之间切换时，把存量优化退化成泛泛重写。

页面不是只在详情页被阅读。凡是页面会出现在 Tool/Feature/Blog/搜索结果/站内推荐列表中，页面的**列表标题与描述**也是独立的转化界面：用户需要在相邻卡片中快速判断任务、结果与适配性。

## 不可颠倒的四层决策顺序

任何改写都按以下顺序做决定。后层不能推翻前层，尤其 SERP 不能让页面承诺超出 Lovart 已验证能力。

1. **页面主题**：这页承接的用户任务、页面类型、storyline 与 primary keyword 是什么？主题不清时先诊断路由，不润色句子。
2. **模块 CRO**：Hero、proof、workflow、CTA、FAQ 各自推动用户从理解到行动的哪一步？先修模块职责和顺序中的缺口，再写具体 copy。
3. **SERP 参考**：SERP 用来识别用户意图、常见承诺、竞争异议与可占据差异；不复制竞品句子，也不把竞品功能变成 Lovart 承诺。
4. **Lovart 知识库红线**：最终所有产品事实、官方术语、能力边界、模型、输入/输出、格式、价格、权利、限制和竞品结论均必须可在 Lovart 知识库追溯。无法验证就删除、降级为问题，或标记 `[待考证]`；不得以“转化需要”为理由补写。

| 本 Skill 负责 | 不负责；改走 |
|---|---|
| 既有页面的 Hero、section、CTA、FAQ、SEO copy 诊断与改写 | 新页面类型/故事线/JSON 骨架：`landing-writer` |
| SERP 意图、竞品承诺、页面差异化与 copy 对齐 | 关键词选题、数据拉取：strategy/data Skill |
| 图文 CTA 叙事协同与 CRO 假设 | 生成/上传/替换图片：`lovart-batch-cover-production`（P0 前仅输出 brief） |
| 模块级 copy diff、事实台账、验收清单 | Sanity patch/import：`sanity-publish` |
| canonical copy 的本地化 brief | 多语言实际翻译：对应 locale writer，例如 `ja-copywriter` |

**不要**为了“更像新页面”而改 page category、storyline、section type 或把整个 `bodyJson` 重建。发现问题根源是结构、图片、性能、产品能力或流量质量时，输出升级建议并停在 copy 边界。

## 必须读取的上下文

开始前，按任务所涉范围读取：

1. [`../landing-writer/SKILL.md`](../landing-writer/SKILL.md)：页面意图、故事线、页面类型和已验证产品术语。
2. [`../landing-writer/references/page-copy-serp.md`](../landing-writer/references/page-copy-serp.md)：SERP、proof、CTA、FAQ 的基础规则。
3. [`../landing-writer/references/landing-ssot/landing-copy-constraints-ssot.md`](../landing-writer/references/landing-ssot/landing-copy-constraints-ssot.md)：页面 7 要素、禁用模式、按类型的差异。
4. [`../../../../insight-data/存量改造/B2-页面兼容性与CRO验收规范-2026-10-21.md`](../../../../insight-data/存量改造/B2-页面兼容性与CRO验收规范-2026-10-21.md)：图、标题、CTA 的关系；仅在页面存在图片时读取。
5. [`../../../../insight-data/存量改造/B2-SERP竞品视觉研究与批次准入规范-2026-10-21.md`](../../../../insight-data/存量改造/B2-SERP竞品视觉研究与批次准入规范-2026-10-21.md)：仅在用户要求 SERP/竞品驱动优化时读取。
6. [`references/scorecard.md`](references/scorecard.md)：输出与验收格式。
7. 日语页面必须读取 [`../ja-copywriter/SKILL.md`](../ja-copywriter/SKILL.md)；其他语言如有对应 locale Skill，同样先读取。优化 canonical 文案不能替代目标市场的本地化审校。
8. [`references/lovart-knowledge-redline.md`](references/lovart-knowledge-redline.md)：事实检索优先级、冲突处理与事实台账格式。

如果页面没有可信的 page source、目标关键词/意图、目标语言或已验证产品事实，先说明缺口。可以做“诊断草案”，但不得编造能力、导出格式、价格、数据、客户或竞品结论。

## 输入契约

每次至少取得下列信息；缺项按处理方式执行：

| 输入 | 必填 | 缺失时 |
|---|---|---|
| 页面 source（线上 URL、Sanity 文档或 bodyJson/JSON） | 是 | 不改写，只给输入清单 |
| 页面类型与现有 storyline | 是 | 从 source 推断并标为“待确认”；不擅自改结构 |
| primary keyword / 目标意图 | 是 | 从 title/slug 提出一个候选并要求确认 |
| target language / market | 是 | 从 `language` 读取；未提供时默认 source 的语言 |
| 已验证产品事实与限制 | 是 | 事实未知处标 `[待考证]`，不以营销话术补齐 |
| SERP/竞品 brief | SERP 驱动任务必填 | 只做内部 copy 卫生，不声称竞争差异 |
| 图片 slot / 截图 | 有 Hero/视觉协同时必填 | 只输出图文风险，不改图片或假设布局 |
| 列表上下文（卡片 title/description、排序、相邻卡片、截断规则） | 列表体验审核必填 | 不评价“靠前卡片”的体验；先请求列表快照或导出 |
| 指标基线（CTR、CTA CTR 等） | 实验任务必填 | 写转化假设，不做效果承诺 |

## 工作流

### 1. 先诊断，不先改

建立 `Copy Diagnosis`，逐项给出证据和严重级别：

1. **页面主题**：页面是否在首屏回答该查询/用户任务，且 category/storyline 没有错路由？
2. **模块 CRO**：Hero、proof、workflow、CTA、FAQ 是否各自承担了推进理解、降低风险或促进行动的职责？
3. **SERP 参考**：用户意图、竞争承诺和异议是否被引用为参考，而不是照抄或越界承诺？
4. **承诺**：是否具体说明 buyer、input、output、edit path、risk reducer？
5. **信息气味**：用户能否在 3 秒内判断“这是给谁、能做什么、下一步是什么”？
6. **图文**：图解释机制/结果，还是只做漂亮背景？是否与 CTA 抢注意力？
7. **列表体验**：卡片标题是否说明具体任务而非裸关键词？描述是否补充结果/适配人群，而非复述标题？在相邻前 30 卡中是否可区分、可扫描、不会被截断成半句？
8. **Lovart 知识库红线**：是否有不受支持的能力、术语、格式、价格、权利、数据、竞品结论或直译腔？

用 `references/scorecard.md` 打分。分数是排优先级工具，不是“改完就一定转化”的保证。

### 2. 决定最小改写范围

按影响优先级修改，默认不超过必要模块：

1. page promise / Hero；
2. 首个 proof 或 workflow section；
3. primary CTA 与 CTA 附近 risk reducer；
4. FAQ 异议；
5. section 标题、描述、SEO title/description。

以下情况**不靠文案硬修**，写为升级建议：

- 该任务没有可验证产品能力或 proof；
- 模块顺序与 intent 根本不匹配；
- 图片比例/裁切/加载性能破坏首屏；
- CTA 指向不可用流程；
- 关键词应路由到不同页面类型。

### 3. 写出页面文案契约

在输出前先写一段简短的 `Copy Contract`：

```text
Audience:
Primary job:
Input → output:
Lovart edit/control path:
Verified proof:
Risk reducer:
Primary CTA:
SERP differentiation:
Image role:
Do-not-claim:
```

每一项必须能在页面 source、已验证事实或 SERP brief 中追溯。`Do-not-claim` 用来防止因模仿竞品而虚构功能。

### 4. 模块级改写

对每个修改模块输出：

```text
section/index:
existing issue:
replacement copy:
why this change:
fact source / [待考证]:
image/CTA dependency:
```

规则：

- Hero 至少包含 subject、buyer、input/output、risk reducer 中 4 项，且不超过一个主承诺。
- 一页一个转换动作。图片讲机制/结果，标题讲价值，CTA 讲下一步。
- proof 紧跟承诺。没有证据时，降低绝对化承诺，不用形容词填充。
- CTA 是动作语句，不是泛口号；语气匹配 query intent。
- FAQ 回答商用/输入输出/编辑控制/适配边界/替代方案等真实异议。
- 只在已有事实支持时保留模型名、格式、速度、价格、权利与数据。

### 5. 输出可执行交付包

始终按以下结构交付：

```markdown
# Copy Optimization Package — {slug}
## Scope and non-goals
## Copy Diagnosis
## Copy Contract
## Prioritized changes
## Section-by-section copy diff
## Listing title and description diff
## Image / CTA compatibility notes
## Fact ledger
## CRO hypothesis and measurement
## Preflight checklist
## Escalations
```

如果需要把改动写回 JSON，另输出最小 field-level patch 草稿；不在本 Skill 内发布。

### 6. 交付前验证

- 对照 scorecard，Hero、proof、CTA、FAQ、事实项全部有结论。
- 页面出现在列表中时，审核 title + card description 的完整显示、相邻差异与目标语言可读性；没有列表上下文时明确标为未审，而不是假定详情页 title 可直接复用。
- 无抽象 AI 空话、无虚构数据、无无依据竞品结论。
- 文案变更未改变页面类型、storyline、section type 或 URL。
- 有图片时，完成 3 秒、5 秒、CTA 注意力与桌面/移动裁切检查。
- 明确建议的 preflight 命令；发布走 `sanity-publish`。

## 输出模式

| 用户需求 | 输出 |
|---|---|
| “这页为什么不转化” | Diagnosis + 优先级 + 需要的数据，不盲目重写 |
| “改 Hero/CTA/FAQ” | Copy Contract + 精确模块 diff |
| “按 SERP/竞品优化” | 含 SERP differentiation 与 do-not-claim 的完整交付包 |
| “整页重写” | 仍按现有 section 顺序逐段替换；若结构应变，升级给 `landing-writer` |
| “日语/其他本地化页面” | 先优化 canonical 意图，再输出本地化 brief；实际语言稿交给对应 locale writer |

## 列表前 30 混合抽样（服务器执行）

用户要求审核“列表页靠前页面”时，不只按流量或只按前端顺序。使用本 Skill 自带的选择器：

```bash
python3 "harness/Skills/02-creation/page-copy-optimizer/scripts/select_list_copy_audit.py" \
  --pages run/list-copy-audit/pages.jsonl \
  --traffic run/list-copy-audit/traffic.csv \
  --out-dir run/list-copy-audit/selected
```

输入约定：

- `pages.jsonl`：全量 CMS 导出；每行至少有 `doc_id`（或 `_id`）、`page_type`、`language`、`slug`、`title`、`description`、`listing_rank`。
- `traffic.csv`：`doc_id,impressions,clicks`；若无 `doc_id`，使用 `page_type,language,slug` 匹配。

脚本对每个 `page_type × language` 取 **列表当前前 30 ∪ 流量/曝光前 30**，去重后输出 `candidates.jsonl`。它只标结构性风险（缺失、重复、疑似裸关键词、描述复述标题、可能截断），不能替代本 Skill 的逐页主题、CRO、SERP 和知识库审核。

若 `listing_rank` 不来自真实前端列表排序，或卡片宽度/截断规则未知，报告必须明确“列表体验未完成验证”。

## 质量边界

- 不把 CTR、CVR、SEO 排名或转化提升写成保证；它们是待验证假设。
- 不复制竞品语句、结构细节或视觉承诺；只提炼其页面的承诺结构与用户异议。
- 不为配合图片而弱化页面真实承诺；图片与文案冲突时先修叙事或 slot。
- 不把“更短”误认为“更好”；删掉的是无信息修辞，保留的是 input、output、proof 和边界。
- **知识库红线优先于 CRO**：任何一句未被 Lovart 知识库支持的“更有转化力”的话，都不能进入 replacement copy。

## 标题（TDK title）长度与结构

- 长度 55–60 字符（60 为硬上限）；CJK 按 ≤30 字控制；低于 45 字的标题视为“信息量不足”，不得作为 replacement。
- 结构三选一：失败/痛点直述、反常识纠正、数字+场景；禁止「主题: 承诺」两词组模具与空泛形容词。
- 必须具备一个具体失败点或场景（Merchant Center、clip four、thumbnail size、RSVP）+ 一个动作或判断；seo.title 与 title 同值。
- 详细规则与示例见 harness/Skills/02-creation/landing-writer/SKILL.md 的「标题标准（55–60 字）」。
- 写回前用 preflight_tdk_i18n.title_reasons + 长度校验；禁止字符截断。
