---
name: lovart-router
description: |
  State-aware profile router — given (stage, scenario) returns (profile_target,
  skills_to_load, next_action). Solves "I'm in profile X but should I be in Y?"
  decisions and prevents skill-bloat by routing instead of duplicating.
  Pair with lovart-pipeline-state: every session starts with `router decide`.
disable-model-invocation: false
---

# lovart-router — state-aware profile router (v1.0)

> **Why this exists**: 6 个 Profile 各管一段,但现实任务是横切的——创作撞 QA bug、
> 发布撞 BLOCK、QA 撞 i18n 缺陷。每个 profile 装所有相关 skill → token 爆炸;装太少
> → 撞到边界时在错的位置硬处理 → profile 污染。
>
> 这个 skill 把"该去哪个 profile / 装哪些 skill"做成**单点决策表**,任何档案的
> 会话开头第一步:`router decide` → 立刻知道下一步该做什么 / 该跳到哪个档案。

## When this skill loads

加载条件:
- **任意** Lovart 会话开头(skill 极轻,几十行决策表)
- 不撞具体 stage——但凡用到 pipeline-state 的会话都该先 `router decide`

不加载:
- 用户问一次性事实问题
- 报告类(月报 / 周报 / Sentinel)
- 项目管理类(Pipeline / Cron 配置)——这些用 `lovart-management` 自带的决策即可

## Commands (6 个)

| subcommand | 用途 | 调用者 |
|------------|------|--------|
| `decide` | **核心命令**:给定状态 + 上下文 → 返回"该去哪个 profile + 装哪些 skill" | 任意会话开头必跑 |
| `matrix` | 打印完整决策表(23 个决策) | 排查 / 文档化时 |
| `profile <name>` | 查单个 profile 详情 | 切换 profile 前 |
| `profiles` | 列全部 6 个 active profile | onboarding / 文档化 |
| `validate` | 校验决策表完整性(orphan stage / 未知 action / 未知 profile) | 修改决策表后 |

## Profile registry (6 个 active)

| profile | work_line | 拥有的 stage | 关键 skill 数 |
|---------|-----------|-------------|--------------|
| `lovart-reports` | S1-data + S6-monitor | S0-todo | 4 |
| `lovart-creation` | S3-content-production | S3-creating, S3-draft, S3-done | 5 |
| `lovart-quality` | S4-review | S4-qa, S4-fix, S4-ready | 4 |
| `lovart-ops` | S5-publish | S5-importing, S5-published, S6-monitoring | 3 |
| `lovart-distribution` | S5b-distribute | (无,操作已发布内容) | 2 |
| `lovart-management` | M0-meta | (无) | 4 |

## Decision matrix (23 个)

```
stage            scenario                     profile                action
S0-todo          default                      lovart-creation        upsert
S0-todo          from_sentinel                lovart-creation        upsert
S3-creating      default                      lovart-creation        execute_skill
S3-draft         default                      lovart-creation        run_hook_and_advance
S3-draft         l1_fluff                     lovart-quality         reroute      ← 你最痛的!
S3-draft         word_count_low               lovart-creation        execute_skill
S3-draft         missing_dates                lovart-creation        patch_artifact
S3-draft         i18n_translation_needed      lovart-creation        execute_skill
S3-done          default                      lovart-creation        advance_only
S4-qa            default                      lovart-quality         execute_skill
S4-fix           default                      lovart-creation        reroute      ← 修复回路
S4-fix           i18n_audit_fail              lovart-creation        reroute
S4-ready         default                      lovart-quality         advance_only
S5-importing     default                      lovart-ops             execute_skill
S5-importing     preflight_fail               lovart-quality         reroute      ← 你最痛的!
S5-importing     sanity_id_exists             lovart-ops             execute_skill
S5-published     default                      lovart-ops             execute_skill
S5-published     needs_distribution           lovart-distribution    reroute
S6-monitoring    default                      lovart-reports         execute_skill
S6-monitoring    ranking_drop                 lovart-creation        execute_skill
ANY              user_asks_state              current                info_only
ANY              user_asks_skill_list         current                info_only
ANY              calendar_oversubscribed      lovart-management      reroute
```

## Typical session flow

### 任意会话开头
```bash
python3 lovart-router/router.py decide
# → 输出: profile_target + skills_to_load + next_action
```

例:
```text
[decide] id=blog-firefly-2026-07  stage=S3-draft  scenario=l1_fluff
  → profile: lovart-quality
  → action:  reroute
  → skills:  lovart-anti-slop
  → reason:  L1 fluff → quality profile specializes in slop detection
```

→ 立刻 `hermes -p lovart-quality`(自动重启) → 该 profile 装的就是 anti-slop → 修 → patch state → 关闭

### 撞到跨档案场景时的"立即路由"
```bash
# 在 lovart-creation 跑着,撞到 L1 fluff
python3 router.py decide --id blog-firefly-2026-07 --from-context "L1 fluff in section 3"
# → 建议跳到 lovart-quality
```

### 修改决策表后校验
```bash
python3 router.py validate
# OK — 23 decisions across 11 stages, 6 profiles
```

## Integration with profile瘦身

下一步改造(在 todo 第 4 步里):
- 把每个 profile 的 SOUL.md 缩短到 80-120 行(只装路由表 + 自身定位)
- 把"我装哪些 skill"改成由 `router decide` 动态决定
- 3 个冗余 profile(`content-gen-lovart` / `qa-of-lovart` / `seo-opt-lovart`)合并掉

## Safety / anti-patterns

- **不要**绕过 `decide` 直接装 skill——这等于回到"靠 agent 自觉"
- **不要**给 profile 加 skill 解决跨档问题——先查 `router.py decide` 是否能路由
- **不要**改决策表不跑 `validate`——orphan stage 会导致静默 fallback
- **不要**给 `info_only` 加 skill——这是常见 over-engineering(用户问状态不需要装 24 个 skill)

## File map

```
1-1 Harness/Skills/06-orchestrate/lovart-router/
├── SKILL.md              ← 本文件
├── router.py             ← 6 subcommand CLI + 23 decisions + 6 profiles
└── tests/smoketest.sh    ← 24 个 router 测试 (TBD)
```

## Related skills

- `lovart-pipeline-state` — router 的输入(state stage 来自它)
- `lovart-content-quality-gates` — `l1_fluff` 触发后真正执行
- `lovart-sanity-publish` — `S5-importing` 触发后真正执行
- `lovart-content-creation-orchestrator` — 改写后直接调 `router decide` 作为 step 1
