# Content Quality Rubric — Anti-Slop 评分标准

> 用途：把 Anti-Slop 从“写作原则”变成可评分、可门禁、可复盘的质量标准。  
> 上游：[Anti-Slop.md](./Anti-Slop.md)  
> 下游：[Quality-Gates.md](./Quality-Gates.md)、`lovart-content-quality-gates`、内容样本库、上线后反馈闭环

---

## 1. 判定原则

内容质量不按“是否像人写”打分，而按是否完成页面任务打分。

每次评审必须先判断内容类型：

- Blog
- Landing Page / Tools / Features / compositePage
- Product Copy
- SEO / Programmatic Page
- i18n / Localization

总分 100 分，但 BLOCK 条件优先级高于分数。触发 BLOCK 时，即使分数超过 80，也不得发布。

---

## 2. 通用评分表（100 分）

| 维度 | 分值 | 满分标准 | 低分信号 |
|---|---:|---|---|
| 读者与场景 | 15 | 明确读者角色、意图、决策阶段和使用场景 | 写给“所有人”；只有泛泛痛点 |
| SERP / 搜索意图对齐 | 15 | 首屏或开头准确回答 query intent；页面类型正确 | 工具词写成科普；对比词写成品牌自夸 |
| 信息密度 | 15 | 每个主要段落都有判断、机制、例子、证据或行动价值 | 大段空话；删除一段不影响理解 |
| 证据与可信度 | 15 | 有事实来源、产品机制、案例、截图、测试、限制说明 | “领先/革命性/10x”无来源 |
| 转化与下一步 | 10 | CTA、FAQ、内链和转化阻力匹配上下文 | CTA 可以放在任何 SaaS 页面 |
| 结构与浏览体验 | 10 | 标题层级清晰；H2 是微型结论；段落节奏自然 | H2 全是概念名；结构像模板 |
| Anti-slop 语言质量 | 10 | 具体、自然、不过度术语化也不过度白话 | unlock / seamless / empower / 赋能 / 闭环堆叠 |
| 本土化 / 语言适配 | 5 | 语言、例子、搜索词、CTA 本地化 | 逐句翻译；简中污染繁中；英语句式污染日语 |
| 完整性 / 防缩水 | 5 | 后半质量不低于前半；计划模块完整 | 后半变提纲；FAQ/Proof/CTA 被省略 |

### 分数解释

| 分数 | 处理 |
|---:|---|
| 90-100 | 可发布；只需轻微编辑 |
| 80-89 | 可进入最终人工审校；不得跳过事实检查 |
| 70-79 | 需要重写薄弱维度后再审 |
| 60-69 | 不建议发布；需要结构性改写 |
| <60 | 视为 AI slop 草稿，重做 brief 和结构 |

---

## 3. BLOCK 条件

触发任一项即不可发布：

- 编造产品能力、价格、模型支持、导出格式、集成、用户数据或竞品数据。
- 可见 `IMAGE PLACEHOLDER`、`[IMAGE N PLACEHOLDER]`、`section_xx` 翻译 marker。
- Blog / SEO 页面没有明确读者和搜索意图。
- Landing / Tool 页面首屏没有说明输入、输出和下一步。
- 对比页只踩竞品，没有 fair verdict 和适用场景。
- 多语言版本明显逐句直译，或 `zh` / `zh-TW` / `ja` 语言污染严重。
- 长文后 30% 明显缩水，只剩总结、泛泛建议或 FAQ 填充。
- 内链使用坏路径：`/博客文章/`、`/cluster/`、`.md)`、`](#)`、`](/)`。
- SEO 页面关键词堆砌到破坏阅读。

---

## 4. Blog 专项 Rubric

Blog 的核心任务是让读者获得更高质量的判断，而不是把关键词写长。

| 维度 | 分值 | 检查问题 |
|---|---:|---|
| 读者定义 | 15 | 读者是谁？他为什么搜？他已经知道什么？ |
| 专家定位 | 15 | 文章体现设计、增长、产品或行业专家视角了吗？ |
| 论证密度 | 20 | 每个 H2 是否有观点、机制、例子、反例或方法？ |
| SERP 差异 | 15 | 相比 Top 页，Lovart 新增了什么认知？ |
| 例子与证据 | 15 | 是否有具体场景、案例、来源、限制或测试方法？ |
| 视觉与信息图 | 10 | 是否识别流程图、对比图、矩阵、截图机会？ |
| 收束与行动 | 10 | 结尾是否给出下一步，而不是“未来可期”？ |

Blog 额外 BLOCK：

- 开头是百科式定义且没有冲突。
- H2 只剩概念词，如 `Benefits`、`Features`、`Conclusion`。
- 文章没有任何具体例子或反例。
- Comparison 没有公平选择框架。
- “测试/评测”文章没有测试方法。

---

## 5. Landing / Tools / Features 专项 Rubric

落地页的核心任务是推动判断和转化。

| 维度 | 分值 | 检查问题 |
|---|---:|---|
| 首屏承接 | 20 | 5 秒内能否说明给谁、做什么、下一步？ |
| 输入输出 | 15 | 是否写清用户输入什么、得到什么？ |
| 工作流 | 15 | 是否展示生成、编辑、导出/使用路径？ |
| Proof | 15 | 是否有可信证据、示例、文件格式、商用说明或限制？ |
| CTA | 10 | CTA 是否降低风险或匹配当前模块？ |
| FAQ | 10 | 是否处理版权、商用、编辑、导出、价格、学习成本？ |
| SEO 结构 | 10 | 关键词、实体词、H1/H2/FAQ 是否自然覆盖？ |
| 故事线匹配 | 5 | 是否匹配 T/F/P/S/C/K/N story line？ |

