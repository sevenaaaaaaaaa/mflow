# 旧版模块 → 新版模块：对应关系与实现说明

> 修订：2026-06  
> **Tools（2026-06-07 核验）**：线上 Tools legacy 已清零；`production-audit-summary.json` 显示 `legacy: 0`，`pull-tools-latest.json` 显示 `528` Tools 中 `legacy: 0`、`draft: 6`（`seo.noIndex`，不参与本地 sync）。正式源 **`Page Gen/Pages/Tools/`**（`sync-tools-from-production.js`）。`pages-legacy/Tools/` **已弃用**。历史 `ru` 下 2 篇 legacy 已由 `ru-tools-legacy-patch-2026-05-29.md` 记录为 patched。  
> **Features**：`Pages/Features/` 仍可为 legacy 或 v2 并存。

---

## 1. 先建立一张「总图」

```
┌─────────────────────────────────────────────────────────────────┐
│  页面 JSON 文件（本地）                                            │
│  Page Gen/Pages/Features/{lang}/{slug}-{lang}.json               │
│  Page Gen/Pages/Tools/{lang}/{slug}-{lang}.json  (v2 only)       │
│  pages-legacy/Tools/  ← 只读迁移源（heroSection）                 │
├─────────────────────────────────────────────────────────────────┤
│  顶层字段（大多不用改）                                            │
│  slug, language, title, seo, url_path, category, id ...          │
├─────────────────────────────────────────────────────────────────┤
│  ★ 真正要换的只有这一块 ★                                          │
│  bodyJson: "[ { type, ...fields }, ... ]"   ← section 数组       │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  Sanity compositePage（线上）                                      │
│  同一份 bodyJson 字符串 → 前端 CompositeSectionRenderer 渲染      │
└─────────────────────────────────────────────────────────────────┘
```

**你需要改的地方只有 `bodyJson` 里每个对象的 `type` 和字段名。**  
`slug`、`title`、`seo`、导入脚本、`category` 等**不用因为换组件而改**（除非 SEO 文案要重写）。

---

## 2. 两套体系对比

| | 旧版（Legacy） | 新版（Composite v2） |
|---|----------------|----------------------|
| **section 数量** | 8 种 `type` | 33 种 `type` |
| **字段结构** | 各 type 字段不统一；常有嵌套 `sections[]` | **字段铺平**在 section 顶层 |
| **渲染** | `legacy/*.tsx` | `CompositeSectionRenderer` + 新组件 |
| **文档** | 散落在 Skills / SOP | `Refresh-Page/README.md` |
| **现网 Features** | 约 69% 为 5 段式 | 尚未批量替换 |
| **现网 Tools** | 长链 7–9 段 | 尚未批量替换 |

**旧 8 种 type 名单：**

`heroSection` · `centeredInputSection` · `contentSection` · `textImageSection` · `threeColumnSection` · `featureGridSection` · `testimonialSection` · `faqSection`  
（另有少量 `ctaSection` 等边缘 type）

---

## 3. 一对一对应表（迁移时查这张表）

> **重要：** 旧 → 新 不总是 **1 个换 1 个**。有时 **1 拆多**（`contentSection`）、**多 并 1**（多个 `textImageSection` → 一条 `feature-detail`）。

| 旧 `type` | 谁在用 | 新 `type`（首选） | 关系 | 字段怎么搬 |
|-----------|--------|-------------------|------|------------|
| `heroSection` | Tools | `prompt-launcher` | 1→1 | 见 §4.1 |
| `centeredInputSection` | Features | `prompt-launcher` | 1→1 | 同 §4.1 |
| `contentSection` | Tools | `feature-detail` 或 `bento-2` | **1→1 条**，内含 N 子块 | 每个 `sections[]` 子项 → `items[]` 或 `features[]` |
| `threeColumnSection` | 两者 | `workflow-horizontal` 或 `portrait-grid-3` | 1→1 | `columns[]` → `steps[]` 或 `cards[]` |
| `textImageSection` | Tools | `feature-detail`（1 个 item） | 多→1 可合并 | 单块 → `items[0]`；交替 `reverse` |
| `featureGridSection` | Features | `feature-grid` | 1→1 | `features[]` → `features[]` + `media.src`←`icon_url` |
| `testimonialSection` | 两者 | `testimonial` 或 `review-grid-3col` | 1→1 | `content`→`quote`，`name`→`author` |
| `faqSection` | 两者 | `faq` | 1→1 | `faq`→`items` |
| `ctaSection` | 少数 | `cta-default` | 1→1 | 补 `buttons[]` |

**可选「升级」插入（旧页没有，新页可加）：**

