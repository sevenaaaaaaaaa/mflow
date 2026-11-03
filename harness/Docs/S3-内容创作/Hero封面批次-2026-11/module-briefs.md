# Hero 封面 Brief · 按模块（93 张 · v2 航道制）

> 投喂文件：`module-A-split.jsonl` / `module-B-cinematic.jsonl` / `module-C-mosaic.jsonl` / `module-D-gallery.jsonl`
> 风格体系：`prompt-v2-style-system.md`（6 条航道冻结 token + 模块模板）
> 执行顺序与风格定调：`NEXT-STEPS.md` ｜ 质检记录：`p0/p1/p2-qc-report.md`
> 全部 93 张已过自动质检：BLOCK 0 / WARN 0。

| 模块 | 张数 | 规格 | 覆盖 |
|---|---:|---|---|
| A · hero-split | 20 | 2160×1620 · 4:3 | 20 个主题族 · 987 页中的 split 页 |
| B · hero-cinematic | 5 | 2400×1500 · 16:10 | 品牌旗舰页 + 行业方案 |
| C · hero-mosaic | 8 | 每瓦 1200×900 · 4:3 | platform / industry 拼贴页 |
| D · hero-gallery | 60 | 每瓦 1200×1200 · 1:1 | 10 套工具矩阵页 |

---

## 模块 A · hero-split（左文右图） —— 20 张

**规格**：2160×1620 · 4:3 · JPG/PNG ≤1.5MB  
**构图要求**：左侧是页面文案栏，视觉重心须落在中右 60% 区域；主体完整、四边 ≥5% 裁切余量（圆角卡片渲染）。可加 5–8s MP4 循环版（必须配 poster）。  
**复杂度预算**：主视觉 ×1 + 支撑元素 ≤2 + 背景处理 ×1；禁止画任何界面  
**出图顺序**：先出 P0 六张（出图即替换 83c980ae.jpg 死链），再出其余 14 个主题族。

| 编号 | 优先级 | 主题 · 航道 | 覆盖页 | Alt |
|---|---|---|---:|---|
| `S-PLA` | P0 | platform · L3-soft-3d | - | Lovart design agent turning one brief card into finished multi-format artworks |
| `S-VID` | P0 | video · L2-cinematic-still | - | Lovart AI video generator — golden-hour frames on a film strip |
| `S-IMG` | P0 | image-gen · L1-photo-editorial | - | Lovart image generation — one vivid landscape painting on an easel |
| `S-SOC` | P0 | social · L1-photo-editorial | - | Lovart social media design — one story print with platform-size crop marks |
| `S-ECO` | P0 | ecommerce · L1-photo-editorial | - | Lovart product photography — from studio shot to listing-ready cutout |
| `S-LOG` | P0 | logo-brand · L5-material-still-life | - | Lovart brand kit — embossed logo mark on cotton paper |
| `S-PRT` | P2 | print · L5-material-still-life | 112 | Lovart print design set — posters, brochures and menus with crop marks |
| `S-DOC` | P2 | docs-deck · L5-material-still-life | 56 | Lovart presentation prints — a rising chart shape on the top sheet |
| `S-AVA` | P2 | avatar · L1-photo-editorial | 36 | Lovart avatar styles — one person in five art styles |
| `S-PED` | P2 | photo-edit · L1-photo-editorial | 33 | Lovart photo editing — faded to vivid on one print |
| `S-IND` | P2 | industry · L1-photo-editorial | 24 | Lovart industry solution — design proofs on a standing board |
| `S-ADS` | P2 | ads · L4-graphic-flat | 23 | Lovart ad creative — bold product silhouette on Swiss grid |
| `S-CRE` | P2 | creator-av · L1-photo-editorial | 23 | Lovart thumbnail A-B test — two prints in a stand |
| `S-CMP` | P2 | compare · L4-graphic-flat | 17 | Lovart vs traditional tools — mess versus one clean card |
| `S-WEB` | P2 | web-ui · L6-paper-craft | 14 | Lovart web design — a paper-craft page layout in layers |
| `S-AUD` | P2 | audio · L5-material-still-life | 13 | Lovart audio visuals — vinyl with waveform groove and cover cards |
| `S-INT` | P2 | interior · L1-photo-editorial | 12 | Lovart interior design — a room model with material layers |
| `S-EDU` | P2 | education · L6-paper-craft | 10 | Lovart education materials — paper-craft classroom set |
| `S-3D` | P2 | 3d · L3-soft-3d | 9 | Lovart 3D generation — sketch card to clay model |
| `S-FAS` | P2 | fashion · L1-photo-editorial | 5 | Lovart fashion design — tailored garment on a dress form |

<details>
<summary>展开本模块全部 Prompt</summary>

**S-PLA** · platform · L3-soft-3d · 4:3
- Prompt：`Soft-body 3D render, matte ceramic materials: a single index card with a folded corner slides into a rounded slot on a minimalist matte console, three small finished artworks — a photo print, a tiny canvas, a glossy cube — resting on a shallow tray beside the slot, warm-grey palette with one coral accent, macro 50mm look, soft key light from upper left with gentle contact shadows, seamless warm-grey paper backdrop, hero scene fills about 65% of frame, 4:3, edges safe for rounded-corner crop, no text, no letters, no watermark, no screens`

**S-VID** · video · L2-cinematic-still · 4:3
- Prompt：`Cinematic still, shot on 35mm film: a physical film strip curves across a dark editing desk, three frames of the same golden-hour scene visible on the strip with one frame lifted slightly off, strictly a two-color deep teal-and-amber palette with no third color, volumetric key light from a window with soft haze, shallow depth of field at 50mm, the film strip is the single hero with only two blurred desk props, 4:3, subtle film grain, edges safe, no text, no letters, no watermark, no screens`

**S-IMG** · image-gen · L1-photo-editorial · 4:3
- Prompt：`High-end editorial photograph: a single wooden easel holding one large canvas with a vivid painted landscape, two brushes and one paint tube resting at the easel base, soft daylight from a studio window, warm neutral palette with one saturated accent coming only from the painting, 85mm shallow depth of field, seamless paper backdrop, canvas fills about 65% of frame, 4:3, edges safe for rounded-corner crop, no text, no letters, no watermark, no screens`

**S-SOC** · social · L1-photo-editorial · 4:3
- Prompt：`High-end commercial photography, overhead view: one vertical 9:16 photo print of a bright lifestyle scene lies on a warm beige seamless surface, beside it three blank white paper cutouts in different aspect ratios — square, wide, vertical — neatly aligned with visible crop marks, palette of beige and off-white with one tangerine accent, soft daylight with precise shadows, 50mm, the photo print is the hero covering about 60% of frame, 4:3, edges safe, no text, no letters, no watermark, no screens`

**S-ECO** · ecommerce · L1-photo-editorial · 4:3
- Prompt：`High-end commercial product photography: one matte ceramic skincare bottle centered on a sand-colored podium, beside it an identical white-background cutout version of the same bottle separated by a thin clean gap — half photographic, half listing-ready, soft beige-to-cream backdrop, single key light with gentle gradient falloff, 100mm macro, palette of sand and cream with one deep-green accent, hero fills about 60% of frame, 4:3, edges safe for rounded-corner crop, no text, no letters, no watermark`

**S-LOG** · logo-brand · L5-material-still-life · 4:3
- Prompt：`Macro still-life photograph: an embossed abstract geometric logo mark pressed into a thick cotton-paper card with a foil-stamped edge catching the light, resting on a stack of two blank cards, palette of ivory paper and charcoal ink with one copper-foil accent, precise raking side light revealing emboss texture, 100mm macro, seamless warm-grey backdrop, the card fills about 65% of frame, 4:3, edges safe for rounded-corner crop, no text, no letters, no watermark`

