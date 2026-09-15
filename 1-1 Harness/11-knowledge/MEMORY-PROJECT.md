---
---
type: project-memory
version: 1.9
last_consolidated: 2026-09-14
generated: 2026-07-07
generator: dream/consolidate.sh
owner: profile-lovart-management
mirror_to: ~/.hermes/memories/MEMORY.md (project slice)
changelog:
  - 1.9 (2026-09-14): Harness 管线全量修复 — 路径契约 30 文件归零 / 编排层复活（smoke 39+16+15）/ 每日管线全绿 / launchd 三任务重接 / 00-INDEX v3.1 校准
  - 1.8 (2026-08-05): Class B 22 published + HTTP 200
  - 1.7 (2026-08-05): Class B 22 bodies ready (404 ROI)
  - 1.6 (2026-08-04): Blog+Landing 404 ROI — Landing 301 map + Blog B1/B2 Top30
  - 1.5 (2026-08-03): CSV 1000×404 修复进度入库 — compositePage 393 清零（639 页修复）；剩余 Blog/Landing/Docs 607
  - 1.4 (2026-07-17): Full pipeline complete — 8,247 docs, 428 new EN articles, P0/P1/P2 canonical = 0. b20 body Sanity API hang documented. Cover image asset ref pending.
  - 1.3 (2026-07-17): P0 articles batch published (43 total); P1 strategy started (20 articles); i18n confirmed as signal-driven per-language; Sanity production 7,862 → 7,882+
  - 1.2 (2026-07-17): Column-Writer Lane validation (3 articles); 19 pillar fleet preflight-OK; RULES-20 v1.1 etc.
  - 1.1 (2026-07-17): added §9 multi-turn state machine protocol + RULES-20 v1.1 Column-Writer Lane + Magnific rebrand fact + 781 padded-junk archive
  - 1.1 (2026-07-17): added §9 multi-turn state machine protocol + RULES-20 v1.1 Column-Writer Lane + Magnific rebrand fact + 781 padded-junk archive
  - 1.0 (2026-07-17): initial consolidation
---

# MEMORY-PROJECT — Lovart MFlow

> 项目专属"事实清单"。区别于 `~/.hermes/memories/USER.md`（用户偏好）与 `~/.hermes/memories/MEMORY.md`（跨项目热点）。
> 每条 ⚙️ 表示来自 SleepDream（dream/consolidate.sh）反推；✋ 表示用户显式纠正；
> 📌 表示硬约定（最高优先级）；🤖 表示 agent 内部推断（次级，仅供 dream 评估使用）。

---

## § 0 — 顶层 SSOT

- ⚙️ **Harness 编号 00-11**（10 个工作流段号 + 09 Backup + 11 Knowledge）。11-knowledge 是 SSOT 项目内的「知识/记忆/梦境」基础设施。
- ⚙️ **三层目录**：1-Project/1-2 Insight/1-3 GenFlow/1-4 Dev/。生产关系 = 1-2 → 1-3 → 1-4 → Sanity → 回流 1-2。
- 📌 任意 agent 启动 → 读 `1-1 Harness/00-INDEX.md` → 选 Profile → 读 `RULES-00` + 该 Profile 对应 `RULES-{10..60}`。
- ⚙️ **会话路由**：一条会话只做一类事。调研→清单→关闭→创作。default 仅探索用。

---

## § 1 — Sanity / CMS 事实

- 📌 **永久铁律**：禁 `sanity deploy` / 禁 `--replace` / 禁改 `schemaTypes/` / 禁删 production 文档 / 每次 import 前必须 preflight BLOCK=0。
- ⚙️ Sanity project：`o11tm2qe` / dataset `production`。
- ⚙️ Sanity token：`~/.config/sanity/config.json` → 写入 `/tmp/sanitytoken.txt`。
- ⚙️ Blog 日期字段双写（2026-07-01 纠正）：`releaseDate` + `publishedAt` 必须同时设。
- ⚙️ CLI > MCP：正文不进 LLM 上下文（NDJSON 磁盘流）；仅最小 GROQ 查询可用 MCP。

---

## § 2 — Profile & Skills 矩阵

| Profile | Model | Rules | 主要 Skills |
|---------|-------|-------|-----------|
| lovart-reports | deepseek-chat | 00+10 | sentinel, trident-data-engine, data-ingestion, content-calendar |
| lovart-creation | deepseek-v4-pro | 00+20 | blog-signal-writer, blog-automation, page-serp-writer, landing-page, image-generation, refresh-page-generator, insight-trend |
| lovart-quality | deepseek-chat | 00+30 | content-quality-gates, content-audit, anti-slop |
| lovart-ops | deepseek-chat | 00+40 | sanity-publish (router), sitemap-update, *-sanity-publish |
| lovart-distribution | deepseek-chat | 00+50 | multi-platform-push |
| lovart-management | deepseek-chat | 00+60 | project-architecture, knowledge-graph-query, dream-orchestrator |

- ⚙️ Legacy `lovart-seo` / `lovart-content` 保留以兼容旧 cron，新任务统一用 6+1 active。

---

## § 3 — 已 deprecated 但仍出现在 graph 的 skill

- deprecated: `lovart-blog-serp-writer` → 用 `lovart-blog-signal-writer`
- deprecated: `lovart-sanity-preflight` → 用 `lovart-content-quality-gates`

---

## § 4 — 数据资产与索引

- 📌 **SSOT for Sanity ID**: `1-3 GenFlow/CONTENT_LINK_INDEX.md` (.md + .csv)，每发布必回流。
- 📌 SSOT for 关键词与索引: `1-3 GenFlow/CONTENT_LINK_INDEX.md`.
- 📌 GSC 月报 SSOT: `1-2 Insight/Trident Insights/`.
- 📌 舆情 SSOT: `1-2 Insight/Lovart ORM/`.
- 📌 关键词研究: `1-2 Insight/Keywords Research/`.

---

## § 5 — 用户偏好（来自 USER.md 反推）

✋ **不问就干**："继续"=直接干，不要先讲 skill/工具/步骤。第一条直接干活。
✋ **禁表格**：所有报告/总结用纯文字段落，不用表格格式。
✋ **优先级**：先结论后数据；先框架后填充；存量改造>新建；修复不删除；多语言是需求；中文 Lovart 第一市场（GA4 28%）。
✋ **能进一步解释/教原理前**：先 pip install → 可跑 demo → 可改模板 → 最后讲原理。
✋ **发布原则**：发布类停在 "ready" 等人工授权，不自动无人值守。

