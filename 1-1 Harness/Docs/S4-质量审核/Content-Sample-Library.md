# Content Sample Library — 人工标注样本库

> 用途：用可复用的好稿/坏稿对照，校准 Rubric 打分、Preflight 阈值和创作模板。  
> 上游：[Content-Quality-Rubric](./Content-Quality-Rubric.md)、[Preflight-Anti-Slop-Gates](./Preflight-Anti-Slop-Gates.md)、SERP Copy Intelligence  
> 下游：创作 skills、空泛词表调参、上线后反馈闭环、黄金模板库

---

## 1. 为什么需要样本库

Rubric 告诉 Agent「怎么判」，Preflight 告诉脚本「拦什么」，但两者都需要**锚定样本**：

- 同样命中 `unlock`，一句可接受、五句应 BLOCK —— 靠样本校准。
- 「薄 H2」与「精悍段落」的边界 —— 靠对照样本。
- Tool 页 hero 怎样算写清输入/输出 —— 靠 gold 样本结构，不靠形容词。

样本库不是范文抄袭库，而是**带维度标注的判断训练集**。

---

## 2. 样本分级

| 级别 | 标签 | 含义 | 用途 |
|---|---|---|---|
| **Gold** | `gold` | 通过 Rubric ≥85，无 BLOCK，上线后表现好或 SERP 结构值得学 | 默认模板、Agent few-shot |
| **Good** | `good` | 通过 Rubric ≥80，可发布，有小瑕疵 | 结构参考 |
| **Borderline** | `borderline` | 70–79 或 WARN 较多，需编辑 | 阈值边界校准 |
| **Bad** | `bad` | <70 或触发 BLOCK / 典型 AI slop | 反例、Preflight 测试 fixture |
| **External** | `external` | 竞品/SERP 页（不照抄文案，只学结构） | 页面形态与信息架构 |

---

## 3. 标注字段（每张样本卡）

每个样本文件使用 YAML frontmatter + 正文注解：

| 字段 | 必填 | 说明 |
|---|---|:---:|
| `sample_id` | ✓ | 唯一 ID，如 `blog-en-good-001` |
| `verdict` | ✓ | gold / good / borderline / bad / external |
| `content_type` | ✓ | blog / tool / feature / comparison / seo / i18n |
| `language` | ✓ | en / zh / ja / … |
| `focus_query` | 建议 | 目标搜索词或页面任务 |
| `rubric_score` | ✓ | 总分 /100 |
| `block_triggered` | ✓ | yes / no |
| `dimension_scores` | ✓ | Rubric 九维或专项维度的简分 |
| `preflight` | ✓ | `pass` + 预期 `codes[]` |
| `reusable_pattern` | ✓ | 一句话可复用结构 |
| `anti_patterns` | bad 必填 | 错在哪 |
| `ledger_snapshot` | 建议 | 关键 H2/section 计划（好稿附） |
| `source` | ✓ | internal / serp_observed / production |
| `tags` | 建议 | 便于检索 |

### 注解正文结构

```markdown
## Excerpt
（代表性片段，非全文）

## Why this verdict
（按 Rubric 维度说明）

## Reuse for Lovart
（结构可学什么，文案不可抄什么）

## Preflight expectation
（跑 anti-slop-preflight 应 pass/fail 及 codes）

## Related
（链接 SERP 报告、storyline、同类样本）
```

---

## 4. 样本目录

文件位置：`1-1 Harness/Skills/lovart-content-quality-gates/samples/`

索引：`samples/index.json`（机器可读）

| ID | 类型 | 语言 | 级别 | 主题 |
|---|---|---|---|---|
| `blog-en-good-001` | Blog | en | good | 视频广告品牌一致性 |
| `blog-en-bad-001` | Blog | en | bad | 典型 AI slop 短文 |
| `tool-en-gold-001` | Tool | en | gold | 商业视频工具页结构（SERP 抽象） |
| `tool-en-bad-001` | Tool | en | bad | 愿景 hero、无 IO/workflow |
| `comparison-en-good-001` | Comparison | en | good | 公平选型 + 测试方法 |
| `comparison-en-bad-001` | Comparison | en | bad | 只踩竞品、无 verdict |
| `i18n-ja-bad-001` | i18n | ja | bad | 中文语序直译 |
| `landing-en-borderline-001` | Tool/Feature | en | borderline | 功能枚举、重复标题 |

---

## 5. 如何使用

### 5.1 创作前（Agent / 编辑）

1. 按 `content_type` + `focus_query` 从 index 找 1 gold + 1 bad。
2. 读 `reusable_pattern`，写入 Ledger 计划。
3. 禁止照抄 external/gold 全文；只复用结构与信息密度。

### 5.2 成稿后校准

```bash
cd "1-1 Harness/Skills/lovart-content-quality-gates/scripts"
node anti-slop-preflight.js --file path/to/draft.md --strict
```

对照同类 bad 样本，确认未命中相同 `anti_patterns`。

### 5.3 Rubric 人工审稿

用样本卡中的 `dimension_scores` 作为锚点：新稿某维明显低于 good 样本同维 → 必填 `Required Fixes`。

### 5.4 Preflight 阈值调参

| 观察 | 动作 |
|---|---|
| good 样本误报 `AS_BANNED_PHRASE` | 从 `anti-slop-rules.js` 收窄该词或改阈值 |
| bad 样本未拦 | 新增规则或降 `AS_BANNED_DENSITY` 阈值 |
| borderline 样本分歧大 | 拆成 good + bad 两条，写清边界说明 |

---

## 6. 新增样本流程

1. 从生产稿、SERP 观察或创作草稿取材。
2. 复制 `samples/_template.md`。
3. 填 frontmatter + 四段注解。
4. 跑 `anti-slop-preflight.js`，核对 `preflight` 字段与实测一致。
5. 更新 `samples/index.json`。
6. 若是 gold：附 Ledger 快照或 storyline 槽位表。

**准入 gold 条件**：Rubric ≥85、无 BLOCK、有具体例子/workflow、Preflight pass、`reusable_pattern` 可被第三方编辑理解。

---

## 7. 与反馈闭环的关系

SSOT：[Content-Feedback-Loop.md](./Content-Feedback-Loop.md) · 登记：`1-1 Harness/Skills/lovart-content-quality-gates/feedback/register.json`

| 信号 | 回流到样本库 |
|---|---|
| GSC 高展示低 CTR | 检查是否 SERP 意图错位 → 降 gold 或改标注（`ACT_DEMOTE_SAMPLE`） |
| 排名上升 | 结构升 gold；记录 query + 页面类型（`ACT_PROMOTE_SAMPLE`） |
| 转化低 | 检查 CTA/FAQ → borderline 注解（`ACT_REWRITE_FAQ_CTA`） |
| 舆情/合规 | bad 样本库增加违规片段（`ACT_ADD_BAD_SAMPLE`） |

```bash
cd "1-1 Harness/Skills/lovart-content-quality-gates/scripts"
node feedback-loop-cli.js evaluate
```

---

## 8. 与现有机制的关系

```text
SERP 报告 → 提取 external/gold 结构
     ↓
样本库（标注卡）
     ↓
Ledger 模板 / 创作 skills few-shot
     ↓
成稿 → anti-slop-preflight → Rubric
     ↓
上线表现 → 反馈闭环 → 更新样本级别与阈值
```

---

## 9. 维护

- 每月从 SERP 报告新增 1–2 条 external 结构样本。
- 每季度审查 gold 是否仍符合产品现状（能力、定价、模型）。
- 样本正文保持短摘录；全文链到 Content Calendar / Pages 正式路径。
