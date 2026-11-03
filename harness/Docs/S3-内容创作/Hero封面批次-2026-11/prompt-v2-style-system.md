# Prompt v2 · 风格航道制与可用性升级（Hero 封面批次）

> 背景：v1 prompt（briefs.md / cover-briefs.jsonl）实测几乎无一稿过。本文件是 v2 体系与重写规范；P0 六张已按 v2 重写作为验证样例。
> 适用：后续全部 93 张按本体系重写（覆盖原 briefs.md 前，本文件为 Prompt SSOT）。

## 1. v1 失效根因（复盘）

1. **风格词空话化**：`clean modern AI design-tool aesthetic / premium studio lighting / soft gradient background` → 模型默认联想 = 紫蓝渐变 + 玻璃 3D 球（过时 SaaS 风）。
2. **风格未按场景分配**：20 主题共用一套后缀，视频页与名片页同味。
3. **复杂度无预算**：并列元素 >4（grid of outputs / light streams / floating chips / orbiting items）→ 生成必然糊。
4. **简单场景缺细节层级**：无材质/布光/点睛色的最低配置 → 生成空洞。
5. **让模型画 UI**：timeline/dashboard/workspace → 乱码假界面，既丑又违反 no-text。

## 2. 风格航道（Style Lanes）——冻结 token 块

每条航道 = 固定风格 token（不逐张改动）+ 专属负面词。主题只做"选航道"动作。

### L1 商业摄影（photo-editorial）
- Token：`high-end commercial photography, 85-100mm lens, soft key light with directional shadow, tangible materials, muted base palette with one saturated accent, seamless paper backdrop`
- 专属负面：`snapshot look, flat cellphone lighting, stock-photo pose`
- 适用主题：ecommerce / avatar / industry / photo-edit / fashion / interior / creator-av

### L2 电影剧照（cinematic-still）
- Token：`cinematic still, shot on 35mm film, volumetric light, layered depth of field, teal-and-amber cinematic palette, subtle film grain, anamorphic feel`
- 专属负面：`HDR over-processing, theme-park color, video-game render`
- 适用主题：video

### L3 柔体三维（soft-3d）
- Token：`soft-body 3D render, matte ceramic and clay materials, macro surface detail, studio HDRI lighting, warm-grey palette with one coral accent, gentle contact shadows`
- 专属负面：`glassmorphism, chrome reflections, neon glow, floating holograms`
- 适用主题：platform / 3d

### L4 图形平面（graphic-flat）
- Token：`editorial flat-graphic composition, bold geometry on Swiss grid, 2-3 color palette with paper grain texture, precise alignment, riso-print texture accents`
- 专属负面：`gradient mesh, skeuomorphism, drop-shadow stacking, clip-art emoji style`
- 适用主题：logo-brand / docs-deck / ads / compare / social（图形向）

### L5 材质静物（material-still-life）
- Token：`macro still-life on colored seamless backdrop, tactile materials — cotton paper, copper foil, vinyl, ceramic — raking side light revealing texture, precise cast shadows`
- 专属负面：`plastic sheen, busy tabletop, cluttered props`
- 适用主题：print / audio / logo-brand（物料向）

### L6 纸艺场景（paper-craft）
- Token：`layered paper-craft diorama, hand-cut paper layers with soft real shadows, warm daylight, playful but disciplined composition`
- 专属负面：`plastic toys, mixed-media mess, glitter`
- 适用主题：education / web-ui（图纸隐喻）

## 3. 模块模板与复杂度预算

### A · hero-split（4:3 · 2160×1620）
```
{Lane token}, {single hero subject}, {one specific moment/state}, {camera: focal length + angle}, {light: direction + quality}, {palette: 2 base + 1 accent}, hero fills about 60-65% of frame, 4:3, edges safe for rounded-corner crop, no text, no letters, no watermark
```
- 预算：主视觉 ×1 + 支撑元素 ≤2 + 背景处理 ×1
- **禁止画任何 UI/界面**；产品感一律用物理隐喻（卡片入槽 / 胶片条 / 打印稿与裁切线 / 展台）
- 层级下限（防"过于简单"）：主体必须有材质纹理 + 双向光比 + 1 个点睛色

### B · hero-cinematic（16:10 · 2400×1500）
```
{Lane token, wide establishing shot}, depth in three layers (foreground / midground / background), each layer holds at most one hero element, {palette}, 16:10, top and bottom 8% fade to page background, no text, no letters, no watermark
```

### C · hero-mosaic（每瓦 4:3 · 1200×900）
```
{Lane token}, one subject only, state {n} of a 4-step sequence on the same subject, locked style reference and seed from tile 1, 4:3, lower 30% kept visually simple for title overlay, no text, no letters, no watermark
```
- 4 瓦必须一次会话连续生成；每瓦元素数 = 1

### D · hero-gallery（每瓦 1:1 · 1200×1200）
```
{Lane token}, portrait of one single object, {material/light detail}, plain seamless backdrop in one flat color, hero fills 70%, bottom 25% clean for label scrim, 1:1, no text, no letters, no watermark
```
- 同套 6 瓦同一会话、同 lane 同 seed、同背景色；6 瓦之间只换对象