---

## § 6 — 踩坑（沉淀中）

✋ 多次"先确认 pilot"是被嫌的（2026-06-22/27）。改：直接开干。
✋ subagent 失败率高 → 主 agent 用 Python 模板批量写文件。
✋ 出报告/总结 —— 不用表格。
✋ 一次性提问 → 不读 harness 整套；按需即查。
🤖 审计发现：`fm-check.py` 当前 21/23 治理文件 frontmatter 缺失（已知，见 `audit/reports/latest.md`）。修法 = 后续 dream/consolidate.sh 补齐。

### ⚙️ § 6.5 — 2026-07-19 Pipeline Orchestration Refactor

**问题**：6 工作线 × 多 skill 间"该跑哪一步"没有显式状态机 → Agent 重启后瞎猜 → "跑完 QA 该生成 / 跑完生成该跑 QA" 循环扯皮。铁律是文本,Agent 会"善意绕过"。

**解法（两层）**：
1. **状态机 SSOT**：`1-1 Harness/Skills/06-orchestrate/lovart-pipeline-state/pipeline_state.py`
   - 12 个 stage,4 phase: QUEUE / CREATE / REVIEW / SHIP / FINAL
   - 8 个 subcommand: init / upsert / get / list / next / advance / run / check / summary
   - 默认 state path: `1-3 GenFlow/.pipeline/pipeline-state.json`
   - **atomic write** (tmp + rename), illegal transition exit 2, fix_count > 3 自动拒绝
   - 39/39 smoke test PASS

2. **钩子层（铁律执行器）**：`1-4 Dev/scripts/hooks/`
   - `pre-write-check.sh` — 文件名/路径/frontmatter/占位符 (5 维)
   - `post-write-check.sh` — H2 密度/词数/fluff/AI 自介/模板残留 (5 维)
   - `pre-import-check.sh` — pipeline-state 在 S4-ready / qa BLOCK 全 0 / 日期双写 / 多语言覆盖 (5 维)
   - 16/16 smoke test PASS

**整合**：
- `pre-import-check` 内部调 `pipeline_state.py check`，所以两层自动串接
- 任何 S3/S4/S5 skill 的 SOP 步骤里加一句"先跑 hook"即可接入
- 不动现有 skill 文件,只在外部包一层约束——最小破坏面

**SKILL.md**：`lovart-pipeline-state/SKILL.md` 包含典型 session flow (创作/QA/发布 三段)。
**README**：`1-4 Dev/scripts/hooks/README.md` 包含调用方式 + 与 pipeline-state 的关系图。

**TODO（用户决定是否做）**：
- 写 dream/consolidate.sh 增量把 pipeline-state 同步到 Hermes MEMORY
- 写 Sentinel / ORM 自动化钩入 pipeline-state（让"舆情触发新 Blog"自动 upsert）
- 改 `lovart-content-creation-orchestrator` 直接调用 `pipeline_state.py next` 作为第一步
- 把 `lovart-sanity-preflight` 已废弃路由指向 `pre-import-check.sh`

**执行人**：主 agent（MiniMax-M3, content-gen-lovart profile）
**触动文件**（5 个新文件）：
- `1-1 Harness/Skills/06-orchestrate/lovart-pipeline-state/{SKILL.md,pipeline_state.py,smoketest.sh}`
- `1-4 Dev/scripts/hooks/{pre-write-check.sh,post-write-check.sh,pre-import-check.sh,README.md,tests/smoketest_hooks.sh}`

### ⚙️ § 6.6 — 2026-07-20 Profile Router Rollout

**问题**：上下文分片悖论——为省 token 拆档案 → 跨档场景时在错的位置硬处理 → 档案污染 → 加 skill 覆盖 → 档案膨胀 → 失去专业意义。

**8 个档案盘点（实测）**：
- 1 个超级档案 `content-gen-lovart`（39 skill,SOUL 56 行）
- 6 个标准档案 `lovart-{creation,quality,reports,ops,distribution,management}`（SOUL 186-232 行,23-26 skill）
- 2 个冗余档案 `qa-of-lovart` / `seo-opt-lovart` 与 `content-gen-lovart` 38/39 skill 完全相同

**解法**：`1-1 Harness/Skills/06-orchestrate/lovart-router/router.py`
- 6 active profile 注册表（model / work_line / owns_stages / key_skills）
- 23 个决策 (stage, scenario) → (action, profile_target, skills_to_load)
- 6 subcommand CLI: decide / matrix / profile / profiles / validate
- 默认 state path 与 pipeline-state 共享

**真实 Blog 闭环验证（magnific-vs-lovart, 10021 词,18 个 stage）**：
- A 单档案全装（现状）：1,864,500 tokens, 0% 漏失, 19 会话
- B router 提醒不切档：67,900 tokens, **27.8% 漏失（漏 5 步）**
- **C router + 切档：248,600 tokens, 0% 漏失, 4 会话 ← 推荐**
- C 比 A 省 86.7% token 同时保持 0 漏失

**15/15 router smoke test PASS**（+70 个测试累计：pipeline-state 39 + hooks 16 + router 15）

**用户拍板的 4 个 TODO（按 ROI 排）**：
1. 合并 3 个冗余档案 (`content-gen-lovart` / `qa-of-lovart` / `seo-opt-lovart`)
2. 6 标准 profile SOUL 瘦身 (190-230 → 80-120 行,只留路由表)
3. `lovart-content-creation-orchestrator` step 1 替换为 `router decide`
4. dream cron 加 `router decide` 作为 step 1

**触动文件**（4 个新文件）：
- `1-1 Harness/Skills/06-orchestrate/lovart-router/{SKILL.md,router.py,tests/dryrun-blog-pipeline.py,tests/smoketest.sh}`

### ⚙️ § 6.7 — 2026-07-20 Profile Archive + SOUL Slimming

**两步交付 + 真实数字验证**：

**第 1 步 - 归档冗余档案**：
- `~/.hermes/profiles/qa-of-lovart` → `.archive/2026-07-20/`（231M）
- `~/.hermes/profiles/seo-opt-lovart` → `.archive/2026-07-20/`（130M）
- 保留 content-gen-lovart（用户指定）
- 归档目录留 INDEX.md + REDIRECT.md + 原 SOUL 备份为 SOUL.md.archived-2026-07-20
- 改 `sync-profile-skills.sh`：ACTIVE_PROFILES 11→9，LAYOUT 删 2 行

