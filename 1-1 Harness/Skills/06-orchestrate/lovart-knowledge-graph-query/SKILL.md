---
description: 知识图谱查询 skill。查询项目知识与依赖关系。
---
# lovart-knowledge-graph-query

> 任意 Profile / 任意 agent 可用。SSOT 在 `1-1 Harness/11-knowledge/`；
> 数据源 `entities.jsonl` + `relationships.jsonl`（由 `kg-emit-jsonl.py` 从 YAML 生成）。

---

## When this skill loads

加载条件（满足任一即可触发）：

- 用户提问 "X 是什么 / 谁在用 X / X 的依赖 / 反向依赖" 关键词命中
- 工作线是 `lovart-management`
- 用户提到 "改 X skill / 加 cron / 加 profile" 之前需要先看影响面
- 任何 agent 启动 Profile 时如果已加载 `11-knowledge/README.md`，会自动具备此图

不加载：单次问题、不修改代码、单一文档编辑。

---

## Process (always run)

1. **确认 SSOT 已 emit**：若 entity 或 relationship 改动未 emit，
   先跑
   ```
   bash 1-1 Harness/11-knowledge/scripts/kg emit
   ```
2. **选择查询类型**（5 类之一）：
   - lookup by id → `kg id <id>`
   - find neighbors → `kg related-to <id> [--direction both|in|out]`
   - find ancestors chain → `kg ancestors <id>`
   - find within N-hops → `kg start <id> --hop N [--type T]`
   - search by name → `kg find <substr> [--kind K]`
3. **若查询结果是空**：用 `kg find` 或 `kg list --kind <kind>` 检查数据集本身。
4. **若想引链**，把上下游也用 `start` 跑一遍，并在 final 给一个完整图 bbox。
5. **若发现假设失败**（orphan / dangling / 找不到），告诉用户而不是猜。

---

## Output format

永远给出：
- 直接查询结果（路径 + 关系 + 关键 notes）
- 关联相关下游（"X 受谁影响"或"X 影响谁"）1 跳
- 一句总结（人话 + 关键的 ID + 它们应当意味的)

示例：

> Profile `lovart-creation` 直接使用以下 skills（按 S3 顺序）：
> 1. `lovart-blog-signal-writer` (hops 1)
> 2. `lovart-blog-automation` (hops 1)
> 3. `lovart-page-serp-writer` (hops 1)
> ...
> 受影响的下游：6 个 skill 中每个都在 Hermes + Claude + 通常 Cursor 至少有一个副本。改任意一个 skill 前必须先看它的 `mirrors` 边以确认哪些工具需要同步。

---

## Hard rules

1. **SSOT 查询前先 emit**；不直接读 YAML（效率低、容易出错）。
2. **不要改 YAML 来"修正"结果**；除非用户明确要求；如果发现真实 dangling/duplicate，告诉用户。
3. **如果跨工具不一致**（如 A 工具某 skill 已弃用，B 工具仍引用），用 audit 报告路径提报，不要自行"修"。
4. **不允许绕过此 skill 的 GB 跳查询 = 全局搜索**；3 跳 = 邻域饱和，足够了；4+ 通常意味着依赖 entanglement，应转交 lovart-management。
5. **结果中保留 id + 当下命名**，禁止冒充/重命名。

---

## Failure modes (NEVER)

- 用 `grep` 全文扫 vault 找答案（慢，瞎）
- 默认假设 `kg orphan` 是 junk → 不，它是要被记录的实体

---

## Reference

- 数据：`1-1 Harness/11-knowledge/{entities,relationships}.yaml`
- 镜像：`1-1 Harness/11-knowledge/{entities,relationships}.jsonl`
- 查询:`1-1 Harness/11-knowledge/scripts/kg-query.py`
- 别名:`1-1 Harness/11-knowledge/scripts/kg <subcommand>`
- 常用查询速查：`1-1 Harness/11-knowledge/queries/queries.md`
- 同步：`1-1 Harness/11-knowledge/dream/consolidate.sh`（emit + 反推 Hermes 记忆）


## 预算（RULES-70 强制）

本 skill 产出同样受 RULES-70 数量预算约束。

- **必须**过质量门禁（post-write-check + geo-check）
