# EN Blog History-only 全量质量审计 — 2026-08-03

> 锚点：`2026-07-20T00:00:00Z`；范围：当前 24-H2 污染且无本地 07-17 draft 的 EN blog
> 总数：**955**

## 结论

- 可直接/清洗后恢复（HISTORY_OK + SCRUB）：**304**
- 可恢复但偏弱、需 refresh（HISTORY_OK_WEAK）：**620**
- 不宜当最终态 / 应重写（EMPTY+THIN+PADDED+ERROR）：**31**
  - EMPTY **19** / THIN **12** / PADDED **0**
- okish 均分 **60.7**，均词数 **2169.2**，FAQ 率 **99.0%**，含坏内链比例 **0.3%**

## 标签分布

- `HISTORY_OK_WEAK`: **620**
- `HISTORY_OK`: **302**
- `HIST_EMPTY`: **19**
- `HIST_THIN`: **12**
- `HISTORY_OK_SCRUB`: **2**

## 标签含义

| 标签 | 含义 | 动作 |
|------|------|------|
| HISTORY_OK | ≥1800 词、未污染、问题少 | 只恢复 body，保留当前 SEO |
| HISTORY_OK_SCRUB | 可恢复但有坏链/禁词 | 恢复 body + 清洗 |
| HISTORY_OK_WEAK | 900–1799 词 | 恢复 body，标 needs-refresh |
| HIST_THIN | 100–899 词 | 高 GSC 可暂恢复+重写，否则 rewrite |
| HIST_EMPTY | <100 词或无 body | 禁止恢复，signal-writer |
| HIST_PADDED_REJECT | 07-20 已含污染骨架 | 禁止用该锚点；另寻更早 revision 或 rewrite |

## 各桶 GSC Top15

### HISTORY_OK (302)

| Imp | Clk | Score | Words | H2 | BadL | Slug |
|----:|----:|------:|------:|---:|-----:|------|
| 25192 | 70 | 70 | 7785 | 14 | 0 | `hedra-ai-review` |
| 18299 | 9 | 64 | 2677 | 11 | 0 | `ai-art-copyright-2026` |
| 11237 | 21 | 76 | 8295 | 33 | 0 | `complete-guide-consistent-ai-character-design` |
| 6914 | 23 | 70 | 8299 | 16 | 0 | `haiper-ai-review` |
| 4063 | 3 | 70 | 2630 | 5 | 0 | `ai-powered-design-agent-for-creators` |
| 2960 | 1 | 70 | 8367 | 28 | 0 | `ai-video-models-compared-2026` |
| 2864 | 10 | 64 | 2014 | 11 | 0 | `media-io-review` |
| 2207 | 15 | 70 | 4511 | 8 | 0 | `ai-brand-kit-generator-indie-brands` |
| 2008 | 2 | 70 | 8452 | 29 | 0 | `complete-guide-ai-face-retouching-portrait-editing` |
| 1927 | 1 | 64 | 2182 | 14 | 0 | `adobe-firefly-vs-ai-design-agents` |
| 1919 | 2 | 64 | 2570 | 9 | 0 | `law-firm-branding-trust-authority-design-2027` |
| 1474 | 5 | 76 | 7522 | 20 | 0 | `complete-guide-free-ai-design-tools-2026` |
| 1383 | 10 | 70 | 3067 | 10 | 0 | `complete-guide-ai-texture-material-generation` |
| 1212 | 0 | 64 | 2850 | 10 | 0 | `best-ai-design-agent-for-ecommerce-seller` |
| 1212 | 0 | 64 | 2882 | 8 | 0 | `best-ai-design-agent-for-ecommerce-seller` |

### HISTORY_OK_WEAK (620)

| Imp | Clk | Score | Words | H2 | BadL | Slug |
|----:|----:|------:|------:|---:|-----:|------|
| 13784 | 8 | 58 | 1603 | 17 | 0 | `luma-dream-machine-review-2025-features-pricing-and-honest-performance-test` |
| 6880 | 17 | 58 | 1578 | 17 | 0 | `imagefx-review` |
| 5206 | 0 | 58 | 1606 | 17 | 0 | `best-ai-design-tools-2026` |
| 5206 | 0 | 58 | 1606 | 17 | 0 | `best-ai-design-tools-2026` |
| 3185 | 6 | 64 | 1584 | 17 | 0 | `sora-ai-review` |
| 2930 | 8 | 58 | 1586 | 15 | 0 | `twitter-image-design-guide` |
| 2480 | 5 | 58 | 1773 | 17 | 0 | `canva-ai-image-generator-review` |
| 2343 | 7 | 58 | 1739 | 17 | 0 | `adobe-illustrator-alternatives` |
| 1681 | 1 | 58 | 1521 | 10 | 0 | `best-sora-alternatives-in-2025-7-ai-video-generators-compared` |
| 1568 | 7 | 58 | 1658 | 17 | 0 | `hailuo-ai-alternatives` |
| 1508 | 1 | 58 | 1510 | 11 | 0 | `adobe-firefly-review-2025-features-pricing-and-honest-hands-on-test` |
| 1391 | 10 | 58 | 1580 | 15 | 0 | `discord-community-design-guide` |
| 1315 | 3 | 58 | 1747 | 17 | 0 | `free-ai-design-tools-2026` |
| 1235 | 7 | 58 | 1604 | 15 | 0 | `how-to-convert-images-vector-free-bing` |
| 1234 | 4 | 58 | 1772 | 17 | 0 | `hailuo-ai-review-2025-cinematic-video-generation-tested-hands-on` |

