---
type: research
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
status: active
---

# Landing Copy Benchmarks

> 第一版 benchmark 池。  
> 目的不是收集“好看页面”，而是为 Lovart 各类页面抽取可复用的承诺结构、proof 结构、workflow 结构、CTA 结构、FAQ objection 结构。

## 使用方法

每次生成页面前，先做：

1. 看 [`PAGE-BRIEF`](../../../1-3%20GenFlow/Page%20Gen/Refresh-Page/PAGE-BRIEF.md)
2. 确认页面类型
3. 到对应池里挑 2-3 个样本
4. 只抽结构，不抄原句
5. 最后按 [`Landing Copy Constraints SSOT`](../../../1-1%20Harness/Skills/02-creation/lovart-landing-page/references/landing-copy-constraints-ssot.md) 产出

所有样本统一用 [`BENCHMARK-TEMPLATE.md`](./BENCHMARK-TEMPLATE.md) 的 6 字段结构记录。

## Pool ↔ 故事线绑定

benchmark 池不是独立分类，而是每条故事线 copy 绑定里的 `benchmarkPool` 字段指向这里。对应关系：

| Pool | 绑定来源 | 故事线 |
|---|---|---|
| `landing` | `landing-storylines.json` | landing-gallery-detail / funnel / brand-trust / trial-now / vs-competitor / offer-close / full |
| `solution` | `solution-storylines.json` | solution-team / ecommerce / agency / enterprise / solo / mission |
| `scenario` | `scenarios-storylines.json` | scenarios-A … scenarios-reviews4（14 条） |
| `feature` | `page-copy-bindings.json` | features-主线 / tab-B / grid-feature / grid-bento6 |
| `tool` | `page-copy-bindings.json` | tools-A/B/tab-A/tab-B/grid-feature/grid-bento6 |
| `product` | `page-copy-bindings.json` | product-标准 / 含社会证明 / 视觉扩展-A/B |
| `topic` | `page-copy-bindings.json` | K1 / K2（关键词 topic-landing 混合页走 landing 池） |

写页面时：先拿故事线 → 读绑定的 `benchmarkPool` → 到对应池抽结构。

---

## Pool: `tool`

### 适用页面

- 具体生成器
- 单 job 工具页
- free / try-now / prompt-start 页面

### 第一批样本

1. **Looka AI Logo Generator**  
   URL: `https://looka.com/ai-logo-generator/`  
   取法：创始人工作流 + 3-step promise + ownership / file formats objection

2. **OpenArt AI Commercial Generator**  
   URL: `https://openart.ai/features/ai-commercial-generator/`  
   取法：product photo / script / prompt 到 commercial 的输入输出写法

3. **Topview Brand Video Maker**  
   URL: `https://www.topview.ai/make/brand-video-maker`  
   取法：material to video 的 result-first promise

4. **Creatify Marketing Video Maker**  
   URL: `https://creatify.ai/tools/marketing-video-maker`  
   取法：product URL、avatar、script、A/B test 的 workflow promise

5. **Canva AI Logo Generator**  
   URL: `https://www.canva.com/ai-logo-generator/`  
   取法：free / ease / ecosystem 结合，但只学结构，不学模板库路线

### Lovart 应学什么

- Hero 先卖 job，不先卖平台
- 工具页必须马上说清 input / output / trial path
- FAQ 要优先回答文件、格式、商用、上手门槛

---

## Pool: `feature`

### 适用页面

- 单点能力
- 技术差异点
- 需要 before/after 或 control narrative 的页

### 第一批样本

1. **Figma AI Design Generator**  
   URL: `https://www.figma.com/solutions/ai-design-generator/`  
   取法：生成后仍可控制的专业表达

2. **Ideogram Character**  
   URL: `https://ideogram.ai/features/character/`  
   取法：单一能力如何承诺清晰结果

3. **Kling AI Video Generator**  
   URL: `https://kling.ai/feature/en/ai-video-generator`  
   取法：技术 feature 如何直接翻译为 pain point benefit

4. **Lovart docs: How Lovart Works**  
   URL: `https://www.lovart.ai/docs/getting-started/how-lovart-works`  
   取法：内部 feature 页的工作流语言与可解释性

### Lovart 应学什么

- 单能力页必须回答“它解决哪一个 friction”
- 必须强调 control after generation
- before/after 和 limitation 比功能罗列更重要

---

## Pool: `product`

### 适用页面

- 产品线总览
- ChatCanvas / Brand Kit 这类产品层级页
- 含定价/协作/治理的页面

### 第一批样本

1. **Canva Magic Design**  
   URL: `https://www.canva.com/magic-design/`  
   取法：Broad product page 如何做 audience segmentation

2. **Runway Product Page**  
   URL: `https://runwayml.com/product`  
   取法：产品能力如何挂回更大 creative toolkit

