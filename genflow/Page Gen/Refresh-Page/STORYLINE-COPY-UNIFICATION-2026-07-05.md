---
type: architecture
version: 1.0
updated: 2026-07-05
scope:
  - tool
  - feature
  - product
  - solution
  - scenario
  - topic
  - landing
---

# 故事线为总纲：六维度统一（2026-07-05）

## 总纲

页面生成以**故事线**为总纲。选定故事线后，6 个维度全部从这一条故事线派生，不各写一套：

| 维度 | 从故事线派生的来源 |
|------|--------------------|
| 文案 | `copy` / `copyDefault`（landing/solution/scenarios）、`page-copy-bindings.json`（feature/tool/product/topic） |
| 模块 | 故事线 `sections`（`type` 顺序） |
| 个性化 | 故事线 `audience` + `intent` → Persona Matrix |
| 配图 | 故事线 `sections` + card title → `image_pool`（范围由模块集界定） |
| CRO | 故事线 `intent` + `ctaStyle`（intent→CRO 阶段见 `page-copy-bindings.json` `governedDimensions.croStageByIntent`） |
| 质检 | `COPY-PREFLIGHT.md`（storyline-driven）+ 质量门禁 |

本次先落地的是「文案 + 模块 + 质检」的机器闭环；个性化 / 配图 / CRO 目前以“从故事线字段派生”的契约固定下来（audience/intent/ctaStyle/sections 已在故事线里），后续如需脚本化可直接挂到同一注册表。

## 背景

文案能力层（copy SSOT + benchmark + copy preflight）是在故事线体系之后补的。补完后出现两套并行：

- 故事线只编码 **结构**（section 顺序）+ intent / audience / signals
- 文案层自带一套 intent 词汇（trial/competitor/brand-trust/offer/education）+ 硬编码的 preflight 假设

两者会各自漂移。本次把它们合并成**一套同源系统**。

## 统一后的架构

### 一个原则：结构与文案绑定同源

每条故事线既定义 section 顺序（结构），又携带 `copy` / `copyDefault` 绑定（文案）：

| 页面类型 | 结构 + 文案绑定所在 | 绑定形态 |
|---|---|---|
| landing | `landing-storylines.json` | 每条 storyline 内嵌 `copy` |
| solution | `solution-storylines.json` | 文件级 `copyDefault` |
| scenario | `scenarios-storylines.json` | 文件级 `copyDefault` |
| feature / tool / product / topic | `page-copy-bindings.json`（结构仍引用 `STORYLINE-BY-DIRECTION.md`） | 页面类型级 `copyDefault` |

### 绑定字段（copySchema）

`intent` · `copyIntentAliases` · `heroType` · `heroMust` · `requiredSections` · `proofTypes` · `ctaStyle` · `faqFocus` · `benchmarkPool`

### intent 以故事线为准

- master intent 词汇 + `intentCrosswalk` 集中在 `page-copy-bindings.json`
- 文案层的 5 类写作分类（trial/competitor/brand-trust/offer/education）通过 crosswalk 映射到 13 个 canonical intent
- 禁止在文案层自定义 intent，需扩展时改故事线绑定

### preflight 从绑定派生

`scripts/lib/landing-copy-rules.js` 启动时把 4 个 SSOT 合成一个 `storylineId → 绑定` 注册表（47 条），校验完全按绑定走：Hero 维度、proof、requiredSections、FAQ、CTA、禁用词；CTA 文案风格也由 `ctaStyle` 派生。

> 新增/调整任一故事线的文案要求 = 只改故事线绑定，脚本 + 文档自动跟随。

### schema 校验先于页面校验

`scripts/validate-storyline-schema.js` 是故事线绑定的守门脚本。它不检查页面文案好坏，只检查 SSOT 自身是否一致：

- 4 个 SSOT JSON 是否可解析
- `masterIntents` 与 `croStageByIntent` 是否一一覆盖
- `intentCrosswalk` 是否只引用合法 intent
- `copy` / `copyDefault` 是否包含必填字段
- `requiredSections` / `proofTypes` 是否与真实 `sections` 对齐
- `heroType` 是否匹配首段 section
- `sectionCount` 是否匹配 `sections.length`
- alias 是否指向存在的故事线

固定运行方式：

```bash
node "genflow/Page Gen/Refresh-Page/scripts/validate-storyline-schema.js"
```

## 迭代规则（防再次漂移）

1. 改**结构**（section 顺序）→ 改对应 storyline JSON 的 `sections`（features/tools/product/topic 改 `STORYLINE-BY-DIRECTION.md`）
2. 改**文案要求**（proof/cta/faq/required）→ 改同一条故事线的 `copy` / `copyDefault`
3. 改 **intent 词汇** → 改 `page-copy-bindings.json` 的 `masterIntents` + `intentCrosswalk`
4. 三者永远在故事线这一层对齐，不在 skill 里另写一套

## 验证（2026-07-05）

| 项 | 结果 |
|---|---|
| 4 个 SSOT + 2 个 manifest JSON 合法 | ✅ |
| Storyline schema validator | ✅ landing 7 / solution 6 / scenario 14 / pageBindingOnly 16 |
| 注册表解析（含 landing/solution/scenario/feature/tool/product/topic + 别名） | 47 条绑定，0 缺失 |
| landing 结构完好 | 7 条（12×6 + 15） |
| landing-examples preflight | 7 / 7 通过，0 错 0 警 |
| keyword-examples preflight | 41 / 41 通过，0 错 0 警 |

## 相关文件

- `landing-storylines.json` / `solution-storylines.json` / `scenarios-storylines.json` / `page-copy-bindings.json`
- `scripts/validate-storyline-schema.js`
- `scripts/lib/landing-copy-rules.js`
- `COPY-PREFLIGHT.md`
- `STORYLINE-BY-DIRECTION.md`
- `harness/Skills/02-creation/lovart-landing-page/references/landing-copy-constraints-ssot.md`
