---
name: lovart-content-audit
description: Step 4 of Lovart Content Pipeline — 深度内容审计（Blog 为主）：合规、文化、可读性、SEO 深度项。
---

# lovart-content-audit

## 路径契约

| 层 | 路径 |
|----|------|
| 文档 SSOT | `1-1 GEO Readme/` |
| Sanity 脚本 | `1-4 Dev/lovart.sanity.studio/scripts/` |
| SEO/Sentinel 脚本 | `1-4 Dev/scripts/` |
| 自动化 | `1-4 Dev/automation/` |
| 本 Skill | `1-1 Harness/Skills/lovart-content-audit/SKILL.md` |

Step 4 of Lovart Content Pipeline — 深度内容审计（Blog 为主）：合规、文化、可读性、SEO 深度项。  
**自动化预检（JSON/MD 结构、SEO 长度、URL、i18n）请先跑** [`lovart-content-quality-gates`](../lovart-content-quality-gates/SKILL.md) + `scripts/preflight-content.js`。

## Triggers

- "审计内容" / "audit content"
- "内容质量检查" / "content quality check"
- "合规审查" / "compliance review"
- "文化敏感检查" / "cultural sensitivity check"
- Pipeline Orchestrator 调用 Step 4

## Prerequisites

- Step 3 内容创作（`lovart-content-writer` / `lovart-features-page` / `lovart-blog-automation`）已完成
- 待审内容存在于对应输出目录

## Audit Dimensions

### Dimension 0: 自动化预检（Tools / Features / Blog MD）

在 Dimension 1–5 之前执行：

```bash
cd 1-4 Dev/lovart.sanity.studio
node scripts/preflight-content.js --type tools|features|blog-md|blog-quality
```

| 已覆盖 | 仍由本 Skill 人工/深度处理 |
|--------|-------------------------|
| JSON/MD 语法、文件名与 language、marker、slug、SEO 长度、url_path 契约、CDN URL | 合规用语、文化敏感、TF-IDF 重复、可读性评分 |
| 可选 HTTP URL 探测 | focus keyword 分布、hreflang 策略 |
| `audit-content-quality.js` 线上 | zh/zh-TW 译文、EN 可读性、占位符 P0/P1 backlog |

### Dimension 1: 内容质量审计

| 检查项 | 规则 | 严重级 |
|--------|------|--------|
| **字数达标** | 按类型最低字数要求 | BLOCK |
| **H2 结构** | 至少 4 个 H2，层级不跳（H2→H4 ×） | BLOCK |
| **FAQ 存在** | ≥3 个 Q&A，问题含长尾关键词 | BLOCK |
| **CTA 存在** | 包含 lovart.ai/signup 或 /pricing | BLOCK |
| **内部链接** | 所有链接 curl 返回 200 | BLOCK |
| **外部链接** | 无竞品注册链接（canva.com/signup ×） | BLOCK |
| **图片占位** | IMAGE PLACEHOLDER 必须有描述 | WARN |
| **Frontmatter** | 所有 required 字段非空 | BLOCK |
| **拼写** | 无 typo（品牌词大小写严格） | WARN |
| **重复内容** | 与已发布内容 TF-IDF 相似度 < 0.7 | BLOCK |
| **可读性** | Flesch-Kincaid Grade ≤ 12 | WARN |

### Dimension 2: SEO 审计

| 检查项 | 规则 | 严重级 |
|--------|------|--------|
| **Title tag** | ≤60 字符，含 focus keyword | BLOCK |
| **Meta description** | 150-160 字符 | WARN |
| **Focus keyword** | 在 H1 + 前 100 词 + 至少 2 个 H2 中出现 | BLOCK |
| **Keyword density** | 1-2%（过高过低均 WARN） | WARN |
| **Alt text** | 所有图片有 alt，含关键词变体 | WARN |
| **Schema type** | frontmatter `seo_schema` 与内容匹配 | WARN |
| **Canonical** | 多语言版本互相引用 hreflang | BLOCK |

### Dimension 3: 全球化监管合规 🌍

针对 10 种语言（en/zh/zh-TW/ja/ko/de/fr/pt/ru/it）的法律法规：

| 市场 | 法规 | 检查内容 |
|------|------|---------|
| **EU (de/fr/it)** | GDPR / DSA | 无未授权个人数据；价格声明含税说明；Cookie 同意提示 |
| **China (zh)** | 广告法 / 个保法 | 无绝对化用语（"最好""第一""唯一"）；无虚假对比数据；用户数据声明 |
| **Japan (ja)** | 景品表示法 | 无夸大功效表述；对比广告需有客观依据 |
| **Korea (ko)** | 电子商务法 | 价格标注含 VAT；退款政策明示 |
| **Russia (ru)** | 广告法 No.38-FZ | 广告标识；竞品对比需可验证数据 |
| **Brazil (pt)** | CDC / LGPD | 消费者权益声明；数据处理透明度 |
| **US/Global (en)** | FTC / CAN-SPAM | 推荐/评测需披露利益关系；邮件退订链接 |

**自动检查规则**：

```python
BLOCKED_PHRASES = {
    "zh": ["最好的", "第一名", "唯一", "100%保证", "绝对"],
    "ja": ["業界No.1", "最高品質", "絶対"],
    "de": ["garantiert", "100% sicher"],
    "all": ["guaranteed results", "100% free forever"],
}
```