### HISTORY_OK_SCRUB (2)

| Imp | Clk | Score | Words | H2 | BadL | Slug |
|----:|----:|------:|------:|---:|-----:|------|
| 1320 | 1 | 65 | 8098 | 27 | 5 | `how-to-choose-ai-image-model` |
| 213 | 0 | 58 | 2162 | 13 | 0 | `why-ai-video-background-removal-is-a-game-changer` |

### HIST_THIN (12)

| Imp | Clk | Score | Words | H2 | BadL | Slug |
|----:|----:|------:|------:|---:|-----:|------|
| 0 | 0 | 59 | 886 | 6 | 0 | `ai-commercial-ad-generator` |
| 0 | 0 | 59 | 881 | 5 | 0 | `ai-video-generation` |
| 0 | 0 | 59 | 835 | 6 | 0 | `background-removal` |
| 0 | 0 | 59 | 860 | 6 | 0 | `character-consistency` |
| 0 | 0 | 59 | 801 | 6 | 0 | `graphic-design` |
| 0 | 0 | 59 | 872 | 6 | 0 | `logo-design` |
| 0 | 0 | 59 | 862 | 6 | 0 | `motion-control` |
| 0 | 0 | 59 | 856 | 6 | 0 | `poster-design` |
| 0 | 0 | 59 | 863 | 6 | 0 | `social-media-video` |
| 0 | 0 | 59 | 899 | 6 | 0 | `talking-avatar` |
| 0 | 0 | 59 | 817 | 6 | 0 | `text-to-image-brand-assets` |
| 0 | 0 | 59 | 826 | 6 | 0 | `workflow-automation` |

### HIST_EMPTY (19)

| Imp | Clk | Score | Words | H2 | BadL | Slug |
|----:|----:|------:|------:|---:|-----:|------|
| 0 | 0 | 6 | 0 | 0 | 0 | `ai-design-business-faq` |
| 0 | 0 | 6 | 0 | 0 | 0 | `ai-design-copyright-faq` |
| 0 | 0 | 6 | 0 | 0 | 0 | `ai-design-tools-faq` |
| 0 | 0 | 6 | 0 | 0 | 0 | `ai-image-generation-faq` |
| 0 | 0 | 6 | 0 | 0 | 0 | `ai-video-generation-faq` |
| 0 | 0 | 6 | 0 | 0 | 0 | `best-ai-design-tools-comparison` |
| 0 | 0 | 6 | 0 | 0 | 0 | `content-creator-toolkit` |
| 0 | 0 | 6 | 0 | 0 | 0 | `free-vs-paid-ai-design-tools` |
| 0 | 0 | 6 | 0 | 0 | 0 | `how-to-batch-create-designs-ai` |
| 0 | 0 | 6 | 0 | 0 | 0 | `how-to-convert-images-vector-free` |
| 0 | 0 | 6 | 0 | 0 | 0 | `how-to-create-designs-with-ai` |
| 0 | 0 | 6 | 0 | 0 | 0 | `how-to-design-business-cards-ai` |
| 0 | 0 | 6 | 0 | 0 | 0 | `how-to-generate-consistent-characters-ai` |
| 0 | 0 | 6 | 0 | 0 | 0 | `how-to-generate-product-images-ai` |
| 0 | 0 | 6 | 0 | 0 | 0 | `how-to-make-social-media-content-ai` |

### HIST_PADDED_REJECT (0)

（无）

## SEO 问题频次（历史文档字段，非当前 production）

- `gsc_intent_template`: 757
- `seo_title_long`: 188
- `seo_desc_len`: 40
- `seo_title_missing`: 21
- `seo_desc_missing`: 19
- `desc_missing`: 19

## 产物

- JSON: `/Users/seveno/Documents/Lovart Local Dev/Output/QA-Memo/en-history-only-quality-audit-2026-08-03.json`
- CSV: `/Users/seveno/Documents/Lovart Local Dev/Output/QA-Memo/en-history-only-quality-audit-2026-08-03.csv`

## 对原策略的修正

- 此前把 ~951 篇 history_only 默认当成 HISTORY_OK_CANDIDATE **过乐观**。
- 必须以本清单为准：EMPTY/THIN/PADDED 不得直接当终态恢复。
- 恢复仍建议 **只 patch body**，当前 SEO 若已清洁则保留。