## 4. 负面词 v2（全局，替代 v1 negative）

```
text, letters, words, watermark, signature, logo text, gibberish UI labels, distorted faces, extra fingers, low resolution, jpeg artifacts, frame border, oversaturated colors, generic purple-blue gradient, glassmorphism cliché, floating 3D blobs, isometric startup illustration, fake UI screens, gibberish interface text, glowing connection lines, floating chips, collage of many elements
```

## 5. 工作流（提升一稿过率）

1. **风格定调先行**：每条航道先出 1 张 3×3 style sheet 小样 → 选定 1 张 → 冻结为该航道的风格参考图（style reference）。此后该航道所有生成携带参考图；**风格决策与单张 prompt 解耦**。
2. **同航道连跑**：按航道分批生成，不跨航道穿插。
3. **每 brief 三变体**：只微调 [moment] 与 [camera] 字段；按评分卡（比例 / 四边安全 / 层级 / 航道 match / 无禁用元素）选 1。
4. **重 roll 纪律**：不合格只改 [moment]/[camera] 两个字段重 roll，禁止改航道 token。
5. **验收**：沿用 README §4 的分变体验收标准 + 本文负面清单。

## 6. P0 六张 v2 重写（验证样例 · 4:3 · 2160×1620）

### S-PLA · platform · L3 柔体三维
- Prompt：`Soft-body 3D render, matte ceramic materials: a single index card with a folded corner slides into a rounded slot on a minimalist matte console, three small finished artworks — a photo print, a tiny canvas, a glossy cube — resting on a shallow tray beside the slot, warm-grey palette with one coral accent, macro 50mm look, soft key light from upper left with gentle contact shadows, seamless warm-grey paper backdrop, hero scene fills about 65% of frame, 4:3, edges safe for rounded-corner crop, no text, no letters, no watermark, no UI screens`
- Alt：`Lovart design agent turning one brief card into finished multi-format artworks`

### S-VID · video · L2 电影剧照
- Prompt：`Cinematic still, shot on 35mm film: a physical film strip curves across a dark editing desk, three frames of the same golden-hour scene visible on the strip with one frame lifted slightly off, deep teal-and-amber palette, volumetric key light from a window with soft haze, shallow depth of field at 50mm, the film strip is the single hero with only two blurred desk props, 4:3, subtle film grain, edges safe, no text, no letters, no watermark, no UI monitors`
- Alt：`Lovart AI video generator — golden-hour frames on a film strip`

### S-IMG · image-gen · L1 商业摄影
- Prompt：`High-end editorial photograph: a single wooden easel holding one large canvas with a vivid painted landscape, two brushes and one paint tube resting at the easel base, soft daylight from a studio window, warm neutral palette with one saturated accent coming only from the painting, 85mm shallow depth of field, seamless paper backdrop, canvas fills about 65% of frame, 4:3, edges safe for rounded-corner crop, no text, no letters, no watermark, no screens`
- Alt：`Lovart image generation — one vivid landscape painting on an easel`

### S-SOC · social · L1 商业摄影
- Prompt：`High-end commercial photography, overhead view: one vertical 9:16 photo print of a bright lifestyle scene lies on a warm beige seamless surface, surrounded by three blank white paper cutouts in different aspect ratios — square, wide, vertical — neatly aligned with visible crop marks, palette of beige and off-white with one tangerine accent, soft daylight with precise shadows, 50mm, the photo print is the hero covering about 60% of frame, 4:3, edges safe, no text, no letters, no watermark, no screens`
- Alt：`Lovart social media design — one story print with platform-size crop marks`

### S-ECO · ecommerce · L1 商业摄影
- Prompt：`High-end commercial product photography: one matte ceramic skincare bottle centered on a sand-colored podium, beside it a identical white-background cutout version of the same bottle separated by a thin clean gap — half photographic, half listing-ready, soft beige-to-cream backdrop, single key light with gentle gradient falloff, 100mm macro, palette of sand and cream with one deep-green accent, hero fills about 60% of frame, 4:3, edges safe for rounded-corner crop, no text, no letters, no watermark`
- Alt：`Lovart product photography — from studio shot to listing-ready cutout`

### S-LOG · logo-brand · L5 材质静物
- Prompt：`Macro still-life photograph: an embossed abstract geometric logo mark pressed into a thick cotton-paper card with a foil-stamped edge catching the light, resting on a stack of two blank cards, palette of ivory paper and charcoal ink with one copper-foil accent, precise raking side light revealing emboss texture, 100mm macro, seamless warm-grey backdrop, the card fills about 65% of frame, 4:3, edges safe for rounded-corner crop, no text, no letters, no watermark`
- Alt：`Lovart brand kit — embossed logo mark on cotton paper`

## 7. 后续

- P0 六张 v2 投喂验证 → 通过后，按本体系重写其余 87 张并覆盖 `cover-briefs.jsonl`（版本号 v2，保留 v1 存档）。
- 每条航道 style sheet 确认后，将参考图 URL 回填至本文件 §2，作为该航道生成时的固定附件。
