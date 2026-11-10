# Hero 封面批次 · 2026-11

> 当前口径 **v6**（2026-11-04）：gallery 按实测结构重做（`REWORK-v5-gallery.md`），并按分批要求收敛到 **每品类 6 个主力行业**。
> **交付总量 307 张，全部 QC 通过**。完整总表见 `ALL-BATCHES.md`，全部 brief 的可读版见 `md/`。

## 1. 模块与总量

| 模块 | 文件 | 张数 | 规格 | QC |
|---|---|---:|---|---|
| A · hero-split | `module-A-split.jsonl` | 20 | 2160×1620 · 4:3 | ✅ 0/0 |
| B · hero-cinematic | `module-B-cinematic.jsonl` | 5 | 2400×1500 · 16:10 | ✅ 0/0 |
| C · hero-mosaic | `module-C-mosaic.jsonl` | 8 | 每瓦 1200×900 · 4:3 | ✅ 0/0 |
| D · hero-gallery | `module-D-gallery.jsonl` | 154 | 见下 | ✅ 0/1 |
| **E1 · B端补充** | `module-D-gallery-b2b4.jsonl` + `batches/E1-*` | 72 | 1200×1200 · 1:1 | ✅ 0/0 |
| **合计** | | **259** | | ✅ |

D 模块细分：

| 子类 | 内容 | 张数 | 规格 | 分批文件 |
|---|---|---:|---|---|
| D1 media 主图 | 18 品类 × 1 | 18 | 2160×1350 · 16:10 | `batches/D1-media.jsonl` |
| D2 行业瓦片 | 18 品类 × 6 行业 | 108 | 1200×1200 · 1:1 | `batches/D2-01…18-*.jsonl` |
| D3 工具瓦片 6 瓦 | 4 套 × 6 | 24 | 1200×1200 · 1:1 | `batches/D3-tools.jsonl` |
| D4 工具瓦片 4 瓦 | 1 套 × 4（11 语言共用） | 4 | 1200×1200 · 1:1 | 同上 |

> 6 个主力行业：**电商零售 / 食品餐饮 / 科技数码 / 时尚美妆 / 极简商务 / 国潮插画**
> （从 12 行业收敛；覆盖广 + 视觉区分度强）

## 2. Hero 变体与封面需求（实测）

全站落地页 ≈ 987 唯一页面（tool 452 / feature 715 / topic 149 / solution 38 / product 1，同名 slug 去重）。

| 变体 | 结构 | 需要封面 | 实测覆盖 |
|---|---|---|---|
| `hero-split` | 左文右图，右侧 4:3 大图 | 1 张/页 | 1,255 页 |
| `hero-cinematic` | 居中标题 + 全宽剧院图 | 1 张/页 | 33 页 |
| `hero-mosaic` | 居中标题 + 4 块拼贴瓦 | 4 张/页 | 14 页 |
| `hero-gallery` | 居中标题 + `gallery` **12 瓦**（行业维度）或 `toolTiles` 6/4 瓦（工具维度）+ media 主图 | **瓦片 + 1 主图** | 69 页 |
| `hero-journey` | step 卡片条（图标） | **不需要** | 11 页 |
| `centeredInputSection` | 输入框首屏 | **不需要** | 22 页 |

## 3. 文件索引

| 文件 | 内容 |
|---|---|
| `README.md` | 本文件 |
| `BATCH-PLAN.md` | 分批投喂计划（D1 + D2×18 + D3） |
| `ALL-BATCHES.md` | **全部批次总表**：274 张构成、行业覆盖、11 步执行顺序、覆盖核对 |
| `E1-b2b-industries.md` | E1 批次说明（4 个 B 端行业） |
| `batches/` | **20 个独立投喂文件**（D1 + D2×18 + D3） |
| `module-A/B/C/D-*.jsonl` | 四模块完整投喂文件 |
| `generate-queue.jsonl` | 187 条按执行顺序合并（含 step / order） |
| `REWORK-v5-gallery.md` | gallery 结构性返工报告（12→6 行业的原因与参数） |
| `prompt-v2-style-system.md` | 风格航道制（6 条航道冻结 token） |
| `NEXT-STEPS.md` | 风格定调 18 候选 + 早期执行说明 |
| `audit-report.md` | 风格一致性与多样性审计 |
| `gallery-ledger.json` / `gallery-plan.json` | gallery 真实台账与测算（数据源） |
| `_archive/` | v1 旧版（弃用） |

## 4. 通用生成规范

1. **图内禁文字**：含排版的 11 个品类（poster/banner/menu/brochure/packaging/video-thumbnail/social-media/product-detail/ppt/resume/data-story）用「抽象灰色条块代替字形」，并声明 `no screens, no UI windows`。
2. **多语言零增量**：同页面 10–11 语言版本共用同一套图。
3. **安全区**：四边 ≥5%；mosaic 下方 30% / gallery 下方 25% 低细节供标题遮罩。
4. **同批一致**：一个品类的 6 张必须同一会话 + 锁 seed + 同风格参考 + 同背景色，只换行业。
5. **机位互异**：6 张分别用正视居中 / 侧角投影 / 微距裁切 / 正俯拍 / 低角度 / 侧轮廓。
6. **命名**：`hero-gallery-{cat}-{industry}-v1.png`。

## 5. 已知现状缺陷（本批次一并修复）

1. **死链**：`83c980ae...jpg`（65 处引用）CDN 已 404 → P0 六张上线后替换。
2. **占位图轮转**：50 个 12 瓦页面共 600 个瓦片位，实际只有 3 张图在轮转，其中一张是「圆圈内数字 1」占位图。
3. **尺寸混乱**：1:1 与 16:10 混用于 4:3 槽位。
4. **QA 页残留**：10 个无 pageType 页面（`seedance_2_5`、`e_commerce` 等）。

## 6. 执行顺序

| Step | 内容 | 张数 |
|---:|---|---:|
| 0 | 风格定调（6 航道 × 3 候选） | 18 |
| 1 | P0 split（替死链） | 6 |
| 2 | P1 cinematic | 5 |
| 3 | P1 mosaic | 8 |
| 4 | P2 其余 split | 14 |
| 5 | D1 media 主图 | 18 |
| 6 | D2 行业瓦片（18 品类 × 6 行业） | 108 |
| 7 | D3/D4 工具瓦片 | 28 |

详见 `BATCH-PLAN.md`。
