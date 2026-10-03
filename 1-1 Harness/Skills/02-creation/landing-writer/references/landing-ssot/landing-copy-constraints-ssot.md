---
type: reference
version: 1.0
updated: 2026-07-05
owner: lovart-landing-page
scope:
  - tool
  - feature
  - product
  - solution
  - scenario
  - topic
  - landing
---

# Landing Copy Constraints SSOT

> 这是 Lovart 落地页文案的人类可读 SSOT（“这页该怎么说”）。  
> **机器可读 SSOT = 故事线里的 copy 绑定**：`landing-storylines.json`（内嵌 `copy`）、`solution-storylines.json` / `scenarios-storylines.json`（`copyDefault`）、`page-copy-bindings.json`（feature/tool/product/topic）。  
> **结构 = 故事线本身**：`STORYLINE-BY-DIRECTION.md` + 各 storyline JSON。  
> 三者关系：结构（section 顺序）与文案绑定（intent/hero/proof/cta/faq）**同源存放在故事线里**；本文件解释绑定背后的写作意图；`COPY-PREFLIGHT` 脚本从故事线绑定**派生**校验，不再硬编码。

---

## 0. 使用顺序

所有 `tool / feature / product / solution / scenario / topic / landing` 页面都按这个顺序执行：

1. 先做 [`PAGE-BRIEF`](../../../../../1-3%20GenFlow/Page%20Gen/Refresh-Page/PAGE-BRIEF.md)
2. 再定 `category` 和故事线（故事线 ID 即文案绑定的 key）
3. 读该故事线的 copy 绑定（landing/solution/scenario 在各自 JSON；feature/tool/product/topic 在 `page-copy-bindings.json`）
4. 再查 benchmark 池：[`Landing Copy Benchmarks`](../../../../../1-2%20Insight/Keywords%20Research/Landing%20Copy%20Benchmarks/README.md)
5. 最后写 copy，并过 [`COPY-PREFLIGHT`](../../../../../1-3%20GenFlow/Page%20Gen/Refresh-Page/COPY-PREFLIGHT.md)

禁止跳过 Brief 直接写 Hero；禁止绕开故事线绑定自定义 intent。

---

## 1. 页面级硬约束

每一页必须同时说清 7 件事，缺一不可：

1. **Buyer / audience**：谁会读，谁会买，谁会执行
2. **Input**：用户拿什么开始，例：prompt、product URL、image、script、brief、reference、brand kit
3. **Output**：用户最后拿到什么，例：logo、PDP visual、commercial、brand video、social pack、export format
4. **Edit path**：生成后怎么改，例：ChatCanvas、Touch Edit、Text Edit、Edit Elements、review loop
5. **Proof**：为什么可信，例：workflow、example、output spec、limitation、format、rights、testimonial、benchmark
6. **CTA**：下一步动作是什么，而且必须和流量阶段匹配
7. **FAQ / objection**：至少回答 3 个高意图问题，而不是泛百科问答

如果页面只讲“Lovart 很强”，但没有 input/output/edit path/proof，这页就是不合格。

---

## 2. Hero 公式

Hero 不能只是抽象 slogan，必须同时覆盖以下 5 项中的至少 4 项：

- **主语**：这页卖的是工具、产品、场景、方案还是整个平台
- **输入**：用户从什么开始
- **输出**：最终产物是什么
- **风险降低点**：free trial、no credit card、commercial-ready、editable、brand-safe、faster than agency handoff
- **目标读者**：为谁而做

### Hero 最小模板

```text
[Primary keyword / page promise]
for [buyer]
from [input]
to [output]
with [risk reducer]
```

### 合格示例

- `AI Logo Generator for founders — from a business brief to editable brand assets, with Brand Kit and export-ready files.`
- `Product video for ecommerce teams — turn PDP stills and product briefs into hooks, demos and retarget cuts without resetting brand context.`

### 不合格示例

- `Design the future with AI`
- `Powerful AI creativity for everyone`
- `Generate amazing content faster`

---

## 3. Section 职责

### Workflow / process 段

必须写清：

- 用户先做什么
- AI 自动做什么
- 人还能改什么
- 最后产物如何进入真实使用场景

禁止把 workflow 写成纯功能列表。

### Comparison 段

必须比较：

- workflow 差异
- editability 差异
- brand continuity 差异
- use-case fit 差异

禁止只写“更快、更强、更便宜”。

### Proof 段

至少要出现以下之一：

- 明确 deliverable
- 明确 export / format / rights
- 明确 before/after
- 明确 use-case
- 明确 limitation / 适用边界
- 明确 testimonial / review / benchmark framework

Logo wall 不是充分 proof，只能算弱信号。

### FAQ 段

FAQ 必须回答高意图异议：

- 能不能商用
- 适不适合我的行业/团队
- 与某类替代方案相比差在哪
- 是否支持某种输入/输出/编辑路径
- 是否能和现有流程衔接

FAQ 不要写成“什么是 Lovart”“为什么选择我们”这种弱问题。

### CTA 段

CTA 必须对应流量阶段：

- 冷流量：降低风险，如 `Start free` / `No credit card`
- 搜索高意图：直接试用或进入 prompt
- 竞品对比：强调切换收益或 workflow clarity
- Retarget / offer：强调限时、权益、升级理由

