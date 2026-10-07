---
type: kb-schema
version: 1.0
last_modified: 2026-07-05
audience: [writer profile, quality profile, mining skill, ingest skill]
status: frozen
---

# KB Schema · Lovart Knowledge Base 统一结构

> **目的**：把 KB 从「手贴 .md 文件堆」变成**可查询、可引用、可 authority 排序、可 capability-mapping**的真知识库。
> 当 writer profile（lovart-creation / lovart-page-serp-writer 等）收到 topic 时，必须**先查 KB** 拿到 grounded context 才下笔。当 writer 引用 URL、Lovart 功能名、产品能力时，必须**全部出自 KB**。

---

## 核心理念

| 老范式 | 新范式 |
|--------|--------|
| Blog/landing 由 LLM 通识 + 标题驱动 | Blog/landing 由 KB-grounded context 驱动 |
| 引用 URL 自由发挥 | 引用 URL 必须是 KB 里登记的 authority URL |
| 拓关键词靠 SERP | 拓关键词要回 KB capability glossary 看 LOvart 真有能力吗 |
| 品牌/产品描述自由 | 品牌/产品表述必须 trace back 到 KB-unit |

---

## 四层数据模型

```
Layer 0 — Source File      实际 .md / .docx / json / 网页快照
Layer 1 — KB Unit          一份文件 → 一/多条 unit（frontmatter + body）
Layer 2 — KB Claim         每 unit 内多个原子声明（claim + evidence + source_url）
Layer 3 — KB Index         by-topic / citations / capability-glossary
```

### Layer 0 — Source File

允许类型：
- `.md`（当前已有）
- `.docx`（已有 `.venv` 提示 mammoth/lxml 准备 → 走 `lovart-kb-ingest` 转 md）
- `.pdf`、`html`、`json`（Phase 4 由 crawler 抓取写入）

示例：`Lovart Docs/Tools/Lovart Canvas Tools Master Touch Edit, Smart Select & Hand Tool.md`

### Layer 1 — KB Unit

一份 KB unit = 一个 markdown 文件 + frontmatter。frontmatter 必填字段：

```yaml
---
type: kb-doc | kb-claim-bundle | kb-capability
version: 1.0
# --- origin / authority ---
origin: official-hand-curated-doc | official-lovart | official-news |
        internal-curated | user-curated | user-placed-docx |
        official-crawl-derived
authority: 5         # 5=官方一手，4=官方二手，3=内部 hand-curated 复盘，2=用户手放，1=其他
source_quality: hand-curated-official | cleaned | needs-rerender | user-curated
fetched_at: 2026-XX-XX
# --- topic / capability ---
topics: ["brand", "agent", "canvas", "tools"]
capabilities:
  - "ChatCanvas"
  - "Smart Select"
  - "Hand Tool"
# --- source URLs（这份 doc 内部提到 / 来自哪些 url）---
source_urls:
  - "https://www.lovart.ai/..."
  - "https://www.lovart.ai/news/..."
# --- cross-refs ---
related_docs:
  - "[[Lovart Introduction/Lovart Agent 官方介绍]]"
  - "[[Lovart News/...]]"
# --- meta ---
crawl_status: hand-placed | crawled-{date} | docx-imported
schema_version: 1.0
---
```

### Origin & source_quality 字段语义

`origin` 标文件**来源类型**。
`source_quality` 标在 KB 中**当前可用度**。kb-mine 排序时按 source_quality 加权：

| source_quality | 排序加成 | 实例 |
|----------------|---------|------|
| `hand-curated-official` | **+3.0** | `Lovart Docs/Agent/...md`（一手 hand-curated 官方原文） |
| `cleaned` | +0.5 | post-magic cleanup pass，无残留 |
| `user-curated` | 0 | `_Lovart Introduction/*` 但经过人工校对 |
| `needs-rerender` | **−2.0** | `Reference/www-lovart-*.md`（噪声大，权威压低，避免 writer 引用） |

> **规则**：writer profile 查询 KB 时，**优先** 命中 `hand-curated-official`（干净 + 高权威 + 排序加成）。当 topic 仅在 crawl-derived 中覆盖（如 `/docs/how-to-prompt`），mine 仍会把它们带出，但 quality_boost=-2.0 让 writer 看得到同时也明白质量低。

### Layer 2 — KB Claim (atomic)

Body 内每个具体声明，必须用一致句法挂在 YAML claim 列表（写在 body 末尾或 frontmatter 的 `claims:` 字段）。

