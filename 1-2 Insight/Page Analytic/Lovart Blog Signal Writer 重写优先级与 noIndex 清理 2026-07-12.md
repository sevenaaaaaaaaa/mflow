---
type: audit-report
scope: sanity-blog-signal-refresh
date: 2026-07-12
status: priority-queue-ready
project: lovart
dataset: production
---

# Lovart Blog Signal Writer 重写优先级与 noIndex 清理 2026-07-12

## 结论

已按用户要求确认主站 Sanity Blog published 视角不存在任何 `seo.noIndex=true`。本轮没有删除 production 文档，没有修改 schema，没有执行 `sanity deploy`，没有使用 `--replace`。

已拉取最近 28 天 GSC page 与 page×query 数据，并与 961 篇英文 Blog 元数据合并，生成 `lovart-blog-signal-writer` 重写优先级队列。

## noIndex 结果

- 检查范围：Sanity production 中 `_type == blog` 且非 `drafts.*` 的 published Blog。
- `seo.noIndex == true`：0。
- 因复扫已为 0，本轮没有实际需要 patch 的 noIndex 文档。

## GSC 数据口径

- 时间范围：2026-06-12 至 2026-07-10。
- GSC page 行数：12,161。
- GSC page×query 行数：25,000，上限已触达。
- Sanity 英文 Blog：961 篇。

## 分层结果

- 第一批：有流量/排名 Top 100：100 篇。
- 第二批：已可见或可收录页面：731 篇。
- 第三批：长尾低价值复核：130 篇。

## 第一批 Top 20

1. `freepik-ai-image-generator-review`：28 天点击 736，曝光 268718，平均排名 7.31，主查询 `freepik ai`。
2. `ai-branding-design`：28 天点击 435，曝光 19118，平均排名 10.58，主查询 `branding ai`。
3. `ai-poster-prompts-tutorial`：28 天点击 213，曝光 6106，平均排名 5.71，主查询 `prompt buat poster ai`。
4. `what-is-civitai-red`：28 天点击 45，曝光 18972，平均排名 6.68，主查询 `civitai red`。
5. `how-to-use-veo3-free`：28 天点击 154，曝光 5554，平均排名 8.63，主查询 `veo 3 free unlimited no sign up`。
6. `10-best-ai-video-editing-tools-2026`：28 天点击 3，曝光 21245，平均排名 7.94，主查询 `capcut ai video workflow long form production 2026`。
7. `craiyon-ai-review`：28 天点击 42，曝光 10846，平均排名 6.78，主查询 `craiyon`。
8. `complete-guide-consistent-ai-character-design`：28 天点击 19，曝光 13872，平均排名 11.34，主查询 `ai image generation face consistency techniques 2026`。
9. `krea-ai-video-generator-review`：28 天点击 15，曝光 10857，平均排名 7.91，主查询 `krea ai review`。
10. `runway-alternatives`：28 天点击 20，曝光 9988，平均排名 7.67，主查询 `runway ml alternative`。
11. `pika-ai-review-2025-ai-video-generation-platform-hands-on-test`：28 天点击 0，曝光 12430，平均排名 8.41，主查询 `无 page×query 命中`。
12. `text-art-ascii-tools-compared`：28 天点击 49，曝光 4652，平均排名 6.68，主查询 `patorjk`。
13. `seedream-4-5-free-guide`：28 天点击 68，曝光 3201，平均排名 8.56，主查询 `seedream 4.5 free`。
14. `ai-powered-design-agent-for-creators`：28 天点击 12，曝光 8950，平均排名 5.85，主查询 `ai design agent`。
15. `best-ai-design-tools-2026`：28 天点击 4，曝光 8655，平均排名 11.07，主查询 `microsoft designer`。
16. `best-ai-design-tools-2026`：28 天点击 4，曝光 8655，平均排名 11.07，主查询 `microsoft designer`。
17. `media-io-review`：28 天点击 26，曝光 5393，平均排名 7.97，主查询 `media.io`。
18. `luma-dream-machine-review-2025-features-pricing-and-honest-performance-test`：28 天点击 4，曝光 8023，平均排名 9.79，主查询 `luma dream machine`。
19. `hedra-ai-review`：28 天点击 29，曝光 4715，平均排名 7.85，主查询 `hedra ai`。
20. `imagefx-review`：28 天点击 25，曝光 4691，平均排名 10.94，主查询 `imagefx`。

## 执行文件

- 队列 CSV：`1-2 Insight/Page Analytic/lovart-blog-signal-writer-priority-queue-2026-07-12.csv`。
- 过程 JSON：`tmp/lovart-blog-signal-writer-priority-queue-2026-07-12.json`。
- GSC + Sanity 输入缓存：`tmp/blog_signal_priority_inputs.json`。

## 下一步

第一批从 Top 100 开始逐篇按 `lovart-blog-signal-writer` 真实重写：使用 GSC 主查询和 page×query 组合确定搜索意图，重写 title/meta/intro/章节/FAQ/内链，并做 quality gates。第二批处理已被 GSC 看见但信号较弱的页面。第三批只做长尾复核，决定是否合并、保留、或低优先级改写。