| 目的 | 可插入的新 section |
|------|-------------------|
| 品牌首屏 | `hero-split` / `hero-cinematic`（放在 `prompt-launcher` **前面**） |
| 信任 | `logo-loop`、`stats`、`proof-block` |
| 竞品 | `comparison-table` |
| 修图类 | `comparison-before-after` |
| 定价 | `pricing-block` |
| 收尾转化 | `cta-default`（`action: "openLogin"`） |

默认整页升级菜谱：**Features → F1**，**Tools → T1**（见 [STORYLINES.md](./STORYLINES.md)）。

---

## 4. 字段级对照（带 JSON 示例）

### 4.1 `heroSection` / `centeredInputSection` → `prompt-launcher`

**旧：**

```json
{
  "type": "heroSection",
  "title": "AI Anime Generator",
  "description": "Create stunning art...",
  "input_placeholder": "Describe your anime...",
  "button_text": "Start Creating",
  "image_url": "https://assets-persist.lovart.ai/...",
  "suggestion": [
    { "value": "...", "label": "Magic girl character" }
  ],
  "tip": "Free to start."
}
```

**新：**

```json
{
  "type": "prompt-launcher",
  "title": "AI Anime Generator",
  "description": "Create stunning art...",
  "input_placeholder": "Describe your anime...",
  "prompts": [
    { "label": "Magic girl character", "prompt": "..." }
  ],
  "cta": { "text": "Start Creating" },
  "tip": "Free to start."
}
```

| 旧字段 | 新字段 |
|--------|--------|
| `suggestion[].label` | `prompts[].label` |
| `suggestion[].value` | `prompts[].prompt` |
| `button_text` | `cta.text` |
| `image_url` | 不进入 launcher；若要首屏大图 → **额外**加一条 `hero-split.media.src` |

---

### 4.2 `contentSection` → `feature-detail`（推荐）

**旧：** 一个 section 里塞多个子块

```json
{
  "type": "contentSection",
  "sections": [
    {
      "title": "Professional Results",
      "description": "...",
      "image_url": "https://...",
      "button_text": "Try now",
      "button_link": "/signup"
    }
  ]
}
```

**新：** 一个 `feature-detail`，多个 `items`

```json
{
  "type": "feature-detail",
  "title": "Professional Results",
  "items": [
    {
      "title": "Professional Results",
      "description": "...",
      "media": { "src": "https://...", "alt": "..." },
      "cta": { "text": "Try now", "href": "/signup", "variant": "primary" }
    }
  ]
}
```

---

### 4.3 `threeColumnSection` → `workflow-horizontal`

| 旧 `columns[i]` | 新 `steps[i]` |
|-----------------|---------------|
| `title` | `title` |
| `description` | `description` |
| `image_url` | （可选）拆成 `workflow-vertical` 才有 `media` |

```json
{
  "type": "workflow-horizontal",
  "title": "How it works",
  "steps": [
    { "step": 1, "title": "Upload", "description": "..." },
    { "step": 2, "title": "Generate", "description": "..." },
    { "step": 3, "title": "Export", "description": "..." }
  ]
}
```

---

### 4.4 `textImageSection` → `feature-detail` 单条

| 旧 | 新 |
|----|-----|
| `title`, `description` | `items[0].title`, `items[0].description` |
| `image_url` | `items[0].media.src` |
| `button_text`, `button_link` | `items[0].cta` |
| （左右布局） | 奇数条 `reverse: true` |

---

### 4.5 `featureGridSection` → `feature-grid`

| 旧 `features[i]` | 新 `features[i]` |
|------------------|------------------|
| `icon_url` | `media: { src: icon_url, alt: title }`（图标当图用） |
| `title`, `description` | 同名 |

```json
{
  "type": "feature-grid",
  "title": "Why teams choose us",
  "columns": 3,
  "features": [
    {
      "title": "Brand Kit",
      "description": "...",
      "media": { "src": "https://...", "alt": "Brand Kit" }
    }
  ]
}
```

---

### 4.6 `testimonialSection` → `testimonial`

| 旧 | 新 |
|----|-----|
| `testimonials[].content` | `testimonials[].quote` |
| `testimonials[].name` | `testimonials[].author` |
| `testimonials[].role` | `testimonials[].role` |
| `avatar_url` | 新版组件可能不展示；迁移报告标 `needs_review` |

---

### 4.7 `faqSection` → `faq`

| 旧 | 新 |
|----|-----|
| `faq[]` | `items[]` |
| `question`, `answer` | 同名 |

---

## 5. 整页替换示例（Features 五段式）

### 旧（5 个 section，228 篇 en 里约 69% 同款）

```
centeredInputSection
  → threeColumnSection
  → featureGridSection
  → testimonialSection
  → faqSection
```

### 新（F1 模板，6 个 section）

```
prompt-launcher          ← centeredInputSection
workflow-horizontal      ← threeColumnSection
feature-grid             ← featureGridSection
testimonial              ← testimonialSection
faq                      ← faqSection
cta-default              ← 新增（旧页多数没有）
```

