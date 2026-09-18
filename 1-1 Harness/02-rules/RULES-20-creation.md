---
type: rule/creation
version: 2.0
updated: 2026-09-18
scope: "profile-lovart-creation"
tools: [mflow, agent]
status: active
path: 1-1 Harness/02-rules/RULES-20-creation.md
---
# RULES 20 — 创作类（Creation）

> 适用路线：Blog 创作、Features/Tools/Solution/Product/Scenario/Landing/Topic 落地页
> 加载 Profile：`lovart-creation`

## 一、硬条款（违反即 BLOCK）

1. **必须**以故事线为总纲：页面生成前先选定故事线，以下 6 个维度全部以该故事线为准
2. **禁止**绕开故事线自定义 intent、模块序列或文案要求
3. **禁止**在 skill 里另写一套与故事线冲突的规则
4. **必须**按执行顺序：`PAGE-BRIEF → 选故事线 → 读该故事线全维度绑定 → 生成 → COPY-PREFLIGHT`
5. **必须**使用 6 维绑定：文案/模块/个性化/配图/CRO/质检全部以故事线为准
6. **禁止**在文章正文出现 IMAGE PLACEHOLDER 或 [REAL SCREENSHOT REQUIRED]
7. **必须**每个 Blog 至少 1 个可引用的观点句（金句）
8. **必须**每 500 字至少 1 个 H2
9. **禁止** slug 使用下划线 `_`（必须 kebab-case）
10. **必须** Blog `body` 为 Portable Text 数组（AB-LP22）
11. **禁止** `seo.structuredData.json` 为空（AB-LP23）
12. **必须**多语言版本语义等价：数据点与结论跨语言一致
13. **禁止**某语言版本字数 < 其他版本 60%（视为未完成）
14. **必须**引用外部权威来源 ≥2 条（完整 URL）
15. **禁止**编造产品数据/竞品数据；不确定的数字标 `[待考证]`
16. **必须**遵循 RULES-70 数量预算与 RULES-80 语言规范

## 二、机器检查映射

| 硬条款 | 检查钩子 |
|--------|---------|
| #1-5 故事线 | pipeline_state.py advance |
| #6 占位符 | post-write-check.sh |
| #7 金句 | content-quality-gates |
| #8 H2 密度 | post-write-check.sh |
| #16 预算/语言 | quota-check.sh + lang-check.sh |

## 三、故事线 6 维绑定

| 维度 | 来源 |
|------|------|
| 文案 | landing/solution/scenarios JSON 的 `copy`/`copyDefault`；feature/tool/product/topic 见 `page-copy-bindings.json` |
| 模块 | 故事线 `sections`（`type` 顺序） |
| 个性化 | 故事线 `audience` + `intent` → Persona Matrix |
| 配图 | 故事线 `sections` + card title → `image_pool` |
| CRO | 故事线 `intent` + `ctaStyle` → 流量阶段 / CTA / 紧迫感 |
| 质检 | `COPY-PREFLIGHT`（storyline-driven）+ 质量门禁 |

**迭代方法**：改故事线绑定（结构改 `sections`；文案改 `copy`；intent 改 `page-copy-bindings.json`）→ 脚本与文档自动跟随。

## 四、参数表

### 机器约定
见 `page-copy-bindings.json` 的 `governedDimensions`；权威结构见 `STORYLINE-BY-DIRECTION.md`。

### Blog 子技能映射

| 内容类型 | Skill |
|---------|-------|
| Getting Started / 101 | lovart-101 |
| Best Practice | lovart-best-practice |
| Complete Guide | lovart-complete-guide |
| Review / Roundup | lovart-review |
| Stack × Stack | lovart-stack-by-stack |
| Insight & Trend | lovart-insight-trend |
| Thought Leadership | lovart-thought-leadership |
| SERP 驱动 Blog | lovart-blog-serp-writer |
| 舆情驱动 Blog | lovart-blog-signal-writer |
| Blog 全流程 | lovart-blog-automation |

### 落地页子技能

| 页面类型 | 生成 skill | 发布 skill |
|---------|-----------|-----------|
| Tools | lovart-landing-page | lovart-tools-sanity-publish |
| Features | lovart-landing-page | lovart-features-sanity-publish |
| Products | lovart-landing-page（泛化） | lovart-product-sanity-publish |
| Scenarios | lovart-landing-page（泛化） | lovart-scenarios-sanity-publish |
| Topics | lovart-landing-page（泛化） | — 缺 |
| Solutions | lovart-landing-page（泛化） | — 缺 |
| Landing Page（投放） | lovart-landing-page | — |
