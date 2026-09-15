# P0 高曝光 15 篇 Blog 基线快照 — 2026-07-07

**用途**：给 2026-07-06 已完成扩写的 15 篇 P0 Blog 建立观察基线，便于未来 2-4 周追踪 CTR、曝光与排名变化。  
**数据源**：`gsc-2026-06.json`、`gsc-may-25k-raw.json`、Sanity production 当前 blog 文档。  
**口径说明**：5 月来自 GSC 25K raw page 维度，6 月来自 GSC 6 月 page 维度汇总；Sanity 标题以 2026-07-07 查询结果为准。

---

## 核心结论

- 这 15 篇里，真正的高曝光核心盘仍然是 `luma-dream-machine-review`、`hedra-ai-review`、`complete-guide-consistent-ai-character-design`、`pika-ai-review`、`ai-video-models-compared-2026`、`ai-image-models-compared-2026` 这几类 review / comparison / complete guide 词。
- 6 月对比 5 月，老牌 review 词多数出现了**曝光回落但排名仍在 6-9 位区间**的情况，说明它们仍然有 SERP 机会，但旧文在 CTR 和结果形态上明显不够强。
- `complete-guide-*` 系列里有几篇出现了**曝光上涨或位置改善**，说明长文深挖方向本身是对的，后续重点要看扩写后 CTR 是否能跟上。
- 有 3 篇在 6 月 page 维度里暂时显示为 `0`：`best-ai-design-tools-2026`、`amazon-requirements-ai-white-background-images`、`complete-guide-object-removal-inpainting-ai`。这更像是数据口径或 URL 命中问题，不宜直接解读为“无流量”。
- 当前最值得盯的不是“有没有曝光”，而是**扩写后能否把 0.0%-0.3% 的 CTR 拉到 0.8%-1.5% 以上**。这才是这批 P0 改造的胜负手。

---

## 单页基线

### 1. `luma-dream-machine-review`
- 当前标题：`Luma Dream Machine Review 2026: Honest Test vs Lovart | Lovart`
- Sanity 更新时间：`2026-07-06T09:09:09Z`
- 6 月基线：15 clicks / 10,742 impressions / CTR 0.1 / pos 8.3
- 5 月基线：47 clicks / 49,538 impressions / CTR 0.09 / pos 7.38
- 判断：流量盘子仍大，但曝光从 5 月高位回落明显；扩写后的重点应看 CTR 能否从 0.1% 拉升。

### 2. `hedra-ai-review`
- 当前标题：`Lovart AI: Hedra Ai Review | Tested 2026`
- Sanity 更新时间：`2026-07-06T09:09:17Z`
- 6 月基线：17 clicks / 6,781 impressions / CTR 0.3 / pos 6.7
- 5 月基线：100 clicks / 40,095 impressions / CTR 0.25 / pos 6.62
- 判断：核心 review 词，排名相对稳定，CTR 略有改善，但曝光回落很大；这是最适合观察“内容升级能否扛住需求波动”的样本。

### 3. `complete-guide-consistent-ai-character-design`
- 当前标题：`The 2026 Complete Guide to Consistent AI Character Design`
- Sanity 更新时间：`2026-07-06T14:51:20Z`
- 6 月基线：12 clicks / 7,376 impressions / CTR 0.2 / pos 8.2
- 5 月基线：9 clicks / 3,866 impressions / CTR 0.23 / pos 9.20
- 判断：这是少数 6 月曝光显著高于 5 月的 complete guide；虽然 CTR 还低，但位置改善，说明主题仍在升温。

### 4. `haiper-ai-review`
- 当前标题：`Lovart AI: Haiper Ai Review 2025 Features Pricing And Real World Performance Test | Tested 2026`
- Sanity 更新时间：`2026-07-06T09:09:32Z`
- 6 月基线：3 clicks / 354 impressions / CTR 0.8 / pos 8.4
- 5 月基线：62 clicks / 21,084 impressions / CTR 0.29 / pos 7.87
- 判断：6 月样本显著缩小，但 CTR 表面上更高；这类词要避免被小样本迷惑，先看后续两周曝光是否恢复。

### 5. `best-ai-design-tools-2026`
- 当前标题：`Best AI Design Tools 2026: 12 Tested Side-by-Side | Lovart`
- Sanity 更新时间：`2026-07-06T14:49:08Z`
- 6 月基线：0 clicks / 0 impressions / CTR 0 / pos 0
- 5 月基线：0 clicks / 2,668 impressions / CTR 0 / pos 6.96
- 判断：这是典型“5 月已有可见曝光、6 月 page 快照未命中”的异常样本。后续要优先核 URL 命中与 canonical，再看扩写后的重新抓取表现。

### 6. `pika-ai-review`
- 当前标题：`AI Video Generator: 2026's Best Tools Tested & Ranked | Lovart`
- Sanity 更新时间：`2026-07-06T09:09:58Z`
- 6 月基线：6 clicks / 2,297 impressions / CTR 0.3 / pos 7.7
- 5 月基线：33 clicks / 15,653 impressions / CTR 0.21 / pos 6.87
- 判断：这篇的标题已经明显往 comparison/roundup 方向拉，但位置略差于 5 月；要看新标题是否真能把 CTR 再抬起来。

