---
description: 管线状态机。12 阶段状态机，原子写，非法转换 exit 2。
---
# lovart-pipeline-state — pipeline state machine (v1.0)

> **Why this exists**: 6 Profile + 6 工作线 × 12 个 skill 的 Lovart 内容工厂里,最
> 大的隐性 bug 是「谁也不知道上一步是谁、下一步给谁」。结果就是:跑完 QA 该生成了、
> 跑完生成该跑 QA,来回扯皮。
>
> 这个 skill 用一个 `pipeline-state.json` + 8 个子命令,把"当前在 S3/S4/S5 哪一步"
> 物理化。每次会话第一步必须 `pipeline_state.py next`,再决定干什么。

## When this skill loads

加载条件：
- 任意 content-producing 会话（Blog / Landing Page / Feature / Tool / Solution /
  Product / Scenario / Topic / i18n 翻译）
- 任意 content-reviewing 会话（QA / preflight / anti-slop / i18n audit）
- 任意 content-publishing 会话（Sanity import / Sitemap / IndexNow）
- 任意 pipeline coordination 会话（orchestrator / management）

不加载:
- 一次性提问（user 问"X 怎么用"）
- 报告类（SEO 周报 / Sentinel / GSC 分析）—— 这些不产内容

## Commands (8 个)

| subcommand | 用途 | 调用者 |
|------------|------|--------|
| `init` | 创建空 state 文件（首次部署） | 一次性 |
| `upsert` | 注册或更新一个 pipeline item | S3 创作前必做 |
| `get` | 看一个 item 详情 | 任意 |
| `list` | 列表（按 phase/stage 过滤） | 任意 |
| `next` | 建议下一个该做的 item | 任意会话开头 |
| `advance` | 把 item 推到下一个 stage | 跨阶段完成时 |
| `run` | 记录 QA 结果 | S4 QA 完成后 |
| `check` | 验证 item 是否准备好进入下一阶段 | 跨阶段前必做 |

`summary` 是第 9 个，但仅用于 dashboard。

## State machine

12 个合法 stage,分 4 个 phase bucket:

```
QUEUE  : S0-todo, S0-skip
CREATE : S3-creating, S3-draft, S3-done, S3-failed
REVIEW : S4-qa, S4-fix, S4-ready, S4-failed
SHIP   : S5-importing, S5-published, S6-monitoring
FINAL  : done, failed, escalated
```

转换规则见 `pipeline_state.py:LEGAL_STAGES` + `TRANSITIONS`。**非法转换 exit 2**。

## Required state file location

默认: `1-3 GenFlow/.pipeline/pipeline-state.json`
（即 vault 根 → Lovart MFlow → 1-3 GenFlow → .pipeline/pipeline-state.json）

用 `--state-path` 可 override。

## Typical session flow

### 创作会话 (lovart-creation)
```bash
# 1) 开 session 先 next
python3 pipeline_state.py next

# 2) 取一个 item,upsert 更新 artifact_path
python3 pipeline_state.py upsert --id blog-firefly-2026-07 \
  --artifact-path "1-3 GenFlow/Blog Pipeline/drafts/firefly.md" \
  --agent lovart-creation \
  --skill lovart-blog-signal-writer

# 3) advance 到 S3-creating
python3 pipeline_state.py advance --id blog-firefly-2026-07 --to S3-creating \
  --reason "starting signal-writer run"

# 4) 写稿中...
python3 pipeline_state.py advance --id blog-firefly-2026-07 --to S3-draft

# 5) 写完
python3 pipeline_state.py advance --id blog-firefly-2026-07 --to S3-done \
  --reason "7500 words, all H2 sections present"
```

### QA 会话 (lovart-quality)
```bash
# 1) 看哪些 S3-done 等 QA
python3 pipeline_state.py list --phase REVIEW

# 2) advance 到 S4-qa
python3 pipeline_state.py advance --id blog-firefly-2026-07 --to S4-qa

# 3) 跑 QA
bash 1-4\ Dev/scripts/hooks/post-write-check.sh --file /path/to/draft.md --target-words 7500

# 4) 记录 QA 结果
python3 pipeline_state.py run --id blog-firefly-2026-07 \
  --qa-result '{"l1_block":0,"l2_block":0,"l7_block":0}'

# 5) 若 fail → S4-fix → 等下轮
python3 pipeline_state.py advance --id blog-firefly-2026-07 --to S4-fix --reason "l1 fluff"
# 若过 → S4-ready
python3 pipeline_state.py advance --id blog-firefly-2026-07 --to S4-ready
```

### 发布会话 (lovart-ops)
```bash
# 1) 看哪些 S4-ready
python3 pipeline_state.py list --phase SHIP

# 2) check 验证
python3 pipeline_state.py check --id blog-firefly-2026-07
bash 1-4\ Dev/scripts/hooks/pre-import-check.sh --id blog-firefly-2026-07 \
  --state-path "1-3 GenFlow/.pipeline/pipeline-state.json" \
  --artifact "1-3 GenFlow/Blog Pipeline/drafts/firefly.md"

# 3) advance 到 S5-importing
python3 pipeline_state.py advance --id blog-firefly-2026-07 --to S5-importing

# 4) import 到 Sanity
sanity dataset import --missing .../blog.ndjson

# 5) advance 到 S5-published（patch publish block 通过 Python 或后续 skill）
python3 pipeline_state.py advance --id blog-firefly-2026-07 --to S5-published
```

## Safety guards

| guard | 触发 | 行为 |
|-------|------|------|
| 非法转换 | transition 不在 TRANSITIONS 表里 | exit 2 + stderr 提示允许的 target |
| fix_count > 3 | 第 4 次 push 到 S4-fix | exit 2（防 Ralph-style fix bleed）；可用 `--force` 覆盖 |
| 上游阶段 BLOCK 未清 | advance 到 S5-importing 但 qa 字段 > 0 | exit 2 |
| ID 格式错 | ID 不匹配 `^[a-z0-9][a-z0-9\-]{2,79}$` | exit 2 |

## Anti-patterns to avoid

- **不要**用本 skill 跟踪「未发布的 brainstorm」—— 这是 content factory 不是 idea bank
- **不要**给同一 slug 重复 upsert——用同一 ID 跟踪，多次 advance
- **不要**手动编辑 `pipeline-state.json`——所有写入走 CLI（保证 atomic write）
- **不要**在没有跑 QA 的情况下 advance 到 S4-ready——`check` 会 exit 1

## File map

```
1-1 Harness/Skills/06-orchestrate/lovart-pipeline-state/
├── SKILL.md              ← 本文件
├── pipeline_state.py     ← CLI（8 个 subcommand）
├── smoketest.sh          ← 39 个测试，验证状态机
└── tests/                ← 真实生产数据下的额外测试（待写）
```

## Related skills

- `lovart-content-quality-gates` —— S4 QA 阶段的执行器（输出 → `run --qa-result`）
- `lovart-sanity-publish` —— S5-importing 后的执行器（输入要求 `pre-import-check` PASS）
- `lovart-sitemap-update` —— S5-published 后的通知器
- `lovart-sentinel` —— S6-monitoring 阶段的反馈源
