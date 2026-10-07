# Solution 页面生产指南（v2 双轴）

> SSOT：`solution-storylines-v2.json`（本目录）  
> 人类可读选型说明：[SOLUTION-TAXONOMY.md](./SOLUTION-TAXONOMY.md)  
> 模块字段字典：[../Refresh-Page/README.md](../Refresh-Page/README.md)  
> **英文参考案例**：`en/`（`noIndex: true`，投产前改 `false`）

---

## 一、页面定位

| 项 | 值 |
|----|-----|
| URL 路径 | `/solution/{slug}` |
| Sanity `category` | `solution` |
| 故事线数 | **12 条**（6 人群 P1–P6 + 6 行业 I1–I6） |
| section 数 | **12**（每条故事线段数相同，模块 `type` 有分叉） |
| 选型规则 | **行业信号优先于人群**；仍模糊 → `solution-p-marketing` |

---

## 二、覆盖矩阵（2026-06-07）

### 行业轴（6/6 ✅）

| ID | 范例 slug | 文件 |
|----|-----------|------|
| `solution-i-ecommerce` | `ai-design-solution-for-shopify` | `ai-design-solution-for-shopify-en.json` |
| `solution-i-saas` | `ai-design-solution-for-saas` | `ai-design-solution-for-saas-en.json` |
| `solution-i-local` | `ai-design-for-small-business-hub` | `ai-design-for-small-business-hub-en.json` |
| `solution-i-wellness` | `ai-design-for-fitness-wellness-hub` | `ai-design-for-fitness-wellness-hub-en.json` |
| `solution-i-mission` | `ai-design-solution-for-nonprofits` | `ai-design-solution-for-nonprofits-en.json` |
| `solution-i-creator` | `ai-design-solution-for-creators` | `ai-design-solution-for-creators-en.json` |

### 人群轴（2/6）

| ID | 范例 slug | 状态 |
|----|-----------|------|
| `solution-p-marketing` | `ai-design-solution-for-marketing-teams` | ✅ JSON |
| `solution-p-agency` | `ai-design-solution-for-agencies` | ✅ JSON |
| `solution-p-founder` | `ai-design-solution-for-startups` | 📝 Markdown 待转 JSON |
| `solution-p-design` | — | ⬜ 待写 |
| `solution-p-enterprise` | `ai-design-solution-for-enterprise` | 📝 Markdown 待转 JSON |
| `solution-p-individual` | `ai-design-solution-for-freelancers` | 📝 Markdown 待转 JSON |

---

## 三、生产流程

```
1. 读 slug / 内容策略稿 → 判断行业轴还是人群轴（行业优先）
2. 从 solution-storylines-v2.json 取 storylines[ID].sections
3. 对照 preview-data.json 填各 type 字段骨架
4. 写入 Pages/Solution/{lang}/{slug}-{lang}.json
5. 校验：section 数 = 12，type 顺序与 SSOT 完全一致
```

### 3.1 旧 ID 别名

发布 JSON 时请用 v2 ID。旧 ID 仅作兼容：

| 旧 ID | 新 ID |
|-------|-------|
| `solution-team` | `solution-p-marketing` |
| `solution-ecommerce` | `solution-i-ecommerce` |
| `solution-agency` | `solution-p-agency` |
| `solution-enterprise` | `solution-p-enterprise` |
| `solution-solo` | `solution-p-individual` |
| `solution-mission` | `solution-i-mission` |

---

## 四、生成与导入脚本

```bash
cd "1-4 Geo Dev/lovart.sanity.studio"
SOLUTIONS="../../1-3 Content Gen/Page Gen/Pages/Solution/en"

# 1. 预检（须 0 BLOCK）
node scripts/preflight-content.js --type composite-v2 --dir "$SOLUTIONS"

# 2. 单篇 dry-run（摘要，勿用 --dry-run 打全量 JSON）
node scripts/import-page.js "$SOLUTIONS/ai-design-solution-for-saas-en.json"

# 3. 安全导入（仅 --missing，不覆盖 Studio 手改）
node scripts/import-page.js "$SOLUTIONS/{slug}-en.json" --import
```

生成本地 JSON：

```bash
node "1-3 Content Gen/Page Gen/Pages/Solution/_generate-industry-examples.js"
node "1-3 Content Gen/Page Gen/Pages/Solution/_generate-examples.js"
node "1-3 Content Gen/Page Gen/Pages/Solution/sync-solution-ssot.js"
```

**2026-06-07**：英文 8 篇已全部导入 production（`seo.noIndex: true`）。  
本地 storyline 已全部 v2 ID；可用 `audit-solution-production.js --sanity` 复核 12 段序列。

```bash
# 结构审计（本地 + production）
node "../../1-3 Content Gen/Page Gen/Pages/Solution/audit-solution-production.js" --sanity

# 已存在文档需同步正文时（慎用，会覆盖 Studio 手改）
node scripts/import-page.js "$SOLUTIONS/{slug}-en.json" --import --replace
```

---

## 五、12 段本体职责

| 序 | 本体 | 用途 |
|----|------|------|
| 1 | 首屏 | 方案价值主张（按故事线选 Hero 变体） |
| 2 | 多栏特性区 | 方案四大/六大支柱 |
| 3 | 能力 Tab | 方案模块切换 |
| 4 | 特性大卡 | `bento-2` 或 `feature-detail` |
| 5 | 步骤教程 | `workflow-vertical` 或 `workflow-horizontal` |
| 6 | 对比 | `comparison-table` 或 `comparison-before-after` |
| 7 | 内容簇 | 垂直场景卡片 |
| 8 | 动态图文 | `showcase-stacked` / `showcase-horizontal` / `canvas-wall` |
| 9 | 证言 | `testimonial` 或 `review-grid-*col` |
| 10 | 定价 | `pricing-block` |
| 11 | FAQ | `faq` |
| 12 | 底部 CTA | `cta-default` |

完整 12 段 `type` 序列见 `solution-storylines-v2.json`。
