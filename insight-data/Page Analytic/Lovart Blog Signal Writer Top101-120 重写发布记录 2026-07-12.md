---
type: audit-report
scope: sanity-blog-signal-refresh
date: 2026-07-12
status: published-top101-120-complete
project: lovart
dataset: production
---

# Lovart Blog Signal Writer Top101-120 重写发布记录 2026-07-12

## 结论

本轮开始执行第二层 `B_indexed_or_visible_refresh`，已完成 Top 101-120，共 20 个 published 文档，并 patch 到 Sanity production。

本轮仍属于第一阶段 signal refresh：按 GSC 查询信号修正搜索意图、标题/SEO、结构块、FAQ、E-E-A-T、内链、图片 brief、CTA 与 Article JSON-LD。最终 7,500 词多轮长文扩写会在更大范围第一阶段完成后统一进入第二阶段。

## 已发布范围

1. `ai-character-consistency-tools-compared`
2. `ai-character-sticker-pack`
3. `7-best-ai-animal-pet-portrait-generators-2026`
4. `vmaker-ai-review`
5. `ai-video-editor-tools-compared`
6. `ai-animal-pet-generators-compared`
7. `how-to-create-music-videos-ai-beat-sync`
8. `creating-negative-space-ai-leave-room-for-text`
9. `ai-image-to-image-guide`
10. `ai-logo-creator`
11. `picsart-ai-review`
12. `pictory-ai-review`
13. `01-pillar-ai-design-technology`
14. `01-bofu-canva-migration-guide`
15. `seedance-ai-review`
16. `complete-guide-ai-animal-pet-portrait-generation`
17. `how-to-choose-ai-image-model`
18. `lovart-nano-banana-2-ai-design-agent`
19. `03-cluster-etsy-listing-images`
20. `nano-banana-presentation-guide`

## 线上验收

published 视角复扫结果：

- 20/20 `seo.noIndex=false`
- 20/20 Article JSON-LD 存在
- 20/20 含 FAQ
- 20/20 含 Derivative Scenarios
- 20/20 含 E-E-A-T Notes
- 20/20 含 Internal Links
- 20/20 含 Image Appendix
- 20/20 含 `https://www.lovart.ai/signup` CTA
- 禁用词与占位符：0 BLOCK

## 过程产物

- 批处理脚本：`tmp/rewrite_signal_batch.py`
- dry-run：`tmp/top101-120-signal-rewrite-dryrun.json`
- apply：`tmp/top101-120-signal-rewrite-applied.json`
- published 复扫：`tmp/top101-120-published-verify.json`

