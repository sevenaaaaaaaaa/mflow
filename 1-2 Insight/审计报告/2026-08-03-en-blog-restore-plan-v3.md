# EN Blog 正文恢复计划 v3 — 2026-08-03

> 综合：Q7 污染复查 + 恢复源质量审计 + 重叠 338 打标 + history_only 955 全量质检  
> 写作/发布标准：`lovart-blog-signal-writer` → 质检 → `status: ready` → 人审 → `lovart-sanity-publish`  
> 清单 SSOT：  
> - `Output/QA-Memo/en-history-only-quality-audit-2026-08-03.csv`  
> - `Output/QA-Memo/en-overlap-restore-tags-2026-08-03.csv`

---

## 一、一句话策略

**先把能救的正文从 History/Local 捞回来（只改 body），再按 GSC 对弱稿/空壳走 signal-writer 真重写；SEO 字段尽量留在当前 production，不整文档时光倒流。**

---

## 二、库存总览（以 2026-08-03 审计为准）

| 池 | 数量 | 说明 |
|----|-----:|------|
| EN 当前 24-H2 污染正文 | ~1,300 | 待处置总量 |
| 已是独立正文（勿动） | 14 | flora / artlist 等近期真重写 |
| history_only（无本地 draft） | **955** | 已全量质检 |
| overlap（有本地 07-17 draft） | **338** | 已全量打标 |
| 合计核对 | 955+338≈1,293 | 与 ~1,300 量级一致（计数时点略差） |

### 2.1 history_only 955

| 标签 | 数量 | 计划动作 |
|------|-----:|----------|
| HISTORY_OK | 302 | Phase A 恢复 body |
| HISTORY_OK_SCRUB | 2 | Phase A 恢复 + 轻清洗 |
| HISTORY_OK_WEAK | 620 | Phase B 恢复 body → 标 refresh |
| HIST_THIN | 12 | Phase D 重写（高 GSC 可先暂恢复再重写） |
| HIST_EMPTY | 19 | Phase D 重写 |
| 07-20 已是现行污染骨架 | 0 | — |

### 2.2 overlap 338

| 标签 | 数量 | 计划动作 |
|------|-----:|----------|
| BOTH_FULL | 21 | Phase C：Local 清洗后导入（字数优势） |
| LOCAL_FULL | 11 | Phase C：Local 清洗后导入 |
| HISTORY_OK | 2 | Phase A 一并恢复 |
| REWRITE | 304 | Phase D 重写 |

### 2.3 合并后的执行桶

| 执行桶 | 约数 | 来源 |
|--------|-----:|------|
| **A 可恢复（强）** | **~306** | hist OK 302+2 scrub + overlap HISTORY_OK 2 |
| **B 可恢复（弱→refresh）** | **~620** | HISTORY_OK_WEAK |
| **C Local 清洗导入** | **~32** | BOTH_FULL 21 + LOCAL_FULL 11 |
| **D 必须重写** | **~335** | overlap REWRITE 304 + hist EMPTY/THIN 31 |
| **Z 已健康** | **14** | 跳过 |

---

## 三、铁律（全阶段）

1. **只 patch `body`**（必要时 cover）；**保留**当前 `title` / `description` / `seo.*`（description 污染已基本清过，History SEO 更脏）。
2. **禁止**从 `blog-padded-junk-2026-07-17` 恢复。
3. **禁止**整文档回滚到 07-20。
4. **禁止**再跑任何 expand/pad/「补字数」灌库脚本。
5. 恢复稿若命中共享 24-H2 指纹或 Canva 开场句 → **BLOCK**，不得 publish。
6. 真重写一律走 `lovart-blog-signal-writer` + 分类子 skill → quality gates → `ready` → **人审授权**后再 `lovart-sanity-publish`。
7. Blog 日期双写纪律不变；本计划默认不改 `releaseDate`/`publishedAt`（除非另开降权任务）。

---

## 四、分阶段计划

### Phase 0 — Freeze & 工具就绪（0.5 天）

