# P1 批次 Brief（13 张 · v2 航道制 · QC 已通过）

> 投喂方式：整段复制「Prompt」到 Lovart，画布按标注比例设置；mosaic 每套 4 瓦**同一会话连续生成**保证同族。
> 质检：`p1-qc-report.md`（BLOCK 0 / WARN 0）。风格体系：`prompt-v2-style-system.md`。

---

## B 系列 · hero-cinematic（5 张 · 2400×1500 · 16:10 · 上下 8% 渐隐）

### C-PLA · platform 平台与 Agent · L3 柔体三维 · 覆盖 12 页（lovart-2-0 / landing-full / zh-enterprise 等）
- 画面：工作台纵深三层——前景 brief 卡片、中景一排成品（画框/陶土件/产品盒）、背景空暖灰空间一束珊瑚色光。无光轨、无界面。
- Prompt：`Soft-body 3D render in matte ceramic materials, wide establishing shot: a long rounded workbench recedes into warm-grey depth — foreground holds one folded-corner index card resting on a shallow tray, midground holds a single row of small finished artworks standing on the bench (one framed print, one clay object, one product box), background is an empty warm-grey studio volume with one soft coral light source, warm-grey palette with one coral accent, macro-soft HDRI lighting with gentle contact shadows, 16:10, top and bottom 8% fading to warm grey, no text, no letters, no watermark, no screens, no panels`
- Alt：`Lovart design agent studio — one brief card becoming a row of finished artworks`

### C-IMG · image-gen 图像生成 · L1 商业摄影 · 覆盖 2 页（ai-image-generator 系列）
- 画面：画室三层——前景虚化画笔筒、中景画架上一幅 vivid 风景大画（全焦点）、背景高窗柔光。点睛色只存在于画内。
- Prompt：`High-end editorial photograph, wide shot of a sunlit painter's studio in three layers — foreground a blurred jar of brushes catching window light, midground one large vivid landscape painting standing on a wooden easel in full focus, background a tall window with soft out-of-focus daylight, warm neutral palette with one saturated accent living only inside the painting, 85mm shallow depth of field, 16:10, top and bottom 8% fading to warm grey, no text, no letters, no watermark, no screens`
- Alt：`Lovart image generation — one vivid painting in a sunlit studio`

### C-ECO · ecommerce 电商与产品图 · L1 商业摄影 · 覆盖 3 页
- 画面：三层叙事"实拍到 listing"——前景瓶身曲线虚化、中景同款瓶子展台全焦点、背景立着该瓶的白底图卡片。
- Prompt：`High-end commercial product photograph, wide shot in three layers — foreground the blurred edge of a matte ceramic bottle, midground the same bottle standing centered on a sand-colored podium in full focus, background a white listing cutout card of the bottle leaning against a cream seamless backdrop, sand and cream palette with one deep-green accent, single key light with gentle falloff, 100mm macro look, 16:10, top and bottom 8% fading to cream, no text, no letters, no watermark`
- Alt：`Lovart product photography — studio shot and listing cutout in one frame`

### C-LOG · logo-brand Logo 与品牌 · L5 材质静物 · 覆盖 4 页
- 画面：三层——前景压凹卡角虚化、中景石台上一列立着的品牌卡（压凹标+铜箔侧光）、背景深灰空间。
- Prompt：`Macro still-life photograph, wide shot in three layers — foreground the blurred embossed corner of a cotton-paper card, midground a short row of upright brand cards standing on a stone ledge, each showing one abstract embossed mark with copper foil catching raking side light, background a deep warm-grey studio void, ivory and charcoal palette with one copper accent, 100mm macro with shallow depth of field, 16:10, top and bottom 8% fading to warm grey, no text, no letters, no watermark`
- Alt：`Lovart brand identity — embossed cards on a stone ledge`

### C-IND · industry 行业方案 · L1 商业摄影（模板化）· 覆盖 12 页（zh-solution 行业页共用）
- 画面：前景工作台边缘虚化、中景一块哑光立牌钉着三张印刷稿、背景半办公半零售的柔焦商业空间。**背景可按行业换装重渲染，前景展板不变**；建议先用零售背景验证模板再放量。
- Prompt：`High-end editorial photograph, wide shot in three layers — foreground the blurred edge of a designer's worktable, midground one matte standing board displaying three small printed design proofs pinned side by side, background a softly blurred modern commercial interior — half office, half retail — built as a swappable backdrop, neutral palette with one warm accent light, 85mm shallow depth of field, 16:10, top and bottom 8% fading to neutral grey, no text, no letters, no watermark, no screens`
- Alt：`Lovart industry solution — printed design proofs in a commercial space`

---

