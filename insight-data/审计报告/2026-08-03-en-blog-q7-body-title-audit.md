# EN Blog Q7 正文模板 + 标题长度审计 — 2026-08-03

## 结论

1. **Q7 属实，但表述需精确：不是「全文每个字节克隆」，而是「换标题的近重复长文」。** 1,300/1,314 篇 EN blog（**98.9%**）共享 **完全相同的 24 个 H2（顺序也相同）**；正文长度全挤在 **20,503–21,109** 字符；开场/中段 boilerplate 同源。
2. **2026-08-03 全量复查（1300/1300 padded）**：H2 序列唯一值 = **1**（100% 命中同一大纲）。8 篇跨品类抽样（Freepik review / branding / Hedra / Sora / realtor agent / Twitter guide / year-in-review / Canva migration）去标题后两两相似度 **0.979–0.990**，共享字符约 **98.7%**。SHA 不同 ≠ 内容不同——只是标题嵌入与极小差分。
3. **真正独立正文只有 14 篇**（近期 column/review 重写，如 `flora-ai-review`）。对照样本开场是真实叙事，且 **不含**「The 6 use cases…」骨架。
4. **模板另有硬伤**：污染正文把 MCoT 错写成 `Multi-Chain of Thought`（正确应为 Mind Chain of Thought）——8/8 抽样命中错误释义，说明是灌库脚本产物，不是人工写作。
5. **「标题过短」**：多数 T1 标题已被改过；残留问题是 slug 标题与 `seo.title` 壳，见后文。权限已于同日提升为项目 Administrator。

## 复查记录（2026-08-03 12:04，production / published）

问：线上 EN blog 是不是真的全都被改成一模一样？

答：**几乎是——准确说是 1,300/1,314 篇近重复同骨架，不是 14 篇之外还有独立长文。**

全量核对（perspective=published）：

- total EN = 1,314
- h2==24 = 1,300；h2≠24 = 14
- 含固定句 `The 6 use cases and their real timelines` = 1,300
- 含 `The benchmark data from 142 campaigns` = 1,300
- 含 Canva 开场 `Template-based tools like Canva*` = 1,304（含少量非 24-H2 正文里顺带提到 Canva）
- 对 1,300 篇 padded **逐篇拉取 H2 列表**：unique H2 sequence = **1（100%）**
- 正文长度：min 20,503 / max 21,109 / avg 20,937
- 跨品类 8 篇全文去标题比对：相似度 97.9%–99.0%；Freepik vs AI Branding 共享字符 98.71%
- 对照 `flora-ai-review`：h2=11，开场是 Elena/植物叙事，无 24-H2 骨架

因此：标题可以不同，slug 可以不同，但点进去的正文对搜索引擎等价于「同一篇 production-workflow 扩写稿换皮」。

## Q7 证据

| 指标 | 数值 |
|------|-----:|
| EN published 总量 | 1,314 |
| H2 恰好 24（模板骨架） | 1,300 |
| 正文长度 20.5k–21.1k | 1,300 |
| blocks 约 48–55 | 1,300 |
| 非模板正文（真实内容） | 14 |
| 含 `Template-based tools like Canva*` | 1,304 |
| padded 全集 H2 序列唯一值 | **1** |
| 8 篇抽样去标题相似度 | **~98–99%** |

共享 H2 指纹（24 个全同）：

1. The 6 use cases and their real timelines
2. The benchmark data from 142 campaigns
3. The decision framework for tool selection
4. …（中间同序）
5. The ROI calculation for switching tools
6. Related Resources

首段几乎都是同一段 Canva/Adobe Express 工具分类开场；标题/首 H1 被替换，正文骨架不变。这是典型的 **blog-padded-junk** 扩写产物，不是「各写各的长文」。

### 仅有的 14 篇真实正文（勿动）

含 `ai-design-2027-predictions`、`flora-ai-review`、`artlist-ai-review`、`hallucination-tax-agencies-fear-generative-ai`、`ai-magazine-design-guide` 等近期重写稿。

## 标题审计（Q8）

| 维度 | 数量 | 说明 |
|------|-----:|------|
| EN title `<30` | 41 | 不算灾难性短 |
| EN title `<40` 且无 `:`/`—`/`?` | 152 | **slug 标题**，列表页观感差 |
| EN `seo.title` 缺失 | 349 | 另一条污染线 |
| EN `seo.title` 形如 `X \| Lovart` 且短 | 476 | 关键词壳 |
| ZH title 空 | 1 | `what-is-civitai-red` |
| ZH title `<12` 字 | 9 | 偏短但中文场景可接受一部分 |

跨语言 title`<30`：zh 563 / ko 93 / ja 112 偏高，但中日韩字符密度不同，**不能与 EN 用同一阈值**；本次优先修 EN slug 标题。