### 7. `complete-guide-ai-face-swap-photo-video`
- 当前标题：`The 2026 Complete Guide to AI Face Swap — Photo & Video`
- Sanity 更新时间：`2026-07-06T12:55:57Z`
- 6 月基线：5 clicks / 2,280 impressions / CTR 0.2 / pos 8.3
- 5 月基线：1 click / 1,525 impressions / CTR 0.07 / pos 7.14
- 判断：曝光和点击都在增长，但排名略有后移；属于“需求还在长、文档深度需要继续吃红利”的类型。

### 8. `complete-guide-image-upscaling-resolution-ai`
- 当前标题：`The 2026 Complete Guide to AI Image Upscaling & Resolution Enhancement`
- Sanity 更新时间：`2026-07-06T12:56:02Z`
- 6 月基线：1 click / 2,218 impressions / CTR 0.0 / pos 10.6
- 5 月基线：0 clicks / 1,270 impressions / CTR 0 / pos 10.03
- 判断：曝光在涨，但还在 10 位附近徘徊；这类页的关键不是有无需求，而是能否从页尾挤进更靠前位置。

### 9. `amazon-requirements-ai-white-background-images`
- 当前标题：`Lovart AI: Amazon Requirements Ai White Background Images | Tested 2026`
- Sanity 更新时间：`2026-07-06T09:10:21Z`
- 6 月基线：0 clicks / 0 impressions / CTR 0 / pos 0
- 5 月基线：6 clicks / 1,076 impressions / CTR 0.56 / pos 8.45
- 判断：5 月数据说明这个词并非没有需求；6 月 page 维度未命中，更像 URL 或收录口径需要复核。

### 10. `ai-video-models-compared-2026`
- 当前标题：`AI Video Generator: 2026's Best Tools Tested & Ranked | Lovart`
- Sanity 更新时间：`2026-07-06T09:10:27Z`
- 6 月基线：1 click / 1,839 impressions / CTR 0.1 / pos 8.6
- 5 月基线：0 clicks / 1,128 impressions / CTR 0 / pos 7.48
- 判断：曝光扩大但点击还没有跟上，说明 query 需求在增，SERP 结果还不够“可点”。

### 11. `twitter-image-design-guide`
- 当前标题：`The Complete Guide to Twitter Image Design: Sizes, Tips & AI Shortcuts`
- Sanity 更新时间：`2026-07-06T09:10:33Z`
- 6 月基线：4 clicks / 1,184 impressions / CTR 0.3 / pos 12.1
- 5 月基线：4 clicks / 1,747 impressions / CTR 0.23 / pos 19.48
- 判断：这是这批里最典型的“排名明显改善但曝光盘收缩”的页面。扩写后如果能把位置继续拉进前 10，回报会很直接。

### 12. `complete-guide-object-removal-inpainting-ai`
- 当前标题：`AI Image Editor: Smart Object Removal & Touch-Up | Lovart`
- Sanity 更新时间：`2026-07-06T12:56:08Z`
- 6 月基线：0 clicks / 0 impressions / CTR 0 / pos 0
- 5 月基线：0 clicks / 1,424 impressions / CTR 0 / pos 8.36
- 判断：5 月已处于首页边缘，但没有拿到点击；这篇很适合作为“高曝光零点击改造”的观察样本。

### 13. `adobe-firefly-review`
- 当前标题：`Lovart AI: Adobe Firefly Review | Tested 2026`
- Sanity 更新时间：`2026-07-06T09:10:46Z`
- 6 月基线：5 clicks / 1,105 impressions / CTR 0.5 / pos 6.3
- 5 月基线：37 clicks / 46,074 impressions / CTR 0.08 / pos 6.43
- 判断：标题改造后，理论上最有机会在相近排名下吃到更高 CTR。这一页很适合作为“标题/描述升级效果”的对照组。

### 14. `ai-image-models-compared-2026`
- 当前标题：`Lovart AI: Ai Image Models Compared 2026 | Tested 2026`
- Sanity 更新时间：`2026-07-06T09:10:52Z`
- 6 月基线：1 click / 1,962 impressions / CTR 0.1 / pos 7.6
- 5 月基线：1 click / 517 impressions / CTR 0.19 / pos 5.83
- 判断：曝光明显放大，但位置略后移、CTR 下降；这是“需求变大但页面竞争力没同步抬升”的典型例子。

### 15. `complete-guide-ai-face-retouching-portrait-editing`
- 当前标题：`The 2026 Complete Guide to AI Face Retouching & Portrait Editing`
- Sanity 更新时间：`2026-07-06T12:56:14Z`
- 6 月基线：1 click / 686 impressions / CTR 0.1 / pos 7.6
- 5 月基线：1 click / 1,328 impressions / CTR 0.08 / pos 8.30
- 判断：曝光回落但位置略有改善，属于可继续观察的尾部样本，不该用单月数据过度解读。

---

## 接下来该怎么盯

- 第一个观察窗：`2026-07-14`  
  看抓取与 impressions 是否开始回升，先确认改写被搜索结果消化。

- 第二个观察窗：`2026-07-21`
  看 CTR 是否开始明显抬升。对这批页面来说，CTR 比 clicks 更早反映改写是否有效。

- 第三个观察窗：`2026-08-04`
  看排名是否从 `6-10` 稳定向前，以及零点击页是否开始破零。

---

## 优先盯盘页

- 第一优先：`hedra-ai-review`、`adobe-firefly-review`、`luma-dream-machine-review`
- 第二优先：`complete-guide-consistent-ai-character-design`、`ai-video-models-compared-2026`、`ai-image-models-compared-2026`
- 异常复核优先：`best-ai-design-tools-2026`、`amazon-requirements-ai-white-background-images`、`complete-guide-object-removal-inpainting-ai`