Landing 额外 BLOCK：

- Hero 只有愿景，没有具体任务。
- Tools 页没有 FAQ 或 CTA。
- Tools composite-v2 混入 legacy section type。
- 未说明编辑和导出路径。
- 用无法核实的 social proof 数字。

---

## 6. Product Copy 专项 Rubric

产品文案的核心任务是让用户知道发生了什么、下一步怎么做、风险是什么。

| 维度 | 分值 | 检查问题 |
|---|---:|---|
| 状态清晰 | 25 | 用户是否知道当前状态？ |
| 下一步明确 | 25 | 用户是否知道下一步怎么做？ |
| 边界说明 | 20 | 高风险、付费、删除、覆盖、权限是否说明后果？ |
| 语气一致 | 15 | 是否专业、自然、不装可爱？ |
| 术语控制 | 15 | 是否避免内部术语外露？ |

Product copy 额外 BLOCK：

- 错误提示只说 failed，不给修复路径。
- 删除/覆盖/付费动作没有后果说明。
- 空状态没有下一步。

---

## 7. SEO / Programmatic Page 专项 Rubric

SEO 页面不是关键词容器，而是搜索意图承接页。

| 维度 | 分值 | 检查问题 |
|---|---:|---|
| 搜索意图 | 20 | query 是信息、工具、比较、交易还是问题型？ |
| 首屏答案 | 20 | 首屏是否直接回答问题？ |
| 语义覆盖 | 15 | 是否覆盖实体词、同义词、长尾问题？ |
| 信息架构 | 15 | 是否便于浏览和跳读？ |
| 转化入口 | 10 | 是否有自然 CTA 或相关工具入口？ |
| FAQ / schema | 10 | FAQ 是否回答真实长尾问题？ |
| 内链 | 10 | 是否连接 Blog、Tools、Features、Pricing 或相关 hub？ |

SEO 额外 BLOCK：

- 关键词重复到影响阅读。
- FAQ 是模板问答，没有真实搜索问题。
- 页面只回答“是什么”，不处理“怎么选/怎么用/为什么信”。

---

## 8. i18n / Localization 专项 Rubric

本土化不是翻译，而是用本地语言重新承接搜索意图。

| 维度 | 分值 | 检查问题 |
|---|---:|---|
| 本地搜索意图 | 25 | 目标语言用户是否会这样搜索和理解？ |
| 标题与首屏 | 20 | title、meta、Hero 是否自然重写？ |
| 例子和痛点 | 20 | 示例是否符合本地市场？ |
| CTA 和 FAQ | 15 | CTA、FAQ 是否符合本地疑虑？ |
| 品牌术语 | 10 | Lovart / MCoT / ChatCanvas 等是否一致？ |
| 语言洁净度 | 10 | 是否无直译腔、语言污染、混用？ |

i18n 额外 BLOCK：

- 简中直接繁转为 `zh-TW`。
- 日语明显中文语序。
- 英文保留中文式长句。
- 未清除 `(section_xx)` marker。
- 文件名 `{slug}-{lang}.json` 与 `language` 不一致。

---

## 9. 评分输出格式

每次人工审稿或 Agent 审稿输出：

```markdown
## Content Quality Score

- Content type:
- Score: /100
- Verdict: Publish / Edit / Rewrite / Block
- BLOCK triggered: yes/no

### Dimension Scores

| Dimension | Score | Notes |
|---|---:|---|
| Reader / Scenario |  |  |
| SERP Intent |  |  |
| Information Density |  |  |
| Evidence / Trust |  |  |
| Conversion / Next Step |  |  |
| Structure / Readability |  |  |
| Anti-slop Language |  |  |
| Localization |  |  |
| Completeness |  |  |

### Required Fixes

1.
2.
3.
```

---

## 10. 自动化映射建议

后续可映射到 `preflight-content.js`：

| Rubric 项 | 自动化可能性 | 检测方向 |
|---|---|---|
| 可见占位符 | 高 | placeholder / image marker / section marker |
| 坏内链 | 高 | regex |
| slug / language 文件名 | 高 | preflight i18n |
| FAQ 数量 | 高 | section / markdown heading |
| CTA 缺失 | 中 | button / signup / pricing / CTA anchor |
| 空泛词密度 | 中 | banned phrase list |
| H2 太薄 | 中 | H2 下字数、例子、动词、数字 |
| 后半缩水 | 中 | 前后 30% 字数和结构密度对比 |
| SERP intent 错位 | 低-中 | 需要 SERP brief 输入 |
| 证据可信度 | 低 | 多数需人工判断 |

---

## 11. 与后续机制的关系

- Preflight 自动门禁：从本 Rubric 中抽取可自动检测项。
- 内容生产 Ledger：用本 Rubric 的 H2/section 要求做逐节记录。
- 人工标注样本库：按本 Rubric 标注好/坏案例。
- 上线后反馈回流：把 CTR、排名、转化、舆情反馈到 Rubric 权重和模板。
- 黄金样本模板库：只沉淀通过 Rubric 且上线后表现好的结构。
