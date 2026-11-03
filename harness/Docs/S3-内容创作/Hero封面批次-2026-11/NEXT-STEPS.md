# 生成队列（NEXT STEPS）· 99 个生成任务

> 投喂文件：`generate-queue.jsonl`（93 条，含 `order` / `step` / `step_name` 字段，按序执行）
> 单任务字段：id / step / order / variant / lane / w / h / ratio / prompt / alt
> 本文档只做执行说明与顺序，prompt 正文以 jsonl 为准。

---

## Step 0 · 风格定调（18 个候选，必做前置）

目的：为 6 条航道各选 1 张**风格参考图**并冻结。此后该航道所有生成都带这张参考图，风格决策与单张 prompt 解耦——这是解决"丑/过时"的关键动作。

做法：每条航道 3 个候选（A/B/C）各生成 1 次，统一 1:1 / 同一测试主体（一个哑光杯子），横向对比后选 1 张。**选定后把该图存为 `style/{lane}.png`，后续生成作为 style reference 附上。**

### L1-photo-editorial

- **A 柔和棚拍**
  `High-end commercial photograph of one matte ceramic cup on a sand-colored seamless surface, 85mm, soft key light from upper left with a gentle falloff shadow, warm sand and cream palette with one deep-green accent, calm and premium, 1:1, no text, no letters, no watermark`
- **B 硬光 editorial**
  `High-end editorial photograph of one matte ceramic cup on a bone-white surface, 85mm, single hard directional light creating a crisp long shadow, warm neutral palette with one saturated accent, confident and graphic, 1:1, no text, no letters, no watermark`
- **C 窗光生活方式**
  `High-end lifestyle photograph of one matte ceramic cup on a linen cloth by a window, 85mm, soft diffused daylight with natural falloff, warm neutral palette with one muted accent, quiet and human, 1:1, no text, no letters, no watermark`

### L2-cinematic-still

- **A 暖调胶片**
  `Cinematic still of one glass bottle on a dark desk, shot on 35mm film, single warm volumetric light from a window with soft haze, teal-and-amber palette, shallow depth of field, subtle film grain, 1:1, no text, no letters, no watermark`
- **B 冷调夜戏**
  `Cinematic still of one glass bottle on a dark desk, shot on 35mm film, moonlit blue key with one practical amber rim light, desaturated cool palette, deep shadows, anamorphic feel, 1:1, no text, no letters, no watermark`
- **C 高反差单光源**
  `Cinematic still of one glass bottle on a dark desk, shot on 35mm film, one narrow hard light source from the side, near-monochrome with one warm highlight, dramatic contrast, 1:1, no text, no letters, no watermark`

### L3-soft-3d

- **A 哑光陶土**
  `Soft-body 3D render of one matte clay cup on a warm-grey seamless backdrop, macro 50mm, soft key light with gentle contact shadow, warm-grey palette with one coral accent, tactile and calm, 1:1, no text, no letters, no watermark`
- **B 圆润塑料 + 大阴影**
  `Soft-body 3D render of one rounded matte plastic cup on a pale sand backdrop, macro 50mm, soft top light casting one large soft shadow, muted palette with one electric accent, playful and clean, 1:1, no text, no letters, no watermark`
- **C 纸感材质**
  `Soft-body 3D render of one paper-textured cup on an off-white backdrop, macro 50mm, gentle HDRI light with fine surface fibers visible, ivory palette with one ink accent, crafted and quiet, 1:1, no text, no letters, no watermark`

### L4-graphic-flat

- **A 瑞士网格静物**
  `Editorial flat-graphic composition of one abstract cup silhouette on a cream field, Swiss grid alignment, paper grain texture with riso-print ink edges, cream and coral with charcoal accent, precise and restrained, 1:1, no text, no letters, no watermark`
- **B 大色块几何**
  `Editorial flat-graphic composition of one abstract cup shape built from two bold geometric blocks, cream field with a strong diagonal shadow shape, riso texture, 2-color palette, confident and poster-like, 1:1, no text, no letters, no watermark`
- **C 拼贴纸感**
  `Editorial flat-graphic collage of one abstract cup assembled from torn paper pieces, ivory field, visible fiber and deckle edges, muted palette with one saturated accent, handmade and editorial, 1:1, no text, no letters, no watermark`

### L5-material-still-life

- **A 棉纸烫金**
  `Macro still-life photograph of one cotton-paper card with an embossed abstract shape and a foil edge, raking side light revealing texture, ivory and charcoal with one copper accent, precise cast shadow, 1:1, no text, no letters, no watermark`
