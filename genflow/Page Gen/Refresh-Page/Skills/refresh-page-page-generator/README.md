# Refresh-Page 对话生成指南

这个目录提供一个可复用的 Cursor Skill，用于把“自然语言需求”转换为 Refresh-Page 页面草稿。

- Skill 文件：`SKILL.md`
- 适用项目：`Lovart/Refresh-Page`

## 1) 你和 Agent 怎么对话

推荐固定成两阶段：

### 阶段 A：只确认故事线（不出 JSON）

直接复制：

```text
请基于 Refresh-Page 规则，先只给我故事线确认单，不要生成 JSON。
页面类型：<Features/Tools/Product/Scenarios/Solution/Landing>
故事线ID：<例如 tools-B>
语言：<zh/en>
目标：<转化/获客/教育/品牌>
目标用户：<人群>
行业：<品类>
CTA目标：<注册/预约/试用>
```

期望返回：

- 页面类型
- 故事线 ID
- 完整 `type` 顺序
- section 数
- 分叉点说明

### 阶段 B：再生成 bodyJson

确认结构后再发：

```text
按刚才确认的故事线，输出可上线 bodyJson 草稿。
要求：
1) 严格沿用该故事线的 type 顺序
2) 字段名必须来自 README 和 preview-data.json
3) 先用占位文案和占位 media URL
4) 结尾附上“我还需要补充的素材清单”
```

## 2) 高效对话模板（常用）

### 模板 1：直接起一页

```text
帮我起一个 <页面类型> 页面，故事线用 <故事线ID>。
先给我 type 顺序确认单，再等我确认后生成 bodyJson。
业务信息：
- 产品：
- 人群：
- 目标：
- CTA：
```

### 模板 2：只替换一个变体位

```text
在不改其余结构的前提下，把 <Tab位/网格位/内容簇位> 替换成 <目标type>，
并把故事线ID切到对应新线。先返回更新后的完整 type 顺序。
```

### 模板 3：批量比较两条故事线

```text
请对比 <故事线ID-A> 和 <故事线ID-B>：
1) 两条线完整 type 顺序
2) 差异 section
3) 各自更适合的场景
先不生成 JSON。
```

## 3) 建议工作流

1. 用 `STORYLINE-BY-DIRECTION.md` 选故事线 ID
2. 先让 Agent 返回完整 `type` 顺序
3. 你确认后再让 Agent 出 `bodyJson`
4. 最后补素材（logo、证言、FAQ、媒体 URL）并回填

## 4) 质量检查清单（给人用）

在把 JSON 发给前端/上 CMS 前，人工检查：

- 是否完全匹配目标故事线的 `type` 顺序
- 每段字段名是否在 `README.md` 中存在
- 是否把“分叉变体”误合并
- CTA 文案与页面目标是否一致
- FAQ/定价/证言是否符合该故事线

## 5) 相关源文件

- `../../STORYLINE-BY-DIRECTION.md`
- `../../README.md`
- `../../preview-data.json`

> 以上三份是本项目生成页面的唯一依据。