- [ ] 确认写权限仍为 Administrator（`users/me`）
- [ ] 冻结 EN blog 批量 mutate（除本计划脚本）
- [ ] 准备脚本：
  - `restore_body_from_history.py`（锚点 `2026-07-20T00:00:00Z`，dry-run/apply，batch≤20）
  - `import_local_scrubbed.py`（剥 scaffold、verified 内链过滤）
  - preflight 守卫：共享 H2 指纹 / Canva 开场 → BLOCK
- [ ] 备份：restore 前把目标 `_id` 当前 body 摘要写入 `Output/QA-Memo/restore-backup-{date}/`

**出门标准**：dry-run 探针 5 篇成功；权限非 Viewer。

---

### Phase A — 强恢复（~306 篇）优先

**对象**：history_only `HISTORY_OK`+`SCRUB` + overlap `HISTORY_OK`  
**动作**：History@07-20 → `set body`；SCRUB 2 篇顺带去坏链  
**顺序**：按 GSC impressions 降序（Hedra、copyright、character-design guide…）

| 步 | 操作 |
|----|------|
| A1 | dry-run 50 篇：确认非空、非 padded、词数≥1800 |
| A2 | apply 50 → 抽 10 篇人工打开对比标题/首段/H2 |
| A3 | 余量分批 apply（每批 50，间隔观察 CDN/API） |
| A4 | 跑指纹扫描：24-H2 命中应为 1300−已恢复数 |

**出门标准**：A 桶 100% 已恢复；抽检 0 篇 Canva 开场；SEO 字段未被覆盖。

---

### Phase B — 弱恢复 + Refresh 队列（~620 篇）

**对象**：`HISTORY_OK_WEAK`（900–1799 词）  
**动作**：同样只恢复 body，恢复后写入 refresh 队列（不是终态）

| 步 | 操作 |
|----|------|
| B1 | dry-run 30 → apply 全量弱恢复（去掉污染壳，先止损重复内容） |
| B2 | 生成 `_signal-queue-en-q7-refresh-weak.md`：按 GSC 分 T1/T2/T3 |
| B3 | T1（曝光≥1000 或点击≥10）优先 signal-writer Content Refresh |

**出门标准**：弱稿不再是 24-H2 克隆；T1 弱稿进入写作队列而非沉睡。

---

### Phase C — Local 完整稿清洗导入（~32 篇）

**对象**：`BOTH_FULL` 21 + `LOCAL_FULL` 11  
**源**：`1-8 Backup/archives/2026-07-17-published-drafts/`  
**动作**：

1. 去掉文末 Internal Links / Image Appendix / E-E-A-T 脚手架表  
2. `/blog/{slug}` 仅保留 verified 列表；高频坏链（如 `magnific-vs-lovart-comparison`）替换或删除  
3. md → Portable Text（`md_to_portable_text`）→ preflight BLOCK=0 → patch body  
4. BOTH_FULL：若 Local 词数显著高于 History（通常 7k vs 1.5–3k）**用 Local**；否则用 History

**出门标准**：32 篇全部无坏 verified 链、无文末 scaffold、词数≥1800（目标 Review/Comparison 向 3600+ 看齐者单独标记）。

---

### Phase D — 必须重写（~335 篇）

**对象**：overlap `REWRITE` 304 + hist `EMPTY` 19 + `THIN` 12  
**动作**：不恢复薄源；按 `lovart-blog-signal-writer` Content Refresh

| 优先级 | 规则 | 处置 |
|--------|------|------|
| D0 | GSC imp≥1000 或 clicks≥10 | 本周开写（column-writer / 对应子 skill） |
| D1 | imp 100–999 | 排期双周 |
| D2 | 无 GSC / 极低 | 可 noindex/降权候选，或低优先级重写 |

THIN 且高 GSC：允许 **先 Phase B 式暂恢复短正文止损**，但必须同周进 D0 队列。

**出门标准**：D0 清单清空或全部 `status: ready` 等人审；禁止用 Local 薄稿充数。

