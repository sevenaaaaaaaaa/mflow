# Anti-Slop 专项 — 入口

> **定位**：质量治理体系的核心专项，确保所有 Lovart 对外内容（落地页、Blog、产品文案、SEO 页面、多语言版本）达到可发布标准。

---

## 目标

消除"AI 泔水"——无对象、无判断、无证据、无转化、无上下文的内容。不是反对 AI 辅助写作，而是让每一段内容承担明确任务：让读者更快理解、更愿意相信、更知道下一步该做什么。

---

## 体系架构

```
SERP 报告 → 外部/标杆结构
    ↓
样本库（标注卡片）←→ 反馈闭环（GSC 信号）
    ↓
创建 Skills / Ledger 模板（few-shot）
    ↓
草稿 → anti-slop-preflight（CREATE）→ preflight-content（TRANSLATE/PRE-PUBLISH）
    ↓
Rubric 人工/Agent 评分 → lovart-content-audit（DEEP QA）
    ↓
发布 → 发布后信号 → 反馈闭环 → 更新样本 & 阈值
```

---

## 核心文件清单

### 文档 SSOT（1-1 GEO Readme/文档/04-质量治理/）

| 文件 | 大小 | 用途 |
|------|------|------|
| **Anti-Slop.md** | 26.6KB / 507行 | 🔴 写作规范 SSOT：总原则、落地页、Blog、产品文案、SEO、语言本土化、防缩水、反例、发布前清单 |
| **Preflight-Anti-Slop-Gates.md** | 6.1KB / 177行 | 错误码映射：Anti-Slop 规则 → 自动化检测码（AS_BANNED_PHRASE、AS_SHRINKAGE 等） |
| **Content-Sample-Library.md** | 6.3KB / 176行 | 样本库：5 级标注（Gold/Good/Borderline/Bad/External），8 个当前样本 |
| **Content-Quality-Rubric.md** | 9.2KB | 评分标准：多维度内容质量评分 |
| **Content-Production-Ledger.md** | 14.0KB | 生产台账：内容生产跟踪 |
| **Content-Feedback-Loop.md** | 8.6KB | 反馈闭环：发布后信号 → 样本调整 |

### 实现脚本（1-1 Harness/Skills/lovart-content-quality-gates/）

| 文件 | 用途 |
|------|------|
| `scripts/anti-slop-preflight.js` | 自动化预检脚本（禁用词、薄 H2、缩水检测） |
| `scripts/lib/anti-slop-rules.js` | 禁用词 SSOT（EN/ZH/JA 三语）+ 阈值配置 |
| `scripts/sample-library-cli.js` | 样本库管理 CLI |
| `scripts/feedback-loop-cli.js` | 反馈闭环 CLI |
| `samples/` (8个) | 标注样本（blog/tool/comparison/landing/i18n 各类型） |
| `references/preflight-anti-slop-gates.md` | 错误码参考 |
| `references/content-sample-library.md` | 样本库参考 |

### 质量门禁层级（Anti-Slop 涉及部分）

| 层级 | 名称 | Anti-Slop 角色 |
|------|------|---------------|
| **L1b** | Anti-Slop 预检 | `anti-slop-preflight.js` — 禁用词密度、薄 H2、缩水、FAQ/CTA 缺失 |
| **L3b** | Anti-Slop 深度审计 | `audit-content-quality.js` + `lovart-content-audit` — 占位符检测、可读性、SERP 意图对齐 |

---

## 关键规则速查

| 规则 | 说明 |
|------|------|
| **禁用词** | EN: unlock, revolutionize, seamless, empower... / ZH: 赋能、闭环、颠覆性、一站式... / JA: 革新的な、シームレス... |
| **缩水检测** | 30/40/30 分段评分：后 30% 密度 < 前 30% → BLOCK |
| **薄 H2** | H2 下 <80 词 → WARN；长文 <3 个 H2 → WARN |
| **四问检查** | 发布前必答：谁读？为什么现在读？读完改变什么？下一步是什么？ |
| **语言边界** | EN 多用具体动作；ZH 禁用无定义黑话；JA 用自然敬体；多语言 ≠ 逐句翻译 |

---

## 跨专项依赖

- **i18n 专项**：Anti-Slop §6（语言本土化 Skills）定义了 10 语言的写作风格要求
- **Content Distribution**：分发内容必须通过 Anti-Slop 预检（Gate 0）
- **Quality Gates Skill**：Anti-Slop 是 L1b 层级的核心组成部分

---

## 相关 Skill

- `lovart-content-quality-gates` — 质量门禁总 Skill（含 Anti-Slop L1b + L3b）
- `lovart-content-audit` — 深度人工审计 Skill
- `lovart-sanity-preflight` — ⚠️ 已废弃，功能合并到 quality-gates
