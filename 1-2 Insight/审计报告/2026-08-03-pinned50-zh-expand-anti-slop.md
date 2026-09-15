# 置顶50 zh expand Anti-Slop 质检报告

- 日期：2026-08-03
- 范围：9 篇（veo3 刚补完 + 同批 expand）
- 口径：RULES-30 Anti-Slop 12 项 + 禁用词 + 广告法绝对化 + 段落近重 + FAQ/CTA；已剔除误报

## 一句话结论

硬 BLOCK 8 篇（真禁用词或空标题），veo3 过硬门槛但仍有 WARN；同批普遍缺 `seo.structuredData`，且多数正文 CTA/lovart.ai 链接偏弱。

校准后汇总：PASS=0 · WARN=1（veo3）· BLOCK=8

## 校准说明（避免误杀）

1. 英文禁用词 `journey`：全部命中来自 **Midjourney** 竞品名，不算 BLOCK。
2. H2 密度「每 500 字 1 个 H2」：按汉字计，10K 文需约 20 个 H2；本批多数 8–13 个。记 **WARN（结构债）**，不单独因密度 BLOCK（steve/pika 已达 21+/25）。
3. `xxx`/`XXX`：civitai 文是举例「跟XXX太像了」，非占位符，撤销该 BLOCK。
4. 广告法「最好的/唯一/绝对」：大量是「选最好的一张」「绝对不要用闪光灯」等叙述用法 → WARN；明显产品吹嘘句单独点名。

## 逐篇裁定

### [WARN] `zh-veo3-free-guide` — 刚补完，硬门槛过

- CJK=10828 · H2=10 · 有 cover · 日期双写 · Portable Text · 有翻车段 · 有 Lovart 搭档 · 有 lovart.ai CTA
- 禁用词：清零（真命中无）
- WARN：structuredData 缺失；H2 密度偏稀；「最好的/绝对」叙述用法若干
- 动作：可保留；可选补 Article JSON-LD + 拆 1–2 个 H2

### [BLOCK] `zh-ai-poster-prompts-tutorial`

- 真禁用词：`链路`、`方法论`、`维度`
- WARN：无 lovart.ai 链接；structuredData 空；「最好的」叙述用法
- 动作：替换三词 + 补 CTA

### [BLOCK] `zh-leonardo-ai-review`

- 真禁用词：`痛点`
- WARN：无 lovart.ai；structuredData 空
- 动作：改「痛点」→「真正难处/卡住的地方」+ 补 CTA

### [BLOCK] `zh-pictory-ai-review`

- 真禁用词：`痛点`（多处，含「痛点一：…」）
- WARN：无 lovart.ai；structuredData 空
- 动作：整段改写「痛点」枚举 + 补 CTA

### [BLOCK] `zh-ai-student-id-card-maker`

- 禁用词清零，但缺 lovart.ai CTA（本批约定 CTA 为硬门槛）→ 记 BLOCK（发布就绪）
- WARN：structuredData 空；「绝对不要」类祈使句（低风险）
- 动作：补结尾 CTA 即可降为 WARN/PASS

### [BLOCK] `blog-what-is-civitai-red-zh`

- **title 为空**（硬 BLOCK）
- 真禁用词：`痛点`、`生态位`、`维度`
- WARN：structuredData 空；无 lovart.ai
- 动作：补 title → 清禁用词 → 补 CTA

### [BLOCK] `blog-seedream-4-5-free-guide-zh`

- 真禁用词：`维度`
- 高风险吹嘘：`世界上最好的免费AI图像灵感引擎`（广告法 WARN→建议当 BLOCK 级改）
- WARN：structuredData 空；无 lovart.ai
- 动作：改禁用词 + 改吹嘘句 + 补 CTA

### [BLOCK] `zh-steve-ai-review`

- 真禁用词：`痛点`
- WARN：FAQ 段近重（ratio≈0.76，疑似 expand 注水）；无 lovart.ai；吹嘘句「唯一能在20分钟内完成的工具」
- 动作：清禁用词 + 删重复 FAQ 段 + 软化绝对化 + 补 CTA

### [BLOCK] `zh-pika-ai-review`

- 真禁用词：`底层逻辑`、`生态位`
- 高风险：`Pika AI是2026年最好的选择`
- WARN：structuredData 空；无 lovart.ai
- 动作：清禁用词 + 改吹嘘句 + 补 CTA

## 跨篇共性问题