```yaml
claims:
  - id: lovart-canvas-tools-001
    text: "Lovart Canvas Master Touch 工具可以编辑任何已生成元素。"
    source_url: "https://www.lovart.ai/docs/canvas/master-touch"
    evidence: "Lovart Canvas Tools Master Touch Edit, Smart Select & Hand Tool.md:line 12-15"
    confidence: high
    citation_marker: "[lovart-canvas-tools-001]"
  - id: lovart-design-agent-002
    text: "Lovart 是 world's first multimodal AI Design Agent (2025-07-28 launch)."
    source_url: "https://www.lovart.ai/news/lovart-design-agent-public-launch-chatcanvas"
    evidence: "Lovart News/...:line 8-12"
    confidence: high
    citation_marker: "[lovart-design-agent-002]"
```

Body 内出现事实声明时，**就用 inline citation marker**：

```markdown
Lovart Canvas Master Touch 可编辑任何已生成元素 [lovart-canvas-tools-001]。
Lovart 于 2025 年 7 月 28 日公开发布 [lovart-design-agent-002]。
```

> 也允许**写 beat 式**：把声明 + 引证绑一行，writer 看到 marker 直接知道从哪查。

### Layer 3 — KB Index (auto-generated)

3 个索引，由 `kb-frontmatter.py` 跑完自动 emit：

| 索引 | 用途 |
|------|------|
| `KB-Index/by-topic.md` | 「我想写'电商商品图' → 给我相关 KB units」 |
| `KB-Index/citations.md` | 「这条 claim 在哪个 unit 里」+ 「这条 claim 被哪篇 blog/landing 引用」 |
| `KB-Index/capability-glossary.md` | **Lovart 产品能力词表**：每个 capability → KB units 列表 → canonical URL。SEO 拓词 / brand / 教程都靠它。 |

> 这些索引**不**手工编辑；frontmatter 改了 → 重新 generate。
> 工具：`insight-data/Knowledge Base/scripts/build-index.py`（Phase 2 写）

---

## 数据流 writer ↔ KB

```
writer profile 启动
  ↓
writer 接 topic (e.g. "Lovart 如何做电商商品图")
  ↓
writer first CALL: lovart-kb-mine --topic "<topic>" --capability-mode
  ↓
miner 返回:
  {
    "topic_hits": [kb-unit A, kb-unit B, ...],
    "capability_hits": [
       {"capability": "ChatCanvas", "kb_units": [...], "canonical_url": "..."},
       ...
    ],
    "verbatim_quotes": [ ... ]      # 可直接 verbatim 复制的句子 + 引证
  }
  ↓
writer 把 KB context 拼到 brief，调用 hermes/opencode 写文
  ↓
writer 必须:
  - 事实声明都用 inline citation marker [claim-id]
  - URL 引用必须出自 capability-glossary 的 canonical_url
  - brand/product 名字必须出自 KB Unit glossary
  ↓
cascade quality checklist（MUST-CITE-KB 规则）
  - 每个 quote / claim 必须有 citation marker
  - 每个 URL 必须命中 KB（不能在 KB 里 = 警告/拒绝）
  - 关键词必须映射到 capabilities（不能映射 = 警告）
```

---

## 与 RULES 的对账

| RULES | 与 KB 的关系 |
|-------|-------------|
| RULES-00 iron | KB ingestion 不删 / 不改 source；frontmatter 不可伪造 authority |
| RULES-30 quality | MUST-CITE-KB 是新增 block_if；与 anti-slop 同级 |
| RULES-20 creation | writer 不能跨越 KB 编造 fact；新 fact 必须先入库 |
| RULES-60 management | KB schema version 由 lovart-management 冻结；变更走 PR |

---

## Phase 路线

| Phase | 此刻 | 范围 |
|-------|------|------|
| P1 | 完成 | Layer 0+1 schema，**24 个现有文件加 frontmatter** |
| P2 | 完成 | Layer 2 claim skeleton，**生成 3 个 KB-Index**，**建 mine/ingest skill** |
| P3 | 待 URL 给 | Layer 0 拓源（爬 Lovart changelog / Reference 等）+ **cascade 接入 KB** |
| P4 | 待 Phase 3 数据累积 | capability-glossary 完全填充 + 引用网络 + cross-graph 整合 |

当 Phase 1+2 完成时，writer profile 可被"先 KB 后写"。这是当前 turn 目标。

---

## Reference

- 上游：项目根 `harness/11-knowledge/`（知识图谱 + 梦境 + audit）
- 下游：`genflow/` (Blog Pipeline / Page Gen) 用 KB 作 context
- 实操：`insight-data/Knowledge Base/scripts/kb-frontmatter.py` / `kb-mine.py` / `kb-ingest.py`
