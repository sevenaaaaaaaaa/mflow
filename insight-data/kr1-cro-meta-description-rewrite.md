# KR1 CRO Action #3 — 5 个非品牌词 Meta 重写（终版）

> **日期**：2026-06-14
> **数据来源**：GSC 5 月第 4 周数据
> **目标**：CTR 从 <0.3% → 2-3%

---

## 当前状态 vs 优化方案

### 1. freepik ai image generator（最大机会）

| 维度 | 当前 | 优化后 |
|------|------|--------|
| **页面** | `/blog/freepik-ai-image-generator-review` | 同一页面，改 Meta |
| **展示量** | 28,270/周 | — |
| **CTR** | 0.11% | 目标 2.5% |
| **排名** | 5.84 | — |
| **当前 Title** | `Freepik AI Image Generator Review: Is It Really Worth It in 2026? \| AI Design Guide by Lovart` | |
| **当前 Description** | （评测文章通用描述） | |

**优化后**：

```
Title: Freepik AI Image Generator — Free Alternative with Design Agent | Lovart

Description: Looking for a Freepik AI alternative? Lovart's free AI design agent generates 
logos, posters, brand kits & marketing assets from one brief. 500 daily credits, no credit card. 
Try the AI design agent that 10M+ creators trust.
```

**改法**：Sanity CMS → 找到这篇博客 → 修改 `seo.title` 和 `seo.description` 字段

---

### 2. flora ai

| 维度 | 当前 | 优化后 |
|------|------|--------|
| **页面** | `/blog/flora-ai-review` | 同一页面，改 Meta |
| **展示量** | 13,244/周 | — |
| **CTR** | 0.27% | 目标 2.5% |
| **排名** | 6.85 | — |
| **当前 Title** | `Flora AI Review: An Honest Look at This Nature-Focused Image Generator \| Best AI Tools by Lovart` | |

**优化后**：

```
Title: Flora AI Alternative — Free AI Image Generator for All Styles | Lovart

Description: Beyond nature-only generators. Lovart's AI design agent creates any visual style — 
logos, brand kits, posters, product photos — from one brief. Free 500 daily credits. 
No design skills needed.
```

---

### 3. artlist ai

| 维度 | 当前 | 优化后 |
|------|------|--------|
| **页面** | `/blog/artlist-ai-review` | 同一页面，改 Meta |
| **展示量** | 8,873/周 | — |
| **CTR** | 0.27% | 目标 3.5% |
| **排名** | **5.17**（前 5！） | — |
| **当前 Title** | `Artlist AI Review: When Music Platform Meets Video Generation \| Best AI Tools by Lovart` | |

**优化后**：

```
Title: Artlist AI Alternative — Free AI Design Agent with Video + Image | Lovart

Description: Lovart is a free AI design agent that creates brand visuals, marketing assets & 
video content from one brief. More than a music platform — full creative campaigns in minutes. 
Trusted by 10M+ creators.
```

**特别说明**：artlist ai 排名已进前 5，是 5 个词中最容易出效果的。只需改 Title/Description 就能大幅提升 CTR。

---

### 4. luma dream machine

| 维度 | 当前 | 优化后 |
|------|------|--------|
| **页面** | `/blog/luma-dream-machine-review` | **需要补充内容**（当前几乎空壳） |
| **展示量** | 5,714/周 | — |
| **CTR** | 0.21% | 目标 2.0% |
| **排名** | 8.46 | — |
| **当前 Title** | `Luma Dream Machine Review - Best Practice \| AI Design Tool by Lovart` | |
| **页面内容** | ⚠️ 几乎无正文，只有引导语和相关文章链接 | |

**优化后**：

```
Title: Luma Dream Machine Alternative — AI Video + Design Agent | Lovart

Description: Lovart goes beyond video generation. Create complete brand campaigns — 
logos, posters, social media & video — with one AI design agent. Free to start. 
500 daily credits, no credit card required.
```

**⚠️ 需要同时补充页面正文**：当前页面是空壳，即使 Meta 优化了，用户点进来也会立即跳出。建议至少补充 500 字的 Luma vs Lovart 对比内容。

---

### 5. freepik ai（意大利语页面问题）

| 维度 | 当前 | 优化后 |
|------|------|--------|
| **页面** | `/it/blog/freepik-ai-image-generator-review` ⚠️ | 需要英文版页面 |
| **展示量** | 1,500/周 | — |
| **CTR** | 0.27% | — |
| **排名** | 6.16 | — |

**问题**：英文搜索词 "freepik ai" 关联到了意大利语页面。

**解法**：
1. 确认英文版 `/blog/freepik-ai-image-generator-review` 是否存在
2. 如果存在，在英文版页面的 `<head>` 中加入 `<link rel="canonical">` 指向英文版
3. 如果不存在，创建英文版页面（复用意大利语版内容翻译）

---

## 预期效果汇总

| 关键词 | 当前周展示 | 当前 CTR | 当前周点击 | 优化后 CTR | 预期周点击 | 周增量 |
|--------|-----------|---------|-----------|-----------|-----------|--------|
| freepik ai image generator | 28,270 | 0.11% | 31 | 2.5% | 707 | +676 |
| flora ai | 13,244 | 0.27% | 36 | 2.5% | 331 | +295 |
| artlist ai | 8,873 | 0.27% | 24 | 3.5% | 311 | +287 |
| luma dream machine | 5,714 | 0.21% | 12 | 2.0% | 114 | +102 |
| freepik ai | 1,500 | 0.27% | 4 | 2.5% | 38 | +34 |
| **合计** | **57,601** | **0.19%** | **107** | **2.6%** | **1,501** | **+1,394** |

**月度增量**：+1,394 × 4.3 = **+5,994 点击/月**
**注册增量**：5,994 × 14.4% = **+863 注册/月**（占 O2 缺口 45,000 的 1.9%）

---

## 执行优先级

| 优先级 | 动作 | 工作量 |
|--------|------|--------|
| **P0** | artlist ai — 改 Title/Description（排名前5，最容易出效果） | 5 分钟 |
| **P0** | freepik ai image generator — 改 Title/Description（展示量最大） | 5 分钟 |
| **P0** | flora ai — 改 Title/Description | 5 分钟 |
| **P1** | luma dream machine — 改 Meta + 补充页面正文 | 1-2 小时 |
| **P1** | freepik ai — 修复英文版 canonical 指向 | 10 分钟 |

**总计**：30 分钟改 Meta + 1-2 小时补内容。改完后 2-4 周可在 GSC 看到 CTR 变化。

---

*KR1 CRO Action #3 终版。下一步：在 Sanity CMS 中修改这 4 篇博客的 seo.title 和 seo.description。*