## GSC 分层重写队列（Q7 执行顺序）

GSC 窗口：2026-05-21 ~ 2026-06-08（`blog-pages-gsc.json`）。

| Tier | 条件 | 篇数 | 动作 |
|------|------|-----:|------|
| T1 | impressions≥1000 且排名 4–20 | 46 unique | **立刻人工/column-writer 重写** |
| T2 | impressions≥500 | 35 | 本周重写 |
| T3 | impressions≥100 | 156 | 排期重写 |
| T4 | 有 GSC 但低信号 | 373 | 降权或 noindex 候选 |
| T5 | 无 GSC 命中 | 688 | 批量降权/合并，不先重写 |

T1 头部（高曝光首页机会）：

- `freepik-ai-image-generator-review` — 113k imp / pos 7.4
- `hedra-ai-review` — 25k / 6.7
- `ai-art-copyright-2026` — 18k / 7.3
- `complete-guide-consistent-ai-character-design` — 11k / 8.6
- `ai-branding-design` — 10k imp / **274 clicks** / pos 11.3
- `runway-alternatives` — 9.3k / 6.3

## 已备好、未写入的修复

### A. EN 标题模式补丁（66 篇高置信）

规则生成，非整批套同一后缀：

- `Brand Kit X Lovart` → `How to Build a Brand Kit for a/an X with Lovart (2026)`
- `Best AI Agent For X` → `Best AI Design Agent for X: What to Check Before You Switch (2026)`
- `AI Design For X` → `AI Design for X: A Workflow That Survives Real Deadlines (2026)`
- `* Tools Comparison` / `* Guide` / `* Best Practices` → 带场景的完整标题

刻意 **未** 对所有 `Best … 2026` 套同一句 `Ranked by Workflow Fit…`（避免 description 污染重演）。

### B. 产物路径（Local Dev，过程缓存）

- 总审计：`~/Documents/Lovart Local Dev/Output/QA-Memo/en-blog-q7-title-audit-2026-08-03.json`
- 重写队列 CSV：`…/en-blog-body-rewrite-queue-2026-08-03.csv`
- 标题 patch 结果（403）：`…/en-title-patch-result-2026-08-03.json`

## 阻塞（权限诊断，2026-08-03 复核）

不是「token 坏了」，是 **组织角色 ≠ 项目角色**：

- 组织 `oxA3yhI8j`（Lovart）：`sevena@lovart.ai` = **administrator** ✓
- 项目 `o11tm2qe`（lovart.ai）：同一 Google 身份成员 `pGsWkXnou` = **viewer** ✗（`role: read`）
- MCP OAuth 已重授；CLI `/tmp/sanitytoken.txt` 与 MCP 同一身份，mutate 仍 403 `permission "update" required`
- 项目仅 2 个 Administrator 成员：`p40QyCnUw`、`pJqOkjyJg`（均非当前登录身份）

解锁（任选其一）：

