---
type: upgrade-brief
scope: blog-quality-upgrade
date: 2026-07-13
status: ready
project: lovart
---

# Lovart Blog Wave1 升级 Brief 2026-07-13

## 结论

Wave 1 的 4 篇文章都已经过了第一阶段 signal refresh，但仍处在“能发”而不是“能赢”的状态。

这轮升级不是全文推倒重写，而是先做第二阶段深写：补强定位、导语、证据、决策框架、FAQ 方向和 cluster 角色。

## 1. freepik-ai-image-generator-review

### 基本定位

- 类型：`Review`
- 目标子 skill：`lovart-review`
- cluster 角色：`comparison / decision pillar`
- 目标读者：想知道 Freepik AI 是否够用的设计师、营销团队、创作者、Founder

### 当前版本的主要问题

- 前段仍有旧标题残留：`Is It Really Worth It in 2025?`
- 有重复 CTA，削弱专业感
- 文章虽然长，但判断轴还不够锋利
- 缺少“什么时候 Freepik 足够、什么时候必须换工作流”的明确结论结构

### 本轮必须补

- 一个更锋利的 opening verdict
- bundle value vs workflow ceiling 的判断框架
- pricing / credits / stock advantage / hidden switching cost 的更清晰比较
- anti-recommendation：什么人不用换、什么人应该直接换

### 本轮不必一次做完

- 不强求整篇改到完美评测终稿
- 先把导语、判断轴、决策段落、FAQ 方向立起来

### 多语言建议

- 值得做多语言
- 但前提是英文版先完成“决策型 review”升级

## 2. complete-guide-consistent-ai-character-design

### 基本定位

- 类型：`Complete Guide`
- 目标子 skill：`lovart-complete-guide`
- cluster 角色：`pillar`
- 目标读者：角色创作者、叙事品牌、独立漫画/游戏团队、需要 recurring character 的营销团队

### 当前版本的主要问题

- 文章足够长，但前段仍偏传统 signal refresh 开头
- 重复 CTA 与轻微重复表述削弱密度
- 核心问题“如何稳定锁角色”还没有被压缩成最清晰的决策树

### 本轮必须补

- 用 `reference -> lock -> repair -> train` 重新组织导语
- 把 `reference image / character lock / LoRA` 变成清晰的层级路线
- 补“什么时候 Lovart 足够，什么时候必须上 LoRA / ComfyUI”的边界
- 强化 failure diagnosis：face drift / outfit bleed / pose collapse

### 本轮不必一次做完

- 不需要立刻重写全部 10 章
- 先把 guide 的方法论骨架和决策路径提纯

### 多语言建议

- 非常值得做多语言
- 但必须等英文版先成为真正 canonical guide

## 3. complete-guide-ai-animal-pet-portrait-generation

### 基本定位

- 类型：`Complete Guide`
- 目标子 skill：`lovart-complete-guide`
- cluster 角色：`pillar / commerce-support`
- 目标读者：宠物肖像卖家、纪念礼物创作者、print-on-demand 团队、宠物品牌内容团队

### 当前版本的主要问题

- 正文很长，但前段重复句较多
- 意图没有被快速拆成“单次肖像 / 打印礼物 / 持续宠物角色 / 社媒头像”几种不同工作
- 还像“长文章”，不像“高质量购买与制作决策指南”

### 本轮必须补

- 先用用途分层重写 opening
- 把 likeness / fur detail / print resolution / style fidelity 变成核心判断标准
- 增加“垂类宠物工具 vs 通用 AI 工具”的决策逻辑
- 把谁适合一次性 portrait、谁适合 recurring mascot 说透

### 本轮不必一次做完

- 不需要立刻重写全文后半段
- 先修前段结构和决策框架，去掉重复

### 多语言建议

- 值得做多语言，但优先级低于前两篇

## 4. complete-guide-ai-video-model-selection-2026

### 基本定位

- 类型：`Complete Guide`
- 目标子 skill：`lovart-complete-guide`
- cluster 角色：`pillar`
- 目标读者：正在比较 Sora / Runway / Kling / Pika / Veo 的创作者、广告团队、视频团队、AI 工作流负责人

### 当前版本的主要问题

- 前段出现明显中英混杂，可信度受损
- 文章有信息量，但“按 use case 选模型”的决策逻辑不够前置
- 当前 broad-intent 很强，但没有把自己打造成真正的 benchmark guide

### 本轮必须补

- 彻底清理前段语言污染
- 用 `job-to-be-done` 结构重建 opening
- 明确：
  - premium hero clip 选谁
  - social iteration 选谁
  - editor-first workflow 选谁
  - multi-shot pipeline 选谁
  - Lovart 在其中扮演 orchestration layer 还是 direct generator

### 本轮不必一次做完

- 不急着重写所有模型条目
- 先把开头、比较逻辑、决策矩阵、FAQ 方向拉正

### 多语言建议

- 先不急着扩多语言
- 这篇必须先把英文支柱页质量做稳

## Wave 1 统一施工策略

### 第一轮先修什么

- opening verdict
- 去噪（重复 CTA / 旧标题 / 语言污染 / 重复段）
- 核心 decision framework
- FAQ 方向
- cluster 角色说明

### 第二轮再补什么

- 更细的证据
- 更完整的 first-person tested walkthrough
- 更深的 anti-recommendation
- 更强的 cluster 与转化路径

## 成功标准

这一轮做完后，不要求 4 篇都立刻成为最终版，但至少要做到：

- 读者一打开就知道“这篇怎么帮我做决定”
- 不再只是 signal refresh 合格稿
- 可以继续进入下一轮深写，而不是回炉重做定位