**S-PRT** · print · L5-material-still-life · 4:3
- Prompt：`Macro still-life photograph, top-down view: three printed pieces — one poster, one tri-fold brochure, one menu — overlapping in a tidy arrangement on a warm grey seamless surface, visible crop marks and bleed guides on the poster edge, cotton paper texture under raking side light, ivory and grey palette with one copper accent, 100mm macro, hero arrangement fills about 60% of frame, 4:3, edges safe for rounded-corner crop, no text, no letters, no watermark`

**S-DOC** · docs-deck · L5-material-still-life · 4:3
- Prompt：`Macro still-life photograph: a short stack of presentation prints fanned slightly on a stone surface, the top sheet showing an abstract rising bar shape in deep ink, one pen resting beside the stack, ivory and charcoal palette with one coral accent, raking side light revealing paper texture, 100mm macro, seamless warm-grey backdrop, hero fills about 60% of frame, 4:3, edges safe for rounded-corner crop, no text, no letters, no watermark`

**S-AVA** · avatar · L1-photo-editorial · 4:3
- Prompt：`High-end editorial photograph: five portrait prints fanned in a small brass stand, each showing the same person in a different art style — photographic, painted, clay, flat poster, ink sketch — warm neutral palette with one saturated accent, 85mm shallow depth of field, soft key light from the upper left with gentle shadows, seamless paper backdrop, the fan fills about 60% of frame, 4:3, edges safe, no text, no letters, no watermark, no screens`

**S-PED** · photo-edit · L1-photo-editorial · 4:3
- Prompt：`High-end editorial photograph: one landscape print with a clean vertical tear line down the middle — the left half dull and faded, the right half vivid and crisp — lying flat on a seamless warm surface with a soft brush and a loupe beside it, neutral palette with the vivid half carrying the only saturated colors, 85mm shallow depth of field, soft directional daylight from the left casting one crisp shadow along the tear, 4:3, edges safe, no text, no letters, no watermark, no screens`

**S-IND** · industry · L1-photo-editorial · 4:3
> 与 C-IND 同模板：背景商业空间可按行业换装
- Prompt：`High-end commercial photograph: one matte standing board on a worktable displaying three small printed design proofs pinned side by side, a softly blurred modern commercial interior — half office, half retail — behind it, neutral palette with one warm accent light, 85mm shallow depth of field, soft ambient studio key light with a warm accent from the right, the board fills about 60% of frame, 4:3, edges safe for rounded-corner crop, no text, no letters, no watermark, no screens`

**S-ADS** · ads · L4-graphic-flat · 4:3
- Prompt：`Editorial flat-graphic composition on a Swiss grid: one bold product silhouette in tangerine against a cream field with a strong diagonal shadow shape, paper grain texture and riso-print ink edges, 2-color palette with one deep charcoal accent, precise alignment, flat poster layout with no photographic perspective under flat even lighting, the hero silhouette fills about 60% of frame, 4:3, edges safe for rounded-corner crop, no text, no letters, no watermark`

**S-CRE** · creator-av · L1-photo-editorial · 4:3
- Prompt：`High-end commercial photograph: two video thumbnail prints standing upright in a small wooden stand, one brightly lit and one dimmer for A-B comparison, a tiny play triangle motif resting in front, warm neutral palette with one saturated accent, 85mm shallow depth of field, soft studio key light from the front-left with gentle shadows, seamless paper backdrop, hero fills about 60% of frame, 4:3, edges safe, no text, no letters, no watermark, no screens`

**S-CMP** · compare · L4-graphic-flat · 4:3
- Prompt：`Editorial flat-graphic composition: the frame divided by one clean vertical rule — left side a messy pile of dull grey paper scraps, right side a single crisp cream card with one coral geometric mark, Swiss grid alignment, paper grain texture, 2-3 color palette, flat poster layout with no photographic perspective under flat even lighting, hero contrast fills about 65% of frame, 4:3, edges safe, no text, no letters, no watermark`

**S-WEB** · web-ui · L6-paper-craft · 4:3
- Prompt：`Layered paper-craft diorama: a hand-cut paper web page layout standing upright in shallow depth — one hero banner layer, two card layers and a rounded chip layer — low macro angle at an equivalent 50mm perspective, soft daylight casting real paper shadows, cream and sage palette with one coral accent, hero diorama fills about 60% of frame, 4:3, edges safe, no text, no letters, no watermark`

**S-AUD** · audio · L5-material-still-life · 4:3
- Prompt：`Macro still-life photograph: a vinyl record half-slid from a matte sleeve with an abstract waveform groove catching raking side light, two small cover-art cards leaning behind it, charcoal and ivory palette with one copper accent, 100mm macro, seamless warm-grey backdrop, hero fills about 65% of frame, 4:3, edges safe, no text, no letters, no watermark`

**S-INT** · interior · L1-photo-editorial · 4:3
- Prompt：`High-end editorial photograph: a miniature living-room model on a worktable with one wall panel lifted to reveal layered material swatches inside, soft window daylight, warm neutral palette with one deep-green accent, 85mm shallow depth of field, seamless backdrop, the model fills about 60% of frame, 4:3, edges safe, no text, no letters, no watermark, no screens`

**S-EDU** · education · L6-paper-craft · 4:3
- Prompt：`Layered paper-craft diorama: a cheerful hand-cut classroom scene — one worksheet-shaped sheet, three flashcards and one tiny book — standing in layered paper depth with soft real shadows, cream and sage palette with one coral accent, warm daylight, shot at a low macro angle, equivalent 50mm perspective, hero fills about 60% of frame, 4:3, edges safe, no text, no letters, no watermark`

**S-3D** · 3d · L3-soft-3d · 4:3
- Prompt：`Soft-body 3D render in matte ceramic materials: a pencil sketch card on the left transforming into a matte clay model of the same object on the right, a thin row of material swatch chips along the base, warm-grey palette with one coral accent, macro 50mm look, soft key light with gentle contact shadows, seamless warm-grey paper backdrop, hero fills about 65% of frame, 4:3, edges safe, no text, no letters, no watermark`

**S-FAS** · fashion · L1-photo-editorial · 4:3
- Prompt：`High-end editorial photograph: a small dress form wearing a miniature tailored garment with two fabric swatches draped over its arm, magazine-quality soft key light, warm neutral palette with one saturated accent, 85mm shallow depth of field, soft directional window light from the side casting gentle fabric shadows, seamless paper backdrop, the dress form fills about 60% of frame, 4:3, edges safe for rounded-corner crop, no text, no letters, no watermark`

</details>


---

## 模块 B · hero-cinematic（居中标题 + 全宽剧院图） —— 5 张

**规格**：2400×1500 · 16:10 · JPG/PNG ≤1.5MB  
**构图要求**：横向电影感单主体；上下各 8% 做渐隐过渡（与页面背景衔接）；文字全在图外；图内不烧录任何文案。可选每条 6–10s 静音循环视频。  
**复杂度预算**：三层深度（前/中/后），每层最多 1 个主元素  
**出图顺序**：品牌旗舰页视觉权重最高，5 张一次性出齐。

| 编号 | 优先级 | 主题 · 航道 | 覆盖页 | Alt |
|---|---|---|---:|---|
| `C-PLA` | P1 | platform · L3-soft-3d | 12 | Lovart design agent studio — one brief card becoming a row of finished artworks |
| `C-IMG` | P1 | image-gen · L1-photo-editorial | 2 | Lovart image generation — one vivid painting in a sunlit studio |
| `C-ECO` | P1 | ecommerce · L1-photo-editorial | 3 | Lovart product photography — studio shot and listing cutout in one frame |
| `C-LOG` | P1 | logo-brand · L5-material-still-life | 4 | Lovart brand identity — embossed cards on a stone ledge |
| `C-IND` | P1 | industry · L1-photo-editorial | 12 | Lovart industry solution — printed design proofs in a commercial space |

<details>
<summary>展开本模块全部 Prompt</summary>