---

## 6. 整页替换示例（Tools 长链）

### 旧（典型 9 段）

```
heroSection → contentSection → threeColumnSection → textImageSection
  → contentSection → testimonialSection → textImageSection → threeColumnSection → faqSection
```

### 新（T1 模板，7 段，合并重复）

```
prompt-launcher          ← heroSection
bento-2                  ← 第 1 个 contentSection（2 个子块）
workflow-horizontal      ← threeColumnSection
feature-detail           ← 合并所有 textImageSection + 第 2 个 contentSection
testimonial              ← testimonialSection
faq                      ← faqSection
cta-default              ← 新增
```

（第 2 个 `threeColumnSection` 若与第一个重复，迁移脚本应 **去重** 或合并进步骤里。）

---

## 7. 需要改哪些地方？（清单）

| 层级 | 改不改 | 说明 |
|------|--------|------|
| `Pages/Features/*.json` 存量 | **暂不** | 保持 legacy，避免线上意外 |
| 新输出目录 e.g. `Pages/Features-v2/` | **要** | 迁移脚本写出新 `bodyJson` |
| 根字段 `schemaVersion: "composite-v2"` | **建议加** | 区分旧新，便于 preflight |
| `bodyJson` 内 `type` + 字段 | **要** | 核心工作 |
| `sanity-studio/scripts/preflight-content.js` | **已支持** | legacy + v2 双 schema；`--type composite-v2` |
| `convert-features.js` / `convert-tools.js` | **一般不用改** | 仍 stringify `bodyJson` 导入 |
| 前端 `CompositeSectionRenderer` | **已存在** | 不在本仓库改（lovart 主工程） |
| Sanity schema | **不用改** | `bodyJson` 仍是字符串 |

---

## 8. 如何实现？（三阶段）

### 阶段 0 — 人工单篇（理解用）

1. 复制一篇 `{slug}-en.json` → `{slug}-en.v2.json`
2. 只改 `bodyJson`：按 §3–§6 手改
3. 本地预览 `/internal/composite-page-all`（需前端环境）
4. 满意后再考虑批量

### 阶段 1 — 脚本骨架（当前）

```bash
cd Lovart/sanity-studio

# 单文件看映射结果（不写盘）
node scripts/migrate-legacy-bodyjson.js \
  --file "../Pages/Features/en/nano-banana-ai-model-en.json" \
  --template F1

# 批量 dry-run + 报告
node scripts/migrate-legacy-bodyjson.js \
  --dir "../Pages/Features/en" \
  --template F1 \
  --dry-run
```

实现位置：

- `scripts/lib/legacy-to-composite.js` — `mapLegacySection()` / `migrateBodyJson()`
- `scripts/migrate-legacy-bodyjson.js` — CLI

### 阶段 2 — 发布

1. 输出写到 `Pages/Features-v2/`（或同路径加 `schemaVersion`）
2. `preflight-content.js` 用新白名单检查
3. `import-page.js` / `convert-features.js` **与现流程相同** import
4. 生产：**不要** `--replace；用新 `_id` 或确认 slug 切换策略

---

## 9. 迁移脚本输出说明

每条输入 JSON 会得到：

```json
{
  "schemaVersion": "composite-v2",
  "migrationTemplate": "F1",
  "bodyJson": "[...新 section 数组...]",
  "migrationReport": {
    "warnings": ["testimonial: avatar_url dropped"],
    "sectionsIn": 5,
    "sectionsOut": 6
  }
}
```

`warnings` 需人工扫一遍；不能自动映射的进报告，不静默丢字段。

---

## 10. 常见问题

**Q：改 type 字符串就够吗？**  
不够。例如 `faqSection.faq` 必须改成 `faq.items`，否则新组件读不到数据。

**Q：旧页还能访问吗？**  
能。前端同时支持 legacy 与新 type；你不改存量文件就不影响现网。

**Q：新 Products 页怎么写？**  
直接用新 `type`，参考 `preview-data.json` + [STORYLINES.md](./STORYLINES.md)，不要再用 `heroSection`。

**Q：icon_url 怎么办？**  
新版 `feature-grid` 用 `media.src`；或手工映射到 README 里的 `icon` key（`cluster-block-dense`）。

---

## 11. 相关命令速查

```bash
# 映射库单测（Node 直接 require）
node -e "
const { migrateBodyJson } = require('./scripts/lib/legacy-to-composite');
const fs = require('fs');
const p = JSON.parse(fs.readFileSync('../Pages/Features/en/nano-banana-ai-model-en.json'));
console.log(JSON.stringify(migrateBodyJson(p, { template: 'F1' }), null, 2).slice(0,2000));
"

# 发布流程不变（v2 文件路径换好后）
node scripts/import-page.js "../Pages/Features-v2/en/{slug}-en.json" --dry-run
```