1. 打开 [manage.sanity.io](https://www.sanity.io/manage/project/o11tm2qe/members) → 把 `sevena@lovart.ai` 的 **项目角色** 从 Viewer 改为 Administrator/Editor  
2. 或用已有项目 Admin 账号创建 **Editor robot token**，写入 `/tmp/sanitytoken.txt`  
3. 提权后跑：`curl -s -H "Authorization: Bearer $(cat /tmp/sanitytoken.txt)" https://o11tm2qe.api.sanity.io/v2024-01-01/users/me` → `roles` 须含 `administrator` 或 `editor`，不能是 `viewer`

## 修复标准（纠偏）

**禁止**再用规则生成标题/正文灌库（会重演 description/padded-junk）。  
一律按 `lovart-blog-signal-writer`：

| 层级 | 动作 |
|------|------|
| T1/T2（GSC 排名 4–20 + 曝光达标） | **Content Refresh**：信号队列 → 按写作类型重写 EN 长文 → quality gates → `status: ready` → **等人审** → `lovart-sanity-publish` patch |
| T3 | 排期进 `_signal-queue`，同一主链 |
| T4/T5 | 降权 / 合并候选，不伪重写 |
| 标题 | 随正文 refresh 按 frontmatter spec 重写（`seo_title`≤60、`description`≤300），不单独批处理套话 |

字数/结构/术语/内链/封面：严格遵循 `cursor-lovart-blog-system-prompt.md` + `LOVART-BLOG-LOCAL-SPEC.md`；长文走 column-writer lane + cascade。  
主站 Sanity 发布走 `lovart-sanity-publish`（signal-writer 默认终端是 blogs.lovart.ai WP，本批污染在 www Sanity，发布口切换到 Sanity 父入口）。

## 下一步（建议执行序）

1. **项目角色提权**（上面 3 步）——同时解锁同日 632 篇降权 batch  
2. 建 `_signal-queue`：先吃 T1 的 46 篇（Content Refresh）  
3. 按 signal-writer Phase 2–3 逐篇重写到 `status: ready`，停等人审  
4. 授权后再 patch Sanity；preflight 加守卫：`h2==24` + 共享 H2 指纹 → BLOCK

## 根因与时间线（2026-08-03 复查）

### 怎么发生的

不是前端读错，也不是「从来没有独立正文」。多数 EN 在 **2026-07-20 前仍是独立文章**；之后被两轮（中间还有一轮骨架注入）批量 `patch body` 覆盖。

| 时间 (UTC) | 事件 | 证据 |
|------------|------|------|
| 2026-07-17 | 已发现并归档 781 篇「脚本扩字 sludge」 | `MEMORY-PROJECT` + `1-8 Backup/archives/blog-padded-junk-2026-07-17/`（1130 文件）；RULES-20 立 Banned Template-Phrase |
| ~2026-07-21→22 | **第一刀：26-H2「6 use cases」骨架灌入** | Freepik 历史：07-20 仍是 GSC 独立稿（14 H2）；07-22 已变 26 H2 / ~21.7k，含 `The 6 use cases…`；抽样 30/30 在 07-22T18 已带该骨架 |
| 2026-07-24T07 左右 | **第二刀：Canva 开场 + 收成 24 H2** | Freepik：`07-24T07:10:20Z` 起 b1=Canva 模板，h2=24，~20.9k；当日 `_updatedAt` 波次 **258** 篇 |
| 2026-07-24 计划误用 | 薄内容重写计划把 EN `body=54` 当成「完整源」去喂多语言 | `Output/QA-Memo/thin-content-rewrite-plan-2026-07-24.md` — 此时 EN 54 blocks 已是污染稿，污染会向 i18n 扩散 |
| 2026-07-30T07 左右 | **第三刀：同模板再覆盖大批** | `_updatedAt` 波次 **1,042** 篇落到现行 24-H2 Canva 近重复稿 |
| 2026-07-28→31 | 仅 14 篇被 column/review 真重写保住 | `flora-ai-review` 等 |

机制定性：扩字/「补厚度」类批量 mutate，用同一 production-workflow 大纲（含错误 MCoT 释义 `Multi-Chain of Thought`）覆盖 `body`；标题多半保留，所以列表页看不出正文已死。

### 还能不能挽回

**能。优先用 Sanity Document History，不要从 junk 归档回滚。**

| 恢复源 | 可用性 | 说明 |
|--------|--------|------|
| **Sanity History `?time=`** | ✅ 主路径 | 抽样 30/30 在 `2026-07-20T00:00:00Z` 仍为独立正文；History 可回溯到至少 2026-05 |
| 建议恢复锚点 | `2026-07-20T00:00:00Z`（或每篇「最后一次无 `The 6 use cases` / 无 Canva 开场」的 revision） | 07-22 起多数已带骨架，不宜用 07-23/07-29 |
| 本地 `1-8 Backup/archives/2026-07-17-published-drafts/` | ✅ 辅路径 | 458 篇独立 rewrite；与当前 padded slug 重叠约 **338** |
| `blog-padded-junk-2026-07-17/` | ❌ 不要当原文 | 那是 07-17 已判定的 sludge（~750 slug 重叠），质量更差 |
| `Backup/mflow-published-2026-08-01` | ❌ 太晚 | 08-01 备份晚于覆盖，本地 md 也未带这套 24-H2 指纹 |

恢复原则：

1. **先 freeze**：禁止再对 EN blog 跑任何 expand/pad/「补字数」脚本  
2. **按 History 批量 dry-run restore** 到 07-20（或逐篇 last-good）→ 抽检 H2 多样性 + 无 Canva 开场  
3. 338 篇可与 `2026-07-17-published-drafts` 交叉校验  
4. History 为空/本来就薄的少数篇 → 再走 `lovart-blog-signal-writer` Content Refresh  
5. 恢复后立刻加 preflight：命中共享 24-H2 指纹或 Canva 开场句 → BLOCK

## 💡 洞察

- 问题：字段看起来「有内容」，前端列表/详情都正常渲染，但 99% EN blog 对搜索引擎是同一篇文章换标题。
- 根源：07-17 刚禁掉一类扩字 sludge 后，07-21~30 又用另一套 26→24 H2 production-workflow 模板批量覆盖；07-24 薄内容计划还误把已污染的 EN body=54 当翻译源。
- 缓解：Sanity History 回滚到 07-20 可大批挽回 → 再对缺口走 signal-writer；停掉一切规则灌正文。