**C-PLA** · platform · L3-soft-3d · 16:10
- Prompt：`Soft-body 3D render in matte ceramic materials, wide establishing shot: a long rounded workbench recedes into warm-grey depth — foreground holds one folded-corner index card resting on a shallow tray, midground holds a single row of small finished artworks standing on the bench (one framed print, one clay object, one product box), background is an empty warm-grey studio volume with one soft coral light source, warm-grey palette with one coral accent, macro-soft HDRI lighting with gentle contact shadows, rendered at an equivalent 50mm perspective, 16:10, top and bottom 8% fading to warm grey, no text, no letters, no watermark, no screens, no panels`

**C-IMG** · image-gen · L1-photo-editorial · 16:10
- Prompt：`High-end editorial photograph, wide shot of a sunlit painter's studio in three layers — foreground a blurred jar of brushes catching window light, midground one large vivid landscape painting standing on a wooden easel in full focus, background a tall window with soft out-of-focus daylight, warm neutral palette with one saturated accent living only inside the painting, 85mm shallow depth of field, 16:10, top and bottom 8% fading to warm grey, no text, no letters, no watermark, no screens`

**C-ECO** · ecommerce · L1-photo-editorial · 16:10
- Prompt：`High-end commercial product photograph, wide shot in three layers — foreground the blurred edge of a matte ceramic bottle, midground the same bottle standing centered on a sand-colored podium in full focus, background a white listing cutout card of the bottle leaning against a cream seamless backdrop, sand and cream palette with one deep-green accent, single key light with gentle falloff, 100mm macro look, 16:10, top and bottom 8% fading to cream, no text, no letters, no watermark`

**C-LOG** · logo-brand · L5-material-still-life · 16:10
- Prompt：`Macro still-life photograph, wide shot in three layers — foreground the blurred embossed corner of a cotton-paper card, midground a short row of upright brand cards standing on a stone ledge, each showing one abstract embossed mark with copper foil catching raking side light, background a deep warm-grey studio void, ivory and charcoal palette with one copper accent, 100mm macro with shallow depth of field, 16:10, top and bottom 8% fading to warm grey, no text, no letters, no watermark`

**C-IND** · industry · L1-photo-editorial · 16:10
> 模板化：背景商业空间可按行业重渲染（零售/餐饮/金融…），前景展板不变
- Prompt：`High-end editorial photograph, wide shot in three layers — foreground the blurred edge of a designer's worktable, midground one matte standing board displaying three small printed design proofs pinned side by side, background a softly blurred modern commercial interior — half office, half retail — built as a swappable backdrop, neutral palette with one warm accent light, 85mm shallow depth of field, soft ambient key light from the left with a warm rim on the board, 16:10, top and bottom 8% fading to neutral grey, no text, no letters, no watermark, no screens`

</details>


---

## 模块 C · hero-mosaic（4 瓦拼贴） —— 8 张

**规格**：每瓦 1200×900 · 4:3  
**构图要求**：4 瓦 = 同一主体的 4 个连续状态（时间轴叙事）；每瓦下方 30% 保持低细节供标题叠加；**每套 4 瓦必须同一会话连续生成 + 锁 seed + 同风格参考**。  
**复杂度预算**：每瓦只允许 1 个元素（或 1 个主体群组）  
**出图顺序**：两套必须先各出 1 瓦试风格，确认后一次性连出剩余 3 瓦。


### M-PLA · platform · L3-soft-3d · 覆盖 3 页

> 叙事：brief → generate → refine → export　｜　4 瓦同一会话连出 + 锁 seed

**M-PLA-1**（brief）
- Prompt：`Soft-body 3D render in matte ceramic materials, warm-grey palette with one coral accent, macro 50mm look, soft key light with gentle contact shadows, seamless warm-grey paper backdrop, one subject only, state 1 of a 4-step sequence on the same matte console: an index card with a folded corner resting on a shallow tray beside a rounded slot, at eye level, the console running left to right, locked seed and style reference shared across all four tiles, 4:3, lower 30% kept visually simple for title overlay, no text, no letters, no watermark, no screens`
- Alt：`Lovart workflow 1 — a brief card ready to drop`

**M-PLA-2**（generate）
- Prompt：`Soft-body 3D render in matte ceramic materials, warm-grey palette with one coral accent, macro 50mm look, soft key light with gentle contact shadows, seamless warm-grey paper backdrop, one subject only, state 2 of a 4-step sequence on the same matte console: the same index card half-inserted into the rounded slot, tilting mid-motion, from a slight three-quarter angle, the console receding into depth, locked seed and style reference shared across all four tiles, 4:3, lower 30% kept visually simple for title overlay, no text, no letters, no watermark, no screens`
- Alt：`Lovart workflow 2 — brief mid-generation`

**M-PLA-3**（refine）
- Prompt：`Soft-body 3D render in matte ceramic materials, warm-grey palette with one coral accent, macro 50mm look, soft key light with gentle contact shadows, seamless warm-grey paper backdrop, one subject only, state 3 of a 4-step sequence on the same matte console: the slot lit with a soft coral tint, the card gone, one small framed print standing fresh on the console, in a closer macro, the slot filling most of the frame, locked seed and style reference shared across all four tiles, 4:3, lower 30% kept visually simple for title overlay, no text, no letters, no watermark, no screens`
- Alt：`Lovart workflow 3 — first artwork delivered`

**M-PLA-4**（export）
- Prompt：`Soft-body 3D render in matte ceramic materials, warm-grey palette with one coral accent, macro 50mm look, soft key light with gentle contact shadows, seamless warm-grey paper backdrop, one subject group only, state 4 of a 4-step sequence on the same matte console: three small finished artworks — a framed print, a clay object, a product box — standing in a neat row, the slot at rest, from a pulled-back wide angle showing the whole console, locked seed and style reference shared across all four tiles, 4:3, lower 30% kept visually simple for title overlay, no text, no letters, no watermark, no screens`
- Alt：`Lovart workflow 4 — full set delivered`


### M-IND · industry · L1-photo-editorial · 覆盖 5 页

> 叙事：brief → generate → batch → deliver　｜　4 瓦同一会话连出 + 锁 seed

**M-IND-1**（brief）
- Prompt：`High-end commercial photograph, sand and cream palette with one deep-green accent, 100mm macro look, single soft key light, seamless warm backdrop, one subject only, state 1 of a 4-step sequence on the same package box: one plain kraft box beside a folded-corner brief card on a worktable, at eye level, the console running left to right, locked seed and style reference shared across all four tiles, 4:3, lower 30% kept visually simple for title overlay, no text, no letters, no watermark`
- Alt：`Lovart industry workflow 1 — blank package and brief`

**M-IND-2**（generate）
- Prompt：`High-end commercial photograph, sand and cream palette with one deep-green accent, 100mm macro look, single soft key light, seamless warm backdrop, one subject only, state 2 of a 4-step sequence on the same package box: the same kraft box now wrapped in a fresh printed sleeve, one corner of the sleeve still lifting, from a slight three-quarter angle, the console receding into depth, locked seed and style reference shared across all four tiles, 4:3, lower 30% kept visually simple for title overlay, no text, no letters, no watermark`
- Alt：`Lovart industry workflow 2 — fresh printed sleeve`

**M-IND-3**（batch）
- Prompt：`High-end commercial photograph, sand and cream palette with one deep-green accent, 100mm macro look, single soft key light, seamless warm backdrop, one subject group only, state 3 of a 4-step sequence on the same package box: five identical sleeved boxes lined in a batch row with one being placed down, in a closer macro, the slot filling most of the frame, locked seed and style reference shared across all four tiles, 4:3, lower 30% kept visually simple for title overlay, no text, no letters, no watermark`
- Alt：`Lovart industry workflow 3 — batch production`

**M-IND-4**（deliver）
- Prompt：`High-end commercial photograph, sand and cream palette with one deep-green accent, 100mm macro look, single soft key light, seamless warm backdrop, one subject only, state 4 of a 4-step sequence on the same package box: the sleeved box standing on a retail shelf beside two blank shelf slots, from a pulled-back wide angle showing the whole console, locked seed and style reference shared across all four tiles, 4:3, lower 30% kept visually simple for title overlay, no text, no letters, no watermark`
- Alt：`Lovart industry workflow 4 — on the shelf`