## C 系列 · hero-mosaic（2 套 × 4 瓦 · 每瓦 1200×900 · 4:3 · 每瓦下方 30% 留白）

> 两套都是"同一主体的 4 个连续状态"，每瓦只 1 个主体；生成时锁 seed + 风格参考，4 瓦一次会话连出。

### M-PLA · platform · L3 柔体三维 · 覆盖 3 页 · 叙事：卡片在 console 上的四状态

- M-PLA-1（待投）：`Soft-body 3D render in matte ceramic materials, warm-grey palette with one coral accent, macro 50mm look, soft key light with gentle contact shadows, seamless warm-grey paper backdrop, one subject only, state 1 of a 4-step sequence on the same matte console: an index card with a folded corner resting on a shallow tray beside a rounded slot, locked seed and style reference shared across all four tiles, 4:3, lower 30% kept visually simple for title overlay, no text, no letters, no watermark, no screens`
  Alt：`Lovart workflow 1 — a brief card ready to drop`
- M-PLA-2（进行中）：`Soft-body 3D render in matte ceramic materials, warm-grey palette with one coral accent, macro 50mm look, soft key light with gentle contact shadows, seamless warm-grey paper backdrop, one subject only, state 2 of a 4-step sequence on the same matte console: the same index card half-inserted into the rounded slot, tilting mid-motion, locked seed and style reference shared across all four tiles, 4:3, lower 30% kept visually simple for title overlay, no text, no letters, no watermark, no screens`
  Alt：`Lovart workflow 2 — brief mid-generation`
- M-PLA-3（首件成品）：`Soft-body 3D render in matte ceramic materials, warm-grey palette with one coral accent, macro 50mm look, soft key light with gentle contact shadows, seamless warm-grey paper backdrop, one subject only, state 3 of a 4-step sequence on the same matte console: the slot lit with a soft coral tint, the card gone, one small framed print standing fresh on the console, locked seed and style reference shared across all four tiles, 4:3, lower 30% kept visually simple for title overlay, no text, no letters, no watermark, no screens`
  Alt：`Lovart workflow 3 — first artwork delivered`
- M-PLA-4（全套交付）：`Soft-body 3D render in matte ceramic materials, warm-grey palette with one coral accent, macro 50mm look, soft key light with gentle contact shadows, seamless warm-grey paper backdrop, one subject group only, state 4 of a 4-step sequence on the same matte console: three small finished artworks — a framed print, a clay object, a product box — standing in a neat row, the slot at rest, locked seed and style reference shared across all four tiles, 4:3, lower 30% kept visually simple for title overlay, no text, no letters, no watermark, no screens`
  Alt：`Lovart workflow 4 — full set delivered`

### M-IND · industry · L1 商业摄影 · 覆盖 5 页 · 叙事：同一包装的四状态

- M-IND-1（坯+brief）：`High-end commercial photograph, sand and cream palette with one deep-green accent, 100mm macro look, single soft key light, seamless warm backdrop, one subject only, state 1 of a 4-step sequence on the same package box: one plain kraft box beside a folded-corner brief card on a worktable, locked seed and style reference shared across all four tiles, 4:3, lower 30% kept visually simple for title overlay, no text, no letters, no watermark`
  Alt：`Lovart industry workflow 1 — blank package and brief`
- M-IND-2（新套封）：`High-end commercial photograph, sand and cream palette with one deep-green accent, 100mm macro look, single soft key light, seamless warm backdrop, one subject only, state 2 of a 4-step sequence on the same package box: the same kraft box now wrapped in a fresh printed sleeve, one corner of the sleeve still lifting, locked seed and style reference shared across all four tiles, 4:3, lower 30% kept visually simple for title overlay, no text, no letters, no watermark`
  Alt：`Lovart industry workflow 2 — fresh printed sleeve`
- M-IND-3（批量列）：`High-end commercial photograph, sand and cream palette with one deep-green accent, 100mm macro look, single soft key light, seamless warm backdrop, one subject group only, state 3 of a 4-step sequence on the same package box: five identical sleeved boxes lined in a batch row with one being placed down, locked seed and style reference shared across all four tiles, 4:3, lower 30% kept visually simple for title overlay, no text, no letters, no watermark`
  Alt：`Lovart industry workflow 3 — batch production`
- M-IND-4（上架）：`High-end commercial photograph, sand and cream palette with one deep-green accent, 100mm macro look, single soft key light, seamless warm backdrop, one subject only, state 4 of a 4-step sequence on the same package box: the sleeved box standing on a retail shelf beside two blank shelf slots, locked seed and style reference shared across all four tiles, 4:3, lower 30% kept visually simple for title overlay, no text, no letters, no watermark`
  Alt：`Lovart industry workflow 4 — on the shelf`
