# Scenarios 页面生产指南

> 依据 [STORYLINE-BY-DIRECTION.md](./STORYLINE-BY-DIRECTION.md) §4.4 **十四条** Scenarios 故事线，生成 **11 段** `bodyJson` 草稿。  
> 机器可读 SSOT：[`scenarios-storylines.json`](./scenarios-storylines.json)  
> **动笔前**：[PAGE-BRIEF.md](./PAGE-BRIEF.md) — 先定立场，再选 `scenarios-*` 故事线。  
> **试点草稿**：`Pages/drafts/scenarios-storyline/Scenarios/en/`（`draft-*`，`seo.noIndex: true`）

---

## 一、页面定位

| 项 | 值 |
|----|-----|
| URL 路径 | `/scenarios/{slug}` |
| Sanity `category` | `scenario` |
| 故事线数 | **14 条**（8 个分叉位） |
| section 数 | **11**（固定） |
| 页面定位 | **职业/场景叙事**：读者问「我这行/这角色能不能用 Lovart？」 |

Scenarios 比 Features/Tools 更「放开」：同一 11 段骨架下，可在 **首屏 / 场景入口 / Tab / 核心控制 / 步骤 / 对比 / 子场景 / 案例 / 证言** 九个位置选用不同变体。  
**规则：** 每个分叉位单独成线；基准段其余位置不变（见 `scenarios-storylines.json`）。

**与相邻类型的分工（Brief 防撞）：**

| 类型 | Hero 主语 | 本页不讲 |
|------|-----------|----------|
| **Scenarios** | 角色/场景（「电商运营的一周」） | 定价套餐、单点 Tool 操作 |
| **Solution** | 组织/行业方案（「Shopify 增长方案」） | 单角色日常细节 |
| **Product** | Lovart 产品名（ChatCanvas） | 职业工作流 |
| **Feature** | 单能力（Touch Edit） | 全链路场景 |

---

## 二、故事线速查（14 条）

| ID | 分叉 | 适合什么场景 |
|----|------|--------------|
| `scenarios-A` | Tab A | 通用基准 |
| `scenarios-B` | Tab B + autoplay | 社媒、输出优先 |
| `scenarios-journey` | `hero-journey` | 全链路旅程 |
| `scenarios-cinematic` | `hero-cinematic` | 品牌感、视觉主导 |
| `scenarios-portrait` | `portrait-grid-3` | 三大子场景入口 |
| `scenarios-vertical` | `workflow-vertical` | 步骤配图详解 |
| `scenarios-bento6` | `bento-6` | 六触点扫描 |
| `scenarios-bento2` | `bento-2` | 双成果简页 |
| `scenarios-before-after` | `comparison-before-after` | 视觉升级对比 |
| `scenarios-blog` | `blog-grid` | 场景 hub / SEO |
| `scenarios-showcase` | `showcase-horizontal` | 案例横滑 |
| `scenarios-stacked` | `showcase-stacked` | 案例纵叠 |
| `scenarios-testimonial` | `testimonial` | 长引言叙事 |
| `scenarios-reviews4` | `review-grid-4col` | 四列评价墙 |

完整 `sections` 数组见 [`scenarios-storylines.json`](./scenarios-storylines.json)。

---

## 三、选型流程（先主题，再故事线）

```
1. 填 PAGE-BRIEF → 确认 category = scenario（Hero 主语是角色/场景）
2. 读 slug / 职业背景 → 对照 themeSignals 选试点主题（或自定义主题物料）
3. 对照职业 → 故事线推荐表 → 选定 scenarios-* ID
4. 从 scenarios-storylines.json 复制 sections → 严格按序填 11 段
5. 从 preview-data.json 复制对应 type 字段骨架 → 替换文案与 media
6. 预检 → 写入 drafts → （可选）import-page --dry-run
```

### 3.1 试点范围（14 篇 · canonical）

**策略**：每条故事线选一个最合适选题，写一篇参考稿。**不做** 5 主题 × 14 故事线全矩阵。

SSOT：`scenarios-storylines.json` → `pilotAssignments`  
清单：`Pages/drafts/scenarios-storyline/MANIFEST-PILOT.md`

| 故事线 | 选题 | 说明 |
|--------|------|------|
| `scenarios-A` | marketing-director | 通用基准 Tab A |
| `scenarios-B` | social-media-manager | 社媒首选 Tab B |
| `scenarios-journey` | ecommerce-operator | 电商全链路首选 |
| `scenarios-cinematic` | brand-manager | 品牌影院首屏 |
| `scenarios-portrait` | social-media-manager | 三类渠道入口 |
| `scenarios-vertical` | freelance-designer | 交付步骤详解 |
| `scenarios-bento6` | marketing-director | 六触点战役 |
| `scenarios-bento2` | freelance-designer | 双成果简页 |
| `scenarios-before-after` | brand-manager | 视觉升级对比 |
| `scenarios-blog` | social-media-manager | 场景 hub / SEO |
| `scenarios-showcase` | ecommerce-operator | 多平台产出横滑 |
| `scenarios-stacked` | freelance-designer | 阶段式案例 |
| `scenarios-testimonial` | brand-manager | 品牌转型证言 |
| `scenarios-reviews4` | marketing-director | 四列评价墙 |

