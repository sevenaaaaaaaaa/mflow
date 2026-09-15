# tools/firecrawl

把 Firecrawl 接进 Lovart 现有项目的最小落地。

## 现状

- 单点脚本:把 `https://www.lovart.ai/changelog` 通过 `/v2/scrape` + JSON Schema
  抓回结构化数据,落盘到 `Output/Firecrawl/changelog-YYYY-MM-DD.json`。
- 输出可直接喂给下游 Sanity pipeline 或 Blog 选题日历。

## 使用

```bash
export FIRECRAWL_API_KEY=***
python3 "$HOME/Documents/Lovart Local Dev/tools/firecrawl/lovart_changelog.py"
```

## 三个端点的取舍(参考本会话真实跑测)

| 端点 | 用途 | 何时不用 |
|---|---|---|
| `/v2/scrape` | 单页 + 可选 json schema 抽取 | 不要全站 |
| `/v2/crawl`  | 全站扫描(异步 job,SDK 自动 poll) | 已知单页 |
| `/v2/agent`  | 无 URL 的自然语言总结 | 知道 URL / 要结构化 |

## 下一步(待你确认再动)

1. cron 化:每周一 09:00 跑 `lovart_changelog.py`,结果发到 Telegram
2. 加 `competitive_changelog.py`:同样的结构化 schema 抓 Midjourney / Runway / Pika
   的 changelog,做对标
3. 接进现有 `Output/Content Calendar/` 的 blog-topic 选取流程