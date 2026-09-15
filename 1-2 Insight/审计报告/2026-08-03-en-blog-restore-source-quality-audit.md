# EN Blog 恢复源质量审计 — History 07-20 vs 本地 Drafts

> 审计日：2026-08-03  
> 对照标准：`lovart-blog-signal-writer`（字数下限、FAQ、内链 verified、SEO 长度、禁模板句、Anti-Slop）  
> 原始数据：`~/Documents/Lovart Local Dev/Output/QA-Memo/en-restore-source-quality-audit-2026-08-03.json`

## 结论（先读这段）

1. **不能一刀切「全用 History」或「全用本地」。** 两套源服务不同人群。
2. **约 955 篇只有 History、没有本地 draft（history_only）→ 不能默认全是 HISTORY_OK。** 2026-08-03 已做全量质检（见 `2026-08-03-en-blog-history-only-quality-audit.md`）：`HISTORY_OK(+SCRUB) 304` / `WEAK 620` / `EMPTY+THIN 31`；07-20 锚点 **0 篇**已是现行 24-H2 污染骨架。
3. **约 338 篇双源重叠 → 多数不能直接拿本地当正文。** 重叠样本里 ~82% 在 07-20 History **正文为空**（文档尚未存在或仍是空壳），对应本地稿又多为 200–500 词薄稿 → 这类应 **REWRITE**，不是恢复。
4. **双源都有完整正文时（重叠样本仅 6 篇，但是高流量审稿型）→ 本地更长、更接近 signal-writer 字数；History 内链更干净。** 正确做法是：**Local 正文 + 内链清洗**，或 **History 正文先上线、再按 Local 扩写**；不要原样灌 Local。
5. **恢复前必须做重点优化，但优化对象要分桶**——不是 1300 篇统一预处理。
6. **SEO 字段：优先保留当前 production 的 title/description/seo.*** 当前 description 的 GSC 模板污染已基本清掉；History 里的 seo/description 反而更脏（抽样常见 `gsc_intent_template`）。**只回滚 `body`（必要时 cover），不要整文档时光倒流。**

## 数据范围

| 集合 | 数量 | 含义 |
|------|-----:|------|
| 当前 EN padded（24-H2 污染） | 1,289–1,300 | 待恢复池 |
| 本地 `2026-07-17-published-drafts` | 458 | 辅源 |
| 双源重叠 | 338 | 可比对 |
| 仅 History | ~951 | 无本地 draft |
| 深度抽样 | 重叠 40（按 GSC 曝光排序）+ 仅 History 20 | 打分 |

评分维度（0–100）：字数、H2、FAQ、第一人称/翻车、verified 内链、禁词/模板句、SEO 字段、是否已是污染骨架。

## 分桶对比

### A. 仅 History（~951）— 恢复主战场

抽样 20 篇（含 Hedra / Haiper / character-design complete guide 等）：

- 均分 **74.8**；score≥70 占 12/20
- **already_padded = 0**
- **bad verified-links = 0**
- 常见问题不在正文，而在 **历史 SEO**：`gsc_intent_template`（11/20）、`seo_title>60`、seo_desc 长度漂移
- 对照当前 production SEO：description GSC 模板已少见；但 `seo_title` 缺失 341、`seo_desc` 长度异常 688、完全干净仅 **25.5%**

**建议**：`patch body` ← History@07-20；**SEO 留在当前文档**；若当前 seo 仍缺/超长，用规则补，不要回滚旧 seo。

### B. 双源重叠（338）— 必须再拆三层

重叠抽样 40 篇（高曝光优先）暴露严重结构问题：

| 子层 | 抽样占比 | 特征 | 处置 |
|------|--------:|------|------|
| History 空壳（<100 词） | **82%**（33/40） | 07-20 时尚无可用正文；本地多为 186–500 词薄稿 | **REWRITE**（signal-writer），禁止恢复薄 Local |
| History 完整 + Local 薄 | ~2–5% | History 可用 | **History 正文** |
| 双源都完整（≥1000 词） | **15%**（6/40） | 见下表 | **Local 清洗** 或 History 先恢复再扩写 |

外推：338 里大约 **~280 篇要重写**，**~60 篇 History 可救**，其中高价值双完整稿约十几到几十篇（需全量普查确认）。

### C. 双完整稿对照（6 篇高信号样本）

| slug | History | Local | 谁更信号写手 | 谁更少 404/垃圾 |
|------|---------|-------|--------------|-----------------|
| freepik-ai-image-generator-review | 80 分 / 3160 词 / badL=0 | 83 分 / 7583 词 / badL=4 | Local（字数+深度） | History（内链） |
| ai-branding-design | 81 / 1897 / 0 | 76 / 7396 / 4 | 互有胜负 | History |
| runway-alternatives | 73 / 2313 / 0 | 76 / 7651 / 4 | Local | History |
| craiyon-ai-review | 68 / 1623 / 0 | 83 / 7475 / 4 | Local | History |
| ai-poster-prompts-tutorial | 75 / 1511 / 0 | 76 / 7449 / 4 | Local 略胜 | History |
| krea-ai-video-generator-review | 68 / 1632 / 0 | 76 / 7528 / 4 | Local | History |