- **B 黑胶哑面**
  `Macro still-life photograph of one vinyl record half out of a matte sleeve, raking side light on the groove, charcoal and ivory with one copper accent, deep shadows, 1:1, no text, no letters, no watermark`
- **C 陶土与铜**
  `Macro still-life photograph of one matte clay tile beside a copper strip on a stone surface, raking side light, warm grey and copper palette, tactile and quiet, 1:1, no text, no letters, no watermark`

### L6-paper-craft

- **A 分层纸雕**
  `Layered paper-craft diorama of one simple house shape in three depth layers, hand-cut paper edges, soft daylight casting real shadows, cream and sage with one coral accent, 1:1, no text, no letters, no watermark`
- **B 白纸极简**
  `Layered paper-craft diorama of one simple house shape in white paper on a white background, hand-cut edges with soft real shadows, near-monochrome with one grey shadow accent, minimal and architectural, 1:1, no text, no letters, no watermark`
- **C 彩色手作**
  `Layered paper-craft diorama of one simple house shape in warm colored paper layers, hand-cut edges, playful daylight shadows, warm palette with one contrasting accent, cheerful and crafted, 1:1, no text, no letters, no watermark`

---

## 正式生成（93 张，按 step 顺序）

### Step 1 · P0 止血（6 张）

6 张 split。**上线优先级最高**：`83c980ae.jpg` 已在 CDN 404，65 处引用全坏。出图后立即替换。

- `S-PLA` · platform · 4:3 · 覆盖 - 页
- `S-VID` · video · 4:3 · 覆盖 - 页
- `S-IMG` · image-gen · 4:3 · 覆盖 - 页
- `S-SOC` · social · 4:3 · 覆盖 - 页
- `S-ECO` · ecommerce · 4:3 · 覆盖 - 页
- `S-LOG` · logo-brand · 4:3 · 覆盖 - 页

### Step 2 · P1 品牌旗舰 cinematic（5 张）

5 张 16:10。用于 lovart-2-0、landing-full、zh-enterprise、行业方案等视觉权重最高的首屏。

- `C-PLA` · platform · 16:10 · 覆盖 12 页
- `C-IMG` · image-gen · 16:10 · 覆盖 2 页
- `C-ECO` · ecommerce · 16:10 · 覆盖 3 页
- `C-LOG` · logo-brand · 16:10 · 覆盖 4 页
- `C-IND` · industry · 16:10 · 覆盖 12 页

### Step 3 · P1 分步叙事 mosaic（8 张）

8 张 4:3。两套各 4 瓦，必须同一会话连出 + 锁 seed。

- `M-PLA-1` · platform · 4:3 · 覆盖 3 页
- `M-PLA-2` · platform · 4:3 · 覆盖 3 页
- `M-PLA-3` · platform · 4:3 · 覆盖 3 页
- `M-PLA-4` · platform · 4:3 · 覆盖 3 页
- `M-IND-1` · industry · 4:3 · 覆盖 5 页
- `M-IND-2` · industry · 4:3 · 覆盖 5 页
- `M-IND-3` · industry · 4:3 · 覆盖 5 页
- `M-IND-4` · industry · 4:3 · 覆盖 5 页

### Step 4 · P2 其余主题族 split（14 张）

14 张 4:3。补齐除 6 大流量族外的全部主题族。

- `S-PRT` · print · 4:3 · 覆盖 112 页
- `S-DOC` · docs-deck · 4:3 · 覆盖 56 页
- `S-AVA` · avatar · 4:3 · 覆盖 36 页
- `S-PED` · photo-edit · 4:3 · 覆盖 33 页
- `S-IND` · industry · 4:3 · 覆盖 24 页
- `S-ADS` · ads · 4:3 · 覆盖 23 页
- `S-CRE` · creator-av · 4:3 · 覆盖 23 页
- `S-CMP` · compare · 4:3 · 覆盖 17 页
- `S-WEB` · web-ui · 4:3 · 覆盖 14 页
- `S-AUD` · audio · 4:3 · 覆盖 13 页
- `S-INT` · interior · 4:3 · 覆盖 12 页
- `S-EDU` · education · 4:3 · 覆盖 10 页
- `S-3D` · 3d · 4:3 · 覆盖 9 页
- `S-FAS` · fashion · 4:3 · 覆盖 5 页

### Step 5 · P2 gallery · G-ADS（6 张）

60 张 1:1。按套跑，每套 6 瓦同一会话 + 锁 seed + 同背景色；套间顺序见下。

- **G-ADS**（ads，背景 cream，覆盖 1 页）：Ad Creative, Display Ad, Carousel Ad, Google Banner, Retargeting, UGC Ad

### Step 5 · P2 gallery · G-CMP（6 张）

