# Lovart Content MKTG — Agent Iron Rules

> **不要再说"我记住了"——直接读这一文件。**
> 这份文档针对 Lovart 用户反复强调的失败模式，写死执行规则。
> 每次新会话开始时，**先扫这份文件再做任何 Blog 发布 / Sanity 写入**。

---

## 🔴 RULE 0 — 置顶文章铁律（用户明确说「不然就卸载」）

### 现象
- 用户在 Lovart Blog 里**人工置顶了某些文章**作为首页/列表的"门面"。
- 任何新发布的 Blog，只要 `publishedAt` 字段为 NULL 或晚于人工置顶文章的日期，**前端会自动把它浮到顶部**，挤掉人工置顶。

### 根因（已证实）
- Sanity `blog` type **没有** `featured` / `pinned` / `sticky` 字段（全部返回 null）。
- 前端排序唯一依赖字段：`publishedAt`（默认 desc）。
- 当 `publishedAt === null` 时，前端/Elementor 回退用 `_createdAt`，新文章立刻排到第一第二。

### 执行规则（每次发布 / import 前后必查）

#### 发布前 — 必查"置顶边界线"
1. 查当前所有人工置顶文章的 **最低 publishedAt**（即最旧的置顶）。
   ```groq
   *[_type=="blog" && pinnedTop==true]{publishedAt, title, slug.current} | order(publishedAt asc)
   ```
   （如 `pinnedTop` 字段不存在，则人工维护一份 `pinned-list.json` 当作 SSOT。）
2. 新文章的 `publishedAt` **必须 ≤ 置顶边界线 − 1 天**，永远不能落在置顶区间内。
3. 默认安全值：`publishedAt = today - 7 days`（即"上周同一天"）。
4. **永不**用 `_createdAt` 当 `publishedAt`。

#### 发布中 — preflight 必须包含此门禁
任何 import / publish 脚本跑之前，必须 output：
```
[置顶铁律] 当前置顶 SSOT: Output/QA-Memo/pinned-list.json
[置顶铁律] 准备 set publishedAt = <date>
[置顶铁律] 拟发布 N 篇，其中 M 篇 publishedAt > 置顶边界线 → 已自动 backdate
```

#### 发布后 — 30 秒内必跑验证
```groq
*[_type=="blog" && language=="en" && publishedAt==null && _createdAt > "<6 weeks ago>"]
```
如果返回值非 0，立刻 patch 每篇到一个 backdate 值。否则立即告知用户。

### 强制约束
- 任何新会话、任何模型、任何执行路径都必须遵守。
- 如果不确定"置顶列表"位置，先查 `Output/QA-Memo/pinned-list.json`。
- 如果找不到，先**问用户**置顶 SSOT 在哪，绝不擅自按当前 publishedAt desc 模拟。
- 用户已经说过"一而再再而三"——本次会话直接固化规则，下次会话从 AGENTS.md 读。

---

## 完整规则目录

依照 Lovart 历史踩坑汇总，铁律如下（每次新增一条加 🔴 编号）：

### 🔴 RULE 0 — 置顶文章铁律（见上）

### 🔴 RULE 1 — Sanity 不动 schemaTypes/
- Schema 修改必须由 Sanity Studio 本地（lovart-wp-headless）或人工在 CMS 后台执行。
- AI Agent 只能 patch 文档内容字段；不得修改 schemaTypes/。

### 🔴 RULE 2 — Sanity publish 永不使用 `--replace` / `deploy`
- 全程 --missing + 增量 patch。
- 任何 "sanity deploy" / "--replace" 命令都直接 BLOCK。

### 🔴 RULE 3 — 删除文档需 user 确认
- 修复优先于删除。任何"异常页"必须先 patch 结构，再考虑删。
- 批量删除前必须先 backup 到 `Output/QA-Memo/deleted-<date>.json`。

### 🔴 RULE 4 — 多语言是要求
- EN/DE/FR/IT/JA/KO/PT/RU/ZH/ZH-TW 都是 SEO+UX 必要组成。
- 任何新页面发布后，必须同步建立多语言版本。

### 🔴 RULE 5 — preflight BLOCK=0 才能 publish
- 不许绕。block>0 即暂停，先修复。

### 🔴 RULE 6 — 报告必须有环比
- 当期快照不允许发。月报 13 章节、每节末有洞察。
- 天数不等时用日均值对比。

### 🔴 RULE 7 — 写作质量 > 一切
- 不堆关键词、不编数据、不写 AI 味。每段回答 4 个 W。
- 多语言必须重写，不许逐句翻译。

### 🔴 RULE 8 — 行为模式
- 结论在前、数据在后。
- 不许 P0/P1/P2 矩阵。简单数字列表。
- 一次问就充分，不二次确认低风险决定。
- 不问就干："继续" = 直接执行。

