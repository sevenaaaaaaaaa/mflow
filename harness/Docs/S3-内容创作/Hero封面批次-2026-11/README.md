# Hero 封面批次制作 · 2026-11

> 排查日期：2026-11-02 ｜ 数据源：Sanity production（o11tm2qe）全量实查 7,373 个已发布 compositePage + 本地资产快照（2026-09-17）
> 复跑脚本：`dev/scripts/tmp_pull_pages.py`（拉数）→ `tmp_pages.jsonl`（全量页面清单）→ `tmp_hero_matrix.py`（矩阵统计）

## 1. 背景与口径

Lovart Global 全站落地页 ≈ **987 个唯一页面**（tool 452 / feature 715 / topic 149 / solution 38 / product 1，tool 与 feature 同名 slug 已去重；另有 10 个无 pageType 的 QA/预览页待清理）。Hero 组件 5 种变体 + 1 种 legacy 输入框首屏：

| 变体 | 结构 | 需要封面 |
|---|---|---|
| `hero-split` | 左文右图，右侧 4:3 大图 | 1 张/格 |
| `hero-cinematic` | 居中标题 + 全宽剧院图（16:10） | 1 张/格（可选 +1 视频版） |
| `hero-mosaic` | 居中标题 + 4 块拼贴瓦 | 4 张/格 |
| `hero-gallery` | 居中标题 + 6 宫格 1:1 工具瓦 | 6 张/格 |
| `hero-journey` | 居中标题 + step 卡片条（图标） | **不需要** |
| `centeredInputSection` | 输入框首屏（feature legacy） | **不需要** |

按 20 个业务主题族交叉现状变体格子，**口径一（按现状真实格子）= 93 张**：

- A 系列 `hero-split`：20 张（每个主题族 1 张）
- B 系列 `hero-cinematic`：5 张（platform / image-gen / ecommerce / logo-brand / industry）
- C 系列 `hero-mosaic`：2 套 × 4 = 8 张（platform / industry）
- D 系列 `hero-gallery`：10 套 × 6 = 60 张

另两个口径备查：**口径三（瓦片全站共享）= 35 张**；**口径二（全交叉补齐）= 20 族 × 12 = 240 张**。

## 2. 文件索引

| 文件 | 内容 | 用法 |
|---|---|---|
| `README.md` | 本文件：背景、规范、验收 | 存档/评审 |
| `briefs.md` | 93 张逐张 brief（Prompt / Alt / 画面要点） | 逐条复制进 Lovart 生成 |
| `cover-briefs.jsonl` | 机器可读 93 行（每行一张，字段自包含） | 批量脚本/表格导入 |

## 3. 通用生成规范（所有批次）

1. **图内禁文字**：标题、标签、按钮全部由前端渲染；生成图内不得出现任何可读字符（含乱码 UI 文字）。多语言共用同一套图，按主题制作、不按语言制作。
2. **安全区**：hero 图以圆角卡片渲染，四边留 ≥5% 裁切余量，主体居中；mosaic/gallery 瓦片按下方标注预留遮罩区。
3. **视觉一致性**：统一"现代 AI 设计工具营销视觉"——柔和渐变背景 + 高级棚拍光 + 高细节锐边；主题族之间用场景内容区分，不用风格漂移。
4. **文件规格**：主尺寸 PNG 或 JPG ≤1.5MB；视频版（可选，仅 B 系列试点）6–10s 静音循环 MP4 ≤8MB + 同构图 poster。
5. **命名**：`hero-{variant}-{theme}-v{n}.{ext}`，如 `hero-split-platform-v1.png`；D 系列瓦片加序号 `-t1…t6`。
6. **随图交付 alt 文案表**（briefs.md 已给英文占位；zh 站点页面 alt 需中文化）。

**全局禁用项（Negative，所有张共用）**：
`text, letters, words, watermark, signature, logo text, gibberish UI labels, distorted faces, extra fingers, low resolution, jpeg artifacts, clutter, frame border, oversaturated colors`

## 4. 分变体验收标准

