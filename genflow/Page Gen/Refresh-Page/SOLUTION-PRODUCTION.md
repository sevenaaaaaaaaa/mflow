# Solution 页面生产指南

> 依据 [STORYLINE-BY-DIRECTION.md](./STORYLINE-BY-DIRECTION.md) §4.5 **六条**故事线，生成 12 段 `bodyJson` 草稿。  
> 机器可读 SSOT：[`solution-storylines.json`](./solution-storylines.json)  
> **参考案例**（英文）：`Page Gen/Pages/Solution/en/`

---

## 一、页面定位

| 项 | 值 |
|----|-----|
| URL 路径 | `/solution/{slug}` |
| Sanity `category` | `solution` |
| 故事线数 | **6 条**（`solution-team` … `solution-mission`） |
| section 数 | **12**（每条故事线段数相同，模块 `type` 有分叉） |
| 页面定位 | 整套方案售卖；**同时按人群与行业**选叙事模块 |

---

## 二、故事线速查

| ID | 编号 | 主轴 | 适用 | 首屏 | 证言段 |
|----|------|------|------|------|--------|
| `solution-team` | S1 | 人群 | 营销团队、创业公司 | `hero-cinematic` | `testimonial` |
| `solution-ecommerce` | S2 | 行业 | Shopify、DTC、电商 | `hero-journey` | `review-grid-3col` |
| `solution-agency` | S3 | 人群 | 代理商、工作室 | `hero-mosaic` | `review-grid-4col` |
| `solution-enterprise` | S4 | 人群 | 大企业、全球团队 | `hero-cinematic` + `bento-6` | `review-grid-3col` |
| `solution-solo` | S5 | 人群 | 自由职业、个体户、小商家 | `hero-split` | `testimonial` + `comparison-before-after` |
| `solution-mission` | S6 | 行业 | 非营利、使命驱动 | `hero-journey` | `testimonial` |

完整 `type` 序列见 `solution-storylines.json` 或 STORYLINE-BY-DIRECTION §4.5.4。

---

## 三、选型流程（先选故事线，再写 JSON）

```
1. 读 slug / 内容策略稿 → 判断主轴是「人群」还是「行业」
2. 对照下方信号表 → 选定 storylines ID
3. 从 solution-storylines.json 复制 sections 数组 → 严格按序填 12 段
4. 从 preview-data.json 复制对应 type 的字段骨架
5. 替换文案与 media → 写入 Pages/Solution/{lang}/{slug}-{lang}.json
```

### 3.1 信号表

| 内容信号 | 故事线 |
|----------|--------|
| Shopify / DTC / PDP / SKU / 转化漏斗 | `solution-ecommerce` |
| 代理商 / 工作室 / 多客户 / pitch / 作品集 | `solution-agency` |
| 大企业 / 全球 / SSO / 治理 / 多区域 | `solution-enterprise` |
| 自由职业 / 个体户 / 一人公司 / 小商家 | `solution-solo` |
| 非营利 / 公益 / 筹款 / 影响力 | `solution-mission` |
| 营销团队 / 创业公司 / 增长团队（**默认**） | `solution-team` |

### 3.2 内容策略稿 → 故事线映射

| Markdown 稿（`03-Solution/`） | 故事线 |
|-------------------------------|--------|
| `ai-design-solution-for-marketing-teams` | `solution-team` |
| `ai-design-solution-for-startups` | `solution-team` |
| `ai-design-solution-for-shopify`（待写） | `solution-ecommerce` |
| `ai-design-solution-for-agencies` | `solution-agency` |
| `ai-design-solution-for-enterprise` | `solution-enterprise` |
| `ai-design-solution-for-freelancers` | `solution-solo` |
| `ai-design-solution-for-solopreneurs` | `solution-solo` |
| `ai-design-for-small-business-hub` | `solution-solo` |
| `ai-design-solution-for-nonprofits` | `solution-mission` |
| `ai-design-for-fitness-wellness-hub` | `solution-solo` |

---

## 四、参考案例（2026-06-07）

| 案例 | 文件 | 故事线 | 受众 |
|------|------|--------|------|
| Marketing Teams | `ai-design-solution-for-marketing-teams-en.json` | `solution-team` | 团队型 B2B |
| Shopify/DTC | `ai-design-solution-for-shopify-en.json` | `solution-ecommerce` | 电商行业 |
| Agencies | `ai-design-solution-for-agencies-en.json` | `solution-agency` | 代理商 |

重新生成范例：

```bash
node "1-3 Content Gen/Page Gen/Pages/Solution/_generate-examples.js"
```

---

## 五、12 段本体职责（跨故事线共用）

| 序 | 本体 | 用途 |
|----|------|------|
| 1 | 首屏 | 方案名 + 价值主张（**按受众选 Hero 变体**） |
| 2 | 多栏特性区 | 方案四大（或六大）支柱 |
| 3 | 能力 Tab | 方案模块切换 |
| 4 | 特性大卡 | 核心交付物（`bento-2` 或 `feature-detail`） |
| 5 | 步骤教程 | 实施路径（横/竖版） |
| 6 | 对比 | vs 传统方案（表格式或前后对比） |
| 7 | 内容簇 | 场景/痛点/行业用例（6 卡） |
| 8 | 动态图文 | 效果展示（堆叠/横滑/作品墙） |
| 9 | 证言 | 客户故事（引用或 review 网格） |
| 10 | 定价 | 套餐（价格走后端） |
| 11 | FAQ | 采购/实施问答 |
| 12 | 底部 CTA | 转化收口 |

**明确不用：** `tool-grid`、`prompt-launcher`、`logo-loop`、页内 CTA

---

## 六、JSON 必备字段

```json
{
  "_type": "compositePage",
  "category": "solution",
  "sourceType": "solution",
  "storyline": "solution-ecommerce",
  "schemaVersion": "composite-v2",
  "url_path": "/solution/{slug}",
  "bodyJson": "[...]",
  "section": [...]
}
```

`storyline` 必须与 `solution-storylines.json` 中的 ID 一致；`section` 的 `type` 顺序必须与该 ID 的 `sections` 数组一致。

---

## 七、验收清单

- [ ] `storyline` 与 12 段 `type` 序列匹配所选故事线（勿混用两条线的模块）
- [ ] 恰好 **12** 个 section
- [ ] `hero-journey` 含 `journeyCards`（5 步）；`hero-mosaic` 含 `mosaicTiles`（4 块）
- [ ] `capability-tabs` 含 4 个 `tabs`，每项有 `content.media`
- [ ] `workflow-vertical` 每步含 `media`；`workflow-horizontal` 含 3 步
- [ ] `comparison-table` 含 `highlightColumn: 3`
- [ ] `comparison-before-after` 含 `before` / `after`（仅 `solution-solo`）
- [ ] `cluster-block-dense` 含 6 张 `cards`
- [ ] `faq` ≥ 6 条
- [ ] 图片 URL 无 404

---

## 八、相关文档

- [STORYLINE-BY-DIRECTION.md](./STORYLINE-BY-DIRECTION.md) §4.5
- [solution-storylines.json](./solution-storylines.json)
- [STORYLINES.md](./STORYLINES.md) — S1～S6 编号
- [FEATURES-PRODUCTION.md](./FEATURES-PRODUCTION.md)
