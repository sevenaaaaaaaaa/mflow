---
type: session-log
session_date: 2026-09-17
session_slug: harness-governance-quota-batch
status: ready
---

# Session Log — Harness 治理（纯度/数量限制/批次上下文/语言规则）

## 用户要求
审所有本地 Harness 与红线提纯降噪；审页面生成 skills/参考样式/故事线/语言规则；**加数量限制防灌水**；**任务拆批次解决子代理上下文**。

## 体检（实测）
- 规则 849 行/8 文件：核心 RULES-00（39 条款/17 硬）+ RULES-20（64/19）健康；**RULES-30 零硬条款**、RULES-10/50 弱；**语言规则几乎缺失**；数量限制仅散落 15/45 skill
- Skills 45 个：体量 903↔32 行；**17 个缺 frontmatter**（Agent 检索拿不到描述）
- 故事线：4 文件含 iCloud 冲突副本（噪音）
- 详见 `docs/harness-audit.md`

## 交付
1. **RULES-70-quota.md**：20 条硬规则（字数/H2/FAQ/数据点/来源/列表/重复句/过渡词/批量预算/自检四问）
2. **RULES-80-language.md**：10 语言规则（脚本族表/通用硬规则/分语言细则/多语言一致性/hreflang）
3. **quota-check.sh**：字数上限 · H2≤7 · FAQ≤5 · 重复句段 · 连续列表项≤12 · 模板过渡词≥6 BLOCK（正例 PASS / 灌水例 BLOCK 3 错 2 警）
4. **lang-check.sh**：简繁混用（zh-TW 混简体 → BLOCK）· 日文简体字形 · 中英标点 · 未翻译残留（实测 2/2 用例正确）
5. **生成链注入**：CONTENT_BUDGET + LANG_RULES[lang] 进 gen_prompt；loop/batch/generate 统一 `run_content_gates()`（4 钩子）
6. **任务拆批次 + 上下文传递**：`batch_size=5` 默认分批；gen/rewrite 批次完成→LLM 生成摘要（含"下批避免"）→注入下一批 prompt（`prior_context`）；其他类型确定性摘要；task.batches/ctx_digest 落盘可见
7. **机械清理**：17 skills 补 frontmatter（45/45 现有描述）；iCloud 冲突副本归档 `_archive/`

## 实测
- 钩子：quota 正例 PASS / 灌水例 BLOCK(3e2w)；lang zh-TW 混简 BLOCK / zh 正常 PASS
- 批次：4 项 → 2 批（batch_size=2），批次摘要生成且含"下批避免"，ctx_digest 累积 277 字符
- 4 项全部：hook=0 geo=0 **quota=0 lang=0** advanced=True（新门禁在真实生成链上生效）
- 测试残留全清（管线 4 + 草稿 4 + 任务 1）

## 踩坑
- `set -o pipefail` 下钩子里 `grep | wc -l` 无匹配即中断（P6 的老坑在 2 个新钩子上重演）→ 统一补 `|| true`。**教训：新写 bash 钩子必须逐个验证"无匹配路径"**

## 遗留（下一轮，已入审计报告）
A1 RULES-30 补硬条款 · A2 RULES-10/50 瘦身 · A3 参考样式统一索引 · A4 各页面生成 skill 内写预算段 · A5 长文 skill 的 budget 豁免机制
