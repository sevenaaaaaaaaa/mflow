---
session_date: 2026-07-20
session_topic: "归档 qa-of-lovart / seo-opt-lovart + 6 标准 profile SOUL 瘦身"
session_slug: "profile-archive-and-soul-slim"
profiles_used: [profile-lovart-management]
tools_used: [lovart-router, lovart-pipeline-state, sync-profile-skills.sh, dryrun-blog-pipeline]
agents: [hermes]
duration_min: 60
files_changed_count: 11
schema_bumps: 0
status: ready
---

# Context
- 上一轮发现 8 个档案中 3 个("超级档案":content-gen-lovart / qa-of-lovart / seo-opt-lovart)38/39 顶层 skill 完全相同 — 冗余档案
- 6 标准 profile SOUL 仍偏长 (186-232 行) — 规则全量快照塞进 SOUL,浪费 token
- 用户拍板:content-gen-lovart 保留,其他两个归档;然后做 SOUL 瘦身

# Solution
**两步交付**:

第 1 步 - 归档冗余档案:
- `~/.hermes/profiles/qa-of-lovart` → `~/.hermes/profiles/.archive/2026-07-20/qa-of-lovart/` (231M)
- `~/.hermes/profiles/seo-opt-lovart` → `~/.hermes/profiles/.archive/2026-07-20/seo-opt-lovart/` (130M)
- 在归档目录留 REDIRECT.md + 在原 SOUL 位置留 archive notice
- 改 `1-1 Harness/09-scripts/sync-profile-skills.sh`:ACTIVE_PROFILES 从 11 → 9,LAYOUT 删 2 行,头部加归档说明

第 2 步 - 6 标准 profile SOUL 瘦身:
- 每个 SOUL 从 186-232 行 → 55-66 行
- 移除内容:规则全量快照 (RULES-00 + RULES-{10,20,30,40,50,60}) — 改用文件路径引用
- 保留内容:identity / routing 指令 / 拥有 stage / "do this / not this" / project roots 1 行 / hard rules 1 行

# Files Changed
| 路径 | 操作 | 备注 |
|------|------|------|
| `~/.hermes/profiles/.archive/2026-07-20/` | 新建目录 | archive root |
| `~/.hermes/profiles/.archive/2026-07-20/INDEX.md` | add | 归档索引 + 替代方案 + 6 个月保留期说明 |
| `~/.hermes/profiles/.archive/2026-07-20/qa-of-lovart/REDIRECT.md` | add | 归档档案的 redirect stub |
| `~/.hermes/profiles/.archive/2026-07-20/seo-opt-lovart/REDIRECT.md` | add | 同上 |
| `~/.hermes/profiles/.archive/2026-07-20/{qa-of,seo-opt}-lovart/SOUL.md` | modify | 替换为 archive notice (原 SOUL 保留为 SOUL.md.archived-2026-07-20) |
| `~/.hermes/profiles/qa-of-lovart` | mv → archive | 231M |
| `~/.hermes/profiles/seo-opt-lovart` | mv → archive | 130M |
| `1-1 Harness/09-scripts/sync-profile-skills.sh` | modify | ACTIVE_PROFILES 11→9, LAYOUT 删 2 行, 头部归档说明 |
| `~/.hermes/profiles/lovart-creation/SOUL.md` | modify | 191→66 行 |
| `~/.hermes/profiles/lovart-quality/SOUL.md` | modify | 232→59 行 |
| `~/.hermes/profiles/lovart-reports/SOUL.md` | modify | 195→58 行 |
| `~/.hermes/profiles/lovart-ops/SOUL.md` | modify | 186→60 行 |
| `~/.hermes/profiles/lovart-distribution/SOUL.md` | modify | 191→55 行 |
| `~/.hermes/profiles/lovart-management/SOUL.md` | modify | 201→61 行 |
| `1-1 Harness/Skills/06-orchestrate/lovart-router/tests/dryrun-blog-pipeline.py` | modify | 用新 SOUL+skill 数重算 |

# Decisions Made
- D1: 保留 content-gen-lovart (用户指定),归档另外 2 个
- D2: 归档后留 REDIRECT.md + archive notice SOUL (任何工具搜 SOUL 不会拿到误导信息)
- D3: 归档保留 6 个月 (2027-01-20 到期) + 触发清理条件写进 INDEX
- D4: SOUL 瘦身 = 移除规则全量快照,改文件路径引用 — SSOT 仍在 vault
- D5: 6 标准 profile 瘦身后实际 55-66 行(比目标 80-120 还短),保留 routing 指令和 hard rules 一句话

# Patterns Observed
- P1: ACTIVE_PROFILES 数从 11 → 9 (legacy lovart-content/lovart-seo 保留 cron 兼容)
- P2: 6 标准 SOUL 总行数 1196 → 359 (省 837 行 = 69%)
- P3: dryrun-blog-pipeline C 策略 248,600 → 155,800 tokens (-37%) — SOUL 瘦身的连锁效应
- P4: 4 套验证全绿:39 + 16 + 15 smoke tests + 9 profile sync = 79 验证点
- P5: sync-profile-skills.sh 删除 lovart-seo / lovart-reports 各 2 个多余 skill (上一轮 SOUL 引用错位已修正)

# Open Questions
- Q1: SOUL 缩水后是否真有效?需跑一次真实会话对比 token (建议下次 cron dry-run)
- Q2: 是否给 content-gen-lovart 的 SOUL 也做瘦身? (目前 56 行已很短,可不动)
- Q3: archive 6 个月到期后由谁决策清理?lovart-management 自动?还是 user 决定?
- Q4: legacy lovart-content / lovart-seo 何时可以归档? (cron 切换到 lovart-creation 之后)

# Cross-References
- entities: skill-lovart-router, skill-lovart-pipeline-state, profile-content-gen-lovart, profile-lovart-creation, profile-lovart-quality
- decisions: MEMORY-PROJECT.md § 6.6 (上轮) + § 6.7 (本 session)
- skills: lovart-router, lovart-pipeline-state, sync-profile-skills.sh
- verification: 79 tests pass (39+16+15+9 sync)

# Tags
- relevant-tags: #profile-archive #soul-slimming #token-optimization #context-fragmentation #2026-07
