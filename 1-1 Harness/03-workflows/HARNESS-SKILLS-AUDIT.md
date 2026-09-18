---
type: audit/harness-skills
updated: 2026-09-18
---

# Harness & Skills 全量盘点

> 2026-09-18 · 用实测数据逐项盘点：规则硬条款密度 · 45 Skills 覆盖与质量 · Harness 目录冗余 · 缺失能力 · 开源社区可补充项

---

## 一、Rules（9 个文件）——硬条款密度

| 文件 | 行数 | 条款 | 硬条款 | 密度 | 状态 |
|------|-----:|-----:|-------:|:---:|------|
| RULES-00-iron | 82 | 39 | 16 | 41% | ✅ 核心 |
| RULES-10-reports | 79 | 16 | 10 | 62% | ✅ |
| **RULES-20-creation** | **239** | **55** | **0** | **0%** | 🔴 全散文，最需要硬条款化 |
| RULES-30-quality | 142 | 53 | 14 | 26% | 🟡 可提高 |
| **RULES-40-ops** | **73** | **25** | **0** | **0%** | 🔴 全散文 |
| RULES-50-distribution | 76 | 20 | 10 | 50% | ✅ |
| **RULES-60-management** | **88** | **13** | **0** | **0%** | 🔴 全散文 |
| RULES-70-quota | 54 | 23 | 18 | 78% | ✅ 最佳 |
| RULES-80-language | 60 | 20 | 13 | 65% | ✅ |

**结论**：RULES-20/40/60 三个文件**零硬条款**，Agent 读到的是散文不是可执行规则。
**修复**：按 RULES-30/10/50 的模式重构为「硬条款 + 参数表」。

---

## 二、Skills 45 个——分维度审计

### 2.1 空描述（16 个 = 35%）→ Agent 检索盲区

```
lovart-kb-ingest / lovart-kb-mine / lovart-blog-signal-writer
lovart-insight-trend / lovart-content-quality-gates / lovart-sanity-preflight
lovart-dream-memory / lovart-dream-orchestrator / lovart-knowledge-graph-query
lovart-new-tool-governance / lovart-pipeline-state / lovart-quality-cascade
lovart-router / lovart-session-log / lovart-session-recap / lovart-universal-prompt
```
**修复**：为全部 16 个补 description（从正文首段提取）

### 2.2 引用不存在的依赖

```
7 个 skill 引用 lovart-core（不存在）
7 个 skill 引用 lovart-blog（不存在）
```
**修复**：lovart-core 应指向 00-INDEX.md；lovart-blog 应指向 lovart-blog-serp-writer 或 lovart-blog-automation

### 2.3 按线上 8 类页面 × 覆盖检查

| 页面类型 | 内容库数 | 生成 | 质检 | 发布 | 缺口 |
|---------|--------:|:---:|:---:|:---:|------|
| blog | 8,572 | ✓ ×3 | ✓ | ✓ | — |
| features | 6,279 | ✓ landing-page | ✓ | ✓ | — |
| tools | 1,661 | ✓ landing-page | ✓ | ✓ | — |
| topics | 409 | ✓ landing-page 泛化 | ✓ | **缺** | 缺专属发布 |
| scenarios | 23 | ✓ landing-page 泛化 | ✓ | ✓ | — |
| solutions | 115 | ✓ landing-page 泛化 | ✓ | **缺** | 缺发布 |
| products | 41 | **缺** | ✓ | ✓ | 缺生成 |
| news | 17 | **缺** | ✓ | **缺** | 全缺 |

### 2.4 体量异常

| 过大（需拆分） | 行数 |
|--------------|-----:|
| ai-self-media-article | **912L** |
| lovart-better-design | **702L** |
| lovart-landing-page | **658L** |

| 过薄（需充实） | 行数 |
|--------------|-----:|
| lovart-review | **46L** |
| lovart-sanity-preflight | **43L** |
| lovart-session-recap | **52L** |
| lovart-best-practice | **53L** |
| lovart-stack-by-stack | **53L** |

### 2.5 引用悬空（lovart-core / lovart-blog 不存在）