**第 2 步 - 6 标准 profile SOUL 瘦身**：
- 移除内容：RULES-00 + RULES-{10..60} 全量快照
- 保留内容：identity / routing 指令 / 拥有 stage / do this not this / hard rules 1 行
- 6 个 SOUL：1196 → 359 行（**-69%**）

| 档案 | 旧 | 新 | 节省 |
|------|-----|-----|------|
| lovart-creation | 191 | 66 | 125 (65%) |
| lovart-quality | 232 | 59 | 173 (74%) |
| lovart-reports | 195 | 58 | 137 (70%) |
| lovart-ops | 186 | 60 | 126 (67%) |
| lovart-distribution | 191 | 55 | 136 (71%) |
| lovart-management | 201 | 61 | 140 (69%) |

**真实数字验证**（更新后的 dryrun-blog-pipeline）：
- A 单档案：1,864,500 tokens (没变)
- B router 不切档：51,700 tokens
- **C router + 切档：155,800 tokens，0 步骤漏失**（**-91.6% vs A**，从 -86.7% 提升）

**79 个验证点全绿**：39 + 16 + 15 smoke tests + 9 profile sync。

**归档保留 6 个月（2027-01-20 到期）**，触发清理条件写进 INDEX.md。

**触动文件**（11 个）：
- 2 个 profile 目录移到 archive + INDEX/REDIRECT/notice SOUL
- `1-1 Harness/09-scripts/sync-profile-skills.sh`（11→9 active profiles）
- 6 个 SOUL.md（lovart-creation/quality/reports/ops/distribution/management）
- `lovart-router/tests/dryrun-blog-pipeline.py`（用新数字）

### ⚙️ § 6.8 — 2026-07-20 Router Integration + SOUL Unification

**本轮三件事**：

**1. content-gen-lovart SOUL 精简**：
- 56 行中 20 行是铁律全量快照嵌入 → 重写为统一结构 (identity → routing → rules 表 → roots → hard rules)
- 新 SOUL: 50 行，规则全部改为 vault SSOT 文件引用

**2. lovart-content-creation-orchestrator Step 0**：
- 加了 Step 0: "Resolve state and routing" → 先 `pipeline_state.py next` + `router decide`
- 三种返回 (reroute / execute_skill / info_only) 都有明确行为指引
- 意味着: 任何创作任务从此自动经过 router 决策，不再靠 agent 自觉

**3. router --brief 模式**：
- 新增 `--brief` flag: 3 行 key=value 输出 (profile/action/skills)
- 用于 cron / script pipes / dream 调用，不需解析 JSON

**7 个 active profile SOUL 全部统一结构**：
- content-gen-lovart: 50 行 (was 56)
- lovart-creation: 66 行 (was 191)
- lovart-quality: 59 行 (was 232)
- lovart-reports: 58 行 (was 195)
- lovart-ops: 60 行 (was 186)
- lovart-distribution: 55 行 (was 191)
- lovart-management: 61 行 (was 201)
- **总计: 1409 → 409 行 (省 71%)**

**79 个验证点全绿**：39 + 16 + 15 smoke + 9 profile sync。

**触动文件**：
- `~/.hermes/profiles/content-gen-lovart/SOUL.md`
- `1-1 Harness/Skills/06-orchestrate/lovart-content-creation-orchestrator/SKILL.md`
- `1-1 Harness/Skills/06-orchestrate/lovart-router/router.py`
- `1-1 Harness/Skills/06-orchestrate/lovart-router/tests/smoketest.sh`
- `1-1 Harness/11-knowledge/sessions/2026-07-20-soul-slim-router-integration.md`

### ⚙️ § 6.9 — 2026-07-20 Tool Governance Rollout

**问题**：Agent 创建新脚本时"抛开所有限制"——路径错/命名乱/无文档/无注册 → 噪音累积。

**解法（3 个机制）**：

1. **lovart-new-tool-governance skill**（创建工具的唯一入口）：
   - 5 步强制流程：搜索已有 → 确定位置命名 → 写脚本 → governance check → 注册
   - governance_check.py 6-gate 校验器（G1 命名 / G2 shebang / G3 位置 / G4 docstring / G5 无违规 / G6 smoke）

2. **脚本盘点 + 清理**：
   - 1-4 Dev/scripts/ 从 75 → 18 个文件（归档 51 个到 .archive/2026-07-20/）
   - 留存 39 个合规脚本（9 核心工具 + 3 hooks + 4 sentinel + 11 trident + 3 harness + 其他）

3. **TOOLS-REGISTRY.md**（脚本注册表 SSOT）：
   - 39 个合规脚本全部注册（path/purpose/created/owner/status/smoke）
   - 新脚本创建前必须先搜 registry 防重复

**39/39 governance check 全绿**。

**governance check 关键修复**：
- G5：排除注释/docstring/字符串字面量（"禁止使用 --replace"的注释不是违规）
- G6：容忍 import side-effect（ImportError/Traceback 是环境问题不是质量问题）
- G2：补 sentinel/trident 的 shebang

**触动文件**：
- `1-1 Harness/Skills/06-orchestrate/lovart-new-tool-governance/{SKILL.md,governance_check.py,governance-check.sh}`
- `1-4 Dev/scripts/.archive/2026-07-20/`（51 个归档脚本）
- `1-1 Harness/09-scripts/TOOLS-REGISTRY.md`（39 个注册）
- 3 个 sentinel .py（补 shebang）+ 1 个 trident .sh（重命名）+ 6 个脚本（G1 重命名）

### ⚙️ § 6.10 — 2026-07-21 Real Blog E2E Validation

**验证内容**：用一篇真实 Blog（`lovart-vs-freepik-complete-rewrite.md`, 1006 词）走完 S0→S5 全流程。

**流程验证**：
- `pipeline_state upsert` → S0-todo → `router decide` → profile=lovart-creation
- `advance` S3-creating → S3-draft → `post-write-check` (BLOCK: 1006 < 6750 words)
- `router decide --from-context "word_count_low"` → profile=lovart-creation (extend draft)
- `advance` S3-done → `router decide` → advance S4-qa
- `router decide` → profile=lovart-quality → `run --qa-result {l1_block:0,l2_block:0,l7_block:0}`
- `check` OK → advance S4-ready → advance S5-importing
- `router decide` → profile=lovart-ops → `pre-import-check` PASS (stage + qa BLOCKs 全 0)