---

### Phase E — SEO 补齐（与正文并行）

当前 padded 池 SEO 并不干净（约 25% 全洁）：缺失 `seo.title`、desc 长度异常等。  
**与 body 恢复解耦**，避免回滚旧 SEO。

- [ ] 补 `seo.title` 缺失  
- [ ] 校正 `seo.description` 至 150–160  
- [ ] 抽查无 GSC intent 模板回流  

---

### Phase F — 门禁固化（防再污染）

- [ ] preflight：共享 24-H2 序列或 Canva 开场 → BLOCK  
- [ ] import 管道禁止无 diff 的「扩字」batch  
- [ ] 周扫：`h2==24 && 指纹命中` 计数告警  

---

## 五、建议日程（可压缩）

| 日序 | 内容 | 产出 |
|------|------|------|
| D0 | Phase 0 + A1 探针 | 脚本 + 5/50 dry-run 报告 |
| D1 | A2–A3 强恢复 | ~306 body 恢复 |
| D2 | B1 弱恢复 | ~620 body 恢复 + refresh 队列 |
| D3 | C 全量 | ~32 Local 清洗导入 |
| D4起 | D0 重写（按 GSC） | 每周固定产能（如 5–10 篇 ready） |
| 并行 | E SEO + F 门禁 | 字段补齐 + BLOCK 规则落地 |

强+弱恢复完成后天数目标：**污染克隆从 ~1300 → 0**（弱稿虽短但已去重）。  
长期质量目标：WEAK/REWRITE 经 signal-writer 升到类型字数 90%+。

---

## 六、风险与回滚

| 风险 | 缓解 |
|------|------|
| History 某篇实际为空/已变 | apply 前逐篇校验 words≥阈值，失败进 D |
| Local 清洗漏坏链 | preflight 扫 `/blog/` ∉ verified ∪ production slug 集 |
| 只恢复 body 导致旧排版怪 | 抽检 Portable Text；表格走项目 string-cells 规范 |
| CDN 列表仍显示旧摘要 | description 未回滚则列表应已是修复后文案；正文 CDN 等候 |
| 误伤 14 篇真稿 | 恢复脚本排除 h2≠24 的 `_id` |

回滚：`restore-backup-{date}/` 中的 body 快照可再 patch 回去。

---

## 七、成功指标

1. `h2==24 && 共享指纹` 计数 = **0**  
2. A+C 桶抽检：无 Canva 开场、无错误 MCoT「Multi-Chain」模板段  
3. D0（高 GSC 重写）按周下降  
4. 不再出现「EN body=54 当翻译源」类误用  

---

## 八、立刻可执行的下一命令（待你授权 apply）

1. 写并跑 `restore_body_from_history.py --tag HISTORY_OK --dry-run --limit 50`  
2. 人审抽检通过后 `--apply`  
3. 同步启动 Phase C 清洗流水线（32 篇）与 Phase D0 队列（从 overlap REWRITE + hist EMPTY 的高 GSC 排序）

---

## 九、相关文档

| 文档 | 用途 |
|------|------|
| `2026-08-03-en-blog-q7-body-title-audit.md` | 污染事实与时间线 |
| `2026-08-03-en-blog-restore-source-quality-audit.md` | History vs Local 谁更好 |
| `2026-08-03-en-blog-overlap-restore-tags.md` | 338 打标 |
| `2026-08-03-en-blog-history-only-quality-audit.md` | 955 质检 |

## 💡 洞察

- 问题：1,300 篇近重复壳要拆，但恢复源质量不均——强恢复只有约 300，弱恢复 620 只能止损，还有约 335 必须真写。  
- 根源：07-21～30 灌库覆盖；本地 draft 大量是空 History 时期的薄稿；SEO 已部分修好故不能整文档回滚。  
- 缓解：分桶 A/B/C/D；先去克隆再补质量；用 signal-writer 吃掉 D 桶高 GSC，而不是第三次规则扩字。