---

## 模块 D · hero-gallery（6 宫格工具瓦） —— 60 张

**规格**：每瓦 1200×1200 · 1:1  
**构图要求**：每瓦 = 单对象肖像（portrait of one object）；底部 25% 留 label 遮罩；**同套 6 瓦必须同一会话 + 同 lane 同 seed + 同背景色**，6 瓦之间只换对象。  
**复杂度预算**：每瓦严格 1 个主体  
**出图顺序**：套间顺序：G-PRT → G-SOC → G-ECO → G-LOG → G-VID → G-IMG → G-DOC → G-ADS → G-CMP → G-PLA。G-PRT 先跑验证（覆盖 58 页、L5 最接近站内现有画风）。


### G-PRT · print · L5-material-still-life · 背景 `ivory` · 覆盖 58 页 （中文页面）

> 同套 6 瓦：同一会话连出 + 锁 seed + 同风格参考。瓦片：海报设计, 传单设计, 名片设计, 菜单设计, 画册封面, 邀请函

**G-PRT-1**（海报设计）
- Prompt：`Macro still-life photograph with raking side light revealing tactile texture, 100mm macro, ivory and grey palette with one copper accent, one subject only: a rolled poster with a vibrant festival-style abstract composition on its visible curl, viewed straight on at eye level, plain seamless backdrop in one flat ivory tone, hero fills about 70% of frame, bottom 25% clean for label scrim, locked seed and style reference shared across all six tiles, 1:1, no text, no letters, no watermark`
- Alt：`Lovart 海报设计 — 活动海报成品`

**G-PRT-2**（传单设计）
- Prompt：`Macro still-life photograph with raking side light revealing tactile texture, 100mm macro, ivory and grey palette with one copper accent, one subject only: a cafe flyer with a coffee motif and a perforated coupon corner, viewed at a slight three-quarter angle, plain seamless backdrop in one flat ivory tone, hero fills about 68% of frame, bottom 25% clean for label scrim, locked seed and style reference shared across all six tiles, 1:1, no text, no letters, no watermark`
- Alt：`Lovart 传单设计 — 门店派发物料`

**G-PRT-3**（名片设计）
- Prompt：`Macro still-life photograph with raking side light revealing tactile texture, 100mm macro, ivory and grey palette with one copper accent, one subject only: a thick letterpress card with an abstract embossed mark, framed as a close macro on the material surface, plain seamless backdrop in one flat ivory tone, hero fills about 76% of frame, bottom 25% clean for label scrim, locked seed and style reference shared across all six tiles, 1:1, no text, no letters, no watermark`
- Alt：`Lovart 名片设计 — 商务名片`

**G-PRT-4**（菜单设计）
- Prompt：`Macro still-life photograph with raking side light revealing tactile texture, 100mm macro, ivory and grey palette with one copper accent, one subject only: a folded menu card with a small dish illustration, seen from directly above in a clean top-down, plain seamless backdrop in one flat ivory tone, hero fills about 66% of frame, bottom 25% clean for label scrim, locked seed and style reference shared across all six tiles, 1:1, no text, no letters, no watermark`
- Alt：`Lovart 菜单设计 — 餐厅菜单页`

**G-PRT-5**（画册封面）
- Prompt：`Overhead still-life photograph of stacked print pieces under soft top light, 100mm macro, ivory and grey palette with one copper accent, one subject only: an album cover with embossed abstract art and a foil edge, seen from a low angle looking slightly upward, plain seamless backdrop in one flat ivory tone, hero fills about 72% of frame, bottom 25% clean for label scrim, locked seed and style reference shared across all six tiles, 1:1, no text, no letters, no watermark`
- Alt：`Lovart 画册/专辑封面 — 印刷级封面`

**G-PRT-6**（邀请函）
- Prompt：`Macro still-life photograph with raking side light revealing tactile texture, 100mm macro, ivory and grey palette with one copper accent, one subject only: an invitation card with a gold-foil edge and a wax-seal motif, viewed as a crisp side profile, plain seamless backdrop in one flat ivory tone, hero fills about 70% of frame, bottom 25% clean for label scrim, locked seed and style reference shared across all six tiles, 1:1, no text, no letters, no watermark`
- Alt：`Lovart 邀请函设计 — 仪式感请柬`


### G-SOC · social · L4-graphic-flat · 背景 `cream` · 覆盖 5 页 （中文页面）

> 同套 6 瓦：同一会话连出 + 锁 seed + 同风格参考。瓦片：小红书图文, 抖音封面, 公众号头图, 微博贴文, B站封面, 社媒日历

**G-SOC-1**（小红书图文）
- Prompt：`Bold flat poster composition with large color blocks and one diagonal slice, high-impact full-bleed layout, paper grain texture with riso-print ink edges, flat poster layout with no photographic perspective, flat even lighting, cream field with coral and charcoal in large blocks, one subject only: a vertical social note-card stack with sticker shapes, cropped tight to the central shape, plain seamless backdrop in one flat cream tone, hero fills 70% of frame, bottom 25% clean for label scrim, locked seed and style reference shared across all six tiles, 1:1, no text, no letters, no watermark`
- Alt：`Lovart 小红书图文 — 笔记封面与配图`

**G-SOC-2**（抖音封面）
- Prompt：`Bold flat poster composition with large color blocks and one diagonal slice, high-impact full-bleed layout, paper grain texture with riso-print ink edges, flat poster layout with no photographic perspective, flat even lighting, cream field with coral and charcoal in large blocks, one subject only: a vertical social cover card with a bold central silhouette and slash shapes, framed as a square full-bleed poster, plain seamless backdrop in one flat cream tone, hero fills 70% of frame, bottom 25% clean for label scrim, locked seed and style reference shared across all six tiles, 1:1, no text, no letters, no watermark`
- Alt：`Lovart 抖音封面 — 高点击竖版封面`

**G-SOC-3**（公众号头图）
- Prompt：`Bold flat poster composition with large color blocks and one diagonal slice, high-impact full-bleed layout, paper grain texture with riso-print ink edges, flat poster layout with no photographic perspective, flat even lighting, cream field with coral and charcoal in large blocks, one subject only: a wide social header card with soft brand-color waves, seen with the diagonal slice cutting corner to corner, plain seamless backdrop in one flat cream tone, hero fills 70% of frame, bottom 25% clean for label scrim, locked seed and style reference shared across all six tiles, 1:1, no text, no letters, no watermark`
- Alt：`Lovart 公众号头图 — 品牌头图横幅`

**G-SOC-4**（微博贴文）
- Prompt：`Bold flat poster composition with large color blocks and one diagonal slice, high-impact full-bleed layout, paper grain texture with riso-print ink edges, flat poster layout with no photographic perspective, flat even lighting, cream field with coral and charcoal in large blocks, one subject only: a square social post card with a punchy central shape and confetti pieces, framed with the subject pushed low, plain seamless backdrop in one flat cream tone, hero fills 70% of frame, bottom 25% clean for label scrim, locked seed and style reference shared across all six tiles, 1:1, no text, no letters, no watermark`
- Alt：`Lovart 微博贴文 — 话题广场图`

**G-SOC-5**（B站封面）
- Prompt：`Bold flat poster composition with large color blocks and one diagonal slice, high-impact full-bleed layout, paper grain texture with riso-print ink edges, flat poster layout with no photographic perspective, flat even lighting, cream field with coral and charcoal in large blocks, one subject only: a social video cover card with an energetic character silhouette and a play triangle, viewed as a bold off-center composition, plain seamless backdrop in one flat cream tone, hero fills 70% of frame, bottom 25% clean for label scrim, locked seed and style reference shared across all six tiles, 1:1, no text, no letters, no watermark`
- Alt：`Lovart B站封面 — 视频封面图`

