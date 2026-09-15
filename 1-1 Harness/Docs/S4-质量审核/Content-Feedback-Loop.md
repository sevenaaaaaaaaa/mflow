# Content Feedback Loop — 上线后反馈闭环

> 用途：把 GSC/Bing/GA4/舆情等上线信号，回流到 Rubric 权重、样本库、空泛词表、Ledger 默认项与改写队列。  
> 上游：发布内容、SEO 月报、舆情监控、SERP 调研  
> 配对：[Content-Quality-Rubric](./Content-Quality-Rubric.md)、[Content-Sample-Library](./Content-Sample-Library.md)、[Preflight-Anti-Slop-Gates](./Preflight-Anti-Slop-Gates.md)  
> 登记文件：`1-1 Harness/Skills/lovart-content-quality-gates/feedback/register.json`

---

## 1. 闭环在 Anti-Slop 体系中的位置

```text
创作前：SERP brief → Ledger → 样本库 gold/bad 对照
创作后：Preflight → Rubric
上线后：反馈闭环 ← 你在这里
     ↓
改写 / 降权 / 升 gold / 调阈值 / 新增 bad 样本
```

没有反馈闭环，Rubric 和样本库会**静态老化**：产品变了、SERP 变了、表现数据不会自动修正创作默认值。

---

## 2. 数据源

| 来源 | 路径 / 工具 | 主要信号 | 刷新频率 |
|---|---|---|---|
| **Google Search Console** | GSC UI / API | 展示、点击、CTR、排名、query-page | 周 |
| **Bing Webmaster** | Bing 后台 | 非品牌词覆盖、点击结构 | 月 |
| **GA4** | 分析后台 | 落地转化、停留、跳出 | 周 |
| **SEO 月报** | `1-2 Insight/Trident Insights/reports/monthly/Lovart-SEO-*.md` | 品牌依赖、缺口词、竞品覆盖 | 月 |
| **非品牌 SEO** | `1-2 Insight/Lovart ORM/monthly/Lovart-NonBrand-SEO-*.md` | 高展示低点击词 | 月 |
| **舆情监控** | ORM 月报 / 告警 | 夸大宣传、用户吐槽、合规风险 | 实时/周 |
| **Sanity 发布记录** | import 日志 / GROQ | slug、language、发布日 | 每次发布 |
| **Preflight / Rubric** | 发布时存档 | 成稿分数、BLOCK、样本 ID | 每次发布 |

**原则**：SEO 报告看**趋势与缺口**；GSC 看**单页单 query**；舆情看**表述风险**。不混用为 OKR 数值。

---

## 3. 信号 → 判断 → 动作

### 3.1 信号矩阵

| 信号 ID | 条件（示例阈值，可调） | 可能根因 | 优先查 Rubric 维 |
|---|---|---|---|
| `SIG_CTR_LOW` | 展示 ≥500 且 CTR < 2%（或低于站点该类型中位数 50%） | 标题/首屏不承接意图、AI 腔、snippet 无差异 | SERP intent、Anti-slop、Reader |
| `SIG_RANK_STUCK` | 发布 ≥60 天，目标 query 排名 >20 | 页面类型错、薄内容、内链弱 | SERP intent、Information density |
| `SIG_RANK_UP` | 目标 query 排名进入 Top 10 且上升 ≥5 | 结构有效 | 全维记录为正向 |
| `SIG_BOUNCE_HIGH` | GA4 跳出 >70% 且停留 <40s（Blog/落地页） | 首屏误导、内容不匹配 | SERP intent、Conversion |
| `SIG_CONV_LOW` | 有流量但 signup/pricing 点击低于同类型 P25 | CTA/FAQ 弱、信任不足 | Conversion、Evidence |
| `SIG_ORM_NEGATIVE` | 舆情命中夸大/虚假/合规 | 事实未核实、对比不公 | Evidence、BLOCK 项 |
| `SIG_BRAND_ONLY` | 页面流量 90%+ 品牌词 | 非品牌意图未覆盖 | SEO 实体、SERP intent |
| `SIG_I18N_GAP` | 同 slug EN 有量，目标语言近零 | 直译、本地意图未重写 | Localization |

### 3.2 动作矩阵

| 动作 ID | 触发信号 | 执行 |
|---|---|---|
| `ACT_REWRITE_HERO` | SIG_CTR_LOW + SERP 意图疑似错位 | 重写 title/meta/首屏；更新 Ledger hero 行 |
| `ACT_REWRITE_FAQ_CTA` | SIG_CONV_LOW, SIG_BOUNCE_HIGH | 从 GSC query 补 FAQ；CTA 对齐顾虑 |
| `ACT_DEMOTE_SAMPLE` | SIG_CTR_LOW 且该页曾作 gold 结构来源 | 样本降 borderline；注解根因 |
| `ACT_PROMOTE_SAMPLE` | SIG_RANK_UP + Rubric ≥80 | 升 gold；写入 `reusable_pattern` |
| `ACT_ADD_BAD_SAMPLE` | SIG_ORM_NEGATIVE, 典型 slop 上线稿 | 摘录进 bad 样本库 |
| `ACT_TIGHTEN_PREFLIGHT` | 同类坏稿重复出现 | 增 `anti-slop-rules.js` 规则或降阈值 |
| `ACT_LOOSEN_PREFLIGHT` | gold 误报 ≥3 次 | 收窄空泛词或改 WARN |
| `ACT_LEDGER_DEFAULT` | SIG_RANK_UP 且某 FAQ/H2 重复有效 | 写入 storyline 默认 Ledger |
| `ACT_SERp_REFRESH` | SIG_RANK_STUCK ≥90 天 | 重跑 SERP brief；考虑改页面类型 |
| `ACT_BLOCK_PHRASE` | SIG_ORM_NEGATIVE 用语重复 | 加入 audit `BLOCKED_PHRASES` |