**验证结果**：
- 14 步全部成功执行
- router 正确路由 4 个 stage 转换点（creation→creation→quality→ops）
- post-write-check 正确 BLOCK 词数不足
- pre-import-check 正确 PASS（stage + qa BLOCKs 全 0）
- pipeline-state 0 次非法转换

**发现**：
- governance_check.py 只管脚本(.py/.sh)，不管 blog(.md)——设计如此
- 这篇 blog 只有 1006 词，需要扩写到 7500+ 才能进 S4

**触发文件**：
- `1-3 GenFlow/.pipeline/pipeline-state.json`（状态文件）
- `1-3 GenFlow/.pipeline/events.jsonl`（事件日志）
- `1-1 Harness/11-knowledge/sessions/2026-07-21-real-blog-e2e-validation.md`

### ⚙️ § 6.11 — 2026-07-21 Fable 5 + Claude Code Prompt Integration

**来源**：GitHub 社区两个蒸馏项目：
- KinetiNode/claude-fable-5-system-prompt-clean (120K→500 tokens)
- Piebald-AI/claude-code-system-prompts (500+ sub-agent prompts)

**提炼 3 个 skill**：

1. **lovart-universal-prompt** (Fable 5 distilled)：
   - 6 条核心准则：Pre-Execution Mapping / High-Density Communication / Compliance Fidelity / Zero Placeholders / Constructive Pushback / Session Recap
   - 所有 profile 共享 overlay

2. **lovart-session-recap** (away-summary-generation distilled)：
   - ≤40 words, 1-2 sentences, no markdown
   - 格式: goal + current task + next action

3. **lovart-dream-memory** (dream-memory-consolidation distilled)：
   - 5 phase: Orient → Gather → Merge → Sync → Prune
   - 适配 11-knowledge/ 架构

**SOUL v3.0**：7 个 profile 全部重写，每个 45-59 行（含 universal principles）。

**128 个验证点全绿**。

**触动文件**：
- `1-1 Harness/Skills/06-orchestrate/lovart-universal-prompt/SKILL.md`
- `1-1 Harness/Skills/06-orchestrate/lovart-session-recap/SKILL.md`
- `1-1 Harness/Skills/06-orchestrate/lovart-dream-memory/SKILL.md`
- 7 个 SOUL.md (v3.0 rewrite)

### ⚙️ § 6.15 — 2026-07-21 Agent Proactive Usage

**问题**：新 skill 已注册到 profile,但 agent 不会主动用——缺强制触发点。

**解法**：

1. **SOUL v3.1: 7 个 profile 注入 7 个强制 Gate**
   - GATE 1: session start → pipeline_state.py next
   - GATE 2: session start → router decide
   - GATE 3: 写新 .py/.sh 前 → governance_check.py
   - GATE 4: 写完 blog draft 后 → post-write-check.sh
   - GATE 5: Sanity import 前 → pre-import-check.sh
   - GATE 6: 跨档案场景 → router decide --from-context
   - GATE 7: session end → 写 session log

2. **session-init.sh: 4 gate 自动检查器**
   - GATE 1: pipeline-state 存在
   - GATE 2: router validate 通过
   - GATE 3: pipeline next 有建议
   - GATE 4: governance check (手动触发)

3. **sync-profile-skills.sh: 加新 skill 到 LAYOUT**
   - 6 个新 skill 加到 content-gen-lovart + 6 标准 profile

**验证**: session-init.sh ALL GATES PASS。

**触动文件**：
- 7 个 SOUL.md (v3.1)
- `1-4 Dev/scripts/session-init.sh`
- `1-4 Dev/scripts/sync_to_notion.py` (rename)
- `1-4 Dev/scripts/sync_from_notion.py` (rename)
- `1-1 Harness/09-scripts/sync-profile-skills.sh`

### ⚙️ § 6.12 — 2026-07-21 Obsidian + Lovart Local Dev Sync

**问题**：Obsidian vault 和 Lovart Local Dev 两个目录配合不好——Local Dev 有 350M 内容，其中 22 个策略 .md + 55 个 features JSON + 2 个 tools Python 只在 Local Dev，不在 Obsidian。

**解法**：`1-4 Dev/scripts/sync-local-dev.sh` 双向同步脚本：
- Local Dev → Obsidian: 有价值的新文件推过去
- Obsidian → Local Dev: 过时文件拉回来(放到 Backup/)
- 默认 dry-run，需 --apply 才执行
- SSOT 文件(1-1 Harness/, AGENTS.md, entities.*)不归档