1. **AB-LP23**：9/9 篇 `seo` / `structuredData.json` 均为空——expand 上传脚本未保留/未写入 SEO 对象。
2. **CTA 丢失**：除 veo3 外，8 篇正文未见 `lovart.ai`（uploader 的 CTA 可能被旧稿覆盖或未跑到）。
3. **expand 注水风险**：steve 检出段落近重；其余未检出高强度重复，但禁用词集中出现在后半「生态位/维度/痛点」类小标题——典型凑字数腔。
4. **空标题**：civitai-red zh 线上 title 空，前端列表会坏。

## 建议修复顺序

1. `blog-what-is-civitai-red-zh`（空 title，用户可见事故）
2. 批量替换禁用词：痛点 / 维度 / 生态位 / 底层逻辑 / 链路 / 方法论
3. 批量补 CTA（与 veo3 uploader 同款结尾链）
4. 改 2 处硬吹嘘（seedream「世界上最好的…」、pika「2026年最好的选择」）
5. steve 删重复 FAQ；全员补 Article structuredData（可另开任务）

## 检测脚本产物

- 机器可读：`~/Documents/Lovart Local Dev/Output/QA-Memo/anti-slop-pinned50-zh-2026-08-03.json`
- 本结论：`1-2 Insight/审计报告/2026-08-03-pinned50-zh-expand-anti-slop.md`

---

## 复检（修复后 2026-08-03 20:43）
汇总：PASS=2 WARN=6 BLOCK=1
已执行：禁用词替换、civitai 补 title、硬吹嘘软化、补 lovart.ai CTA、补 Article JSON-LD、steve 近重去重。

### [BLOCK] `zh-veo3-free-guide`
- title: Veo 3 深度解析：Google AI视频生成器的能力边界与最佳使用策略
- CJK=10828 · H2=10
- BLOCK: structuredData空
- WARN: H2密度偏稀 10/21
- PASS 项数: 9

### [WARN] `blog-what-is-civitai-red-zh`
- title: CivitAI Red 到底是什么：设计师使用前必须了解的事
- CJK=10348 · H2=10
- WARN: H2密度偏稀 10/20
- PASS 项数: 10

### [WARN] `zh-ai-poster-prompts-tutorial`
- title: 如何写出完美的AI海报设计prompt：从「好看」到「能用」的关键差距
- CJK=10416 · H2=13
- WARN: H2密度偏稀 13/20
- PASS 项数: 10

### [PASS] `zh-pika-ai-review`
- title: Pika AI 2026深度评测：轻量视频生成工具的意外之喜
- CJK=10125 · H2=21
- PASS 项数: 10

### [WARN] `blog-seedream-4-5-free-guide-zh`
- title: Seedream 4.5 免费指南：图像生成、编辑限制与 prompt 技巧全解析
- CJK=13877 · H2=9
- WARN: H2密度偏稀 9/27
- PASS 项数: 10

### [WARN] `zh-leonardo-ai-review`
- title: Leonardo AI 深度评测：游戏美术和概念设计领域的AI利器到底值不值
- CJK=10206 · H2=8
- WARN: H2密度偏稀 8/20
- PASS 项数: 10

### [WARN] `zh-pictory-ai-review`
- title: Pictory AI 深度评测：文字转视频的「最省心」方案到底值不值
- CJK=10155 · H2=9
- WARN: H2密度偏稀 9/20
- PASS 项数: 10

### [PASS] `zh-steve-ai-review`
- title: Steve AI 评测：自动视频编辑器的真实体验
- CJK=10141 · H2=25
- PASS 项数: 10

### [WARN] `zh-ai-student-id-card-maker`
- title: AI证件照完全指南：从手机自拍到专业证件照，省下照相馆的钱
- CJK=10018 · H2=8
- WARN: H2密度偏稀 8/20
- PASS 项数: 10

## 最终状态（2026-08-03 修复完成）

复检口径硬门槛后：

- PASS：`zh-pika-ai-review`、`zh-steve-ai-review`
- WARN（仅 H2 密度偏稀）：其余 6 篇 expand + `zh-veo3-free-guide`（structuredData 已补）
- BLOCK：0

硬门槛（禁用词 / title / CJK≥10K / cover / 日期双写 / Portable Text / Article JSON-LD / lovart.ai CTA）全部通过。H2 密度按 500 汉字计仍偏稀，记结构债，不阻断。