规律：

- Local rewrite 普遍 **7.4k–7.6k 词**，更接近 Review/Comparison 下限，FAQ 齐全。
- Local 几乎都有 **未进 verified 列表的内链**（高频：`magnific-vs-lovart-comparison`、`lovart-vs-freepik-complete`、`freepik-ai-image-generator-vs-lovart`）。
- Local 常见 **文末 scaffold**（Internal Links / Image Appendix / E-E-A-T 表）——适合本地写作，不该原样进 Sanity Portable Text。
- History 更短，但 **内链干净、无 24-H2 污染、无 Canva 开场**。

## 相对 signal-writer 的符合度

| 要求 | History@07-20（有正文时） | 本地 drafts |
|------|---------------------------|-------------|
| 字数下限（How-To≥1800 / Review≈3600） | 中等；部分审核稿达标，大量不足 | 完整 rewrite 很高；薄 draft 很差 |
| FAQ / 场景块 | 有正文时常见 FAQ | 完整稿好；薄稿只有壳 |
| Verified 内链 | **优** | **差**（抽样 39/40 有坏链） |
| 禁模板 / 污染骨架 | 07-20 锚点未中 24-H2 | 未中 24-H2；但含 production-workflow 等旧扩写气味 |
| SEO title/desc | 历史字段较脏 | frontmatter 较全但仍有长度问题 |
| 头尾垃圾 | 较少 scaffold | 文末表格/附录残留多 |
| 可直接 ready | 少（SEO+字数需补） | **抽样 0 篇**不经清洗可 ready |

## 恢复前要不要重点优化？

**要，而且必须分桶优化；不要「先统一美化再恢复」。**

### 必须做（BLOCK 级，恢复前/恢复时）

1. **只恢复 `body`（+必要 cover）**，保留当前 `title` / `description` / `seo.*`（若当前 description 已清洁）。
2. **拒绝恢复**：Local 词数 <1800 且 History 空壳 → 进 rewrite 队列。
3. **拒绝恢复**：任何源若检出 `The 6 use cases…` 或 Canva 开场句（07-20 抽样为 0，仍要做守卫）。
4. **Local 选用时强制**：
   - 剥离文末 Internal Links / Image Appendix / E-E-A-T 大表（或改成正文内链，不留写作脚手架）
   - 内链改写/删除到 verified 列表；高频坏链 `magnific-vs-lovart-comparison` 等一律替换或去掉
5. **恢复后 preflight**：H2 指纹 ≠ 24 共享列表；无 Canva 开场；抽查内链 slug 存在于 production。

### 应该做（高 ROI，可与恢复同一批）

1. 当前 production SEO 补齐：`seo.title` 缺失 ~341、`seo.description` 长度异常 ~688。
2. 双完整高流量 6+ 篇：优先 **Local 清洗后发布**（字数优势大），不要只退回较短 History。
3. History 恢复稿若 < 类型字数 90%：标记 `needs-refresh`，进 T1/T2 signal-writer，而不是当作最终态。

### 不要做

1. 不要从 `blog-padded-junk-2026-07-17` 恢复。
2. 不要整文档回滚到 07-20（会把已修好的 description 弄脏）。
3. 不要把 Local 薄 programmatic 稿（Brand Kit × N）当「可恢复资产」。

## 推荐执行序

1. **全量普查 338 重叠**：给每篇打标 `HISTORY_OK / LOCAL_FULL / REWRITE`（History@07-20 词数 + Local 词数）。
2. **Phase R1**：history_only（~951）+ overlap/`HISTORY_OK` → 只 patch body；dry-run 50 → 全量。
3. **Phase R2**：overlap/`LOCAL_FULL`（预计数十篇）→ 清洗内链+去 scaffold → convert → patch。
4. **Phase R3**：REWRITE 桶（重叠里大头 + History 也空的）→ `_signal-queue` 按 GSC 排 T1。
5. **Phase R4**：SEO 字段补齐（与正文恢复解耦，可并行）。

## 产物

- 详细打分：`Output/QA-Memo/en-restore-source-quality-audit-2026-08-03.json`
- 策略细化：`Output/QA-Memo/en-restore-strategy-refined-2026-08-03.json`

## 💡 洞察

- 问题：两套「可恢复源」质量不对等；若盲目全量 History，会漏掉 Local 里少数高质量长文；若盲目全量 Local，会把大量薄稿和坏内链灌回 production。
- 根源：07-17 本地 archive 混着完整 rewrite 与 programmatic 薄草稿；07-20 History 对「之后才创建的文档」是空的；SEO 已在污染事件后被部分修好，与正文命运不同步。
- 缓解：分桶恢复 + 只回滚 body + Local 必清洗 + 空壳走 signal-writer；恢复前优化聚焦内链/文末脚手架/SEO 补齐，而不是再写一套扩字脚本。