60 张 1:1。按套跑，每套 6 瓦同一会话 + 锁 seed + 同背景色；套间顺序见下。

- **G-CMP**（compare，背景 ivory，覆盖 2 页）：速度对比, 成本对比, 质量对比, 协作对比, 商用权对比, 工作流对比

### Step 5 · P2 gallery · G-DOC（6 张）

60 张 1:1。按套跑，每套 6 瓦同一会话 + 锁 seed + 同背景色；套间顺序见下。

- **G-DOC**（docs-deck，背景 ivory，覆盖 6 页）：Pitch Deck, Presentation, Infographic, Report, Resume, Whitepaper

### Step 5 · P2 gallery · G-ECO（6 张）

60 张 1:1。按套跑，每套 6 瓦同一会话 + 锁 seed + 同背景色；套间顺序见下。

- **G-ECO**（ecommerce，背景 sand，覆盖 5 页）：淘宝主图, 京东详情, 拼多多场景图, 抖音带货, 白底图, 店铺装修

### Step 5 · P2 gallery · G-IMG（6 张）

60 张 1:1。按套跑，每套 6 瓦同一会话 + 锁 seed + 同背景色；套间顺序见下。

- **G-IMG**（image-gen，背景 warm beige，覆盖 3 页）：Text to Image, Image to Image, Product Photo, Illustration, Stock Photo, Style Transfer

### Step 5 · P2 gallery · G-LOG（6 张）

60 张 1:1。按套跑，每套 6 瓦同一会话 + 锁 seed + 同背景色；套间顺序见下。

- **G-LOG**（logo-brand，背景 warm grey，覆盖 7 页）：Logo Maker, Brand Identity, Style Guide, Color Palette, Typography, Icon Set

### Step 5 · P2 gallery · G-PLA（6 张）

60 张 1:1。按套跑，每套 6 瓦同一会话 + 锁 seed + 同背景色；套间顺序见下。

- **G-PLA**（platform，背景 warm grey，覆盖 5 页）：Design Agent, ChatCanvas, Multi-Model, Brand Kit, Template Library, Workflow

### Step 5 · P2 gallery · G-PRT（6 张）

60 张 1:1。按套跑，每套 6 瓦同一会话 + 锁 seed + 同背景色；套间顺序见下。

- **G-PRT**（print，背景 ivory，覆盖 58 页）：海报设计, 传单设计, 名片设计, 菜单设计, 画册封面, 邀请函

### Step 5 · P2 gallery · G-SOC（6 张）

60 张 1:1。按套跑，每套 6 瓦同一会话 + 锁 seed + 同背景色；套间顺序见下。

- **G-SOC**（social，背景 cream，覆盖 5 页）：小红书图文, 抖音封面, 公众号头图, 微博贴文, B站封面, 社媒日历

### Step 5 · P2 gallery · G-VID（6 张）

60 张 1:1。按套跑，每套 6 瓦同一会话 + 锁 seed + 同背景色；套间顺序见下。

- **G-VID**（video，背景 deep charcoal，覆盖 3 页）：Image to Video, Text to Video, Product Video, Social Clips, Video Editor, Storyboard

---

## Gallery 套间建议顺序（为什么这么排）

1. **G-PRT** 先跑 —— 覆盖 58 个 zh-topic 页影响面最大，且 L5 材质静物最接近站内已有成功画风，风险最低、验证效果最好。
2. **G-SOC / G-ECO** —— 中文站点流量集中，且 L4/L1 已过 style sheet 验证。
3. **G-LOG / G-VID / G-IMG** —— 英文主力页，L5/L2/L1。
4. **G-DOC / G-ADS / G-CMP / G-PLA** —— L4 占比高，最后跑，便于统一调整 L4 航道参考图。

> 若 L4 首套（G-SOC）出图气质与站内摄影风 hero 差异过大，暂停其余 L4 四套，先调 style sheet 再继续。

## 交付与验收

| 项 | 要求 |
|---|---|
| 命名 | `hero-{variant}-{theme}-v1.{ext}`，瓦片加 `-t1…t6` |
| 尺寸 | split 2160×1620 · cinematic 2400×1500 · mosaic 瓦 1200×900 · gallery 瓦 1200×1200 |
| 体积 | ≤1.5MB（JPG q85 或 PNG 优化） |
| 图内文字 | 零。含乱码 UI 文字即废稿 |
| 安全区 | 四边 ≥5% 裁切余量；mosaic 下方 30% / gallery 下方 25% 保持低细节 |
| 同套一致 | gallery/mosaic 一套内背景色、光向、色彩完全一致 |
| 随图交付 | alt 文案（jsonl 已给）+ 中文页面用中文 alt |