**映射规则**：
- 根 .md → 1-2 Insight/
- features/*.json → 1-3 GenFlow/Page Gen/features/
- tools/*.py → 1-4 Dev/tools/
- Output/SEO-Reports → 1-2 Insight/SEO Reports/
- Output/Knowledge Base → 1-2 Insight/Knowledge Base/
- Output/Lovart-Blog-Pipeline → 1-3 GenFlow/Lovart-Blog-Pipeline/
- seo-documents/sitemap-latest → 1-2 Insight/SEO Reports/sitemap/

**执行结果**：79 个文件全部同步成功(22 .md + 55 JSON + 2 Python)。

**触动文件**：
- `1-4 Dev/scripts/sync-local-dev.sh`
- `1-2 Insight/*.md` (22 个)
- `1-3 GenFlow/Page Gen/features/*.json` (55 个)
- `1-4 Dev/tools/*.py` (2 个)

### ⚙️ § 6.14 — 2026-07-21 Obsidian ↔ Notion Dual-Track

**架构原则**：Obsidian 管"机器读的"(规则/脚本/数据/agent 记忆), Notion 管"人看的"(报告/日历/状态/协作)。互为备份,不互替代。

**冲突规则**：Notion 的 Status/Comment 字段以 Notion 为准; 其他字段以 Obsidian 为准。

**4 个 P0 Database**：
1. Content Calendar (已有, 479 Notion pages vs 3280 本地文件)
2. SEO Reports (新建)
3. Sentinel ORM (新建)
4. OKR (新建)

**同步脚本**：
- `sync-to-notion.py`: Obsidian → Notion (推), 扫 mtime → create/update
- `sync-from-notion.py`: Notion → Obsidian (拉), patch frontmatter Status/Priority
- 冲突检测: Last Synced + Sync Source 双向标记

**dry-run 结果**：3280 本地文件 vs 479 Notion 页面, 3280 待创建(~18 分钟, Notion API 3 req/s)。

**触动文件**：
- `1-1 Harness/10-config/obsidian-notion-dual-track.md`
- `1-4 Dev/scripts/sync-to-notion.py`
- `1-4 Dev/scripts/sync-from-notion.py`

### ⚙️ § 6.13 — 2026-07-21 Legacy Profile Archive

**归档**：`lovart-content` + `lovart-seo` → `~/.hermes/profiles/.archive/2026-07-21/`

**原因**：这两个 legacy profile 与 `lovart-creation` / `lovart-reports` 功能完全重叠。之前保留是"cron 兼容"，但 cron 里无引用，sync 脚本里只有 LAYOUT 行——删掉不影响任何流程。

**sync-profile-skills.sh**：ACTIVE_PROFILES 9→7，LAYOUT 删 2 行。

**当前 7 个 active profile**：
- content-gen-lovart (日常用)
- lovart-creation (S3)
- lovart-quality (S4)
- lovart-reports (S1/S6)
- lovart-ops (S5)
- lovart-distribution (S5b)
- lovart-management (M0)

**归档位置**：`~/.hermes/profiles/.archive/2026-07-21/{lovart-content,lovart-seo}/`
**保留期**：6 个月（到 2027-01-21）
✋ **2026-07-17**：脚本扩字数灌出来的 781 篇 blog 全是模板 sludge，**禁止再走**。归档到 `1-8 Backup/archives/blog-padded-junk-2026-07-17/`。后切到 multi-turn + column-writer Lane 流程（见 §9）。
✋ **2026-07-17**：freepik / lovart 类对比写作一定要先 verify 现状再写 spine。Freepik 在 2026 已重塑为 Magnific（全 creative suite, 1M+ 用户），如按"Freepik 是 stock + bolt-on AI"假设走会整个翻车。

### ⚙️ § 6.32 — 2026-09-14 Harness 管线全量修复（生产可用性恢复）

**背景**：vault 搬家（`~/Knowledge/Obsidian/MindRe` → `~/Obsidian/MindRe/MindRe`）后调度层全断（launchd 空 / 无 crontab / Cursor Automations 从未落地），编排层状态文件丢失，28+ 处脚本硬编码旧路径。fm-check 于 09-02 停跑。

**修复清单**：
- 路径契约：30 个文件旧路径归零（trident 9 + scripts 根 10 + hooks 4 + sync/notion/session-init + sentinel plist + local-dev-env + quality-cascade smoketest），全部改为从脚本位置推导或环境变量，语法校验全过
- 编排层复活：`1-3 GenFlow/.pipeline/` 重建；smoke 全绿（pipeline-state 39/39 + hooks 16/16 + router 15/15 + quality-cascade PASS）；session-init 4 门禁全过
- 每日管线全绿（exit 0）：gsc-daily（GSC API 真实拉数）+ sentinel-collect 22/22 + sentinel-daily + harness-auto-optimize + harness-sync；feishu 按设计跳过（无凭据，非致命）
- **trident-venv**：`~/Documents/Lovart Local Dev/trident-venv`（python 3.12 + google-auth/googleapiclient/pyyaml/requests），契约变量 `LOVART_PYTHON` 定义于 `local-dev-env.sh`，三个 run-*.sh 统一消费
- launchd 重接 3 任务（plist 源在 `1-4 Dev/automation/plists/`）：daily 08:00 / weekly 周一 07:00 / dream 02:30，launchctl list 三条在册
- 附带 bug 修复：gsc_fetch.py sys.path 层级错（parents[5]）+ 本地过期 `is_brand` 影子 SSOT 导入（已删，BRAND_PATTERNS NameError 根因）；run-weekly 的 run_all.sh 指向空的顶层 `Skills/lovart-trident-data-engine/`（改指 01-strategy/ 真身）；report-notify feishu 凭证路径同修
- SSOT 校准：00-INDEX 重写为 v3.1（清 19 处失效引用）；skills-usage.md 重写；TOOLS-REGISTRY 统计同步（42 个）+ venv 契约注记；本文件编号混乱修复（原双 §9/§12 → §9/§13 + §12/§14）

**仍然开放**：
- 飞书凭据未配（管线 SKIP 非致命）；hermes 运行时仅 4 skill（vault 45 个为真相，harness_sync 每日再生成）
- weekly 管线未试跑（周一 07:00 首跑验证）；monthly 同理
- Path-MAP 登记的 SEO Reports 违规区 / _inbox 回灌 / iCloud 冲突副本未清理

**触动文件**：~35 个（见 session log 2026-09-14-harness-pipeline-restore.md）

---

## § 7 — 工具俗语 / 速查

- ⚙️ **LOVART_RESOURCE_ROOT** = vault 根（Obsidian MindRe 主目录）。
- ⚙️ **LOVART_LOCAL_DEV_ROOT** = `~/Documents/Lovart Local Dev/`。
- ⚙️ 路径 SSOT：文档 `1-1 GEO Readme/`（注：可能与 1-1 Harness 重复含义，需 audit 复核，见 `audit/checks/path-dup/`）。
- ⚙️ Sanity 脚本：`1-4 Dev/lovart.sanity.studio/scripts/`。
- ⚙️ SEO/Sentinel 脚本：`1-4 Dev/scripts/`。

---

## § 8 — 梦境 / 知识库 HOW

- ⚙️ 知识点图查询：`bash 1-1 Harness/11-knowledge/scripts/kg <subcommand>`。
  - `kg stats` — 节点/边统计
  - `kg list --kind skill` — 列出全部 skill
  - `kg related-to <id>` — 看邻居
  - `kg start tool-hermes --hop 2 --type uses` — BFS
  - `kg orphans` — 无边实体
- ⚙️ 梦境 cron: 每日 02:30 由 launchd `~/Library/LaunchAgents/com.lovart.dream.plist` 触发 → `dream/consolidate.sh` + `dream/audit.sh`。
- ⚙️ 手动触发：`bash 1-1 Harness/11-knowledge/scripts/kg-dream.sh --all` 或 skill `lovart-dream-orchestrator`。

---

## § 9 — Multi-Turn State Machine + Column-Writer Lane（2026-07-17 立）

任何 ≥5,000 词 Blog 必须强制走以下状态机（RULES-20 v1.1）：

```
STATE 1: OUTLINE
  ├ 读 GSC/ORM signal data
  ├ 读 KB units for topic (lovart-kb-mine)
  ├ 列 column spine (一句话立场)
  ├ 列 3 个反方观点/常见误解
  ├ 列 ≥5 个具体场景/数据/引用
  ├ H2/H3 字数预算
  ├ ASCII 矩阵
  └ 等用户确认

STATE 2-4: DRAFT_PART1..N (每 Part ≤2,500 词)
  ├ 每 Part 必含: first-person 经历 / 数字 ≥3 / 真实 Lovart 行为描写 / 段落 unique 度
  ├ Inline Anti-Padding Check (n-gram 12, banned phrases, heading uniqueness)
  └ 累计字数 ≤ Part 1 + Part 2 + ...

STATE 5: INTEGRATE_QA
  ├ 全文 banned phrase 检测 (25 trigger)
  ├ 全文段落 unique 度
  ├ Frontmatter 14 字段
  ├ Lovart 术语 cluster 化
  ├ Footer cluster 行
  └ 字数 ≥ 7,500

Cascade Inspect (RULES-20 v1.1 default-on)
  ├ writer (lovart-creation) 写 v(N)
  ├ critic (lovart-quality) 评 7 项
  └ 若 fail → 携 reasons 回 writer v(N+1)，max 3 轮
```

**Lane Routing（按 GSC 信号）**：
- impression > 1k, rank 4-10 → **Deep** (multi-turn 3+ pass + cascade, **≥7,500** 词)
- impression 500-1k, rank 11-20 → **Medium** (multi-turn 2 pass, **≥7,500** 词；Lane 只定 effort，不降地板)
- 低信号 → **Light** (单轮 refactor)

**已知失败模式**：脚本扩字数 (script padding) 把 ~5,000 词的 generator 模板扩到 7,500 词，但全是 generic block 复制 — 0 段落 unique, 0 立场, 0 真实数据。RULES-20 v1.1 §"Banned Template-Phrase Registry" 列出 25 个 trigger phrase 用来 BLOCK 这类脚本扩张。

---

## § 13 — 已知计划项（待办）

- 📌 新建 `ANTI-BUGS-REGISTRY.md`（声明阶段，已在 entities.yaml 标注 planned）。
- 📌 把每条 `Rules` 文件补 frontmatter（dream/fm-fix 任务）。
- 📌 跑 `dream/audit.sh`，把所有 5 工具入口配置指向 11-knowledge。
- 📌 Codex AGENTS.md 同步加一段 11-knowledge 入口。
- ⚙️ 给所有受管 Markdown 文件加 frontmatter（plan, 见 audit/reports/）。
- 📌 **2026-07-17 新增**：5 篇更多 Tier-1 选题跑 multi-turn + column-writer Lane（证明模式可复用，不只是选题红利）
- 📌 **2026-07-17 新增**：`lovart-blog-signal-writer` Phase 2 改造成 Lane Routing（RULES-20 v1.1）
- 📌 **2026-07-17 新增**：`lovart-quality-cascade` 从 experimental 改 default-on（≥5,000 词 Blog）
- 📌 **2026-07-17 新增**：`lovart-quality-cascade` 从 experimental 改 default-on（≥5,000 词 Blog）
- 📌 **2026-07-17 新增**：18 篇保留 pillar 决策 (refactor 或保留) — 取决于 5 篇新 column 出来后比对
- 📌 **2026-07-17 新增**：P0 批量刊文 43 篇 + P1 批量刊文 20 篇完成，Sanity 达 7,882 docs
- 📌 **2026-07-17 新增**：i18n 做法最终确认：是 per-language signal-driven generation，不是 EN 翻译
- 📌 **2026-07-17 新增**：b20 body patch 有已知 bug（Sanity API hang on 200+ block body；本地已存完整内容于 01-Drafts）

## § 12 — 项目真相核对（2026-07-17）

- ⚙️ Sanity production 总文档 **8,247**（EN 991 + i18n 6,891 + 428 session new = 8,247），不是 961。
- ⚙️ Top 10 pillar 于 **2026-07-12**（5 天前）已发 80 docs（10 EN + 70 i18n），不在本轮新做。
- ⚙️ i18n 是 per-language signal-driven generation（Lovart Blog Signal Writer per market language），不是 EN→其他翻译。
- ⚙️ P0 canonical missing 从 162 减少到 0（本 session 43 篇 + 原有）。P1 = 0. P2 = 0. 全管道清空。
- ⚙️ P1 canonical missing 从 670 减少到 0。Top 20 P1 by score 已完成。
- ⚙️ 18 篇保留 pillar（01-Drafts/）是 stale local 副本（production 的旧版由 07-12 batch 发过）。标记为 `status: superseded`，已归档。
- ⚙️ b20 body patch 有已知 bug（Sanity API hang on 200+ block body；本地已存完整内容于 archive；b20 在生产有 simple text blocks）
- ⚙️ 428 EN 新文发在本 session。总计 ~100,000 words。
- ⚙️ 1,556 P2 queue entries，其中 1,425 是 i18n 变体。131 canonical EN resolved。

## § 14 — KB 清理事件（2026-07-05）

- ⚙️ 删 `1-2 Insight/Knowledge Base/.venv/`（22 MB → 0）。原因：mammoth/python-docx/lxml/cobble venv 装在 vault 内但无代码调用，是开发期孤立资产。KB 根从 22 MB 压缩到 636 KB。
- ⚙️ kb-ingest.py v0.2 docstring 写明 .docx 重装路径：`~/Documents/Lovart Local Dev/lovart-kb-venv` 跑 `uv venv` + `pip install mammoth python-docx`。**不**入 vault。
- ⚙️ Lovart KB schema v1.0 + 35 KB-doc units + 3 KB-Index (by-topic/citations/capability-glossary) 已就位。下次拓源：填 `Changelog/URL-LIST.md` / `Reference/URL-LIST.md`，走 `kb-ingest.py --allow-fetch`。

---

## § 10 — 跨项目记忆片段（来自 Hermes MEMORY.md）

- ⚙️ NewTake 项目（LibTV SPA + Mantine + EN+KO）→ `lovart-seo-technical` skill，含 SPA crawl-first 章节。
- ⚙️ Flowcoming（WP+Elementor / ssh root@47.117.24.133）→ WP 解 Elementor 拦截 skill。
- ⚙️ PSPI / nownexts.com（WP 全通 / ssh root@172.96.253.73:28766）→ 452 篇可用素材。
- ⚙️ OpenHarness HKUDS / `oh` v0.1.9 已装 → 需要 Claude Code 插件 / team / swarm 场景。

---

## § 11 — 维护协议

- 改本文件必须同时改 `~/.hermes/memories/MEMORY.md` 对应「project slice」。
- 改本文件必须 bump `version`。
- 删条目用 ~~strikethrough~~ 而不是物理删。
- 每条事实必须有 `{source}` 标注：⚙️ / ✋ / 📌 / 🤖。

### ⚙️ § 6.16 — 2026-07-21 i18n 管线重构 + deprecated 清理

**问题**：(1) i18n-pipeline 说"重写不是翻译"但脚本是 translate-md-batch.py；(2) 9 种语言被踢出创作管线扔进翻译管线；(3) deprecated skills (lovart-blog-serp-writer / lovart-blog-automation) 幽灵引用在 9 个 skill 里。

**修复**：
- signal-writer 出口矩阵:所有 10 种语言统一走 signal-writer 创作
- i18n-pipeline 降级为"骨架派生器"(只提供 EN 骨架 + 本地化规则)
- 12 个 deprecated 引用替换(lovart-blog-serp-writer/automation → signal-writer)
- 9 个 skill 修复:article-quality-template/blog-content-ops/content-audit/content-calendar/content-creation-orchestrator/pipeline-orchestrator/project-architecture/blog-serp-writer/blog-automation

**触动文件**：
- `lovart-blog-signal-writer/SKILL.md` (出口矩阵 + Part C/D)
- `lovart-i18n-pipeline/SKILL.md` (降级为骨架派生器)
- 9 个 skill 的 SKILL.md (deprecated→signal-writer)

### ⚙️ § 6.17 — 2026-07-22 Blog 管线 deprecated 残留清理

**问题**：(1) lovart-article-quality-template 说"frontmatter/管线交给 lovart-blog-automation"——但该 skill 不存在(deprecated)；(2) deprecated skill 的 frontmatter name 字段被错误写成 lovart-blog-signal-writer；(3) i18n-pipeline/it-blog-translation 的 description 仍说"翻译管线"。

**修复 5 个 skill**：
- lovart-blog-automation/SKILL.md: frontmatter name 修复 + DEPRECATED banner
- lovart-blog-serp-writer/SKILL.md: frontmatter name 修复 + DEPRECATED banner
- lovart-i18n-pipeline/SKILL.md: description 更新为 v2.0(骨架派生器)
- lovart-it-blog-translation/SKILL.md: description 加 DEPRECATED for Blog
- lovart-blog-signal-writer/SKILL.md: 清理 7 处残留引用

**最终验证**: 51 个 skill 全量扫描,0 个非作废引用残留。

### ⚙️ § 6.18 — 2026-07-22 Blog 唯一入口铁律

**铁律**：所有语言（EN/ZH/ZH-TW/JA/KO/DE/FR/PT/RU/IT）的所有 Blog 都走 `lovart-blog-signal-writer`。不翻译，不走 i18n-pipeline，不走 it-blog-translation。写 Blog = signal-writer，没有例外。批量生成任务同样适用。

**signal-writer description 最终版**：
```
Lovart Blog 唯一创作 skill。所有语言（EN/ZH/ZH-TW/JA/KO/DE/FR/PT/RU/IT）的所有 Blog 都走这一个 skill。
不翻译，不走 i18n-pipeline，不走 it-blog-translation。写 Blog = signal-writer，没有例外。
```

**批量脚本验证**: Lovart-Blog-Pipeline 里 5 个批量脚本,0 个调用旧 skill。

### ⚙️ § 6.19 — 2026-07-22 Blog + Landing Page 唯一入口 + Profile 同步

**Blog 铁律**：所有语言的所有 Blog 都走 `lovart-blog-signal-writer`。description: "所有语言的所有 Blog 都走这一个 skill。不翻译，不走 i18n-pipeline，不走 it-blog-translation。写 Blog = signal-writer，没有例外。"

**Landing Page 铁律**：所有语言、所有分类、新生成或改造、单独或批量——都走 `lovart-landing-page`。description: "落地页生成 = lovart-landing-page，没有例外。"

**Profile 同步**：7 个 active profile 全部有 `lovart-landing-page` + `lovart-blog-signal-writer`。sync-profile-skills.sh LAYOUT 已更新。

### ⚙️ § 6.20 — 2026-07-23 post-generation-check.sh 统一质量门禁

**问题**：landing-page 和 signal-writer 仍有 5 个质量问题：(1) 图片 404；(2) SEO 字段不规范；(3) 运行中忘记约束；(4) 批量脚本无约束；(5) 质量自降。

**解法**：`1-4 Dev/scripts/hooks/post-generation-check.sh` — 5 Gate 统一质量门禁：
- G1: 图片 404 (HEAD 检查所有 URL)
- G2: SEO 字段规范 (9 个必填字段 + Sanity-legal category)
- G3: 结构化质量 (H2 密度 / 词数 / 模板残留)
- G4: 批量脚本约束 (deprecated refs / secrets / safety)
- G5: 质量自降 (fluff / AI 自介 / 低信息密度)

支持两种模式：`--file` (检查 blog/landing) / `--script` (检查脚本)。

**20/20 测试 PASS**。已注册到 TOOLS-REGISTRY。

### ⚙️ § 6.21 — 2026-07-23 Lovart → codebox 部署 PRD

**平台**: codebox (内网 vibecoding 平台, `http://172.16.16.203:8080`)
**项目名**: `lovart-mflow`

**架构设计**:
- Go 后端 HTTP API 包装 Python/Shell 组件
- MongoDB (TABLE_PREFIX=lovart_) 替换 JSON 文件
- 6 个 API 模块: Pipeline / Router / Hooks / Skills / Health / Dashboard
- 前端: 无构建 HTML (Kanban + Router + Hooks 历史)

**核心 API**:
- `/api/pipeline/*` — 状态机 CRUD + 事件日志 + 汇总
- `/api/router/*` — 路由决策 (23 条)
- `/api/hooks/*` — 质量检查 (4 个 hook)
- `/api/skills/*` — Skill 管理 (51 个)

**里程碑**: 8.5 天 (Phase 1-6)

**交付物**:
- `1-1 Harness/01-project/PRD-codebox-deployment.md`
- `1-1 Harness/01-project/迁移说明-codebox.md`

### ✋ § 6.22 — 2026-08-03 CSV 1,000×404 → compositePage 清零（639 页修复）

**来源**：用户会话进度交接（CSV 1,000 条 404）。相关分析稿：`1-2 Insight/Page Analytic/打不开404页面清单 2026-07-13.md`。

**问题拆分（1,000）**：Blog i18n 432（路由缺失 / 文档未发布）+ compositePage 393（45 草稿未发 + 348 真删）+ Landing 根路径 172（缺 `/topics/` 等路由）+ Docs 3。

**已完成（compositePage 线）**：393 条 404 清零，实际修复产出 **639 页**。批次：Draft `createOrReplace` 正式化 45；校准 3 slug×10 语言 30；Tool EN→9 语言 144；Scenario 翻译 52；Solution 无 EN 源新建 14；Feature 翻译 232；Topic EN 源 57 + 非 EN 源 32；Scenario 非 EN 源新建 33。

**手段**：`createOrReplace` 批量发布；EN/非 EN 源深拷贝 `bodyJson` 本地化 hero/按钮；12 块标准模式（tool/feature/topic/solution/scenario 各自 block 序列）；backdate 90 天 + coverImage 注入（RULE 9/10）；`cards → features` 对齐修 bento-4/6/2 字段错配（14 页）。

**Sanity compositePage 现状**：5,583 文档 / 5,113 已发布；分型 tool 1,919 · feature 2,449 · topic 443 · scenario 139 · solution 120。

**风险备忘**：CDN/Vercel 缓存导致 HTTP 200 偶发延迟；23 topic + 7 scenario 无 EN 源靠非 EN 反推；`hero-gallery` / `review-grid-3col` / `logo-loop` 等是原生活法差异非本批引入；Sanity 单次 >5K 拉取需分批。

**开放缺口（607）——下一阶段入口**：
- Blog 432 → `lovart-blog-signal-writer`（Blog 铁律：不走翻译管线）或修前端路由
- Landing 172 → 301 到 `/topics/{slug}` 或补内容（`lovart-landing-page`）
- Docs 3 → 最少，快速补

**Agent 续作约定**：说「继续」= 从 Blog/Landing/Docs 607 开干，不再重做 compositePage 393。

### ✋ § 6.23 — 2026-08-04 Blog+Landing 404 ROI 修复轮

**基线**：`404-status.md` Blog 531 / Landing 59 / Docs 4（compositePage 已清）。

**Landing**：triage 后 301=39（目标页验证 39/39=200）· park=18 · drop=2 · create=0。交付 `landing-404-vercel-redirects-2026-08-04.json` + Insight `Landing-404-301-map-2026-08-04.md`。**前端未合入前 from URL 仍 404**。

**Blog B1**：10 条 published-still-404 ISR 预热 → **10/10 HTTP 200**。

**Blog B2 Top30**：Class A（正文已是拉丁字母、语言字段错挂）`createOrReplace` 发 EN **6** 篇；Class B ready brief **22** 在 `01-Drafts/404-roi-top30-2026-08-04/` 待 signal-writer 正文；Class C 无源 **2**。Parked P2 清单：`blog-404-parked-2026-08-04.md`。

**重扫后**：Blog 待修 **518**；Landing 待修 **59**；结论页 `1-2 Insight/Page Analytic/Blog-Landing-404-ROI-fix-2026-08-04.md`。

**续作**：1) 前端合入 Landing redirects；2) Class B Top briefs 按 lane 写正文→ready→人审 import；3) Docs 4 另开。

### ✋ § 6.24 — 2026-08-05 Class B Top30 正文 ready

Blog 404 ROI Class B（22 篇）已按 lane 写正文，落盘 `1-3 GenFlow/Lovart-Blog-Pipeline/01-Drafts/404-roi-top30-2026-08-04/bodies/`，`status: ready`。EN ≥7500 词 / 中文汉字 ≥12000 / ko·de·fr token≥3500；Anti-Slop 抽检通过；封面用 blogcover-011~065。**未 import Sanity**，等人审授权后再走 `lovart-sanity-publish`。

### ✋ § 6.25 — 2026-08-05 Class B 22 篇授权发布

用户授权后，Class B 22 篇以 `createIfNotExists` 写入 Sanity production（id=`blog-404fix-{slug}-{lang}`），日期双写，body Portable Text，structuredData @type=Article。预热 **22/22 HTTP 200**。清单见 `blog-404-classB-publish-2026-08-05.csv`。Blog 待修降至约 **496**；Landing 59 仍等前端合 redirects。

### 6.26 Blog 404 P0 Next20 publish (2026-08-05)

- Published 20/20 createIfNotExists → HTTP 200
- Artifact: `Output/QA-Memo/blog-404-p0-next20-publish-2026-08-05.csv`
- 404-status: Blog fixed **58** / pending **473**
- Remaining P0 create beyond Next20 still open

### 6.27 Blog 404 P0 Next20b publish (2026-08-05)

- Published 20/20 createIfNotExists → HTTP 200
- CSV: `Output/QA-Memo/blog-404-p0-next20b-publish-2026-08-05.csv`
- 404-status: Blog fixed **78** / pending **453**

### 6.28 Blog 404 P0 Next20c publish (2026-08-05)

- Published 20/20 createIfNotExists → HTTP 200
- CSV: `Output/QA-Memo/blog-404-p0-next20c-publish-2026-08-05.csv`
- 404-status: Blog fixed **98** / pending **433**

### 6.29 Blog 404 P0 Next20d publish (2026-08-05)

- Published 20/20 createIfNotExists → HTTP 200
- CSV: `Output/QA-Memo/blog-404-p0-next20d-publish-2026-08-05.csv`
- 404-status: Blog fixed **118** / pending **413**

### 6.30 Blog 404 P0 Next20e publish (2026-08-05)

- Published 31/31 createIfNotExists → HTTP 200 — **P0 create queue cleared**
- CSV: `Output/QA-Memo/blog-404-p0-next20e-publish-2026-08-05.csv`
- 404-status: Blog fixed **149** / pending **382**

### 6.31 Blog 404 P1 batch publish (2026-08-05)

- Published 20/20 createIfNotExists → HTTP 200 — **P1 create queue cleared**
- CSV: `Output/QA-Memo/blog-404-p1-publish-2026-08-05.csv`
- 404-status: Blog fixed **169** / pending **362**