各主题新建同类页时，优先用**首选故事线**（见 §3.2），不必把 14 条线都跑一遍。

场景背景来源：`04-职业工作流内容规划.md`（Content Strategy）。

> 历史矩阵扩展稿（70 篇）仍保留在本地/Sanity（`noIndex`），评审与对外分享以 **MANIFEST-PILOT.md** 为准。

### 3.2 职业 → 故事线信号表

| 内容信号 | 首选故事线 | 常用备选 |
|----------|------------|----------|
| 电商 / SKU / PDP / 漏斗 | `scenarios-journey` | `scenarios-bento6`、`scenarios-before-after`、`scenarios-showcase` |
| 社媒 / 内容日历 / 多平台尺寸 | `scenarios-B` | `scenarios-portrait`、`scenarios-showcase`、`scenarios-blog` |
| 自由职业 / 客户交付 / 修订轮次 | `scenarios-vertical` | `scenarios-portrait`、`scenarios-stacked`、`scenarios-testimonial` |
| 营销总监 / 跨渠道战役 / 创意运营 | `scenarios-bento6` | `scenarios-journey`、`scenarios-reviews4` |
| 品牌经理 / 品牌系统 / 一致性治理 | `scenarios-cinematic` | `scenarios-before-after`、`scenarios-testimonial` |
| 场景 SEO hub / 教育导流 | `scenarios-blog` | `scenarios-portrait`、`scenarios-A` |

---

## 四、11 段本体职责（跨故事线共用）

| 序 | 本体 | 基准 `type` | 用途 |
|----|------|-------------|------|
| 1 | 首屏 | `hero-split` | 场景名 + 角色价值主张 |
| 2 | 场景入口 | `cluster-block-dense` | 痛点/运营卡点（6 卡） |
| 3 | 能力 Tab | `capability-tabs` | 四类能力切换（A/B 布局） |
| 4 | 核心控制 | `bento-4` | Lovart 四控制速览 |
| 5 | 步骤教程 | `workflow-horizontal` | 简三步落地 |
| 6 | 对比 | `comparison-table` | vs 旧工作流 |
| 7 | 子场景/内容 | `cluster-block-dense` | 子场景簇或 `blog-grid` |
| 8 | 案例深度 | `feature-detail` | 深度案例叙事 |
| 9 | 社会证明 | `review-grid-3col` | 评价/证言 |
| 10 | FAQ | `faq` | 角色专属问答 |
| 11 | 底部 CTA | `cta-default` | 转化收口 |

**明确不用：** `prompt-launcher`、`tool-grid`、`logo-loop`、页内 CTA、`pricing-block`、`hero-mosaic`、`hero-gallery`

---

## 五、一键生成

在 `dev/lovart.sanity.studio/` 下：

```bash
# P0 三主题（42 篇）
node scripts/generate-scenarios-storyline-drafts.js

# P1 两主题（28 篇）
node scripts/generate-scenarios-new-themes.js

# 单主题 × 14 故事线
node scripts/generate-scenarios-new-themes.js --theme brand-manager

# 单故事线 × 全部主题
node scripts/generate-scenarios-storyline-drafts.js --storyline scenarios-cinematic

# 预览
node scripts/generate-scenarios-storyline-drafts.js --dry-run
```

输出目录：`Pages/drafts/scenarios-storyline/Scenarios/en/`  
清单：`MANIFEST.md`（P0）+ `MANIFEST-new-themes.md`（P1）

---

## 六、JSON 必备字段

```json
{
  "slug": "draft-ecommerce-operator-scenarios-a",
  "language": "en",
  "category": "scenario",
  "schemaVersion": "composite-v2",
  "storylineId": "scenarios-A",
  "storylineTemplate": "scenarios-A",
  "draftStatus": "local-only",
  "draftTheme": "ecommerce-operator",
  "bodyJson": "[...]",
  "seo": {
    "noIndex": true
  }
}
```

---

## 七、验收清单

- [ ] `storylineId` 与 11 段 `type` 序列匹配所选故事线
- [ ] 恰好 **11** 个 section
- [ ] `capability-tabs`：B 线含 `autoplayIntervalMs: 6000`
- [ ] 两个 `cluster-block-dense`：序 2 痛点、序 7 子场景
- [ ] `faq` ≥ 4 条；`seo.noIndex: true`；slug 前缀 `draft-`

预检：

```bash
node scripts/preflight-content.js --dir "../Pages/drafts/scenarios-storyline/Scenarios/en" --composite-v2
```

---

## 八、安全同步到 Sanity（试点稿）

铁律：**`import --missing` only** · **`noIndex: true`** · ❌ `--replace`

详见 `harness/Skills/lovart-scenarios-sanity-publish/SKILL.md`。

---

## 九、相关文件

| 文件 | 作用 |
|------|------|
| `scenarios-storylines.json` | 14 条故事线 SSOT |
| `scripts/lib/scenarios-storylines.js` | 生成器逻辑 |
| `scripts/generate-scenarios-storyline-drafts.js` | P0 生成 |
| `scripts/generate-scenarios-new-themes.js` | P1 生成 |
