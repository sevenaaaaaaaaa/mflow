# 11-knowledge — 知识 / 记忆 / 审计（SSOT）

本目录是知识树、项目记忆、会话日志与一致性审计的单一事实来源（SSOT）。
**生产数据（记忆事实、会话日志、实体图谱）属于本地运行时数据，不入公开仓库。**

## 约定结构

```
11-knowledge/
├── README.md            本文件
├── KNOWLEDGE-TREE.md    知识树索引（可选，本地维护）
├── MEMORY-PROJECT.md    项目记忆事实（Agent 依赖其回答；「记忆审阅」页可更正/标过时）
├── entities.yaml        实体图谱（品牌/站点/目的地）
├── sessions/            会话日志 {YYYY-MM-DD}-{slug}.md（session-log skill 产出）
└── project/             项目 PRD / 迁移说明 / 复盘
```

## 上手

1. 复制 `MEMORY-PROJECT.example.md` 为 `MEMORY-PROJECT.md`，写入你自己的项目事实；
2. 每段 Agent 会话结束前用 session-log skill 归档；
3. 「记忆审阅」页（工作台 → 系统）可以更正事实、标过时，Agent 即时生效。
