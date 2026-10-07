# genflow — 创作层（本地数据）

内容生产与状态机运行时目录。**生成物、日历、分发队列等属于本地数据，不入公开仓库**。

## 约定结构（管线自动创建）

```
genflow/
├── .pipeline/           12 阶段状态机（pipeline-state.json / events.jsonl）
├── Console-Gen/         工作台生成的草稿（{item_id}.md）
├── Content Calendar/    内容日历（成品文章库）
├── Content Distribution/ 分发队列与站外稿
└── bv-skill-v01/        Better Design 内容方法论（已开源）
```

多项目实例的数据在 `run/projects/{id}/`，本目录为默认项目的兼容路径。