---

## 4. 反馈登记表

每篇上线内容一条记录，文件：`feedback/register.json`（见模板）。

### 4.1 必填字段

| 字段 | 说明 |
|---|---|
| `content_id` | slug 或 Sanity `_id` |
| `content_type` | blog / tool / feature / … |
| `language` | en / zh / ja / … |
| `focus_query` | 主目标词 |
| `published_at` | ISO 日期 |
| `sample_ref` | 创作时参考的样本 ID（可选） |
| `rubric_score` | 发布时分数 |
| `url` | canonical URL |

### 4.2 观测字段（定期更新）

| 字段 | 来源 |
|---|---|
| `impressions_28d` | GSC |
| `clicks_28d` | GSC |
| `ctr_28d` | GSC |
| `avg_position_28d` | GSC |
| `bounce_rate_28d` | GA4 |
| `signup_clicks_28d` | GA4 事件 |
| `top_queries` | GSC top 5 |
| `signals` | 计算得出的 SIG_* 列表 |
| `actions` | 待执行 ACT_* 列表 |
| `status` | watch / action_needed / resolved / promoted |

### 4.3 月度复盘记录

```markdown
## Feedback Review — YYYY-MM

- Pages reviewed: N
- Promoted to gold: [ids]
- Demoted / rewrite queue: [ids]
- Preflight changes: [rules]
- New bad samples: [ids]
- SERP report follow-ups: [links]
```

存于：`feedback/reviews/YYYY-MM.md`

---

## 5. 月度工作流（建议每月第一个工作日）

### Step 1 — 拉数据

1. 从 SEO 月报更新「缺口词 / 品牌依赖」摘要。
2. 从 GSC 导出近 28 天：query + page（或 API）。
3. 从 GA4 拉同 URL 转化与跳出。
4. 扫舆情月报有无内容相关负面。

### Step 2 — 更新 register

```bash
cd "1-1 Harness/Skills/lovart-content-quality-gates/scripts"
node feedback-loop-cli.js import --csv path/to/gsc-page-export.csv
node feedback-loop-cli.js evaluate
node feedback-loop-cli.js report --month 2026-06
```

`import` 合并 CSV 行到 `register.json`；`evaluate` 打 SIG_*；`report` 输出 Markdown 复盘草稿。

### Step 3 — 分类处理

| 队列 | 处理人 | SLA |
|---|---|---|
| **P0 合规/舆情** | 编辑 + 法务复核 | 48h |
| **P1 高展示低 CTR** | 编辑重写首屏 | 2 周 |
| **P2 排名停滞** | SEO + 编辑 SERP 刷新 | 1 月 |
| **P3 样本升降** | 内容负责人 | 月内 |

### Step 4 — 回流机制

1. **样本库**：`sample-library-cli.js` 更新 verdict / 注解。
2. **Preflight**：`anti-slop-rules.js` + `calibrate`。
3. **Ledger**：更新 storyline 默认 section（Content-Production-Ledger §4.4）。
4. **Rubric**：若某维连续背锅，在复盘里提议调权重（需负责人确认）。

### Step 5 — 归档

- 保存 `feedback/reviews/YYYY-MM.md`
- 重大改写附 Before/After Rubric 分

---

## 6. CSV 导入格式（GSC 页面级）

`feedback-loop-cli.js import` 接受简化 CSV：

```csv
url,impressions,clicks,ctr,position,period_end
https://www.lovart.ai/tools/ai-commercial-generator,12000,180,0.015,14.2,2026-06-01
```

匹配规则：URL path → `register.json` 的 `url` 或 `content_id`（slug）。

---

## 7. 与 Rubric / 样本 / Preflight 的映射

| 反馈结论 | Rubric | 样本库 | Preflight |
|---|---|---|---|
| 首屏意图错位 | 重评 SERP intent | 降 gold / 增 borderline | — |
| AI 腔导致 CTR 低 | 重评 Anti-slop | 增 bad 摘录 | 加 AS_BANNED |
| 结构有效排名升 | 存档 dimension 高分 | 升 gold | — |
| FAQ 缺导致转化低 | Conversion 低分 | good FAQ 进 Ledger 默认 | UX_FAQ 已有 |
| 事实投诉 | Evidence BLOCK | bad + ORM 标签 | — |

---

## 8. 禁止事项

- 不因短期波动（<28 天、<200 展示）频繁改 gold 样本。
- 不把品牌词 CTR 与非品牌词混评。
- 不未核实就因竞品上涨降 Lovart 稿；先 SERP 刷新。
- 反馈闭环**不自动发布**改写；只产出队列与建议，人工或 Agent 带 Ledger 重写。

---

## 9. 完整机制栈（当前状态）

| 机制 | 文档 | 状态 |
|---|---|---|
| Anti-Slop 原则 | Anti-Slop.md | ✅ |
| Rubric | Content-Quality-Rubric.md | ✅ |
| Ledger | Content-Production-Ledger.md | ✅ |
| Preflight | Preflight-Anti-Slop-Gates.md | ✅ |
| 样本库 | Content-Sample-Library.md | ✅ |
| **反馈闭环** | **本文档** | ✅ |

---

## 10. 维护

- 每季度审查阈值（CTR%、排名天数）是否适配各语言市场。
- 新渠道（如 DuckDuckGo 验证报告）可作为补充信号，不替代 GSC。
- `register.json` 过大时按年归档：`feedback/archive/register-2025.json`。
