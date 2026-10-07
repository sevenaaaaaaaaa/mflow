---
name: refresh-page-page-generator
description: 依据 Refresh-Page 项目的故事线与 JSON 模块字典，生成可上线的页面 bodyJson 草稿。用于用户提到 Features/Tools/Product/Scenarios/Solution/Landing、故事线、type 序列、section 组合、落地页生成、页面文案填充时。
disable-model-invocation: true
---

# Refresh Page Page Generator

## 目标

把“对话需求”稳定转换成 Refresh-Page 可落地的页面草稿：

1. 选页面类型（Features / Tools / Product / Scenarios / Solution / Landing）
2. 选故事线 ID（每个分叉/变体都算独立故事线）
3. 产出完整 `type` 顺序
4. 按 `preview-data.json` 字段骨架填文案，生成 `bodyJson`

## 只使用这三份真源

- 页面与故事线：`../../STORYLINE-BY-DIRECTION.md`
- 字段字典：`../../README.md`
- JSON 示例：`../../preview-data.json`

不要引入这三份之外的“自拟编号体系”。

## 对话执行流程（必须按序）

### 第一步：确认 8 个输入

若用户没一次性给全，先补齐：

1. 页面类型（六选一）
2. 故事线 ID（如 `tools-B`、`features-grid-feature`）
3. 页面语言（zh/en）
4. 页面目标（获客、转化、教育、品牌）
5. 目标用户（如 Shopify 商家、设计团队）
6. 行业/品类（如美妆、家居、SaaS）
7. CTA 目标动作（注册、预约、试用）
8. 是否需要“先只出 type 序列，不出完整 JSON”

### 第二步：先回传“故事线确认单”

先返回一段简表让用户确认，再写 JSON：

- 页面类型
- 故事线 ID
- 完整 `type` 顺序
- section 数
- 关键分叉点（如 Tab 布局 A/B、内容簇 A/B、网格位变体）

### 第三步：生成 JSON 草稿

确认后，按以下规则输出：

- 顶层是 `bodyJson` 数组
- 每段必须包含正确 `type`
- 字段名严格来自 `README.md` 与 `preview-data.json`
- 文案与媒体按用户业务改写，不改结构
- 不删除故事线中的固定段位

### 第四步：自检（输出前）

逐项检查：

- `type` 顺序是否与故事线一致
- 每段字段是否存在于组件定义
- CTA 是否和页面目标一致
- FAQ/定价/证言是否按该故事线包含
- 是否误用过时文档（如 FULL-STORYLINE-*）
- 文案是否通过 `../../COPY-PREFLIGHT.md`

## 输出模板

### 模板 A：仅确认故事线

```markdown
页面类型：<type>
故事线 ID：<id>
section 数：<n>

type 顺序：
`type-1 → type-2 → ... → type-n`

分叉说明：
- <分叉点 1>
- <分叉点 2>
```

### 模板 B：输出 bodyJson 草稿

```json
[
  { "type": "hero-split", "...": "..." },
  { "type": "cluster-block-dense", "...": "..." }
]
```

并在 JSON 后附 3 条说明：

- 当前故事线 ID
- 可替换的变体位（如网格位、Tab 位）
- 下一步需要用户补的素材（logo、客户证言、FAQ、媒体 URL）

## 常见用户句式 -> 处理动作

- “给我做一个 Tools 的页面”
  - 先追问故事线 ID（`tools-A/B/tab/grid-*`）
- “先别写 JSON，先让我看结构”
  - 只输出模板 A
- “换成 Tab 的另一种布局”
  - 仅替换 Tab 位并切换到对应故事线 ID
- “把网格换成更规整的”
  - 网格位切到 `feature-grid`，故事线改为对应 `*-grid-feature`

## 强约束

- 每个分叉、每个变体都视作新故事线
- 不把不同故事线混成一条
- 不发明 README 不存在的 `type`
- 不把示例字段改成自定义键名
- 除非用户明确要求，否则先“确认故事线”再“生成 JSON”

