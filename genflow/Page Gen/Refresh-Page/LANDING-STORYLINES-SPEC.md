# Landing Page 故事线定稿（2026-06-07）

> **本文件为 §4.6 的生效 SSOT**，待合并进 [STORYLINE-BY-DIRECTION.md](./STORYLINE-BY-DIRECTION.md) 与 [For-Landing-Page-制作人.md](../../1-1%20GEO%20Readme/文档/03-角色手册/For-Landing-Page-制作人.md)。  
> 机器可读：[`landing-storylines.json`](./landing-storylines.json)

---

## 定位

面向**投放人员**的 composite-v2 落地页类型。

- **投放线（6 条）**：各 **12 段**，适合 Meta / Google 实际上线  
- **满配 demo（1 条）**：**15 段**，模块验收用，**不建议投放**  
- **7 线并集**覆盖：试用、Logo、证言、定价、Gallery、对比变体、多种 Hero

---

## 六条投放故事线

| 故事线 ID | 投放意图 | 适用场景 |
|-----------|----------|----------|
| `landing-gallery-detail` | 广泛认知 | 广泛匹配、多工具入口 |
| `landing-gallery-funnel` | 漏斗教育 | 再营销、全链路教育创意 |
| `landing-brand-trust` | 品牌 upper funnel | 品牌 campaign、信任建立 |
| `landing-trial-now` | Search 试用转化 | 工具词、即时试用 |
| `landing-vs-competitor` | 竞品抢量 | 竞品词、vs/alternative |
| `landing-offer-close` | 再营销收口 | 促销、底部漏斗 |

**别名：** `landing-A` → `landing-gallery-detail`；`landing-B` → `landing-gallery-funnel`

---

## 满配 demo

| 故事线 ID | section 数 | 用途 |
|-----------|------------|------|
| `landing-full` | 15 | 制作人 QA、内部预览，非投放 |

---

## 自动分配信号

| 信号 | 故事线 |
|------|--------|
| 竞品 / alternative / vs | `landing-vs-competitor` |
| 试用 / try now / 工具 Search 词 | `landing-trial-now` |
| 品牌曝光 / upper funnel | `landing-brand-trust` |
| 促销 / retarget / pricing | `landing-offer-close` |
| 漏斗阶段叙事 | `landing-gallery-funnel` |
| 内部 demo / 模块验收 | `landing-full` |
| 默认 / 多工具矩阵 | `landing-gallery-detail` |

---

## 全量 type 顺序

见 [`landing-storylines.json`](./landing-storylines.json) 各条 `sections` 数组。

---

## 参考案例

| # | 故事线 | 主题 | JSON |
|---|--------|------|------|
| 1 | `landing-gallery-detail` | Shopify 增长 | `landing-examples/en/draft-lovart-shopify-growth-landing-gallery-detail-en.json` |
| 2 | `landing-gallery-funnel` | Creative Studio | `landing-examples/en/draft-lovart-creative-studio-landing-gallery-funnel-en.json` |
| 3 | `landing-brand-trust` | Brand Campaign | `landing-examples/en/draft-lovart-brand-campaign-landing-brand-trust-en.json` |
| 4 | `landing-trial-now` | AI Design Agent Trial | `landing-examples/en/draft-lovart-tool-trial-landing-trial-now-en.json` |
| 5 | `landing-vs-competitor` | vs Midjourney | `landing-examples/en/draft-lovart-competitor-alt-landing-vs-competitor-en.json` |
| 6 | `landing-offer-close` | Black Friday Retarget | `landing-examples/en/draft-lovart-promo-retarget-landing-offer-close-en.json` |
| 7 | `landing-full` | Platform Demo | `landing-examples/en/draft-lovart-platform-landing-full-en.json` |

生成：`node Refresh-Page/scripts/generate-landing-examples.js`

---

## 六类对照表更新

| Landing Page | 故事线 | 本体数 | 含定价 | 含试用 | 含 Gallery |
|--------------|--------|--------|--------|--------|------------|
| Landing Page | **7** | **12～15** | 仅 full + offer-close | trial-now + full | ✓ |
