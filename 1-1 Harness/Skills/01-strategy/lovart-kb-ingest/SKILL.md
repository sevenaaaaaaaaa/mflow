---
description: 知识库采集 skill。从外部来源拉取内容并结构化入库 Knowledge Base。
---
# lovart-kb-ingest — KB 拓源 (crawler + ingest)

> **位置**：1-2 Insight/Knowledge Base/{Changelog,Reference}/URL-LIST.md 是用户给料的入口。
> Skill 读 list → fetch → html→md → 入层 → 重生成 KB-Index，**不会**自动发 publish。
> v0.1 skeleton：HTTP fetch 接 curl，HTML→md 接 markdownify 或 html2text。

---

## When this skill loads

加载条件：

- 用户给了 URL 列表（粘到 Changelog/URL-LIST.md 或 Reference/URL-LIST.md）
- 用户说"抓官方 changelog 入 KB"、"二级 doc 入库"、"capability 词表更新"
- 网站抓了一波，需要把 KB 同步更新
- KB-Index 容量需要扩张（low KB hits on topic → prompt ingest）

不加载：

- 当前 KB 已覆盖目标 topic
- 与 Lovart 无关的外部 URL（KB 是 Lovart-域的 source-of-truth）

---

## Process

### Step 1 — 读 URL list

```
python3 1-2 Insight/Knowledge Base/scripts/kb-ingest.py --root <vault>
```

默认 dry-run：harvest all URLs from both `URL-LIST.md` files, 与 `.ingested.json` cache diff，告诉你**会**抓多少。

### Step 2 — 走 fetch

```
python3 .../kb-ingest.py --root <vault> --allow-fetch --max-per-run 10
```

落地：
- HTML → markdown（markdownify or html2text fallback）
- 落入 `1-2 Insight/Knowledge Base/Changelog/{slug}.md` 或 `Reference/{slug}.md`
- 在 `Changelog/.ingested.json` 记一条 `{url, status, path, ts}`
- 失败 continue，不 abort

### Step 3 — frontmatter + index 重 build

```
python3 .../kb-frontmatter.py --root <vault>
python3 .../build-index.py --root <vault> --write
```

新文件立刻有 KB schema frontmatter（origin=official-crawl-derived, authority=4-5, capabilities 自动 token-match），
KB-Index/{by-topic, citations, capability-glossary}.md 全部重生成。

### Step 4 — KB entry 触发能力词表扩张（v0.3 待做）

训练一个本地 LLM 或用 deepseek 把新 entry 拆解成 atomic claims（带 inline citation marker） — 这是 v0.3 范围，v0.1 只 cover 1-3。

---

## 速率/护栏

- 默认 `--max-per-run 10`：每次 cron / 手动跑至多 10 条 URL 不烧 lovero 站点
- 上 `~/.hermes/agent-cron-add` 加 KB ingest 时用 `0 4 * * *` 频率（夜间慢速）
- 失败不重试同 URL 5 分钟（避免站点故障时暴风循环）

---

## Hard rules

1. **不写 Layer 1+ 之外的格式**：KB ingest 只产生 KB-doc format 的 .md（不要写 .json / .csv 跳出 schema）
2. **不在 ingest 时改 body**：原始 HTML 移除 script/style 后保留 markdown 结构
3. **URL 必须 already-in-URL-LIST**：手入 URL → schema check existing；不走 IRC/bot 推
4. **frontmatter 不强制覆盖**：ingest 完成后 `kb-frontmatter.py` 自动加，新 ingest 不会破坏原 schema_version
5. **不强写**：抓失败只 skip + log；不修改 cache

---

## Failure modes (NEVER)

- 「ingest 把 production URL 写入 Sanity」→ ingest 仅写 vault KB；publish 走另外的 sanity pipeline。
- 「把 URL 直接贴到 Lovart 主站」→ ingest 仅写 KB，不 publish。
- 「自动覆盖原 KB entry」→ `kb-frontmatter.py` 默认 partial；ingest → KB 后老 entry 保留，重复 URL 才覆盖（带版本 bump）。
- 「每天 fetch 100+ URL」→ 站点拥塞 + 限速 + audit 失败；保证 max-per-run=10。

---

## Reference

- 数据接口：`1-2 Insight/Knowledge Base/Changelog/URL-LIST.md` + `Reference/URL-LIST.md`
- cache：`1-2 Insight/Knowledge Base/Changelog/.ingested.json`
- 入库脚本：`1-2 Insight/Knowledge Base/scripts/kb-ingest.py`
- 后处理：`1-2 Insight/Knowledge Base/scripts/kb-frontmatter.py` + `build-index.py --write`
- Shared schema：`1-2 Insight/Knowledge Base/KB-SCHEMA.md`
- 关联 skill：`lovart-kb-mine`（查询 KB）
