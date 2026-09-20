---
type: session-log
session_date: 2026-09-20
session_topic: "P2-1 正文编辑器 + 版本 + 改动对照：把阅读器从只读变成工作台，编辑与门禁强绑定"
session_slug: content-editor-p2-1
profiles_used: [profile-lovart-management]
tools_used: [console.py, console.html, test_console_units.py, docs/editor.md]
agents: [cowork]
duration_min: 110
files_changed_count: 6
schema_bumps: 0
status: ready
---

# Context

P2 盘点里排第一的缺口：阅读器**全只读**（`openReader` 25 处调用无一可写，前端 `diff` 出现 0 次），
AI 出稿后人只能「通过 / 打回重跑」，改一个词都要回 Sanity 或重跑 Loop。
而内容团队最高频的动作恰恰是"改两句就能发"。

# Solution

## 后端（console.py）

- `editable_path()` —— **唯一写入闸门**。白名单三处根：`run/projects/*/content`、`run/library`、`1-3 GenFlow`；
  只收 `.md`；拒绝路径穿越。RULES / docs / 报告一律只读（它们是 SSOT 或脚本产物，UI 里改会和生成链打架）。
- `content_snapshot()` —— 写前快照，保留 10 版，落 `run/versions/<路径哈希>/`。
- `content_diff()` —— `difflib.SequenceMatcher` 行级 opcodes，未改动长段折叠成 `gap`。
- `content_save()` —— 快照 → 原子写 → **`run_content_gates` 重跑四门禁** → 结论落 `last-gate.json` → 审计。
- `content_restore()` / `content_text_of()` / `content_gate_state()`。
- 端点：`GET content/raw|versions|diff` + `POST content/save|restore|preview`。
- **发布硬拦**：`_bh_publish_sanity` 读 `content_gate_state`，最近一次人工编辑 BLOCK 的稿子直接抛错。
  没编辑过的稿子无此记录 → 行为与之前完全一致，**零回归**。
- `_bh_rewrite` 回传 `source_path`，批量详情才能给「原稿 vs 新稿」的 diff。

## 前端（console.html）

阅读器重写为 **阅读 / 编辑 / 改动** 三视图 + 工具栏 + 历史版本下拉：
- 编辑态：左 markdown 右实时预览（debounce 400ms）。预览走 `POST /api/content/preview`，
  **与正式渲染同一个 renderer**——否则"编辑时看到的"和"发出去的"会不一样。
- 字数用**词当量**（ASCII 词 + CJK/2），与 `quota-check` 同口径，否则字数骗人。
- 保存后就地渲染四门禁结果（复用 `fmtHook`）；BLOCK 明确说"文件已存，但进不了发布链"。
- diff 视图：`+/-` 行高亮 + 左侧色条 + 折叠 gap + 「恢复这一版」。
- 批量详情改稿条目加「↔ 看改动 / ✎ 编辑」。
- 离开/切视图有 dirty 确认；`⌘/Ctrl+S` 保存。

# Verification（实测）

- 端到端冒烟 14 项全过（隔离 console + 真实 HTTP）：raw/save/versions/diff/跨文件 diff/preview/
  restore/restore 后内容一致/restore 不丢东西 + 三条安全边界（拒绝 ROADMAP、拒绝 RULES、拒绝路径穿越）。
- 发布硬拦双向验证：BLOCK 稿 → 抛「未通过门禁」；改成 ok=True → 不再被本守卫拦。
- 单测 42 → **55**；6/6 GATE PASS。

# 过程中抓到并修掉的 3 个 bug（都是自己引入的）

| # | bug | 怎么暴露的 | 修法 |
|---|-----|-----------|------|
| 1 | **版本号秒级时间戳 → 同秒内快照互相覆盖，版本真的丢** | `test_snapshot_rotation_keeps_n` 期望 10 版，实际 1 版 | 微秒 + 碰撞计数（仍只含数字与短横，restore 的 ts 清洗不受影响） |
| 2 | `editable_path` / `rel_of` 按 `PROJECT` 判边界 | `MFLOW_RUN_DIR` 搬到项目外后合法路径全被判死 | 安全边界改判「在可编辑根之内」；新增容错 `rel_or_abs` |
| 3 | 端点处理器里漏换 `rel_of` → `rel_or_abs` | 冒烟测试 4 项连环失败（raw/versions/restore 校验） | 补上 2 处 |

# Decisions Made

- D1: **编辑必须与门禁绑定**。绕过门禁的编辑入口等于给 RULES 开后门。
- D2: 门禁 BLOCK **不回滚用户的文件**——用户的修改不该被吞；改为「保存但不给发」。
- D3: 发布硬拦只对**有编辑记录**的稿子生效，存量稿零回归。
- D4: 预览必须复用生产 renderer，不自己写个 markdown 渲染器——否则预览会骗人。
- D5: 不做协同编辑 / 文档锁。当前团队规模下后写覆盖先写可接受，真出现冲突再上 mtime 抢锁提示。

# Patterns Observed

- P1: **"某某据此拦截"写在文档里不等于代码里有**。第一版我在注释里写了"发布链据此拦截"，
  实际并没有接——补 `content_gate_state` + `_bh_publish_sanity` 守卫才让这句话成立。
- P2: 时间戳做唯一键必须验证碰撞。秒级、甚至毫秒级，在循环里都会撞。
- P3: 引入 env 可覆盖的路径常量后，**所有基于旧常量做边界判断的地方都要复查**——
  改了 `RUN_DIR` 却没改 `rel_of` 的调用点，就是 bug #2/#3。
- P4: 单测与端到端冒烟抓到的是**不同类**的 bug：单测抓逻辑（版本覆盖），冒烟抓接线（漏换函数）。两个都要跑。

# Open Questions

- Q1: 内容库镜像里改完的稿子，要不要提供「一键推回 Sanity」的快捷入口（目前要走批量发布）？
- Q2: 编辑器要不要支持「只改某个版块」（composite 落地页按 section 编辑），而非整篇 md？
- Q3: 10 版快照是否够？要不要按内容哈希去重（连续保存无改动不占版本位）？

# Cross-References

- decisions: docs/editor.md, docs/p2-plan.md
- related sessions: 2026-09-20-warmup-docs-refresh.md

# Tags

- relevant-tags: #editor #diff #versions #quality-gates #p2 #no-regression