3. **Adobe Express Create**  
   URL: `https://www.adobe.com/express/create`  
   取法：产品总览如何连接 editor、template、workflow

4. **Lovart AI Design Agent**  
   URL: `https://www.lovart.ai/features/ai-design-agent`  
   取法：内部现有 product-adjacent 页面可作为反面与正面样本，校正重复段和泛化表达

### Lovart 应学什么

- 产品页不能像工具页一样只卖一次点击
- 要解释产品在团队流程中的位置
- 需要 pricing / governance / collaboration / deliverable 逻辑

---

## Pool: `solution`

### 适用页面

- 团队级方案页
- 行业解决方案页
- 组合能力售卖页

### 第一批样本

1. **monday AI for Graphic Design**  
   URL: `https://monday.com/blog/ai-agents/ai-for-graphic-design/`  
   取法：workflow framing 与团队问题导向

2. **Creatify Marketing Video Maker**  
   URL: `https://creatify.ai/tools/marketing-video-maker`  
   取法：虽是 tool page，但可借其 marketing-team solution language

3. **Reeporter AI**  
   URL: `https://reeporter.ai/`  
   取法：从 product URL 到 full video workflow 的 solution-style promise

### Lovart 应学什么

- 先卖组织问题，再卖 feature
- 方案页要写 handoff、throughput、brand governance、multi-channel rollout
- CTA 更接近“see workflow / talk to team / start pilot”

---

## Pool: `scenario`

### 适用页面

- 按角色、行业、场景组织的页
- 例如电商、营销团队、代理商、创作者

### 第一批样本

1. **Prezent Canva Alternatives**  
   URL: `https://www.prezent.ai/blog/canva-alternatives`  
   取法：按 use case 窄化 intent，而不是广泛比工具

2. **Guideflow AI Design Tools**  
   URL: `https://www.guideflow.com/blog/ai-design-tools`  
   取法：best-for taxonomy，适合作为 scenario persona 抽法参考

3. **内部参考：landing-storylines audience 字段**  
   来源：`landing-storylines.json`  
   取法：`ecommerce-ops`、`agencies`、`brand-marketers`、`tool-keywords` 等 audience signals

### Lovart 应学什么

- 场景页要先写“这类人每天在卡什么”
- 不要一上来讲产品大全
- Hero 主语必须是角色/行业/工作周，而不是产品名

---

## Pool: `topic`

### 适用页面

- category education
- 概念解释
- model routing / workflow education

### 第一批样本

1. **Neolemon consistent character guide**  
   URL: `https://www.neolemon.com/blog/best-ai-character-generator-for-consistent-characters/`  
   取法：technical topic 如何通过 benchmark framework 建立可信度

2. **Neolemon image reference guide**  
   URL: `https://www.neolemon.com/blog/ai-image-generators-that-support-image-reference/`  
   取法：education-first problem framing

3. **Synthesia best AI video generators**  
   URL: `https://www.synthesia.io/post/best-ai-video-generators`  
   取法：tested listicle + criteria + decision support

4. **Venngage best AI ad generators**  
   URL: `https://venngage.com/blog/best-ai-ad-generator/`  
   取法：先交代测试标准，再讲 best-for

### Lovart 应学什么

- topic 页要有 decision framework
- 必须给读者“怎么选”的标准
- 列表页不能只做竞品导流，必须有 Lovart-fit narrative

---

## Pool: `landing`

### 适用页面

- paid landing
- conquest landing
- trial landing
- trust landing
- retarget offer landing

### 第一批样本

1. **内部 7 条 landing 故事线样本**  
   来源：`1-3 GenFlow/Page Gen/Refresh-Page/landing-examples/en/`  
   取法：直接抽 `landing-gallery-detail / funnel / brand-trust / trial-now / vs-competitor / offer-close / full`

2. **Looka AI Logo Generator**  
   URL: `https://looka.com/ai-logo-generator/`  
   取法：search-convert 承诺怎么写

3. **OpenArt AI Commercial Generator**  
   URL: `https://openart.ai/features/ai-commercial-generator/`  
   取法：commercial landing 的 input-output workflow

4. **Canva Magic Design**  
   URL: `https://www.canva.com/magic-design/`  
   取法：broad landing 的分流入口

### Lovart 应学什么

- landing 核心不是内容全，而是承诺精准
- trial / competitor / trust / offer 各有不同 CTA 逻辑
- `landing-full` 只能做内部 QA，不做真实投放 benchmark

---

## 下一轮补样优先级

优先补充顺序：

1. `tool`
2. `landing`
3. `feature`
4. `product`
5. `solution`
6. `scenario`
7. `topic`

原因：Lovart 当前最容易放大文案问题的是关键词工具页、投放 landing 和 feature/模型联动页。
