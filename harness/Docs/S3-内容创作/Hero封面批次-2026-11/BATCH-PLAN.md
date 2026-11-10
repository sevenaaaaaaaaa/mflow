# D 模块分批投喂计划（6 主力行业 · 154 张）

> 目录：`batches/`，每个文件可独立投喂，跑完再开下一个。
> 行业维度（6 个主力）：电商零售 / 食品餐饮 / 科技数码 / 时尚美妆 / 极简商务 / 国潮插画

## 一览

| 批次 | 文件 | 张数 | 规格 | 说明 |
|---|---|---:|---|---|
| D1 | `D1-media.jsonl` | 18 | 2160×1350 · 16:10 | 18 品类总览主图 |
| D2-01 | `D2-01-logo.jsonl` | 6 | 1200×1200 · 1:1 | logo design　— |
| D2-02 | `D2-02-ecommerce-main.jsonl` | 6 | 1200×1200 · 1:1 | ecommerce main image　— |
| D2-03 | `D2-03-business-card.jsonl` | 6 | 1200×1200 · 1:1 | business card design　— |
| D2-04 | `D2-04-cover.jsonl` | 6 | 1200×1200 · 1:1 | cover design　— |
| D2-05 | `D2-05-brand-identity.jsonl` | 6 | 1200×1200 · 1:1 | brand identity system　— |
| D2-06 | `D2-06-font.jsonl` | 6 | 1200×1200 · 1:1 | type specimen design　— |
| D2-07 | `D2-07-illustration.jsonl` | 6 | 1200×1200 · 1:1 | illustration design　— |
| D2-08 | `D2-08-menu.jsonl` | 6 | 1200×1200 · 1:1 | menu design　⚠ 含排版 |
| D2-09 | `D2-09-brochure.jsonl` | 6 | 1200×1200 · 1:1 | brochure design　⚠ 含排版 |
| D2-10 | `D2-10-packaging.jsonl` | 6 | 1200×1200 · 1:1 | packaging design　⚠ 含排版 |
| D2-11 | `D2-11-poster.jsonl` | 6 | 1200×1200 · 1:1 | poster design　⚠ 含排版 |
| D2-12 | `D2-12-banner.jsonl` | 6 | 1200×1200 · 1:1 | banner design　⚠ 含排版 |
| D2-13 | `D2-13-social-media.jsonl` | 6 | 1200×1200 · 1:1 | social media design　⚠ 含排版 |
| D2-14 | `D2-14-video-thumbnail.jsonl` | 6 | 1200×1200 · 1:1 | video thumbnail design　⚠ 含排版 |
| D2-15 | `D2-15-product-detail.jsonl` | 6 | 1200×1200 · 1:1 | product detail page design　⚠ 含排版 |
| D2-16 | `D2-16-ppt.jsonl` | 6 | 1200×1200 · 1:1 | presentation slide design　⚠ 含排版 |
| D2-17 | `D2-17-resume.jsonl` | 6 | 1200×1200 · 1:1 | resume design　⚠ 含排版 |
| D2-18 | `D2-18-data-story.jsonl` | 6 | 1200×1200 · 1:1 | infographic design　⚠ 含排版 |
| D3 | `D3-tools.jsonl` | 28 | 1200×1200 · 1:1 | 6 瓦套 ×4 + 4 瓦套 ×1 |
| **合计** | | **154** | | |

## 执行顺序建议

1. **D1 先跑**（18 张）—— 这 18 张是每品类的总览图，跑完能一眼看出 18 个品类是否都成立，成本最低的验证。
2. **D2 按序号跑**，先跑前 6 批（logo / ecommerce-main / business-card / cover / brand-identity / font，共 36 张），这 6 个品类不含排版语义，生成最稳。
3. **中间 5 批**（illustration / menu / brochure / packaging / poster，30 张）开始引入排版。
4. **最后 7 批**（banner / social-media / video-thumbnail / product-detail / ppt / resume / data-story，42 张）全部含排版，用前面验证过的「抽象条块」手法。
5. **D3 最后跑**（28 张）—— 工具瓦片有明确 toolTiles label 参照，风险最低。

## 每批操作纪律

| 项 | 要求 |
|---|---|
| 同批同会话 | 一个品类的 6 张必须同一会话连续生成 |
| 锁 seed | 同批 6 张共用同一 seed + 同一风格参考图 |
| 机位互斥 | 6 张自动分配不同机位（正视/侧角/微距/俯拍/低角度/侧轮廓） |
| 背景一致 | 同批 6 张背景为同一 flat 色 |
| 只换行业 | 6 张之间只变行业配色/材质/气质，不变构图语言 |
| 排版品类 | 图内不得出现可读字符；排版层级用抽象灰色条块表达 |
| 命名 | `hero-gallery-{cat}-{industry}-v1.png` |

## 6 行业视觉参数速查

| 行业 | 配色 | 材质 | 气质 |
|---|---|---|---|
| 电商零售 | vivid coral + clean white + charcoal | 光泽印面、锐利边 | punchy、价格前置、高能量 |
| 食品餐饮 | terracotta + cream + deep olive | 有机肌理、碎屑与蒸汽感 | 温暖、可触、诱人 |
| 科技数码 | deep navy + electric cyan + cool white | 哑光复合材质、细网格 | 精准、工程感、前倾 |
| 时尚美妆 | blush nude + soft charcoal | 缎面、珠光 | 编辑部式优雅、从容 |
| 极简商务 | mono-tone warm grey + one ink | 无涂布纸、发丝线 | 安静、精确、大留白 |
| 国潮插画 | vermilion + antique gold + warm off-white | 水墨肌理、印章红 | 传统而现代、克制的华丽 |

## 批次进度追踪

| 批次 | 状态 | 备注 |
|---|---|---|
| D1 media | ☐ 待生成 | |
| D2-01 logo | ☐ 待生成 | |
| D2-02 ecommerce-main | ☐ 待生成 | |
| D2-03 business-card | ☐ 待生成 | |
| D2-04 cover | ☐ 待生成 | |
| D2-05 brand-identity | ☐ 待生成 | |
| D2-06 font | ☐ 待生成 | |
| D2-07 illustration | ☐ 待生成 | |
| D2-08 menu | ☐ 待生成 | |
| D2-09 brochure | ☐ 待生成 | |
| D2-10 packaging | ☐ 待生成 | |
| D2-11 poster | ☐ 待生成 | |
| D2-12 banner | ☐ 待生成 | |
| D2-13 social-media | ☐ 待生成 | |
| D2-14 video-thumbnail | ☐ 待生成 | |
| D2-15 product-detail | ☐ 待生成 | |
| D2-16 ppt | ☐ 待生成 | |
| D2-17 resume | ☐ 待生成 | |
| D2-18 data-story | ☐ 待生成 | |
| D3 tools | ☐ 待生成 | |