**G-SOC-6**（社媒日历）
- Prompt：`Bold flat poster composition with large color blocks and one diagonal slice, high-impact full-bleed layout, paper grain texture with riso-print ink edges, flat poster layout with no photographic perspective, flat even lighting, cream field with coral and charcoal in large blocks, one subject only: a social content calendar card with mini thumbnail tiles filling the days, framed as a clean centered emblem, plain seamless backdrop in one flat cream tone, hero fills 70% of frame, bottom 25% clean for label scrim, locked seed and style reference shared across all six tiles, 1:1, no text, no letters, no watermark`
- Alt：`Lovart 社媒日历 — 排期与素材一体`


### G-ECO · ecommerce · L1-photo-editorial · 背景 `sand` · 覆盖 5 页 （中文页面）

> 同套 6 瓦：同一会话连出 + 锁 seed + 同风格参考。瓦片：淘宝主图, 京东详情, 拼多多场景图, 抖音带货, 白底图, 店铺装修

**G-ECO-1**（淘宝主图）
- Prompt：`High-end commercial photograph, 85mm shallow depth of field, soft key light, sand and cream palette with one deep-green accent, one subject only: a product on a tiny podium with radiating paper accent shapes, viewed straight on at eye level, plain seamless backdrop in one flat sand tone, hero fills about 70% of frame, bottom 25% clean for label scrim, locked seed and style reference shared across all six tiles, 1:1, no text, no letters, no watermark`
- Alt：`Lovart 淘宝主图 — 高点击主图`

**G-ECO-2**（京东详情）
- Prompt：`High-end commercial photograph, 85mm shallow depth of field, soft key light, sand and cream palette with one deep-green accent, one subject only: a scroll of product detail cards standing upright in a row, viewed at a slight three-quarter angle, plain seamless backdrop in one flat sand tone, hero fills about 68% of frame, bottom 25% clean for label scrim, locked seed and style reference shared across all six tiles, 1:1, no text, no letters, no watermark`
- Alt：`Lovart 京东详情页 — 卖点分屏`

**G-ECO-3**（拼多多场景图）
- Prompt：`High-end commercial photograph, 85mm shallow depth of field, soft key light, sand and cream palette with one deep-green accent, one subject only: a product scene with small gift boxes and burst-shaped paper badges, framed as a close macro on the material surface, plain seamless backdrop in one flat sand tone, hero fills about 76% of frame, bottom 25% clean for label scrim, locked seed and style reference shared across all six tiles, 1:1, no text, no letters, no watermark`
- Alt：`Lovart 拼多多场景图 — 促销场景图`

**G-ECO-4**（抖音带货）
- Prompt：`High-end commercial photograph, 85mm shallow depth of field, soft key light, sand and cream palette with one deep-green accent, one subject only: a vertical selling frame with a product hero and energetic paper shapes, seen from directly above in a clean top-down, plain seamless backdrop in one flat sand tone, hero fills about 66% of frame, bottom 25% clean for label scrim, locked seed and style reference shared across all six tiles, 1:1, no text, no letters, no watermark`
- Alt：`Lovart 抖音带货素材 — 直播切片封面`

**G-ECO-5**（白底图）
- Prompt：`High-end commercial photograph, 85mm shallow depth of field, soft key light, sand and cream palette with one deep-green accent, one subject only: a flawless white-background product cutout with a soft contact shadow, seen from a low angle looking slightly upward, plain seamless backdrop in one flat sand tone, hero fills about 72% of frame, bottom 25% clean for label scrim, locked seed and style reference shared across all six tiles, 1:1, no text, no letters, no watermark`
- Alt：`Lovart 白底图 — 平台合规抠图`

**G-ECO-6**（店铺装修）
- Prompt：`High-end commercial photograph, 85mm shallow depth of field, soft key light, sand and cream palette with one deep-green accent, one subject only: a storefront banner triptych of three connected product cards, viewed as a crisp side profile, plain seamless backdrop in one flat sand tone, hero fills about 70% of frame, bottom 25% clean for label scrim, locked seed and style reference shared across all six tiles, 1:1, no text, no letters, no watermark`
- Alt：`Lovart 店铺装修 — 首页 banner 组合`


### G-LOG · logo-brand · L5-material-still-life · 背景 `warm grey` · 覆盖 7 页 

> 同套 6 瓦：同一会话连出 + 锁 seed + 同风格参考。瓦片：Logo Maker, Brand Identity, Style Guide, Color Palette, Typography, Icon Set

**G-LOG-1**（Logo Maker）
- Prompt：`Macro still-life photograph with raking side light revealing tactile texture, 100mm macro, ivory and charcoal palette with one brass accent, one subject only: a logo-mark card with golden-ratio guide arcs and a tiny brass compass, viewed straight on at eye level, plain seamless backdrop in one flat warm grey tone, hero fills about 70% of frame, bottom 25% clean for label scrim, locked seed and style reference shared across all six tiles, 1:1, no text, no letters, no watermark`
- Alt：`Lovart Logo Maker — marks built on grids`

**G-LOG-2**（Brand Identity）
- Prompt：`Macro still-life photograph with raking side light revealing tactile texture, 100mm macro, ivory and charcoal palette with one brass accent, one subject only: one card showing an abstract mark applied across tiny brand objects, viewed at a slight three-quarter angle, plain seamless backdrop in one flat warm grey tone, hero fills about 68% of frame, bottom 25% clean for label scrim, locked seed and style reference shared across all six tiles, 1:1, no text, no letters, no watermark`
- Alt：`Lovart Brand Identity — logo everywhere it matters`

**G-LOG-3**（Style Guide）
- Prompt：`Macro still-life photograph with raking side light revealing tactile texture, 100mm macro, ivory and charcoal palette with one brass accent, one subject only: a specimen card with large abstract glyph shapes and fine rule lines, framed as a close macro on the material surface, plain seamless backdrop in one flat warm grey tone, hero fills about 76% of frame, bottom 25% clean for label scrim, locked seed and style reference shared across all six tiles, 1:1, no text, no letters, no watermark`
- Alt：`Lovart Style Guide — type and usage rules`

**G-LOG-4**（Color Palette）
- Prompt：`Macro still-life photograph with raking side light revealing tactile texture, 100mm macro, ivory and charcoal palette with one brass accent, one subject only: a fanned swatch deck with harmonious color chips, seen from directly above in a clean top-down, plain seamless backdrop in one flat warm grey tone, hero fills about 66% of frame, bottom 25% clean for label scrim, locked seed and style reference shared across all six tiles, 1:1, no text, no letters, no watermark`
- Alt：`Lovart Color Palette — brand color systems`

**G-LOG-5**（Typography）
- Prompt：`Macro still-life photograph with raking side light revealing tactile texture, 100mm macro, ivory and charcoal palette with one brass accent, one subject only: a dramatic letterpress abstract glyph with rich ink texture, seen from a low angle looking slightly upward, plain seamless backdrop in one flat warm grey tone, hero fills about 72% of frame, bottom 25% clean for label scrim, locked seed and style reference shared across all six tiles, 1:1, no text, no letters, no watermark`
- Alt：`Lovart Typography — expressive type design`

**G-LOG-6**（Icon Set）
- Prompt：`Macro still-life photograph with raking side light revealing tactile texture, 100mm macro, ivory and charcoal palette with one brass accent, one subject only: a neat family of rounded glyph tiles in one style, viewed as a crisp side profile, plain seamless backdrop in one flat warm grey tone, hero fills about 70% of frame, bottom 25% clean for label scrim, locked seed and style reference shared across all six tiles, 1:1, no text, no letters, no watermark`
- Alt：`Lovart Icon Set — consistent icon families`


### G-VID · video · L2-cinematic-still · 背景 `deep charcoal` · 覆盖 3 页 

> 同套 6 瓦：同一会话连出 + 锁 seed + 同风格参考。瓦片：Image to Video, Text to Video, Product Video, Social Clips, Video Editor, Storyboard

