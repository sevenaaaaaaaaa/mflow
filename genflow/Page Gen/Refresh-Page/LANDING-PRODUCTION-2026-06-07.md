# Landing Page 生产指南（2026-06-07）

> 依据 [LANDING-STORYLINES-SPEC.md](./LANDING-STORYLINES-SPEC.md) 与 [`landing-storylines.json`](./landing-storylines.json)  
> 面向**投放人员**：6 条 12 段投放线 + 1 条 15 段满配 demo

---

## 故事线一览

| 故事线 ID | 投放意图 | section 数 | 参考案例 |
|-----------|----------|------------|----------|
| `landing-gallery-detail` | 广泛认知 / 多工具矩阵 | 12 | Shopify 增长 |
| `landing-gallery-funnel` | 漏斗教育 / 再营销 | 12 | Creative Studio |
| `landing-brand-trust` | 品牌 upper funnel | 12 | Brand Campaign |
| `landing-trial-now` | Search 试用转化 | 12 | Tool Trial |
| `landing-vs-competitor` | 竞品 / alternative | 12 | Competitor Alt |
| `landing-offer-close` | 促销 / 再营销收口 | 12 | Promo Retarget |
| `landing-full` | **内部 demo（非投放）** | **15** | Platform Demo |

**别名：** `landing-A` → `landing-gallery-detail`；`landing-B` → `landing-gallery-funnel`

---

## 自动分配信号

| 创意 / 关键词信号 | 故事线 |
|-------------------|--------|
| 竞品 / vs / alternative | `landing-vs-competitor` |
| try free / 工具 Search 词 | `landing-trial-now` |
| brand awareness / upper funnel | `landing-brand-trust` |
| pricing / promo / retarget | `landing-offer-close` |
| 漏斗阶段 / acquire→convert | `landing-gallery-funnel` |
| 内部 QA / 模块验收 | `landing-full` |
| 默认 / 多工具 gallery | `landing-gallery-detail` |

---

## 一键生成参考 JSON

```bash
node "1-3 Content Gen/Page Gen/Refresh-Page/scripts/generate-landing-examples.js"
node "1-3 Content Gen/Page Gen/Refresh-Page/scripts/generate-landing-examples.js" --dry-run
```

**输出：** `landing-examples/en/draft-*-en.json` + `landing-examples/manifest.json`

---

## 制作流程

### 1. 选故事线

对照上表「投放意图」，或查 `landing-storylines.json` → `routingSignals`。

### 2. 复制参考 JSON

```bash
cp landing-examples/en/draft-lovart-shopify-growth-landing-gallery-detail-en.json \
   landing-examples/en/draft-<your-theme>-<storyline>-en.json
```

修改 `slug`、`title`、`bodyJson` 文案与 `media.src`。字段骨架从 [preview-data.json](./preview-data.json) 复制。

### 3. 结构预检

在 `Refresh-Page/` 目录：

```bash
node -e '
const fs=require("fs"),path=require("path");
const ssot=JSON.parse(fs.readFileSync("landing-storylines.json","utf8"));
const DIR="landing-examples/en";
for(const f of fs.readdirSync(DIR).filter(x=>x.endsWith(".json"))){
  const p=JSON.parse(fs.readFileSync(path.join(DIR,f)));
  const sid=p.storylineId;
  const exp=(ssot.storylines[sid]||{}).sections;
  const act=JSON.parse(p.bodyJson).map(s=>s.type);
  if(!exp||exp.join()!==act.join())console.log("ORDER",f);
}'
```

期望 0 行输出。

### 4. 批量导入 Sanity

```bash
cd "dev/lovart.sanity.studio"
node scripts/import-landing-drafts.js --dry-run
node scripts/import-landing-drafts.js --import   # production · --missing only
```

**范围：** `landing-examples/en/`（含 `keywords/`，递归）· 2026-06-07 已导入 **48** 篇 `category: topic` · 全部 `seo.noIndex: true` · slug 前缀 `draft-`

NDJSON：`~/lovart/import-landing-drafts.ndjson`

---

## 相关文件

| 文件 | 作用 |
|------|------|
| [landing-storylines.json](./landing-storylines.json) | 机器可读 SSOT |
| [LANDING-STORYLINES-SPEC.md](./LANDING-STORYLINES-SPEC.md) | 定稿说明 |
| [landing-examples/MANIFEST.md](./landing-examples/MANIFEST.md) | 案例清单 |
| `scripts/generate-landing-examples.js` | 生成入口 |

> 旧版 [LANDING-PRODUCTION.md](./LANDING-PRODUCTION.md)（2 条线）已被本文 supersede。
