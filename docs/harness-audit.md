# Harness 与红线审计（2026-09-17）

> 目标（用户要求）：提高纯度与可用性、降低噪音；审页面生成 skills/参考样式/故事线/语言规则；
> 给任务加数量限制防灌水；任务拆批次以解决子代理上下文问题。

## 一、体检结果（实测数字）

### 规则（849 行 / 8 文件）
| 文件 | 条款 | 硬条款* | 软建议 | 判断 |
|------|-----:|-------:|------:|------|
| RULES-00-iron | 39 | 17 | 1 | ✅ 核心，密度高 |
| RULES-20-creation | 64 | 19 | 0 | ✅ 最大且有效 |
| RULES-30-quality | 38 | **0** | 0 | ⚠️ 无硬条款（全散文）→ 已由钩子补硬（quota/lang） |
| RULES-10-reports | 5 | **0** | 0 | ⚠️ 条款过少（内容靠正文段落） |
| RULES-50-distribution | 18 | 1 | 0 | ⚠️ 弱 |
| RULES-40-ops | 25 | 6 | 1 | 🟡 |
| RULES-60-management | 13 | 2 | 1 | 🟡 |

\* 硬条款 = 含「禁止/必须/不可/一律/永远/不得」或数字阈值

**结论**：核心（00/20）健康；**语言规则几乎缺失**（仅 00/20/30 各提 1-2 次）；数量限制散落（仅 15/45 skill 提到）。

### Skills（45 个）
- 体量极不均：903 行（ai-self-media-article）/ 697（lovart-better-design）… 32 行（lovart-review）、39（stack-by-stack / best-practice）
- **17 个缺 frontmatter** → Agent 技能检索（P12.2）拿不到描述 → 已修复（补 name+description）
- 数量约束覆盖不足：字数 2 / H2 5 / FAQ 7 / 上限词 5（共 45）

### 故事线 / 参考样式
- 08-storyline 仅 4 文件，其中 `FEATURES-PRODUCTION 2.md` 是 **iCloud 冲突副本**（噪音）→ 已归档 `1-1 Harness/_archive/`
- 参考样式分散在 skills/references 与 Docs/S3-创作，未统一索引（列为遗留）

## 二、本轮修复（已交付）

1. **新增 `RULES-70-quota.md`**：数量限制与防注水（20 条硬规则：字/H2/FAQ/数据点/列表/重复句/过渡词/批量预算）
2. **新增 `RULES-80-language.md`**：10 语言生成规则（脚本族/本地化/分语言细则/多语言一致性/hreflang）
3. **新增钩子 `quota-check.sh`**：字数上限 · H2 ≤7 · FAQ ≤5 · 重复句段 · 连续列表项 · 模板过渡词（≥6 BLOCK）
4. **新增钩子 `lang-check.sh`**：简繁混用 · 日文简体字形 · 中英标点 · 未翻译残留
5. **生成链注入**：`CONTENT_BUDGET` + `LANG_RULES[lang]` 进 gen_prompt；loop/batch/generate 三链统一走 `run_content_gates()`（4 钩子）
6. **任务拆批次**：`batch_size=5` 分批执行 + **上下文摘要传递**（gen/rewrite 用 LLM 生成批次摘要注入下一批；其他类型确定性摘要），解决"子代理没有上下文"
7. **机械清理**：17 个 skill 补 frontmatter；iCloud 冲突副本归档

## 三、遗留（下一轮）

| # | 项 | 说明 |
|---|----|------|
| A1 | RULES-30 补硬条款 | 无硬条款 → 把质量规则改写成可执行钩子条款 |
| A2 | RULES-10/50 瘦身 | 条款稀少但正文长，考虑并入或改写 |
| A3 | 参考样式统一索引 | skills/references 与 Docs/S3-创作 合并入口 |
| A4 | 每个页面生成 skill 加预算段 | 目前只靠全局 RULES-70 注入，skill 内未写预算 |
| A5 | 长文（7500 词）skill 与 quota 冲突处理 | 长文流程需显式豁免 budget（按 skill 覆盖） |