**G-VID-1**（Image to Video）
- Prompt：`Cinematic still, shot on 35mm film, strictly a two-color teal-and-amber palette with no additional accent color, soft volumetric light with subtle film grain, one subject only: a small framed landscape photo with one corner lifting into a soft motion trail, viewed straight on at eye level, plain seamless backdrop in one flat deep charcoal tone, hero fills about 70% of frame, bottom 25% clean for label scrim, locked seed and style reference shared across all six tiles, 1:1, no text, no letters, no watermark`
- Alt：`Lovart Image to Video — still photos set in motion`

**G-VID-2**（Text to Video）
- Prompt：`Cinematic still, shot on 35mm film, strictly a two-color teal-and-amber palette with no additional accent color, soft volumetric light with subtle film grain, one subject only: a tiny open book with a miniature glowing scene rising from its pages, viewed at a slight three-quarter angle, plain seamless backdrop in one flat deep charcoal tone, hero fills about 68% of frame, bottom 25% clean for label scrim, locked seed and style reference shared across all six tiles, 1:1, no text, no letters, no watermark`
- Alt：`Lovart Text to Video — descriptions become footage`

**G-VID-3**（Product Video）
- Prompt：`Cinematic still, shot on 35mm film, strictly a two-color teal-and-amber palette with no additional accent color, soft volumetric light with subtle film grain, one subject only: a sneaker on a tiny turntable with a circular motion trail, framed as a close macro on the material surface, plain seamless backdrop in one flat deep charcoal tone, hero fills about 76% of frame, bottom 25% clean for label scrim, locked seed and style reference shared across all six tiles, 1:1, no text, no letters, no watermark`
- Alt：`Lovart Product Video — 360-degree product showcase`

**G-VID-4**（Social Clips）
- Prompt：`Cinematic still, shot on 35mm film, strictly a two-color teal-and-amber palette with no additional accent color, soft volumetric light with subtle film grain, one subject only: a vertical phone-shaped frame holding a bold short-video scene, seen from directly above in a clean top-down, plain seamless backdrop in one flat deep charcoal tone, hero fills about 66% of frame, bottom 25% clean for label scrim, locked seed and style reference shared across all six tiles, 1:1, no text, no letters, no watermark`
- Alt：`Lovart Social Clips — platform-ready short videos`

**G-VID-5**（Video Editor）
- Prompt：`Cinematic still, shot on 35mm film, strictly a two-color teal-and-amber palette with no additional accent color, soft volumetric light with subtle film grain, one subject only: a short film strip with trim notches and color tabs, seen from a low angle looking slightly upward, plain seamless backdrop in one flat deep charcoal tone, hero fills about 72% of frame, bottom 25% clean for label scrim, locked seed and style reference shared across all six tiles, 1:1, no text, no letters, no watermark`
- Alt：`Lovart Video Editor — refine clips in one canvas`

**G-VID-6**（Storyboard）
- Prompt：`Cinematic still, shot on 35mm film, strictly a two-color teal-and-amber palette with no additional accent color, soft volumetric light with subtle film grain, one subject only: three small sketch cards with the middle one turning photoreal, viewed as a crisp side profile, plain seamless backdrop in one flat deep charcoal tone, hero fills about 70% of frame, bottom 25% clean for label scrim, locked seed and style reference shared across all six tiles, 1:1, no text, no letters, no watermark`
- Alt：`Lovart Storyboard — sketch to screen`


### G-IMG · image-gen · L1-photo-editorial · 背景 `warm beige` · 覆盖 3 页 

> 同套 6 瓦：同一会话连出 + 锁 seed + 同风格参考。瓦片：Text to Image, Image to Image, Product Photo, Illustration, Stock Photo, Style Transfer

**G-IMG-1**（Text to Image）
- Prompt：`High-end commercial photograph, 85mm shallow depth of field, soft key light, warm neutral palette with one saturated accent, one subject only: a paintbrush conjuring a small landscape scene from a swirl of pigment, viewed straight on at eye level, plain seamless backdrop in one flat warm beige tone, hero fills about 70% of frame, bottom 25% clean for label scrim, locked seed and style reference shared across all six tiles, 1:1, no text, no letters, no watermark`
- Alt：`Lovart Text to Image — prompt to artwork`

**G-IMG-2**（Image to Image）
- Prompt：`High-end commercial photograph, 85mm shallow depth of field, soft key light, warm neutral palette with one saturated accent, one subject only: one photo print split diagonally into photographic and painterly halves, viewed at a slight three-quarter angle, plain seamless backdrop in one flat warm beige tone, hero fills about 68% of frame, bottom 25% clean for label scrim, locked seed and style reference shared across all six tiles, 1:1, no text, no letters, no watermark`
- Alt：`Lovart Image to Image — restyle any photo`

**G-IMG-3**（Product Photo）
- Prompt：`High-end commercial photograph, 85mm shallow depth of field, soft key light, warm neutral palette with one saturated accent, one subject only: a perfume bottle under dramatic rim light with a soft contact shadow, framed as a close macro on the material surface, plain seamless backdrop in one flat warm beige tone, hero fills about 76% of frame, bottom 25% clean for label scrim, locked seed and style reference shared across all six tiles, 1:1, no text, no letters, no watermark`
- Alt：`Lovart Product Photo — studio-grade product images`

**G-IMG-4**（Illustration）
- Prompt：`High-end commercial photograph, 85mm shallow depth of field, soft key light, warm neutral palette with one saturated accent, one subject only: a small framed flat-illustration scene with painterly texture, seen from directly above in a clean top-down, plain seamless backdrop in one flat warm beige tone, hero fills about 66% of frame, bottom 25% clean for label scrim, locked seed and style reference shared across all six tiles, 1:1, no text, no letters, no watermark`
- Alt：`Lovart Illustration — cohesive illustration sets`

**G-IMG-5**（Stock Photo）
- Prompt：`High-end commercial photograph, 85mm shallow depth of field, soft key light, warm neutral palette with one saturated accent, one subject only: a candid lifestyle photo print of two people collaborating, seen from a low angle looking slightly upward, plain seamless backdrop in one flat warm beige tone, hero fills about 72% of frame, bottom 25% clean for label scrim, locked seed and style reference shared across all six tiles, 1:1, no text, no letters, no watermark`
- Alt：`Lovart Stock Photos — license-free lifestyle imagery`

**G-IMG-6**（Style Transfer）
- Prompt：`High-end commercial photograph, 85mm shallow depth of field, soft key light, warm neutral palette with one saturated accent, one subject only: a cityscape photo print with a famous-painting texture flowing over one half, viewed as a crisp side profile, plain seamless backdrop in one flat warm beige tone, hero fills about 70% of frame, bottom 25% clean for label scrim, locked seed and style reference shared across all six tiles, 1:1, no text, no letters, no watermark`
- Alt：`Lovart Style Transfer — apply any art style`


### G-DOC · docs-deck · L4-graphic-flat · 背景 `ivory` · 覆盖 6 页 

> 同套 6 瓦：同一会话连出 + 锁 seed + 同风格参考。瓦片：Pitch Deck, Presentation, Infographic, Report, Resume, Whitepaper

**G-DOC-1**（Pitch Deck）
- Prompt：`Editorial flat-graphic layout on a strict Swiss grid, thin hairline rules and generous white space, small precise type-free layout blocks, paper grain texture with riso-print ink edges, flat poster layout with no photographic perspective, flat even lighting, ivory field with ink-blue and charcoal accents, one subject only: a slide card with a rising bar shape and confident layout blocks, viewed straight on as a page spread, plain seamless backdrop in one flat ivory tone, hero fills 70% of frame, bottom 25% clean for label scrim, locked seed and style reference shared across all six tiles, 1:1, no text, no letters, no watermark`
- Alt：`Lovart Pitch Deck — investor-ready slides`