### Dimension 4: 文化敏感性检查 🎭

| 检查项 | 风险场景 | 处理方式 |
|--------|---------|---------|
| **颜色象征** | 白色在东亚部分场景代表丧事 | WARN + 人工复核 |
| **手势/图像** | OK 手势在巴西有冒犯含义 | BLOCK |
| **节日引用** | 引用特定宗教节日可能排斥其他群体 | WARN |
| **性别/种族** | 示例人物需多样化 | WARN |
| **数字忌讳** | 4（中日韩）、13（西方） | WARN |
| **政治敏感** | 国旗、地图边界、台湾/西藏/克里米亚相关 | BLOCK |
| **宗教符号** | 十字架、新月、六芒星等宗教符号 | BLOCK |
| **食物/动物** | 猪（伊斯兰文化）、牛（印度教文化） | WARN |
| **历史事件** | 引用可能在某些市场敏感的历史事件 | BLOCK |

**地图/领土特别规则**：
- zh 版本：使用中国标准地图审图号
- 所有版本：避免展示有争议边界的地图
- 如需地图：使用简化图形，不标注有争议区域

### Dimension 5: 品牌一致性

| 检查项 | 标准 |
|--------|------|
| 品牌名 | "Lovart" 不是 "LovArt" 或 "LOVART" |
| 产品名 | MCoT / ChatCanvas / Touch Edit / Nano Banana — 精确拼写 |
| 竞品提及 | 客观陈述，不贬低（"differs from" 而非 "is better than"） |
| 语气 | 专业但友好，避免过度推销语气 |
| Logo 使用 | 仅使用官方 Logo URL |

## Audit Report Format

```markdown
# Content Audit Report — {slug}

**审计时间**: YYYY-MM-DD HH:MM
**内容类型**: {type}
**目标语言**: {languages}

## 📊 审计评分

| 维度 | 得分 | 状态 |
|------|------|------|
| 内容质量 | 92/100 | ✅ PASS |
| SEO | 88/100 | ✅ PASS |
| 全球合规 | 100/100 | ✅ PASS |
| 文化敏感 | 95/100 | ⚠️ WARN |
| 品牌一致 | 100/100 | ✅ PASS |

**总评**: ✅ PASS / ⚠️ CONDITIONAL / ❌ BLOCK

## 🚫 BLOCK 项 (必须修复)
- [无]

## ⚠️ WARN 项 (建议修复)
- zh 版本第 3 段使用了"最好的"，建议改为"领先的"
- 缺少 alt text: IMAGE PLACEHOLDER #4

## ✅ 通过项
- 字数: 3,847 (要求 ≥3,600) ✓
- FAQ: 5 个 Q&A ✓
- CTA: lovart.ai/signup ✓
- 内部链接: 4/4 返回 200 ✓
```

## Decision Logic

```
IF any BLOCK item exists:
    → 返回 Step 3 修复，标记具体修复项
    → 修复后重新审计

IF only WARN items:
    → 标记为 CONDITIONAL PASS
    → 可进入 Step 5，但建议在发布前人工复核 WARN 项

IF all PASS:
    → 直接进入 Step 5
```

## Output

```
Output/Audit Reports/
└── YYYY-MM-DD/
    ├── audit-{slug}.md
    ├── audit-{slug}-zh.md
    └── audit-summary.md            ← 当日所有审计汇总
```

## Downstream

PASS / CONDITIONAL PASS → `lovart-content-quality-gates`（统一 L1/NDJSON 技术预检）→ `lovart-sanity-publish` (Step 5)  
WordPress 子站 → `lovart-multi-platform-push`（跳过 Sanity preflight）  
BLOCK → 回退到 Step 3 修复

**Step 5 发布前必守**（三条 Sanity 管道共用）：[`first-run-and-incremental-policy.md`](../lovart-sanity-publish/references/first-run-and-incremental-policy.md)

- **首次**：认证 + login + 拉线上参照到本地（Blog：`sync-blog-taxonomy`）→ 再 import  
- **已有**：本地/线上同 `_id` 已存在 → 不全量重发  
- **日常**：仅增量，`import --missing` only；全量仅用户明确要求

## Anti-Bugs（禁止再犯）

> 全量目录：[ANTI-BUGS-REGISTRY.md](../../../1-1%20GEO%20Readme/ANTI-BUGS-REGISTRY.md)

| ID | 本 Skill 门禁 |
|----|--------------|
| AB-S01 | 正文禁止 `IMAGE PLACEHOLDER`；brief 写入 `imageBriefs`（不上屏） |
| AB-C01 | 线上占位审计用 `audit-content-quality.js` 严格 regex，勿宽松 GROQ |
| AB-C02 | zh/zh-TW P0 须 `translate-zh-rewrite.py`；EN 定稿后再译 |
| AB-C03 | EN 可读性 Flesch ≤12（WARN）；P0 slug 先 EN 编辑批次 |
| AB-C04 | `imageBriefs` 仅 Studio 可见；验收前端不渲染 |
| AB-A02 | SEO/category 改动不必全量前端 diff；见 Registry 附录 B |


## 预算（RULES-70 强制）

本 skill 产出受 RULES-70 数量预算约束（字数/H2/FAQ/数据点/来源）。