### 🔴 RULE 9 — 新发布博客必须 backdate 90 天 + 表格 Portable Text 必带 _key
**根因（2026-07-07 发现，已修）**：
- `Output/SEO-Reports/Refactoring/scripts/patch-sanity.py` 之前完全没设 `publishedAt` 字段，导致所有走这条管线的博客 publishedAt 丢失（fallback 到 `_createdAt`，前端立即显示为最新）。
- `translate_it_reliable.py` 之前依赖 EN 源透传 publishedAt，EN 源是 2026-05 系列日期，所以 it 翻译全部聚集在 5 月而非"近期"分散。
- `markdown_to_portable_text` 表格转换缺 `_key`（顶层、row、cell 都缺），Sanity 强 schema 下前端渲染丢格式。

**强制约束**：
1. **任何**新发布/翻译/refactor 脚本最终 create 或 patch 文档时，`publishedAt` 必须显式设置 = `(today_now - 90 天) + 8h`（或更早）。可以比 90 天更早，但绝不能比今天新。
2. **`publishedAt` 必须 `< pinned-list.json boundary_floor.value - 1 天`** —— pin 边界保护。
3. Markdown 表格转换必须走 SSOT `~/Documents/Lovart Local Dev/scripts/md_to_portable_text.py`。
   Lovart 已部署 schema：`tableRow.cells` = **`string[]`**（不是 block，也不是 tableCell）。
   合法形态：`table(_key) → tableRow(_key) → cells: ["文本", ...]`。
   禁止：cells 塞 `_type:block` / `_type:tableCell`；禁止脚本内联 `def md_to_pt`。
   import 前跑：`python3 validate_pt_body.py --ndjson import.ndjson`（BLOCK>0 停）。
4. 任何发布后 30 秒内必跑自检：
   ```groq
   *[_type=="blog" && publishedAt==null && !(_id in path("drafts.**"))]{_id, title}
   ```
   返回非 0 立即 patch。

### 🔴 RULE 10 — 新发布博客必须设 coverImage（2026-07-22）
**根因**：`_patch_zh_blogs.py` 及多个 translate 脚本 `createOrReplace` blog 时不设 `coverImage`，导致新博客列表页无封面。

**封面库**（SSOT 在 `sanity_helpers.py` 的 `COVER_POOL`）：
- 15 张 `/images/blog/xxx-hero.jpg`（设计专题，assets-persist.lovart.ai CDN 代理）
- 9 张 `https://liblibai-online.liblib.cloud/blog-card-cover/xxx.png`

**强制约束**：
1. **任何**新 blog 的 `createOrReplace` mutation **必须**包含 `coverImage` 字段 = 从 COVER_POOL 随机选取。
2. `releaseDate` 必须与 `publishedAt` 同时设置（见 RULE 9）。
3. 发布后 30 秒内必跑自检：
   ```groq
   *[_type=="blog" && (!defined(coverImage) || coverImage == "")]{_id, title}
   ```
   返回非 0 立即 patch。
4. `sanity_helpers.py` 提供了 `make_blog_doc(id, title, slug, language, body)` 工厂函数——自动注入 coverImage + publishedAt + releaseDate。所有新脚本应使用此函数。

### 🔴 RULE 11 — publishedAt vs releaseDate 字段用途铁律（2026-07-31）
**根因（已犯无数次）**：前端 Blog 列表页排序**只认 `releaseDate` 字段**，不认 `publishedAt`。
- `publishedAt` = SEO/语义发布时间，用于 RSS、sitemap、结构化数据。`前端列表排序不用它`。
- `releaseDate` = **前端列表页实际排序字段**（`order(releaseDate desc)`）。改排序 = 改 `releaseDate`。

**强制约束**：
1. **任何排序/沉底/置顶操作，一律改 `releaseDate`，不是 `publishedAt`**。改 `publishedAt` 无效。
2. 新发布/翻译时 `releaseDate` 必须与 `publishedAt` 同时设置（二者值可相同，但必须都存在）。
3. 自检查询（验证排序是否生效）必须查 `releaseDate`：
   ```groq
   *[_type=="blog" && language=="ja"] | order(releaseDate desc) {title, releaseDate}[0..5]
   ```
4. **多语言权重分层**（核心排序逻辑）：
   按"语言匹配度 + 内容质量"分三层，用 `releaseDate` 日期差实现权重：
   - **Tier A（最高）**：语言纯正匹配 + 质量达标 → `releaseDate` = 近期（如 `2026-07-29`）
     - `ja`：正文 CJK(日) > 10% 且英文占比 < 30%；`zh-TW`：繁体 CJK > 10% 且英文占比 < 30%
     - 质量达标：无 `[IMAGE PLACEHOLDER]` 残留、正文 ≥ 800 字
   - **Tier B（中）**：混排（目标语言 + 英文/中文混杂，有部分翻译）→ `releaseDate` = 中间（如 `2026-01-15`）
     - 判定：目标语言 CJK > 10% 但英文占比 ≥ 30%
   - **Tier C（最低，沉底）**：纯英文/中文照搬（未翻译）或质量极低 → `releaseDate` = 最老（如 `2025-01-01`）
     - 判定：`ja`/`zh-TW` 正文 CJK ≤ 10%（英文正文）；或 `[IMAGE PLACEHOLDER]` 残留 ≥ 3；或正文 < 500 字
   - 日期降序 = 权重降序：Tier A > Tier B > Tier C
5. 任何时候不确定前端用哪个字段 → 先跑 `order(releaseDate desc)` 验证线上排序，不要猜。