**G-DOC-2**（Presentation）
- Prompt：`Editorial flat-graphic layout on a strict Swiss grid, thin hairline rules and generous white space, small precise type-free layout blocks, paper grain texture with riso-print ink edges, flat poster layout with no photographic perspective, flat even lighting, ivory field with ink-blue and charcoal accents, one subject only: a keynote slide card on a tiny stage shape with a spotlight cone, framed as a tight crop on the grid modules, plain seamless backdrop in one flat ivory tone, hero fills 70% of frame, bottom 25% clean for label scrim, locked seed and style reference shared across all six tiles, 1:1, no text, no letters, no watermark`
- Alt：`Lovart Presentation — stage-ready slides`

**G-DOC-3**（Infographic）
- Prompt：`Editorial flat-graphic layout on a strict Swiss grid, thin hairline rules and generous white space, small precise type-free layout blocks, paper grain texture with riso-print ink edges, flat poster layout with no photographic perspective, flat even lighting, ivory field with ink-blue and charcoal accents, one subject only: a data poster card with icons, flow arrows and abstract data shapes, seen slightly off-axis as a stacked page, plain seamless backdrop in one flat ivory tone, hero fills 70% of frame, bottom 25% clean for label scrim, locked seed and style reference shared across all six tiles, 1:1, no text, no letters, no watermark`
- Alt：`Lovart Infographic — data made visual`

**G-DOC-4**（Report）
- Prompt：`Editorial flat-graphic layout on a strict Swiss grid, thin hairline rules and generous white space, small precise type-free layout blocks, paper grain texture with riso-print ink edges, flat poster layout with no photographic perspective, flat even lighting, ivory field with ink-blue and charcoal accents, one subject only: a small stack of report cards with abstract data motifs, viewed as a generous margin-led layout, plain seamless backdrop in one flat ivory tone, hero fills 70% of frame, bottom 25% clean for label scrim, locked seed and style reference shared across all six tiles, 1:1, no text, no letters, no watermark`
- Alt：`Lovart Report — polished business reports`

**G-DOC-5**（Resume）
- Prompt：`Editorial flat-graphic layout on a strict Swiss grid, thin hairline rules and generous white space, small precise type-free layout blocks, paper grain texture with riso-print ink edges, flat poster layout with no photographic perspective, flat even lighting, ivory field with ink-blue and charcoal accents, one subject only: a minimal CV card with an abstract avatar shape and clean rule lines, framed as a single module isolated on the grid, plain seamless backdrop in one flat ivory tone, hero fills 70% of frame, bottom 25% clean for label scrim, locked seed and style reference shared across all six tiles, 1:1, no text, no letters, no watermark`
- Alt：`Lovart Resume — clean professional CV design`

**G-DOC-6**（Whitepaper）
- Prompt：`Editorial flat-graphic layout on a strict Swiss grid, thin hairline rules and generous white space, small precise type-free layout blocks, paper grain texture with riso-print ink edges, flat poster layout with no photographic perspective, flat even lighting, ivory field with ink-blue and charcoal accents, one subject only: a whitepaper cover card with an embossed abstract diagram, seen as a full-spread cover layout, plain seamless backdrop in one flat ivory tone, hero fills 70% of frame, bottom 25% clean for label scrim, locked seed and style reference shared across all six tiles, 1:1, no text, no letters, no watermark`
- Alt：`Lovart Whitepaper — credible long-form design`


### G-ADS · ads · L4-graphic-flat · 背景 `cream` · 覆盖 1 页 

> 同套 6 瓦：同一会话连出 + 锁 seed + 同风格参考。瓦片：Ad Creative, Display Ad, Carousel Ad, Google Banner, Retargeting, UGC Ad

**G-ADS-1**（Ad Creative）
- Prompt：`Flat graphic badge-and-label composition with layered offset cards and one stamped badge shape, crisp edges and precise registration, paper grain texture with riso-print ink edges, flat poster layout with no photographic perspective, flat even lighting, cream field with tangerine and charcoal accents, one subject only: a bold ad card with a product silhouette and diagonal energy shapes, seen slightly from above as stacked labels, plain seamless backdrop in one flat cream tone, hero fills 70% of frame, bottom 25% clean for label scrim, locked seed and style reference shared across all six tiles, 1:1, no text, no letters, no watermark`
- Alt：`Lovart Ad Creative — scroll-stopping ad visuals`

**G-ADS-2**（Display Ad）
- Prompt：`Flat graphic badge-and-label composition with layered offset cards and one stamped badge shape, crisp edges and precise registration, paper grain texture with riso-print ink edges, flat poster layout with no photographic perspective, flat even lighting, cream field with tangerine and charcoal accents, one subject only: a trio of banner cards in leaderboard and rectangle proportions, framed tight on the stamped badge, plain seamless backdrop in one flat cream tone, hero fills 70% of frame, bottom 25% clean for label scrim, locked seed and style reference shared across all six tiles, 1:1, no text, no letters, no watermark`
- Alt：`Lovart Display Ads — every banner size on brand`

**G-ADS-3**（Carousel Ad）
- Prompt：`Flat graphic badge-and-label composition with layered offset cards and one stamped badge shape, crisp edges and precise registration, paper grain texture with riso-print ink edges, flat poster layout with no photographic perspective, flat even lighting, cream field with tangerine and charcoal accents, one subject only: three swipe cards fanned with sequential product shapes, viewed as an offset card peeking behind the hero card, plain seamless backdrop in one flat cream tone, hero fills 70% of frame, bottom 25% clean for label scrim, locked seed and style reference shared across all six tiles, 1:1, no text, no letters, no watermark`
- Alt：`Lovart Carousel Ads — swipe-through stories`

**G-ADS-4**（Google Banner）
- Prompt：`Flat graphic badge-and-label composition with layered offset cards and one stamped badge shape, crisp edges and precise registration, paper grain texture with riso-print ink edges, flat poster layout with no photographic perspective, flat even lighting, cream field with tangerine and charcoal accents, one subject only: a crisp banner card with a product cutout shape and accent blocks, framed as a small badge centered in space, plain seamless backdrop in one flat cream tone, hero fills 70% of frame, bottom 25% clean for label scrim, locked seed and style reference shared across all six tiles, 1:1, no text, no letters, no watermark`
- Alt：`Lovart Google Banners — paid search creatives`

**G-ADS-5**（Retargeting）
- Prompt：`Flat graphic badge-and-label composition with layered offset cards and one stamped badge shape, crisp edges and precise registration, paper grain texture with riso-print ink edges, flat poster layout with no photographic perspective, flat even lighting, cream field with tangerine and charcoal accents, one subject only: a reminder card with a returning product shape and a soft light trail, seen as a corner-tucked label arrangement, plain seamless backdrop in one flat cream tone, hero fills 70% of frame, bottom 25% clean for label scrim, locked seed and style reference shared across all six tiles, 1:1, no text, no letters, no watermark`
- Alt：`Lovart Retargeting Ads — win-back creatives`

**G-ADS-6**（UGC Ad）
- Prompt：`Flat graphic badge-and-label composition with layered offset cards and one stamped badge shape, crisp edges and precise registration, paper grain texture with riso-print ink edges, flat poster layout with no photographic perspective, flat even lighting, cream field with tangerine and charcoal accents, one subject only: a casual handheld-style ad card with an authentic candid feel, framed as a clean single-card impression, plain seamless backdrop in one flat cream tone, hero fills 70% of frame, bottom 25% clean for label scrim, locked seed and style reference shared across all six tiles, 1:1, no text, no letters, no watermark`
- Alt：`Lovart UGC Ads — authentic creator-style ads`


### G-CMP · compare · L4-graphic-flat · 背景 `ivory` · 覆盖 2 页 （中文页面）

> 同套 6 瓦：同一会话连出 + 锁 seed + 同风格参考。瓦片：速度对比, 成本对比, 质量对比, 协作对比, 商用权对比, 工作流对比