禁止所有页面都用同一句 CTA。

---

## 4. 禁用文案模式

以下内容默认禁止：

- 抽象 AI 空话：`AI-powered creativity`, `unlock your workflow`, `revolutionize design`
- 没有来源的数字：用户数、效率倍数、收入提升、时间缩短
- 模板化 CTA：所有页面都 `Start creating now`
- 竞品拉踩：用情绪化语气说对手“不行”
- 假社会证明：编造 logo、客户、媒体背书、评分
- 只讲技术参数，不翻译成用户收益
- 把所有页面写成同一种“平台介绍”

---

## 5. Proof 层级

文案中可用的 proof 强弱如下：

### 强 proof

- 官方文档已验证的功能、格式、流程
- 页面内明确示例与 deliverable
- 真实流程前后对比
- 已验证的 pricing / rights / export format

### 中 proof

- test criteria
- best-for decision rules
- 结构化 benchmark 总结
- verified testimonials

### 弱 proof

- logo loop
- generic reviews
- “trusted by creators” 一类泛句

弱 proof 不能单独承担整页可信度。

---

## 6. 页面类型差异

### `tool`

- 核心承诺：立刻完成一个具体 job
- 必须出现：input、output、prompt/trial path、FAQ、single-job proof
- 不应写成平台总览

### `feature`

- 核心承诺：一个能力解决一个明确 friction
- 必须出现：before/after、edit/control、与相邻 feature 的边界
- 不应写成产品总目录

### `product`

- 核心承诺：产品线为什么值得团队采买或长期使用
- 必须出现：role of the product、how it fits workflow、proof、pricing or adoption logic（若结构允许）
- 不应写成具体职业场景指南

### `solution`

- 核心承诺：一整套组织级方案如何替代碎片化流程
- 必须出现：buyer、team workflow、handoff reduction、governance、proof
- 不应写成单功能介绍

### `scenario`

- 核心承诺：这个角色 / 行业 / 场景怎么用 Lovart
- 必须出现：day-in-the-life problem、workflow fit、deliverables、objections
- 不应塞 pricing、tool-grid、trial-heavy 结构

### `topic`

- 核心承诺：解释一个更广的概念、品类或方法
- 必须出现：education、decision framework、internal links、FAQ
- 不应伪装成 narrow tool page

### `landing`

- 核心承诺：围绕流量意图做转化
- 必须出现：与故事线匹配的 Hero、proof、CTA、FAQ
- 不应混成全平台百科页，除非是 `landing-full` 内部 demo

---

## 7. Intent 到 copy emphasis 的映射

> **intent 以故事线为准。** 下面 5 个是本文件的写作分类；每一类通过 `intentCrosswalk` 映射到故事线的 canonical intent（见 `page-copy-bindings.json` 的 `masterIntents` + `intentCrosswalk`）。写作时先看故事线 intent，再套对应 emphasis。

| 本文件写作分类 | 映射到的故事线 canonical intent | 典型故事线 |
|---|---|---|
| trial | `search-convert`、`tool-activation` | `landing-trial-now`、`tools-*` |
| competitor | `competitor-conquest` | `landing-vs-competitor` |
| brand-trust | `brand-upper-funnel` | `landing-brand-trust` |
| offer | `retarget-offer` | `landing-offer-close` |
| education | `acquire-broad`、`acquire-educate`、`solution-consideration`、`scenario-education`、`feature-adoption`、`product-consideration`、`topic-education` | gallery-*、solution-*、scenarios-*、features-*、product-*、K1/K2 |

### trial（search-convert / tool-activation）

- Hero 强调 input/output/risk reducer
- 中段要有 `prompt-launcher` 或明确 start path
- FAQ 优先回答上手门槛、格式、是否可试

### competitor（competitor-conquest）

- Hero 强调 switch reason
- 中段必须有 comparison or before/after
- FAQ 优先回答迁移、替代路径、与竞品的真实差异

### brand-trust（brand-upper-funnel）

- Hero 强调品牌级结果，而不是单 job
- 中段加 testimonial / logo / campaign continuity
- FAQ 优先回答团队适配、品牌一致性、流程协同

### offer（retarget-offer）

- Hero 强调 offer + why now
- 中段减少教育，强化 proof、pricing、review、bottom CTA
- FAQ 聚焦权益、升级、风险

### education（acquire-* / solution / scenario / feature / product / topic）

- Hero 不强卖，先定范围（承诺按具体页面类型收窄，见 §6）
- 中段给 decision framework、workflow、internal links
- FAQ 回答选择逻辑与适用边界
- 具体到 solution/scenario/product 时，emphasis 收窄为对应页面类型的承诺

---

## 8. Benchmark 抽样模板

每个 benchmark 样本只抽这 6 个字段：

1. `page promise`
2. `hero formula`
3. `proof shape`
4. `workflow shape`
5. `cta shape`
6. `faq objection shape`

不要抄原句，只总结结构。

---

## 9. Copy Preflight 入口

正式输出前必须过：

- [`COPY-PREFLIGHT.md`](../../../../../1-3%20GenFlow/Page%20Gen/Refresh-Page/COPY-PREFLIGHT.md)

如果 preflight 过不了，优先改 page promise / Hero / proof / CTA / FAQ，而不是先改修辞。