```
7 个 skill 引用 lovart-core（不存在）→ 应指向 00-INDEX.md
7 个 skill 引用 lovart-blog（不存在）→ 应指向 lovart-blog-serp-writer
```
涉及：lovart-101 / best-practice / insight-trend / review / stack-by-stack / thought-leadership / better-design

---

## 三、Harness 目录冗余审计

| 目录 | 项数 | 评估 | 建议 |
|------|:---:|------|------|
| **01-project** | 7 | PRD/迁移说明/项目管理文档 → 不属于 Harness 规则体系 | **移到 11-knowledge/project/** |
| **05-skills** | 2 | 仅 2 个治理元文件 → 与 03-workflows 重复 | **并入 03-workflows/** |
| **07-okr** | 3 | 季度总结（历史文档）→ 不是规则 | **移到 11-knowledge/okr/** |
| **09-scripts** | 3 | 数据流图 / TOOLS-REGISTRY / sync 脚本 | ✅ 保留 |
| **10-config** | 6 | GSC/Notion/双轨等外部配置文档 | ✅ 保留 |
| **11-knowledge** | 159 | **sessions/ 占 81 篇**（会话日志） | **归档 60 天以上的旧会话** |
| **Docs/** | 65 | 角色手册 / S1-S6 阶段手册 / 参考配置 | ✅ 保留（S0-S6 手册是核心） |
| **04-setup** | 2 | 路径契约 + README | ✅ 保留 |
| **03-workflows** | 2 | PRD + REFERENCE-INDEX | ✅ 保留 |

**清理后 Harness 从 ~500 文件 → ~300 文件**（主要是归档 81 篇旧会话日志）

---

## 四、从开源社区补充的能力

### 高优先级（直接可用）

| 能力 | 现状 | 开源方案 | 复杂度 |
|------|------|---------|:---:|
| **Flesch 可读性评分** | 无 | textstat (Python) | 低 |
| **原创性/查重检测** | 无 | difflib + 历史稿件对比 | 中 |
| **Schema.org 生成器** | 手动写 structuredData | 从 composite doc 自动生成 JSON-LD | 低 |
| **hreflang 校验** | 无 | 检查多语言页面 hreflang 一致性 | 低 |
| **内部链接建议** | 无 | 从内容库 17.5k 篇中自动找相关页做内链 | 中 |
| **DeepL 翻译** | 无 | DeepL API → 翻译 + 本地化重写 | 中 |
| **email newsletter** | 无 | Beehiiv/Mailchimp API | 中 |

### 中期有价值

| 能力 | 说明 |
|------|------|
| HN/Reddit poster | 自动发帖引流（RULES-50 已有 16 平台但缺 HN/PH）|
| Live competitor monitor | 竞品页面变更/价格变动自动通知 |
| Core Web Vitals checker | 页面性能监控 |
| Plagiarism check | 内容原创性检测 |

---

## 五、执行优先级

| # | 动作 | 影响面 | 耗时 |
|:---:|------|--------|:---:|
| **1** | RULES-20 硬条款化（239 行全散文 → 15+ 硬条款） | 🔴 创作规则是最高频引用 | 2h |
| **2** | RULES-40/60 硬条款化 | 同上 | 1h |
| **3** | 16 个 skill 补 description（Agent 检索盲区）| 直接影响 Agent 任务台质量 | 1h |
| **4** | 修复 7 个 skill 的 lovart-core/lovart-blog 悬空引用 | Agent 加载时会报错 | 0.5h |
| **5** | Harness 目录瘦身（01-project→11-knowledge / 07-okr→11-knowledge / 81 篇旧会话归档） | 降低噪音 | 0.5h |
| **6** | 4 个缺失页面类型的 publish skill（topics/solutions/products/news）| 发布覆盖不全 | 2h |
| **7** | 3 个过薄 skill 补充（review/preflight/stack-by-stack） | 质量提升 | 1h |
| **8** | Flesch 可读性评分接入 quality-gates | 自动化 | 1h |
| **9** | Schema.org 自动生成器 | 发布时自动生成 JSON-LD | 1h |
| **10** | 内链建议器（从 17.5k 库自动找相关页）| GEO 加分项 | 2h |

