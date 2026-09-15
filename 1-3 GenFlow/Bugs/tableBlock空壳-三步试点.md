# tableBlock 空壳 — 三步试点与 DE 扩量（2026-08-05）

## 人话结论

按约定三步走：EN MD 干净表 → 德语重写 → 只补 `rows`（完整 body + 指纹门禁），每批 ≤10。  
**DE 空壳文档 192 → 156**（空节点约 279 → 200）。未全量，未抄英文进德文。

## Step 1 补源

本地几乎没有德/法 MD。可用路径：

1. EN 草稿 / Content Calendar MD 里**干净矩形表**当语义源  
2. 按空表前后标题对齐槽位  
3. **德语重写**（保留 Lovart / Brand Kit / Touch Edit / ChatCanvas / MCoT / Edit Elements / Auto-Resize / Seedance）  
4. 定价数字只来自同文 Draft；图注附录 / 对不上的 FAQ 槽 → 跳过

机器源目录：`~/Documents/Lovart Local Dev/Output/QA-Memo/tableblock-de-*.json`

## Step 2 只 patch rows

- 拉完整 `body`  
- 只重建目标下标 `{_type:tableBlock,_key?,rows}`  
- 其它节点 JSON 指纹不变；CTA link / `_key` 不回退  

## 已修汇总（DE）

早期试点 + batch2：prompts / freepik / flora×2 / vidu

batch3（10 槽 / 6 篇）：

- `picsart-ai-vs-lovart-comparison` @22 功能矩阵、@35 定价（@45 FAQ 跳过）  
- `ai-design-roi-calculator-how-to-measure` @47/49/51 三例 ROI → stillBad=0  
- `ab-testing-designs-generating-variations-ai` @8 假设、@34 结果（@48 跳过）  
- `how-to-build-design-system-with-ai` @66 Build vs Buy → stillBad=0  
- `brand-kit-attorney-lovart` @9 配色  
- `ai-art-platforms-compared-2026` @10 四强矩阵  

batch4（10 槽）：platforms @30 Community；accountant/architect/bakery-artisan 配色；6 篇 brand-kit 字体表  

batch5（10 槽）：再 10 篇 brand-kit 字体表  

batch6–7（17 槽）：brand-kit 字体表继续；**可对齐 brand-kit 槽已耗尽**，剩 ~27 多为 FAQ/附录  

batch9（10 槽）：`pricing-page-meta-optimization` 4 表清零；`ai-banner` 主对比；`ai-video-models` 3 表；`auto-resize` 平台尺寸；`case-study-stock` 结果表  

batch10–11（18 槽）：`design-workflow` 框架+P3/P4/P5/合计（@33/@45/@80 无 MD 对应仍跳过）；body/collage/animal/background/text-art 主对比；animal 品种准确度；background 手机壁纸；image-model-selection 2 表；vet case-study；google-ads asset map + Do/Don't  

batch12（4 槽，Content Calendar 非 brand-kit 扫尾）：  
- `how-to-choose-ai-art-platform` @33 Preisvergleich（MD 价表，标 laut Draft）  
- `complete-guide-ai-music-video-creation` @30 工具表  
- `how-to-create-floor-plans-architecture-ai` @23 阶段表  
- `how-to-create-music-videos-ai-beat-sync` @46 平台导出表  

**Content Calendar 非 brand-kit 可对齐队列已耗尽**：剩余空壳多为 FAQ / 图注附录 / related-link 尾 / 标题与 MD 表意不对齐（强塞会错位）。

## 刻意跳过

- 图注 / Image Appendix 空壳  
- FAQ 区无 MD 对应表（banner/auto-resize/animal/body/collage/video/text-art 残留等）  
- `flora-ai-review` @12 Core Feature（EN 无功能表）  
- brand-kit 残留 ~27：多半 FAQ/附录  
- `design-workflow` @33/@45/@80：Agency-wins / E-E-A-T 区，无对应数据表  
- `step-by-step-ad-creatives` @30：附录槽，不放 Step4 copy 表  
- `complete-guide-ai-avatar` @45：3D/FAQ 区，不对齐 headshot 表  
- `price-lists` @23：结构步骤槽，不对齐心理学表  

## 下一轮可选

1. 扩大源：非 Content Calendar 的草稿/history（仍要上下文对齐）  
2. FAQ/附录空壳：要么删壳（需单独决策），要么留着不填  
3. 开 FR 同流程（同样小批 + 德语同级的法语重写）  
4. 仍不一次清完 ~156  