**G-CMP-1**（速度对比）
- Prompt：`Duotone flat composition split by one hard vertical seam, mirrored structure on both sides, paper grain texture with riso-print ink edges, flat poster layout with no photographic perspective, flat even lighting, muted warm grey on one side and soft coral on the other, one subject only: one card split by a clean rule: left a dissolving stopwatch shape, right a queue of small clocks, split vertically down the middle, plain seamless backdrop in one flat ivory tone, hero fills 70% of frame, bottom 25% clean for label scrim, locked seed and style reference shared across all six tiles, 1:1, no text, no letters, no watermark`
- Alt：`Lovart vs 传统工具 — 速度对比`

**G-CMP-2**（成本对比）
- Prompt：`Duotone flat composition split by one hard vertical seam, mirrored structure on both sides, paper grain texture with riso-print ink edges, flat poster layout with no photographic perspective, flat even lighting, muted warm grey on one side and soft coral on the other, one subject only: two cards side by side on the same surface: a tidy subscription card against a heap of coins, split with a diagonal seam, plain seamless backdrop in one flat ivory tone, hero fills 70% of frame, bottom 25% clean for label scrim, locked seed and style reference shared across all six tiles, 1:1, no text, no letters, no watermark`
- Alt：`Lovart vs 传统工具 — 成本对比`

**G-CMP-3**（质量对比）
- Prompt：`Duotone flat composition split by one hard vertical seam, mirrored structure on both sides, paper grain texture with riso-print ink edges, flat poster layout with no photographic perspective, flat even lighting, muted warm grey on one side and soft coral on the other, one subject only: one card torn in half: the left half crisp and sharp, the right half blurred, split with the seam off-center to the left, plain seamless backdrop in one flat ivory tone, hero fills 70% of frame, bottom 25% clean for label scrim, locked seed and style reference shared across all six tiles, 1:1, no text, no letters, no watermark`
- Alt：`Lovart vs 传统工具 — 质量对比`

**G-CMP-4**（协作对比）
- Prompt：`Duotone flat composition split by one hard vertical seam, mirrored structure on both sides, paper grain texture with riso-print ink edges, flat poster layout with no photographic perspective, flat even lighting, muted warm grey on one side and soft coral on the other, one subject only: one card showing a lone cursor on the left and a synced team of cursors on the right, split as stacked halves, plain seamless backdrop in one flat ivory tone, hero fills 70% of frame, bottom 25% clean for label scrim, locked seed and style reference shared across all six tiles, 1:1, no text, no letters, no watermark`
- Alt：`Lovart vs 传统工具 — 协作对比`

**G-CMP-5**（商用权对比）
- Prompt：`Duotone flat composition split by one hard vertical seam, mirrored structure on both sides, paper grain texture with riso-print ink edges, flat poster layout with no photographic perspective, flat even lighting, muted warm grey on one side and soft coral on the other, one subject only: two stacked cards: a cleared-rights seal on top, a caution triangle below, split with a narrow center gutter, plain seamless backdrop in one flat ivory tone, hero fills 70% of frame, bottom 25% clean for label scrim, locked seed and style reference shared across all six tiles, 1:1, no text, no letters, no watermark`
- Alt：`Lovart vs 传统工具 — 商用授权对比`

**G-CMP-6**（工作流对比）
- Prompt：`Duotone flat composition split by one hard vertical seam, mirrored structure on both sides, paper grain texture with riso-print ink edges, flat poster layout with no photographic perspective, flat even lighting, muted warm grey on one side and soft coral on the other, one subject only: one wide card: a row of separate tool cards on the left, one unified canvas card on the right, split as a wide low-contrast seam, plain seamless backdrop in one flat ivory tone, hero fills 70% of frame, bottom 25% clean for label scrim, locked seed and style reference shared across all six tiles, 1:1, no text, no letters, no watermark`
- Alt：`Lovart vs 传统工具 — 工作流对比`


### G-PLA · platform · L3-soft-3d · 背景 `warm grey` · 覆盖 5 页 

> 同套 6 瓦：同一会话连出 + 锁 seed + 同风格参考。瓦片：Design Agent, ChatCanvas, Multi-Model, Brand Kit, Template Library, Workflow

**G-PLA-1**（Design Agent）
- Prompt：`Soft-body 3D render in matte ceramic materials, warm-grey palette with one coral accent, macro 50mm look, soft key light with gentle contact shadows, one subject only: a small matte console with a rounded slot and one index card halfway in, viewed straight on at eye level, plain seamless backdrop in one flat warm grey tone, hero fills about 70% of frame, bottom 25% clean for label scrim, locked seed and style reference shared across all six tiles, 1:1, no text, no letters, no watermark`
- Alt：`Lovart Design Agent — a full campaign from one brief`

**G-PLA-2**（ChatCanvas）
- Prompt：`Soft-body 3D render in matte ceramic materials, warm-grey palette with one coral accent, macro 50mm look, soft key light with gentle contact shadows, one subject only: a matte speech-bubble ceramic tile leaning against a tiny framed poster, viewed at a slight three-quarter angle, plain seamless backdrop in one flat warm grey tone, hero fills about 68% of frame, bottom 25% clean for label scrim, locked seed and style reference shared across all six tiles, 1:1, no text, no letters, no watermark`
- Alt：`Lovart ChatCanvas — chat turns into designs`

**G-PLA-3**（Multi-Model）
- Prompt：`Soft-body 3D render in matte ceramic materials, warm-grey palette with one coral accent, macro 50mm look, soft key light with gentle contact shadows, one subject only: a small rotary dial with four material swatch chips beside it, framed as a close macro on the material surface, plain seamless backdrop in one flat warm grey tone, hero fills about 76% of frame, bottom 25% clean for label scrim, locked seed and style reference shared across all six tiles, 1:1, no text, no letters, no watermark`
- Alt：`Lovart Multi-Model — one brief, many engines`

**G-PLA-4**（Brand Kit）
- Prompt：`Soft-body 3D render in matte ceramic materials, warm-grey palette with one coral accent, macro 50mm look, soft key light with gentle contact shadows, one subject only: a tidy kit card with an abstract mark, color dots and a tiny ruler, seen from directly above in a clean top-down, plain seamless backdrop in one flat warm grey tone, hero fills about 66% of frame, bottom 25% clean for label scrim, locked seed and style reference shared across all six tiles, 1:1, no text, no letters, no watermark`
- Alt：`Lovart Brand Kit — every design identity in one place`

**G-PLA-5**（Template Library）
- Prompt：`Soft-body 3D render in matte ceramic materials, warm-grey palette with one coral accent, macro 50mm look, soft key light with gentle contact shadows, one subject only: a fanned stack of small template cards, seen from a low angle looking slightly upward, plain seamless backdrop in one flat warm grey tone, hero fills about 72% of frame, bottom 25% clean for label scrim, locked seed and style reference shared across all six tiles, 1:1, no text, no letters, no watermark`
- Alt：`Lovart Template Library — start every design from proven layouts`

**G-PLA-6**（Workflow）
- Prompt：`Soft-body 3D render in matte ceramic materials, warm-grey palette with one coral accent, macro 50mm look, soft key light with gentle contact shadows, one subject only: three linked matte nodes joined by a thin clay rod, viewed as a crisp side profile, plain seamless backdrop in one flat warm grey tone, hero fills about 70% of frame, bottom 25% clean for label scrim, locked seed and style reference shared across all six tiles, 1:1, no text, no letters, no watermark`
- Alt：`Lovart Workflow — automated design pipeline`


---

## 通用交付规范（四模块共用）

| 项 | 要求 |
|---|---|
| 命名 | `hero-{variant}-{theme}-v1.{ext}`；瓦片加 `-t1…t6` |
| 体积 | ≤1.5MB（JPG q85 或优化 PNG） |
| 图内文字 | 零。含乱码 UI 文字即废稿 |
| 安全区 | 四边 ≥5% 裁切余量 |
| 同套一致 | mosaic/gallery 一套内背景色、光向、色彩须完全一致 |
| 禁用元素 | 紫蓝渐变、玻璃拟态、悬浮 3D 球、等距插画、光轨、floating chips、多点拼贴 |
| 随图交付 | alt 文案（本文已给）；zh 页面用中文 alt |

