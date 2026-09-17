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

## 三、A1-A5 已完成（2026-09-17 第二轮）

| # | 项 | 结果 |
|---|----|------|
| A1 | RULES-30 补硬条款 | ✅ 重构为 **15 条硬条款**（含阈值/禁止项）+ 机器检查映射（4 钩子同源）+ 参数表 |
| A2 | RULES-10/50 瘦身 | ✅ RULES-10：5 条款 → **10 硬条款** + 参数表；RULES-50：1 硬条款 → **10 硬条款** + 参数表（信息未删，只重排为规则+表） |
| A3 | 参考样式统一索引 | ✅ 新增 `1-1 Harness/03-workflows/REFERENCE-INDEX.md`（故事线/模板/方法论/策略/规则 六类，含维护规则） |
| A4 | 页面生成 skill 加预算段 | ✅ **16 个 skill** 统一加「预算（RULES-70 强制）」段（含交付前必过四钩子） |
| A5 | 长文 budget 豁免 | ✅ `quota-check.sh --profile longform --max-words N`；`budget_profile` 贯通 item/params → prompt+门禁；skill frontmatter 声明（signal-writer / ai-self-media-article 已声明）；RULES-70 §五 三条豁免纪律 |

**附带修复（本轮实测暴露）**：
- 批量生成**内部重试**：门禁不过（尤其 quota 超字数）带反馈重写，最多 3 轮 → 实测 retry-b 2420→2159 字符后通过
- pipeline-state 读改写加全局锁 `PS_LOCK`（12 处调用点走 `ps_run`）——并发批量任务/loop 共用同一状态文件的安全保障
- 参考目录 iCloud 冲突副本 5 个 → 归档 `_archive/icloud-dups-20260917/`