| 系列 | 尺寸/比例 | 验收要点 |
|---|---|---|
| A split | 2160×1620（4:3） | 重心在中右 60%；四边裁切安全；单主体清晰；与左侧文案栏气质衔接 |
| B cinematic | 2400×1500（16:10） | 上下 8% 渐隐过渡；横向电影感单主体；无图内文字 |
| C mosaic | 每瓦 1200×900（4:3） | 4 瓦同叙事节奏；每瓦下方 30% 低细节（叠加标题用） |
| D gallery | 每瓦 1200×1200（1:1） | 主体居中占 70%；底部 25% 留 label 遮罩；6 瓦色调有节奏、风格统一 |

## 5. 现状问题（随批次修复）

1. **死链**：`83c980aef699e166b93c41e1ae583fd7f447e09e.jpg`（快照中 65 处引用）CDN 已 404 → P0 六张 split 上线后替换其引用。
2. **复用失衡**：快照期 50 个 tool slug 仅共用 9 张 hero 图；本批次按主题族解耦。
3. **尺寸混乱**：1:1（1200×1200）与 16:10（2160×1350）混用于 4:3 槽位；本批次统一按验收表规格出图。
4. **QA 页残留**：10 个无 pageType 页面（`seedance_2_5`、`e_commerce`、`marketers-preview-20260608` 等）建议清理或补 pageType。

## 6. 批次与优先级

| 批次 | 内容 | 数量 | 说明 |
|---|---|---:|---|
| **P0** | A 系列 6 大流量族 split（S-PLA/VID/IMG/SOC/ECO/LOG） | 6 | 同时修复死链引用 |
| **P1** | B 系列 5 张 + C 系列 8 张 | 13 | 品牌页与行业方案首屏 |
| **P2** | 其余 A 系列 14 张 + D 系列 60 张 | 74 | D 系列可先出 1 套通用 6 瓦过渡 |

## 7. 主题族 × 变体矩阵（口径一）

| 主题族 | 页面数 | split | cinematic | mosaic | gallery | 封面小计 |
|---|---:|---:|---:|---:|---:|---:|
| platform 平台与 Agent 能力 | 197 | 1 | 1 | 4 | 6 | 12 |
| video 视频生成与编辑 | 132 | 1 | – | – | 6 | 7 |
| print 印刷与品牌物料 | 112 | 1 | – | – | 6 | 7 |
| image-gen 图像生成 | 81 | 1 | 1 | – | 6 | 8 |
| social 社媒内容 | 79 | 1 | – | – | 6 | 7 |
| ecommerce 电商与产品图 | 57 | 1 | 1 | – | 6 | 8 |
| docs-deck 文档与演示 | 56 | 1 | – | – | 6 | 7 |
| logo-brand Logo 与品牌 | 54 | 1 | 1 | – | 6 | 8 |
| avatar 头像与人物 | 36 | 1 | – | – | – | 1 |
| photo-edit 照片编辑与增强 | 33 | 1 | – | – | – | 1 |
| industry 行业方案（zh-solution） | 24 | 1 | 1 | 4 | – | 6 |
| ads 广告素材 | 23 | 1 | – | – | 6 | 7 |
| creator-av 创作者频道物料 | 23 | 1 | – | – | – | 1 |
| compare 对比与替代 | 17 | 1 | – | – | 6 | 7 |
| web-ui 网站与 UI | 14 | 1 | – | – | – | 1 |
| audio 音频与音乐 | 13 | 1 | – | – | – | 1 |
| interior 室内与房产 | 12 | 1 | – | – | – | 1 |
| education 教育物料 | 10 | 1 | – | – | – | 1 |
| 3d 3D 与模型 | 9 | 1 | – | – | – | 1 |
| fashion 时尚服饰 | 5 | 1 | – | – | – | 1 |
| **合计** | **987** | **20** | **5** | **8** | **60** | **93** |

> industry 族的 cinematic/mosaic 一张覆盖 12 个行业，已按"模板化可换装"设计；若数据表现好，二期按 TOP3 行业扩量（+12~20 张）。
